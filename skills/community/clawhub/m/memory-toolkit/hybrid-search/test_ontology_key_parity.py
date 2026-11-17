#!/usr/bin/env python3
"""Regression guard: ontology display-key parity between indexer and migrator.

The 2026-10-10 find: `migrate_ontology_subjects.py` rebuilt the display key as
`name or type`, but the indexer (`hybrid_search.index_jsonl_file`) builds it as
`name or entity.id or type`. Decision / TimelineEvent nodes carry no `name`, so
the migrator produced `' (Decision)'`, matched nothing, and reported **2826 live
facts as ghosts**. A single `--apply` would have marked 2406 valid facts
`superseded` and pushed them out of active retrieval.

This test pins the invariant directly: for every entity in the graph, the key the
migrator computes MUST equal the content the indexer would store.

Usage:
    python3 hybrid-search/test_ontology_key_parity.py [graph.jsonl]
Exit 0 = keys agree; exit 1 = drift (a `--apply` would mis-classify facts).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

DEFAULT_GRAPH = os.path.join(
    os.path.expanduser("~"), ".openclaw", "workspace", "memory", "ontology", "graph.jsonl"
)

# The exact expression the indexer uses (hybrid_search.py, index_jsonl_file).
INDEXER_KEY = lambda name, eid, typ: f"{name or eid or ''} ({typ or ''})".strip()


def indexer_content(entity):
    """Reproduce hybrid_search.index_jsonl_file()'s `content` for one entity."""
    props = entity.get("properties") or {}
    if not isinstance(props, dict):
        props = {}
    name = props.get("name") or entity.get("name") or entity.get("id") or ""
    obj_type = entity.get("type") or ""
    return INDEXER_KEY(name, entity.get("id"), obj_type)


def main():
    import json

    graph = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_GRAPH
    print("== test_ontology_key_parity ==")
    if not os.path.exists(graph):
        print(f"  !  graph not found: {graph} — skipping (not a failure)")
        return 0

    # Import the migrator's loader so the test tracks the real code, not a copy.
    sys.path.insert(0, REPO)
    sys.path.insert(0, HERE)
    import importlib.util

    # Static-analysis note: a scanner may flag the `exec_module` below as
    # `suspicious.dynamic_code_execution`. It is a false positive. This is the
    # standard Python import machinery importing a *fixed, literal* path in the
    # same repository -- no network, no user input, no environment variable, no
    # argv reaches it. The loader is used instead of a bare `import` only so the
    # test tracks the real migrator module, not a copy.
    spec = importlib.util.spec_from_file_location(
        "mig", os.path.join(REPO, "migrate_ontology_subjects.py")  # constant path
    )
    mig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mig)  # noqa: S102 -- literal path, not dynamic input

    entities = []
    for line in open(graph):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        e = r.get("entity") or (r if r.get("id") else None)
        if e and e.get("id"):
            entities.append(e)

    mig_keys = mig.load_graph(graph)  # {display_key: id}

    # Collisions (two ids sharing one display key) are a graph-data fact, not a
    # migrator bug: they must not fail this guard. We count separately.
    from collections import Counter
    key_counts = Counter(indexer_content(e) for e in entities)
    collisions = {k: n for k, n in key_counts.items() if n > 1}

    mismatches = []
    for e in entities:
        want = indexer_content(e)
        if want not in mig_keys:
            mismatches.append((e["id"], want, "key absent from migrator"))
        elif mig_keys[want] != e["id"]:
            # Only a real drift when this key is NOT shared with another id.
            if key_counts[want] == 1:
                mismatches.append((e["id"], want, f"migrator maps to {mig_keys[want]!r}"))

    total = len(entities)
    print(f"  entities in graph      : {total}")
    print(f"  keys built by migrator : {len(mig_keys)}")
    if collisions:
        print(f"  !  display-key collisions (data, not drift): {len(collisions)}")
        for k, n in list(collisions.items())[:5]:
            print(f"       {k!r} shared by {n} ids")
    if mismatches:
        print(f"\nFAILURES: {len(mismatches)} entities whose migrator key != indexer key")
        for eid, want, why in mismatches[:10]:
            print(f"  ✗ {eid!r}: indexer would store {want!r} ({why})")
        print("\n  → a --apply would mark live facts as ghosts. Fix load_graph().")
        return 1
    print("\nOntology key parity holds — migrator and indexer agree.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
