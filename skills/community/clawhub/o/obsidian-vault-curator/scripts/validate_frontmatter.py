#!/usr/bin/env python3
import argparse
import os
import re
import sys

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
ALLOWED_STATUS = {"current", "historical", "concept", "needs-review", "reactivatable"}
ALLOWED_DOC_KIND = {"reference", "howto", "explanation", "tutorial", "research", "adr", "log", "index", "concept"}
ALLOWED_REVIEW = {"unreviewed", "reviewed", "conflict", "migrate-plan-ready", "migrated"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}
TOPIC_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = {}
    current_key = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        list_match = LIST_ITEM_RE.match(line)
        if list_match and current_key:
            data.setdefault(current_key, []).append(list_match.group(1).strip())
            continue
        if ":" not in line:
            current_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [part.strip().strip('"\'') for part in inner.split(",") if part.strip()]
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip('"\'')
    return data


def iter_markdown_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".obsidian", ".git", ".trash", "node_modules"}]
        for filename in filenames:
            if filename.lower().endswith(".md"):
                yield os.path.join(dirpath, filename)


def check_file(path: str):
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    fm = parse_frontmatter(text)
    errors = []
    if fm is None:
        errors.append("missing frontmatter")
        return errors
    if "status" in fm and fm["status"] not in ALLOWED_STATUS:
        errors.append(f"invalid status: {fm['status']}")
    if "doc_kind" in fm and fm["doc_kind"] not in ALLOWED_DOC_KIND:
        errors.append(f"invalid doc_kind: {fm['doc_kind']}")
    if "review_state" in fm and fm["review_state"] not in ALLOWED_REVIEW:
        errors.append(f"invalid review_state: {fm['review_state']}")
    if "confidence" in fm and fm["confidence"] not in ALLOWED_CONFIDENCE:
        errors.append(f"invalid confidence: {fm['confidence']}")
    if "topic" in fm and fm["topic"]:
        if not isinstance(fm["topic"], str) or not TOPIC_SLUG_RE.match(fm["topic"]):
            errors.append(f"invalid topic slug: {fm['topic']}")
    for key in ("canonical_for", "supersedes", "superseded_by"):
        if key in fm and not isinstance(fm[key], list):
            errors.append(f"{key} should be a list")
    if "canonical" in fm and not isinstance(fm["canonical"], bool):
        errors.append("canonical should be true/false")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate controlled frontmatter on one slice.")
    parser.add_argument("target", help="Folder or note path to inspect")
    args = parser.parse_args()

    root = os.path.abspath(args.target)
    if not os.path.exists(root):
        raise SystemExit(f"Target not found: {root}")
    files = [root] if os.path.isfile(root) else sorted(iter_markdown_files(root))
    if not files:
        print(f"No markdown files found in target: {root}")
        sys.exit(1)
    failures = 0
    for path in files:
        errors = check_file(path)
        if errors:
            failures += 1
            print(f"[FAIL] {path}")
            for error in errors:
                print(f"  - {error}")
    if failures == 0:
        print(f"OK: validated {len(files)} markdown files")
        return
    print(f"\n{failures} file(s) failed validation")
    sys.exit(1)


if __name__ == "__main__":
    main()
