#!/usr/bin/env python3
"""bigquery.py - run BigQuery SQL with a service-account key. No gcloud, no SDK.

Usage:
    python3 bigquery.py --key ~/.config/gcp/billing-reader.json --project my-proj --sql "SELECT 1"
    python3 bigquery.py --key ... --project ... --file references/queries-monthly-net.sql

Prints JSON: {totalRows, schema, rows, bytesProcessed}. Exits 1 with the API error body on failure.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bigquery_token import get_token  # noqa: E402


def run_query(key, project, sql, max_rows=1000, timeout=180):
    token = get_token(key)
    body = json.dumps({
        "query": sql,
        "useLegacySql": False,
        "timeoutMs": 60000,
        "maxResults": max_rows,
    }).encode()
    url = "https://bigquery.googleapis.com/bigquery/v2/projects/%s/queries" % project
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def flatten(res):
    fields = [f["name"] for f in res.get("schema", {}).get("fields", [])]
    rows = []
    for row in res.get("rows", []):
        rows.append({k: v.get("v") for k, v in zip(fields, row["f"])})
    return fields, rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--project", required=True, help="project that runs the job (a project with Job User)")
    ap.add_argument("--sql")
    ap.add_argument("--file")
    ap.add_argument("--max-rows", type=int, default=1000)
    a = ap.parse_args()
    sql = a.sql or (open(a.file).read() if a.file else "SELECT 1 AS ok")
    try:
        res = run_query(a.key, a.project, sql, a.max_rows)
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.code, "body": e.read().decode()[:1500]}, indent=1))
        sys.exit(1)
    if "errors" in res:
        print(json.dumps({"errors": res["errors"]}, indent=1))
        sys.exit(1)
    fields, rows = flatten(res)
    print(json.dumps({
        "totalRows": res.get("totalRows"),
        "schema": fields,
        "rows": rows,
        "bytesProcessed": res.get("totalBytesProcessed"),
    }, indent=1))
