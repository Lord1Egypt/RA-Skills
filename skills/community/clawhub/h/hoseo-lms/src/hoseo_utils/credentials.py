import json
import os

from hoseo_utils.constants import CREDENTIALS_PATH


def load_credentials(path: str = None) -> dict:
    creds_path = os.path.expanduser(path or CREDENTIALS_PATH)
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Credentials file not found: {creds_path}")
    with open(creds_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def set_secure_permissions(path: str):
    os.chmod(path, 0o600)

