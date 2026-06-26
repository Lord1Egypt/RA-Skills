#!/usr/bin/env python3
"""
RunOptimizationPipeline.py
One-command pipeline for module maintenance:
1) Naming audit
2) Content/link audit
3) Module order validation
4) Reference map rebuild
5) Module graph rebuild
6) Conflict scan
7) Encoding normalization
8) Summary output
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    target = Path(args.target).resolve()

    naming_script = skill_root / "Scripts" / "NamingAudit.py"
    content_script = skill_root / "Scripts" / "ContentLinkAudit.py"
    order_script = skill_root / "Scripts" / "ValidateModuleOrder.py"
    map_script = skill_root / "Scripts" / "BuildReferenceMap.py"
    graph_script = skill_root / "Scripts" / "BuildModuleGraph.py"
    conflict_script = skill_root / "Scripts" / "DetectRuleConflicts.py"
    normalize_script = skill_root / "Scripts" / "NormalizeEncoding.py"

    n_rc, n_out, n_err = run([sys.executable, str(naming_script), str(target), "--json"], skill_root)
    c_rc, c_out, c_err = run([sys.executable, str(content_script), str(target), "--json"], skill_root)
    o_rc, o_out, o_err = run([sys.executable, str(order_script)], skill_root)
    m_rc, m_out, m_err = run([sys.executable, str(map_script)], skill_root)
    g_rc, g_out, g_err = run([sys.executable, str(graph_script)], skill_root)
    f_rc, f_out, f_err = run([sys.executable, str(conflict_script)], skill_root)
    z_rc, z_out, z_err = run([sys.executable, str(normalize_script)], skill_root)

    result = {
        "target": str(target),
        "naming": {"rc": n_rc, "data": json.loads(n_out) if n_out else None, "stderr": n_err},
        "content_link": {"rc": c_rc, "data": json.loads(c_out) if c_out else None, "stderr": c_err},
        "module_order": {"rc": o_rc, "stdout": o_out, "stderr": o_err},
        "reference_map": {"rc": m_rc, "stdout": m_out, "stderr": m_err},
        "module_graph": {"rc": g_rc, "stdout": g_out, "stderr": g_err},
        "conflict_scan": {"rc": f_rc, "stdout": f_out, "stderr": f_err},
        "normalize_encoding": {"rc": z_rc, "stdout": z_out, "stderr": z_err},
    }

    ok = n_rc == 0 and c_rc == 0 and o_rc == 0 and m_rc == 0 and g_rc == 0 and f_rc == 0 and z_rc == 0
    result["ok"] = ok

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        naming_count = result["naming"]["data"]["count"] if result["naming"]["data"] else -1
        dup_count = result["content_link"]["data"]["duplicate_count"] if result["content_link"]["data"] else -1
        miss_count = result["content_link"]["data"]["missing_link_count"] if result["content_link"]["data"] else -1
        print(f"Target: {target}")
        print(f"Naming Issues: {naming_count}")
        print(f"Duplicate Paragraph Groups: {dup_count}")
        print(f"Missing Links: {miss_count}")
        print(f"ModuleOrder: {'OK' if o_rc == 0 else 'FAILED'}")
        print(f"ReferenceMap: {'OK' if m_rc == 0 else 'FAILED'}")
        print(f"ModuleGraph: {'OK' if g_rc == 0 else 'FAILED'}")
        print(f"ConflictScan: {'OK' if f_rc == 0 else 'FAILED'}")
        print(f"NormalizeEncoding: {'OK' if z_rc == 0 else 'FAILED'}")
        print(f"Pipeline: {'OK' if ok else 'FAILED'}")

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
