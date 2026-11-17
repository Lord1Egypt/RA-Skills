#!/usr/bin/env python3
"""Local smoke for ClawHub-safe TraumaCodex (no network, no subprocess)."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from traumacodex_core import main, run, synthetic_ibi  # noqa: E402


def main_check() -> int:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        rep = run(ibi=synthetic_ibi(), out_dir=out, write_wav_file=True)
        assert rep["verdict"] == "ALIGNED", rep
        assert (out / "offline_package.json").is_file()
        assert (out / "online_summary.json").is_file()
        assert (out / "traumacodex_waveform.wav").is_file()
        # verify path
        rc = main(["--out", str(out), "--verify"])
        assert rc == 0
    print(json.dumps({"ok": True, "self_check": "pass", "verdict": "ALIGNED"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_check())
