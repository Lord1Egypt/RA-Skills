#!/usr/bin/env python3
"""
Memory Vector Wrapper - MetaClaw Integration
Version: 1.0.0 (2026-04-01)
- Generic MetaClaw Skill für ClawHub
- Hybrid Retrieval (semantic + FTS)
- JSON-Output für einfachen Parsing
- Session-basierte Consolidation

Nutzung:
    # Direkt aufrufen:
    python3 memory_vector_wrapper.py "query" --limit 5
    
    # Als Modul importieren:
    from memory_vector_wrapper import search_hybrid
    results = search_hybrid("query", limit=3)
"""

import os
# Workaround for OpenMP duplicate library error on macOS
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Pfade - WORKSPACE Environment Variable (default: ~/.openclaw/workspace)
WORKSPACE = Path(os.environ.get("WORKSPACE", str(Path.home() / ".openclaw" / "workspace")))
VENV_PATH = WORKSPACE / ".venv-metaclaw"
LANCEDB_DIR = WORKSPACE / ".lancedb"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
TABLE_NAME = "memory"


def check_venv() -> bool:
    """Prüft ob das Virtual Environment existiert."""
    return VENV_PATH.exists()


def check_db() -> bool:
    """Prüft ob die Datenbank initialisiert ist."""
    return LANCEDB_DIR.exists() and (LANCEDB_DIR / f"{TABLE_NAME}.lance").exists()


