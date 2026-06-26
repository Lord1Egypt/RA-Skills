#!/usr/bin/env python3
"""Export Obsidian vault vector notes to vectors.json."""

import json
import re
import sys
from pathlib import Path

VAULT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "obsidian-vault" / "compass" / "vectors"
OUTPUT = Path(__file__).resolve().parent / "vectors.json"


def parse_frontmatter(text: str) -> dict | None:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        # Parse list values like [0.8, -0.6, 0.3]
        if val.startswith("[") and val.endswith("]"):
            try:
                val = json.loads(val)
            except json.JSONDecodeError:
                pass
        # Parse numbers
        elif re.match(r"^-?\d+\.?\d*$", val):
            val = float(val)
        # Strip wiki links
        if isinstance(val, str) and val.startswith("[[") and val.endswith("]]"):
            val = val[2:-2]
        fm[key] = val
    return fm


def main():
    vault_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else VAULT_DIR
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT

    if not vault_dir.exists():
        print(f"No vectors directory: {vault_dir}")
        json.dump([], output.open("w"))
        return

    vectors = []
    for md in sorted(vault_dir.glob("*.md")):
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        if not fm or fm.get("type") != "vector":
            continue
        vectors.append({
            "file": md.name,
            "date": fm.get("date", ""),
            "what": fm.get("what", ""),
            "why_essence": fm.get("why_essence", ""),
            "direction": fm.get("direction", [0, 0, 0]),
            "intensity": float(fm.get("intensity", 0.5)),
            "confidence": float(fm.get("confidence", 0.5)),
            "cluster": fm.get("cluster", "uncategorized"),
            "tags": fm.get("tags", []),
        })

    output.write_text(json.dumps(vectors, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported {len(vectors)} vectors to {output}")


if __name__ == "__main__":
    main()
