#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import fetch_url_source, slugify, timestamp_slug, write_text
from config import LibrarianSettings
from pipeline import LibrarianPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian librarian: ingest notes, search your vault, ask questions")
    parser.add_argument("--vault-path", help="Override OBSIDIAN_VAULT_PATH for this run")
    subparsers = parser.add_subparsers(dest="command")

    # --- ingest (default / legacy behaviour) ---
    ingest_parser = subparsers.add_parser("ingest", help="Save text or a URL into the vault")
    source_group = ingest_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--text", help="Raw text to ingest")
    source_group.add_argument("--text-file", help="Path to a text/markdown file to ingest")
    source_group.add_argument("--url", help="URL to fetch and ingest")
    source_group.add_argument("--inbox-file", help="Existing file already staged inside the vault inbox")
    ingest_parser.add_argument("--title", help="Optional title override for the final note")
    ingest_parser.add_argument("--keep-inbox", action="store_true", help="Keep the staged inbox file after processing")
    ingest_parser.add_argument("--print-json", action="store_true", help="Print a JSON manifest instead of plain text paths")

    # --- ask ---
    ask_parser = subparsers.add_parser("ask", help="Ask a question against your vault using RAG")
    ask_parser.add_argument("question", nargs="+", help="The question to ask")
    ask_parser.add_argument("--category", default=None, help="Filter results to a specific category")
    ask_parser.add_argument("--threshold", type=float, default=0.65, help="Minimum similarity threshold (default 0.65)")
    ask_parser.add_argument("--limit", type=int, default=5, help="Max chunks to retrieve (default 5)")
    ask_parser.add_argument("--print-json", action="store_true", help="Print JSON output instead of formatted text")

    # --- reindex ---
    reindex_parser = subparsers.add_parser("reindex", help="Re-embed and index the full vault into Supabase")
    reindex_parser.add_argument("--file", default=None, help="Re-index a single file instead of the full vault")

    return parser


def stage_manual_text(settings: LibrarianSettings, text: str, label: str) -> Path:
    settings.inbox_path.mkdir(parents=True, exist_ok=True)
    inbox_path = settings.inbox_path / f"{timestamp_slug(label)}.md"
    write_text(inbox_path, text.strip() + "\n")
    return inbox_path


def cmd_ingest(args: argparse.Namespace, settings: LibrarianSettings) -> None:
    settings.vault_path.mkdir(parents=True, exist_ok=True)
    settings.inbox_path.mkdir(parents=True, exist_ok=True)

    if not settings.gemini_api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

    if args.inbox_file:
        inbox_path = Path(args.inbox_file).expanduser().resolve()
    elif args.url:
        try:
            fetched_title, fetched_body = fetch_url_source(args.url)
        except Exception as exc:
            raise RuntimeError(f"OpenClaw librarian URL ingest failed for {args.url}: {exc}") from exc
        raw_text = (
            f"Source URL: {args.url}\n"
            f"Source Title: {fetched_title}\n\n"
            f"{fetched_body.strip()}\n"
        )
        inbox_path = stage_manual_text(settings, raw_text, fetched_title or "web-source")
    elif args.text_file:
        source_path = Path(args.text_file).expanduser().resolve()
        raw_text = source_path.read_text(encoding="utf-8")
        inbox_path = stage_manual_text(settings, raw_text, source_path.stem)
    else:
        label = args.title or "manual-paste"
        inbox_path = stage_manual_text(settings, args.text or "", label)

    pipeline = LibrarianPipeline(settings)
    processed = pipeline.process_file(inbox_path, keep_inbox=args.keep_inbox, title_override=args.title)

    manifest = {
        "vault_path": str(settings.vault_path),
        "inbox_file": str(processed.raw.file_path),
        "final_path": str(processed.final_path),
        "title": processed.synthesized.title,
        "category": processed.architected.category,
        "needs_review": bool(processed.architected.frontmatter.get("needs_review")),
        "source": processed.architected.frontmatter.get("source"),
        "tags": processed.architected.frontmatter.get("tags") or [],
    }

    if args.print_json:
        print(json.dumps(manifest, indent=2))
    else:
        print(processed.final_path.resolve())
        print(f"MEDIA: {processed.final_path.resolve()}")


def cmd_ask(args: argparse.Namespace, settings: LibrarianSettings) -> None:
    from rag_answer import ask, format_answer

    if not settings.gemini_api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

    question = " ".join(args.question)
    result = ask(
        settings,
        question,
        category_filter=args.category,
        threshold=args.threshold,
        limit=args.limit,
    )

    if args.print_json:
        print(json.dumps({
            "query": result.query,
            "answer": result.answer,
            "sources": [
                {
                    "file_path": s.file_path,
                    "chunk_index": s.chunk_index,
                    "similarity": s.similarity,
                    "title": s.metadata.get("title", ""),
                }
                for s in result.sources
            ],
        }, indent=2))
    else:
        print(format_answer(result))


def cmd_reindex(args: argparse.Namespace, settings: LibrarianSettings) -> None:
    from vault_embedder import reindex_file, reindex_full_vault

    if not settings.gemini_api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

    if args.file:
        file_path = Path(args.file).expanduser().resolve()
        count = reindex_file(settings, file_path)
        print(f"Re-indexed {count} chunks from {file_path}", file=sys.stderr)
    else:
        count = reindex_full_vault(settings)
        print(f"Full vault re-index complete: {count} chunks", file=sys.stderr)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    settings = LibrarianSettings.from_env()
    if args.vault_path:
        settings.obsidian_vault_path = args.vault_path

    if args.command == "ask":
        cmd_ask(args, settings)
    elif args.command == "reindex":
        cmd_reindex(args, settings)
    elif args.command == "ingest":
        cmd_ingest(args, settings)
    else:
        # Legacy fallback: if no subcommand, check for old-style flags
        # Re-parse with legacy parser for backwards compatibility
        legacy_args = _parse_legacy_args()
        if legacy_args:
            cmd_ingest(legacy_args, settings)
        else:
            parser.print_help()
            sys.exit(1)


def _parse_legacy_args() -> argparse.Namespace | None:
    parser = argparse.ArgumentParser()
    source_group = parser.add_mutually_exclusive_group(required=False)
    source_group.add_argument("--text", default=None)
    source_group.add_argument("--text-file", default=None)
    source_group.add_argument("--url", default=None)
    source_group.add_argument("--inbox-file", default=None)
    parser.add_argument("--vault-path", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--keep-inbox", action="store_true")
    parser.add_argument("--print-json", action="store_true")

    try:
        args = parser.parse_args()
    except SystemExit:
        return None

    if args.text or args.text_file or args.url or args.inbox_file:
        return args
    return None


if __name__ == "__main__":
    main()
