#!/usr/bin/env python3
"""Compare two plan versions and output diff report."""
import argparse, json, sys

def diff_plan(original_path: str, revised_path: str) -> dict:
    with open(original_path) as f:
        orig = json.load(f)
    with open(revised_path) as f:
        rev = json.load(f)
    
    orig_ir = orig.get("plan_ir", orig)
    rev_ir = rev.get("plan_ir", rev)
    
    orig_nodes = {n["node_id"]: n for n in orig_ir.get("nodes", [])}
    rev_nodes = {n["node_id"]: n for n in rev_ir.get("nodes", [])}
    
    added = set(rev_nodes.keys()) - set(orig_nodes.keys())
    removed = set(orig_nodes.keys()) - set(rev_nodes.keys())
    common = set(orig_nodes.keys()) & set(rev_nodes.keys())
    
    modified = []
    for nid in sorted(common):
        orig_purpose = orig_nodes[nid].get("purpose", "")
        rev_purpose = rev_nodes[nid].get("purpose", "")
        orig_skill = orig_nodes[nid].get("target_skill", "")
        rev_skill = rev_nodes[nid].get("target_skill", "")
        changes = []
        if orig_purpose != rev_purpose:
            changes.append(f"purpose changed: '{orig_purpose}' → '{rev_purpose}'")
        if orig_skill != rev_skill:
            changes.append(f"target_skill changed: '{orig_skill}' → '{rev_skill}'")
        if changes:
            modified.append({"node_id": nid, "changes": changes})
    
    return {
        "original_nodes": len(orig_nodes),
        "revised_nodes": len(rev_nodes),
        "nodes_added": sorted(added),
        "nodes_removed": sorted(removed),
        "nodes_modified": modified,
        "summary": f"+{len(added)} nodes, -{len(removed)} nodes, ~{len(modified)} modified"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True)
    parser.add_argument("--revised", required=True)
    parser.add_argument("--output", default="diff.json")
    args = parser.parse_args()
    
    result = diff_plan(args.original, args.revised)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Diff: {result['summary']}")
    if result["nodes_added"]: print(f"  Added: {result['nodes_added']}")
    if result["nodes_removed"]: print(f"  Removed: {result['nodes_removed']}")
    if result["nodes_modified"]:
        for m in result["nodes_modified"]:
            print(f"  Modified {m['node_id']}: {', '.join(m['changes'])}")

if __name__ == "__main__":
    main()
