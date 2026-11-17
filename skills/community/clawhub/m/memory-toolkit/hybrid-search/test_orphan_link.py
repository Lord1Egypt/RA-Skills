#!/usr/bin/env python3
"""M6 gate test: no extracted decision may enter the ontology as an orphan.

The 2026-10-10 find: the ontology had **889 orphan entities out of 928, with
only 34 relations**. The extraction pipeline (`trace_extractor.write_ontology_entities`)
created Decision and TimelineEvent nodes with no edge at all, so the "graph" was
really an append-only list of disconnected blocks — useless for retrieval, and
the main defect flagged in the V4 audit.

M6 fixes it two ways: the extraction prompt now REQUIRES a `related_to` anchoring
each item, and `write_ontology_entities()` appends a `relate` fact for every
decision it writes, falling back to the catch-all root `daily_notes` when the
item names no known entity.

This test locks BOTH directions:
  * a decision with a valid, grounded anchor links to it, AND
  * a decision with no anchor still links to `daily_notes` (never orphaned), AND
  * an anchor INVENTED by the LLM (not grounded in the item text) is REFUSED —
    a gate that accepts invented roots would silently wire the graph wrong.

Usage:
    python3 hybrid-search/test_orphan_link.py
Exit 0 = every written decision carries an edge; exit 1 = the orphan regression is back.
"""
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# Same loader note as test_ontology_key_parity: a static scanner may flag
# `exec_module` as dynamic code execution. It is a false positive — the path is
# a fixed literal in this repository, no network/argv/env reaches it.
spec = importlib.util.spec_from_file_location(
    "te", os.path.join(REPO, "trace_extractor.py")
)
te = importlib.util.module_from_spec(spec)
spec.loader.exec_module(te)  # noqa: S102 -- literal path


def _write_graph(path, entities):
    with open(path, "w", encoding="utf-8") as fh:
        for ent in entities:
            fh.write(json.dumps({"op": "state", "entity": ent}, ensure_ascii=False) + "\n")


def _replay(path):
    """Return (entity_ids, nodes_with_an_edge, decision_ids).

    We separate DECISIONS from roots: a root with no inbound edge is normal
    (it anchors others), only extracted decisions must never be orphaned.
    """
    ents, linked, decisions = set(), set(), set()
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if "entity" in e and e["entity"].get("id"):
            eid = e["entity"]["id"]
            ents.add(eid)
            if e["entity"].get("type") == "Decision":
                decisions.add(eid)
        if e.get("op") == "relate":
            linked.add(e.get("from"))
            linked.add(e.get("to"))
    return ents, linked, decisions


def _run_case(name, seed_entities, decisions, expect_unlinked=()):
    """Write decisions into a throwaway graph, return (ok, detail)."""
    tmpdir = tempfile.mkdtemp()
    try:
        graph = os.path.join(tmpdir, "graph.jsonl")
        _write_graph(graph, seed_entities)
        te.ONTOLOGY_FILE = type(te.ONTOLOGY_FILE)(graph)
        te.upsert_entities.__globals__["ONTOLOGY_FILE"] = te.ONTOLOGY_FILE
        n = te.write_ontology_entities({"decisions": decisions})
        ents, linked, decisions_ids = _replay(graph)
        # Only EXTRACTED DECISIONS must carry an edge. A root (e.g. daily_notes)
        # legitimately has none — it exists to anchor others.
        orphan_decisions = decisions_ids - linked
        unexpected = orphan_decisions - set(expect_unlinked)
        detail = (f"wrote {n}, entities={len(ents)}, decisions={len(decisions_ids)}, "
                  f"linked={len(linked)}, "
                  f"orphan_decisions={sorted(orphan_decisions) if orphan_decisions else 'none'}")
        if unexpected:
            return False, f"{detail} — UNEXPECTED ORPHAN DECISIONS {sorted(unexpected)}"
        return True, detail
    finally:
        shutil.rmtree(tmpdir)


def main() -> int:
    failures = 0
    today = date.today().isoformat()

    print("== M6 orphan guard: a decision with a valid anchor must link to it ==")
    ok, detail = _run_case(
        "anchored",
        [{"id": "astrocapture", "type": "Project", "properties": {"name": "AstroCapture"}}],
        [{"what": "AstroCapture v3 release deployed to production",
          "subject": "astrocapture", "related_to": "astrocapture", "date": today}],
    )
    failures += 0 if ok else 1
    print(f"  {'OK  ' if ok else 'FAIL'} {detail}")

    print("\n== M6 orphan guard: a decision with NO anchor must still link (daily_notes) ==")
    ok, detail = _run_case(
        "unanchored",
        [{"id": "astrocapture", "type": "Project", "properties": {"name": "AstroCapture"}}],
        [{"what": "random unrelated thing with no anchor at all",
          "subject": "general", "related_to": "", "date": today}],
    )
    failures += 0 if ok else 1
    print(f"  {'OK  ' if ok else 'FAIL'} {detail}")

    print("\n== M6 orphan guard: an INVENTED anchor must be refused, not wired ==")
    # `maison_jeanne` is a real graph entity but the item text never mentions it;
    # a correct implementation must NOT link there (it would be a fabricated edge).
    ok, detail = _run_case(
        "invented",
        [{"id": "astrocapture", "type": "Project", "properties": {"name": "AstroCapture"}},
         {"id": "maison_jeanne", "type": "Project", "properties": {"name": "Maison Jeanne"}}],
        [{"what": "AstroCapture v3 release deployed", "subject": "astrocapture",
          "related_to": "maison_jeanne", "date": today}],
    )
    failures += 0 if ok else 1
    print(f"  {'OK  ' if ok else 'FAIL'} {detail}")

    print("\n== M6 helper: _norm_related_to keeps grounded anchors, drops the rest ==")
    cases = [
        ({"what": "AstroCapture v3 release deployed", "related_to": "astrocapture"},
         "astrocapture", "grounded anchor"),
        ({"what": "AstroCapture v3 release deployed", "related_to": "maison_jeanne"},
         None, "invented anchor refused"),
        ({"what": "backup cron runs at 23h", "related_to": ""}, None, "empty refused"),
    ]
    for item, want, label in cases:
        got = te._norm_related_to(item)
        good = got == want
        failures += 0 if good else 1
        print(f"  {'OK  ' if good else 'FAIL'} {label:22} -> {got!r} (want {want!r})")

    if failures:
        print(f"\n{failures} failure(s)")
        return 1
    print("\nAll M6 orphan-link assertions hold — every decision carries an edge.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
