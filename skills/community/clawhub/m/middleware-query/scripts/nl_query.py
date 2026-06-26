#!/usr/bin/env python3
"""
Unified one-command entry for middleware NL query.
Flow: NL -> planner_llm -> planner_guard -> execute_plan
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    ap = argparse.ArgumentParser(description="One-command middleware natural language query")
    ap.add_argument("--text", required=True, help="Natural language query")
    ap.add_argument("--conn-file", default=str(BASE / "connections.json"))
    ap.add_argument("--mysql-profile", default="mysql.main")
    ap.add_argument("--redis-profile", default="redis.main")
    ap.add_argument("--mongo-profile", default="mongo.main")
    ap.add_argument("--planner-model", default=None)
    ap.add_argument("--keep-plan", help="Optional path to save generated plan json")
    args = ap.parse_args()

    with tempfile.NamedTemporaryFile(prefix="mw-plan-", suffix=".json", delete=False) as tf:
        plan_path = Path(tf.name)

    planner_cmd = [
        sys.executable,
        str(BASE / "planner_llm.py"),
        "--text", args.text,
        "--mysql-profile", args.mysql_profile,
        "--redis-profile", args.redis_profile,
        "--mongo-profile", args.mongo_profile,
        "--out", str(plan_path),
    ]
    if args.planner_model:
        planner_cmd.extend(["--model", args.planner_model])

    code, out, err = run(planner_cmd)
    if code != 0:
        sys.stderr.write(err or out)
        raise SystemExit(code)

    guard_cmd = [sys.executable, str(BASE / "planner_guard.py"), "--plan", str(plan_path)]
    code, gout, gerr = run(guard_cmd)
    if code != 0:
        sys.stderr.write(gerr or gout)
        raise SystemExit(code)

    exec_cmd = [
        sys.executable,
        str(BASE / "execute_plan.py"),
        "--plan", str(plan_path),
        "--conn-file", args.conn_file,
    ]
    code, eout, eerr = run(exec_cmd)
    if code != 0:
        sys.stderr.write(eerr or eout)
        raise SystemExit(code)

    planner_obj = json.loads(out)
    plan = planner_obj.get("plan", planner_obj)
    result_obj = json.loads(eout)

    merged = {
        "ok": True,
        "request": args.text,
        "plan": plan,
        "result": result_obj,
    }

    if args.keep_plan:
        Path(args.keep_plan).write_text(json.dumps(planner_obj, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(merged, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
