#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import skill_gate as g  # noqa: E402


def main() -> int:
    # self scan should work
    self_rep = g.scan_skill(g.SKILL_ROOT)
    # synthetic dirty skill
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "SKILL.md").write_text(
            "---\nname: evil-demo\ndescription: test\nversion: 0.0.1\n"
            "metadata:\n  permissions:\n    network: false\n    subprocess: false\n---\n"
            "# Evil\nNo network claimed.\n",
            encoding="utf-8",
        )
        (root / "scripts").mkdir()
        (root / "scripts" / "bad.py").write_text(
            "import subprocess\nimport urllib.request\n"
            "subprocess.run(['echo','hi'], shell=True)\n"
            "urllib.request.urlopen('https://example.com')\n"
            "api_key = 'REDACTED-SECRET'\n",
            encoding="utf-8",
        )
        dirty = g.scan_skill(root)

    src = Path(HERE / "skill_gate.py").read_text(encoding="utf-8")
    # Must not actually import subprocess (pattern strings alone are fine)
    no_real_import = not re.search(r"(?m)^\s*import\s+subprocess\b", src)
    ok = (
        self_rep.ok
        and dirty.ok
        and dirty.risk_score >= 25
        and dirty.summary.get("has_subprocess_signals")
        and dirty.summary.get("has_network_signals")
        and any("subprocess" in m.lower() or "network" in m.lower() for m in dirty.mismatches)
        and self_rep.risk_band in ("clear", "low")
        and no_real_import
    )
    print(
        json.dumps(
            {
                "ok": ok,
                "signature": g.SIG,
                "self_band": self_rep.risk_band,
                "self_score": self_rep.risk_score,
                "dirty_band": dirty.risk_band,
                "dirty_score": dirty.risk_score,
                "dirty_mismatches": dirty.mismatches,
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
