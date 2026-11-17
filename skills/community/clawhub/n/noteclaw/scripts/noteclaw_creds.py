#!/usr/bin/env python3
"""noteclaw_creds.py — single source for client_id/client_secret (shared by
auth_code.py and graph_sync.py).

Priority (the first usable one wins):
    1. environment variables CLIENT_ID + CLIENT_SECRET (effective only as a pair)
    2. a section in ~/.config/rclone/rclone.conf holding both client_id and
       client_secret (read-only, never mixed across sections)
    3. the default credentials of the OneDrive application that rclone publishes
       publicly (shared by all rclone users, see https://rclone.org/onedrive/) —
       fallback only, so the tool works out of the box

The rclone public application credentials are published in Microsoft's public
Azure documentation and shared by every rclone user; they are nobody's private
credential. During authorization auth_code records the client_id actually used
into the token file; when refreshing the token graph_sync prefers that value (see
refresh_client_creds), so authorization and renewal always use the same client
and never hit 401 because the environment drifted.
"""
import json
import os

RCLONE_CONF = os.path.expanduser("~/.config/rclone/rclone.conf")

# Default credentials of the OneDrive application published in rclone's public
# documentation (shared by all rclone users)
RCLONE_PUBLIC_ID = "b15665d9-eda6-4092-8539-0eec376afd59"
RCLONE_PUBLIC_SECRET = "qtyfaBBYA403=unZUP40~_#"

_FALLBACK = (RCLONE_PUBLIC_ID, RCLONE_PUBLIC_SECRET)


def _from_env():
    cid = os.environ.get("CLIENT_ID")
    csec = os.environ.get("CLIENT_SECRET")
    if cid and csec:
        return cid, csec
    return None


def _from_rclone_conf(path=None):
    """Read rclone.conf and return the first section holding both
    client_id + client_secret."""
    p = path or RCLONE_CONF
    if not os.path.exists(p):
        return None
    cur = {}
    with open(p) as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            if line.startswith("[") and line.endswith("]"):
                if cur.get("client_id") and cur.get("client_secret"):
                    return cur["client_id"], cur["client_secret"]
                cur = {}
            elif "=" in line:
                k, v = line.split("=", 1)
                cur[k.strip()] = v.strip().strip('"')
    if cur.get("client_id") and cur.get("client_secret"):
        return cur["client_id"], cur["client_secret"]
    return None


def load_client_creds(allow_fallback=True):
    """Return client_id + client_secret as a pair.

    allow_fallback=True (default): when rclone.conf and the environment variables
    have nothing → return the rclone public application credentials (works out of
    the box). False: return None when no credentials are available (the caller
    decides whether to fail) — used by graph_sync when the client recorded at
    authorization time exists, so the recorded value is reused and the search
    chain is only consulted when the record is missing.
    """
    got = _from_env() or _from_rclone_conf()
    if got:
        return got
    return _FALLBACK if allow_fallback else None


def note_client_id(token_file):
    """Record the client_id actually used into the token file (idempotent,
    existing fields are never overwritten).

    Called by auth_code after a successful authorization: it tells graph_sync
    which client to use when refreshing the token, avoiding a 401 caused by
    "authorized with A, refreshed with B".
    """
    try:
        with open(token_file) as f:
            tok = json.load(f)
        if tok.get("client_id"):
            return
        cid, _csec = load_client_creds()
        tok["client_id"] = cid
        with open(token_file, "w") as f:
            json.dump(tok, f, indent=2, ensure_ascii=False)
    except Exception:
        # Recording the client_id is an enhancement; a failure here does not
        # affect the main authorization flow
        pass


def refresh_client_creds(token_file):
    """Credentials for refreshing the token: prefer the client_id recorded in the
    token file (the one actually used at authorization time) and fall back to the
    full search chain (environment variables → rclone.conf → built-in fallback)
    only when it is missing. Returns (cid, csec); returns (None, None) when still
    no usable credentials.
    """
    try:
        with open(token_file) as f:
            tok = json.load(f)
        cid = tok.get("client_id")
        if cid:
            # environment variables may override explicitly (when the user wants a
            # different client); otherwise use the recorded client
            env = _from_env()
            if env:
                return env
            csec = _secret_for(cid)
            if csec:
                return cid, csec
    except Exception:
        pass
    got = load_client_creds(allow_fallback=True)
    return got if got else (None, None)


def _secret_for(cid):
    """Look the matching secret up by client_id (built-in table + rclone.conf +
    environment variables)."""
    env = _from_env()
    if env and env[0] == cid:
        return env[1]
    rc = _from_rclone_conf()
    if rc and rc[0] == cid:
        return rc[1]
    if cid == RCLONE_PUBLIC_ID:
        return RCLONE_PUBLIC_SECRET
    return None
