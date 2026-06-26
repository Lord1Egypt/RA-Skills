#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from email.utils import parseaddr
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openai import OpenAI

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
]


@dataclass
class EmailRecord:
    message_id: str
    thread_id: str
    from_email: str
    from_name: str
    subject: str
    body: str
    internet_message_id: str


def load_gateway_token() -> str:
    cfg_path = Path("~/.openclaw/openclaw.json").expanduser()
    if not cfg_path.exists():
        return ""
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    return cfg.get("gateway", {}).get("auth", {}).get("token", "")


def decode_mime_header(value: str) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def decode_base64url(data: str) -> str:
    if not data:
        return ""
    padded = data + "=" * (-len(data) % 4)
    raw = base64.urlsafe_b64decode(padded.encode("utf-8"))
    return raw.decode("utf-8", errors="ignore")


def html_to_text(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\n\s+\n", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def find_part(payload: dict[str, Any], mime_type: str) -> str:
    if payload.get("mimeType") == mime_type:
        body_data = payload.get("body", {}).get("data", "")
        return decode_base64url(body_data)

    for part in payload.get("parts", []) or []:
        found = find_part(part, mime_type)
        if found:
            return found

    return ""


def extract_email_record(message: dict[str, Any]) -> EmailRecord:
    payload = message.get("payload", {})
    headers = {h.get("name", "").lower(): h.get("value", "") for h in payload.get("headers", [])}
    from_value = decode_mime_header(headers.get("from", ""))
    from_name, from_email = parseaddr(from_value)
    subject = decode_mime_header(headers.get("subject", ""))
    internet_message_id = headers.get("message-id", "")

    plain_body = find_part(payload, "text/plain")
    if plain_body:
        body = plain_body
    else:
        html_body = find_part(payload, "text/html")
        body = html_to_text(html_body)

    if not body:
        body = message.get("snippet", "")

    return EmailRecord(
        message_id=message.get("id", ""),
        thread_id=message.get("threadId", ""),
        from_email=from_email,
        from_name=from_name,
        subject=subject,
        body=body.strip(),
        internet_message_id=internet_message_id,
    )


def build_reply_prompt(record: EmailRecord, agency_profile: str, style_rules: str) -> tuple[str, str]:
    system = (
        "You are an assistant that writes short, personalized sales follow-up emails for a digital marketing agency. "
        "Be professional, warm, and specific. Do not invent facts. "
        "If details are missing, ask one concise clarifying question in the draft. "
        "Return plain text only."
    )

    user = (
        f"Agency profile:\n{agency_profile}\n\n"
        f"Style rules:\n{style_rules}\n\n"
        f"Incoming email metadata:\n"
        f"From Name: {record.from_name or 'Unknown'}\n"
        f"From Email: {record.from_email or 'Unknown'}\n"
        f"Subject: {record.subject or '(no subject)'}\n\n"
        f"Incoming email content:\n{record.body[:12000]}\n\n"
        "Write a personalized follow-up reply as if replying in the same thread. "
        "Include a clear next step and keep it under 180 words unless complexity requires more."
    )

    return system, user


def ensure_label(service: Any, user_id: str, label_name: str) -> str:
    result = service.users().labels().list(userId=user_id).execute()
    for item in result.get("labels", []):
        if item.get("name", "").lower() == label_name.lower():
            return item["id"]

    created = service.users().labels().create(
        userId=user_id,
        body={
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show",
        },
    ).execute()
    return created["id"]


def get_credentials(client_secret_file: Path, token_file: Path, auth_mode: str) -> Credentials:
    creds: Credentials | None = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_file), SCOPES)
        if auth_mode == "console":
            creds = flow.run_local_server(
                port=0,
                open_browser=False,
                authorization_prompt_message="Open this URL to authorize this app:\n{url}",
            )
        else:
            creds = flow.run_local_server(port=0)

    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text(creds.to_json(), encoding="utf-8")
    return creds


def generate_reply_text(client: OpenAI, model: str, record: EmailRecord, agency_profile: str, style_rules: str) -> str:
    system, user = build_reply_prompt(record, agency_profile, style_rules)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
    )
    text = resp.choices[0].message.content or ""
    return text.strip()


def to_reply_subject(subject: str) -> str:
    if not subject:
        return "Re: (no subject)"
    if subject.lower().startswith("re:"):
        return subject
    return f"Re: {subject}"


def create_gmail_draft(service: Any, user_id: str, profile_email: str, record: EmailRecord, reply_text: str) -> str:
    message = MIMEText(reply_text, "plain", "utf-8")
    message["To"] = record.from_email
    message["From"] = profile_email
    message["Subject"] = to_reply_subject(record.subject)
    if record.internet_message_id:
        message["In-Reply-To"] = record.internet_message_id
        message["References"] = record.internet_message_id

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    payload = {
        "message": {
            "raw": raw_message,
            "threadId": record.thread_id,
        }
    }
    draft = service.users().drafts().create(userId=user_id, body=payload).execute()
    return draft.get("id", "")


