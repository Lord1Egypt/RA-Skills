#!/usr/bin/env python3
import re, sys
from pathlib import Path
def main(path: str) -> None:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    in_fence = False
    print("## Table of Contents")
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level, title = len(m.group(1)), m.group(2).strip()
            anchor = re.sub(r"[^a-z0-9\- ]", "", title.lower()).replace(" ", "-")
            print(f"{"  " * (level-1)}- [{title}](#{anchor})")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "README.md")
