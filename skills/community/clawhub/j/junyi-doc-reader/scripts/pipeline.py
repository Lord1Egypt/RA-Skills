#!/usr/bin/env python3
"""pipeline.py - Main entry point for doc-reader (v5).

Orchestrates: pre-check → converter → chunker → enricher → assembler.
Manages state for crash recovery via state.json.
v5: Added feishu document source and date-based splitting for daily notes.

Usage:
  # Local file
  python3 scripts/pipeline.py <input_file> --output <output_dir> \
    [--mode archive-only|archive+index|archive+index+insights] \
    [--split-by year|topic|chapter|none]

  # Feishu document
  python3 scripts/pipeline.py --source feishu --doc-token XXX --account YYY \
    --output <output_dir> [--mode ...] [--split-by date] [--dry-run]
"""

import argparse
import hashlib
import json
import os
import sys
import time

# Resolve script directory for sibling imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import converter
import chunker
import enricher as enricher_mod
import assembler
import feishu_fetcher
import worklog_splitter


# Steps in order
STEPS = ["convert", "chunk", "enrich", "assemble"]

SUPPORTED_FORMATS = {".docx", ".pdf", ".txt", ".text", ".md", ".markdown"}


def compute_file_hash(path):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def generate_job_id():
    """Generate a job ID based on timestamp."""
    return time.strftime("%Y%m%d-%H%M%S")


def load_state(output_dir):
    """Load state.json if it exists."""
    state_path = os.path.join(output_dir, "state.json")
    if os.path.exists(state_path):
        with open(state_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_state(output_dir, state):
    """Persist state to state.json."""
    state_path = os.path.join(output_dir, "state.json")
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def detect_mode(requested_mode, source="local"):
    """Auto-select mode based on env vars, requested mode, and source type."""
    api_key = os.environ.get("DOC_READER_API_KEY", "")
    allow_external = os.environ.get("DOC_READER_ALLOW_EXTERNAL", "false").lower()

    if requested_mode == "archive+index+insights":
        if not api_key:
            print("[pipeline] WARNING: No DOC_READER_API_KEY set. Downgrading to archive+index.")
            return "archive+index"
        if allow_external == "false":
            print("[pipeline] WARNING: DOC_READER_ALLOW_EXTERNAL=false. Downgrading to archive+index.")
            print("  Set DOC_READER_ALLOW_EXTERNAL=true to enable LLM enrichment.")
            return "archive+index"
        # Feishu source requires explicit ALLOW_EXTERNAL for insights
        if source == "feishu" and allow_external != "true":
            print("[pipeline] WARNING: Feishu source requires DOC_READER_ALLOW_EXTERNAL=true for insights mode.")
            print("  Downgrading to archive+index.")
            return "archive+index"
        return "archive+index+insights"

    if requested_mode:
        return requested_mode

    # Auto-detect
    if api_key and allow_external == "true":
        return "archive+index+insights"
    elif api_key:
        return "archive+index"
    else:
        return "archive-only"


def pre_check(input_path):
    """Validate input file and gather metadata."""
    if not os.path.exists(input_path):
        print(f"ERROR: File not found: {input_path}")
        sys.exit(1)

    ext = os.path.splitext(input_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"ERROR: Unsupported format '{ext}'.")
        print(f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}")
        sys.exit(1)

    file_size = os.path.getsize(input_path)
    if file_size == 0:
        print("WARNING: Input file is empty (0 bytes)")

    # Estimate page count (rough: 2500 chars/page for text, or file size based)
    est_pages = max(1, file_size // 2500) if ext in (".txt", ".md", ".markdown") else max(1, file_size // 5000)

    print(f"[pipeline] Input: {os.path.basename(input_path)}")
    print(f"[pipeline] Format: {ext}, Size: {file_size:,} bytes, Est. pages: ~{est_pages}")

    return {
        "format": ext,
        "file_size": file_size,
        "est_pages": est_pages,
    }


def run_feishu_pipeline(doc_token, account, output_dir, mode, split_by, dry_run=False):
    """Run the feishu document pipeline (v5)."""
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Fetch and normalize
    print("=" * 50)
    print("STEP 1: Fetching from Feishu")
    print("=" * 50)
    md_path, source_meta = feishu_fetcher.fetch_and_normalize(doc_token, account, output_dir)
    print(f"[pipeline] Fetched: {source_meta['title']} ({source_meta['chars']:,} chars)")
    print()

    # Step 2: Route based on split_by
    if split_by == "date":
        # Daily notes branch
        print("=" * 50)
        print("STEP 2: Splitting by date (daily notes)")
        print("=" * 50)
        result = worklog_splitter.split_and_write(md_path, output_dir, dry_run)

        if result.get("fallback_reason"):
            print(f"[pipeline] Date split failed: {result['fallback_reason']}")
            print("[pipeline] Falling back to standard pipeline...")
            split_by = "none"
            # Fall through to standard pipeline below
        else:
            # Daily notes branch complete
            print(f"[pipeline] Split into {result['sections']} daily notes")
            if result.get("unmatched_blocks"):
                print(f"[pipeline] {result['unmatched_blocks']} unmatched blocks")

            # Generate manifest
            manifest = {
                "job_id": time.strftime("%Y%m%d-%H%M%S"),
                "source_type": "feishu",
                "source_path": f"feishu://{doc_token}",
                "source_hash": source_meta["content_hash"],
                "mode": mode,
                "split_by": "date",
                "converter": "feishu_fetcher",
                "chunk_count": result["sections"],
                "status": "completed_with_warnings" if result.get("unmatched_blocks") else "completed",
                "warnings": [f"{result['unmatched_blocks']} unmatched blocks"] if result.get("unmatched_blocks") else [],
                "outputs": result.get("files", []),
            }
            manifest_path = os.path.join(output_dir, "manifest.json")
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)

            print()
            print("=" * 50)
            print("COMPLETE (daily notes)")
            print("=" * 50)
            print(f"Daily notes: {result['sections']}")
            print(f"Confidence:  {result['confidence']:.2f}")
            print(f"Output:      {output_dir}")
            if result.get("index_file"):
                print(f"Index:       {result['index_file']}")
            return manifest

    # Standard pipeline branch (also used as fallback from date split)
    print("=" * 50)
    print("STEP 2: Chunking")
    print("=" * 50)
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunker.chunk_text(text)
    chunks_path = os.path.join(output_dir, "chunks.jsonl")
    with open(chunks_path, "w", encoding="utf-8") as f:
        for ch in chunks:
            f.write(json.dumps(ch, ensure_ascii=False) + "\n")
    print(f"[pipeline] {len(chunks)} chunks generated")
    print()

    # Step 3: Enrich (optional)
    enriched_path = os.path.join(output_dir, "enriched_chunks.jsonl")
    if mode == "archive+index+insights":
        print("=" * 50)
        print("STEP 3: LLM Enrichment")
        print("=" * 50)
        try:
            failed = enricher_mod.enrich(chunks_path, enriched_path)
        except Exception as e:
            print(f"[pipeline] Enrichment error: {e}. Continuing without.")
            mode = "archive+index"
    else:
        print(f"STEP 3: Enrichment skipped (mode: {mode})")
    print()

    # Step 4: Assemble
    print("=" * 50)
    print("STEP 4: Assembling output")
    print("=" * 50)
    final_chunks_path = enriched_path if os.path.exists(enriched_path) else chunks_path
    outputs = assembler.assemble(final_chunks_path, output_dir, "none", mode=mode)

    # Generate manifest
    manifest = {
        "job_id": time.strftime("%Y%m%d-%H%M%S"),
        "source_type": "feishu",
        "source_path": f"feishu://{doc_token}",
        "source_hash": source_meta["content_hash"],
        "mode": mode,
        "split_by": split_by,
        "converter": "feishu_fetcher",
        "chunk_count": len(chunks),
        "status": "completed",
        "warnings": [],
        "outputs": outputs,
    }
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 50)
    print("COMPLETE")
    print("=" * 50)
    print(f"Mode:    {mode}")
    print(f"Chunks:  {len(chunks)}")
    print(f"Output:  {output_dir}")
    return manifest


