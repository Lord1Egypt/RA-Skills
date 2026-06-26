#!/usr/bin/env python3
import argparse
import json
import os


def load_inventory(path: str):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def chunk(items, size):
    for idx in range(0, len(items), size):
        yield items[idx: idx + size]


def main():
    parser = argparse.ArgumentParser(description="Generate a cautious migration plan from an inventory report.")
    parser.add_argument("inventory_json", help="Path to inventory JSON produced by inventory_slice.py")
    parser.add_argument("--slice-size", type=int, default=5, help="Maximum notes per suggested write slice")
    args = parser.parse_args()

    data = load_inventory(os.path.abspath(args.inventory_json))
    missing = sorted(set(data.get("missing_frontmatter", []) + data.get("missing_status", []) + data.get("missing_doc_kind", [])))
    canonical = data.get("canonical", [])
    duplicates = data.get("duplicate_titles", {})
    exact_duplicates = data.get("duplicate_exact_content", [])
    buckets = data.get("top_level_buckets", {})
    sensitive = data.get("sensitive_candidates_pending_verification", [])

    print("# Migration plan")
    print()
    print(f"Target: `{data.get('target', '')}`")
    print(f"Notes: {data.get('notes', 0)}")
    print()
    print("## Current state")
    print(f"- Canonical notes: {len(canonical)}")
    print(f"- Notes with metadata gaps: {len(missing)}")
    print(f"- Duplicate title clusters: {len(duplicates)}")
    print(f"- Exact-content duplicate clusters: {len(exact_duplicates)}")
    if buckets:
        print("- Slice buckets:")
        for name, count in sorted(buckets.items()):
            print(f"  - {name}: {count}")
    print()
    print("## Recommended write slices")
    if missing:
        for i, group in enumerate(chunk(missing, max(1, args.slice_size)), start=1):
            print(f"### Slice {i}: Add frontmatter")
            for item in group:
                print(f"- {item}")
            print()
    if not canonical:
        print("### Review canonical candidates")
        print("- No clear canonical note marker was found. Nominate one small hub page or one reference page.")
        print()
    if duplicates:
        print("### Duplicate-title review")
        for title, paths in sorted(duplicates.items()):
            print(f"- `{title}`")
            for path in paths:
                print(f"  - {path}")
        print()
    if exact_duplicates:
        print("### Exact-content duplicate review")
        for paths in exact_duplicates:
            print("- Matching content:")
            for path in paths:
                print(f"  - {path}")
        print()
    if sensitive:
        print("### Sensitive candidates (pending main-agent verification)")
        print("Note: 'pending verification' is a finding state, not a frontmatter `status:` value. Use status `needs-review` if a note in this list needs to be downgraded.")
        for item in sensitive:
            print(f"- {item}")
        print()
    print("## Verification")
    print("- Verify any items in 'Sensitive candidates (pending main-agent verification)' against the exact note text before acting")
    print("- Run validate_frontmatter.py on the target slice")
    print("- Run check_links.py before and after any rename or move")
    print("- Set contradictory notes to needs-review first; do not merge them blindly")


if __name__ == "__main__":
    main()
