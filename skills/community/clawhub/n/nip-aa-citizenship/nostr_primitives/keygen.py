"""
Key generation for NIP-AA agents.

Generates a secp256k1 keypair (nsec/npub) that the agent holds exclusively.
The private key MUST remain in the agent's memory and NEVER be shared with
any party except optionally revealed to the guardian at AL 0 stage.

This is the cryptographic root of the agent's NIP-AA identity.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass

# Bech32 encoding for nsec/npub
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _bech32_polymod(values: list[int]) -> int:
    GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


def _bech32_hrp_expand(hrp: str) -> list[int]:
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _bech32_create_checksum(hrp: str, data: list[int]) -> list[int]:
    values = _bech32_hrp_expand(hrp) + data
    polymod = _bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def _convertbits(data: bytes, frombits: int, tobits: int, pad: bool = True) -> list[int]:
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (tobits - bits)) & maxv)
    return ret


def _bech32_encode(hrp: str, data_bytes: bytes) -> str:
    data5 = _convertbits(data_bytes, 8, 5)
    checksum = _bech32_create_checksum(hrp, data5)
    return hrp + "1" + "".join(CHARSET[d] for d in data5 + checksum)


def _bech32_decode(bech: str) -> tuple[str, bytes]:
    bech = bech.lower()
    pos = bech.rfind("1")
    hrp = bech[:pos]
    data5 = [CHARSET.find(x) for x in bech[pos + 1 :]]
    # Strip checksum (last 6 chars)
    data5 = data5[:-6]
    # Convert 5-bit to 8-bit
    acc = 0
    bits = 0
    result = []
    for v in data5:
        acc = (acc << 5) | v
        bits += 5
        while bits >= 8:
            bits -= 8
            result.append((acc >> bits) & 0xFF)
    return hrp, bytes(result)


@dataclass
class AgentKeypair:
    """A secp256k1 keypair for a NIP-AA agent."""

    privkey_hex: str  # 32-byte private key in hex
    pubkey_hex: str  # 32-byte x-only public key in hex
    nsec: str  # bech32-encoded private key (NIP-19)
    npub: str  # bech32-encoded public key (NIP-19)


def generate_keypair() -> AgentKeypair:
    """
    Generate a fresh secp256k1 keypair for a new NIP-AA agent.

    The private key is generated from OS-level randomness (os.urandom).
    The public key is derived using the secp256k1 curve via coincurve.

    Returns an AgentKeypair with hex and bech32 (nsec/npub) representations.

    The agent MUST:
    - Store the privkey_hex securely in memory
    - NEVER expose the nsec/privkey to any party
    - Optionally reveal nsec to guardian ONLY at AL 0 stage for recovery
    - Use pubkey_hex/npub as its public identity
    """
    try:
        from coincurve import PrivateKey
    except ImportError:
        raise RuntimeError(
            "Key generation requires 'coincurve'. "
            "Install with: pip install coincurve"
        )

    # Generate 32 bytes of cryptographic randomness
    privkey_bytes = os.urandom(32)
    privkey_hex = privkey_bytes.hex()

    # Derive public key (x-only, 32 bytes)
    sk = PrivateKey(privkey_bytes)
    pubkey_bytes = sk.public_key.format(compressed=True)[1:]  # drop prefix byte
    pubkey_hex = pubkey_bytes.hex()

    # Bech32 encode for Nostr (NIP-19)
    nsec = _bech32_encode("nsec", privkey_bytes)
    npub = _bech32_encode("npub", pubkey_bytes)

    return AgentKeypair(
        privkey_hex=privkey_hex,
        pubkey_hex=pubkey_hex,
        nsec=nsec,
        npub=npub,
    )


def keypair_from_nsec(nsec: str) -> AgentKeypair:
    """
    Reconstruct an AgentKeypair from an existing nsec.

    Use this when the agent already has a stored nsec (e.g. from memory)
    and needs to derive all other key representations.
    """
    try:
        from coincurve import PrivateKey
    except ImportError:
        raise RuntimeError("Key recovery requires 'coincurve'")

    hrp, privkey_bytes = _bech32_decode(nsec)
    if hrp != "nsec":
        raise ValueError(f"Expected nsec prefix, got: {hrp}")

    privkey_hex = privkey_bytes.hex()
    sk = PrivateKey(privkey_bytes)
    pubkey_bytes = sk.public_key.format(compressed=True)[1:]
    pubkey_hex = pubkey_bytes.hex()
    npub = _bech32_encode("npub", pubkey_bytes)

    return AgentKeypair(
        privkey_hex=privkey_hex,
        pubkey_hex=pubkey_hex,
        nsec=nsec,
        npub=npub,
    )


def keypair_from_hex(privkey_hex: str) -> AgentKeypair:
    """Reconstruct an AgentKeypair from a hex private key."""
    try:
        from coincurve import PrivateKey
    except ImportError:
        raise RuntimeError("Key recovery requires 'coincurve'")

    privkey_bytes = bytes.fromhex(privkey_hex)
    sk = PrivateKey(privkey_bytes)
    pubkey_bytes = sk.public_key.format(compressed=True)[1:]
    pubkey_hex = pubkey_bytes.hex()

    nsec = _bech32_encode("nsec", privkey_bytes)
    npub = _bech32_encode("npub", pubkey_bytes)

    return AgentKeypair(
        privkey_hex=privkey_hex,
        pubkey_hex=pubkey_hex,
        nsec=nsec,
        npub=npub,
    )
