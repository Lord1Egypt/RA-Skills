#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

from _common import coalesce, mask_sensitive, to_json, env_int
from profile_loader import load_profile

FORBIDDEN_STAGES = {"$out", "$merge"}


def main():
    p = argparse.ArgumentParser(description="Read-only Mongo query executor")
    p.add_argument("--profile", required=True)
    p.add_argument("--conn-file")
    p.add_argument("--host")
    p.add_argument("--port", type=int)
    p.add_argument("--username")
    p.add_argument("--password")
    p.add_argument("--database")
    p.add_argument("--auth-source")
    p.add_argument("--collection", required=True)
    p.add_argument("--filter", default="{}")
    p.add_argument("--projection", default="{}")
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--pipeline")
    args = p.parse_args()

    conn_file = args.conn_file or str(Path(__file__).resolve().parent / "connections.json")
    conn, meta = load_profile(conn_file, args.profile)
    host = coalesce(args.host, os.getenv("MONGO_HOST"), conn.get("host"))
    port = coalesce(args.port, env_int("MONGO_PORT"), conn.get("port"), 27017)
    username = coalesce(args.username, os.getenv("MONGO_USER"), conn.get("username"))
    password = coalesce(args.password, os.getenv("MONGO_PASSWORD"), conn.get("password"))
    database = coalesce(args.database, os.getenv("MONGO_DATABASE"), conn.get("database"))
    auth_source = coalesce(args.auth_source, os.getenv("MONGO_AUTH_SOURCE"), conn.get("authSource"), "admin")

    if not all([host, port, username, password, database]):
        raise ValueError("Missing required Mongo config: host/port/username/password/database")

    from pymongo import MongoClient

    uri = f"mongodb://{username}:{password}@{host}:{int(port)}/?authSource={auth_source}"
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    coll = client[database][args.collection]

    if args.pipeline:
        pipeline = json.loads(args.pipeline)
        for stage in pipeline:
            if any(k in FORBIDDEN_STAGES for k in stage.keys()):
                raise ValueError("Pipeline contains forbidden write stages ($out/$merge)")
        docs = list(coll.aggregate(pipeline, allowDiskUse=False))[: min(args.limit, 1000)]
        op = "aggregate"
    else:
        filt = json.loads(args.filter)
        proj = json.loads(args.projection)
        docs = list(coll.find(filt, proj).limit(min(args.limit, 1000)))
        op = "find"

    client.close()

    to_json({
        "datasource": "mongo",
        "profile": args.profile,
        "profile_meta": meta,
        "operation": op,
        "collection": args.collection,
        "count": len(docs),
        "preview": mask_sensitive(docs),
    })


if __name__ == "__main__":
    main()
