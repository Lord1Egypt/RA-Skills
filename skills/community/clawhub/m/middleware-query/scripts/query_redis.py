#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

from _common import coalesce, mask_sensitive, to_json, env_int
from profile_loader import load_profile

ALLOWED = {"get", "mget", "hget", "hgetall", "smembers", "zrange", "scan", "ttl", "type"}


def main():
    p = argparse.ArgumentParser(description="Read-only Redis query executor")
    p.add_argument("--profile", required=True)
    p.add_argument("--conn-file")
    p.add_argument("--host")
    p.add_argument("--port", type=int)
    p.add_argument("--username")
    p.add_argument("--password")
    p.add_argument("--db", type=int)
    p.add_argument("--command", required=True, choices=sorted(ALLOWED))
    p.add_argument("--key")
    p.add_argument("--field")
    p.add_argument("--keys", nargs="*")
    p.add_argument("--pattern", default="*")
    p.add_argument("--count", type=int, default=100)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--stop", type=int, default=50)
    args = p.parse_args()

    conn_file = args.conn_file or str(Path(__file__).resolve().parent / "connections.json")
    conn, meta = load_profile(conn_file, args.profile)
    host = coalesce(args.host, os.getenv("REDIS_HOST"), conn.get("host"))
    port = coalesce(args.port, env_int("REDIS_PORT"), conn.get("port"), 6379)
    username = coalesce(args.username, os.getenv("REDIS_USER"), conn.get("username"), "default")
    password = coalesce(args.password, os.getenv("REDIS_PASSWORD"), conn.get("password"))
    db = coalesce(args.db, env_int("REDIS_DB"), conn.get("db"), 0)

    if not all([host, port, username, password]) and password is not None:
        raise ValueError("Missing required Redis config: host/port/username/password")

    import redis

    r = redis.Redis(host=host, port=int(port), username=username, password=password, db=int(db), socket_timeout=5, decode_responses=True)
    cmd = args.command

    if cmd in {"get", "hgetall", "smembers", "ttl", "type"} and not args.key:
        raise ValueError("--key is required for this command")
    if cmd == "hget" and (not args.key or not args.field):
        raise ValueError("--key and --field are required for hget")

    if cmd == "get":
        out = r.get(args.key)
    elif cmd == "mget":
        out = r.mget(args.keys or [])
    elif cmd == "hget":
        out = r.hget(args.key, args.field)
    elif cmd == "hgetall":
        out = r.hgetall(args.key)
    elif cmd == "smembers":
        out = list(r.smembers(args.key))
    elif cmd == "zrange":
        out = r.zrange(args.key, args.start, args.stop, withscores=True)
    elif cmd == "scan":
        cursor, keys = r.scan(cursor=0, match=args.pattern, count=min(args.count, 1000))
        out = {"cursor": cursor, "keys": keys}
    elif cmd == "ttl":
        out = r.ttl(args.key)
    elif cmd == "type":
        out = r.type(args.key)
    else:
        raise ValueError("Unsupported command")

    to_json({
        "datasource": "redis",
        "profile": args.profile,
        "profile_meta": meta,
        "operation": cmd,
        "result": mask_sensitive(out),
    })


if __name__ == "__main__":
    main()
