#!/usr/bin/env python3
"""
KG Type Fixer - Fixes entities missing type field by inferring from ID prefix.

Usage:
    python3 kg_type_fixer.py [--dry-run] [--kg-path PATH]

Type inference rules:
    find_     -> Finding
    commit_   -> Commitment
    dec_      -> Decision
    lesson_   -> LessonLearned
    skil_     -> Skill
    skill_    -> Skill
    skc_      -> SkillCard
    ent_      -> Entity
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Type inference mapping from ID prefix to entity type
PREFIX_TYPE_MAP: Dict[str, str] = {
    "find_": "Finding",
    "commit_": "Commitment",
    "dec_": "Decision",
    "lesson_": "LessonLearned",
    "skil_": "Skill",
    "skill_": "Skill",
    "skc_": "SkillCard",
    "ent_": "Entity",
}


def infer_type(entity_id: str) -> Tuple[str, bool]:
    """
    Infer entity type from ID prefix.

    Returns:
        Tuple of (inferred_type, was_inferred)
    """
    for prefix, entity_type in PREFIX_TYPE_MAP.items():
        if entity_id.startswith(prefix):
            return entity_type, True
    return "", False


def parse_jsonl_file(filepath: Path) -> List[str]:
    """
    Parse JSONL file, handling multi-object merge lines.

    JSONL should have one JSON object per line, but sometimes multiple
    objects get merged into a single line. This function splits them
    while preserving valid JSON objects.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # First, try simple line splitting
    lines = []
    current = ''
    in_string = False
    escape_next = False

    for char in content:
        if escape_next:
            current += char
            escape_next = False
            continue

        if char == '\\' and in_string:
            current += char
            escape_next = True
            continue

        if char == '"':
            in_string = not in_string
            current += char
        elif char == '\n' and not in_string:
            if current.strip():
                lines.append(current)
            current = ''
        else:
            current += char

    if current.strip():
        lines.append(current)

    # Now split any lines with multiple JSON objects
    result_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split on }\n{ pattern (newline between closing and opening brace)
        # But be careful about being inside strings
        objects = re.split(r'(?<=})\s*(?={)', line)
        for obj in objects:
            obj = obj.strip()
            if obj:
                result_lines.append(obj)

    return result_lines


def fix_kg_file(filepath: Path, dry_run: bool = True) -> Dict[str, int]:
    """
    Fix entities missing type field in KG file.

    Args:
        filepath: Path to graph.jsonl file
        dry_run: If True, don't write changes

    Returns:
        Statistics dictionary
    """
    stats = {pt.rstrip("_"): 0 for pt in PREFIX_TYPE_MAP}
    stats["no_inference"] = 0
    stats["already_has_type"] = 0
    stats["relations"] = 0
    stats["errors"] = 0

    lines = parse_jsonl_file(filepath)
    fixed_lines = []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        try:
            obj = json.loads(line)

            # Handle relation objects (skip them)
            if obj.get("op") in ("create", "update") and "relation" in obj:
                stats["relations"] += 1
                fixed_lines.append(line)
                continue

            # Handle entity objects (create or update operations)
            if obj.get("op") in ("create", "update") and "entity" in obj:
                entity = obj["entity"]
                entity_id = entity.get("id", "")
                entity_type = entity.get("type")

                if entity_type is not None:
                    # Entity already has type
                    stats["already_has_type"] += 1
                    fixed_lines.append(line)
                elif entity_id:
                    # Try to infer type from ID prefix
                    inferred_type, was_inferred = infer_type(entity_id)
                    if was_inferred:
                        entity["type"] = inferred_type
                        obj["entity"] = entity
                        fixed_lines.append(json.dumps(obj, ensure_ascii=False))
                        # Update stats using prefix (use singular form: find -> finding)
                        prefix_to_type = {
                            "find": "finding", "commit": "commitment", "dec": "decision",
                            "lesson": "lessonlearned", "skil": "skill", "skill": "skill",
                            "skc": "skillcard", "ent": "entity"
                        }
                        for prefix in PREFIX_TYPE_MAP:
                            if entity_id.startswith(prefix):
                                key = prefix.rstrip("_")
                                stats[key] = stats.get(key, 0) + 1
                                break
                    else:
                        stats["no_inference"] += 1
                        fixed_lines.append(line)
                else:
                    # No ID, can't infer
                    stats["no_inference"] += 1
                    fixed_lines.append(line)
            else:
                # Other object types (relate, etc.)
                fixed_lines.append(line)

        except json.JSONDecodeError as e:
            print(f"ERROR: JSON decode error at line {line_num}: {e}", file=sys.stderr)
            print(f"  Content: {line[:100]}...", file=sys.stderr)
            stats["errors"] += 1
            fixed_lines.append(line)

    # Write back if not dry run
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            for line in fixed_lines:
                f.write(line + '\n')

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Fix entities missing type field in KG by inferring from ID prefix"
    )
    parser.add_argument(
        "--kg-path",
        type=str,
        default="/Users/richard/.openclaw/workspace/memory/ontology/graph.jsonl",
        help="Path to graph.jsonl file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would be changed without making changes (default: True)"
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_true",
        help="Actually write changes to the KG file"
    )

    args = parser.parse_args()

    dry_run = args.dry_run and not args.no_dry_run
    kg_path = Path(args.kg_path)

    if not kg_path.exists():
        print(f"ERROR: KG file not found: {kg_path}", file=sys.stderr)
        sys.exit(1)

    print(f"KG Type Fixer")
    print(f"=" * 50)
    print(f"KG Path: {kg_path}")
    print(f"Mode: {'DRY RUN (no changes written)' if dry_run else 'LIVE (changes will be written)'}")
    print()

    stats = fix_kg_file(kg_path, dry_run=dry_run)

    print("Statistics:")
    print("-" * 30)
    for prefix, count in sorted(stats.items()):
        if count > 0:
            print(f"  {prefix}: {count}")
    print()
    print(f"Total entities already with type: {stats['already_has_type']}")
    print(f"Total relations (unchanged): {stats['relations']}")
    print(f"Entities without type inference: {stats['no_inference']}")
    print(f"Parse errors: {stats['errors']}")

    if dry_run:
        print()
        print("DRY RUN: No changes were written.")
        print("Run with --no-dry-run to apply fixes.")


if __name__ == "__main__":
    main()
