#!/usr/bin/env python3
"""
create.py — Post type schemas, validation, and formatting helpers.

Defines structured post types for each platform with required fields,
character limits, and validation rules. The agent uses these to create
and validate content before publishing.

Usage (as library):
    from create.create import XTweet, LinkedInPost, validate, from_draft, post_types
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field, fields, asdict, MISSING
from pathlib import Path
from typing import Any


# ── Post Type Schemas ───────────────────────────────────────────────────────


@dataclass
class XTweet:
    """Single X/Twitter post."""
    platform: str = field(default="x", init=False)
    post_type: str = field(default="tweet", init=False)
    text: str = ""                    # required, max 280 chars
    media_path: str | None = None     # optional image/video
    image_prompt: str | None = None   # optional: generate image from this prompt

    MAX_TEXT_LENGTH = 280


@dataclass
class XThread:
    """Multi-tweet X/Twitter thread."""
    platform: str = field(default="x", init=False)
    post_type: str = field(default="thread", init=False)
    segments: list[str] = field(default_factory=list)  # required, each max 280 chars
    media_path: str | None = None     # optional, attaches to first tweet
    image_prompt: str | None = None   # optional: generate image from this prompt

    MAX_SEGMENT_LENGTH = 280


@dataclass
class LinkedInPost:
    """LinkedIn feed post."""
    platform: str = field(default="linkedin", init=False)
    post_type: str = field(default="post", init=False)
    text: str = ""                    # required, ~200 words recommended, max ~3000 chars
    media_path: str | None = None     # optional single image
    image_prompt: str | None = None   # optional: generate image from this prompt

    MAX_TEXT_LENGTH = 3000
    RECOMMENDED_WORDS = 200


@dataclass
class LinkedInArticle:
    """LinkedIn long-form article."""
    platform: str = field(default="linkedin", init=False)
    post_type: str = field(default="article", init=False)
    title: str = ""                   # required
    body: str = ""                    # required, 600-1000 words
    cover_image: str | None = None    # recommended
    intro_post: str | None = None     # short feed post to promote it

    MIN_WORDS = 600
    MAX_WORDS = 1000


# ── Registry ────────────────────────────────────────────────────────────────

POST_TYPE_CLASSES = {
    ("x", "tweet"): XTweet,
    ("x", "thread"): XThread,
    ("linkedin", "post"): LinkedInPost,
    ("linkedin", "article"): LinkedInArticle,
}


def post_types() -> dict[str, dict[str, Any]]:
    """Return all available post types with their field definitions.

    Useful for agent introspection — shows what fields are required
    and what constraints apply.
    """
    result = {}
    for (platform, ptype), cls in POST_TYPE_CLASSES.items():
        key = f"{platform}_{ptype}"
        field_info = {}
        for f in fields(cls):
            if f.name in ("platform", "post_type"):
                continue
            field_info[f.name] = {
                "type": str(f.type),
                "default": None if f.default is MISSING else f.default,
            }
        # Add constraints from class attributes
        constraints = {}
        for attr in dir(cls):
            if attr.startswith("MAX_") or attr.startswith("MIN_") or attr.startswith("RECOMMENDED_"):
                constraints[attr.lower()] = getattr(cls, attr)
        result[key] = {
            "platform": platform,
            "post_type": ptype,
            "fields": field_info,
            "constraints": constraints,
        }
    return result


# ── Validation ──────────────────────────────────────────────────────────────


def validate(post) -> list[str]:
    """Validate a post dataclass. Returns list of error strings (empty = valid)."""
    errors = []

    if isinstance(post, XTweet):
        if not post.text.strip():
            errors.append("text is required")
        elif len(post.text) > XTweet.MAX_TEXT_LENGTH:
            errors.append(f"text exceeds {XTweet.MAX_TEXT_LENGTH} chars ({len(post.text)})")

    elif isinstance(post, XThread):
        if not post.segments:
            errors.append("segments list is required and must not be empty")
        for i, seg in enumerate(post.segments, 1):
            if len(seg) > XThread.MAX_SEGMENT_LENGTH:
                errors.append(f"segment {i} exceeds {XThread.MAX_SEGMENT_LENGTH} chars ({len(seg)})")
            if not seg.strip():
                errors.append(f"segment {i} is empty")

    elif isinstance(post, LinkedInPost):
        if not post.text.strip():
            errors.append("text is required")
        elif len(post.text) > LinkedInPost.MAX_TEXT_LENGTH:
            errors.append(f"text exceeds {LinkedInPost.MAX_TEXT_LENGTH} chars ({len(post.text)})")

    elif isinstance(post, LinkedInArticle):
        if not post.title.strip():
            errors.append("title is required")
        if not post.body.strip():
            errors.append("body is required")
        else:
            word_count = len(post.body.split())
            if word_count < LinkedInArticle.MIN_WORDS:
                errors.append(f"body is {word_count} words (minimum {LinkedInArticle.MIN_WORDS})")
            if word_count > LinkedInArticle.MAX_WORDS:
                errors.append(f"body is {word_count} words (maximum {LinkedInArticle.MAX_WORDS})")

    if hasattr(post, "media_path") and post.media_path:
        if not Path(post.media_path).exists():
            errors.append(f"media_path does not exist: {post.media_path}")

    # Auto-generate image if image_prompt is set but media_path is empty
    if hasattr(post, "image_prompt") and post.image_prompt and not post.media_path:
        try:
            # Add scripts/ parent to path so 'scripts' packages are importable
            import scripts.create.image_gen as img_mod
            generate_image = img_mod.generate_image
            platform_name = "x" if post.platform == "x" else "linkedin"
            path = generate_image(
                prompt=post.image_prompt,
                platform=platform_name,
            )
            post.media_path = path
            print(f"[create] Generated image: {path}", file=sys.stderr)
        except Exception as exc:
            errors.append(f"image generation failed: {exc}")

    if hasattr(post, "cover_image") and post.cover_image:
        if not Path(post.cover_image).exists():
            errors.append(f"cover_image does not exist: {post.cover_image}")

    return errors


# ── Draft Parsing ───────────────────────────────────────────────────────────


def _parse_draft_metadata(text: str) -> dict[str, str]:
    """Extract metadata fields from a draft markdown file."""
    meta = {}
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            meta["title"] = stripped[2:].strip()
        elif stripped.startswith("_Format:"):
            meta["format"] = stripped.strip("_").split(":", 1)[1].strip().lower()
        elif stripped.startswith("_Status:"):
            meta["status"] = stripped.strip("_").split(":", 1)[1].strip()
        elif stripped.startswith("_Topic:"):
            meta["topic"] = stripped.strip("_").split(":", 1)[1].strip()
        elif stripped == "---":
            break
    return meta


def _extract_body(text: str) -> str:
    """Extract the body content after metadata headers."""
    lines = text.splitlines()
    body_start = 0
    for idx, line in enumerate(lines):
        if line.strip() == "---":
            body_start = idx + 1
            break
    while body_start < len(lines) and lines[body_start].strip() in ("", "---"):
        body_start += 1
    return "\n".join(lines[body_start:]).strip()


def from_draft(path: str | Path) -> XTweet | XThread | LinkedInPost | LinkedInArticle:
    """Parse a markdown draft file into the appropriate post type.

    Infers platform from filename (e.g. 'X Tweet - Title.md', 'LinkedIn Post - Title.md').
    """
    path = Path(path)
    text = path.read_text()
    meta = _parse_draft_metadata(text)
    body = _extract_body(text)

    # Infer platform and type from filename
    name_lower = path.name.lower()
    fmt = meta.get("format", "")

    if name_lower.startswith("x"):
        # Check if it's a thread (numbered segments)
        if "thread" in fmt or re.search(r"(?m)^\d+\.\s+", body):
            segments = _parse_thread_segments(body)
            return XThread(segments=segments)
        return XTweet(text=body)

    elif name_lower.startswith("linkedin"):
        if "article" in fmt:
            return LinkedInArticle(
                title=meta.get("title", path.stem),
                body=body,
            )
        return LinkedInPost(text=body)

    raise ValueError(f"Cannot infer platform from filename: {path.name}")


def _parse_thread_segments(body: str) -> list[str]:
    """Parse numbered thread segments from body text."""
    matches = list(re.finditer(r"(?m)^(?P<num>\d+)\.\s+", body))
    if not matches:
        return [body.strip()]
    segments = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        segment = re.sub(r"\n{3,}", "\n\n", body[start:end].strip())
        if segment:
            segments.append(segment)
    return segments


# ── Draft Serialization ─────────────────────────────────────────────────────


def to_draft(post, path: str | Path) -> None:
    """Serialize a post type back to markdown draft format."""
    path = Path(path)
    lines = []

    if isinstance(post, (XTweet, XThread)):
        platform_label = "X"
    else:
        platform_label = "LinkedIn"

    title = getattr(post, "title", None) or path.stem.split(" - ", 1)[-1] if " - " in path.stem else path.stem
    lines.append(f"# {title}")
    lines.append(f"_Format: {post.post_type.title()}_")
    lines.append("_Status: draft_")
    lines.append("")
    lines.append("---")
    lines.append("")

    if isinstance(post, XThread):
        for i, seg in enumerate(post.segments, 1):
            lines.append(f"{i}. {seg}")
            lines.append("")
    elif isinstance(post, LinkedInArticle):
        lines.append(post.body)
    elif isinstance(post, (XTweet, LinkedInPost)):
        lines.append(post.text)

    path.write_text("\n".join(lines) + "\n")


# ── Preview ─────────────────────────────────────────────────────────────────


def format_preview(post) -> str:
    """Human-readable preview of a post."""
    lines = [f"Platform: {post.platform}", f"Type: {post.post_type}"]

    if isinstance(post, XTweet):
        lines.append(f"Length: {len(post.text)}/{XTweet.MAX_TEXT_LENGTH} chars")
        lines.append(f"\n{post.text}")

    elif isinstance(post, XThread):
        lines.append(f"Segments: {len(post.segments)}")
        for i, seg in enumerate(post.segments, 1):
            lines.append(f"\n[{i}/{len(post.segments)}] ({len(seg)}/{XThread.MAX_SEGMENT_LENGTH} chars)")
            lines.append(seg)

    elif isinstance(post, LinkedInPost):
        word_count = len(post.text.split())
        lines.append(f"Words: {word_count} (recommended: ≤{LinkedInPost.RECOMMENDED_WORDS})")
        lines.append(f"Chars: {len(post.text)}/{LinkedInPost.MAX_TEXT_LENGTH}")
        lines.append(f"\n{post.text}")

    elif isinstance(post, LinkedInArticle):
        word_count = len(post.body.split())
        lines.append(f"Title: {post.title}")
        lines.append(f"Words: {word_count} ({LinkedInArticle.MIN_WORDS}-{LinkedInArticle.MAX_WORDS})")
        if post.cover_image:
            lines.append(f"Cover: {post.cover_image}")
        lines.append(f"\n{post.body[:500]}{'...' if len(post.body) > 500 else ''}")

    if hasattr(post, "media_path") and post.media_path:
        lines.append(f"\nMedia: {post.media_path}")
    elif hasattr(post, "image_prompt") and post.image_prompt:
        lines.append(f"\nImage prompt: {post.image_prompt[:80]}{'...' if len(post.image_prompt) > 80 else ''}")
        lines.append("  (run validate() to generate the image)")

    errors = validate(post)
    if errors:
        lines.append(f"\nValidation errors:")
        for e in errors:
            lines.append(f"  - {e}")
    else:
        lines.append(f"\n✓ Valid")

    return "\n".join(lines)
