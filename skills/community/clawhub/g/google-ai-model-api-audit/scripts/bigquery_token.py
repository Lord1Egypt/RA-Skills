#!/usr/bin/env python3
"""bigquery_token.py - mint a BigQuery access token from a service-account JSON key.

No gcloud, no bq CLI, no SDK. Works even when the user's gcloud session is expired,
which is the usual reason the bq CLI refuses --service_account_credential_file.

Usage:
    python3 bigquery_token.py --key /path/to/key.json
    python3 bigquery_token.py --key ... --quiet      # warm the cache only

Importable:
    from bigquery_token import get_token
    get_token('/path/key.json')

Scope defaults to BigQuery. Token is cached in /tmp with 0600 perms.
"""
import argparse
import base64
import json
import os
import time
import urllib.parse
import urllib.request

DEFAULT_SCOPE = "https://www.googleapis.com/auth/bigquery"


def _b64(data: bytes) -> bytes:
    return base64.urlsafe_b64encode(data).rstrip(b"=")


def _signed_jwt(key: dict, scope: str) -> str:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT", "kid": key["private_key_id"]}
    claim = {
        "iss": key["client_email"],
        "scope": scope,
        "aud": key["token_uri"],
        "iat": now,
        "exp": now + 3600,
    }
    signing_input = b".".join([
        _b64(json.dumps(header).encode()),
        _b64(json.dumps(claim).encode()),
    ])
    pk = serialization.load_pem_private_key(key["private_key"].encode(), password=None)
    sig = pk.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return (signing_input + b"." + _b64(sig)).decode()


def get_token(key_path: str, scope: str = DEFAULT_SCOPE, force: bool = False) -> str:
    key_path = os.path.expanduser(key_path)
    cache = "/tmp/bqtok-" + os.path.basename(key_path) + ".json"
    if not force and os.path.exists(cache):
        try:
            c = json.load(open(cache))
            if c.get("exp", 0) > time.time() + 60:
                return c["token"]
        except Exception:
            pass
    key = json.load(open(key_path))
    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": _signed_jwt(key, scope),
    }).encode()
    req = urllib.request.Request(
        key["token_uri"], data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.load(r)
    json.dump({"token": resp["access_token"], "exp": time.time() + resp["expires_in"]}, open(cache, "w"))
    os.chmod(cache, 0o600)
    return resp["access_token"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="service-account JSON key path")
    ap.add_argument("--scope", default=DEFAULT_SCOPE)
    ap.add_argument("--force", action="store_true", help="ignore cached token")
    ap.add_argument("--quiet", action="store_true", help="do not print the token")
    a = ap.parse_args()
    t = get_token(a.key, a.scope, a.force)
    if not a.quiet:
        print(t)
