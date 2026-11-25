#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ModelDeck download verifier (standard library only).

Checks a model file three ways: byte size, SHA256, and the GGUF header.
Run it on every artifact before importing it into a runtime.

    python verify_download.py --file model-Q4_K_M.gguf \
        --sha256 <EXPECTED_SHA256> --size <EXPECTED_BYTES>

Exit codes
    0  all requested checks passed
    2  size mismatch
    3  SHA256 mismatch
    4  not a GGUF file (or header truncated)
    5  I/O or permission error
    6  bad arguments

Notes
    * The hash is computed by streaming 8 MiB chunks, so memory stays flat on
      multi-gigabyte files.
    * A truncated download usually fails the size check first; a corrupted one
      fails the hash check. The GGUF header check catches the case where a file
      has plausible size and hash but is not a GGUF at all (wrong artifact).
    * Output is ASCII so it survives any Windows console code page.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys

CHUNK = 8 * 1024 * 1024
PROGRESS_EVERY = 512 * 1024 * 1024
GGUF_MAGIC = b"GGUF"

EXIT_OK, EXIT_SIZE, EXIT_HASH, EXIT_GGUF, EXIT_IO, EXIT_USAGE = 0, 2, 3, 4, 5, 6


def human(n: float) -> str:
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(n) < 1024.0 or unit == "TiB":
            return "%.2f %s" % (n, unit)
        n /= 1024.0
    return "%.2f TiB" % n


def read_gguf_header(path: str) -> dict:
    with open(path, "rb") as fh:
        head = fh.read(24)
    if len(head) < 4:
        return {"ok": False, "reason": "file shorter than 4 bytes"}
    if head[:4] != GGUF_MAGIC:
        return {"ok": False, "reason": "magic is %r, expected b'GGUF'" % head[:4]}
    if len(head) < 24:
        return {"ok": False, "reason": "header truncated before counts"}
    version = struct.unpack("<I", head[4:8])[0]
    tensor_count = struct.unpack("<Q", head[8:16])[0]
    meta_count = struct.unpack("<Q", head[16:24])[0]
    if not (1 <= version <= 9):
        return {"ok": False, "reason": "implausible GGUF version %d" % version}
    if tensor_count == 0:
        return {"ok": False, "reason": "GGUF declares zero tensors"}
    return {
        "ok": True,
        "version": version,
        "tensor_count": tensor_count,
        "metadata_count": meta_count,
    }


def sha256_of(path: str, show_progress: bool) -> str:
    digest = hashlib.sha256()
    done = 0
    with open(path, "rb") as fh:
        while True:
            block = fh.read(CHUNK)
            if not block:
                break
            digest.update(block)
            done += len(block)
            if show_progress and done % PROGRESS_EVERY < CHUNK:
                sys.stderr.write("  hashed %s\r" % human(done))
                sys.stderr.flush()
    if show_progress:
        sys.stderr.write(" " * 40 + "\r")
        sys.stderr.flush()
    return digest.hexdigest()


def normalize_hex(value: str) -> str:
    return value.strip().lower().replace(":", "").replace(" ", "")


def main(argv) -> int:
    p = argparse.ArgumentParser(description="Verify a downloaded model file (size, SHA256, GGUF header).")
    p.add_argument("--file", required=True, help="path to the downloaded artifact")
    p.add_argument("--sha256", default="", help="expected SHA256 (hex; colons and spaces ignored)")
    p.add_argument("--size", type=int, default=-1, help="expected size in bytes")
    p.add_argument("--allow-non-gguf", action="store_true",
                   help="skip the GGUF header check (for auxiliary files)")
    p.add_argument("--no-hash", action="store_true", help="skip hashing (size and header only)")
    p.add_argument("--json", action="store_true", help="emit a JSON report on stdout")
    args = p.parse_args(argv)

    report = {"file": args.file, "checks": {}, "ok": False, "exit_code": EXIT_OK}
    path = os.path.abspath(args.file)

    if not os.path.isfile(path):
        report["checks"]["exists"] = False
        report["exit_code"] = EXIT_IO
        emit(report, args.json, "FAIL: no such file: %s" % args.file)
        return EXIT_IO

    actual_size = os.path.getsize(path)
    report["size_bytes"] = actual_size
    report["size_human"] = human(actual_size)

    if args.size >= 0:
        size_ok = actual_size == args.size
        report["checks"]["size"] = size_ok
        if not size_ok:
            report["exit_code"] = EXIT_SIZE
            emit(report, args.json,
                 "FAIL: size mismatch: got %d bytes, expected %d (delta %+d). "
                 "Re-run the download with resume enabled before retrying."
                 % (actual_size, args.size, actual_size - args.size))
            return EXIT_SIZE
    else:
        report["checks"]["size"] = None

    header = {"ok": True, "skipped": True}
    if not args.allow_non_gguf:
        header = read_gguf_header(path)
        report["checks"]["gguf"] = header["ok"]
        report["gguf"] = header
        if not header["ok"]:
            report["exit_code"] = EXIT_GGUF
            emit(report, args.json,
                 "FAIL: GGUF header check failed (%s). The file is truncated, "
                 "partially written, or not a GGUF artifact." % header.get("reason"))
            return EXIT_GGUF

    if args.sha256 and not args.no_hash:
        show = sys.stderr.isatty()
        try:
            actual_hash = sha256_of(path, show)
        except OSError as exc:
            report["exit_code"] = EXIT_IO
            emit(report, args.json, "FAIL: cannot read file: %s" % exc)
            return EXIT_IO
        expected = normalize_hex(args.sha256)
        report["sha256_actual"] = actual_hash
        report["sha256_expected"] = expected
        hash_ok = actual_hash == expected
        report["checks"]["sha256"] = hash_ok
        if not hash_ok:
            report["exit_code"] = EXIT_HASH
            emit(report, args.json,
                 "FAIL: SHA256 mismatch.\n  actual  : %s\n  expected: %s\n"
                 "Delete the file and download it again; do not import a file "
                 "whose hash does not match." % (actual_hash, expected))
            return EXIT_HASH
    elif not args.no_hash:
        show = sys.stderr.isatty()
        try:
            actual_hash = sha256_of(path, show)
        except OSError as exc:
            report["exit_code"] = EXIT_IO
            emit(report, args.json, "FAIL: cannot read file: %s" % exc)
            return EXIT_IO
        report["sha256_actual"] = actual_hash
        report["checks"]["sha256"] = None
        sys.stderr.write("info: no expected SHA256 supplied; computed value recorded.\n")

    report["ok"] = True
    lines = ["PASS: %s" % os.path.basename(path),
             "  size   : %s (%d bytes)" % (report["size_human"], actual_size)]
    if header.get("ok") and not header.get("skipped"):
        lines.append("  gguf   : v%d, %d tensors, %d metadata entries"
                     % (header["version"], header["tensor_count"], header["metadata_count"]))
    if report.get("sha256_actual"):
        lines.append("  sha256 : %s" % report["sha256_actual"])
    emit(report, args.json, "\n".join(lines))
    return EXIT_OK


def emit(report: dict, as_json: bool, text: str) -> None:
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(text)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        sys.stderr.write("interrupted\n")
        sys.exit(130)
