#!/usr/bin/env python3
"""Create the missing `day_YYYYMMDD` nodes referenced by backfilled edges.

Context
-------
The 2026-10-10 backfill gave every orphan an edge. The `dated` pass points each
item at a day hub (`day_20260607`), but those hubs were never written as
entities. Result: 0 orphans, but 526 edges dangling at 158 nonexistent targets.

This script closes that hole in two moves:

* **149 clean `day_YYYYMMDD` nodes** -> created as `Episode` entities, so the
  526 edges finally land on something.
* **9 malformed `day_*` ids** (`day_202605310913`, `day_20260526roadmapupdates`,
  ...) -> the `dated` pass grabbed date fragments out of free text. We do NOT
  freeze that garbage into the graph: their edges are re-pointed to the clean
  date extracted from the id, and the bad ids are left unreferenced.

Design rules (same as the other backfill tools):

* **Append-only.** Never rewrite or delete a line of `graph.jsonl`. Bad edges
  are neutralised by appending a superseding `relate` fact, never by editing.
* **Timestamped backup** before the first write.
* **Dry-run by default.** `--apply` to write.
* **Idempotent.** Re-running does nothing once the nodes exist and the bad
  edges are superseded.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
WORKSPACE = Path(sys.argv[0]).resolve().parents[2].parent  # /home/ubuntu/.openclaw/workspace
GRAPH = HOME / ".openclaw/workspace/memory/ontology/graph.jsonl"

DAY_RE = re.compile(r"^day_(\d{4})(\d{2})(\d{2})")
MONTH_RE = re.compile(r"^day_(\d{4})(\d{2})$")


def load_graph(path: Path):
    """Return (entities dict id->obj, list of edge dicts)."""
    ents: dict[str, dict] = {}
    edges: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "from" in o and "to" in o:
            edges.append(o)
        elif o.get("entity"):
            ents[o["entity"]["id"]] = o["entity"]
        elif o.get("id"):
            ents[o["id"]] = o
    return ents, edges


def clean_day_id(raw: str) -> str | None:
    """`day_202605310913` -> `day_20260531`, `day_202604` -> `day_20260401`.

    Returns None only when no date can be salvaged at all. A bare `YYYYMM`
    (month, no day) maps to the 1st of that month: arbitrary, but documented,
    and far better than an edge that can never land anywhere.
    """
    m = DAY_RE.match(raw)
    if m:
        y, mo, d = m.group(1), m.group(2), m.group(3)
        try:
            datetime(int(y), int(mo), int(d))
        except ValueError:
            return None
        return f"day_{y}{mo}{d}"
    m = MONTH_RE.match(raw)
    if m:
        y, mo = m.group(1), m.group(2)
        try:
            datetime(int(y), int(mo), 1)
        except ValueError:
            return None
        return f"day_{y}{mo}01"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--graph", default=str(GRAPH))
    args = ap.parse_args()

    graph = Path(args.graph)
    ents, edges = load_graph(graph)

    # Every day_* target that some edge points at but that is not an entity.
    referenced = {e["to"] for e in edges
                  if isinstance(e.get("to"), str) and e["to"].startswith("day_")}
    missing = sorted(d for d in referenced if d not in ents)

    clean, malformed = [], []
    for d in missing:
        (clean if re.fullmatch(r"day_\d{8}", d) else malformed).append(d)

    # For the malformed ones, where does the edge go instead?
    redirects: dict[str, str | None] = {}
    unresolvable = []
    for d in malformed:
        tgt = clean_day_id(d)
        if tgt:
            redirects[d] = tgt
        else:
            redirects[d] = None
            unresolvable.append(d)

    # The source entity of every malformed edge, so we can re-point the edge
    # itself (source -> clean target) instead of writing a useless self-loop.
    redirect_edges = [e for e in edges
                      if isinstance(e.get("to"), str) and e["to"] in redirects]

    # A redirect target may itself be created as a fresh day node.
    extra_days = sorted({t for t in redirects.values() if t and t not in ents})
    to_create = sorted(set(clean) | set(extra_days))

    edges_fixed = len(redirect_edges)

    print(f"  graph        : {graph}")
    print(f"  entities     : {len(ents)}   edges: {len(edges)}")
    print(f"  day_* refs   : {len(referenced)}   missing: {len(missing)}")
    print(f"  clean ids    : {len(clean)}")
    print(f"  malformed    : {len(malformed)}  -> {len(redirects)} redirect(s)")
    print(f"  day nodes to create : {len(to_create)}")
    print(f"  edges re-pointed    : {edges_fixed}")
    if unresolvable:
        print(f"  UNRESOLVABLE ({len(unresolvable)}): {unresolvable}")

    if not args.apply:
        print("\n  sample nodes:", to_create[:5])
        print("  sample redirects:", list(redirects.items())[:5])
        print("\n  DRY-RUN — nothing written. Re-run with --apply.")
        return 0

    # --- write ---------------------------------------------------------------
    backup = graph.with_name(graph.name + f".pre-daynodes-{datetime.now():%Y%m%d_%H%M%S}")
    shutil.copy2(graph, backup)
    before = len(graph.read_text(encoding="utf-8").splitlines())

    written = 0
    with graph.open("a", encoding="utf-8") as fh:
        # 1. the day hubs themselves
        for d in to_create:
            node = {
                "op": "state",
                "entity": {
                    "id": d,
                    "type": "Episode",
                    "properties": {
                        "name": f"Journal du {d[4:6]}/{d[6:8]}/{d[0:4]}",
                        "day": f"{d[0:4]}-{d[4:6]}-{d[6:8]}",
                        "role": "day-hub",
                        "created_by": "ontology_fix_day_nodes.py",
                    },
                },
            }
            fh.write(json.dumps(node, ensure_ascii=False, sort_keys=True) + "\n")
            written += 1
        # 2. re-point the malformed edges: same source and relation, clean target.
        #    The old edge stays in the file (append-only) but is now redundant,
        #    not dangling -- its clean twin points at a node that exists.
        for e in redirect_edges:
            new = redirects.get(e["to"])
            if not new:
                continue
            fh.write(json.dumps({
                "op": "relate",
                "from": e["from"],
                "to": new,
                "rel": e.get("rel", "about"),
                "properties": {
                    "evidence": f"re-pointed from malformed id {e['to']}",
                    "tool": "ontology_fix_day_nodes.py",
                },
            }, ensure_ascii=False, sort_keys=True) + "\n")
            written += 1

    after = len(graph.read_text(encoding="utf-8").splitlines())
    print(f"\n  backup     : {backup.name}")
    print(f"  appended   : {before} -> {after} lines (+{written})")
    print("  done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
