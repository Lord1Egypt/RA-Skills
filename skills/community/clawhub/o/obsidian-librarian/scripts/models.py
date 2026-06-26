#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class RawInboxItem:
    file_path: Path
    raw_content: str
    detected_at: datetime


@dataclass
class SynthesizedContent:
    title: str
    markdown_body: str
    summary: str


@dataclass
class ArchitectOutput:
    frontmatter: dict[str, Any]
    wikilinked_body: str
    category: str


@dataclass
class ProcessedNote:
    raw: RawInboxItem
    synthesized: SynthesizedContent
    architected: ArchitectOutput
    final_path: Path
