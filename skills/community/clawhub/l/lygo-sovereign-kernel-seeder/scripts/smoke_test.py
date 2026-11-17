#!/usr/bin/env python3
"""Smoke: seed ephemeral egg → verify → cleanup. Consent via env for CI."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="lygo_seed_smoke_"))
    try:
        note = tmp / "module.txt"
        note.write_text("LYGO sovereign seed smoke\n", encoding="utf-8")
        env = os.environ.copy()
        env["LYGO_KERNEL_SEED_CONSENT"] = "yes"
        env["LYGO_SEED_ROOT"] = str(tmp)
        r1 = subprocess.run(
            [
                sys.executable,
                str(HERE / "seed_kernel.py"),
                "--i-consent",
                "--egg-id",
                "smoke-seed",
                "--kind",
                "seed",
                "--title",
                "Smoke Seed",
                "--summary",
                "smoke",
                "--file",
                str(note),
                "--root",
                str(tmp),
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        if r1.returncode != 0:
            print(r1.stdout)
            print(r1.stderr, file=sys.stderr)
            print("SMOKE_FAIL seed", r1.returncode)
            return 1
        r2 = subprocess.run(
            [sys.executable, str(HERE / "verify_seed.py"), "--root", str(tmp), "--json"],
            capture_output=True,
            text=True,
        )
        if r2.returncode != 0:
            print(r2.stdout)
            print(r2.stderr, file=sys.stderr)
            print("SMOKE_FAIL verify")
            return 1
        rep = json.loads(r2.stdout)
        if rep.get("verdict") != "ALIGNED":
            print(rep)
            print("SMOKE_FAIL verdict")
            return 1
        print(json.dumps({"status": "SMOKE_OK", "registry_merkle_root": rep.get("computed_merkle_root")}, indent=2))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
