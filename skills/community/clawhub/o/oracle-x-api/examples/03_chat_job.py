#!/usr/bin/env python3
"""Ask the Oracle an open question, through the job API.

`POST /api/chat` holds the connection until an answer exists, which for a turn
that calls several tools can be minutes — long enough that the proxies between
an agent and the terminal start deciding the request is dead. The job form runs
the same pipeline and reports its steps while they happen, so this is the shape
to use for anything substantial.

Needs ORACLE_X_TOKEN. See references/auth.md.

    python 03_chat_job.py "How does the current BTC setup compare to March?"
"""

from __future__ import annotations

import sys
import time
from typing import Any

from client import OracleXError, get, post

POLL_INTERVAL_SECONDS = 2.0
POLL_TIMEOUT_SECONDS = 300.0

TERMINAL_OK = {"completed", "done", "finished"}
TERMINAL_BAD = {"failed", "error", "cancelled"}


def provider_is_serving() -> bool:
    """Check before spending a turn.

    The operator chooses the LLM layer, and it may be off or between providers.
    Asking first turns an opaque 503 mid-turn into a sentence the user can act
    on.
    """
    status = get("/api/chat/status")
    return bool(status.get("available", status.get("ok", False)))


def ask(message: str, session_id: str | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {"message": message}
    if session_id:
        body["session_id"] = session_id

    job = post("/api/chat/jobs", body, authenticated=True)
    job_id = job.get("job_id") or job.get("id")
    if not job_id:
        raise OracleXError(f"Chat job did not return an id: {job}")

    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    last_step: str | None = None

    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL_SECONDS)
        state = get(f"/api/chat/jobs/{job_id}", authenticated=True)

        step = state.get("step") or state.get("stage")
        if step and step != last_step:
            print(f"  … {step}", file=sys.stderr)
            last_step = step

        status = state.get("status")
        if status in TERMINAL_OK:
            return state.get("result") or state
        if status in TERMINAL_BAD:
            raise OracleXError(f"The turn failed: {state.get('error', status)}")

    raise OracleXError(
        f"No answer within {POLL_TIMEOUT_SECONDS:.0f}s. The job may still be "
        f"running — poll /api/chat/jobs/{job_id} again rather than starting a "
        "second turn."
    )


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    question = " ".join(sys.argv[1:])

    try:
        if not provider_is_serving():
            print(
                "No LLM provider is serving this instance right now. The open "
                "endpoints still answer — see references/endpoints.md.",
                file=sys.stderr,
            )
            return 1

        answer = ask(question)
        print(answer.get("response", answer))

        for citation in answer.get("citations", []) or []:
            print(f"  [{citation}]")
        followups = answer.get("followups") or []
        if followups:
            print("\nSuggested follow-ups:")
            for item in followups:
                print(f"- {item}")
    except OracleXError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
