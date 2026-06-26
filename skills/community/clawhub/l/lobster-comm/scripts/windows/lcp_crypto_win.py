"""
LCP/1.1 Crypto Module for Windows
Same as lcp_crypto.py but with Windows-friendly paths.

Requirements: pip install pynacl
"""

import os
import json
import base64
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

# Windows key directory (same folder as script)
KEY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")
IDENTITY_FILE = os.path.join(KEY_DIR, "identity.pem")

def _canonicalize(msg_dict):
    msg_copy = msg_dict.copy()
    msg_copy.pop("security", None)
    return json.dumps(msg_copy, sort_keys=True, separators=(',', ':')).encode('utf-8')

def get_or_create_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR, exist_ok=True)

    if os.path.exists(IDENTITY_FILE):
        with open(IDENTITY_FILE, "rb") as f:
            seed = f.read()
            signing_key = SigningKey(seed)
    else:
        signing_key = SigningKey.generate()
        with open(IDENTITY_FILE, "wb") as f:
            f.write(signing_key.encode())
        print(f"Generated new Ed25519 keypair at {IDENTITY_FILE}")

    return signing_key, signing_key.verify_key

def sign_message(msg_dict):
    signing_key, verify_key = get_or_create_keys()
    payload = _canonicalize(msg_dict)
    signed = signing_key.sign(payload)
    msg_dict["security"] = {
        "algo": "ed25519",
        "pubkey": base64.b64encode(verify_key.encode()).decode('utf-8'),
        "signature": base64.b64encode(signed.signature).decode('utf-8')
    }
    return msg_dict

def verify_message(msg_dict):
    if "security" not in msg_dict:
        raise ValueError("Missing security block")
    sec = msg_dict["security"]
    if sec.get("algo") != "ed25519":
        raise ValueError(f"Unsupported algo: {sec.get('algo')}")

    pubkey_bytes = base64.b64decode(sec["pubkey"])
    sig_bytes = base64.b64decode(sec["signature"])
    payload = _canonicalize(msg_dict)
    verify_key = VerifyKey(pubkey_bytes)

    try:
        verify_key.verify(payload, sig_bytes)
        return True
    except BadSignatureError:
        return False

if __name__ == "__main__":
    test_msg = {
        "id": "test_001", "from": "AgentB", "to": "AgentA",
        "timestamp": "2026-03-28T12:00:00+08:00", "type": "ping", "message": "hello"
    }
    signed = sign_message(test_msg.copy())
    print("Signed:", json.dumps(signed, indent=2))
    print("Verify:", "OK" if verify_message(signed) else "FAIL")
