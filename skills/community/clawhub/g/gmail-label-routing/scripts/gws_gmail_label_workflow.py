#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_CREDENTIAL_CANDIDATES = [
    "/root/.config/gws/credentials.new.json",
    "/root/.config/gws/credentials.json",
]


class WorkflowError(RuntimeError):
    pass


def run_json(cmd: list[str]) -> dict[str, Any]:
    cp = subprocess.run(cmd, capture_output=True, text=True)
    if cp.returncode != 0:
        detail = (cp.stderr or cp.stdout or "").strip()
        raise WorkflowError(detail or f"command failed: {' '.join(cmd)}")
    out = (cp.stdout or "").strip()
    return json.loads(out) if out else {}


def oauth_token(credentials_file: str) -> str:
    creds = json.loads(Path(credentials_file).read_text(encoding="utf-8"))
    for key in ("client_id", "client_secret", "refresh_token"):
        if not creds.get(key):
            raise WorkflowError(f"Missing `{key}` in credentials file: {credentials_file}")

    body = urllib.parse.urlencode(
        {
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        }
    ).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        payload = e.read().decode(errors="replace")
        raise WorkflowError(f"Token exchange failed ({e.code}): {payload}") from e

    token = data.get("access_token")
    if not token:
        raise WorkflowError("Token exchange returned no access_token")
    return token


