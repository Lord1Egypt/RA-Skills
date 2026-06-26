#!/bin/bash
set -euo pipefail

CMD="${1:-system-prompt}"
WORKDIR="${2:-.}"
ADD_DIRS_RAW="${3:-${CC_ADD_DIRS:-}}"
DOC_BASENAME="${CLAUDE_DELEGATE_DOC_BASENAME:-CLAUDE.delegate.md}"

python3 - "$CMD" "$WORKDIR" "$ADD_DIRS_RAW" "$DOC_BASENAME" <<'PY'
from pathlib import Path
import os
import sys

cmd, workdir_raw, add_dirs_raw, doc_basename = sys.argv[1:5]
workspace_doc_names = ["AGENTS.md", "TOOLS.md", "README.md"]


def norm(path: str):
    if not path:
        return None
    expanded = os.path.expandvars(os.path.expanduser(path))
    try:
        return Path(expanded).absolute()
    except Exception:
        return Path(expanded)


roots = []
seen_roots = set()


def add_root(path: str):
    candidate = norm(path)
    if candidate is None:
        return
    key = str(candidate)
    if key in seen_roots:
        return
    seen_roots.add(key)
    roots.append(candidate)


add_root(workdir_raw)
for item in add_dirs_raw.split(":"):
    add_root(item)


def ancestor_chain(path: Path):
    chain = [path]
    chain.extend(path.parents)
    return chain


delegate_docs = []
coord_docs = []
seen_delegate = set()
seen_coord = set()

for root in roots:
    for folder in ancestor_chain(root):
        delegate_candidate = folder / doc_basename
        if delegate_candidate.is_file():
            key = str(delegate_candidate)
            if key not in seen_delegate:
                seen_delegate.add(key)
                delegate_docs.append(key)
        for name in workspace_doc_names:
            candidate = folder / name
            if candidate.is_file():
                key = str(candidate)
                if key not in seen_coord:
                    seen_coord.add(key)
                    coord_docs.append(key)

if cmd == "list":
    print("\n".join(delegate_docs))
    raise SystemExit(0)

if cmd != "system-prompt":
    raise SystemExit(f"Unknown command: {cmd}")

lines = [
    "Claude Delegate bootstrap:",
    f"- Before substantive work, discover and read every `{doc_basename}` file you can reach from the current workdir, its ancestor directories, and any extra add-dir roots.",
    "- Start with the nearest repo or workspace file and let it override broader guidance when there is tension.",
    "- Then inspect the immediate workspace before editing, especially nearby `AGENTS.md`, `TOOLS.md`, `README.md`, and the files most relevant to the task.",
    "- You are operating alongside other local agents and operator workflows, so treat these docs as coordination context, not optional decoration.",
    "- Use quick shell discovery if you think more nearby copies exist, but do not skip the listed files.",
]

if delegate_docs:
    lines.append("")
    lines.append(f"Discovered `{doc_basename}` files (nearest-first):")
    for path in delegate_docs:
        lines.append(f"- {path}")
else:
    lines.append("")
    lines.append(f"No `{doc_basename}` files were pre-discovered from the current roots. Still do a quick local check before you start.")

if coord_docs:
    lines.append("")
    lines.append("Nearby workspace docs worth checking early:")
    for path in coord_docs:
        lines.append(f"- {path}")

print("\n".join(lines))
PY
