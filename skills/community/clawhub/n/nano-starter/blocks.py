"""Nano state-block construction, hashing and signing. Offline.

A state block's hash is blake2b-256 over six fixed-width fields, and the
signature is ed25519-blake2b over that hash. Both happen here, in the
caller's process; the node is only ever handed an already-signed block.
That is what "non-custodial" means operationally - the key never needs
to leave, so it never does.

Balances are integer raw throughout (1 XNO = 10**30 raw). There is no
float in this file and there must never be one: 10**30 does not fit in a
double, so a float balance silently loses the low-order digits, which is
where the money is.
"""

from hashlib import blake2b

import ed25519_blake2b as _ed
import nanoaddr as _addr

STATE_PREAMBLE = (6).to_bytes(32, "big")
ZERO32 = bytes(32)
MAX_BALANCE_RAW = 2 ** 128 - 1


def block_hash(account_pk: bytes, previous: bytes, representative_pk: bytes,
               balance_raw: int, link: bytes) -> bytes:
    """The 32-byte hash a Nano node will compute for this state block."""
    for name, value in (("account", account_pk), ("previous", previous),
                        ("representative", representative_pk), ("link", link)):
        if len(value) != 32:
            raise ValueError("%s must be 32 bytes, got %d" % (name, len(value)))
    if not isinstance(balance_raw, int):
        raise ValueError("balance must be an integer number of raw, got %s"
                         % type(balance_raw).__name__)
    if balance_raw < 0 or balance_raw > MAX_BALANCE_RAW:
        raise ValueError("balance out of range for a 128-bit raw field: %d" % balance_raw)
    digest = blake2b(digest_size=32)
    digest.update(STATE_PREAMBLE)
    digest.update(account_pk)
    digest.update(previous)
    digest.update(representative_pk)
    digest.update(balance_raw.to_bytes(16, "big"))
    digest.update(link)
    return digest.digest()


def work_root(previous: bytes, account_pk: bytes) -> str:
    """What proof-of-work is computed over.

    The previous block hash, except for the very first block of an
    account, which has no previous and uses the public key instead.
    """
    root = account_pk if previous == ZERO32 else previous
    return root.hex().upper()


def build_signed(private_key: bytes, account_pk: bytes, previous: bytes,
                 representative_pk: bytes, balance_raw: int, link: bytes,
                 subtype: str) -> dict:
    """A complete state block bar its work, ready for `NanoNode.process`.

    `_subtype` is consumed by the node RPC call and is not part of the
    block or its hash.
    """
    if subtype not in ("receive", "send", "open", "change"):
        raise ValueError("unknown state block subtype %r" % subtype)
    digest = block_hash(account_pk, previous, representative_pk, balance_raw, link)
    signature = _ed.sign(digest, private_key, account_pk)
    return {
        "type": "state",
        "account": _addr.encode(account_pk),
        "previous": previous.hex().upper(),
        "representative": _addr.encode(representative_pk),
        "balance": str(balance_raw),
        "link": link.hex().upper(),
        "signature": signature.hex().upper(),
        "_hash": digest.hex().upper(),
        "_subtype": subtype,
        "_work_root": work_root(previous, account_pk),
    }
