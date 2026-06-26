#!/usr/bin/env python3
"""Calculate the OpenMath proof hash using the on-chain protobuf layout."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path


def encode_varint(number: int) -> bytearray:
    """Encode an integer as a protobuf varint."""
    encoded = bytearray()
    while number >= 0x80:
        encoded.append((number & 0x7F) | 0x80)
        number >>= 7
    encoded.append(number & 0x7F)
    return encoded


def encode_string(field_number: int, value: str) -> bytearray:
    """Encode a protobuf string field (wire type 2)."""
    tag = (field_number << 3) | 2
    data = value.encode("utf-8")
    encoded = bytearray()
    encoded.extend(encode_varint(tag))
    encoded.extend(encode_varint(len(data)))
    encoded.extend(data)
    return encoded


def encode_uint64(field_number: int, value: int) -> bytearray:
    """Encode a protobuf uint64 field (wire type 0)."""
    tag = (field_number << 3) | 0
    encoded = bytearray()
    encoded.extend(encode_varint(tag))
    encoded.extend(encode_varint(value))
    return encoded


def read_detail_input(detail_input: str) -> str:
    """Read theorem detail from a file path when possible, else treat input as literal text."""
    path = Path(detail_input)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return detail_input


def calculate_proof_hash(theorem_id: int, prover: str, detail: str) -> str:
    """
    Simulate the on-chain Keeper.GetProofHash logic.

    Layout:
    - field 1: theorem_id (uint64)
    - field 2: detail (string)
    - field 3: prover (string)
    """
    encoded = bytearray()
    encoded.extend(encode_uint64(1, theorem_id))
    encoded.extend(encode_string(2, detail))
    encoded.extend(encode_string(3, prover))

    return hashlib.sha256(encoded).hexdigest()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the proof hash for an OpenMath theorem submission."
    )
    parser.add_argument("theorem_id", type=int, help="Theorem ID")
    parser.add_argument("prover_address", help="Shentu prover address")
    parser.add_argument(
        "detail_content_or_file",
        help="Proof content or a path to a proof file",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        detail = read_detail_input(args.detail_content_or_file)
        print(calculate_proof_hash(args.theorem_id, args.prover_address, detail))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
