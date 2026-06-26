#!/usr/bin/env python3
"""Unit tests for bin/log-resolution.py — sanitizer, ledger I/O, concurrency.

Dependency-free: run with `python3 tests/test_log_resolution.py` (exit 0 = pass).
"""
import importlib.util
import json
import math
import os
import sys
import tempfile
import threading

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location(
    "log_resolution", os.path.join(REPO, "bin", "log-resolution.py")
)
lr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lr)

_failures = []


def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        _failures.append(name)


# --- sanitizer: secrets/PII must be redacted ---
# Assemble secret-shaped fixtures from parts so no literal token is ever committed
# verbatim (GitHub secret-scanning push protection scans raw file bytes). The
# joined strings still match the SECRET_PATTERNS regexes at runtime.
def j(*parts):
    return "".join(parts)

SECRETS = [
    j("the key sk", "_live_", "4eC39HqLyjWDarjtT1zdp7dc"),
    j("rotate sk", "-proj-", "abc123def456ghi789jkl012mno345"),
    j("gh", "p_", "16C7e42F292c6912E7710c838347Ae178B4a"),
    j("wh", "sec_", "abcdef0123456789abcdef0123456789"),
    j("header Bearer ", "eyJhbGciOiJIUzI1NiJ9", ".payloadpart.sigpart"),
    j("Authorization Basic ", "dXNlcjpwYXNzd29yZA=="),
    j("AKIA", "IOSFODNN7", "EXAMPLE in config"),
    j("xapp", "-1-", "A1234567890-abcdefghij"),
    j("conn postgres://admin:", "s3cr3tpw", "@db.internal/app"),
    "email her at jane.doe@acme.com",
    j("password=", "hunter2supersecret"),
    "ssn 123-45-6789",
    "call +1 415 555 0123 now",
    j("dead", "beef", "deadbeefdeadbeefdeadbeefdeadbeef12"),
]
for s in SECRETS:
    clean, red = lr.sanitize(s)
    check(f"redacts secret: {s[:28]!r}", red and clean == lr.REDACTED)

# --- sanitizer: benign noun phrases pass through verbatim ---
for benign in ["the auth middleware", "src/server/routes/login.ts", "the failing test"]:
    clean, red = lr.sanitize(benign)
    check(f"keeps benign: {benign!r}", (not red) and clean == benign)

# --- sanitizer: control chars stripped ---
clean, red = lr.sanitize("the\x07 bell\x00 char")
check("strips control chars", red and "\x07" not in clean and "\x00" not in clean)

# --- sanitizer: over-long (non-secret) value is truncated, not stored whole ---
long_val = "the file " * 30  # 270 chars, spaces break base64/hex patterns
clean, red = lr.sanitize(long_val)
check("truncates long value", red and len(clean) < 200 and "truncated" in clean)

# --- sanitizer: empty/None safe ---
check("empty value safe", lr.sanitize("") == ("", False))

# --- confidence validation: clamp + reject nan/inf ---
check("confidence clamps high", lr.clean_confidence(5.0) == 1.0)
check("confidence clamps low", lr.clean_confidence(-1.0) == 0.0)
check("confidence default on None", lr.clean_confidence(None) == 0.5)
check("confidence rejects nan", lr.clean_confidence(float("nan")) == 0.5)
check("confidence rejects inf", lr.clean_confidence(float("inf")) == 0.5)

# --- prompt_hash validation: hex digest kept, anything else dropped ---
check("keeps hex digest", lr.clean_hash("a" * 64) == "a" * 64)
check("drops raw text hash", lr.clean_hash("rotate the api key please") == "")
check("drops short non-hex", lr.clean_hash("xyz") == "")

# --- ledger round-trip: nested dir creation + count ---
with tempfile.TemporaryDirectory() as d:
    led_path = os.path.join(d, "sub", "ledger.json")
    lr.update_ledger(led_path, lambda l: l["resolutions"].append({"pronoun": "it"}))
    reloaded = lr.load(led_path)
    check("update_ledger creates nested dir + persists", reloaded["resolution_count"] == 1)

# --- corrupt ledger: backed up, not silently destroyed ---
with tempfile.TemporaryDirectory() as d:
    bad = os.path.join(d, "bad.json")
    with open(bad, "w") as f:
        f.write("{ not json")
    data = lr.load(bad)
    check("corrupt ledger falls back to EMPTY", data["resolution_count"] == 0)
    check("corrupt ledger backed up to .corrupt", os.path.exists(bad + ".corrupt"))

# --- save refuses NaN (defense in depth) ---
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "l.json")
    try:
        lr.save(p, {"resolutions": [{"confidence": float("nan")}]})
        check("save rejects NaN", False)
    except ValueError:
        check("save rejects NaN", not os.path.exists(p))  # nothing written

# --- concurrency: N parallel writes through the real locked path keep all entries ---
with tempfile.TemporaryDirectory() as d:
    led_path = os.path.join(d, "ledger.json")
    lr.save(led_path, lr._empty())
    N = 40

    def worker(i):
        lr.update_ledger(led_path,
                         lambda l, i=i: l["resolutions"].append({"pronoun": "it", "ref": i}))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    final = lr.load(led_path)
    check(f"concurrent writes keep all {N} entries (no lost updates)",
          final["resolution_count"] == N)

print()
if _failures:
    print(f"{len(_failures)} FAILED: {_failures}")
    sys.exit(1)
print("all tests passed")
sys.exit(0)
