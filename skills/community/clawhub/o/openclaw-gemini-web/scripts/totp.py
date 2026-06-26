#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, unquote, urlparse


DEFAULT_ALGORITHM = "SHA1"
DEFAULT_DIGITS = 6
DEFAULT_PERIOD = 30


@dataclass(frozen=True)
class TotpConfig:
    secret_base32: str
    algorithm: str = DEFAULT_ALGORITHM
    digits: int = DEFAULT_DIGITS
    period: int = DEFAULT_PERIOD
    issuer: Optional[str] = None
    account_name: Optional[str] = None


def normalize_secret(secret: str) -> str:
    normalized = "".join(secret.strip().split()).upper()
    if not normalized:
        raise ValueError("secret is empty")
    return normalized


def parse_otpauth_uri(uri: str) -> TotpConfig:
    parsed = urlparse(uri)
    if parsed.scheme != "otpauth":
        raise ValueError("otpauth URI must start with otpauth://")
    if parsed.netloc.lower() != "totp":
        raise ValueError("only otpauth://totp URIs are supported")

    label = unquote(parsed.path.lstrip("/"))
    params = parse_qs(parsed.query)
    secret = params.get("secret", [None])[0]
    if not secret:
        raise ValueError("otpauth URI is missing secret")

    issuer = params.get("issuer", [None])[0]
    algorithm = params.get("algorithm", [DEFAULT_ALGORITHM])[0].upper()
    digits = int(params.get("digits", [DEFAULT_DIGITS])[0])
    period = int(params.get("period", [DEFAULT_PERIOD])[0])

    account_name = None
    if ":" in label:
        label_issuer, account_name = label.split(":", 1)
        if not issuer:
            issuer = label_issuer
    elif label:
        account_name = label

    return TotpConfig(
        secret_base32=normalize_secret(secret),
        algorithm=algorithm,
        digits=digits,
        period=period,
        issuer=issuer,
        account_name=account_name,
    )


def parse_totp_source(*, secret: str | None = None, uri: str | None = None) -> TotpConfig:
    if uri:
        return parse_otpauth_uri(uri)
    if secret:
        return TotpConfig(secret_base32=normalize_secret(secret))
    raise ValueError("provide either a base32 secret or an otpauth URI")


def decode_secret(secret_base32: str) -> bytes:
    normalized = normalize_secret(secret_base32)
    padding = "=" * ((8 - (len(normalized) % 8)) % 8)
    try:
        return base64.b32decode(normalized + padding, casefold=True)
    except Exception as exc:  # pragma: no cover - defensive rewording
        raise ValueError("invalid base32 secret") from exc


def generate_totp(
    secret: str,
    *,
    timestamp: int | float | None = None,
    digits: int = DEFAULT_DIGITS,
    period: int = DEFAULT_PERIOD,
    algorithm: str = DEFAULT_ALGORITHM,
) -> str:
    if digits <= 0:
        raise ValueError("digits must be positive")
    if period <= 0:
        raise ValueError("period must be positive")

    digest_name = algorithm.lower()
    try:
        digest = getattr(hashlib, digest_name)
    except AttributeError as exc:
        raise ValueError(f"unsupported algorithm: {algorithm}") from exc

    key = decode_secret(secret)
    now = int(time.time() if timestamp is None else timestamp)
    counter = now // period
    counter_bytes = counter.to_bytes(8, "big")
    mac = hmac.new(key, counter_bytes, digest).digest()
    offset = mac[-1] & 0x0F
    binary = int.from_bytes(mac[offset : offset + 4], "big") & 0x7FFFFFFF
    otp = binary % (10**digits)
    return f"{otp:0{digits}d}"


def load_source_from_env(var_name: str) -> tuple[str | None, str | None]:
    raw = os.environ.get(var_name)
    if not raw:
        raise ValueError(f"environment variable {var_name} is empty or unset")
    if raw.startswith("otpauth://"):
        return None, raw
    return raw, None


def load_source_from_json(path: str, key: str) -> tuple[str | None, str | None]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw = payload.get(key)
    if not raw:
        raise ValueError(f"key {key!r} was not found in {path}")
    if isinstance(raw, str) and raw.startswith("otpauth://"):
        return None, raw
    if not isinstance(raw, str):
        raise ValueError(f"key {key!r} in {path} must be a string")
    return raw, None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate TOTP codes from a base32 secret or otpauth URI without third-party dependencies."
    )
    parser.add_argument("--secret", help="Base32-encoded TOTP secret")
    parser.add_argument("--uri", help="otpauth://totp/... URI")
    parser.add_argument("--env", help="Read the secret or otpauth URI from an environment variable")
    parser.add_argument("--json-file", help="Read the secret or otpauth URI from a JSON file")
    parser.add_argument("--json-key", default="secret", help="Key to read when using --json-file")
    parser.add_argument("--time", type=int, help="Unix timestamp override for reproducible output")
    parser.add_argument("--digits", type=int, help="Override number of digits")
    parser.add_argument("--period", type=int, help="Override TOTP period in seconds")
    parser.add_argument("--algorithm", help="Override digest algorithm, for example SHA1 or SHA256")
    parser.add_argument("--json", action="store_true", help="Print a JSON payload instead of a bare code")
    return parser


def resolve_config(args: argparse.Namespace) -> TotpConfig:
    secret = args.secret
    uri = args.uri

    if args.env:
        secret, uri = load_source_from_env(args.env)
    elif args.json_file:
        secret, uri = load_source_from_json(args.json_file, args.json_key)

    config = parse_totp_source(secret=secret, uri=uri)
    return TotpConfig(
        secret_base32=config.secret_base32,
        algorithm=(args.algorithm or config.algorithm).upper(),
        digits=args.digits or config.digits,
        period=args.period or config.period,
        issuer=config.issuer,
        account_name=config.account_name,
    )


def main() -> int:
    args = build_parser().parse_args()
    config = resolve_config(args)
    code = generate_totp(
        config.secret_base32,
        timestamp=args.time,
        digits=config.digits,
        period=config.period,
        algorithm=config.algorithm,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "code": code,
                    "issuer": config.issuer,
                    "accountName": config.account_name,
                    "algorithm": config.algorithm,
                    "digits": config.digits,
                    "period": config.period,
                },
                ensure_ascii=True,
            )
        )
    else:
        print(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
