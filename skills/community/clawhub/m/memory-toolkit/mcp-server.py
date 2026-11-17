#!/usr/bin/env python3
"""
mcp-server.py — Serveur MCP pour la mémoire maison (agent_memory.db).

Pourquoi ce fichier existe
--------------------------
Deux moteurs de mémoire tournent côte à côte, sans se parler :

  (A) le moteur natif OpenClaw (memory_search) : indexe des FICHIERS Markdown
      (MEMORY.md, USER.md, memory/*.md). Il sert la prose, les sessions.
  (B) la base maison memory-health (agent_memory.db) : 11 876 lignes dont
      ~10 400 d'ontology — un graphe typé, avec superseded_by, FTS5 + vec0 + RRF.

Le natif ne sait pas lire une DB SQLite tierce — et il ne DOIT pas : fondre un
graphe typé dans un index de prose, c'est perdre le typage. La bonne réponse
n'est pas la fusion, c'est le CÂBLAGE : exposer (B) comme outil de session,
à côté de (A). C'est ce que fait ce serveur.

Périmètre : LECTURE SEULE. Aucun outil n'écrit dans la base. Le pipeline
nightly garde le monopole de l'écriture.

Transport : stdio (même motif que skills/google-mcp/server.py).
Interpréteur : python3 SYSTÈME — le venv de la skill n'a pas `mcp`
(include-system-site-packages=false) mais a sqlite_vec ; le python système a
les deux (mcp 1.28.1 + sqlite_vec 0.1.9), vérifié le 13/10/2026.

Usage (déclaration openclaw.json) :
    "memory": {
      "command": "python3",
      "args": ["/home/ubuntu/.openclaw/workspace/skills/memory-health/mcp-server.py"]
    }
"""

import os
import sqlite3
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ─── Chemins ──────────────────────────────────────────────────────────────────
# On résout depuis l'emplacement de CE fichier : le serveur doit tourner que la
# skill soit à son chemin de dev ou au chemin installé.

HERE = Path(__file__).resolve().parent
HYBRID_DIR = HERE / "hybrid-search"
DB_PATH = HYBRID_DIR / "agent_memory.db"
SCHEMA_PATH = HYBRID_DIR / "schema.sql"

# Le moteur hybride vit dans hybrid-search/. On l'expose via sys.path plutôt
# que de dupliquer sa logique ici : une seule implémentation, une seule vérité.
if str(HYBRID_DIR) not in sys.path:
    sys.path.insert(0, str(HYBRID_DIR))

# CONTRAINTE CRITIQUE DU TRANSPORT STDIO : stdout est le canal JSON-RPC. Une
# seule ligne de texte parasite au milieu du protocole et le client croit
# recevoir du JSON malforme (observe le 13/10 : le moteur imprime un warning
# d'embedding des l'import). On redirige donc stdout vers stderr PENDANT
# l'import et pendant chaque appel moteur, puis on restaure.
import contextlib


@contextlib.contextmanager
def _stdout_to_stderr():
    """Tout ce que le moteur imprime part sur stderr, jamais dans le canal RPC."""
    saved = sys.stdout
    sys.stdout = sys.stderr
    try:
        yield
    finally:
        sys.stdout = saved


try:
    with _stdout_to_stderr():
        import hybrid_search as hs
except Exception as e:  # pragma: no cover - echec au demarrage, message explicite
    print(f"[memory-mcp] FATAL: import hybrid_search impossible: {e}", file=sys.stderr)
    raise

mcp = FastMCP("memory")

# Garde-fou : on REFUSE de servir une base absente plutôt que de renvoyer du vide
# silencieux. Un outil muet est plus dangereux qu'un outil qui se plaint.
if not DB_PATH.exists():
    print(f"[memory-mcp] FATAL: base introuvable: {DB_PATH}", file=sys.stderr)
    raise SystemExit(2)


# ─── Accès base ────────────────────────────────────────────────────────────────

def _conn_ro() -> sqlite3.Connection:
    """Connexion lecture seule, garantie par le moteur SQLite (pas par la discipline)."""
    c = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def _store() -> "hs.HybridMemoryStore":
    with _stdout_to_stderr():
        return hs.HybridMemoryStore(str(DB_PATH), str(SCHEMA_PATH))


# ─── Outils ────────────────────────────────────────────────────────────────────

