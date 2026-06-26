#!/usr/bin/env python3
"""
BuildModuleGraph.py
Generate module dependency graph from markdown links in References/*.md
Outputs:
- References/ModuleGraph.md (human-readable)
- References/ModuleGraph.json (machine-readable)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REF_DIR = Path(__file__).resolve().parents[1] / "References"
GRAPH_MD = REF_DIR / "ModuleGraph.md"
GRAPH_JSON = REF_DIR / "ModuleGraph.json"

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)", re.IGNORECASE)
SEE_ALSO_RE = re.compile(r"See also:\s*<([^>]+\.md)>", re.IGNORECASE)


def parse_links(text: str) -> list[str]:
    links = LINK_RE.findall(text)
    links += SEE_ALSO_RE.findall(text)
    return links


def build_graph() -> dict:
    modules = sorted(p.name for p in REF_DIR.glob("*.md") if p.name not in {"ModuleGraph.md", "ReferenceMap.md"})
    edges: dict[str, list[str]] = {m: [] for m in modules}

    for mod in modules:
        p = REF_DIR / mod
        text = p.read_text(encoding="utf-8", errors="ignore")
        deps: list[str] = []
        for raw in parse_links(text):
            name = Path(raw).name
            if name in edges and name != mod:
                deps.append(name)
        edges[mod] = sorted(set(deps))

    return {"modules": modules, "edges": edges}


def write_outputs(graph: dict) -> None:
    GRAPH_JSON.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Module Graph", "", "Auto-generated dependency graph between markdown modules.", "", "## Nodes"]
    for m in graph["modules"]:
        lines.append(f"- `{m}`")

    lines.append("")
    lines.append("## Edges")
    for src in graph["modules"]:
        deps = graph["edges"].get(src, [])
        if deps:
            lines.append(f"- `{src}` -> {', '.join(f'`{d}`' for d in deps)}")
        else:
            lines.append(f"- `{src}` -> (none)")

    lines.append("")
    lines.append("## Notes")
    lines.append("- Rebuild with: `python Scripts/BuildModuleGraph.py`")
    lines.append("- Pair with `BuildReferenceMap.py` after adding new modules.")

    GRAPH_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    graph = build_graph()
    write_outputs(graph)
    print(f"Updated: {GRAPH_MD}")
    print(f"Updated: {GRAPH_JSON}")
    print(f"Modules: {len(graph['modules'])}")


if __name__ == "__main__":
    main()
