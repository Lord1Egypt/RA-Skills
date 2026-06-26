#!/usr/bin/env python3
"""
LLM planner (v3): NL -> JSON plan with schema validation + retry repair.
Requires OPENAI_API_KEY. Falls back to router_nl when unavailable.
"""
import argparse
import json
import os
from typing import Any, Dict, Optional

from plan_schema import validate_with_schema
from router_nl import route

SYSTEM_PROMPT = """You are a strict middleware query planner.
Output ONLY valid JSON object (no markdown).
Rules:
1) datasource in [mysql, redis, mongo]
2) mysql action must be sql_query and read-only SQL (SELECT/WITH/EXPLAIN SELECT)
3) redis action in [get,mget,hget,hgetall,smembers,zrange,scan,ttl,type]
4) mongo action in [find,aggregate], never write operations.
5) include profile field.
6) keep limit <= 1000.
"""


def call_openai(prompt: str, model: str) -> Optional[Dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        text = getattr(resp, "output_text", "") or ""
        return json.loads(text)
    except Exception:
        return None


def plan_with_retry(text: str, mysql_profile: str, redis_profile: str, mongo_profile: str, model: str, max_retries: int = 2):
    base_prompt = (
        f"User request: {text}\n"
        f"Default profiles: mysql={mysql_profile}, redis={redis_profile}, mongo={mongo_profile}\n"
        "Return a single JSON plan."
    )

    last_errors = []
    for i in range(max_retries + 1):
        prompt = base_prompt
        if i > 0 and last_errors:
            prompt += "\nFix these validation errors: " + "; ".join(last_errors)

        plan = call_openai(prompt, model)
        if not plan:
            break

        ok, errs = validate_with_schema(plan)
        if ok:
            return plan, []
        last_errors = errs

    # fallback rule planner
    fallback = route(text, mysql_profile, redis_profile, mongo_profile)
    ok, errs = validate_with_schema(fallback)
    return fallback, errs


def main():
    p = argparse.ArgumentParser(description="LLM-based NL middleware planner with schema validation")
    p.add_argument("--text", required=True)
    p.add_argument("--mysql-profile", default="mysql.main")
    p.add_argument("--redis-profile", default="redis.main")
    p.add_argument("--mongo-profile", default="mongo.main")
    p.add_argument("--model", default=os.getenv("MW_PLANNER_MODEL", "gpt-4o-mini"))
    p.add_argument("--out")
    args = p.parse_args()

    plan, errs = plan_with_retry(
        text=args.text,
        mysql_profile=args.mysql_profile,
        redis_profile=args.redis_profile,
        mongo_profile=args.mongo_profile,
        model=args.model,
    )

    output = {
        "ok": len(errs) == 0,
        "plan": plan,
        "validation_errors": errs,
    }
    raw = json.dumps(output, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(raw)
    print(raw)


if __name__ == "__main__":
    main()
