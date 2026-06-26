#!/usr/bin/env python3
"""
Project Knowledge Graph — indexer + query CLI.

Indexes project artifacts (recaps, plans, project memory files, architecture docs, skills)
into a local FalkorDB graph. Query by concept across projects.

Usage:
    knowledge index                     # Scan and index all projects
    knowledge query "search terms"      # Query by concept
    knowledge query "terms" --project CI # Filter by project
    knowledge query "terms" --type skill # Filter by doc type
    knowledge stats                     # Show corpus stats
    knowledge doctor                    # Check connectivity and health
"""

import os
import sys
import json
import re
import hashlib
import argparse
import textwrap
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import Optional

# ── Config ──────────────────────────────────────────────────────────────

# Default to localhost. Warn if overridden to non-localhost.
FALKORDB_HOST = os.environ.get("KNOWLEDGE_FALKORDB_HOST", "localhost")
FALKORDB_PORT = int(os.environ.get("KNOWLEDGE_FALKORDB_PORT", "16379"))

if FALKORDB_HOST not in ("localhost", "127.0.0.1", "::1"):
    print(f"⚠️  KNOWLEDGE_FALKORDB_HOST is set to '{FALKORDB_HOST}' — not localhost!", file=sys.stderr)
    print(f"   This will send your project data to a REMOTE FalkorDB instance.", file=sys.stderr)
    print(f"   Set to 'localhost' or unset to keep data local.", file=sys.stderr)
    response = input("   Continue with remote host? [y/N] ").strip().lower()
    if response != "y":
        print("   Aborted.", file=sys.stderr)
        sys.exit(1)
GRAPH_NAME = "knowledge"

# Project roots — paths to scan
PROJECT_ROOTS = {
    "CI": os.path.expanduser("~/Projects/cruisingintelligence"),
    "Trip-Ledger": os.path.expanduser("~/Desktop/commissiontracker"),
    "TTESS": os.path.expanduser("~/Desktop/TTESS"),
    "Beacon": os.path.expanduser("~/Desktop/beacon"),
    "Beacon-v2": os.path.expanduser("~/Desktop/beacon-v2"),
    "Rider-Scout": os.path.expanduser("~/Desktop/riderscout-saas"),
    "Custom-Skills": os.path.expanduser("~/.hermes/skills"),
    "Hermes-Agent": os.path.expanduser("~/.hermes/hermes-agent"),
}

# Document types and their file globs within a project
DOC_TYPE_GLOBS = {
    "recap": ["docs/recaps/*.md", "docs/daily-recaps/*.md"],
    "plan": ["docs/plans/*.md", ".hermes/plans/*.md"],
    "claude": ["CLAUDE.md", ".claude/CLAUDE.md"],
    "architecture": [
        "docs/architecture/*.md",
        "docs/features/*.md",
        "docs/operations/*.md",
        "docs/pipeline/*.md",
        "TECHNICAL-DOCUMENTATION.md",
        "FUNCTIONAL-SPECIFICATIONS.md",
        "docs/technical-documentation.md",
        "docs/functional-specifications.md",
    ],
    "skill": [
        "SKILL.md",
        "skills/*/SKILL.md",
        "skills/*/*/SKILL.md",
        "*/SKILL.md",
        "*/*/SKILL.md",
    ],
}

# Directories to exclude from scanning (relative to project root)
EXCLUDE_DIRS = {"node_modules", ".next", "venv", ".venv", "__pycache__",
                ".git", "dist", "build", ".worktrees", ".hermes"}

# FalkorDB has a ~32KB string property limit; keep chunks reasonable
MAX_CHUNK_SIZE = 2000

# ── FalkorDB Connection ─────────────────────────────────────────────────

def get_falkordb():
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        # Test connection
        db.select_graph(GRAPH_NAME).query("RETURN 1")
        return db
    except Exception as e:
        print(f"❌ Cannot connect to FalkorDB at {FALKORDB_HOST}:{FALKORDB_PORT}", file=sys.stderr)
        print(f"   Error: {e}", file=sys.stderr)
        print(f"   Start the container:", file=sys.stderr)
        print(f"   docker run -d --restart=unless-stopped -p 127.0.0.1:{FALKORDB_PORT}:6379 -v knowledge-graph-data:/data --name knowledge-graph falkordb/falkordb:latest", file=sys.stderr)
        sys.exit(1)