def search_vector(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Führt semantische Suche über LanceDB durch.
    
    Args:
        query: Suchbegriff oder Frage
        limit: Maximale Anzahl Ergebnisse
    
    Returns:
        Liste von Suchergebnissen mit Score
    """
    # Dependencies importieren (mit VEnv-Pfad)
    import glob
    venv_libs = list(VENV_PATH.glob("lib/python*"))
    if venv_libs:
        venv_site_packages = venv_libs[0] / "site-packages"
        if venv_site_packages.exists():
            sys.path.insert(0, str(venv_site_packages))
    
    try:
        import lancedb
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except ImportError as e:
        return [{"error": f"Dependencies nicht verfügbar: {e}"}]
    
    try:
        # DB öffnen
        db = lancedb.connect(str(LANCEDB_DIR))
        
        # list_tables() gibt ein ListTablesResponse Objekt zurück
        tables_response = db.list_tables()
        table_list = tables_response.tables if hasattr(tables_response, 'tables') else list(tables_response)
        
        if TABLE_NAME not in table_list:
            return [{"error": "Tabelle nicht gefunden. Bitte memory-vector-init.py ausführen."}]
        
        table = db.open_table(TABLE_NAME)
        
        # Model laden (cached)
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Query embedden
        query_embedding = model.encode(query).tolist()
        
        # Suche durchführen
        results = table.search(query_embedding).limit(limit).to_pandas()
        
        # Formatieren
        formatted = []
        for _, row in results.iterrows():
            item = {
                "id": row.get("id", "unknown"),
                "path": row.get("path", "unknown"),
                "snippet": row.get("content", "")[:500],
                "date": row.get("date", ""),
                "type": row.get("type", ""),
                "tags": list(row.get("tags", [])) if hasattr(row.get("tags", []), 'tolist') else row.get("tags", []),
                "score": float(row.get("_distance", 0)),
                "relevance": 1 - float(row.get("_distance", 0))
            }
            formatted.append(item)
        
        return formatted
    
    except Exception as e:
        return [{"error": f"Suche fehlgeschlagen: {e}"}]


def search_keyword(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fallback: Keyword-basierte Suche über Memory-Files.
    
    Args:
        query: Suchbegriff
        limit: Maximale Anzahl Ergebnisse
    
    Returns:
        Liste von Suchergebnissen (ohne semantischen Score)
    """
    import re
    
    results = []
    query_lower = query.lower()
    
    # Files durchsuchen
    files_to_search = []
    
    if MEMORY_FILE.exists():
        files_to_search.append(MEMORY_FILE)
    
    if MEMORY_DIR.exists():
        files_to_search.extend(sorted(MEMORY_DIR.glob("*.md")))
    
    for file_path in files_to_search:
        try:
            content = file_path.read_text(encoding="utf-8")
            content_lower = content.lower()
            
            # Score: Anzahl der Vorkommen
            count = content_lower.count(query_lower)
            
            if count > 0:
                # Snippet mit Kontext
                idx = content_lower.find(query_lower)
                start = max(0, idx - 100)
                end = min(len(content), idx + 400)
                snippet = content[start:end]
                
                results.append({
                    "id": str(file_path.relative_to(WORKSPACE)),
                    "path": str(file_path),
                    "snippet": snippet,
                    "date": file_path.stem if re.match(r"\d{4}-\d{2}-\d{2}", file_path.stem) else "",
                    "type": "daily" if "memory" in str(file_path.parent) else "main",
                    "tags": [],
                    "score": 0,
                    "count": count,
                    "method": "keyword"
                })
        
        except Exception as e:
            continue
    
    # Nach Count sortieren
    results.sort(key=lambda x: x.get("count", 0), reverse=True)
    
    return results[:limit]


def search_fts(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    LanceDB Full-Text Search (Keyword-Suche mit FTS).
    
    Args:
        query: Suchbegriff
        limit: Maximale Anzahl Ergebnisse
    
    Returns:
        Liste von Suchergebnissen mit FTS-Score
    """
    import glob
    venv_libs = list(VENV_PATH.glob("lib/python*"))
    if venv_libs:
        venv_site_packages = venv_libs[0] / "site-packages"
        if venv_site_packages.exists():
            sys.path.insert(0, str(venv_site_packages))
    
    try:
        import lancedb
        import numpy as np
    except ImportError as e:
        return [{"error": f"Dependencies nicht verfügbar: {e}"}]
    
    try:
        # DB öffnen
        db = lancedb.connect(str(LANCEDB_DIR))
        
        # Tables prüfen
        tables_response = db.list_tables()
        table_list = tables_response.tables if hasattr(tables_response, 'tables') else list(tables_response)
        
        if TABLE_NAME not in table_list:
            return [{"error": "Tabelle nicht gefunden. Bitte memory-vector-init.py ausführen."}]
        
        table = db.open_table(TABLE_NAME)
        
        # FTS Suche durchführen
        results = table.search(query, query_type="fts").limit(limit).to_pandas()
        
        # Formatieren
        formatted = []
        for _, row in results.iterrows():
            item = {
                "id": row.get("id", "unknown"),
                "path": row.get("path", "unknown"),
                "snippet": row.get("content", "")[:500],
                "date": row.get("date", ""),
                "type": row.get("type", ""),
                "tags": list(row.get("tags", [])) if hasattr(row.get("tags", []), 'tolist') else row.get("tags", []),
                "score": float(row.get("_score", 0)),
                "relevance": float(row.get("_score", 0)),
                "method": "fts"
            }
            formatted.append(item)
        
        return formatted
    
    except Exception as e:
        return [{"error": f"FTS Suche fehlgeschlagen: {e}"}]


def search_hybrid(query: str, limit: int = 5, semantic_weight: float = 0.6) -> List[Dict[str, Any]]:
    """
    Hybrid-Suche: Kombiniert semantische und FTS-Suche.
    
    Args:
        query: Suchbegriff oder Frage
        limit: Maximale Anzahl Ergebnisse
        semantic_weight: Gewichtung semantischer Score (0.0-1.0)
    
    Returns:
        Liste von Suchergebnissen mit kombiniertem Score
    """
    # Prüfe VEnv
    if not check_venv():
        return [{
            "error": "Virtual Environment nicht gefunden",
            "hint": "Bitte ausführen: python3 -m venv .venv-metaclaw && pip install lancedb sentence-transformers"
        }]
    
    # Prüfe DB
    if not check_db():
        return search_keyword(query, limit)
    
    # Semantische Suche
    semantic_results = search_vector(query, limit)
    if semantic_results and "error" in semantic_results[0]:
        print(f"⚠️  Vector-Suche fehlgeschlagen: {semantic_results[0]['error']}", file=sys.stderr)
        return search_keyword(query, limit)
    
    # FTS Suche
    fts_results = search_fts(query, limit)
    if fts_results and "error" in fts_results[0]:
        print(f"⚠️  FTS-Suche fehlgeschlagen: {fts_results[0]['error']}", file=sys.stderr)
        return search_keyword(query, limit)
    
    # Results deduplizieren und scores kombinieren
    combined = {}
    
    # Semantic results (score: 0.6 * relevance)
    for r in semantic_results:
        key = r.get("id", "")
        if key not in combined:
            combined[key] = {
                **r,
                "combined_score": 0.0,
                "method": "hybrid"
            }
        combined[key]["combined_score"] += semantic_weight * r.get("relevance", 0)
    
    # FTS results (score: 0.4 * score)
    for r in fts_results:
        key = r.get("id", "")
        if key not in combined:
            combined[key] = {
                **r,
                "combined_score": 0.0,
                "method": "hybrid"
            }
        combined[key]["combined_score"] += (1 - semantic_weight) * r.get("relevance", 0)
    
    # Sortieren nach combined_score
    result_list = list(combined.values())
    result_list.sort(key=lambda x: x.get("combined_score", 0), reverse=True)
    
    return result_list[:limit]


def main():
    """CLI Interface."""
    parser = argparse.ArgumentParser(
        description="Memory Vector Wrapper für MetaClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("query", help="Suchbegriff oder Frage")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Anzahl der Ergebnisse")
    parser.add_argument("--json", "-j", action="store_true", help="JSON-Output (Default)")
    parser.add_argument("--text", "-t", action="store_true", help="Text-Output")
    parser.add_argument("--mode", "-m", type=str, default="hybrid", 
                        choices=["semantic", "keyword", "hybrid", "fts"],
                        help="Suchmodus: semantic, keyword, fts, hybrid (default: hybrid)")
    
    args = parser.parse_args()
    
    # Suche durchführen basierend auf Modus
    if args.mode == "semantic":
        if not check_db():
            results = search_keyword(args.query, args.limit)
        else:
            results = search_vector(args.query, args.limit)
            for r in results:
                r["method"] = "semantic"
    elif args.mode == "keyword":
        results = search_keyword(args.query, args.limit)
    elif args.mode == "fts":
        if not check_db():
            results = search_keyword(args.query, args.limit)
        else:
            results = search_fts(args.query, args.limit)
    else:  # hybrid (default)
        results = search_hybrid(args.query, args.limit)
    
    # Output
    if args.text:
        print(f"\n🔍 Ergebnisse für: \"{args.query}\"")
        print(f"   Modus: {args.mode}\n")
        if results and "error" in results[0]:
            print(f"❌ {results[0]['error']}")
            if "hint" in results[0]:
                print(f"   💡 {results[0]['hint']}")
        else:
            for i, r in enumerate(results):
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"#{i+1} {r.get('id', 'unknown')}")
                print(f"📁 {r.get('path', '')}")
                print(f"📅 {r.get('date', '')} | 🏷️  {r.get('type', '')}")
                print(f"🔍 Score: {r.get('combined_score', r.get('score', 0)):.4f} | Methode: {r.get('method', '')}")
                print(f"\n💬 {r.get('snippet', '')[:200]}...")
        print()
    else:
        # JSON Output (Default)
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
