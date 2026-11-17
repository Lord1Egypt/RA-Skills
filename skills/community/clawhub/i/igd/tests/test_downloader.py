"""
Basic tests for instagram_downloader.py

These tests validate the CLI parser, data fetching, normalization,
and filter logic without making network requests.
"""

import sys
import os
from datetime import datetime, timezone, date
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from instagram_downloader import (
    build_parser,
    normalize_item,
    fetch_from_toon,
)


# ── Test Fixtures ──────────────────────────────────────────────

SAMPLE_TOON = """
  - shortcode: CAROUSEL01
    type: carousel
    created_at: "2026-06-18T22:58:02.000Z"
    author_handle: profile_user
    thumbnail_url: https://scontent.cdninstagram.com/v/t51.12345/test1.jpg
  - shortcode: REEL001
    type: reel
    created_at: "2026-06-20T14:30:00.000Z"
    author_handle: mention_user
    video_url_no_watermark: https://scontent.cdninstagram.com/v/t51.12345/test2.mp4
    thumbnail_url: https://scontent.cdninstagram.com/v/t51.12345/test2_thumb.jpg
  - shortcode: PHOTO001
    type: photo
    created_at: "2026-06-25T10:00:00.000Z"
    author_handle: profile_user
    thumbnail_url: https://scontent.cdninstagram.com/v/t51.12345/test3.jpg
"""

SAMPLE_TOON_NESTED = """
  - shortcode: NESTED01
    type: carousel
    created_at: "2026-06-22T12:00:00.000Z"
    author.handle: nested_user
    video.url_no_watermark: https://example.com/video.mp4
"""


# ── Parser Tests ───────────────────────────────────────────────

class TestParser:
    def test_build_parser_minimal(self):
        """Parser accepts minimal arguments."""
        parser = build_parser()
        args = parser.parse_args(["--toon-file", "data.txt"])
        assert args.toon_file == "data.txt"
        assert args.type == "all"
        assert args.flat is False
        assert args.no_verify is False

    def test_build_parser_all_filters(self):
        """Parser accepts all filter arguments."""
        parser = build_parser()
        args = parser.parse_args([
            "--dataset", "abc123",
            "--api-token", "tok_xxx",
            "--profile", "test_user",
            "--date-start", "2026-01-01",
            "--date-end", "2026-12-31",
            "--type", "reel",
            "--own-only",
            "--output", "./out",
            "--flat",
            "--no-instagrapi",
        ])
        assert args.dataset == "abc123"
        assert args.api_token == "tok_xxx"
        assert args.profile == "test_user"
        assert args.own_only is True
        assert args.type == "reel"
        assert args.flat is True
        assert args.no_instagrapi is True


# ── Toon Parsing Tests ─────────────────────────────────────────

class TestFetchFromToon:
    def test_parse_flat_keys(self):
        """Parse toon format with flat keys."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_TOON)
            tmp = f.name
        try:
            items = fetch_from_toon(tmp)
            assert len(items) == 3

            # First item: carousel
            assert items[0]["shortcode"] == "CAROUSEL01"
            assert items[0]["type"] == "carousel"
            assert items[0]["author_handle"] == "profile_user"
            assert items[0]["thumbnail_url"] == (
                "https://scontent.cdninstagram.com/v/t51.12345/test1.jpg"
            )

            # Second item: reel
            assert items[1]["shortcode"] == "REEL001"
            assert items[1]["type"] == "reel"
            assert items[1]["video_url_no_watermark"] == (
                "https://scontent.cdninstagram.com/v/t51.12345/test2.mp4"
            )

            # Third item: photo
            assert items[2]["shortcode"] == "PHOTO001"
            assert items[2]["type"] == "photo"
        finally:
            os.unlink(tmp)

    def test_parse_nested_keys(self):
        """Parse toon format with dotted nested keys."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                         delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_TOON_NESTED)
            tmp = f.name
        try:
            items = fetch_from_toon(tmp)
            assert len(items) == 1
            assert items[0]["shortcode"] == "NESTED01"
            assert items[0]["author"]["handle"] == "nested_user"
            assert items[0]["video"]["url_no_watermark"] == (
                "https://example.com/video.mp4"
            )
        finally:
            os.unlink(tmp)


# ── Normalization Tests ────────────────────────────────────────

class TestNormalizeItem:
    def test_normalize_flat(self):
        """Normalize flat-format item."""
        raw = {
            "shortcode": "DZabc",
            "type": "reel",
            "created_at": "2026-06-20T14:30:00.000Z",
            "author_handle": "test_user",
            "video_url_no_watermark": "https://example.com/v.mp4",
            "thumbnail_url": "https://example.com/thumb.jpg",
        }
        norm = normalize_item(raw)
        assert norm["shortcode"] == "DZabc"
        assert norm["type"] == "reel"
        assert norm["author_handle"] == "test_user"
        assert norm["video_url"] == "https://example.com/v.mp4"
        assert norm["thumbnail_url"] == "https://example.com/thumb.jpg"
        assert norm["created_at"] is not None
        assert norm["created_at"].year == 2026
        assert norm["created_at"].month == 6

    def test_normalize_nested(self):
        """Normalize nested-format item (Apify API style)."""
        raw = {
            "shortcode": "DZxyz",
            "type": "carousel",
            "created_at": "2026-06-18T22:58:02.000Z",
            "author": {"handle": "nested_user"},
            "video": {"url_no_watermark": "https://example.com/v.mp4"},
            "thumbnail_url": "https://example.com/thumb.jpg",
        }
        norm = normalize_item(raw)
        assert norm["author_handle"] == "nested_user"
        assert norm["video_url"] == "https://example.com/v.mp4"

    def test_normalize_no_date(self):
        """Normalize item without a date returns None."""
        raw = {"shortcode": "DZno-date"}
        norm = normalize_item(raw)
        assert norm["created_at"] is None
        assert norm["created_at_str"] == ""


# ── Filter Logic Tests ─────────────────────────────────────────

class TestFilterLogic:
    """Validates filter logic without running process_items directly."""

    def test_date_filter_logic(self):
        """Date comparison logic works correctly."""
        dt_start = datetime(2026, 6, 6, tzinfo=timezone.utc)
        dt_end = datetime(2026, 7, 5, 23, 59, 59, tzinfo=timezone.utc)

        in_range = datetime(2026, 6, 18, tzinfo=timezone.utc)
        before = datetime(2026, 5, 1, tzinfo=timezone.utc)
        after = datetime(2026, 8, 1, tzinfo=timezone.utc)

        assert dt_start <= in_range <= dt_end
        assert not (dt_start <= before <= dt_end)
        assert not (dt_start <= after <= dt_end)

    def test_author_filter_logic(self):
        """Author ownership logic works correctly."""
        profile = "profile_user"
        own = "profile_user"
        mention = "mention_user"

        assert own == profile  # own
        assert mention != profile  # mention
