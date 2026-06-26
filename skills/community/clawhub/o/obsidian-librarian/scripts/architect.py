#!/usr/bin/env python3
from __future__ import annotations

import re

from common import gemini_generate_json
from config import LibrarianSettings
from models import ArchitectOutput, SynthesizedContent
from prompts import ARCHITECT_PROMPT
from vault_index import VaultIndex


ARCHITECT_SCHEMA = {
    "type": "object",
    "properties": {
        "tags": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string"},
        "source": {"type": "string"},
        "wikilinks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "link": {"type": "string"},
                },
                "required": ["text", "link"],
            },
        },
    },
    "required": ["tags", "category", "source", "wikilinks"],
}


class MetadataArchitect:
    def __init__(self, settings: LibrarianSettings, vault_index: VaultIndex) -> None:
        self.settings = settings
        self.vault_index = vault_index

    def architect(self, content: SynthesizedContent, raw_content: str | None = None) -> ArchitectOutput:
        concepts = self.vault_index.get_concepts_list()
        concept_blob = "\n".join(f"- {concept}" for concept in concepts[:500]) or "- None yet"
        category_blob = "\n".join(
            f"- {name}: {desc}" for name, desc in self.settings.categories.items()
        )
        prompt = ARCHITECT_PROMPT.format(
            categories=category_blob,
            concepts=concept_blob,
            markdown_body=content.markdown_body,
        )

        fallback_frontmatter = {
            "title": content.title,
            "summary": content.summary,
            "tags": [],
            "source": "manual paste",
            "needs_review": True,
        }

        try:
            payload = gemini_generate_json(
                api_key=self.settings.gemini_api_key,
                model=self.settings.gemini_model,
                prompt=prompt,
                schema=ARCHITECT_SCHEMA,
                temperature=0.2,
            )
            tags = self._normalize_tags(payload.get("tags") or [])
            category = payload.get("category") or "Uncategorized"
            if category not in self.settings.categories.keys():
                category = "Uncategorized"
            source = (payload.get("source") or "manual paste").strip()
            source_hint = self._extract_source_hint(raw_content or "")
            if source_hint:
                source = source_hint
            wikilinks = payload.get("wikilinks") or []
            wikilinked_body = self._apply_wikilinks(content.markdown_body, wikilinks, set(concepts))
            frontmatter = {
                "title": content.title,
                "summary": content.summary,
                "tags": tags,
                "source": source,
                "needs_review": False,
            }
            return ArchitectOutput(frontmatter=frontmatter, wikilinked_body=wikilinked_body, category=category)
        except Exception:
            source_hint = self._extract_source_hint(raw_content or "") or "manual paste"
            return ArchitectOutput(
                frontmatter={**fallback_frontmatter, "source": source_hint},
                wikilinked_body=content.markdown_body,
                category="Uncategorized",
            )

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for tag in tags:
            clean = re.sub(r"\s+", "-", str(tag).strip().lower())
            clean = re.sub(r"[^a-z0-9_-]+", "", clean)
            if not clean or clean in seen:
                continue
            seen.add(clean)
            result.append(clean)
        return result[:8]

    def _apply_wikilinks(self, body: str, wikilinks: list[dict], concepts: set[str]) -> str:
        result = body
        ordered = sorted(
            [
                {"text": str(item.get("text", "")).strip(), "link": str(item.get("link", "")).strip()}
                for item in wikilinks
            ],
            key=lambda item: len(item["text"]),
            reverse=True,
        )
        for item in ordered:
            text = item["text"]
            link = item["link"]
            if not text or not link or link not in concepts:
                continue
            if f"[[{link}]]" in result:
                continue
            pattern = self._phrase_pattern(text)
            replacement = f"[[{link}]]"
            result, count = pattern.subn(replacement, result, count=1)
            if count == 0 and text != link:
                fallback_pattern = self._phrase_pattern(link)
                result = fallback_pattern.sub(replacement, result, count=1)
        return result

    @staticmethod
    def _phrase_pattern(text: str) -> re.Pattern[str]:
        escaped = re.escape(text)
        if text[:1].isalnum():
            escaped = r"\b" + escaped
        if text[-1:].isalnum():
            escaped = escaped + r"\b"
        return re.compile(rf"(?<!\[\[){escaped}(?!\]\])", flags=re.IGNORECASE)

    @staticmethod
    def _extract_source_hint(raw_content: str) -> str | None:
        match = re.search(r"^Source URL:\s*(https?://\S+)\s*$", raw_content, flags=re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None
