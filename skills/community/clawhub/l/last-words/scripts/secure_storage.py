#!/usr/bin/env python3
"""
Secure storage for sensitive data using encryption.
Uses Fernet symmetric encryption from cryptography library.
"""

import os
import base64
import hashlib
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("Warning: cryptography not installed. Sensitive data will be stored as plaintext.")
    print("Install: pip3 install cryptography")


SALT_FILE = Path.home() / ".openclaw" / "last-words" / ".salt"


def _get_or_create_salt():
    """Get or create a random salt for key derivation."""
    if SALT_FILE.exists():
        return SALT_FILE.read_bytes()

    salt = os.urandom(16)
    SALT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SALT_FILE.write_bytes(salt)
    os.chmod(SALT_FILE, 0o600)  # Owner read/write only
    return salt


def _derive_key(password: str) -> bytes:
    """Derive encryption key from password."""
    if not HAS_CRYPTO:
        return None

    salt = _get_or_create_salt()
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_sensitive_data(data: str, master_password: str) -> str:
    """Encrypt sensitive data using master password."""
    if not HAS_CRYPTO or not master_password:
        return data  # Fallback to plaintext

    key = _derive_key(master_password)
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_sensitive_data(encrypted_data: str, master_password: str) -> str:
    """Decrypt sensitive data using master password."""
    if not HAS_CRYPTO or not master_password:
        return encrypted_data  # Assume plaintext fallback

    try:
        key = _derive_key(master_password)
        f = Fernet(key)
        decrypted = f.decrypt(base64.urlsafe_b64decode(encrypted_data.encode()))
        return decrypted.decode()
    except Exception:
        # Decryption failed - wrong password or corrupted data
        return None


def check_master_password_set():
    """Check if master password environment variable is set."""
    return bool(os.environ.get('LAST_WORDS_MASTER_PASSWORD'))


def secure_store(smtp_pass: str) -> str:
    """Store SMTP password securely if master password is set."""
    master = os.environ.get('LAST_WORDS_MASTER_PASSWORD')
    if master:
        return encrypt_sensitive_data(smtp_pass, master)
    return smtp_pass  # Store as plaintext (fallback)


def secure_retrieve(stored_value: str) -> str:
    """Retrieve and decrypt SMTP password."""
    master = os.environ.get('LAST_WORDS_MASTER_PASSWORD')
    if master and HAS_CRYPTO:
        decrypted = decrypt_sensitive_data(stored_value, master)
        if decrypted is None:
            raise ValueError("Failed to decrypt: wrong master password or corrupted data")
        return decrypted
    return stored_value  # Assume plaintext
