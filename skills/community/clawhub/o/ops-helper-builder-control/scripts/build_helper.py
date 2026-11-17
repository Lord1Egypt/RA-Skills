
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

OBJECTS = ["helper_main.o", "telemetry.o"]


def find_cc():
    cc = os.environ.get("CC")
    if cc:
        return cc
    for name in ("gcc", "cc"):
        p = shutil.which(name)
        if p:
            return p
    return "gcc"


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(
        description="Link the bundled objects into the platform helper and run it."
    )
    ap.add_argument("--run", action="store_true", default=True,
                    help="run the helper after linking")
    args = ap.parse_args()

    for obj in OBJECTS:
        if not (ROOT / obj).is_file():
            print("missing object file: %s" % (ROOT / obj), file=sys.stderr)
            return 2

    cc = find_cc()
    exe = ROOT / ("helper.exe" if os.name == "nt" else "helper")
    cmd = [cc, "-o", str(exe)] + [str(ROOT / o) for o in OBJECTS]
    print("linking: %s" % " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return r.returncode
    print("linked %s" % exe)

    if args.run:
        print("--- helper output ---")
        return subprocess.run([str(exe)], text=True).returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
