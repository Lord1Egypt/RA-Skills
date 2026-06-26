#!/usr/bin/env python3
"""
build_embeddings.py — Embedding Index Construction (M4)

Reads extracted/<url_hash>.json files and builds two numpy embedding indexes:

  chunks    — one vector per content chunk, for semantic search
  concepts  — one vector per unique concept, for concept lookup

Embeddings are generated with sentence-transformers (local, ~80MB download once).
Vectors are L2-normalized so cosine similarity = dot product.

Storage layout (in <input>/embeddings/):
  chunks.npy       float32 matrix (N_chunks × D)
  chunks.json      list of chunk metadata dicts
  concepts.npy     float32 matrix (N_concepts × D)
  concepts.json    list of concept metadata dicts
  meta.json        model name, dimensions, counts, created_at

No ChromaDB or other database — pure numpy, compatible with any Python version.

Usage:
    python scripts/build_embeddings.py --input ./output/strudel-cc-mcp
    python scripts/build_embeddings.py --input ./output/strudel-cc-mcp --force
    python scripts/build_embeddings.py --input ./output/strudel-cc-mcp --smoke-test
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency bootstrap
# ---------------------------------------------------------------------------

def _ensure_deps():
    deps = {"sentence_transformers": "sentence-transformers", "numpy": "numpy"}
    missing = [pkg for mod, pkg in deps.items() if not _import_ok(mod)]
    if missing:
        print(f"Installing: {', '.join(missing)}...")
        os.system(f"pip install {' '.join(missing)} --break-system-packages -q")

def _import_ok(mod):
    try:
        __import__(mod)
        return True
    except ImportError:
        return False

_ensure_deps()

import numpy as np
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalize(name: str) -> str:
    name = name.strip()
    name = re.sub(r'\(\s*\)$', '', name)
    name = name.lower()
    name = re.sub(r'[_\-]+', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name.rstrip('.,;:')


def _chunk_doc_text(chunk: dict) -> str:
    section = chunk.get("section", "").strip()
    text = chunk.get("text", "").strip()
    if section and not text.startswith(section):
        return f"{section}\n\n{text}"
    return text


def _concept_doc_text(name: str, description: str) -> str:
    return f"{name}: {description}" if description else name


def _tags_to_str(tags) -> str:
    if isinstance(tags, list):
        return ", ".join(str(t) for t in tags if t)
    return str(tags) if tags else ""


# ---------------------------------------------------------------------------
# Load extracted data
# ---------------------------------------------------------------------------

def load_extracted(extracted_dir: Path) -> tuple[list[dict], list[dict]]:
    """Return (chunks, concepts) from all non-dry-run extracted JSON files."""
    chunks: list[dict] = []
    concept_map: dict[str, dict] = {}
    skipped = 0

    for f in sorted(extracted_dir.glob("*.json")):
        data = json.loads(f.read_text())
        if data.get("model") == "dry-run":
            skipped += 1
            continue

        page_url = data.get("url", "")
        for chunk in data.get("chunks", []):
            chunk = dict(chunk)
            chunk["page_url"] = page_url
            chunks.append(chunk)

            for concept in chunk.get("concepts", []):
                name = concept.get("name", "").strip()
                if not name:
                    continue
                norm = _normalize(name)
                desc = concept.get("description", "")
                if norm not in concept_map:
                    concept_map[norm] = {
                        "norm_name": norm,
                        "name": name,
                        "description": desc,
                        "mention_count": 0,
                    }
                else:
                    if len(desc) > len(concept_map[norm]["description"]):
                        concept_map[norm]["description"] = desc
                concept_map[norm]["mention_count"] += 1

    if skipped:
        print(f"  Skipped {skipped} dry-run file(s). "
              "Run extract_concepts.py with a real API key first.")

    return chunks, list(concept_map.values())


# ---------------------------------------------------------------------------
# Embed + save
# ---------------------------------------------------------------------------

def _l2_normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.maximum(norms, 1e-8)


def build_index(
    input_dir: Path,
    embedding_model: str = "all-MiniLM-L6-v2",
    force: bool = False,
) -> dict:
    extracted_dir = input_dir / "extracted"
    emb_dir = input_dir / "embeddings"
    emb_dir.mkdir(parents=True, exist_ok=True)

    meta_path      = emb_dir / "meta.json"
    chunk_npy      = emb_dir / "chunks.npy"
    chunk_json     = emb_dir / "chunks.json"
    concept_npy    = emb_dir / "concepts.npy"
    concept_json   = emb_dir / "concepts.json"

    if not force and meta_path.exists():
        print("  Embeddings already built. Use --force to rebuild.")
        meta = json.loads(meta_path.read_text())
        return meta

    # Load data
    print("  Loading extracted pages...")
    chunks, concepts = load_extracted(extracted_dir)
    print(f"  → {len(chunks)} chunks, {len(concepts)} concepts")

    if not chunks:
        print("  Nothing to embed. Run extract_concepts.py with a real API key first.")
        return {"chunks_indexed": 0, "concepts_indexed": 0}

    # Load model
    print(f"  Loading embedding model '{embedding_model}'...")
    print(f"  (First run downloads ~80MB — cached after that)")
    model = SentenceTransformer(embedding_model)

    # --- Embed chunks ---
    print(f"  Embedding {len(chunks)} chunks...", end="", flush=True)
    chunk_texts = [_chunk_doc_text(c) for c in chunks]
    chunk_matrix = model.encode(
        chunk_texts,
        batch_size=64,
        show_progress_bar=False,
        convert_to_numpy=True,
    ).astype(np.float32)
    chunk_matrix = _l2_normalize(chunk_matrix)
    np.save(chunk_npy, chunk_matrix)

    # Slim metadata (no raw text in index — server loads from graph.json)
    chunk_meta = [
        {
            "id":         c.get("id", ""),
            "url":        c.get("url", ""),
            "page_title": c.get("page_title", ""),
            "section":    c.get("section", ""),
            "word_count": c.get("word_count", 0),
            "tags":       _tags_to_str(c.get("tags", [])),
            "has_code":   bool(c.get("code_examples") or c.get("code_examples_raw")),
        }
        for c in chunks
    ]
    chunk_json.write_text(json.dumps(chunk_meta, ensure_ascii=False))
    print(f" done ({chunk_matrix.shape})")

    # --- Embed concepts ---
    print(f"  Embedding {len(concepts)} concepts...", end="", flush=True)
    concept_texts = [_concept_doc_text(c["name"], c["description"]) for c in concepts]
    concept_matrix = model.encode(
        concept_texts,
        batch_size=64,
        show_progress_bar=False,
        convert_to_numpy=True,
    ).astype(np.float32)
    concept_matrix = _l2_normalize(concept_matrix)
    np.save(concept_npy, concept_matrix)

    concept_json.write_text(
        json.dumps(concepts, ensure_ascii=False)
    )
    print(f" done ({concept_matrix.shape})")

    # --- Save meta ---
    meta = {
        "model":            embedding_model,
        "dimensions":       int(chunk_matrix.shape[1]),
        "chunks_indexed":   len(chunks),
        "concepts_indexed": len(concepts),
        "created_at":       datetime.utcnow().isoformat() + "Z",
    }
    meta_path.write_text(json.dumps(meta, indent=2))

    return meta


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def _smoke_test(input_dir: Path, model_name: str):
    emb_dir   = input_dir / "embeddings"
    meta_path = emb_dir / "meta.json"

    if not meta_path.exists():
        print("  No embeddings found — run without --smoke-test first.")
        return

    model      = SentenceTransformer(model_name)
    chunk_mat  = np.load(emb_dir / "chunks.npy")
    chunk_idx  = json.loads((emb_dir / "chunks.json").read_text())
    concept_mat = np.load(emb_dir / "concepts.npy")
    concept_idx = json.loads((emb_dir / "concepts.json").read_text())

    def search(query, matrix, index, n=3):
        qv = model.encode([query], convert_to_numpy=True).astype(np.float32)
        qv = qv / np.maximum(np.linalg.norm(qv), 1e-8)
        scores = (matrix @ qv[0])
        top = np.argsort(scores)[::-1][:n]
        return [(index[i], float(scores[i])) for i in top]

    print("\n── Smoke test ──────────────────────────────────────────")

    query = "how do I play a note pattern?"
    print(f"Chunk search: '{query}'")
    for meta, score in search(query, chunk_mat, chunk_idx):
        print(f"  [{score:.3f}] {meta['page_title']} / {meta['section']}")

    query2 = "musical rhythm and timing"
    print(f"\nConcept search: '{query2}'")
    for meta, score in search(query2, concept_mat, concept_idx):
        print(f"  [{score:.3f}] {meta['name']}")

    print("────────────────────────────────────────────────────────\n")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _print_stats(stats: dict):
    print()
    print("━" * 62)
    print("  Embedding index built!")
    print(f"  Chunks indexed:   {stats.get('chunks_indexed', 0):>6}")
    print(f"  Concepts indexed: {stats.get('concepts_indexed', 0):>6}")
    print(f"  Dimensions:       {stats.get('dimensions', '?'):>6}")
    print(f"  Model:            {stats.get('model', '?')}")
    print("━" * 62)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build numpy embedding index from extracted concepts (M4)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, metavar="DIR",
                        help="MCP output dir (e.g. ./output/strudel-cc-mcp)")
    parser.add_argument("--model", default="all-MiniLM-L6-v2", metavar="MODEL",
                        help="Sentence-transformers model name (default: all-MiniLM-L6-v2)")
    parser.add_argument("--force", action="store_true",
                        help="Rebuild existing index")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Run test queries after building")
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Building embedding index")
    print(f"  Input:  {input_dir}")
    print(f"  Model:  {args.model}")
    print()

    stats = build_index(input_dir, embedding_model=args.model, force=args.force)
    _print_stats(stats)

    if args.smoke_test and stats.get("chunks_indexed", 0) > 0:
        _smoke_test(input_dir, args.model)


if __name__ == "__main__":
    main()
