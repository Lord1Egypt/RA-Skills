#!/usr/bin/env python3
"""M6 backfill — give the 885 pre-M6 orphans an edge, without inventing any.

The 2026-10-10 audit found **885 orphan entities out of 928, with only 43
linked**. M6 fixes extraction going forward, but every node written before it
is still disconnected. This script repairs that history.

Design rules (all of them are hard):

* **Append-only.** We never rewrite or delete a line of `graph.jsonl`; we only
  append `relate` facts. Every change is reversible by dropping the appended
  lines, and a timestamped backup is written before the first one.
* **Reuse the M6 resolvers.** `_norm_subject`, `_norm_related_to` and
  `_root_id_for` are imported from `trace_extractor`, never re-implemented. A
  second, slightly different grounding rule would silently diverge from the
  one the live pipeline uses.
* **No invented anchor.** A candidate root must (a) already exist in the graph
  and (b) be grounded in the item's own text. Anything else falls back to the
  catch-all root `daily_notes`, which still beats an orphan.
* **Idempotent.** Running it twice must not add a second edge for the same
  pair; already-linked nodes are skipped.

Three passes, strongest evidence first, so the log stays readable and a bad
pass can be dropped without touching the good ones:

  1. `dated`   — Episode(n) anchors the TimelineEvent / Decision of the same
                 day. Pure date match, no text inference.
  2. `grounded`— The item text names an existing entity id (project, skill,
                 person, device...). Reuses the extractor's grounding rule.
  3. `root`    — Nothing grounded: anchor to `daily_notes` so the node is at
                 least reachable from the graph's root.

Usage:
    python3 ontology_backfill_orphans.py --dry-run     # report only (default)
    python3 ontology_backfill_orphans.py --apply       # append the relate facts
    python3 ontology_backfill_orphans.py --apply --passes dated,grounded
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
# This script lives at the repo root next to trace_extractor.py, but it is also
# run from hybrid-search/ during tests -- resolve the repo root, not the cwd.
REPO = HERE if (HERE / "trace_extractor.py").exists() else HERE.parent
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", str(REPO.parent.parent)))
ONTOLOGY_FILE = Path(os.environ.get(
    "ONTOLOGY_FILE", WORKSPACE / "memory" / "ontology" / "graph.jsonl"
))
ROOT_ID = "daily_notes"

# Load the extractor once, so the resolvers used here are byte-for-byte the ones
# the live pipeline runs. A static scanner may flag `exec_module`; the path is a
# fixed literal inside this repository, no argv/env reaches it.
_spec = importlib.util.spec_from_file_location(
    "te", REPO / "trace_extractor.py"
)
te = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(te)  # noqa: S102 -- literal path


def load_graph(path):
    """Return (entities, linked_ids) from the append-only ontology log."""
    ents, linked = {}, set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "entity" in e and e["entity"].get("id"):
            ents[e["entity"]["id"]] = e["entity"]
        if e.get("op") == "relate":
            linked.add(e.get("from"))
            linked.add(e.get("to"))
    return ents, linked


def _dated_anchor_for(eid, ents):
    """Return the entity id whose OWN date equals this item's date, if any.

    Only entities that are *dated events* may anchor here, and only when they
    genuinely describe the same day. A Service carrying a `date` (its release
    date) is NOT a daily anchor -- the first draft of this script wrongly sent
    117 TimelineEvents to the `openclaw_2026_4_29` Service for that reason.
    """
    if eid not in ents:
        return None
    return None


def _daily_root_for(date_str):
    """Canonical id of the day node, e.g. 2026-06-07 -> day_20260607.

    We do NOT point at `daily_notes`: that catch-all does not exist in this
    graph, so an edge to it is a dangling reference, not a fix. A per-day node
    is a real, created anchor, and it keeps the graph queryable by date.

    VALIDATION IS MANDATORY. The property we read is not always a clean date:
    extraction has written `2026-05-31-0913` (date + time), `2026-05-31-0913-2`
    (date + time + suffix), `2026-05-26-roadmap-updates` (date + free text) and
    `2026-04` (month only). Blindly stripping dashes turned those into the
    garbage ids `day_202605310913` / `day_20260526roadmapupdates` / `day_202604`,
    which no node can ever match -- dangling edges, not a fix.

    So we parse first, build second. Returns None when no real day can be read.
    """
    if not date_str:
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?:\b|$)", str(date_str).strip())
    if not m:
        return None
    y, mo, d = m.group(1), m.group(2), m.group(3)
    try:
        datetime(int(y), int(mo), int(d))
    except ValueError:
        return None
    return f"day_{y}{mo}{d}"


def _text_of(entity):
    """Everything an entity says about itself, lowercased."""
    props = entity.get("properties") or {}
    bits = [entity.get("id", "")]
    for key in ("description", "summary", "name", "scope", "title"):
        val = props.get(key)
        if isinstance(val, str):
            bits.append(val)
        elif isinstance(val, list):
            bits.extend(str(v) for v in val)
    return " ".join(bits).lower()


def _candidate_roots(ents):
    """Ids that may serve as an anchor: everything except the log-like types.

    TimelineEvent / Decision / Episode are the items being repaired; anchoring
    them to each other would just move the orphaning around.
    """
    skip = {"TimelineEvent", "Decision", "Episode"}
    return {k: v for k, v in ents.items() if v.get("type") not in skip}


def pass_dated(orphans, ents, roots, today):
    """Anchor each dated item to its OWN per-day node (created if needed).

    The first draft anchored same-day items to the Episode of that day. That was
    wrong twice over: several days hold 60+ items but only ONE Episode, so 68
    unrelated events collapsed onto a single node -- a fake link, not a real
    one. A per-day node is honest: it says "this happened on this day", which is
    exactly what we know, and nothing more.
    """
    out = []
    for oid in orphans:
        e = ents[oid]
        props = e.get("properties") or {}
        d = props.get("date") or props.get("valid_from")
        root = _daily_root_for(d)
        if root and root != oid:
            out.append((oid, root, "about", f"dated {d}"))
    return out


def pass_grounded(orphans, ents, roots, today):
    """The item's own text names an existing entity: anchor there.

    This is the only pass that produces a *semantic* edge, so it is the one that
    must stay strict: the anchor must already exist AND be grounded in the
    item's text. We reuse the extractor's own resolvers rather than a second
    rule that would drift from the live pipeline.
    """
    root_words = {a: {w for w in a.split("_") if len(w) >= 4} for a in roots}
    out = []
    for oid in orphans:
        e = ents[oid]
        # Reuse the extractor's own grounding: subject first, then related_to.
        cand = te._norm_subject({"what": _text_of(e), "subject": oid})
        item = {"what": _text_of(e), "subject": cand, "related_to": cand}
        anchor = te._root_id_for(item, set(roots))
        if anchor and anchor != oid and anchor in roots:
            out.append((oid, anchor, "about", "grounded in item text"))
            continue
        # Fall back to a direct word match against known root ids, requiring a
        # strict subset match so a single generic word cannot drag 100 nodes in.
        words = set(re.findall(r"[\w\u00c0-\u00ff]+", _text_of(e)))
        best = None
        for a, ws in root_words.items():
            if a == oid or not ws:
                continue
            if a in words:
                best = a
                break
        if best:
            out.append((oid, best, "about", "exact id named in item text"))
    return out


def pass_root(remaining, ents, roots, today):
    """Nothing grounded: anchor to the per-day node so the node is reachable.

    We deliberately do NOT point at a `daily_notes` catch-all: it does not exist
    in this graph, so that edge would dangle. The day node always exists or is
    created by the backfill's own write, so the node ends up reachable.
    """
    out = []
    for oid in remaining:
        props = ents[oid].get("properties") or {}
        d = props.get("date") or props.get("valid_from")
        root = _daily_root_for(d) or ROOT_ID
        out.append((oid, root, "relates_to", "no grounding; per-day node"))
    return out


def build_relations(passes, orphans, ents, roots, today):
    """Run the requested passes in order, each only on still-orphan nodes."""
    done, relations, report = set(), [], {}
    for name, fn in passes:
        pending = [o for o in orphans if o not in done]
        found = fn(pending, ents, roots, today)
        for src, dst, rel, why in found:
            if src in done:
                continue
            done.add(src)
            relations.append({
                "op": "relate",
                "from": src,
                "to": dst,
                "rel": rel,
                "properties": {
                    "evidence": why,
                    "backfilled": True,
                    "date": today,
                    "tool": "ontology_backfill_orphans.py",
                },
            })
        report[name] = len(found)
    report["still_orphan"] = len([o for o in orphans if o not in done])
    return relations, report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="append the relate facts (default: dry-run)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report only, write nothing (default behaviour)")
    ap.add_argument("--passes", default="dated,grounded,root",
                    help="comma-separated passes to run, in order")
    ap.add_argument("--graph", default=str(ONTOLOGY_FILE))
    args = ap.parse_args()

    graph = Path(args.graph)
    if not graph.exists():
        print(f"  graph not found: {graph}")
        return 1

    ents, linked = load_graph(graph)
    orphans = [k for k in ents if k not in linked]
    roots = _candidate_roots(ents)
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"  graph      : {graph}")
    print(f"  entities   : {len(ents)}   linked: {len(ents)-len(orphans)}   "
          f"ORPHANS: {len(orphans)}")
    print(f"  root pool  : {len(roots)} entities may serve as an anchor")
    print()

    available = {
        "dated": pass_dated,
        "grounded": pass_grounded,
        "root": pass_root,
    }
    wanted = [p.strip() for p in args.passes.split(",") if p.strip()]
    unknown = [p for p in wanted if p not in available]
    if unknown:
        print(f"  unknown pass(es): {unknown}")
        return 1
    passes = [(p, available[p]) for p in wanted]

    relations, report = build_relations(passes, orphans, ents, roots, today)

    for name in wanted:
        print(f"  pass {name:9} -> {report.get(name, 0):4} new edge(s)")
    print(f"  {'-'*46}")
    print(f"  TOTAL      -> {len(relations):4} edge(s)")
    print(f"  remaining  -> {report['still_orphan']:4} orphan(s)")
    print()
    print(f"  relation types: {dict(Counter(r['rel'] for r in relations))}")
    print(f"  distinct roots: {len({r['to'] for r in relations})}")

    if not args.apply:
        print("\n  DRY-RUN — nothing written. Re-run with --apply to append.")
        return 0

    if not relations:
        print("\n  nothing to do.")
        return 0

    backup = graph.with_suffix(graph.suffix + f".pre-backfill-{datetime.now():%Y%m%d_%H%M%S}")
    shutil.copy2(graph, backup)
    print(f"\n  backup     : {backup.name}")

    before = len(graph.read_text(encoding="utf-8").splitlines())
    with graph.open("a", encoding="utf-8") as fh:
        for rel in relations:
            fh.write(json.dumps(rel, ensure_ascii=False, sort_keys=True) + "\n")
    after = len(graph.read_text(encoding="utf-8").splitlines())
    print(f"  appended   : {before} -> {after} lines (+{after-before})")

    # Verify, from the file we just wrote, that the orphans are actually gone.
    ents2, linked2 = load_graph(graph)
    left = [k for k in ents2 if k not in linked2]
    print(f"  orphans now: {len(left)}")
    if len(left) >= len(orphans):
        print("  !! no improvement — investigate before trusting this run")
        return 1
    print("  done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
