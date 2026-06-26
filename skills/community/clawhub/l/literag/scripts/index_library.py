#!/usr/bin/env python3
from __future__ import annotations

from literag_common import build_parser, find_library, index_library, load_config, resolve_config_path


def main() -> None:
    parser = build_parser("Index one LiteRAG library")
    parser.add_argument("library")
    parser.add_argument("--limit-files", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=16, help="Chunk/DB work batch size")
    parser.add_argument("--embedding-batch-size", type=int, default=None, help="Embedding request batch size; defaults to config.embedding.batchSize")
    parser.add_argument("--progress-every", type=int, default=25)
    args = parser.parse_args()

    config = load_config(resolve_config_path(args))
    library = find_library(config, args.library)

    print(f"library: {library.id}")
    print("mode: incremental")

    def on_progress(progress: dict) -> None:
        every = max(1, args.progress_every)
        current = progress["current"]
        total = progress["total"]
        if current == 1 or current == total or current % every == 0:
            print(
                f"progress: {current}/{total} | changed={progress['changed']} | "
                f"docs={progress['docs_reindexed']} chunks={progress['chunks_indexed']} "
                f"embeddings_committed={progress['embeddings_indexed']} "
                f"buffered={progress.get('embeddings_buffered', 0)} "
                f"inflight={progress.get('embeddings_inflight', 0)} "
                f"outstanding={progress.get('embeddings_outstanding', 0)} "
                f"batches_inflight={progress.get('embedding_batches_inflight', 0)}"
            )

    stats = index_library(
        config,
        library,
        limit_files=args.limit_files,
        batch_size=args.batch_size,
        embedding_batch_size=args.embedding_batch_size,
        progress_callback=on_progress,
    )
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
