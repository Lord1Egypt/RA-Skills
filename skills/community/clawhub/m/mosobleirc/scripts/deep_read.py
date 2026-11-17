#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from mosobleirc_core import (
    DEFAULT_DATA_ROOT,
    MosOblEIRCError,
    StateStore,
)

def _review(base: dict, reasons: list[str], **extra) -> dict:
    return {**base, **extra, "ok": False, "status": "REVIEW",
            "needs_user_confirmation": True, "reasons": reasons}

def check_candidate(meter_id: int, black_digits: str, red_digits: str,
                    ambiguous: bool, data_root: Path) -> dict:
    store = StateStore(data_root)
    profile = store.get_reference(meter_id)
    base = {
        "provider_contacted": False,
        "meter_id": meter_id,
        "apartment": profile.get("apartment"),
        "address": profile.get("address"),
        "physical_serial": profile.get("physical_serial"),
    }
    int_digits = profile.get("integer_digits")
    dec_digits = profile.get("decimal_digits")
    if not int_digits or dec_digits is None:
        return _review(base, ["meter_layout_not_calibrated"])

    black = str(black_digits or "").strip()
    red = str(red_digits or "").strip()
    if (not black.isdigit() or (red and not red.isdigit()) or
            len(black) != int(int_digits) or len(red) != int(dec_digits)):
        return _review(base, ["digit_layout_mismatch"],
                       black_digits=black, red_digits=red)

    integer = int(black)
    decimal = int(red) if red else 0
    reading = integer + (decimal / (10 ** int(dec_digits)) if dec_digits else 0.0)
    candidate = {
        "canonical_digits": black + red,
        "black_digits": black,
        "red_digits": red,
        "integer_part": integer,
        "decimal_part": decimal,
        "reading_value": reading,
    }
    reasons: list[str] = []
    if ambiguous:
        reasons.append("vision_ambiguous")
    previous = profile.get("last_provider_value")
    if previous is not None:
        delta = integer - int(float(previous))
        if delta < 0:
            reasons.append("reading_decreased")
        if delta > 50:
            reasons.append("unusually_large_jump")
    if reasons:
        return _review(base, reasons, **candidate)
    return {**base, **candidate, "ok": True, "status": "GREEN",
            "needs_user_confirmation": False, "reasons": []}

def main() -> int:
    ap = argparse.ArgumentParser(prog="mosobleirc-deep-read")
    ap.add_argument("--meter-id", type=int, required=True)
    ap.add_argument("--black-digits", required=True)
    ap.add_argument("--red-digits", required=True)
    ap.add_argument("--ambiguous", action="store_true")
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    args = ap.parse_args()
    try:
        result = check_candidate(args.meter_id, args.black_digits, args.red_digits,
                                 args.ambiguous, args.data_root)
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return 0
    except MosOblEIRCError as exc:
        print(json.dumps({"ok": False, "status": "RED",
                          "provider_contacted": False,
                          "error": type(exc).__name__,
                          "message": str(exc)[:200]},
                         ensure_ascii=False, separators=(",", ":")))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
