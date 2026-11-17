"""Nano account addresses: parse, checksum, normalise. Standard library only."""
import hashlib

ALPHABET = "13456789abcdefghijkmnopqrstuwxyz"
_INDEX = {c: i for i, c in enumerate(ALPHABET)}


class InvalidAccount(ValueError):
    pass


def _decode(chars):
    n = 0
    for c in chars:
        if c not in _INDEX:
            raise InvalidAccount(f"invalid character {c!r} in account")
        n = n * 32 + _INDEX[c]
    return n


def _encode(n, length):
    out = []
    for _ in range(length):
        out.append(ALPHABET[n & 31])
        n >>= 5
    return "".join(reversed(out))


def public_key(account):
    """Return the 32-byte public key of a nano_/xrb_ address, verifying its checksum."""
    if not isinstance(account, str):
        raise InvalidAccount("account must be a string")
    if account.startswith("nano_"):
        body = account[5:]
    elif account.startswith("xrb_"):
        body = account[4:]
    else:
        raise InvalidAccount("account must start with nano_ or xrb_")
    if len(body) != 60:
        raise InvalidAccount("account must have 60 characters after the prefix")
    key_n = _decode(body[:52])
    if key_n >> 256:
        raise InvalidAccount("account key has non-zero padding bits")
    key = key_n.to_bytes(32, "big")
    check = _decode(body[52:]).to_bytes(5, "big")
    expected = hashlib.blake2b(key, digest_size=5).digest()[::-1]
    if check != expected:
        raise InvalidAccount("account checksum does not match")
    return key


def from_public_key(key):
    if len(key) != 32:
        raise InvalidAccount("public key must be 32 bytes")
    check = hashlib.blake2b(key, digest_size=5).digest()[::-1]
    return "nano_" + _encode(int.from_bytes(key, "big"), 52) + _encode(int.from_bytes(check, "big"), 8)


def normalise(account):
    """Validate and return the canonical nano_ form (xrb_ is accepted and converted)."""
    return from_public_key(public_key(account))


def is_valid(account):
    try:
        public_key(account)
        return True
    except InvalidAccount:
        return False
