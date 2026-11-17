#!/usr/bin/env python3
"""
memory-audit.py — État de la mémoire en une seule commande.

Pourquoi ce fichier existe
--------------------------
Le diagnostic de la base mémoire (doublons, orphelins, fragments, cohérence des
index) était produit à la main, en écrivant du Python jetable à chaque fois.
Ce n'est pas une connexion à la mémoire : c'est de l'enquête. Ce script rend ces
mesures reproductibles, lisibles par un humain et parsables par un agent.

READ-ONLY STRICT. Aucune écriture, aucun UPDATE, aucun DELETE. Il ouvre la base
en `mode=ro` (URI SQLite) pour que ce soit garanti par le moteur, pas par la
discipline de l'auteur.

Usage :
    python3 memory-audit.py                 # rapport humain
    python3 memory-audit.py --json          # rapport machine
    python3 memory-audit.py --db <path>     # base alternative (copie hors état)
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace")).resolve()
DEFAULT_DB = WORKSPACE / "skills" / "memory-health" / "hybrid-search" / "agent_memory.db"

# Un fait atomique tient tout seul. En dessous de ce seuil, c'est un fragment
# de phrase, pas une assertion — la maladie observée le 13/10/2026.
MIN_ATOMIC_LEN = 25

# Catégories épisodiques : leur source est un log daté, pas une note stable.
# Les compter comme "orphelines" serait un faux positif.
EPISODIC = {"daily-note", "archive"}


def connect_ro(db: Path) -> sqlite3.Connection:
    """Ouvre la base en lecture seule, garantie par le moteur SQLite."""
    if not db.exists():
        raise FileNotFoundError(f"base introuvable : {db}")
    uri = f"file:{db}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def q1(conn, sql, *args):
    return conn.execute(sql, args).fetchone()


def audit_status(conn) -> dict:
    out = {}
    for r in conn.execute("SELECT COALESCE(status,'(null)') s, COUNT(*) n FROM memories GROUP BY s ORDER BY n DESC"):
        out[r["s"]] = r["n"]
    return out


def audit_categories(conn) -> list:
    return [
        {"category": r["category"], "n": r["n"]}
        for r in conn.execute("SELECT COALESCE(category,'(null)') category, COUNT(*) n FROM memories GROUP BY category ORDER BY n DESC")
    ]


def audit_duplicates(conn) -> dict:
    """Doublons exacts (md5 du contenu trimé), séparés ontology / reste."""
    seen, dups = {}, []
    for r in conn.execute("SELECT id, content, category FROM memories WHERE status='active'"):
        h = hashlib.md5((r["content"] or "").strip().encode()).hexdigest()
        if h in seen:
            dups.append({"id": r["id"], "twin": seen[h], "category": r["category"]})
        else:
            seen[h] = r["id"]
    total_active = q1(conn, "SELECT COUNT(*) n FROM memories WHERE status='active'")["n"]
    ont = sum(1 for d in dups if d["category"] == "ontology")
    return {
        "total": len(dups),
        "ontology": ont,
        "other": len(dups) - ont,
        "active_total": total_active,
        "pct": round(100.0 * len(dups) / total_active, 1) if total_active else 0.0,
        "sample": dups[:6],
    }


def audit_orphans(conn) -> dict:
    """Lignes dont la source ne existe plus sur disque (hors catégories épisodiques)."""
    missing, present = Counter(), Counter()
    for r in conn.execute(
        "SELECT source, COUNT(*) n FROM memories WHERE category NOT IN ('ontology','daily-note','archive') GROUP BY source"
    ):
        s = r["source"] or ""
        if not s:
            missing["(source vide)"] += r["n"]
            continue
        p = Path(s) if s.startswith("/") else WORKSPACE / s
        (present if p.exists() else missing)[s[:70]] += r["n"]
    return {
        "present_lines": sum(present.values()),
        "present_sources": len(present),
        "missing_lines": sum(missing.values()),
        "missing_sources": len(missing),
        "top_missing": missing.most_common(8),
    }


def audit_fragments(conn) -> dict:
    """Contenus non atomiques (< MIN_ATOMIC_LEN), hors ontology."""
    rows = [
        {"id": r["id"], "len": r["l"], "category": r["category"], "status": r["status"], "content": r["content"]}
        for r in conn.execute(
            "SELECT id, length(content) l, content, category, status FROM memories "
            "WHERE length(content) < ? AND category != 'ontology' ORDER BY l",
            (MIN_ATOMIC_LEN,),
        )
    ]
    return {"min_atomic_len": MIN_ATOMIC_LEN, "count": len(rows), "rows": rows[:15],
            "active": sum(1 for r in rows if r["status"] == "active")}


def audit_index(conn) -> dict:
    mem = q1(conn, "SELECT COUNT(*) n FROM memories")["n"]
    fts = q1(conn, "SELECT COUNT(*) n FROM memories_fts")["n"]
    try:
        vec = q1(conn, "SELECT COUNT(*) n FROM memories_vec_rowids")["n"]
    except sqlite3.Error:
        vec = None
    novec = q1(
        conn, "SELECT COUNT(*) n FROM memories m LEFT JOIN memories_vec_rowids v ON v.rowid=m.id WHERE v.rowid IS NULL"
    )["n"]
    return {"memories": mem, "fts": fts, "vec": vec, "without_vector": novec,
            "fts_gap": mem - fts, "vec_gap": (mem - vec) if vec is not None else None}


def audit_ontology(conn) -> dict:
    total = q1(conn, "SELECT COUNT(*) n FROM memories WHERE category='ontology'")["n"]
    if not total:
        return {"total": 0}
    by_status = {r["s"]: r["n"] for r in conn.execute(
        "SELECT COALESCE(status,'(null)') s, COUNT(*) n FROM memories WHERE category='ontology' GROUP BY s")}
    repeated = [
        {"subject": r["subject"], "n": r["n"]}
        for r in conn.execute(
            "SELECT subject, COUNT(*) n FROM memories WHERE category='ontology' AND status='active' "
            "AND subject IS NOT NULL GROUP BY subject HAVING COUNT(*)>1 ORDER BY n DESC LIMIT 10")
    ]
    return {"total": total, "by_status": by_status, "repeated_subjects": repeated,
            "repeated_count": len(repeated)}


def audit_freshness(conn) -> dict:
    return {
        "last_created": q1(conn, "SELECT MAX(created_at) d FROM memories")["d"],
        "last_updated": q1(conn, "SELECT MAX(updated_at) d FROM memories")["d"],
        "by_month": [
            {"month": r["m"], "n": r["n"]}
            for r in conn.execute(
                "SELECT substr(created_at,1,7) m, COUNT(*) n FROM memories "
                "WHERE created_at IS NOT NULL GROUP BY m ORDER BY m DESC LIMIT 8")
        ],
    }


def build_report(db: Path) -> dict:
    conn = connect_ro(db)
    try:
        return {
            "db": str(db),
            "db_bytes": db.stat().st_size,
            "status": audit_status(conn),
            "categories": audit_categories(conn),
            "duplicates": audit_duplicates(conn),
            "orphans": audit_orphans(conn),
            "fragments": audit_fragments(conn),
            "index": audit_index(conn),
            "ontology": audit_ontology(conn),
            "freshness": audit_freshness(conn),
        }
    finally:
        conn.close()


def render_human(rep: dict) -> str:
    L = []
    a = L.append
    a("═" * 62)
    a("  🧠 AUDIT MÉMOIRE")
    a(f"  base : {rep['db']}")
    a(f"  taille : {rep['db_bytes'] / 1048576:.2f} Mo")
    a("═" * 62)

    a("\n▸ STATUT")
    for s, n in rep["status"].items():
        a(f"    {s:16s} {n:6d}")

    a("\n▸ CATÉGORIES (top 10)")
    for c in rep["categories"][:10]:
        a(f"    {str(c['category'])[:22]:24s} {c['n']:6d}")

    d = rep["duplicates"]
    a("\n▸ DOUBLONS EXACTS (actifs)")
    a(f"    total            {d['total']:6d}  ({d['pct']}% des {d['active_total']} actifs)")
    a(f"      dont ontology  {d['ontology']:6d}")
    a(f"      hors ontology  {d['other']:6d}   ← le gisement utile")
    for s in d["sample"]:
        a(f"      [{s['id']}] ~ [{s['twin']}]  {s['category']}")

    o = rep["orphans"]
    a("\n▸ ORPHELINS (source disparue du disque)")
    a(f"    présentes : {o['present_lines']:6d} lignes / {o['present_sources']} sources")
    a(f"    absentes  : {o['missing_lines']:6d} lignes / {o['missing_sources']} sources")
    for s, n in o["top_missing"][:5]:
        a(f"      {n:5d}  {s}")

    f = rep["fragments"]
    a(f"\n▸ FRAGMENTS NON ATOMIQUES (< {f['min_atomic_len']} car)")
    a(f"    total {f['count']}  ·  encore actifs : {f['active']}")
    for r in f["rows"][:8]:
        a(f"      [{r['id']}] len={r['len']:3d} {r['status']:10s} {r['content']!r}")

    i = rep["index"]
    a("\n▸ COHÉRENCE DES INDEX")
    a(f"    memories {i['memories']:6d}  ·  FTS {i['fts']:6d}  ·  vec {i['vec'] if i['vec'] is not None else 'N/A'}")
    a(f"    sans vecteur        {i['without_vector']:6d}")
    a(f"    écart FTS           {i['fts_gap']:6d}")

    g = rep["ontology"]
    if g.get("total"):
        a(f"\n▸ ONTOLOGY ({g['total']} lignes, {100.0 * g['total'] / i['memories']:.0f}% du volume)")
        for s, n in g["by_status"].items():
            a(f"    {s:16s} {n:6d}")
        if g["repeated_subjects"]:
            a(f"    sujets répétés (actifs) : {g['repeated_count']}")
            for s in g["repeated_subjects"][:6]:
                a(f"      {s['n']:5d} ×  {str(s['subject'])[:50]}")

    fr = rep["freshness"]
    a("\n▸ FRAÎCHEUR")
    a(f"    dernier ajout   {fr['last_created']}")
    a(f"    dernière maj    {fr['last_updated']}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Audit mémoire — READ-ONLY")
    ap.add_argument("--json", action="store_true", help="sortie machine")
    ap.add_argument("--db", type=str, default=None, help="base alternative")
    args = ap.parse_args()

    db = Path(args.db).resolve() if args.db else DEFAULT_DB
    try:
        rep = build_report(db)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 2
    except sqlite3.Error as e:
        print(f"❌ SQLite : {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(rep, indent=2, ensure_ascii=False, default=str))
    else:
        print(render_human(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
