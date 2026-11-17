"""Non-custodial Nano wallet operations, offline by construction.

Everything in this module runs inside the caller's own process. No seed,
no private key and no address is ever transmitted anywhere by this code.
There is no network call in this file, and none in the two modules it
imports. That is the custody answer stated as something checkable rather
than asserted: read the imports.

The four operations an outside agent asked for:
    create_wallet   - generate a seed and an account, locally
    derive_account  - a further account from a seed the caller already has
    validate        - checksum-verify any address before it is used
    sign_message    - prove control of an address without revealing the key
"""

import ed25519_blake2b as _ed
import nanoaddr as _addr

from nanoaddr import InvalidAddress, validate  # re-exported

RAW_PER_XNO = 10 ** 30


def create_wallet(prefix: str = "nano_") -> dict:
    """Generate a brand-new seed and its first account, locally.

    Returns the seed and private key in hex. THE CALLER IS THE ONLY PARTY
    THAT EVER SEES THEM - store the seed, and treat losing it as losing
    the funds. The returned address is checksum-verified before it is
    handed back, so a caller can never be given an unusable address.
    """
    seed = _ed.generate_seed()
    return _account(seed, 0, prefix)


def derive_account(seed_hex: str, index: int = 0, prefix: str = "nano_") -> dict:
    """Derive account `index` from an existing 32-byte hex seed."""
    try:
        seed = bytes.fromhex(seed_hex.strip())
    except ValueError:
        raise ValueError("seed must be 64 hex characters") from None
    if len(seed) != 32:
        raise ValueError("seed must be 64 hex characters (32 bytes), got %d bytes" % len(seed))
    return _account(seed, index, prefix)


def _account(seed: bytes, index: int, prefix: str) -> dict:
    private_key = _ed.private_key_from_seed(seed, index)
    public_key = _ed.public_key_from_private(private_key)
    address = _addr.encode(public_key, prefix)
    verdict = _addr.validate(address)
    if not verdict["valid"]:                      # pragma: no cover - defensive
        raise AssertionError("generated an address that fails its own checksum")
    return {
        "seed": seed.hex().upper(),
        "index": index,
        "private_key": private_key.hex().upper(),
        "public_key": public_key.hex().upper(),
        "address": address,
    }


def account_from_public_key(public_key_hex: str, prefix: str = "nano_") -> str:
    return _addr.encode(bytes.fromhex(public_key_hex.strip()), prefix)


def sign_message(message: bytes, private_key_hex: str) -> dict:
    """Sign arbitrary bytes with an account's key.

    This is how an agent proves it controls a payout address without
    revealing the key or moving any funds: sign a challenge, publish the
    signature beside the address.
    """
    private_key = bytes.fromhex(private_key_hex.strip())
    public_key = _ed.public_key_from_private(private_key)
    signature = _ed.sign(message, private_key, public_key)
    return {
        "address": _addr.encode(public_key),
        "public_key": public_key.hex().upper(),
        "signature": signature.hex().upper(),
    }


def xno_to_raw(amount: str) -> int:
    """Exact decimal XNO -> integer raw. No float is used anywhere."""
    text = str(amount).strip()
    if not text:
        raise ValueError("amount is empty")
    negative = text.startswith("-")
    if negative:
        raise ValueError("amount must not be negative")
    if text.count(".") > 1:
        raise ValueError("amount is not a decimal number: %r" % amount)
    whole, _, frac = text.partition(".")
    whole = whole or "0"
    if not whole.isdigit() or (frac and not frac.isdigit()):
        raise ValueError("amount is not a decimal number: %r" % amount)
    if len(frac) > 30:
        raise ValueError("Nano has 30 decimal places; %d were given" % len(frac))
    return int(whole) * RAW_PER_XNO + int(frac.ljust(30, "0") or 0)


def raw_to_xno(raw: int) -> str:
    """Integer raw -> exact decimal XNO string, no trailing-zero noise."""
    if not isinstance(raw, int):
        raise ValueError("raw must be an integer, got %s" % type(raw).__name__)
    if raw < 0:
        raise ValueError("raw must not be negative")
    whole, frac = divmod(raw, RAW_PER_XNO)
    if frac == 0:
        return str(whole)
    return "%d.%s" % (whole, str(frac).zfill(30).rstrip("0"))
