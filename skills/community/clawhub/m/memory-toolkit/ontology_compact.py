#!/usr/bin/env python3
"""Ontology graph compactor (GC for the OP-log).

Reads memory/ontology/graph.jsonl (an append-only operation log), replays it
into a consolidated state, and writes one line per active entity.

Safety: backs up first, writes to a temp file, validates entity-by-entity,
and only swaps in place if the state is provably identical.

Usage:
    python3 scripts/ontology-compact.py --dry-run   # report only
    python3 scripts/ontology-compact.py             # compact if safe
    python3 scripts/ontology-compact.py --min-gain 10  # skip if <10% smaller
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw/workspace"))
GRAPH = WORKSPACE / "memory" / "ontology" / "graph.jsonl"
BACKUP_DIR = WORKSPACE / "memory" / "ontology" / "backups"


def replay(path):
    """Replay the op-log into final entity state + superseded ids.

    M3: relations are replayed too, not just entities. A `relate` op whose source
    or target entity is superseded (or never existed) used to survive compaction
    as an orphan edge. We now collect them so they can be dropped explicitly and
    reported, instead of silently lingering in the graph.
    """
    entities = {}
    superseded = set()
    order = []
    relations = []          # every relate op seen, in order
    bad = 0
    total = 0

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue
        if r.get("op") == "supersede":
            eid = r.get("entity_id")
            if eid:
                superseded.add(eid)
            continue
        if r.get("op") == "relate":
            relations.append(r)
            continue
        e = r.get("entity")
        if not e or not e.get("id"):
            continue
        if e["id"] not in entities:
            order.append(e["id"])
        entities[e["id"]] = e

    return entities, superseded, order, relations, total, bad


def _rel_endpoints(rel):
    """Extract (source, target) from a relate op, tolerating naming variants."""
    src = rel.get("from") or rel.get("source") or rel.get("subject")
    dst = rel.get("to") or rel.get("target") or rel.get("object")
    if isinstance(src, dict):
        src = src.get("id")
    if isinstance(dst, dict):
        dst = dst.get("id")
    return src, dst


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


DB_PATH = WORKSPACE / "skills" / "memory-health" / "hybrid-search" / "agent_memory.db"


def entity_subject(entity: dict) -> str | None:
    """Map an ontology entity to the subject key the indexer writes for it.

    Must stay in lockstep with hybrid_search.index_jsonl_file: that code sets
    subject from the entity's own `id` (normalised), else from the source key.
    Here the entity is gone from the graph, so we reconstruct the same key from
    the entity dict captured during replay. Returns None when no id is usable.
    """
    if not isinstance(entity, dict):
        return None
    props = entity.get("properties") if isinstance(entity.get("properties"), dict) else {}
    raw = entity.get("id") or props.get("name")
    if not isinstance(raw, str) or not raw.strip():
        return None
    import re
    key = re.sub(r"[^\w]+", "_", raw.strip().lower()).strip("_")
    return key or None


def sync_db_superseded(dropped_ids) -> int | None:
    """v3.3 — mirror a graph compaction into the hot DB.

    For every entity id that just left graph.jsonl, mark its indexed facts as
    superseded. Without this, the DB keeps ACTIVE rows for entities that no
    longer exist in the reference nomenclature — ghosts that only surface months
    later (689 found on 2026-10-05, cleaned by migrate_ontology_subjects.py).

    Best-effort by design: returns the affected row count, or None if the DB is
    missing/locked/unavailable. A graph compaction that already succeeded must
    never be reported as failed because the DB could not be reached.
    """
    if not dropped_ids:
        return 0
    if not DB_PATH.exists():
        return None
    try:
        import sqlite3
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA foreign_keys=ON")
        ids = list(dropped_ids)
        placeholders = ",".join("?" for _ in ids)
        cur = conn.execute(
            f"UPDATE memories SET status='superseded', updated_at=? "
            f"WHERE subject IN ({placeholders}) AND status='active'",
            (datetime.now().isoformat(timespec="seconds"), *ids),
        )
        conn.commit()
        n = cur.rowcount
        conn.close()
        return n
    except Exception as e:  # best-effort: never abort a successful compaction
        print(f"  db sync   : SKIPPED ({e})")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-gain", type=float, default=5.0,
                    help="skip compaction if gain is below this percentage")
    args = ap.parse_args()

    if not GRAPH.exists():
        print(f"no graph at {GRAPH}")
        return 1

    entities, superseded, order, relations, total, bad = replay(GRAPH)
    active = [e for e in order if e not in superseded]
    active_set = set(active)

    # M3 — drop relations whose source or target is no longer an active entity.
    # Kept relations are re-emitted (they were previously discarded entirely,
    # which is how orphans silently accumulated).
    kept_rel, orphan_rel = [], []
    for rel in relations:
        src, dst = _rel_endpoints(rel)
        if src in active_set and dst in active_set:
            kept_rel.append(rel)
        else:
            orphan_rel.append((src, dst))

    lines_out = []
    for eid in active:
        lines_out.append(json.dumps({"op": "state", "entity": entities[eid]},
                                    ensure_ascii=False, sort_keys=True))
    for rel in kept_rel:
        lines_out.append(json.dumps(rel, ensure_ascii=False, sort_keys=True))
    payload = ("\n".join(lines_out) + "\n") if lines_out else ""

    size_before = GRAPH.stat().st_size
    size_after = len(payload.encode("utf-8"))
    gain = (size_before - size_after) / size_before * 100 if size_before else 0

    print(f"  lines     : {total} -> {len(active)}  ({total - len(active)} dropped)")
    print(f"  size      : {size_before:,} -> {size_after:,} o  (-{gain:.0f}%)")
    print(f"  entities  : {len(active)} active, {len(superseded)} superseded")
    print(f"  relations : {len(kept_rel)} kept, {len(orphan_rel)} orphan(s) dropped")
    if orphan_rel:
        for src, dst in orphan_rel[:5]:
            print(f"    ⤫ orphan: {src} -> {dst}")
    if bad:
        print(f"  WARNING   : {bad} unparsable line(s)")

    if args.dry_run:
        print("  (dry-run: nothing written)")
        return 0

    if gain < args.min_gain:
        print(f"  skip: gain {gain:.1f}% below threshold {args.min_gain}%")
        return 0

    # --- backup ---
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUP_DIR / f"graph.jsonl.pre-compact-{stamp}"
    shutil.copy2(GRAPH, backup)
    assert md5(backup) == md5(GRAPH), "backup checksum mismatch"

    # --- write temp + validate ---
    tmp = GRAPH.with_suffix(".jsonl.tmp")
    tmp.write_text(payload)
    new_entities, _, new_order, _, _, _ = replay(tmp)
    if sorted(new_order) != sorted(active):
        tmp.unlink()
        print("  ABORT: entity set mismatch after compaction")
        return 2
    if any(entities[k] != new_entities.get(k) for k in active):
        tmp.unlink()
        print("  ABORT: entity content mismatch after compaction")
        return 2

    # --- swap ---
    os.replace(tmp, GRAPH)
    print(f"  compacted. backup: {backup.name}")

    # --- v3.3: sync ontology -> hot DB (M4 causality link) ---
    # Compaction drops entities from the reference nomenclature; without this,
    # their indexed rows stay ACTIVE in agent_memory.db and become ghosts that
    # only surface as surprises months later (689 found on 2026-10-05). When an
    # entity leaves the graph, its facts must leave the active retrieval radius
    # in the SAME breath. Best-effort: a missing/locked DB must never abort a
    # graph compaction that already succeeded.
    #
    # The set to mirror is the DIFF between the pre-compaction live set and the
    # post-compaction one. Relying only on explicit `supersede` ops missed every
    # entity that simply vanishes because the compacted source no longer lists
    # it — which is exactly how the 689 ghosts were created.
    dropped_ids = (set(order) - set(active)) | set(superseded)
    # Re-map entity ids to the subject key the indexer actually writes.
    dropped_subjects = {entity_subject(entities[eid]) for eid in dropped_ids if eid in entities}
    dropped_subjects.discard(None)
    synced = sync_db_superseded(dropped_subjects)
    if synced is not None:
        print(f"  db sync   : {synced} fact(s) superseded for "
              f"{len(dropped_subjects)} dropped subject(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
