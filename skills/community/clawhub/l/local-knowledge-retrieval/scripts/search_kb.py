#!/usr/bin/env python3
"""
Search BM25 index for knowledge-base projects.

Usage:
    python search_kb.py <project_name> "<expanded_query>"
    
    <project_name>: project folder name under knowledge-base/
    <expanded_query>: space-separated keywords (already expanded by AI)

Output:
    JSON to stdout: [{"path": "...", "rel_path": "...", "score": 0.xx, "rank": 1}, ...]
    
    Returns up to top-K results (default: 10).
    Empty list if no matches.
    Error message to stderr if index not found.
"""

import sys
import json
import argparse
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
# Workspace root: prefer cwd, fall back to file-path heuristic
if (Path.cwd() / 'AGENTS.md').exists():
    WORKSPACE = Path.cwd()
else:
    WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent
KB_ROOT = WORKSPACE / "knowledge-base"
DEFAULT_TOP_K = 10

# ── Search ──────────────────────────────────────────────────────────

def search(project_name: str, query: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    """
    Search BM25 index for project, return ranked file list.
    
    Args:
        project_name: folder name under knowledge-base/
        query: space-separated expanded query terms
        top_k: max results to return
        
    Returns:
        List of dicts with path, rel_path, score, rank
    """
    import bm25s
    
    kb_dir = KB_ROOT / project_name
    index_dir = kb_dir / ".bm25_index"
    
    if not index_dir.exists():
        # Index missing — auto-rebuild (programmatic enforcement)
        import subprocess, sys
        build_script = str(Path(__file__).resolve().parent / "build_kb_index.py")
        print(f"  [.] BM25 index not found for '{project_name}', auto-rebuilding...", file=sys.stderr)
        result = subprocess.run(
            [sys.executable, build_script, "--project", project_name],
            capture_output=True, text=True, cwd=str(WORKSPACE)
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Auto-rebuild failed for project '{project_name}': {result.stderr}"
            )
        print(f"  [OK] Index rebuilt automatically.\n", file=sys.stderr)
        # Retry after rebuild — index should now exist
        if not index_dir.exists():
            raise FileNotFoundError(
                f"Index still missing after auto-rebuild for '{project_name}'."
            )
    
    # Load index
    retriever = bm25s.BM25.load(str(index_dir), load_corpus=False)
    
    # Load file mapping
    mapping_path = index_dir / "file_mapping.json"
    if not mapping_path.exists():
        raise FileNotFoundError(f"File mapping not found for project '{project_name}'")
    
    file_mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    
    # Tokenize query (AI has already expanded it, no further stemming needed) (AI has already expanded it, no further stemming needed)
    query_tokens = bm25s.tokenize([query], stopwords=None)
    
    # Search
    results, scores = retriever.retrieve(query_tokens, k=top_k)
    
    # Format results
    output = []
    for i in range(results.shape[1]):
        doc_idx = results[0, i]
        score = float(scores[0, i])
        
        if score <= 0 or doc_idx < 0:
            continue
        
        if doc_idx < len(file_mapping):
            file_info = file_mapping[doc_idx]
            rel_path = file_info.get("rel_path", "")
            
            output.append({
                "rank": i + 1,
                "score": round(score, 4),
                "path": file_info.get("path", ""),
                "rel_path": rel_path,
                "name": file_info.get("name", ""),
            })
    
    return output


def main():
    parser = argparse.ArgumentParser(description="Search BM25 knowledge-base index")
    parser.add_argument("project", help="Project name (folder under knowledge-base/)")
    parser.add_argument("query", help="Expanded search query (space-separated terms)")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="Max results (default: 10)")
    
    args = parser.parse_args()
    
    try:
        results = search(args.project, args.query, args.top_k)
        # Output JSON
        print(json.dumps(results, ensure_ascii=False, indent=2))
        
        if not results:
            print("  (no results found)", file=sys.stderr)
            
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}), ensure_ascii=False)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Search failed: {e}"}), ensure_ascii=False)
        sys.exit(1)


if __name__ == "__main__":
    main()

