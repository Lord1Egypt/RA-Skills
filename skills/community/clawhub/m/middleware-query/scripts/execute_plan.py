#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

from planner_guard import validate_plan

BASE = Path(__file__).resolve().parent


def run(cmd: list[str]):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    print(proc.stdout)


def main():
    p = argparse.ArgumentParser(description="Execute validated middleware query plan")
    p.add_argument("--plan", required=True)
    p.add_argument("--conn-file", default=str(BASE / "connections.json"))
    args = p.parse_args()

    raw_plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    plan = raw_plan.get("plan") if isinstance(raw_plan, dict) and "plan" in raw_plan else raw_plan
    guard = validate_plan(plan)
    if not guard.ok:
        print(json.dumps({"ok": False, "errors": guard.errors}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    ds = plan["datasource"]
    profile = plan["profile"]

    if ds == "mysql":
        cmd = [
            sys.executable,
            str(BASE / "query_sql.py"),
            "--profile", profile,
            "--conn-file", args.conn_file,
            "--sql", plan["sql"],
            "--limit", str(plan.get("limit", 100)),
        ]
    elif ds == "redis":
        cmd = [
            sys.executable,
            str(BASE / "query_redis.py"),
            "--profile", profile,
            "--conn-file", args.conn_file,
            "--command", plan["action"],
        ]
        for k in ["key", "field", "pattern", "count", "start", "stop"]:
            if k in plan:
                cmd.extend([f"--{k}", str(plan[k])])
        if "keys" in plan and isinstance(plan["keys"], list):
            cmd.append("--keys")
            cmd.extend([str(x) for x in plan["keys"]])
    elif ds == "mongo":
        cmd = [
            sys.executable,
            str(BASE / "query_mongo.py"),
            "--profile", profile,
            "--conn-file", args.conn_file,
            "--collection", plan["collection"],
            "--limit", str(plan.get("limit", 100)),
        ]
        if plan["action"] == "find":
            cmd.extend(["--filter", json.dumps(plan.get("filter", {}), ensure_ascii=False)])
            if "projection" in plan:
                cmd.extend(["--projection", json.dumps(plan["projection"], ensure_ascii=False)])
        else:
            cmd.extend(["--pipeline", json.dumps(plan["pipeline"], ensure_ascii=False)])
    else:
        raise SystemExit(f"Unsupported datasource: {ds}")

    run(cmd)


if __name__ == "__main__":
    main()