def ensure_graph(db):
    """Ensure the knowledge graph exists, create index on Chunk.id."""
    g = db.select_graph(GRAPH_NAME)
    try:
        g.query("CREATE INDEX ON :Chunk(id)")
    except Exception:
        pass  # index may already exist
    try:
        g.query("CREATE INDEX ON :Chunk(project)")
    except Exception:
        pass
    return g

# ── Document Discovery ──────────────────────────────────────────────────

def find_documents(project_name: str, project_root: str) -> list[dict]:
    """Find all markdown documents in a project matching known doc types."""
    docs = []
    root = Path(project_root)
    if not root.exists():
        return docs

    for doc_type, globs in DOC_TYPE_GLOBS.items():
        for pattern in globs:
            for path in sorted(root.glob(pattern)):
                if path.is_file() and path.suffix == ".md":
                    # Determine the type more specifically for skills
                    final_type = doc_type
                    if "skills/" in str(path) or ".hermes/skills" in str(path):
                        final_type = "skill"
                    rel_path = path.relative_to(root) if root in path.parents else path
                    docs.append({
                        "path": str(path),
                        "rel_path": str(rel_path),
                        "project": project_name,
                        "type": final_type,
                        "mtime": path.stat().st_mtime,
                    })
    return docs

# ── Chunking ────────────────────────────────────────────────────────────

def chunk_document(content: str) -> list[dict]:
    """Split markdown content into chunks by heading-2 boundaries and paragraphs."""
    chunks = []
    lines = content.split("\n")
    current_heading = ""
    current_section_heading = ""
    current_buffer = []
    current_start_line = 1

    def flush_buffer():
        nonlocal current_buffer
        if current_buffer:
            text = "\n".join(current_buffer).strip()
            if text:
                chunks.append({
                    "text": text,
                    "heading": current_heading,
                    "section_heading": current_section_heading,
                    "start_line": current_start_line,
                })
            current_buffer = []

    for i, line in enumerate(lines, 1):
        # Heading 1 — top-level section
        if re.match(r"^# [^#]", line):
            flush_buffer()
            current_heading = re.sub(r"^#+\s*", "", line).strip()
            current_section_heading = ""
            current_start_line = i + 1
        # Heading 2 — subsection boundary
        elif re.match(r"^## [^#]", line):
            flush_buffer()
            current_section_heading = re.sub(r"^#+\s*", "", line).strip()
            current_start_line = i + 1
        else:
            current_buffer.append(line)

        # If buffer exceeds max size, flush at paragraph boundary
        if sum(len(l) for l in current_buffer) > MAX_CHUNK_SIZE and line.strip() == "":
            flush_buffer()
            current_start_line = i + 1

    flush_buffer()
    return chunks

