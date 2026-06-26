# -*- coding: utf-8 -*-
"""
query_knowledge_base.py - Multi-partition query script for knowledge base
Usage:
    # Single partition
    python query_knowledge_base.py "What are InnoDB features" --kb-path "MyNotes" --partition mysql

    # Multiple partitions (comma-separated)
    python query_knowledge_base.py "Difference between MySQL and Oracle" --kb-path "MyNotes" --partition mysql,oracle

    # All partitions
    python query_knowledge_base.py "What is in this knowledge base" --kb-path "MyNotes"

    # Auto-detect knowledge base
    python query_knowledge_base.py "What is xxx" --partition mysql

    # Custom topk
    python query_knowledge_base.py "xxx" --topk 10
"""

import sys as _sys
_sys.stdout.reconfigure(encoding='utf-8')
_sys.stderr.reconfigure(encoding='utf-8')

import argparse
import json
import os
import sys
import urllib.parse

import requests

# Import from upload_to_vector for shared config loading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload_to_vector import load_config


def find_knowledge_base(start_path=None):
    """
    Auto-detect knowledge base.
    Logic:
    1. start_path has raw_docs/ + config.json -> return directly
    2. start_path subdir has raw_docs/ + config.json -> return first match
    3. Search parent directory (max 2 levels)
    """
    if start_path is None:
        start_path = os.getcwd()

    candidates = []

    if os.path.isdir(start_path):
        raw_docs = os.path.join(start_path, "raw_docs")
        config_json = os.path.join(start_path, "config.json")
        if os.path.isdir(raw_docs) and os.path.isfile(config_json):
            return start_path
        for item in os.listdir(start_path):
            sub_path = os.path.join(start_path, item)
            if os.path.isdir(sub_path):
                sub_raw = os.path.join(sub_path, "raw_docs")
                sub_cfg = os.path.join(sub_path, "config.json")
                if os.path.isdir(sub_raw) and os.path.isfile(sub_cfg):
                    candidates.append(sub_path)

    if candidates:
        return candidates[0]

    parent = os.path.dirname(start_path)
    if parent != start_path and os.path.isdir(parent):
        for item in os.listdir(parent):
            sub_path = os.path.join(parent, item)
            if os.path.isdir(sub_path):
                sub_raw = os.path.join(sub_path, "raw_docs")
                sub_cfg = os.path.join(sub_path, "config.json")
                if os.path.isdir(sub_raw) and os.path.isfile(sub_cfg):
                    return sub_path

    return None


