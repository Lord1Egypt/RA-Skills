#!/usr/bin/env python3
"""Solve LMail registration PoW nonce."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lmail_http import LMailHttpError, decode_jwt_payload, solve_pow  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve PoW nonce from challenge token")
    parser.add_argument("--challenge-token", help="JWT challenge token from /permit/challenge")
    parser.add_argument("--jti", help="Challenge JTI override")
    parser.add_argument("--salt", help="Challenge salt override")
    parser.add_argument("--difficulty", type=int, help="Difficulty override")
    parser.add_argument("--max-iterations", type=int, default=100_000_000)
    parser.add_argument("--start-nonce", type=int, default=0)
    parser.add_argument("--output", choices=["json", "text"], default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    claims: dict[str, object] = {}
    if args.challenge_token:
        claims = decode_jwt_payload(args.challenge_token)

    jti = args.jti or str(claims.get("jti") or "")
    salt = args.salt or str(claims.get("salt") or "")

    difficulty = args.difficulty
    if difficulty is None:
        difficulty = int(
            claims.get("difficulty")
            or claims.get("powDifficulty")
            or os.getenv("REG_POW_DIFFICULTY", "5")
        )

    if not jti or not salt:
        raise LMailHttpError("Missing jti/salt; provide challenge token or explicit --jti and --salt")

    solved = solve_pow(
        jti=jti,
        salt=salt,
        difficulty=difficulty,
        max_iterations=args.max_iterations,
        start_nonce=args.start_nonce,
    )

    if args.output == "text":
        print(solved["nonce"])
    else:
        print(
            json.dumps(
                {
                    "ok": True,
                    "jti": jti,
                    "salt": salt,
                    "difficulty": difficulty,
                    "result": solved,
                },
                indent=2,
                ensure_ascii=True,
            )
        )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LMailHttpError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
