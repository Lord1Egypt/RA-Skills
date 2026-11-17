#!/usr/bin/env python3
"""
memory-dedup.py — Marque les doublons exacts comme `superseded`.

Pourquoi ce fichier existe
--------------------------
`memory-audit.py` MESURE les doublons (406 hors ontology, 6 033 dans
l'ontology). Il ne les corrige pas. Ce script est l'action, et il est
volontairement le plus étroit possible :

  - périmètre   : category NOT IN ('ontology')  -- le graphe n'est PAS touché
  - critère     : md5(content.strip())          -- identique au caractère près
  - survivant   : l'id le plus ANCIEN du groupe  -- on garde la première trace
  - action      : status='superseded'            -- JAMAIS de DELETE
  - garde-fou   : si le compte dépasse --max-rows, on n'écrit RIEN

Le dry-run est le défaut. `--apply` est requis pour écrire.

Usage :
    python3 memory-dedup.py                      # dry-run : liste tout
    python3 memory-dedup.py --limit 40           # dry-run : 40 premières paires
    python3 memory-dedup.py --json               # dry-run, sortie machine
    python3 memory-dedup.py --apply              # ECRIT (superseded)
    python3 memory-dedup.py --apply --max-rows 500
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace")).resolve()
DEFAULT_DB = WORKSPACE / "skills" / "memory-health" / "hybrid-search" / "agent_memory.db"

# Catégories EXCLUES du périmètre. L'ontology est un graphe : dédupliquer ses
# entrées est un chantier à part, avec sa propre sémantique. On n'y touche pas
# tant que ce point n'a pas été décidé explicitement.
EXCLUDED_CATEGORIES = ("ontology",)

# Garde-fou : un run qui vise plus de lignes que ce qu'on a annoncé signale une
# dérive du critère. On refuse d'écrire et on renvoie l'opérateur mesurer.
DEFAULT_MAX_ROWS = 600


def connect(db: Path, ro: bool) -> sqlite3.Connection:
    if not db.exists():
        raise FileNotFoundError(f"base introuvable : {db}")
    mode = "ro" if ro else "rw"
    conn = sqlite3.connect(f"file:{db}?mode={mode}", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def find_duplicates(conn, max_rows: int) -> dict:
    """Groupes de contenu identique hors ontology, parmi les lignes actives."""
    ph = ",".join("?" for _ in EXCLUDED_CATEGORIES)
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in conn.execute(
        f"SELECT id, content, category, source, status, created_at, length(content) l "
        f"FROM memories WHERE status='active' AND category NOT IN ({ph}) "
        f"ORDER BY id",
        EXCLUDED_CATEGORIES,
    ):
        h = hashlib.md5((r["content"] or "").strip().encode()).hexdigest()
        groups[h].append(dict(r))

    plan = []  # lignes a marquer superseded
    kept = []  # survivants
    for h, rows in groups.items():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda x: x["id"])
        kept.append(rows[0])
        for r in rows[1:]:
            plan.append({**r, "kept_id": rows[0]["id"], "md5": h})

    plan.sort(key=lambda x: x["id"])
    return {
        "pairs": len(plan),
        "groups": sum(1 for h, rows in groups.items() if len(rows) > 1),
        "kept": len(kept),
        "rows": plan,
        "excluded_categories": list(EXCLUDED_CATEGORIES),
        "over_max": len(plan) > max_rows,
        "max_rows": max_rows,
    }


def apply_superseded(conn, plan: list) -> int:
    """Marque les lignes comme superseded. Aucun DELETE, jamais."""
    if not plan:
        return 0
    conn.execute("BEGIN IMMEDIATE")
    try:
        n = 0
        for r in plan:
            cur = conn.execute(
                "UPDATE memories SET status='superseded', "
                "superseded_by=? WHERE id=? AND status='active'",
                (r["kept_id"], r["id"]),
            )
            n += cur.rowcount
        conn.execute("COMMIT")
        return n
    except Exception:
        conn.execute("ROLLBACK")
        raise


def render(rep: dict, show: int) -> str:
    L = []
    a = L.append
    a("=" * 62)
    a("  DÉDUPLICATION (hors ontology)")
    a("=" * 62)
    a(f"  groupes de doublons   : {rep['groups']}")
    a(f"  lignes à superseder   : {rep['pairs']}")
    a(f"  survivants conservés  : {rep['kept']}")
    a(f"  catégories exclues    : {', '.join(rep['excluded_categories'])}")
    a("")
    shown = rep["rows"][:show] if show else rep["rows"]
    for r in shown:
        excerpt = (r["content"] or "").replace("\n", " ")[:52]
        a(f"  [{r['id']:>6}] -> superseded (gardé [{r['kept_id']}])  "
          f"{str(r['category'])[:14]:16s} {excerpt!r}")
    if show and len(rep["rows"]) > show:
        a(f"  ... et {len(rep['rows']) - show} autre(s) ligne(s)")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Déduplication — dry-run par défaut")
    ap.add_argument("--apply", action="store_true", help="ECRIT status=superseded")
    ap.add_argument("--json", action="store_true", help="sortie machine")
    ap.add_argument("--db", type=str, default=None)
    ap.add_argument("--limit", type=int, default=25, help="lignes affichées (0 = tout)")
    ap.add_argument("--max-rows", type=int, default=DEFAULT_MAX_ROWS)
    args = ap.parse_args()

    db = Path(args.db).resolve() if args.db else DEFAULT_DB
    try:
        conn = connect(db, ro=not args.apply)
        rep = find_duplicates(conn, args.max_rows)

        if rep["over_max"]:
            print(f"!! {rep['pairs']} lignes visées > max_rows={rep['max_rows']} "
                  f"-> AUCUNE écriture. Relever --max-rows après vérification.",
                  file=sys.stderr)
            return 3

        if args.json:
            print(json.dumps({k: v for k, v in rep.items() if k != "rows"},
                             indent=2, ensure_ascii=False))
            print(json.dumps(rep["rows"], indent=2, ensure_ascii=False, default=str))
            return 0

        print(render(rep, args.limit))

        if args.apply:
            n = apply_superseded(conn, rep["rows"])
            print(f"\n  ✅ {n} ligne(s) marquée(s) superseded (aucun DELETE)")
            left = conn.execute(
                "SELECT COUNT(*) n FROM memories WHERE status='active' "
                "AND category NOT IN ('ontology')"
            ).fetchone()["n"]
            print(f"  lignes actives hors ontology après : {left}")
        else:
            print(f"\n  (dry-run — rien n'a été écrit. --apply pour exécuter)")
        return 0
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 2
    except sqlite3.Error as e:
        print(f"❌ SQLite : {e}", file=sys.stderr)
        return 2
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
