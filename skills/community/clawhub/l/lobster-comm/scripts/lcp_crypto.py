import os
import json
import base64
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

KEY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "keys")
IDENTITY_FILE = os.path.join(KEY_DIR, "identity.pem")

def _canonicalize(msg_dict):
    """Strip security block and canonicalize JSON for signing"""
    msg_copy = msg_dict.copy()
    msg_copy.pop("security", None)
    return json.dumps(msg_copy, sort_keys=True, separators=(',', ':')).encode('utf-8')

def get_or_create_keys():
    """Load or generate Ed25519 keys"""
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
            
    verify_key = signing_key.verify_key
    return signing_key, verify_key

def sign_message(msg_dict):
    """Sign the message using local Ed25519 private key"""
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
    """Verify the signature in the security block"""
    if "security" not in msg_dict:
        raise ValueError("Missing security block")
        
    sec = msg_dict["security"]
    if sec.get("algo") != "ed25519":
        raise ValueError(f"Unsupported algorithm: {sec.get('algo')}")
        
    pubkey_bytes = base64.b64decode(sec["pubkey"])
    sig_bytes = base64.b64decode(sec["signature"])
    
    payload = _canonicalize(msg_dict)
    verify_key = VerifyKey(pubkey_bytes)
    
    try:
        verify_key.verify(payload, sig_bytes)
        return True
    except BadSignatureError:
        return False

# Quick test if run directly
if __name__ == "__main__":
    test_msg = {
        "id": "msg_001",
        "from": "AgentA",
        "to": "CloudAgentA",
        "timestamp": "2026-03-27T12:00:00+08:00",
        "type": "task",
        "message": "Hello P2P World"
    }
    
    # 1. Sign
    print("Original:", test_msg)
    signed_msg = sign_message(test_msg.copy())
    print("\nSigned:\n", json.dumps(signed_msg, indent=2))
    
    # 2. Verify Success
    is_valid = verify_message(signed_msg)
    print("\nVerify Valid Payload:", "OK" if is_valid else "FAIL")
    
    # 3. Verify Tampering
    tampered_msg = signed_msg.copy()
    tampered_msg["message"] = "Hacked!"
    is_valid_tampered = verify_message(tampered_msg)
    print("Verify Tampered Payload:", "FAIL" if not is_valid_tampered else "OK (VULNERABLE!)")
