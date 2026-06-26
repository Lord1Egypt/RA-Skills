"""
Enable Banking — Shared Auth & API Module
JWT generation, authenticated API requests, mandant I/O.
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    import jwt
    import requests
except ImportError:
    print("❌ Missing dependencies. Run: pip install PyJWT cryptography requests", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------
SKILL_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
MANDANTEN_DIR = SKILL_DIR / "mandanten"
DATA_DIR = SKILL_DIR / "data"
PENDING_DIR = SKILL_DIR / "pending_callbacks"
API_BASE = "https://api.enablebanking.com"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config() -> dict:
    """Load config.json from the skill directory."""
    if not CONFIG_PATH.exists():
        print(f"❌ Config not found at {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    required = ["applicationId", "keyPath"]
    for key in required:
        if not config.get(key):
            print(f"❌ Missing required config field: {key}", file=sys.stderr)
            sys.exit(1)
    return config


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------

def generate_jwt(config: dict) -> str:
    """Generate RS256 JWT for Enable Banking API."""
    pem_path = Path(config["keyPath"]).expanduser().resolve()
    if not pem_path.exists():
        print(f"❌ Private key not found: {pem_path}", file=sys.stderr)
        sys.exit(1)

    with open(pem_path, "rb") as f:
        private_key = f.read()

    now = int(time.time())
    payload = {
        "iss": "enablebanking.com",
        "aud": "api.enablebanking.com",
        "iat": now,
        "exp": now + 3600,
    }
    headers = {
        "typ": "JWT",
        "alg": "RS256",
        "kid": config["applicationId"],
    }
    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def api_request(method: str, endpoint: str, token: str, retries: int = MAX_RETRIES, **kwargs) -> dict | None:
    """Authenticated API request with retry logic (429 + timeout)."""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    for attempt in range(1, retries + 1):
        try:
            resp = requests.request(method, url, headers=headers, timeout=20, **kwargs)
            if resp.status_code in (200, 201):
                return resp.json()
            elif resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", 60))
                print(f"⚠️  Rate limited. Waiting {wait}s... (attempt {attempt}/{retries})", file=sys.stderr)
                time.sleep(wait)
                continue
            elif resp.status_code == 401:
                print("❌ 401 Unauthorized — JWT invalid. Check applicationId and key.", file=sys.stderr)
                sys.exit(1)
            elif resp.status_code == 403:
                print("❌ 403 Forbidden — Session expired or consent denied.", file=sys.stderr)
                sys.exit(1)
            else:
                error_detail = ""
                try:
                    error_detail = resp.json().get("message", resp.text[:200])
                except Exception:
                    error_detail = resp.text[:200]
                print(f"❌ API {resp.status_code}: {error_detail}", file=sys.stderr)
                if attempt < retries:
                    print(f"  Retrying in {RETRY_DELAY}s...", file=sys.stderr)
                    time.sleep(RETRY_DELAY)
                else:
                    return None
        except requests.exceptions.ConnectionError:
            print("❌ Cannot reach api.enablebanking.com", file=sys.stderr)
            if attempt < retries:
                time.sleep(RETRY_DELAY)
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out (attempt {attempt}/{retries})", file=sys.stderr)
            if attempt < retries:
                time.sleep(RETRY_DELAY)
    return None


# ---------------------------------------------------------------------------
# Mandant I/O
# ---------------------------------------------------------------------------

def load_mandant(mandant_id: str) -> dict:
    """Load mandanten/{mandant_id}.json."""
    MANDANTEN_DIR.mkdir(parents=True, exist_ok=True)
    path = MANDANTEN_DIR / f"{mandant_id}.json"
    if not path.exists():
        print(f"❌ Mandant not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def save_mandant(mandant_id: str, data: dict) -> None:
    """Save mandanten/{mandant_id}.json (chmod 600)."""
    MANDANTEN_DIR.mkdir(parents=True, exist_ok=True)
    path = MANDANTEN_DIR / f"{mandant_id}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.chmod(path, 0o600)


def list_mandanten() -> list[str]:
    """Return list of mandant IDs from mandanten/ directory."""
    MANDANTEN_DIR.mkdir(parents=True, exist_ok=True)
    return [
        p.stem for p in sorted(MANDANTEN_DIR.glob("*.json"))
    ]