def run_pipeline(input_path, output_dir, mode, split_by):
    """Run the full local-file pipeline with state management."""
    os.makedirs(output_dir, exist_ok=True)

    # Pre-check
    meta = pre_check(input_path)
    source_hash = compute_file_hash(input_path)

    # Check for existing state (resume support)
    state = load_state(output_dir)
    if state and state.get("source_hash") == source_hash:
        print(f"[pipeline] Resuming job {state['job_id']} from step: {state.get('last_completed', 'none')}")
    else:
        if state:
            print("[pipeline] Source file changed, starting fresh")
        state = {
            "job_id": generate_job_id(),
            "source_path": os.path.abspath(input_path),
            "source_hash": source_hash,
            "mode": mode,
            "split_by": split_by,
            "last_completed": None,
            "warnings": [],
            "failed_chunks": [],
            "status": "running",
        }
        save_state(output_dir, state)

    print(f"[pipeline] Job: {state['job_id']}, Mode: {mode}")
    print()

    # Define file paths
    md_path = os.path.join(output_dir, "converted.md")
    chunks_path = os.path.join(output_dir, "chunks.jsonl")
    enriched_path = os.path.join(output_dir, "enriched_chunks.jsonl")

    last_done = state.get("last_completed")
    steps_done = STEPS[:STEPS.index(last_done) + 1] if last_done and last_done in STEPS else []

    # Step 1: Convert
    if "convert" not in steps_done:
        print("=" * 50)
        print("STEP 1/4: Converting to Markdown")
        print("=" * 50)
        warnings = converter.convert(input_path, md_path)
        state["warnings"].extend(warnings)
        state["last_completed"] = "convert"
        save_state(output_dir, state)
        print()

    # Step 2: Chunk
    if "chunk" not in steps_done:
        print("=" * 50)
        print("STEP 2/4: Splitting into chunks")
        print("=" * 50)
        with open(md_path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunker.chunk_text(text)
        with open(chunks_path, "w", encoding="utf-8") as f:
            for ch in chunks:
                f.write(json.dumps(ch, ensure_ascii=False) + "\n")
        print(f"[pipeline] {len(chunks)} chunks generated")
        state["chunk_count"] = len(chunks)
        state["last_completed"] = "chunk"
        save_state(output_dir, state)
        print()

    # Step 3: Enrich (only in insights mode)
    if "enrich" not in steps_done:
        if mode == "archive+index+insights":
            print("=" * 50)
            print("STEP 3/4: LLM Enrichment")
            print("=" * 50)
            try:
                failed = enricher_mod.enrich(chunks_path, enriched_path)
                state["failed_chunks"] = failed
            except SystemExit:
                print("[pipeline] Enrichment failed. Continuing without enrichment.")
                state["warnings"].append("Enrichment failed, downgraded to archive+index")
                mode = "archive+index"
                state["mode"] = mode
            except Exception as e:
                print(f"[pipeline] Enrichment error: {e}. Continuing without enrichment.")
                state["warnings"].append(f"Enrichment error: {e}")
                mode = "archive+index"
                state["mode"] = mode
        else:
            print("STEP 3/4: Enrichment skipped (mode: {})".format(mode))

        state["last_completed"] = "enrich"
        save_state(output_dir, state)
        print()

    # Step 4: Assemble
    if "assemble" not in steps_done:
        print("=" * 50)
        print("STEP 4/4: Assembling output")
        print("=" * 50)

        # Use enriched chunks if available, else plain chunks
        final_chunks_path = enriched_path if os.path.exists(enriched_path) else chunks_path

        outputs = assembler.assemble(
            final_chunks_path, output_dir, split_by,
            warnings=state.get("warnings"),
            failed_chunks=state.get("failed_chunks"),
            mode=mode,
        )

        state["last_completed"] = "assemble"
        state["outputs"] = outputs
        save_state(output_dir, state)
        print()

    # Generate manifest.json
    manifest = {
        "job_id": state["job_id"],
        "source_path": state["source_path"],
        "source_hash": state["source_hash"],
        "mode": mode,
        "converter": "pandoc" if meta["format"] == ".docx" else ("pdftotext" if meta["format"] == ".pdf" else "direct"),
        "chunk_count": state.get("chunk_count", 0),
        "status": "completed_with_warnings" if state.get("warnings") or state.get("failed_chunks") else "completed",
        "warnings": state.get("warnings", []),
        "outputs": state.get("outputs", []),
    }

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    state["status"] = manifest["status"]
    save_state(output_dir, state)

    # Clean up intermediate file
    if os.path.exists(md_path):
        pass  # Keep converted.md for debugging; user can delete

    # Summary
    print("=" * 50)
    print("COMPLETE")
    print("=" * 50)
    print(f"Job ID:    {state['job_id']}")
    print(f"Mode:      {mode}")
    print(f"Chunks:    {state.get('chunk_count', '?')}")
    print(f"Status:    {manifest['status']}")
    print(f"Output:    {output_dir}")
    if manifest["warnings"]:
        print(f"Warnings:  {len(manifest['warnings'])}")
    print(f"\nFiles generated:")
    for f_name in state.get("outputs", []):
        print(f"  - {f_name}")
    print(f"  - manifest.json")
    print(f"  - chunks.jsonl")

    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="doc-reader pipeline (v5): convert, chunk, enrich, and assemble documents. Supports local files and Feishu cloud documents.",
    )
    parser.add_argument("input_file", nargs="?", default=None, help="Path to input document (required for local source)")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument(
        "--source",
        choices=["local", "feishu"],
        default="local",
        help="Document source (default: local)",
    )
    parser.add_argument("--doc-token", default=None, help="Feishu document token (required for feishu source)")
    parser.add_argument("--account", default=None, help="Feishu account name (required for feishu source)")
    parser.add_argument(
        "--mode", "-m",
        choices=["archive-only", "archive+index", "archive+index+insights"],
        default=None,
        help="Processing mode (auto-detected if not specified)",
    )
    parser.add_argument(
        "--split-by",
        choices=["year", "topic", "chapter", "date", "none"],
        default="none",
        help="Split output into parts by this dimension",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing (date split only)")
    parser.add_argument("--title", default=None, help="Document title (optional, auto-detected for feishu)")

    args = parser.parse_args()

    # Parameter validation
    if args.source == "feishu":
        if not args.doc_token:
            parser.error("--doc-token is required when --source=feishu")
        if not args.account:
            parser.error("--account is required when --source=feishu")
        if args.input_file:
            parser.error("input_file conflicts with --source=feishu (use --doc-token instead)")
    else:
        if not args.input_file:
            parser.error("input_file is required for local source")
        if args.doc_token:
            parser.error("--doc-token conflicts with local source")
        if args.split_by == "date":
            parser.error("--split-by date is only supported with --source=feishu")

    mode = detect_mode(args.mode, args.source)

    if args.source == "feishu":
        run_feishu_pipeline(args.doc_token, args.account, args.output, mode, args.split_by, args.dry_run)
    else:
        run_pipeline(args.input_file, args.output, mode, args.split_by)


if __name__ == "__main__":
    main()