def process_once(
    service: Any,
    openai_client: OpenAI,
    args: argparse.Namespace,
    user_id: str,
    profile_email: str,
    processed_label_id: str,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "processed": 0,
        "created_drafts": [],
        "skipped": [],
        "errors": [],
    }

    search = service.users().messages().list(
        userId=user_id,
        q=args.query,
        maxResults=args.max_emails,
    ).execute()
    messages = search.get("messages", [])

    for msg in messages:
        message_id = msg.get("id", "")
        try:
            full = service.users().messages().get(userId=user_id, id=message_id, format="full").execute()
            record = extract_email_record(full)

            if not record.from_email:
                out["skipped"].append({"message_id": message_id, "reason": "missing_sender"})
                continue

            if record.from_email.lower() == profile_email.lower():
                out["skipped"].append({"message_id": message_id, "reason": "sender_is_self"})
                continue

            reply_text = generate_reply_text(
                client=openai_client,
                model=args.openai_model,
                record=record,
                agency_profile=args.agency_profile,
                style_rules=args.style_rules,
            )

            draft_id = create_gmail_draft(
                service=service,
                user_id=user_id,
                profile_email=profile_email,
                record=record,
                reply_text=reply_text,
            )

            out["created_drafts"].append(
                {
                    "message_id": record.message_id,
                    "thread_id": record.thread_id,
                    "from": record.from_email,
                    "subject": record.subject,
                    "draft_id": draft_id,
                }
            )
            out["processed"] += 1

            labels_to_add = [processed_label_id]
            labels_to_remove: list[str] = []
            if args.mark_read:
                labels_to_remove.append("UNREAD")

            service.users().messages().modify(
                userId=user_id,
                id=message_id,
                body={
                    "addLabelIds": labels_to_add,
                    "removeLabelIds": labels_to_remove,
                },
            ).execute()

        except Exception as exc:
            out["errors"].append({"message_id": message_id, "error": str(exc)})

    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read Gmail, generate AI reply, save as Gmail drafts.")
    parser.add_argument("--gmail-user-id", default="me")
    parser.add_argument("--query", default="in:inbox is:unread -from:me -label:openclaw_auto_drafted")
    parser.add_argument("--query-file", default="")
    parser.add_argument("--max-emails", type=int, default=5)
    parser.add_argument("--poll-interval", type=int, default=0)
    parser.add_argument("--mark-read", action="store_true")
    parser.add_argument("--processed-label", default="openclaw_auto_drafted")

    parser.add_argument(
        "--client-secret-file",
        default=os.environ.get("GOOGLE_CLIENT_SECRET_FILE", "~/.config/gmail-auto-draft/google-client-secret.json"),
    )
    parser.add_argument(
        "--token-file",
        default=os.environ.get("GMAIL_TOKEN_FILE", "~/.config/gmail-auto-draft/token.json"),
    )
    parser.add_argument("--auth-mode", choices=["local", "console"], default="local")

    parser.add_argument("--openai-model", default=os.environ.get("OPENAI_MODEL", "openclaw:main"))
    parser.add_argument("--openai-base-url", default=os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:18789/v1"))
    parser.add_argument(
        "--agency-profile",
        default=(
            "We are a digital marketing agency. We help clients with lead generation, paid ads, "
            "creative strategy, landing pages, and conversion optimization."
        ),
    )
    parser.add_argument("--agency-profile-file", default="")
    parser.add_argument(
        "--style-rules",
        default=(
            "Use concise language, personalize opening line, include one clear CTA, "
            "avoid hard-selling, keep tone confident and friendly."
        ),
    )
    parser.add_argument("--style-rules-file", default="")

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.query_file:
        query_file = Path(args.query_file).expanduser().resolve()
        if not query_file.exists():
            print(f"Query file not found: {query_file}", file=sys.stderr)
            return 2
        args.query = query_file.read_text(encoding="utf-8").strip()

    if args.agency_profile_file:
        agency_profile_file = Path(args.agency_profile_file).expanduser().resolve()
        if not agency_profile_file.exists():
            print(f"Agency profile file not found: {agency_profile_file}", file=sys.stderr)
            return 2
        args.agency_profile = agency_profile_file.read_text(encoding="utf-8").strip()

    if args.style_rules_file:
        style_rules_file = Path(args.style_rules_file).expanduser().resolve()
        if not style_rules_file.exists():
            print(f"Style rules file not found: {style_rules_file}", file=sys.stderr)
            return 2
        args.style_rules = style_rules_file.read_text(encoding="utf-8").strip()

    openai_api_key = os.environ.get("OPENAI_API_KEY", "") or load_gateway_token()
    if not openai_api_key:
        print("OPENAI_API_KEY is required (or configure gateway.auth.token for local OpenClaw endpoint)", file=sys.stderr)
        return 2

    client_secret_file = Path(args.client_secret_file).expanduser().resolve()
    token_file = Path(args.token_file).expanduser().resolve()

    if not client_secret_file.exists():
        print(f"Google OAuth client secret file not found: {client_secret_file}", file=sys.stderr)
        return 2

    try:
        creds = get_credentials(client_secret_file, token_file, args.auth_mode)
        service = build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId=args.gmail_user_id).execute()
        profile_email = profile.get("emailAddress", "")

        if not profile_email:
            print("Unable to resolve authenticated Gmail address", file=sys.stderr)
            return 2

        openai_client = OpenAI(api_key=openai_api_key, base_url=args.openai_base_url)
        processed_label_id = ensure_label(service, args.gmail_user_id, args.processed_label)

        while True:
            result = process_once(
                service=service,
                openai_client=openai_client,
                args=args,
                user_id=args.gmail_user_id,
                profile_email=profile_email,
                processed_label_id=processed_label_id,
            )
            result["ts"] = int(time.time())
            print(json.dumps(result, ensure_ascii=False))
            sys.stdout.flush()

            if args.poll_interval <= 0:
                break
            time.sleep(args.poll_interval)

        return 0

    except HttpError as exc:
        print(f"Gmail API error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
