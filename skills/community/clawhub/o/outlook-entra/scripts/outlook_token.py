"""
outlook_token.py — Lecture, écriture, refresh des tokens OAuth Microsoft.
Gère le chiffrement AES-GCM si TOKEN_FILE_KEY est défini.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

# ── Config loader ───────────────────────────────────────────────────────────────

def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    v = v.strip('"').strip("'")
                    os.environ.setdefault(k, v)

load_env()

TENANT_ID       = os.getenv("AZURE_TENANT_ID", "")
CLIENT_ID       = os.getenv("AZURE_CLIENT_ID", "")
CLIENT_SECRET   = os.getenv("AZURE_CLIENT_SECRET", "")
DEVICE_CODE_URL = os.getenv("OAUTH_DEVICE_CODE_URL",
    f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/devicecode")
TOKEN_URL       = os.getenv("OAUTH_TOKEN_URL",
    f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token")
GRAPH_BASE      = os.getenv("MS_GRAPH_BASE_URL", "https://graph.microsoft.com/v1.0")
TOKEN_FILE      = os.path.expanduser(os.getenv("TOKEN_FILE", "~/.openclaw/outlook_tokens.json"))
TOKEN_FILE_KEY  = os.getenv("TOKEN_FILE_KEY", "")
SCOPES_DEVICE_CODE = os.getenv("SCOPES_DEVICE_CODE", "user.read openid profile offline_access")
REQUEST_TIMEOUT  = int(os.getenv("REQUEST_TIMEOUT", "30"))

# ── Token file helpers ─────────────────────────────────────────────────────────

def _fernet() -> Optional[Fernet]:
    if not TOKEN_FILE_KEY or not HAS_CRYPTO:
        return None
    import hashlib, base64
    salt = b"outlook-entra-salt-v1"
    key  = hashlib.pbkdf2_hmac("sha256", TOKEN_FILE_KEY.encode(), salt, 100_000, dklen=32)
    fkey = base64.urlsafe_b64encode(key)
    return Fernet(fkey)

def _read_raw(path: str) -> dict:
    with open(path) as f:
        content = f.read().strip()
    fernet = _fernet()
    if fernet:
        content = fernet.decrypt(content.encode()).decode()
    return json.loads(content)

def _write_raw(path: str, data: dict):
    content = json.dumps(data, indent=2)
    fernet = _fernet()
    if fernet:
        content = fernet.encrypt(content.encode()).decode()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# ── Public API ────────────────────────────────────────────────────────────────

def get_token() -> Optional[dict]:
    if not Path(TOKEN_FILE).exists():
        return None
    return _read_raw(TOKEN_FILE)

def save_token(token_data: dict):
    _write_raw(TOKEN_FILE, token_data)

def is_token_expired(token: dict, margin_seconds: int = 120) -> bool:
    if "expires_at" not in token:
        return True
    return time.time() >= token["expires_at"] - margin_seconds

def ensure_valid_token(requests_mod=None) -> str:
    import requests as req
    req = requests_mod or req

    token = get_token()
    if not token:
        raise RuntimeError(
            "Aucun token trouvé. Lancez d'abord `python scripts/outlook_auth.py` pour vous authentifier."
        )

    if not is_token_expired(token):
        return token["access_token"]

    print(f"[outlook_token] Token expiré — refresh en cours…", file=sys.stderr)
    payload = {
        "grant_type":    "refresh_token",
        "client_id":     CLIENT_ID,
        "refresh_token": token["refresh_token"],
    }
    resp = req.post(TOKEN_URL, data=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    new_token = resp.json()
    new_token["expires_at"] = time.time() + new_token.get("expires_in", 3600)
    save_token(new_token)
    return new_token["access_token"]

def revoke_token():
    import requests as req
    token = get_token()
    if not token:
        return
    payload = {
        "client_id":   CLIENT_ID,
        "grant_type":  "refresh_token",
        "token":       token.get("refresh_token", ""),
    }
    try:
        req.post(TOKEN_URL, data=payload, timeout=REQUEST_TIMEOUT)
    except Exception:
        pass
    Path(TOKEN_FILE).unlink(missing_ok=True)

def refresh_token() -> dict:
    """Effectue un refresh du token et sauvegarde le nouveau token.
    Retourne le nouveau token data.
    """
    import requests as req
    token = get_token()
    if not token or not token.get("refresh_token"):
        raise RuntimeError("Aucun refresh_token disponible.")

    payload = {
        "grant_type":    "refresh_token",
        "client_id":     CLIENT_ID,
        "refresh_token": token["refresh_token"],
    }
    resp = req.post(TOKEN_URL, data=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    new_token = resp.json()
    new_token["expires_at"] = time.time() + new_token.get("expires_in", 3600)
    save_token(new_token)
    return new_token
