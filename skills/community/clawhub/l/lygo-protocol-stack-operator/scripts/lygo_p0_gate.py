#!/usr/bin/env python3
"""
Standalone P0.4 byte gate (canonical f32 semantics). No network. Max 8192 bytes/file.
Usage: python lygo_p0_gate.py <file> [file...]
Exit 0 if all AMPLIFY or SOFTEN; exit 2 if any QUARANTINE.
"""
from __future__ import annotations

import hashlib
import math
import struct
import sys
from pathlib import Path

MAX_BYTES = 8192
PHI_MIN = 0.618
PHI_MAX = 1.618
ENTROPY_LOW = 0.25
ENTROPY_HIGH = 0.90
COMP_MIN_LEN = 64
COMP_POOR = 0.90


def f32(x: float) -> float:
    return struct.unpack("<f", struct.pack("<f", float(x)))[0]


def round4(x: float) -> float:
    v = f32(x) * 10000.0
    add = 0.5 if v >= 0.0 else -0.5
    return int(v + add) / 10000.0


def entropy_norm(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    length = f32(float(len(data)))
    ent = f32(0.0)
    for c in freq:
        if c:
            p = f32(f32(float(c)) / length)
            ent = f32(ent - f32(p * f32(math.log2(p))))
    denom = f32(math.log2(length)) if len(data) > 1 else f32(1.0)
    return f32(min(f32(ent / denom), f32(1.0)))


def compression_ratio(data: bytes) -> float:
    if len(data) < COMP_MIN_LEN:
        return f32(0.0)
    repeats = 0
    limit = len(data) - 7
    for i in range(0, limit, 4):
        if data[i : i + 4] == data[i + 4 : i + 8]:
            repeats += 1
    ratio = f32(f32(float(repeats)) / f32(float(len(data))))
    if ratio > f32(1.0):
        ratio = f32(1.0)
    return f32(f32(1.0) - ratio)


def validate_bytes(data: bytes) -> dict:
    if len(data) > MAX_BYTES:
        return {
            "verdict": "QUARANTINE",
            "phi_risk": round4(PHI_MAX),
            "risk": 1.0,
            "hash16": hashlib.sha256(data).hexdigest()[:16],
        }
    ent = entropy_norm(data)
    comp = compression_ratio(data)
    risk = f32(0.0)
    if ent > f32(ENTROPY_HIGH):
        risk = f32(risk + f32(0.30))
    elif ent < f32(ENTROPY_LOW):
        risk = f32(risk + f32(0.15))
    if comp > f32(COMP_POOR):
        risk = f32(risk + f32(0.25))
    risk = f32(min(risk, f32(1.0)))
    size_damp = f32(f32(float(len(data))) / f32(128.0)) if len(data) < 128 else f32(1.0)
    phi_risk = f32(risk * f32(PHI_MAX) * size_damp)
    if phi_risk < f32(PHI_MIN):
        verdict = "AMPLIFY"
    elif phi_risk <= f32(PHI_MAX):
        verdict = "SOFTEN"
    else:
        verdict = "QUARANTINE"
    if ent < f32(ENTROPY_LOW) and verdict == "AMPLIFY":
        verdict = "SOFTEN"
    return {
        "verdict": verdict,
        "phi_risk": round4(phi_risk),
        "risk": round4(risk),
        "entropy": round4(ent),
        "compression": round4(comp),
        "hash16": hashlib.sha256(data).hexdigest()[:16],
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: lygo_p0_gate.py <file> [file...]", file=sys.stderr)
        return 1
    quarantine = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"SKIP not file: {path}")
            continue
        data = path.read_bytes()
        r = validate_bytes(data)
        print(
            f"{path.name}|{r['verdict']}|phi={r['phi_risk']:.4f}|"
            f"risk={r['risk']:.4f}|hash16={r['hash16']}"
        )
        if r["verdict"] == "QUARANTINE":
            quarantine += 1
    return 2 if quarantine else 0


if __name__ == "__main__":
    raise SystemExit(main())