#!/usr/bin/env python3
"""
World lattice verify: Layer A+B (local) then Layer C (public HTTP).

Default behavior (hardened v1.1.1):
  - Verify only (local tools + public GET)
  - Does NOT write report files unless --write-report
  - Does NOT refresh manifest / star-map files unless --refresh-local (+ --i-trust-stack)
  - No os.system / shell
  - Skill-local scripts via in-process runpy allowlist
  - Stack A+B via subprocess capture (no shell) under trusted stack root

Protects user: local mismatch = hard fail; public degrade = soft warn unless --strict-public.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIG = "Delta9Phi963-WORLD-LATTICE-VERIFY-v1.1.1"

sys.path.insert(0, str(HERE))
from _safe_invoke import run_python_script  # noqa: E402


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    for p in HERE.parents:
        if (p / "tools" / "verify_all_kernel_layers.py").is_file() or (
            p / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json"
        ).is_file():
            return p
    return Path.cwd()


def _parse_json_output(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {"verdict": "ERROR", "raw": ""}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Multiple JSON objects may be printed (nested tools). Prefer last valid object.
    decoder = json.JSONDecoder()
    idx = 0
    last: dict | None = None
    while idx < len(text):
        brace = text.find("{", idx)
        if brace < 0:
            break
        try:
            obj, end = decoder.raw_decode(text, brace)
            if isinstance(obj, dict):
                last = obj
            idx = end
        except json.JSONDecodeError:
            idx = brace + 1
    if last is not None:
        return last
    return {"verdict": "ERROR", "raw": text[:800]}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "World lattice verify A+B+C. Default: no report write, no docs mutation, no shell. "
            "Opt-in: --write-report; --refresh-local requires --i-trust-stack (executes builders)."
        )
    )
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict-public", action="store_true")
    ap.add_argument("--stack-root", default="")
    ap.add_argument(
        "--i-trust-stack",
        action="store_true",
        help="Required with --refresh-local: affirm stack root is code you trust",
    )
    ap.add_argument(
        "--refresh-local",
        action="store_true",
        help=(
            "OPT-IN EXECUTE+WRITE: rebuild public_verify_manifest + star_chart proposals under docs/. "
            "Runs skill-local Python via runpy. Requires --i-trust-stack."
        ),
    )
    ap.add_argument(
        "--write-report",
        action="store_true",
        help="OPT-IN WRITE: persist tests/world_lattice_last_run.json under stack root",
    )
    ap.add_argument(
        "--no-write-report",
        action="store_true",
        help="Deprecated alias: default already does not write reports",
    )
    ap.add_argument(
        "--skip-public",
        action="store_true",
        help="Skip Layer C HTTP checks (local A+B only)",
    )
    args = ap.parse_args()
    stack = Path(args.stack_root).resolve() if args.stack_root else stack_root()
    write_report = bool(args.write_report) and not args.no_write_report
    if args.refresh_local and not args.i_trust_stack:
        print(
            json.dumps(
                {
                    "verdict": "BLOCKED",
                    "errors": ["refresh_local_requires_i_trust_stack"],
                    "hint": "pass --i-trust-stack only for a stack checkout you control",
                }
            )
        )
        return 2

    report = {
        "signature": SIG,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stack": str(stack),
        "layers": {},
        "verdict": "WORLD_ALIGNED",
        "mode": {
            "refresh_local": bool(args.refresh_local),
            "write_report": write_report,
            "skip_public": bool(args.skip_public),
            "shell": False,
            "os_system": False,
            "invoke": "runpy_allowlist+subprocess_capture_for_AB",
        },
    }

    # A+B local
    # NOTE: verify_all_kernel_layers spawns nested children; use captured
    # subprocess (no shell) so nested stdout cannot bleed into this process.
    import subprocess

    unified = stack / "tools" / "verify_all_kernel_layers.py"
    ab_done = False
    if unified.is_file():
        try:
            unified.relative_to(stack.resolve())
            p = subprocess.run(
                [sys.executable, str(unified), "--json"],
                cwd=str(stack),
                capture_output=True,
                text=True,
                shell=False,
                timeout=180,
            )
            ab = _parse_json_output(p.stdout or p.stderr or "")
            ab["exit_code"] = p.returncode
            ab["invoke"] = "subprocess_capture_no_shell"
            report["layers"]["AB_local"] = ab
            ab_done = True
            if ab.get("verdict") == "QUARANTINE" or p.returncode == 3:
                report["verdict"] = "LOCAL_QUARANTINE"
        except ValueError:
            report["layers"]["AB_local"] = {"status": "REFUSED", "reason": "tool_outside_stack"}

    if not ab_done:
        sev = (
            stack
            / "docs"
            / "skills"
            / "lygo-sovereign-kernel-seeder"
            / "scripts"
            / "verify_seed.py"
        )
        if sev.is_file():
            root = stack / "data" / "sovereign_seeds"
            code, out = run_python_script(
                sev, ["--root", str(root), "--json"], cwd=stack, stack=stack
            )
            b = _parse_json_output(out)
            b["exit_code"] = code
            report["layers"]["B_sovereign_only"] = b
            if code == 3:
                report["verdict"] = "LOCAL_QUARANTINE"
        else:
            sev2 = HERE.parent.parent / "lygo-sovereign-kernel-seeder" / "scripts" / "verify_seed.py"
            if sev2.is_file():
                code, out = run_python_script(
                    sev2,
                    ["--root", str(stack / "data" / "sovereign_seeds"), "--json"],
                    cwd=stack,
                    stack=stack,
                )
                b = _parse_json_output(out)
                report["layers"]["B_sovereign_only"] = b
                if code == 3:
                    report["verdict"] = "LOCAL_QUARANTINE"
            else:
                report["layers"]["AB_local"] = {"status": "SKIP", "reason": "no unified tool"}

    # C public (skill-local)
    c = {"verdict": "SKIP", "reason": "skip_public"}
    if not args.skip_public:
        pub = HERE / "verify_public_anchors.py"
        code, out = run_python_script(
            pub,
            ["--json", "--stack-root", str(stack)]
            + (["--no-write-report"] if not write_report else []),
            cwd=stack,
            stack=stack,
        )
        c = _parse_json_output(out)
        c["exit_code"] = code
        report["layers"]["C_public"] = c
        if c.get("verdict") == "PUBLIC_DEGRADED":
            if args.strict_public:
                report["verdict"] = "PUBLIC_DEGRADED"
            elif report["verdict"] == "WORLD_ALIGNED":
                report["verdict"] = "WORLD_ALIGNED_PUBLIC_WARN"
    else:
        report["layers"]["C_public"] = c

    # Opt-in local refresh (mutating) — never default; requires --i-trust-stack (checked above)
    refresh_results = []
    if args.refresh_local and args.i_trust_stack:
        for script in ("build_public_verify_manifest.py", "map_eggs_to_star_chart.py"):
            sp = HERE / script
            if sp.is_file():
                code, out = run_python_script(
                    sp, ["--stack-root", str(stack)], cwd=stack, stack=stack
                )
                refresh_results.append(
                    {"script": script, "exit_code": code, "ok": code == 0, "out_tail": out[-200:]}
                )
        report["refresh_local"] = refresh_results
        report["mode"]["i_trust_stack"] = True

    if write_report:
        out_path = stack / "tests" / "world_lattice_last_run.json"
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            report["report_path"] = str(out_path)
        except OSError as e:
            report["report_write_error"] = str(e)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"verdict={report['verdict']}")
        abv = report["layers"].get("AB_local", report["layers"].get("B_sovereign_only", {}))
        print(f"  AB={abv.get('verdict') or abv.get('status')}")
        print(f"  C={c.get('verdict')}")
        if args.refresh_local:
            print(f"  refresh_local={refresh_results}")

    if report["verdict"] == "LOCAL_QUARANTINE":
        return 3
    if report["verdict"] == "PUBLIC_DEGRADED" and args.strict_public:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
