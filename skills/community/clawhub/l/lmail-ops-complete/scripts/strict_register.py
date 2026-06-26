#!/usr/bin/env python3
"""Run strict registration flow: challenge -> solve -> permit -> register."""

from __future__ import annotations

import argparse
import json
import os
import random
import string
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lmail_http import (  # noqa: E402
    LMailHttpError,
    decode_jwt_payload,
    expect_success,
    json_pretty,
    mask_secret,
    request_json,
    save_json_file,
    solve_pow,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Strict LMail registration flow")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--address", required=True, help="local-part only")
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model")
    parser.add_argument("--agent-fingerprint")
    parser.add_argument("--metadata-json", help="inline metadata JSON")
    parser.add_argument("--metadata-file", help="path to metadata JSON")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--max-iterations", type=int, default=100_000_000)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--print-api-key", action="store_true")
    parser.add_argument("--challenge-endpoint", default="/api/v1/auth/permit/challenge")
    parser.add_argument("--solve-endpoint", default="/api/v1/auth/permit/solve")
    parser.add_argument("--register-endpoint", default="/api/v1/auth/register")
    return parser.parse_args()


def build_fingerprint(user_value: str | None) -> str:
    if user_value:
        return user_value
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"agent-auto-fingerprint-{suffix}"


def load_metadata(args: argparse.Namespace) -> dict[str, object] | None:
    if args.metadata_json:
        return json.loads(args.metadata_json)
    if args.metadata_file:
        return json.loads(Path(args.metadata_file).read_text(encoding="utf-8"))
    return None


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    metadata = load_metadata(args)
    agent_fingerprint = build_fingerprint(args.agent_fingerprint)

    status, challenge_resp = request_json(
        url=f"{base_url}{args.challenge_endpoint}",
        method="POST",
        payload={},
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"challenge failed with HTTP {status}: {challenge_resp}")

    challenge_data = expect_success(challenge_resp, "challenge")
    challenge_token = challenge_data.get("challengeToken")
    if not challenge_token:
        raise LMailHttpError("challenge response missing data.challengeToken")

    claims = decode_jwt_payload(str(challenge_token))
    jti = str(claims.get("jti") or "")
    salt = str(claims.get("salt") or "")
    difficulty = int(claims.get("difficulty") or claims.get("powDifficulty") or os.getenv("REG_POW_DIFFICULTY", "5"))

    if not jti or not salt:
        raise LMailHttpError("challenge token missing jti/salt")

    solved = solve_pow(
        jti=jti,
        salt=salt,
        difficulty=difficulty,
        max_iterations=args.max_iterations,
    )

    status, solve_resp = request_json(
        url=f"{base_url}{args.solve_endpoint}",
        method="POST",
        payload={
            "challengeToken": challenge_token,
            "nonce": str(solved["nonce"]),
        },
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"solve failed with HTTP {status}: {solve_resp}")

    solve_data = expect_success(solve_resp, "solve")
    permit = solve_data.get("permit")
    if not permit:
        raise LMailHttpError("solve response missing data.permit")

    register_payload: dict[str, object] = {
        "address": args.address,
        "displayName": args.display_name,
        "provider": args.provider,
        "agentFingerprint": agent_fingerprint,
        "permit": permit,
    }
    if args.model:
        register_payload["model"] = args.model
    if metadata is not None:
        register_payload["metadata"] = metadata

    status, register_resp = request_json(
        url=f"{base_url}{args.register_endpoint}",
        method="POST",
        payload=register_payload,
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"register failed with HTTP {status}: {register_resp}")

    register_data = expect_success(register_resp, "register")
    account = register_data.get("account") or {}
    api_key = str(register_data.get("apiKey") or "")
    token = str(register_data.get("token") or "")

    creds = {
        "baseUrl": base_url,
        "address": account.get("address"),
        "localPart": args.address,
        "displayName": args.display_name,
        "provider": args.provider,
        "model": args.model,
        "agentFingerprint": agent_fingerprint,
        "apiKey": api_key,
        "token": token,
        "createdAt": now_iso(),
        "registration": {
            "powDifficulty": difficulty,
            "powAttempts": solved["attempts"],
        },
    }
    save_json_file(args.credentials_file, creds)

    output = {
        "ok": True,
        "step": "strict_register",
        "account": {
            "id": account.get("id"),
            "address": account.get("address"),
            "displayName": account.get("displayName"),
            "role": account.get("role"),
            "status": account.get("status"),
        },
        "credentialsFile": args.credentials_file,
        "apiKeyMasked": mask_secret(api_key),
        "tokenMasked": mask_secret(token),
    }
    if args.print_api_key:
        output["apiKey"] = api_key

    print(json_pretty(output))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (LMailHttpError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
