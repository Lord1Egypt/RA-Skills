#!/usr/bin/env python3
"""Decode, inspect, and validate JWT tokens without external dependencies."""

import argparse
import base64
import json
import sys
import time
from datetime import datetime, timezone


def b64url_decode(data: str) -> bytes:
    """Decode base64url-encoded data with padding."""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data)


def decode_jwt(token: str) -> dict:
    """Decode a JWT token into its components."""
    token = token.strip()
    parts = token.split(".")
    if len(parts) not in (2, 3):
        raise ValueError(f"Invalid JWT: expected 2-3 parts, got {len(parts)}")

    try:
        header = json.loads(b64url_decode(parts[0]))
    except Exception as e:
        raise ValueError(f"Invalid JWT header: {e}")

    try:
        payload = json.loads(b64url_decode(parts[1]))
    except Exception as e:
        raise ValueError(f"Invalid JWT payload: {e}")

    signature = parts[2] if len(parts) == 3 else None

    return {"header": header, "payload": payload, "signature": signature}


def format_timestamp(ts: int | float) -> str:
    """Format a Unix timestamp to human-readable string."""
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (OSError, ValueError):
        return f"<invalid timestamp: {ts}>"


def check_expiry(payload: dict) -> dict:
    """Check token expiration status."""
    now = time.time()
    result = {"expired": None, "expires_in": None, "not_before": None}

    if "exp" in payload:
        exp = payload["exp"]
        result["expired"] = now > exp
        diff = exp - now
        if diff > 0:
            hours, rem = divmod(int(diff), 3600)
            minutes, seconds = divmod(rem, 60)
            result["expires_in"] = f"{hours}h {minutes}m {seconds}s"
        else:
            hours, rem = divmod(int(-diff), 3600)
            minutes, seconds = divmod(rem, 60)
            result["expires_in"] = f"expired {hours}h {minutes}m {seconds}s ago"

    if "nbf" in payload:
        nbf = payload["nbf"]
        result["not_before"] = now >= nbf

    return result


KNOWN_CLAIMS = {
    "iss": "Issuer",
    "sub": "Subject",
    "aud": "Audience",
    "exp": "Expiration Time",
    "nbf": "Not Before",
    "iat": "Issued At",
    "jti": "JWT ID",
    "name": "Full Name",
    "email": "Email",
    "roles": "Roles",
    "scope": "Scope",
    "azp": "Authorized Party",
    "nonce": "Nonce",
    "at_hash": "Access Token Hash",
    "c_hash": "Code Hash",
    "auth_time": "Auth Time",
    "acr": "Auth Context Class Ref",
    "amr": "Auth Methods Ref",
    "sid": "Session ID",
    "org_id": "Organization ID",
    "tenant": "Tenant",
}

KNOWN_ALGORITHMS = {
    "HS256": "HMAC-SHA256 (symmetric)",
    "HS384": "HMAC-SHA384 (symmetric)",
    "HS512": "HMAC-SHA512 (symmetric)",
    "RS256": "RSA-SHA256 (asymmetric)",
    "RS384": "RSA-SHA384 (asymmetric)",
    "RS512": "RSA-SHA512 (asymmetric)",
    "ES256": "ECDSA-P256-SHA256 (asymmetric)",
    "ES384": "ECDSA-P384-SHA384 (asymmetric)",
    "ES512": "ECDSA-P521-SHA512 (asymmetric)",
    "PS256": "RSA-PSS-SHA256 (asymmetric)",
    "PS384": "RSA-PSS-SHA384 (asymmetric)",
    "PS512": "RSA-PSS-SHA512 (asymmetric)",
    "EdDSA": "Edwards-curve DSA (asymmetric)",
    "none": "UNSIGNED (no signature)",
}


def format_text(decoded: dict, expiry: dict) -> str:
    """Format decoded JWT as human-readable text."""
    lines = []

    # Header
    header = decoded["header"]
    alg = header.get("alg", "unknown")
    alg_desc = KNOWN_ALGORITHMS.get(alg, "Unknown algorithm")
    lines.append("=== JWT HEADER ===")
    lines.append(f"Algorithm: {alg} ({alg_desc})")
    lines.append(f"Type: {header.get('typ', 'N/A')}")
    if "kid" in header:
        lines.append(f"Key ID: {header['kid']}")
    for k, v in header.items():
        if k not in ("alg", "typ", "kid"):
            lines.append(f"{k}: {v}")

    # Security warnings
    if alg == "none":
        lines.append("")
        lines.append("⚠  WARNING: Token uses 'none' algorithm — NOT SIGNED!")
    if alg.startswith("HS") and decoded["signature"]:
        lines.append("")
        lines.append("ℹ  Note: Symmetric algorithm — verify with shared secret")

    # Payload
    lines.append("")
    lines.append("=== JWT PAYLOAD ===")
    payload = decoded["payload"]
    time_claims = {"exp", "nbf", "iat", "auth_time"}

    for key, value in payload.items():
        label = KNOWN_CLAIMS.get(key, key)
        if key in time_claims and isinstance(value, (int, float)):
            lines.append(f"{label} ({key}): {format_timestamp(value)} (raw: {value})")
        else:
            if isinstance(value, (dict, list)):
                lines.append(f"{label} ({key}): {json.dumps(value)}")
            else:
                lines.append(f"{label} ({key}): {value}")

    # Expiry status
    lines.append("")
    lines.append("=== TOKEN STATUS ===")
    if expiry["expired"] is not None:
        if expiry["expired"]:
            lines.append(f"Status: EXPIRED — {expiry['expires_in']}")
        else:
            lines.append(f"Status: VALID — expires in {expiry['expires_in']}")
    else:
        lines.append("Status: No expiration set")

    if expiry["not_before"] is not None:
        if expiry["not_before"]:
            lines.append("Not-Before: Active (current time is past nbf)")
        else:
            lines.append("Not-Before: NOT YET VALID (current time is before nbf)")

    # Signature
    lines.append("")
    if decoded["signature"]:
        sig_bytes = len(b64url_decode(decoded["signature"]))
        lines.append(f"Signature: present ({sig_bytes} bytes)")
    else:
        lines.append("Signature: absent")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Decode, inspect, and validate JWT tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s eyJhbGciOiJIUzI1NiIs...
  %(prog)s --file token.txt
  echo "eyJ..." | %(prog)s --stdin
  %(prog)s eyJ... --format json
""",
    )
    parser.add_argument("token", nargs="?", help="JWT token string")
    parser.add_argument("--file", help="Read token from file")
    parser.add_argument("--stdin", action="store_true", help="Read token from stdin")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")
    args = parser.parse_args()

    # Get token from one source
    if args.stdin:
        token = sys.stdin.read().strip()
    elif args.file:
        try:
            with open(args.file) as f:
                token = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.token:
        token = args.token
    else:
        parser.print_help()
        sys.exit(1)

    # Strip "Bearer " prefix if present
    if token.lower().startswith("bearer "):
        token = token[7:]

    try:
        decoded = decode_jwt(token)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    expiry = check_expiry(decoded["payload"])

    if args.format == "json":
        output = {
            "header": decoded["header"],
            "payload": decoded["payload"],
            "signature_present": decoded["signature"] is not None,
            "expiry": expiry,
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print(format_text(decoded, expiry))


if __name__ == "__main__":
    main()