def content_hash(text: str) -> str:
    """SHA256 hash of chunk content for change detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

# ── Indexing ────────────────────────────────────────────────────────────

def index_document(g, doc: dict):
    """Index a single document into FalkorDB. Uses MERGE for idempotency."""
    try:
        content = Path(doc["path"]).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠  Could not read {doc['rel_path']}: {e}")
        return 0, 0

    chunks = chunk_document(content)
    chunk_count = 0
    skip_count = 0

    for chunk in chunks:
        cid = content_hash(chunk["text"])
        # Build heading chain
        heading_chain = chunk["heading"]
        if chunk["section_heading"]:
            heading_chain += " / " + chunk["section_heading"]

        # MERGE on content_hash — if the text hasn't changed, skip
        merge_query = (
            "MERGE (c:Chunk {id: $cid}) "
            "ON CREATE SET "
            "  c.text = $text, "
            "  c.source_file = $source_file, "
            "  c.project = $project, "
            "  c.type = $type, "
            "  c.heading = $heading, "
            "  c.start_line = $start_line, "
            "  c.hash = $hash, "
            "  c.mtime = $mtime, "
            "  c.indexed_at = timestamp() "
            "ON MATCH SET "
            "  c.mtime = CASE WHEN c.hash <> $hash THEN $mtime ELSE c.mtime END, "
            "  c.text = CASE WHEN c.hash <> $hash THEN $text ELSE c.text END, "
            "  c.hash = CASE WHEN c.hash <> $hash THEN $hash ELSE c.hash END, "
            "  c.source_file = $source_file "
            "RETURN c.hash"
        )

        try:
            result = g.query(
                merge_query,
                params={
                    "cid": doc["project"] + "::" + doc["rel_path"] + "::" + str(chunk["start_line"]) + "::" + cid,
                    "text": chunk["text"],
                    "source_file": doc["rel_path"],
                    "project": doc["project"],
                    "type": doc["type"],
                    "heading": heading_chain,
                    "start_line": chunk["start_line"],
                    "hash": cid,
                    "mtime": doc["mtime"],
                }
            )
            # If hash matched, skip was returned — count as noop
            if result.result_set and result.result_set[0][0] == cid:
                chunk_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"  ⚠  MERGE failed for {doc['rel_path']}:{chunk['start_line']}: {e}")

    return chunk_count, skip_count

def index_all(dry_run: bool = False) -> dict:
    """Index all project documents."""
    db = get_falkordb()
    g = ensure_graph(db)

    total_chunks = 0
    total_skipped = 0
    total_docs = 0
    project_counts = {}

    for project_name in sorted(PROJECT_ROOTS.keys()):
        project_root = PROJECT_ROOTS[project_name]
        docs = find_documents(project_name, project_root)
        project_docs = 0
        project_chunks = 0

        if not docs:
            print(f"  {project_name}: no documents found at {project_root}")
            continue

        print(f"\n📁 {project_name} ({len(docs)} documents):")

        for doc in docs:
            if dry_run:
                try:
                    content = Path(doc["path"]).read_text(encoding="utf-8", errors="replace")
                    c = len(chunk_document(content))
                    print(f"    {doc['rel_path']}: ~{c} chunks")
                    project_chunks += c
                except Exception:
                    pass
                continue

            indexed, skipped = index_document(g, doc)
            project_chunks += indexed
            total_skipped += skipped
            project_docs += 1
            if indexed > 0:
                print(f"    ✓ {doc['rel_path']}: {indexed} chunks", end="")
                if skipped > 0:
                    print(f" ({skipped} unchanged)")
                else:
                    print()

        total_chunks += project_chunks
        total_docs += project_docs
        project_counts[project_name] = {"docs": project_docs, "chunks": project_chunks}

    return {
        "projects": len(PROJECT_ROOTS),
        "documents": total_docs,
        "chunks": total_chunks,
        "skipped": total_skipped,
        "project_counts": project_counts,
    }

# ── Querying ────────────────────────────────────────────────────────────

def tokenize(text: str) -> list[str]:
    """Extract significant tokens from text."""
    text = text.lower()
    # Remove markdown formatting
    text = re.sub(r"[#*`_~\[\]()>|-]", " ", text)
    # Split on non-alpha
    tokens = re.findall(r"[a-z][a-z0-9]{2,}", text)
    return tokens

def compute_tfidf(query_tokens: list[str], doc_tokens: list[str], doc_count: int, doc_freq: dict) -> float:
    """Simple TF-IDF score for a document given query terms."""
    if not query_tokens or not doc_tokens:
        return 0.0

    doc_counter = Counter(doc_tokens)
    score = 0.0
    for token in set(query_tokens):
        if token in doc_counter:
            tf = doc_counter[token] / len(doc_tokens)
            idf = max(0.1, (doc_count - doc_freq.get(token, 0) + 0.5) / (doc_freq.get(token, 0) + 0.5))
            score += tf * idf
    return score

def query_knowledge(search_term: str, project_filter: Optional[str] = None,
                    type_filter: Optional[str] = None, limit: int = 10) -> list[dict]:
    """Query the knowledge graph by concept using CONTAINS + TF-IDF ranking."""
    db = get_falkordb()
    g = db.select_graph(GRAPH_NAME)

    # Build Cypher query
    conditions = ['c.text CONTAINS $search']
    params = {"search": search_term}

    if project_filter:
        conditions.append("c.project = $project")
        params["project"] = project_filter
    if type_filter:
        conditions.append("c.type = $type")
        params["type"] = type_filter

    where_clause = " AND ".join(conditions)

    # Fetch candidates via CONTAINS
    cypher = (
        f"MATCH (c:Chunk) "
        f"WHERE {where_clause} "
        f"RETURN c.text, c.source_file, c.project, c.type, c.heading, c.id "
        f"LIMIT 200"
    )
    try:
        result = g.query(cypher, params=params)
    except Exception as e:
        print(f"❌ Query failed: {e}", file=sys.stderr)
        return []

    if not result.result_set:
        return []

    # Compute TF-IDF for ranking
    query_tokens = tokenize(search_term)
    doc_count = len(result.result_set)

    # Build doc frequency
    doc_freq = Counter()
    all_doc_tokens = []
    for row in result.result_set:
        tokens = tokenize(row[0])
        all_doc_tokens.append(tokens)
        for t in set(tokens):
            doc_freq[t] += 1

    scored = []
    for i, row in enumerate(result.result_set):
        text, source_file, project, doc_type, heading, chunk_id = row
        tfidf = compute_tfidf(query_tokens, all_doc_tokens[i], doc_count, doc_freq)

        # Extract first meaningful snippet (first ~300 chars, breaking at sentence)
        snippet = text[:300].strip()
        # Try to end at a sentence boundary
        sentence_end = max(snippet.rfind(". "), snippet.rfind("?\n"), snippet.rfind("!\n"))
        if sentence_end > 100:
            snippet = snippet[:sentence_end + 1]

        scored.append({
            "score": round(tfidf, 4),
            "project": project,
            "file": source_file,
            "type": doc_type,
            "heading": heading,
            "snippet": snippet,
            "id": chunk_id,
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]

# ── Stats ───────────────────────────────────────────────────────────────

def get_stats() -> dict:
    """Get corpus statistics from FalkorDB."""
    db = get_falkordb()
    g = db.select_graph(GRAPH_NAME)

    stats = {}
    try:
        total = g.query("MATCH (c:Chunk) RETURN count(c) as cnt")
        stats["total_chunks"] = total.result_set[0][0] if total.result_set else 0
    except Exception:
        stats["total_chunks"] = 0

    try:
        by_project = g.query(
            "MATCH (c:Chunk) RETURN c.project, count(c) as cnt ORDER BY cnt DESC"
        )
        stats["by_project"] = [(r[0], r[1]) for r in (by_project.result_set or [])]
    except Exception:
        stats["by_project"] = []

    try:
        by_type = g.query(
            "MATCH (c:Chunk) RETURN c.type, count(c) as cnt ORDER BY cnt DESC"
        )
        stats["by_type"] = [(r[0], r[1]) for r in (by_type.result_set or [])]
    except Exception:
        stats["by_type"] = []

    return stats

# ── Delete ───────────────────────────────────────────────────────────────

def delete_chunks(project=None, doc_type=None, all_chunks=False):
    """Delete chunks by project, type, or all."""
    db = get_falkordb()
    g = db.select_graph(GRAPH_NAME)
    if all_chunks:
        cypher = "MATCH (c:Chunk) DETACH DELETE c RETURN count(c) as cnt"
        params = {}
    else:
        conds, params = [], {}
        if project:
            conds.append("c.project = $project")
            params["project"] = project
        if doc_type:
            conds.append("c.type = $type")
            params["type"] = doc_type
        if not conds:
            print("Specify --project, --type, or --all")
            return 0
        cypher = "MATCH (c:Chunk) WHERE " + " AND ".join(conds) + " DETACH DELETE c RETURN count(c) as cnt"
    try:
        r = g.query(cypher, params=params)
        n = r.result_set[0][0] if r.result_set else 0
        label = "all" if all_chunks else " ".join(f"{k}={v}" for k, v in params.items())
        print(f"Deleted {n} chunks ({label})")
        return n
    except Exception as e:
        print(f"Delete failed: {e}")
        return 0

# ── Doctor ──────────────────────────────────────────────────────────────

def doctor():
    """Check environment and connectivity."""
    print("🔍 Knowledge Graph Doctor")
    print()

    # Check FalkorDB
    try:
        from falkordb import FalkorDB
        db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        info = db.select_graph(GRAPH_NAME).query("RETURN 1")
        print(f"✅ FalkorDB: connected at {FALKORDB_HOST}:{FALKORDB_PORT}")
    except ImportError:
        print("❌ FalkorDB Python package not installed")
        print("   Run: pip install falkordb")
    except Exception as e:
        print(f"❌ FalkorDB: {e}")
        print(f"   Start container: docker run -d --restart=always -p {FALKORDB_PORT}:6379 --name knowledge-graph falkordb/falkordb")
        return

    # Check project roots — use targeted globs, NOT rglob
    print()
    for name, root in PROJECT_ROOTS.items():
        p = Path(root)
        if p.exists():
            # Count only the doc-type files we actually index
            docs = find_documents(name, str(p))
            print(f"✅ {name}: {root} ({len(docs)} indexed documents)")
        else:
            print(f"⚠  {name}: {root} — not found")

    # Check stats
    print()
    stats = get_stats()
    print(f"📊 Corpus: {stats['total_chunks']} chunks indexed")
    if stats["by_project"]:
        for project, count in stats["by_project"]:
            print(f"   {project}: {count} chunks")

# ── CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Project Knowledge Graph — index and query project artifacts via FalkorDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              knowledge index                          # Index all projects
              knowledge query "FalkorDB replication"   # Search by concept
              knowledge query "batch writes" --project CI
              knowledge query "soft delete" --type skill
              knowledge stats                          # Show corpus stats
              knowledge doctor                         # Health check
        """),
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # index
    index_parser = subparsers.add_parser("index", help="Index all project documents")
    index_parser.add_argument("--dry-run", action="store_true", help="Preview without indexing")

    # query
    query_parser = subparsers.add_parser("query", help="Query the knowledge graph")
    query_parser.add_argument("terms", nargs="+", help="Search terms")
    query_parser.add_argument("--project", "-p", help="Filter by project name")
    query_parser.add_argument("--type", "-t", help="Filter by document type (recap, plan, skill, claude, architecture)")
    query_parser.add_argument("--limit", "-l", type=int, default=10, help="Max results (default: 10)")

    # stats
    subparsers.add_parser("stats", help="Show corpus statistics")

    # doctor
    subparsers.add_parser("doctor", help="Check environment and connectivity")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete chunks from the graph")
    delete_parser.add_argument("--project", "-p", help="Delete all chunks for a project")
    delete_parser.add_argument("--type", "-t", help="Delete all chunks of a type (recap, plan, skill, claude, architecture)")
    delete_parser.add_argument("--all", action="store_true", help="Delete ALL chunks")

    args = parser.parse_args()

    if args.command == "index":
        start = datetime.now()
        result = index_all(dry_run=args.dry_run)
        elapsed = (datetime.now() - start).total_seconds()
        if not args.dry_run:
            print(f"\n✅ Indexed {result['chunks']} chunks across {result['documents']} documents "
                  f"({result['projects']} projects) in {elapsed:.1f}s")
            if result['skipped'] > 0:
                print(f"   {result['skipped']} chunks unchanged (skipped)")

    elif args.command == "query":
        terms = " ".join(args.terms)
        results = query_knowledge(terms, project_filter=args.project,
                                  type_filter=getattr(args, "type", None), limit=args.limit)
        if not results:
            print("No results found.")
            return

        print(f"🔍 Results for \"{terms}\"")
        if args.project:
            print(f"   Project: {args.project}")
        if args.type:
            print(f"   Type: {args.type}")
        print()

        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['project']}] {r['file']}")
            print(f"   Type: {r['type']}  |  Heading: {r['heading']}  |  Score: {r['score']}")
            print(f"   {r['snippet']}")
            print()

    elif args.command == "stats":
        stats = get_stats()
        print(f"📊 Knowledge Graph Corpus")
        print(f"   Total chunks: {stats['total_chunks']}")
        print()
        print("   By project:")
        for project, count in stats["by_project"]:
            print(f"     {project}: {count}")
        print()
        print("   By type:")
        for dtype, count in stats["by_type"]:
            print(f"     {dtype}: {count}")

    elif args.command == "doctor":
        doctor()

    elif args.command == "delete":
        if not args.project and not args.type and not args.all:
            print("Specify --project, --type, or --all to delete chunks")
        else:
            delete_chunks(project=args.project, doc_type=getattr(args, "type", None),
                          all_chunks=args.all)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
