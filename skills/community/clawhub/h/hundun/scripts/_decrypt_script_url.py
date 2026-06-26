#!/usr/bin/env python3
"""Decrypt script_url: hex = IV(16B) + AES-CBC ciphertext. Usage: python _decrypt_script_url.py [hex] or stdin"""
import sys

# 32-byte key (hex, 64 chars). Same as server.
SCRIPT_URL_KEY_HEX = "4d0f8b3e9c1a4b0c9f3a2e1d0c9b8a7f6e5d4c3b2a1908f7e6d5c4b3a29180700"

def main():
    cipher_raw = sys.stdin.read().strip() if not sys.stdin.isatty() else (sys.argv[1] if len(sys.argv) > 1 else "")
    if not cipher_raw:
        sys.exit(1)
    cipher_raw = "".join(c for c in cipher_raw if c in "0123456789abcdefABCDEF")
    if not cipher_raw:
        sys.exit(1)
    data = bytes.fromhex(cipher_raw)
    if len(data) < 17:
        sys.exit(1)
    iv = data[:16]
    ciphertext = data[16:]
    key_hex = SCRIPT_URL_KEY_HEX
    if len(key_hex) % 2:
        key_hex = key_hex[:64]
    key = bytes.fromhex(key_hex)
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
    except ImportError:
        try:
            from Cryptodome.Cipher import AES
            from Cryptodome.Util.Padding import unpad
        except ImportError:
            sys.stderr.write("pip install pycryptodome\n")
            sys.exit(1)
    aes = AES.new(key, AES.MODE_CBC, iv)
    plain = aes.decrypt(ciphertext)
    plain = unpad(plain, AES.block_size)
    print(plain.decode("utf-8"), end="")

if __name__ == "__main__":
    main()
