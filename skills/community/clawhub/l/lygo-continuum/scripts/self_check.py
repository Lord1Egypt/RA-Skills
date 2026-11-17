#!/usr/bin/env python3
"""Self-check for lygo-continuum — no network, path confinement, write gates."""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import continuum as c  # noqa: E402


def main() -> int:
    src = (HERE / "continuum.py").read_text(encoding="utf-8")
    no_subprocess_import = not re.search(r"(?m)^\s*import\s+subprocess\b", src)
    no_urllib = not re.search(r"(?m)^\s*import\s+urllib\b", src)
    no_requests = "import requests" not in src

    demo = c.cmd_demo()

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "f.txt").write_text("hello continuum\n", encoding="utf-8")
        cap = c.seal_capsule(
            claims=[
                {"kind": "file_contains", "path": "f.txt", "needle": "continuum"},
                {"kind": "file_sha256", "path": "f.txt"},
            ],
            task_summary="unit",
            agent="self_check",
            base=root,
        )
        v1 = c.verify_capsule(cap, base=root)
        broken = dict(cap)
        broken["root_hash"] = "0" * 64
        v2 = c.verify_capsule(broken, base=root)
        kinds_ok = "file_sha256" in c.CLAIM_KINDS and "json_path_eq" in c.CLAIM_KINDS

        # Path confinement
        esc = c.evaluate_claim(
            {"id": "x", "kind": "file_exists", "path": "../outside.txt"},
            base=root,
        )
        abs_esc = c.evaluate_claim(
            {"id": "y", "kind": "file_exists", "path": str(Path.home() / "secret.txt")},
            base=root,
        )
        glob_esc = c.evaluate_claim(
            {"id": "z", "kind": "glob_count_gte", "pattern": "../*", "n": 1},
            base=root,
        )
        path_ok = (
            esc.get("ok") is False
            and "rejected" in (esc.get("detail") or "").lower()
            and abs_esc.get("ok") is False
            and glob_esc.get("ok") is False
        )

        # Write gate
        outside = root.parent / "continuum_should_not_write.json"
        ok_w, why = c.authorize_write(outside, base=root, consent=False, allow_any=False)
        ok_in, _ = c.authorize_write(root / "capsule.json", base=root, consent=False, allow_any=False)
        write_ok = (not ok_w) and ok_in and why == "out_must_be_under_base_or_state"

    ok = (
        demo.get("ok") is True
        and v1.get("ok") is True
        and v2.get("integrity_ok") is False
        and no_subprocess_import
        and no_urllib
        and no_requests
        and kinds_ok
        and path_ok
        and write_ok
        and c.VERSION == "1.0.1"
        and c.SCHEMA == "lygo.continuum.v1"
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "signature": c.SIG,
                "version": c.VERSION,
                "demo_ok": demo.get("ok"),
                "verify_ok": v1.get("ok"),
                "integrity_detects_tamper": v2.get("integrity_ok") is False,
                "path_confinement": path_ok,
                "write_gate": write_ok,
                "no_subprocess_import": no_subprocess_import,
                "no_network_imports": no_urllib and no_requests,
                "claim_kinds": len(c.CLAIM_KINDS),
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
