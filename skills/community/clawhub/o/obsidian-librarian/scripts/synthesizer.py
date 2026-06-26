#!/usr/bin/env python3
from __future__ import annotations

import re
import time

from common import gemini_generate_text, slugify
from config import LibrarianSettings
from models import RawInboxItem, SynthesizedContent
from prompts import SYNTHESIZER_PROMPT


class ContentSynthesizer:
    def __init__(self, settings: LibrarianSettings) -> None:
        self.settings = settings

    def synthesize(self, raw: RawInboxItem) -> SynthesizedContent:
        x_post = self._synthesize_x_post(raw)
        if x_post is not None:
            return x_post

        prompt = SYNTHESIZER_PROMPT.format(raw_content=raw.raw_content)
        delays = [2, 4, 8]
        last_error: Exception | None = None

        for attempt in range(len(delays) + 1):
            try:
                markdown = gemini_generate_text(
                    api_key=self.settings.gemini_api_key,
                    model=self.settings.gemini_model,
                    prompt=prompt,
                    temperature=0.3,
                ).strip()
                title = self._extract_title(markdown) or self._fallback_title(raw)
                markdown = self._ensure_h1(markdown, title)
                summary = self._extract_summary(markdown)
                return SynthesizedContent(title=title, markdown_body=markdown, summary=summary)
            except Exception as exc:
                last_error = exc
                if attempt >= len(delays):
                    break
                time.sleep(delays[attempt])

        fallback = self._fallback_markdown(raw, last_error)
        title = self._extract_title(fallback) or self._fallback_title(raw)
        summary = self._extract_summary(fallback)
        return SynthesizedContent(title=title, markdown_body=fallback, summary=summary)

    def _synthesize_x_post(self, raw: RawInboxItem) -> SynthesizedContent | None:
        parsed = self._parse_x_post_capture(raw.raw_content)
        if parsed is None:
            return None

        published_date = parsed["published"].split("T", 1)[0] if parsed["published"] else "unknown-date"
        title = f"X Post by {parsed['author_name']} ({published_date})"

        summary_parts = [
            f"This note captures an X post by {parsed['author_name']} (@{parsed['author_username']})",
        ]
        if parsed["published"]:
            summary_parts.append(f"published on {published_date}")
        if parsed["likes"] or parsed["replies"]:
            engagement: list[str] = []
            if parsed["likes"]:
                engagement.append(f"{parsed['likes']} likes")
            if parsed["replies"]:
                engagement.append(f"{parsed['replies']} replies")
            summary_parts.append("with " + " and ".join(engagement))
        summary = " ".join(summary_parts).strip() + "."
        if parsed["post_text"]:
            if self._is_plain_url(parsed["post_text"]):
                summary += " The post body consists of a link, which is preserved below."
            else:
                summary += " The post text is preserved below."

        lines = [
            f"# {title}",
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Post Details",
            "",
            f"- **Author**: {parsed['author_name']} (@{parsed['author_username']})",
            f"- **Published Date**: {published_date}",
            f"- **Original Post URL**: `{parsed['source_url']}`",
        ]
        if parsed["likes"]:
            lines.append(f"- **Likes**: {parsed['likes']}")
        if parsed["replies"]:
            lines.append(f"- **Replies**: {parsed['replies']}")

        if parsed["post_text"]:
            lines.extend([
                "",
                "## Post Content",
                "",
            ])
            if self._is_plain_url(parsed["post_text"]):
                lines.extend([
                    "The post body is a URL:",
                    "",
                    f"- `{parsed['post_text']}`",
                ])
            else:
                lines.append(parsed["post_text"])

        if parsed["external_urls"]:
            lines.extend([
                "",
                "## Associated Links",
                "",
            ])
            for url in parsed["external_urls"]:
                lines.append(f"- `{url}`")

        if parsed["linked_sources"]:
            lines.extend([
                "",
                "## Linked Sources",
                "",
            ])
            for source in parsed["linked_sources"]:
                lines.extend([
                    f"### {source['title']}",
                    "",
                    f"- **Linked URL**: `{source['url']}`",
                ])
                if source["body"]:
                    lines.extend([
                        "",
                        source["body"],
                    ])
                lines.append("")
            if lines[-1] == "":
                lines.pop()

        markdown = "\n".join(lines).strip() + "\n"
        return SynthesizedContent(title=title, markdown_body=markdown, summary=summary)

    def _fallback_title(self, raw: RawInboxItem) -> str:
        stem = raw.file_path.stem.replace("-", " ").strip()
        return stem.title() or slugify(raw.file_path.stem, fallback="captured-note").replace("-", " ").title()

    def _fallback_markdown(self, raw: RawInboxItem, error: Exception | None) -> str:
        title = self._fallback_title(raw)
        reason = str(error) if error else "unknown error"
        body = raw.raw_content.strip() or "No content was captured."
        return (
            f"# {title}\n\n"
            "## Summary\n\n"
            f"Source imported with minimal cleanup because Gemini synthesis failed ({reason}).\n\n"
            "## Captured Content\n\n"
            f"{body}\n"
        )

    @staticmethod
    def _extract_title(markdown: str) -> str:
        for line in markdown.splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return ""

    @staticmethod
    def _ensure_h1(markdown: str, title: str) -> str:
        if re.search(r"^#\s+", markdown, flags=re.MULTILINE):
            return markdown
        return f"# {title}\n\n{markdown.strip()}"

    @staticmethod
    def _extract_summary(markdown: str) -> str:
        lines = [line.rstrip() for line in markdown.splitlines()]
        summary_lines: list[str] = []
        collecting = False

        for line in lines:
            stripped = line.strip()
            if stripped.lower() in {"## summary", "summary"}:
                collecting = True
                continue
            if collecting:
                if stripped.startswith("#"):
                    break
                if stripped:
                    summary_lines.append(stripped)
                elif summary_lines:
                    break

        if summary_lines:
            return " ".join(summary_lines).strip()

        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped
        return ""

    @staticmethod
    def _is_plain_url(text: str) -> bool:
        return bool(re.fullmatch(r"https?://\S+", text.strip()))

    @classmethod
    def _parse_x_post_capture(cls, raw_content: str) -> dict[str, object] | None:
        source_url_match = re.search(
            r"^Source URL:\s*(https?://(?:www\.)?(?:x|twitter)\.com/[^\s]+/status/\d+)\s*$",
            raw_content,
            flags=re.MULTILINE,
        )
        author_match = re.search(r"^Author:\s*(.+?)\s+\(@([^)]+)\)\s*$", raw_content, flags=re.MULTILINE)
        if not source_url_match or not author_match:
            return None

        published = cls._match_value(raw_content, "Published")
        likes = cls._match_value(raw_content, "Likes")
        replies = cls._match_value(raw_content, "Replies")

        lines = raw_content.splitlines()
        post_text = ""
        external_urls: list[str] = []
        linked_sources: list[dict[str, str]] = []

        replies_index = next((i for i, line in enumerate(lines) if line.startswith("Replies:")), -1)
        if replies_index >= 0:
            idx = replies_index + 1
            while idx < len(lines) and not lines[idx].strip():
                idx += 1
            post_lines: list[str] = []
            while idx < len(lines):
                stripped = lines[idx].strip()
                if stripped == "External URLs:" or stripped.startswith("## Linked Source:"):
                    break
                post_lines.append(lines[idx].rstrip())
                idx += 1
            post_text = "\n".join(line for line in post_lines).strip()

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("- http://") or stripped.startswith("- https://"):
                external_urls.append(stripped[2:].strip())

        current_source: dict[str, str] | None = None
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("## Linked Source:"):
                if current_source:
                    linked_sources.append(current_source)
                current_source = {"title": stripped.split(":", 1)[1].strip(), "url": "", "body": ""}
            elif current_source is not None and stripped.startswith("Linked URL:"):
                current_source["url"] = stripped.split(":", 1)[1].strip()
            elif current_source is not None:
                if current_source["body"]:
                    current_source["body"] += "\n" + line.rstrip()
                else:
                    current_source["body"] = line.rstrip()
        if current_source:
            linked_sources.append(current_source)

        return {
            "source_url": source_url_match.group(1),
            "author_name": author_match.group(1).strip(),
            "author_username": author_match.group(2).strip(),
            "published": published,
            "likes": likes,
            "replies": replies,
            "post_text": post_text,
            "external_urls": external_urls,
            "linked_sources": linked_sources,
        }

    @staticmethod
    def _match_value(raw_content: str, label: str) -> str:
        match = re.search(rf"^{re.escape(label)}:\s*(.+?)\s*$", raw_content, flags=re.MULTILINE)
        return match.group(1).strip() if match else ""