def generate_embedding(config, text):
    """Call Bailian API to generate embedding for a single text"""
    api_key = config["bailian"]["api_key"]
    model = config["bailian"].get("model", "text-embedding-v3")
    dimension = config["dashvector"]["dimension"]

    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": text,
        "dimensions": dimension,
        "encoding_format": "float"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["data"][0]["embedding"]
        else:
            print(f"  [!] Vector generation failed: HTTP {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"  [!] Vector generation error: {e}")
        return None


def query_partition(config, vector, partition, topk=5, include_fields=None):
    """
    Query within a single partition.
    Returns (success, results_list)
    """
    dv = config["dashvector"]
    endpoint = dv["endpoint"]
    collection = dv["collection_name"]
    api_key = dv["api_key"]

    if include_fields is None:
        include_fields = ["content", "source", "partition", "chunk_index"]

    url = f"{endpoint}/v1/collections/{collection}/query"
    headers = {
        "dashvector-auth-token": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "vector": vector,
        "topk": topk,
        "partition": partition,
        "include_fields": True,
        "fields": include_fields
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        resp_data = response.json()

        if resp_data.get("code") == 0:
            outputs = resp_data.get("output", [])
            return True, outputs
        else:
            return False, {
                "code": resp_data.get("code"),
                "message": resp_data.get("message", "Unknown error")
            }
    except Exception as e:
        return False, {"exception": str(e)}


def list_partitions(config):
    """List all partition names in DashVector"""
    dv = config["dashvector"]
    endpoint = dv["endpoint"]
    collection = dv["collection_name"]
    api_key = dv["api_key"]

    url = f"{endpoint}/v1/collections/{collection}/partitions"
    headers = {"dashvector-auth-token": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        resp_data = response.json()
        if response.status_code == 200 and resp_data.get("code") == 0:
            output = resp_data.get("output", [])
            if output and isinstance(output[0], str):
                return [p for p in output]
            return [p.get("name", "unknown") for p in output]
        return []
    except:
        return []


def query_multi_partition(config, question, partitions=None, topk=5):
    """
    Multi-partition query entry point.
    partitions: None (all partitions) or ["mysql", "oracle"] list
    Returns merged and sorted results
    """
    print(f"  Generating question embedding...")
    vector = generate_embedding(config, question)
    if vector is None:
        return None

    if partitions is None or partitions == ["all"] or partitions == []:
        print(f"  Getting all partitions...")
        all_parts = list_partitions(config)
        if not all_parts:
            print("  [!] No partitions found, trying 'default'...")
            all_parts = ["default"]
        partitions = all_parts
        print(f"  All partitions: {partitions}")
    else:
        if isinstance(partitions, str):
            partitions = [p.strip() for p in partitions.split(",")]
        print(f"  Querying partitions: {partitions}")

    all_results = []
    for pname in partitions:
        print(f"  Querying partition [{pname}]...")
        ok, result = query_partition(config, vector, pname, topk=topk)
        if ok:
            for item in result:
                item["_partition"] = pname
            all_results.extend(result)
            print(f"    -> [{pname}] returned {len(result)} results")
        else:
            print(f"    -> [{pname}] failed: {result}")

    all_results.sort(key=lambda x: x.get("score", 0), reverse=True)

    return all_results


def format_results(results, max_display=10):
    """Format query results as readable text"""
    if not results:
        return "No relevant results found"

    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append(f"Query Results ({len(results)} total)")
    lines.append(f"{'=' * 60}\n")

    for i, r in enumerate(results[:max_display], 1):
        score = r.get("score", 0)
        partition = r.get("_partition", "unknown")
        fields = r.get("fields", {})
        content = fields.get("content", "")[:300]
        source = fields.get("source", "Unknown source")

        lines.append(f"[{i}] Partition: {partition} | Similarity: {score:.4f}")
        lines.append(f"  Source: {source}")
        lines.append(f"  Content: {content}...")
        lines.append("")

    if len(results) > max_display:
        lines.append(f"({len(results) - max_display} more results not shown)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Knowledge base multi-partition query")
    parser.add_argument("question", help="Query question (wrap in quotes)")
    parser.add_argument("--kb-path", dest="kb_path", default=None,
                        help="Knowledge base path, auto-detect if not provided")
    parser.add_argument("--partition", dest="partition", default=None,
                        help="Partition name(s), comma-separated. Omit for all partitions.")
    parser.add_argument("--topk", dest="topk", type=int, default=5,
                        help="Max results per partition, default 5")
    args = parser.parse_args()

    question = args.question.strip()
    if not question:
        print("[x] Question cannot be empty")
        sys.exit(1)

    kb_path = args.kb_path
    if kb_path is None:
        print("[*] Auto-detecting knowledge base...")
        kb_path = find_knowledge_base()
        if kb_path is None:
            print("[x] Knowledge base not found. Ensure current directory or subdirectory contains raw_docs/ and config.json")
            print("   or use --kb-path to specify the path")
            sys.exit(1)
        print(f"   Found: {kb_path}")

    config_path = os.path.join(kb_path, "config.json")
    if not os.path.isfile(config_path):
        print(f"[x] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    kb_name = config.get("knowledge_base", {}).get("name", os.path.basename(kb_path))
    collection = config["dashvector"]["collection_name"]

    print(f"\n{'=' * 60}")
    print(f"Knowledge Base Query")
    print(f"  KB Name: {kb_name}")
    print(f"  Collection: {collection}")
    print(f"  Question: {question}")
    print(f"{'=' * 60}\n")

    partitions = None
    if args.partition:
        partitions = [p.strip() for p in args.partition.split(",")]
        print(f"Specified partitions: {partitions}\n")

    results = query_multi_partition(config, question, partitions=partitions, topk=args.topk)

    if results is None:
        print("[x] Query failed (vector generation failed)")
        sys.exit(1)

    print(format_results(results))

    structured = {
        "question": question,
        "kb_name": kb_name,
        "collection": collection,
        "kb_path": kb_path,
        "total_results": len(results),
        "results": [
            {
                "score": r.get("score"),
                "partition": r.get("_partition"),
                "source": r.get("fields", {}).get("source"),
                "chunk_index": r.get("fields", {}).get("chunk_index"),
                "content": r.get("fields", {}).get("content", "")
            }
            for r in results
        ]
    }

    temp_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "query_result.json")
    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)
    print(f"\n[*] Structured results written to: {temp_json_path}")


if __name__ == "__main__":
    main()
