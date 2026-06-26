#!/usr/bin/env python3
from __future__ import annotations

from literag_common import build_parser, index_library, load_config, resolve_config_path


def main() -> None:
    parser = build_parser("Index all LiteRAG libraries")
    parser.add_argument("--limit-files", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--progress-every", type=int, default=25)
    args = parser.parse_args()

    config = load_config(resolve_config_path(args))
    print("mode: incremental")
    for library in config.libraries:
        print(f"== {library.id} ==")

        def on_progress(progress: dict) -> None:
            every = max(1, args.progress_every)
            current = progress["current"]
            total = progress["total"]
            if current == 1 or current == total or current % every == 0:
                print(
                    f"progress: {current}/{total} | changed={progress['changed']} | "
                    f"docs={progress['docs_reindexed']} chunks={progress['chunks_indexed']} embeddings={progress['embeddings_indexed']}"
                )

        stats = index_library(
            config,
            library,
            limit_files=args.limit_files,
            batch_size=args.batch_size,
            progress_callback=on_progress,
        )
        for key, value in stats.items():
            print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    main()
