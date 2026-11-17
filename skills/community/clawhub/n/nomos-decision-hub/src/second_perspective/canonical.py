"""Canonical JSON serialization for deterministic hash computation.

Every data structure that participates in hash-chain audit events must be
serialized through this module. The output is deterministic: keys are sorted,
and the same Python object always produces the same canonical representation.
"""

import json
from typing import Any


def canonical_json(obj: Any) -> bytes:
    """Return a deterministic UTF-8 encoded JSON representation of *obj*.

    - Keys are sorted alphabetically.
    - No extra whitespace.
    - Floats and Decimals are serialised as strings so that hash computation
      is not affected by floating-point binary representation differences.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
        allow_nan=False,
    ).encode("utf-8")