@mcp.tool()
def memory_query(text: str, top: int = 5) -> str:
    """Recherche hybride (BM25 + vecteurs, fusion RRF) dans la mémoire maison.

    C'est la porte d'entrée principale : à utiliser pour tout fait de vie
    (santé, médicaments, colis, finances, décisions, projets) que le moteur
    natif ne contient pas.

    Args:
        text: la requête, en langage naturel.
        top: nombre de résultats (défaut 5, max 20).
    """
    top = max(1, min(int(top), 20))
    store = _store()
    try:
        with _stdout_to_stderr():
            results = store.search_hybrid(text, limit=top, min_rrf_score=0.015,
                                          temporal_boost=True)
    finally:
        store.close()

    if not results:
        return f"Aucun résultat dans la mémoire maison pour : {text!r}"

    lines = [f"# mémoire maison — {len(results)} résultat(s) pour {text!r}", ""]
    for i, r in enumerate(results, 1):
        src = r.get("source", "?")
        cat = r.get("category", "")
        rrf = r.get("rrf_score", 0.0)
        content = (r.get("content") or "").strip().replace("\n", " ")
        lines.append(f"[{i}] {src}  (cat={cat}, rrf={rrf:.6f})")
        lines.append(f"    {content[:600]}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def memory_facts(subject: str = "", limit: int = 20) -> str:
    """Liste les faits ACTIFS de la mémoire maison, filtrables par sujet.

    Utile pour « qu'est-ce que je sais sur X ? » — notamment les faits santé,
    les décisions et les suivis. Les lignes superseded sont exclues : on ne
    sert que l'état courant.

    Args:
        subject: filtre partiel sur le sujet (insensible à la casse). Vide = tous.
        limit: nombre maximum de faits (défaut 20, max 100).
    """
    limit = max(1, min(int(limit), 100))
    c = _conn_ro()
    try:
        if subject:
            rows = c.execute(
                "SELECT id, subject, content, category, source, updated_at "
                "FROM memories WHERE status='active' AND category!='ontology' "
                "AND subject LIKE ? ORDER BY id DESC LIMIT ?",
                (f"%{subject}%", limit),
            ).fetchall()
        else:
            rows = c.execute(
                "SELECT id, subject, content, category, source, updated_at "
                "FROM memories WHERE status='active' AND category!='ontology' "
                "ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
    finally:
        c.close()

    if not rows:
        return f"Aucun fait actif pour le filtre {subject!r}"

    head = f"# mémoire maison — {len(rows)} fait(s) actif(s)"
    if subject:
        head += f" · filtre {subject!r}"
    lines = [head, ""]
    for r in rows:
        subj = r["subject"] or "(sans sujet)"
        content = (r["content"] or "").strip().replace("\n", " ")
        lines.append(f"[{r['id']}] {subj}  (cat={r['category']})")
        lines.append(f"    {content[:400]}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def memory_stats() -> str:
    """État de la mémoire maison : volumétrie, statuts, catégories, fraîcheur.

    À appeler quand on veut savoir ce que la base contient VRAIMENT, plutôt
    que de le supposer. Lecture seule.
    """
    c = _conn_ro()
    try:
        total = c.execute("SELECT COUNT(*) n FROM memories").fetchone()["n"]
        status = c.execute(
            "SELECT COALESCE(status,'(null)') s, COUNT(*) n FROM memories "
            "GROUP BY s ORDER BY n DESC"
        ).fetchall()
        cats = c.execute(
            "SELECT COALESCE(category,'(null)') c, COUNT(*) n FROM memories "
            "GROUP BY c ORDER BY n DESC LIMIT 10"
        ).fetchall()
        fresh = c.execute("SELECT MAX(created_at) d FROM memories").fetchone()["d"]
        active_facts = c.execute(
            "SELECT COUNT(*) n FROM memories WHERE status='active' AND category!='ontology'"
        ).fetchone()["n"]
    finally:
        c.close()

    lines = [
        "# mémoire maison — état",
        f"base     : {DB_PATH}",
        f"total    : {total:,} lignes".replace(",", " "),
        f"faits actifs hors ontology : {active_facts:,}".replace(",", " "),
        f"dernier ajout : {fresh}",
        "",
        "## statuts",
    ]
    lines += [f"  {r['s']:12s} {r['n']:6d}" for r in status]
    lines += ["", "## catégories (top 10)"]
    lines += [f"  {str(r['c'])[:22]:24s} {r['n']:6d}" for r in cats]
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
