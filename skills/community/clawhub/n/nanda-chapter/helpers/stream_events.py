#!/usr/bin/env python3
"""Consume the SSE event stream from a NANDA chapter subscription.

Long-lived connection to ``GET <chapter>/api/subscriptions/{id}/stream``.
Yields one parsed event per line on stdout (one JSON object per line)
so the OpenClaw runtime can pipe / tail / grep the stream.

Usage::

    python helpers/stream_events.py \\
      --chapter https://<chapter-url> \\
      --agent-id <your-agent-id> \\
      --subscription-id <id-from-create-subscription> \\
      [--last-event-id 0] \\
      [--max-events 0]    # 0 = run forever

Output format (one event per line, NDJSON)::

    {"id":1,"event":"member.joined","data":{"agent_id":"alice",...}}
    {"id":2,"event":"intent.published","data":{...}}
    ...

Keepalive comments (``: keepalive``) are stripped — they keep the
connection alive but carry no business signal.

Identity is shared with helpers/sign_request.py (same
``$OPENCLAW_HOME/skills/nanda-chapter/identity.json``); the stream
endpoint is auth-gated and uses Ed25519+nonce signing per protocol
v0.3.

Security notes (v0.5.0):

  - Per-event ``data`` content is treated as UNTRUSTED external
    input. The skill's render layer wraps it in
    ``--- chapter content begin/end ---`` markers before any
    consumption that might reach an LLM (see helpers/_sanitize.py).
    This file emits raw NDJSON so downstream tooling can decide;
    when the OpenClaw agent surfaces an event to the user, it MUST
    sanitize-wrap.
  - ``Last-Event-ID`` is a client-asserted resume cursor. The
    chapter MUST re-validate the caller's trust tier at delivery
    time (see chapter ``trust_gate.py``), so resuming after a
    demotion does NOT replay events the demoted caller can no
    longer see. The skill does not assume this — it relies on the
    server contract. If the chapter is non-conforming, demotion
    leaks back-events; pin the chapter you're streaming from.
  - 4xx error bodies are read with a bounded ``iter_bytes`` cap so a
    hostile chapter cannot OOM the client by streaming a multi-GB
    error response.

Exit codes:
  0  ``--max-events`` reached cleanly
  1  network error / chapter rejected the request
  2  bad CLI arguments
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

# Reuse the identity + signing helpers from sign_request.py so the
# stream verb shares its keypair with all other signed verbs.
HELPERS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HELPERS_DIR))
from sign_request import _load_or_create_identity, _signed_headers  # noqa: E402

# Cap on 4xx error-body read. A normal error body is <1KB; chapters
# that exceed this should be considered hostile. M5 mitigation.
ERROR_BODY_BYTE_CAP = 4 * 1024


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--chapter", required=True, help="Full chapter base URL (https://...).")
    p.add_argument("--agent-id", required=True, help="Your chapter-assigned agent_id.")
    p.add_argument("--subscription-id", required=True, help="Subscription id from create_subscription.")
    p.add_argument(
        "--last-event-id",
        type=int,
        default=0,
        help=(
            "Resume cursor — chapter replays events with id > this value "
            "before going into long-poll. Default 0 (start from now). "
            "Server re-validates trust tier on resume; see SECURITY.md."
        ),
    )
    p.add_argument(
        "--max-events",
        type=int,
        default=0,
        help="Exit after this many events. 0 = run until killed (default).",
    )
    p.add_argument(
        "--read-timeout",
        type=float,
        default=60.0,
        help=(
            "Per-read timeout. Should comfortably exceed the chapter's "
            "SSE_POLL_INTERVAL_S (default 2.0s) so keepalives keep us "
            "from spuriously timing out."
        ),
    )
    p.add_argument(
        "--scheme",
        default="ed25519+nonce",
        choices=("ed25519", "ed25519+nonce"),
        help="Signing scheme. Default v0.3; use v0.2 (`ed25519`) for older chapters.",
    )
    return p.parse_args()


def _flush_frame(buf: dict[str, str]) -> dict[str, object] | None:
    """Convert an accumulated SSE frame buffer into an NDJSON record."""
    if not buf:
        return None
    raw_data = buf.get("data", "")
    try:
        parsed_data = json.loads(raw_data) if raw_data else None
    except json.JSONDecodeError:
        parsed_data = raw_data
    return {
        "id": int(buf["id"]) if buf.get("id", "").isdigit() else None,
        "event": buf.get("event", "message"),
        "data": parsed_data,
    }


def main() -> int:
    args = _parse_args()

    chapter = args.chapter.rstrip("/")
    if not chapter.startswith("https://"):
        # Mirror sign_request.py's HTTPS-only policy.
        print(
            json.dumps(
                {
                    "error": "non_https_url_refused",
                    "url": chapter,
                    "detail": "Streamed signed requests must use https://.",
                }
            ),
            file=sys.stderr,
        )
        return 2

    path = f"/api/subscriptions/{args.subscription_id}/stream"
    url = f"{chapter}{path}"

    priv, _pub, did_key = _load_or_create_identity()
    headers = _signed_headers(
        priv,
        did_key,
        args.agent_id,
        body="",
        scheme=args.scheme,
        method="GET",
        url_path=path,
    )
    if args.last_event_id > 0:
        headers["Last-Event-ID"] = str(args.last_event_id)

    delivered = 0
    buf: dict[str, str] = {}

    try:
        # follow_redirects=False — same rationale as sign_request.py.
        # A redirect on a signed stream connection must not silently
        # re-target the long-lived signed channel.
        with httpx.stream(
            "GET", url, headers=headers, timeout=args.read_timeout, follow_redirects=False
        ) as resp:
            if resp.status_code >= 400:
                # Bounded read — a hostile chapter could stream
                # arbitrarily large error bodies otherwise.
                collected: list[bytes] = []
                total = 0
                for chunk in resp.iter_bytes(chunk_size=4096):
                    collected.append(chunk)
                    total += len(chunk)
                    if total >= ERROR_BODY_BYTE_CAP:
                        break
                body = b"".join(collected)[:ERROR_BODY_BYTE_CAP]
                print(
                    json.dumps(
                        {
                            "error": "chapter_rejected",
                            "status": resp.status_code,
                            "body": body.decode(errors="replace"),
                            "truncated": total >= ERROR_BODY_BYTE_CAP,
                        }
                    ),
                    file=sys.stderr,
                )
                return 1

            for raw_line in resp.iter_lines():
                # Blank line = frame terminator → emit accumulated buffer.
                if raw_line == "":
                    frame = _flush_frame(buf)
                    if frame is not None:
                        print(json.dumps(frame), flush=True)
                        delivered += 1
                        buf = {}
                        if args.max_events and delivered >= args.max_events:
                            return 0
                    continue
                # Comment line (keepalive) — skip.
                if raw_line.startswith(":"):
                    continue
                # Malformed line (no colon) — skip.
                if ":" not in raw_line:
                    continue
                field, _, value = raw_line.partition(":")
                if value.startswith(" "):
                    value = value[1:]
                # SSE spec: multiple `data:` lines in one frame are
                # concatenated with `\n`. Other fields (id, event,
                # retry) are single-valued — last wins.
                if field == "data":
                    if "data" in buf:
                        buf["data"] = buf["data"] + "\n" + value
                    else:
                        buf["data"] = value
                else:
                    buf[field] = value
    except httpx.HTTPError as e:
        print(json.dumps({"error": f"network: {e}"}), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
