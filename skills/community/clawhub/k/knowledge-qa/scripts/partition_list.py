# -*- coding: utf-8 -*-
"""
partition_list.py - Check DashVector partition status
Usage:
    python partition_list.py
    python partition_list.py --kb-path "MyNotes"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
import argparse
from upload_to_vector import load_config


def list_partitions_with_counts(config):
    """
    Get partition list and document counts.
    DashVector has no direct count API, so we probe each partition
    and cross-reference with local indexed_files.json.
    """
    dv = config["dashvector"]
    endpoint = dv["endpoint"]
    collection = dv["collection_name"]
    api_key = dv["api_key"]
    dim = dv["dimension"]

    parts_url = f"{endpoint}/v1/collections/{collection}/partitions"
    r = requests.get(parts_url, headers={"dashvector-auth-token": api_key}, timeout=30)
    rd = r.json()

    if r.status_code != 200 or rd.get("code") != 0:
        print(f"Failed to get partition list: {rd}")
        return []

    partitions = rd.get("output", [])
    if partitions and isinstance(partitions[0], str):
        partitions = [{"name": p} for p in partitions]

    indexed_path = config["knowledge_base"]["indexed_files_path"]
    local_counts = {}
    if os.path.exists(indexed_path):
        with open(indexed_path, "r", encoding="utf-8") as f_read:
            idx = json.load(f_read)
        from collections import Counter
        local_counts = Counter(file_entry.get("partition", "default") for file_entry in idx.get("files", []))

    results = []
    for p in partitions:
        pname = p.get("name", "unknown")

        query_url = f"{endpoint}/v1/collections/{collection}/query"
        q = requests.post(query_url, headers={
            "dashvector-auth-token": api_key,
            "Content-Type": "application/json"
        }, json={
            "vector": [0.0] * dim,
            "topk": 100,
            "partition": pname,
            "include_fields": False
        }, timeout=30)
        qd = q.json()

        has_data = qd.get("code") == 0 and len(qd.get("output", [])) > 0
        local_count = local_counts.get(pname, 0)

        results.append({
            "partition": pname,
            "has_data": has_data,
            "local_indexed": local_count,
            "note": "Has data" if has_data else "Empty (no data in this partition)"
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Check DashVector partition status")
    parser.add_argument("--kb-path", dest="kb_path", default=None,
                        help="Knowledge base path, auto-detect if not provided")
    args = parser.parse_args()

    print("=" * 50)
    print("DashVector Partition Status")
    print("=" * 50)

    config = load_config(args.kb_path)
    print(f"\nCollection: {config['dashvector']['collection_name']}\n")

    results = list_partitions_with_counts(config)

    if not results:
        print("No partitions found")
        return

    print(f"{'Partition':<20} {'Local Index':<12} {'Cloud Status':<20} Note")
    print("-" * 70)
    for r in results:
        print(f"{r['partition']:<20} {r['local_indexed']:<12} {str(r['has_data']):<20} {r['note']}")

    print(f"\nTotal: {len(results)} partitions")
    print("\nNote: Local Index = count from indexed_files.json")
    print("      Cloud Status = probing via vector query")


if __name__ == "__main__":
    main()
