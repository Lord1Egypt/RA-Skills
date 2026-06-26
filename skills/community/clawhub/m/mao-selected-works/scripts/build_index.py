#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from common import (
    ROOT,
    chunk_paragraphs,
    embed_texts,
    infer_article_title,
    infer_article_number,
    int_to_chinese,
    infer_volume,
    infer_volume_number,
    load_config,
    normalize_aliases,
    parse_frontmatter,
    relative_to_root,
    split_paragraphs,
)


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode = WAL;

        DROP TABLE IF EXISTS documents;
        DROP TABLE IF EXISTS passages;
        DROP TABLE IF EXISTS passage_vectors;
        DROP TABLE IF EXISTS document_fts;
        DROP TABLE IF EXISTS passage_fts;

        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_path TEXT NOT NULL UNIQUE,
            volume TEXT,
            volume_no INTEGER,
            article_no INTEGER,
            article_title TEXT NOT NULL,
            aliases_json TEXT NOT NULL,
            date TEXT,
            content TEXT NOT NULL
        );

        CREATE TABLE passages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            passage_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );

        CREATE TABLE passage_vectors (
            passage_id INTEGER PRIMARY KEY,
            embedding_json TEXT NOT NULL,
            FOREIGN KEY(passage_id) REFERENCES passages(id)
        );

        CREATE VIRTUAL TABLE document_fts USING fts5(
            article_title,
            aliases,
            volume,
            content
        );

        CREATE VIRTUAL TABLE passage_fts USING fts5(
            article_title,
            volume,
            content
        );
        """
    )


def load_markdown_records(corpus_dir: Path) -> list[dict[str, str | list[str] | None]]:
    records: list[dict[str, str | list[str] | None]] = []
    for path in sorted(corpus_dir.glob("*.md")):
        if path.name in {"SUMMARY.md", "目录.md"}:
            continue
        raw = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(raw)
        article_title = infer_article_title(body, metadata, path.name)
        volume_no = infer_volume_number(metadata, path.name, body)
        volume = infer_volume(body, metadata)
        if volume_no:
            volume = f"第{int_to_chinese(volume_no)}卷"
        aliases = normalize_aliases(metadata)
        date = str(metadata["date"]).strip() if metadata.get("date") else None
        records.append(
            {
                "source_path": relative_to_root(path),
                "volume": volume,
                "volume_no": volume_no,
                "article_no": infer_article_number(metadata, path.name),
                "article_title": article_title,
                "aliases": aliases,
                "date": date,
                "content": body.strip(),
            }
        )
    return records


def index_records(conn: sqlite3.Connection, records: list[dict[str, str | list[str] | None]], config: dict) -> dict[str, int]:
    chunk_size = int(config.get("chunk_size", 900))
    chunk_overlap = int(config.get("chunk_overlap", 120))
    rag_cfg = config.get("rag", {})
    build_embeddings = bool(rag_cfg.get("enabled")) and bool(rag_cfg.get("build_embeddings_on_index"))

    doc_count = 0
    passage_count = 0

    for record in records:
        aliases_json = json.dumps(record["aliases"], ensure_ascii=False)
        cursor = conn.execute(
            """
            INSERT INTO documents (source_path, volume, volume_no, article_no, article_title, aliases_json, date, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["source_path"],
                record["volume"],
                record["volume_no"],
                record["article_no"],
                record["article_title"],
                aliases_json,
                record["date"],
                record["content"],
            ),
        )
        document_id = int(cursor.lastrowid)
        conn.execute(
            """
            INSERT INTO document_fts(rowid, article_title, aliases, volume, content)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                document_id,
                record["article_title"],
                " ".join(record["aliases"]),
                record["volume"] or "",
                record["content"],
            ),
        )

        paragraphs = split_paragraphs(str(record["content"]))
        chunks = chunk_paragraphs(paragraphs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        embeddings: list[list[float]] = []
        if build_embeddings and chunks:
            embeddings = embed_texts(chunks, config)

        for passage_index, chunk in enumerate(chunks, start=1):
            passage_cursor = conn.execute(
                """
                INSERT INTO passages (document_id, passage_index, content)
                VALUES (?, ?, ?)
                """,
                (document_id, passage_index, chunk),
            )
            passage_id = int(passage_cursor.lastrowid)
            conn.execute(
                """
                INSERT INTO passage_fts(rowid, article_title, volume, content)
                VALUES (?, ?, ?, ?)
                """,
                (
                    passage_id,
                    record["article_title"],
                    record["volume"] or "",
                    chunk,
                ),
            )
            if embeddings:
                conn.execute(
                    """
                    INSERT INTO passage_vectors (passage_id, embedding_json)
                    VALUES (?, ?)
                    """,
                    (passage_id, json.dumps(embeddings[passage_index - 1])),
                )
            passage_count += 1

        doc_count += 1

    return {"documents": doc_count, "passages": passage_count}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build SQLite indexes for Mao Selected Works corpus.")
    parser.add_argument(
        "--corpus-dir",
        default="",
        help="Directory containing Markdown corpus files. Defaults to data/, then falls back to corpus/markdown/.",
    )
    parser.add_argument(
        "--config",
        default=str(ROOT / "config" / "search.json"),
        help="Search configuration file. Falls back to config/search.example.json when missing.",
    )
    parser.add_argument(
        "--db",
        default="",
        help="Override database path. Defaults to config.database_path.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    candidate_dirs: list[Path] = []
    if args.corpus_dir:
        candidate_dirs.append(Path(args.corpus_dir).expanduser().resolve())
    candidate_dirs.extend([(ROOT / "data").resolve(), (ROOT / "corpus" / "markdown").resolve()])

    corpus_dir = next((path for path in candidate_dirs if path.exists() and any(path.glob("*.md"))), None)
    if corpus_dir is None:
        checked = ", ".join(path.as_posix() for path in candidate_dirs)
        raise SystemExit(f"No Markdown corpus directory found. Checked: {checked}")

    config = load_config(Path(args.config).expanduser().resolve())
    db_path = Path(args.db).expanduser().resolve() if args.db else (ROOT / config.get("database_path", "index/search.sqlite")).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    records = load_markdown_records(corpus_dir)
    if not records:
        raise SystemExit(f"No Markdown files found in {corpus_dir}")

    with sqlite3.connect(db_path) as conn:
        create_schema(conn)
        summary = index_records(conn, records, config)
        conn.commit()

    summary.update(
        {
            "database_path": db_path.as_posix(),
            "corpus_dir": corpus_dir.as_posix(),
            "rag_enabled": bool(config.get("rag", {}).get("enabled")),
            "embeddings_built": bool(config.get("rag", {}).get("enabled"))
            and bool(config.get("rag", {}).get("build_embeddings_on_index")),
        }
    )

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(
            f"Indexed {summary['documents']} documents and {summary['passages']} passages into {summary['database_path']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
