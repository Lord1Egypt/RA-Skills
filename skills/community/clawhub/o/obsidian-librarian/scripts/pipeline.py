#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from architect import MetadataArchitect
from config import LibrarianSettings
from file_manager import VaultFileManager
from models import ProcessedNote, RawInboxItem
from synthesizer import ContentSynthesizer
from vault_index import VaultIndex


class LibrarianPipeline:
    def __init__(self, settings: LibrarianSettings) -> None:
        self.settings = settings
        self.vault_index = VaultIndex(settings.vault_path, settings.inbox_folder).build()
        self.synthesizer = ContentSynthesizer(settings)
        self.architect = MetadataArchitect(settings, self.vault_index)
        self.file_manager = VaultFileManager(settings)

    def process_file(self, file_path: Path, *, keep_inbox: bool = False, title_override: str | None = None) -> ProcessedNote:
        raw = RawInboxItem(
            file_path=file_path,
            raw_content=file_path.read_text(encoding="utf-8"),
            detected_at=datetime.now(timezone.utc),
        )
        synthesized = self.synthesizer.synthesize(raw)
        if title_override:
            synthesized.title = title_override.strip()
            synthesized.markdown_body = self._override_h1(synthesized.markdown_body, synthesized.title)

        architected = self.architect.architect(synthesized, raw.raw_content)
        final_path = self.file_manager.write_note(architected, synthesized)
        self.vault_index.add_concept(synthesized.title, [])
        if not keep_inbox:
            self.file_manager.remove_inbox_file(file_path)

        self._try_reindex(final_path)

        return ProcessedNote(raw=raw, synthesized=synthesized, architected=architected, final_path=final_path)

    def _try_reindex(self, file_path: Path) -> None:
        try:
            from vault_embedder import reindex_file
            count = reindex_file(self.settings, file_path)
            print(f"RAG: indexed {count} chunks from {file_path.name}", file=sys.stderr)
        except Exception as exc:
            print(f"RAG: indexing failed for {file_path.name}: {exc}", file=sys.stderr)

    @staticmethod
    def _override_h1(markdown: str, title: str) -> str:
        lines = markdown.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("# "):
                lines[index] = f"# {title}"
                return "\n".join(lines)
        return f"# {title}\n\n{markdown.strip()}"