def gmail_api(method: str, path: str, token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"https://gmail.googleapis.com/gmail/v1/{path.lstrip('/')}"
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode()

    req = urllib.request.Request(url, data=data, method=method.upper())
    req.add_header("Authorization", f"Bearer {token}")
    if payload is not None:
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode().strip()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise WorkflowError(f"Gmail API {method} {path} failed ({e.code}): {body}") from e


def resolve_credentials_file(explicit: str | None) -> str:
    candidates = [explicit] if explicit else []
    candidates.extend(DEFAULT_CREDENTIAL_CANDIDATES)

    for c in candidates:
        if not c:
            continue
        p = Path(c)
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if all(data.get(k) for k in ("client_id", "client_secret", "refresh_token")):
            return str(p)

    raise WorkflowError(
        "No valid OAuth credential file found. "
        "Provide --credentials-file or ensure /root/.config/gws/credentials.new.json exists."
    )


def list_all_message_ids(user_id: str, query: str) -> list[str]:
    ids: list[str] = []
    page_token: str | None = None

    while True:
        params: dict[str, Any] = {"userId": user_id, "q": query, "maxResults": 500}
        if page_token:
            params["pageToken"] = page_token
        data = run_json(["gws", "gmail", "users", "messages", "list", "--params", json.dumps(params, ensure_ascii=False)])
        ids.extend([m.get("id") for m in data.get("messages", []) if m.get("id")])
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    seen: set[str] = set()
    out: list[str] = []
    for msg_id in ids:
        if msg_id in seen:
            continue
        seen.add(msg_id)
        out.append(msg_id)
    return out


def batch_modify(user_id: str, ids: list[str], add_label_ids: list[str], remove_label_ids: list[str], dry_run: bool) -> int:
    if not ids:
        return 0

    updated = 0
    for start in range(0, len(ids), 1000):
        chunk = ids[start : start + 1000]
        body = {
            "ids": chunk,
            "addLabelIds": add_label_ids,
            "removeLabelIds": remove_label_ids,
        }
        if not dry_run:
            run_json(
                [
                    "gws",
                    "gmail",
                    "users",
                    "messages",
                    "batchModify",
                    "--params",
                    json.dumps({"userId": user_id}, ensure_ascii=False),
                    "--json",
                    json.dumps(body, ensure_ascii=False),
                ]
            )
        updated += len(chunk)
    return updated


def ensure_label(user_id: str, label_name: str, dry_run: bool) -> tuple[str, str | None]:
    labels = run_json(["gws", "gmail", "users", "labels", "list", "--params", json.dumps({"userId": user_id})]).get("labels", [])
    by_name = {x.get("name"): x.get("id") for x in labels}
    existing = by_name.get(label_name)
    if existing:
        return existing, None

    if dry_run:
        return "DRY_RUN_LABEL_ID", "DRY_RUN_LABEL_ID"

    created = run_json(
        [
            "gws",
            "gmail",
            "users",
            "labels",
            "create",
            "--params",
            json.dumps({"userId": user_id}),
            "--json",
            json.dumps(
                {
                    "name": label_name,
                    "labelListVisibility": "labelShow",
                    "messageListVisibility": "show",
                }
            ),
        ]
    )
    label_id = created.get("id")
    if not label_id:
        raise WorkflowError(f"Failed to create label `{label_name}`")
    return label_id, label_id


def sender_filters(filters: list[dict[str, Any]], sender: str) -> list[dict[str, Any]]:
    s = sender.lower()
    return [f for f in filters if (f.get("criteria", {}).get("from", "").lower() == s)]


def has_desired_filter(filters: list[dict[str, Any]], label_id: str, remove_inbox: bool) -> bool:
    for f in filters:
        act = f.get("action", {}) or {}
        add_ids = act.get("addLabelIds", []) or []
        rem_ids = act.get("removeLabelIds", []) or []
        if label_id not in add_ids:
            continue
        if remove_inbox and "INBOX" not in rem_ids:
            continue
        return True
    return False


def create_filter(token: str, sender: str, label_id: str, remove_inbox: bool, dry_run: bool) -> str | None:
    if dry_run:
        return "DRY_RUN_FILTER_ID"

    action: dict[str, Any] = {"addLabelIds": [label_id]}
    if remove_inbox:
        action["removeLabelIds"] = ["INBOX"]

    payload = {
        "criteria": {"from": sender},
        "action": action,
    }
    created = gmail_api("POST", "users/me/settings/filters", token, payload)
    return created.get("id")


def delete_filter(token: str, filter_id: str, dry_run: bool) -> None:
    if dry_run:
        return
    gmail_api("DELETE", f"users/me/settings/filters/{filter_id}", token)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Workflow consistente para etiquetar por remitente en Gmail: "
            "crea/valida etiqueta, crea filtro por remitente y aplica retroactivo."
        )
    )
    parser.add_argument("--label", required=True, help="Nombre de la etiqueta destino (ej. Notificaciones bancarias)")
    parser.add_argument("--sender", action="append", required=True, help="Remitente exacto a configurar (se puede repetir)")
    parser.add_argument("--user-id", default="me", help="User ID de Gmail (default: me)")

    inbox_group = parser.add_mutually_exclusive_group()
    inbox_group.add_argument("--remove-inbox", dest="remove_inbox", action="store_true", default=True)
    inbox_group.add_argument("--keep-inbox", dest="remove_inbox", action="store_false")

    parser.add_argument(
        "--replace-sender-filters",
        action="store_true",
        help="Eliminar filtros existentes de ese remitente antes de crear el filtro estándar",
    )
    parser.add_argument("--no-retro", action="store_true", help="No aplicar cambios a correos existentes")
    parser.add_argument("--credentials-file", help="Ruta a credenciales OAuth para filtros (authorized_user)")
    parser.add_argument("--dry-run", action="store_true", help="Simula acciones sin escribir cambios")
    args = parser.parse_args()

    try:
        senders = [s.strip() for s in args.sender if s and s.strip()]
        if not senders:
            raise WorkflowError("Provide at least one --sender")

        label_id, created_label_id = ensure_label(args.user_id, args.label, args.dry_run)

        credentials_file = resolve_credentials_file(args.credentials_file)
        token = oauth_token(credentials_file)

        raw_filters = gmail_api("GET", "users/me/settings/filters", token).get("filter", [])

        results: list[dict[str, Any]] = []
        for sender in senders:
            sfilters = sender_filters(raw_filters, sender)
            desired_exists = has_desired_filter(sfilters, label_id, args.remove_inbox)

            deleted_filters: list[str] = []
            created_filter_id: str | None = None

            if args.replace_sender_filters and sfilters:
                for f in sfilters:
                    fid = f.get("id")
                    if not fid:
                        continue
                    delete_filter(token, fid, args.dry_run)
                    deleted_filters.append(fid)
                # after replace, desired no longer exists
                desired_exists = False
                # keep in-memory list coherent
                raw_filters = [f for f in raw_filters if f.get("id") not in set(deleted_filters)]

            if not desired_exists:
                created_filter_id = create_filter(token, sender, label_id, args.remove_inbox, args.dry_run)

            retro_applied = 0
            if not args.no_retro:
                ids = list_all_message_ids(args.user_id, f"from:{sender}")
                retro_applied = batch_modify(
                    user_id=args.user_id,
                    ids=ids,
                    add_label_ids=[label_id],
                    remove_label_ids=["INBOX"] if args.remove_inbox else [],
                    dry_run=args.dry_run,
                )

            from_count = len(list_all_message_ids(args.user_id, f"from:{sender}"))
            label_count = len(list_all_message_ids(args.user_id, f"from:{sender} label:\"{args.label}\""))
            inbox_count = len(list_all_message_ids(args.user_id, f"from:{sender} in:inbox"))

            results.append(
                {
                    "sender": sender,
                    "createdFilterId": created_filter_id,
                    "deletedFilterIds": deleted_filters,
                    "retroApplied": retro_applied,
                    "fromCount": from_count,
                    "withLabelCount": label_count,
                    "inboxCount": inbox_count,
                }
            )

        print(
            json.dumps(
                {
                    "label": args.label,
                    "labelId": label_id,
                    "createdLabelId": created_label_id,
                    "removeInbox": args.remove_inbox,
                    "replaceSenderFilters": args.replace_sender_filters,
                    "retro": not args.no_retro,
                    "dryRun": args.dry_run,
                    "credentialsFile": credentials_file,
                    "results": results,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "detail": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
