#!/usr/bin/env python3
"""
Exact rational-arithmetic certificates.

A numerical claim in a theory paper must be backed by a script that runs in
EXACT arithmetic (fractions.Fraction, integers, sympy.Rational). Floats are not
evidence: they can be wrong by an amount invisible at 1e-16.

This tool:
  1. statically scans the certificate script for float contamination
     (float literals, bare `/` division, math/numpy float paths);
  2. executes it and requires an explicit CERTIFIED / REFUTED verdict line;
  3. writes a machine-readable certificate with a hash of the script.

Usage:
    python rational_certificate.py --script 07-audit-trail/check_bound.py
    python rational_certificate.py --demo
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

CONTAMINATION_RULES = {
    "float_literal": lambda t: any(isinstance(n, ast.Constant) and isinstance(n.value, float)
                                   for n in ast.walk(t)),
    "float_call": lambda t: any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                                and n.func.id == "float" for n in ast.walk(t)),
    "bare_division": lambda t: any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)
                                   for n in ast.walk(t)),
    "float_module": lambda t: any(
        (isinstance(n, ast.Import) and any(a.name.split(".")[0] in ("math", "numpy", "scipy")
                                           for a in n.names))
        or (isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0]
            in ("math", "numpy", "scipy"))
        for n in ast.walk(t)),
}

DEMO = '''\
"""Demo certificate: sum_{i=1}^{n} 1/(i(i+1)) == n/(n+1)  (exact)."""
from fractions import Fraction

def check():
    for n in range(1, 21):
        lhs = sum(Fraction(1, i * (i + 1)) for i in range(1, n + 1))
        rhs = Fraction(n, n + 1)
        if lhs != rhs:
            print(f"REFUTED at n={n}: {lhs} != {rhs}")
            return False
    # a claim that is FALSE, checked exactly:
    if sum(Fraction(1, i * (i + 1)) for i in range(1, 6)) == Fraction(1, 1):
        print("REFUTED: unexpected equality")
        return False
    print("CERTIFIED: identity holds exactly for n=1..20")
    return True

check()
'''


def scan(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        return [f"script does not parse: {e}"]
    return [name for name, fn in CONTAMINATION_RULES.items() if fn(tree)]


def run_script(path: Path) -> tuple[int, str, str]:
    r = subprocess.run([sys.executable, str(path)], capture_output=True,
                       text=True, timeout=300)
    return r.returncode, r.stdout, r.stderr


def parse_verdict(stdout: str) -> str:
    for line in stdout.splitlines():
        s = line.strip().upper()
        if s.startswith("CERTIFIED"):
            return "CERTIFIED"
        if s.startswith("REFUTED"):
            return "REFUTED"
    return "NO_VERDICT"


def main() -> int:
    ap = argparse.ArgumentParser(description="Exact rational-arithmetic certificate runner")
    ap.add_argument("--script", help="path to a certificate script")
    # -o matches every other command that takes an output path
    ap.add_argument("--out", "-o", default="07-audit-trail")
    ap.add_argument("--demo", action="store_true", help="run a built-in exact example")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 unless the verdict is CERTIFIED with no float contamination")
    args = ap.parse_args()

    if args.demo:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "demo_certificate.py"
            p.write_text(DEMO, encoding="utf-8")
            rc, out, err = run_script(p)
            print(out.strip() or err.strip())
            print(f"\nfloat contamination scan: {scan(p) or 'none'}")
            return 0 if parse_verdict(out) == "CERTIFIED" else 1

    if not args.script:
        print("error: --script or --demo required", file=sys.stderr)
        return 2

    script = Path(args.script).expanduser().resolve()
    if not script.is_file():
        print(f"error: script not found: {script}", file=sys.stderr)
        return 2

    contamination = scan(script)
    rc, out, err = run_script(script)
    verdict = parse_verdict(out)
    digest = hashlib.sha256(script.read_bytes()).hexdigest()

    cert = {
        "script": str(script),
        "sha256": digest,
        "executed_at": datetime.now().isoformat(timespec="seconds"),
        "exit_code": rc,
        "verdict": verdict,
        "float_contamination": contamination,
        "stdout_tail": out[-2000:],
        "stderr_tail": err[-1000:],
    }

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cert_path = out_dir / f"certificate-{script.stem}.json"
    cert_path.write_text(json.dumps(cert, indent=2), encoding="utf-8")

    print(f"verdict           : {verdict}")
    print(f"exit code         : {rc}")
    print(f"float contamination: {contamination or 'none'}")
    if contamination:
        print("  WARNING: floats detected. This is not machine-precision evidence.")
        print("  Use fractions.Fraction / integers / sympy.Rational and integer division.")
    print(f"certificate       : {cert_path}")

    if args.strict:
        return 0 if (verdict == "CERTIFIED" and not contamination and rc == 0) else 1
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
