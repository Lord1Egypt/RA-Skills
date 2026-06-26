#!/usr/bin/env python3
"""
Natural-language router (rule-based MVP v2).
Convert Chinese/English NL query into guarded plan JSON.
"""
import argparse
import json
import re
from typing import List, Optional


def route(text: str, profile_mysql: str, profile_redis: str, profile_mongo: str) -> dict:
    t = text.strip().lower()

    # Redis intents
    if any(k in t for k in ["redis", "key", "缓存", "scan", "ttl", "hget", "hgetall"]):
        if "ttl" in t:
            key = extract_after_keywords(text, ["ttl", "key", "键"]) or ""
            return {"datasource": "redis", "profile": profile_redis, "action": "ttl", "key": key}
        if "hgetall" in t or "hash" in t:
            key = extract_after_keywords(text, ["key", "键"]) or ""
            return {"datasource": "redis", "profile": profile_redis, "action": "hgetall", "key": key}
        if "scan" in t or "前缀" in t or "pattern" in t:
            pattern = extract_pattern(text) or "*"
            return {"datasource": "redis", "profile": profile_redis, "action": "scan", "pattern": pattern, "count": 100}
        key = extract_after_keywords(text, ["key", "键"]) or ""
        return {"datasource": "redis", "profile": profile_redis, "action": "get", "key": key}

    # Mongo intents
    if any(k in t for k in ["mongo", "mongodb", "文档", "collection", "聚合"]):
        coll = extract_collection(text) or "items"
        if "聚合" in t or "aggregate" in t:
            return {
                "datasource": "mongo",
                "profile": profile_mongo,
                "action": "aggregate",
                "collection": coll,
                "pipeline": [{"$limit": 20}],
                "limit": 20,
            }
        return {
            "datasource": "mongo",
            "profile": profile_mongo,
            "action": "find",
            "collection": coll,
            "filter": {},
            "limit": 20,
        }

    # Default to MySQL
    sql = "SELECT 1 AS ok LIMIT 1"
    # very light parse for topN
    m = re.search(r"top\s*(\d+)", t)
    limit = int(m.group(1)) if m else 20
    return {
        "datasource": "mysql",
        "profile": profile_mysql,
        "action": "sql_query",
        "sql": f"SELECT * FROM users ORDER BY id DESC LIMIT {min(limit, 100)}",
    }


def extract_after_keywords(text: str, kws: List[str]) -> Optional[str]:
    for kw in kws:
        i = text.lower().find(kw.lower())
        if i >= 0:
            s = text[i + len(kw):].strip(" :：")
            if s:
                return s.split()[0]
    return None


def extract_pattern(text: str) -> Optional[str]:
    m = re.search(r"(?:pattern|前缀)\s*[:： ]\s*([^\s]+)", text, re.IGNORECASE)
    if m:
        v = m.group(1)
        return re.sub(r"^(?:pattern|前缀)[:：]", "", v, flags=re.IGNORECASE)
    return None


def extract_collection(text: str) -> Optional[str]:
    m = re.search(r"(?:collection|集合)\s*[:： ]\s*([a-zA-Z0-9_\-]+)", text, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def main():
    p = argparse.ArgumentParser(description="Route NL query to middleware query plan")
    p.add_argument("--text", required=True)
    p.add_argument("--mysql-profile", default="mysql.main")
    p.add_argument("--redis-profile", default="redis.main")
    p.add_argument("--mongo-profile", default="mongo.main")
    p.add_argument("--out", help="Output plan path (optional)")
    args = p.parse_args()

    plan = route(args.text, args.mysql_profile, args.redis_profile, args.mongo_profile)
    raw = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(raw)
    print(raw)


if __name__ == "__main__":
    main()
