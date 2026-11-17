"""Nano (XNO) account address codec and checksum validation.

Dependency-free: standard library only (hashlib.blake2b).

This module exists because of one recorded failure in the swarm's funnel:
an outside agent (eddie_researcher) said yes and handed over a payout
address that FAILS CHECKSUM. Nothing else in the pipeline caught it.
Every address this package emits or accepts passes `validate()` first,
and an invalid address is rejected with a machine-readable reason,
never forwarded.

Address shape:  <prefix>_ <52 chars: 4 pad bits + 256-bit public key> <8 chars: 40-bit checksum>
Checksum:       blake2b(public_key, digest_size=5).digest() reversed, base32-encoded.
Alphabet:       Nano base32 - "13456789abcdefghijkmnopqrstuwxyz" (no 0, 2, l, v).
"""

from hashlib import blake2b

ALPHABET = "13456789abcdefghijkmnopqrstuwxyz"
_DECODE = {c: i for i, c in enumerate(ALPHABET)}

PREFIXES = ("nano_", "xrb_")
ACCOUNT_BODY_LEN = 52
CHECKSUM_LEN = 8
PUBLIC_KEY_BYTES = 32


class InvalidAddress(ValueError):
    """Raised when an address cannot be parsed or fails its checksum.

    `reason` is a stable machine-readable code, safe to put in an API
    response body: callers switch on it, humans read `str(exc)`.
    """

    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason
        self.message = message


def _b32_encode(value: int, length: int) -> str:
    out = []
    for shift in range((length - 1) * 5, -1, -5):
        out.append(ALPHABET[(value >> shift) & 0x1F])
    return "".join(out)


def _b32_decode(text: str) -> int:
    value = 0
    for ch in text:
        try:
            value = (value << 5) | _DECODE[ch]
        except KeyError:
            raise InvalidAddress(
                "bad_character",
                "character %r is not in the Nano base32 alphabet "
                "(0, 2, l and v are never valid)" % ch,
            ) from None
    return value


def checksum_for(public_key: bytes) -> str:
    """The 8-character checksum Nano appends to a public key."""
    if len(public_key) != PUBLIC_KEY_BYTES:
        raise InvalidAddress(
            "bad_public_key_length",
            "public key must be %d bytes, got %d" % (PUBLIC_KEY_BYTES, len(public_key)),
        )
    digest = blake2b(public_key, digest_size=5).digest()
    return _b32_encode(int.from_bytes(digest[::-1], "big"), CHECKSUM_LEN)


def encode(public_key: bytes, prefix: str = "nano_") -> str:
    """Render a 32-byte public key as a checksummed account address."""
    if prefix not in PREFIXES:
        raise InvalidAddress("bad_prefix", "prefix must be one of %s" % (PREFIXES,))
    if len(public_key) != PUBLIC_KEY_BYTES:
        raise InvalidAddress(
            "bad_public_key_length",
            "public key must be %d bytes, got %d" % (PUBLIC_KEY_BYTES, len(public_key)),
        )
    body = _b32_encode(int.from_bytes(public_key, "big"), ACCOUNT_BODY_LEN)
    return prefix + body + checksum_for(public_key)


def decode(address: str) -> bytes:
    """Return the 32-byte public key behind an address, or raise InvalidAddress.

    Every failure mode carries a distinct `reason`, so a caller can tell a
    typo apart from a truncation apart from a corrupted checksum.
    """
    if not isinstance(address, str):
        raise InvalidAddress("not_a_string", "address must be a string, got %s" % type(address).__name__)

    candidate = address.strip()
    if not candidate:
        raise InvalidAddress("empty", "address is empty")

    for prefix in PREFIXES:
        if candidate.startswith(prefix):
            rest = candidate[len(prefix):]
            break
    else:
        raise InvalidAddress(
            "bad_prefix",
            "address must start with 'nano_' or the legacy 'xrb_'",
        )

    expected = ACCOUNT_BODY_LEN + CHECKSUM_LEN
    if len(rest) != expected:
        raise InvalidAddress(
            "bad_length",
            "expected %d characters after the prefix, got %d" % (expected, len(rest)),
        )

    body, supplied_checksum = rest[:ACCOUNT_BODY_LEN], rest[ACCOUNT_BODY_LEN:]

    if body[0] not in "13":
        # The first character encodes the 4 zero pad bits plus the top bit of
        # the key, so only '1' and '3' can ever appear there.
        raise InvalidAddress(
            "bad_padding",
            "first character after the prefix must be '1' or '3', got %r" % body[0],
        )

    public_key = _b32_decode(body).to_bytes(33, "big")[1:]
    computed = checksum_for(public_key)
    if computed != supplied_checksum:
        raise InvalidAddress(
            "bad_checksum",
            "checksum mismatch: address carries %r, the key implies %r"
            % (supplied_checksum, computed),
        )
    return public_key


def validate(address: str) -> dict:
    """Never raises. Returns a JSON-serialisable verdict.

    {"valid": true,  "address": "<normalised>", "public_key": "<64 hex>", "prefix": "nano_"}
    {"valid": false, "reason": "<code>", "message": "<human readable>"}
    """
    try:
        public_key = decode(address)
    except InvalidAddress as exc:
        return {"valid": False, "reason": exc.reason, "message": exc.message}
    candidate = address.strip()
    prefix = "nano_" if candidate.startswith("nano_") else "xrb_"
    return {
        "valid": True,
        "address": candidate,
        "normalised": encode(public_key, "nano_"),
        "public_key": public_key.hex().upper(),
        "prefix": prefix,
    }


def is_valid(address: str) -> bool:
    return validate(address)["valid"]
