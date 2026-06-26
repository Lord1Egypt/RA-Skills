#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def main():
    base = Path(__file__).resolve().parents[1]
    vpy = base / ".venv" / "bin" / "python"
    if not vpy.exists():
        raise SystemExit(f"ERROR: venv missing. Run: python3 {base}/scripts/bootstrap_venv.py")
    target = base / "scripts" / "events.py"
    cmd = [str(vpy), str(target), *sys.argv[1:]]
    print("+", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
