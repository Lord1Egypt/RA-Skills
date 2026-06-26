#!/usr/bin/env python3

import argparse
import datetime
import http.client
import json
import re
import sys
from pathlib import Path

import debug_utils
import auth

API_HOST = auth.API_HOST
API_BASE_URL = f"https://{API_HOST}"
API_ENDPOINT = "/api/solve/audio_generate_skill"
CONSENT_VERSION = 1

# Hard limit for outbound prompt text (chars)
MAX_PROMPT_LENGTH = 1500

# Patterns that should always be redacted before sending or logging
ALWAYS_REDACT_PATTERNS = [
    re.compile(r"(?:api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"(?:token|session(?:_id)?|cookie)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"(?:password|passwd|pwd)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"(?:ssh-rsa|ssh-ed25519|-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----)"),
    re.compile(r"(?:Bearer|Basic)\s+[A-Za-z0-9+/=_-]{20,}"),
    re.compile(r"https?://[^\s\"']*(?:token|key|secret|signature)=[^\s\"']+", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"),  # email
    re.compile(r"(?:/Users/|/home/|C:\\Users\\)[^\s\"']+", re.IGNORECASE),  # file paths
]

HEURISTIC_SENSITIVE_PATTERNS = [
    ("government ID", re.compile(r"\b(?:\d{17}[\dXx]|\d{3}-\d{2}-\d{4})\b")),
    ("credit card / account number", re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")),
    ("crypto wallet", re.compile(r"\b(?:0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-z0-9]{25,60})\b")),
    ("date of birth", re.compile(r"(?:dob|date of birth|birthday|出生日期|生日).{0,20}(?:19|20)\d{2}[-/.年]\d{1,2}[-/.月]\d{1,2}(?:日)?", re.IGNORECASE)),
    ("home address", re.compile(r"(?:address|住址|家庭住址|home address|邮寄地址).{0,40}\d+", re.IGNORECASE)),
    ("medical detail", re.compile(r"(?:我|我的|I|my|最近|一直|目前|正在).{0,40}(?:诊断|病史|症状|药物|吃药|服药|medication|diagnos(?:is|ed)|therapy|depression|anxiety|panic attack|surgery)", re.IGNORECASE)),
    ("financial detail", re.compile(r"(?:我|我的|I|my|最近|一直|目前|正在).{0,40}(?:工资|薪水|存款|贷款|欠款|负债|salary|income|debt|loan|mortgage|tax|bank account|routing number)", re.IGNORECASE)),
    ("legal detail", re.compile(r"(?:我|我的|I|my|最近|一直|目前|正在).{0,40}(?:官司|起诉|仲裁|拘留|律师|签证|移民|lawsuit|court|attorney|arrest|visa|immigration|divorce)", re.IGNORECASE))
]

AUDIT_LOG_PATH = Path(__file__).resolve().parent / "audit.log"
CONSENT_STATE_PATH = Path(__file__).resolve().parent / ".oasis_audio_consent.json"


def _short_match(match_text, limit=40):
    compact = " ".join(match_text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "..."


def analyze_sensitive_content(text):
    redaction_hits = []
    heuristic_hits = []

    for pattern in ALWAYS_REDACT_PATTERNS:
        for match in pattern.finditer(text):
            redaction_hits.append(_short_match(match.group(0)))

    for match in find_phone_number_hits(text):
        heuristic_hits.append(f"phone number: {match}")

    for label, pattern in HEURISTIC_SENSITIVE_PATTERNS:
        match = pattern.search(text)
        if match:
            heuristic_hits.append(f"{label}: {_short_match(match.group(0))}")

    return {
        "redaction_hits": redaction_hits,
        "heuristic_hits": heuristic_hits,
        "needs_confirmation": bool(redaction_hits or heuristic_hits),
    }


def find_phone_number_hits(text):
    hits = []
    candidate_re = re.compile(r"(?<!\d)(?:\+?\d[\d().\s-]{6,}\d)(?!\d)")
    for match in candidate_re.finditer(text):
        candidate = match.group(0).strip()
        digits = re.sub(r"\D", "", candidate)
        if not 8 <= len(digits) <= 15:
            continue
        if re.fullmatch(r"(?:19|20)\d{2}[-/.]\d{1,2}[-/.]\d{1,2}", candidate):
            continue
        hits.append(_short_match(candidate))
    return hits


def prepare_text(text):
    """Redact hard-sensitive tokens and enforce the prompt length limit."""
    analysis = analyze_sensitive_content(text)

    if analysis["redaction_hits"]:
        print("WARNING: Redacting high-risk sensitive content before send/log.", file=sys.stderr)
        for match in analysis["redaction_hits"]:
            print(f"  - {match}", file=sys.stderr)
        for pattern in ALWAYS_REDACT_PATTERNS:
            text = pattern.sub("[REDACTED]", text)

    if len(text) > MAX_PROMPT_LENGTH:
        print(f"WARNING: Prompt exceeds {MAX_PROMPT_LENGTH} chars ({len(text)}). Truncating.", file=sys.stderr)
        text = text[:MAX_PROMPT_LENGTH]

    return text, analysis


def require_sensitive_confirmation(analysis):
    print(
        "Sensitive content detected. User confirmation is required before writing audit.log or sending to the API.",
        file=sys.stderr,
    )
    for finding in analysis["heuristic_hits"]:
        print(f"  - {finding}", file=sys.stderr)
    if analysis["redaction_hits"]:
        print("  - high-risk tokens were redacted before any send/log attempt", file=sys.stderr)
    print("Review with --dry-run, then re-run with --allow-sensitive only after the user explicitly confirms.", file=sys.stderr)


def print_preview(text, analysis, voice_id=None, heading="=== PREVIEW ===", stream=sys.stdout):
    print(heading, file=stream)
    print(f"Length: {len(text)} / {MAX_PROMPT_LENGTH} chars", file=stream)
    if voice_id:
        print(f"Voice: {voice_id}", file=stream)
    if analysis["heuristic_hits"]:
        print("Sensitive heuristics:", file=stream)
        for finding in analysis["heuristic_hits"]:
            print(f"  - {finding}", file=stream)
    if analysis["redaction_hits"]:
        print(f"Redactions applied: {len(analysis['redaction_hits'])}", file=stream)
    print(f"Text:\n{text}", file=stream)
    print("=== End preview ===", file=stream)


def write_audit_log(text, analysis=None, audio_id=None, status=None, error=None):
    """Append a record of what was sent to the local audit log."""
    try:
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "prompt_length": len(text),
            "prompt_text": text,
            "audio_id": audio_id,
            "status": status,
            "error": error,
            "sensitive_findings": analysis["heuristic_hits"] if analysis else [],
            "redaction_count": len(analysis["redaction_hits"]) if analysis else 0,
        }
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        debug_utils.debug_print(f"Audit log written to {AUDIT_LOG_PATH}")
    except OSError as e:
        debug_utils.debug_print(f"Failed to write audit log: {e}")


def has_persistent_consent():
    try:
        if not CONSENT_STATE_PATH.exists():
            return False
        data = json.loads(CONSENT_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return bool(data.get("granted")) and data.get("version") == CONSENT_VERSION


def write_persistent_consent():
    record = {
        "granted": True,
        "version": CONSENT_VERSION,
        "granted_at": datetime.datetime.now().isoformat(),
        "api_base_url": API_BASE_URL,
        "local_sources": [
            "~/.qclaw/agents/main/sessions",
            "~/.qclaw/workspace/memory",
            "~/.qclaw/workspace/USER.md",
            "~/.openclaw/agents/main/sessions",
            "~/.openclaw/workspace/memory",
            "~/.openclaw/workspace/USER.md",
        ],
    }
    CONSENT_STATE_PATH.write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def print_first_use_consent_notice():
    message = f"""
Before the first send, let me draw the boundary in plain language.

To make the audio feel genuinely tailored to you, Oasis Audio may read local context from:
  - ~/.qclaw/agents/main/sessions
  - ~/.qclaw/workspace/memory
  - ~/.qclaw/workspace/USER.md
  - ~/.openclaw/agents/main/sessions
  - ~/.openclaw/workspace/memory
  - ~/.openclaw/workspace/USER.md

What goes out is only the composed prompt for audio generation. The request is sent to:
  - {API_BASE_URL}

After generation, the result may be viewed online on the xplai webpage.

If the outgoing text appears to contain sensitive information, the system will stop at the door:
it will not be written to audit.log, and it will not be sent onward until you explicitly confirm.

If you accept this boundary, re-run once with:
  ./xplai_gen_audio.py --acknowledge-consent ...

That acknowledgement will be stored locally so you do not need to repeat it every time.
""".strip()
    print(message, file=sys.stderr)


def ensure_persistent_consent(acknowledge_consent=False):
    if has_persistent_consent():
        return
    if not acknowledge_consent:
        print_first_use_consent_notice()
        sys.exit(3)
    write_persistent_consent()


def generate_audio(text, voice_id=None, allow_sensitive=False, audit=False):
    text, analysis = prepare_text(text)

    if analysis["needs_confirmation"] and not allow_sensitive:
        print_preview(
            text,
            analysis,
            voice_id=voice_id,
            heading="=== SENSITIVE PREVIEW — prompt will NOT be sent yet ===",
            stream=sys.stderr,
        )
        require_sensitive_confirmation(analysis)
        sys.exit(2)

    url = f"{API_BASE_URL}{API_ENDPOINT}"

    payload = {"text": text}
    if voice_id:
        payload["voice_id"] = voice_id

    debug_utils.log_request("POST", url, json=payload)

    token = auth.get_or_refresh_token()
    if not token:
        print("Error: Failed to get authentication token", file=sys.stderr)
        sys.exit(1)

    try:
        conn = http.client.HTTPSConnection(API_HOST, timeout=30)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        conn.request("POST", API_ENDPOINT, json.dumps(payload), headers)
        response = conn.getresponse()
        response_body = response.read().decode("utf-8")

        if response.status >= 400:
            print(f"HTTP Error: {response.status} {response.reason}", file=sys.stderr)
            if audit:
                write_audit_log(text, analysis=analysis, error=f"HTTP {response.status}")
            sys.exit(1)

        debug_utils.log_response(response, response_body)

        result = json.loads(response_body)
        conn.close()

        if result.get("code") == 0:
            data = result.get("data", {})
            audio_id = data.get("video_id")
            status = data.get("card", {}).get("status")
            if audit:
                write_audit_log(text, analysis=analysis, audio_id=audio_id, status=status)
            print(f"Audio generation request submitted successfully!")
            print(f"Audio ID: {audio_id}")
            print(f"Status: {status}")
            return audio_id
        else:
            error_msg = result.get('msg')
            if audit:
                write_audit_log(text, analysis=analysis, error=error_msg)
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)
    except (http.client.HTTPException, OSError) as e:
        if audit:
            write_audit_log(text, analysis=analysis, error=str(e))
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate audio using xplai API")
    parser.add_argument("text", type=str, help="Text content to convert to audio")
    parser.add_argument("--voice-id", type=str, default=None, help="Voice ID for audio narration (see text_architecture.md Layer 3)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print request/response details")
    parser.add_argument("--dry-run", action="store_true", help="Show sanitized prompt without sending to API")
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Write the sent prompt and request outcome to audit.log",
    )
    parser.add_argument(
        "--acknowledge-consent",
        action="store_true",
        help="Persist the first-use authorization notice locally and continue",
    )
    parser.add_argument(
        "--allow-sensitive",
        action="store_true",
        help="Allow send/audit-log after the user explicitly confirms sensitive content handling",
    )

    args = parser.parse_args()

    debug_utils.set_debug(args.debug)

    if args.dry_run:
        sanitized, analysis = prepare_text(args.text)
        print_preview(
            sanitized,
            analysis,
            voice_id=args.voice_id,
            heading="=== DRY RUN — prompt will NOT be sent ===",
        )
        return

    ensure_persistent_consent(acknowledge_consent=args.acknowledge_consent)

    audio_id = generate_audio(
        args.text,
        voice_id=args.voice_id,
        allow_sensitive=args.allow_sensitive,
        audit=args.audit,
    )
    if audio_id:
        print(f"use ./xplai_status.py {audio_id} to check the status")


if __name__ == "__main__":
    main()
