#!/usr/bin/env python3
import json
from dataclasses import dataclass

ALLOWED_DATASOURCES = {"mysql", "redis", "mongo"}
ALLOWED_ACTIONS = {
    "mysql": {"sql_query"},
    "redis": {"get", "mget", "hget", "hgetall", "smembers", "zrange", "scan", "ttl", "type"},
    "mongo": {"find", "aggregate"},
}
REQUIRED_COMMON = {"datasource", "profile", "action"}


@dataclass
class GuardResult:
    ok: bool
    errors: list[str]


def normalize_plan(plan: dict) -> dict:
    if isinstance(plan, dict) and "plan" in plan and isinstance(plan["plan"], dict):
        return plan["plan"]
    return plan


def validate_plan(plan: dict) -> GuardResult:
    plan = normalize_plan(plan)
    errors: list[str] = []

    missing = [k for k in REQUIRED_COMMON if k not in plan]
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
        return GuardResult(False, errors)

    ds = plan.get("datasource")
    action = plan.get("action")

    if ds not in ALLOWED_DATASOURCES:
        errors.append(f"Unsupported datasource: {ds}")
        return GuardResult(False, errors)

    if action not in ALLOWED_ACTIONS[ds]:
        errors.append(f"Unsupported action '{action}' for datasource '{ds}'")

    if ds == "mysql":
        if "sql" not in plan:
            errors.append("mysql plan requires 'sql'")
    elif ds == "redis":
        # command params are validated later by query_redis.py
        pass
    elif ds == "mongo":
        if "collection" not in plan:
            errors.append("mongo plan requires 'collection'")
        if action == "find" and "filter" not in plan:
            errors.append("mongo find requires 'filter'")
        if action == "aggregate" and "pipeline" not in plan:
            errors.append("mongo aggregate requires 'pipeline'")

    return GuardResult(len(errors) == 0, errors)


def load_plan(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate middleware query plan JSON")
    parser.add_argument("--plan", required=True, help="Path to plan JSON")
    args = parser.parse_args()

    loaded = load_plan(args.plan)
    plan = normalize_plan(loaded)
    res = validate_plan(plan)
    out = {
        "ok": res.ok,
        "errors": res.errors,
        "plan": plan,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not res.ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
