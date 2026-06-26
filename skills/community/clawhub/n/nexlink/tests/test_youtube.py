#!/usr/bin/env python3
"""Tests for the YouTube transcript module."""

import json
import os
import sys
import unittest

# Ensure the skill root is on the path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, SKILL_ROOT)

from modules.youtube.youtube import (
    extract_video_id,
    get_transcript,
    list_languages,
    format_filename,
    build_parser,
)


class TestYouTubeIDExtraction(unittest.TestCase):
    """Test video ID extraction from various URL formats."""

    valid_id = "dQw4w9WgXcQ"

    def test_standard_url(self):
        self.assertEqual(
            extract_video_id(f"https://www.youtube.com/watch?v={self.valid_id}"),
            self.valid_id,
        )

    def test_short_url(self):
        self.assertEqual(
            extract_video_id(f"https://youtu.be/{self.valid_id}"),
            self.valid_id,
        )

    def test_shorts_url(self):
        self.assertEqual(
            extract_video_id(f"https://www.youtube.com/shorts/{self.valid_id}"),
            self.valid_id,
        )

    def test_embed_url(self):
        self.assertEqual(
            extract_video_id(f"https://www.youtube.com/embed/{self.valid_id}"),
            self.valid_id,
        )

    def test_raw_id(self):
        self.assertEqual(extract_video_id(self.valid_id), self.valid_id)

    def test_url_with_extra_params(self):
        self.assertEqual(
            extract_video_id(
                f"https://www.youtube.com/watch?v={self.valid_id}&t=30s&ab_channel=Test"
            ),
            self.valid_id,
        )

    def test_url_in_text(self):
        self.assertEqual(
            extract_video_id(
                f"Check this out: https://youtu.be/{self.valid_id} it's great!"
            ),
            self.valid_id,
        )

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            extract_video_id("not-a-real-id")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            extract_video_id("")

    def test_almost_valid_length(self):
        """12 characters should fail, 11 is required."""
        with self.assertRaises(ValueError):
            extract_video_id("a" * 12)


class TestFormatFilename(unittest.TestCase):
    """Test filename generation."""

    def test_text_filename(self):
        self.assertEqual(format_filename("abcd1234xyz", "en", "text"), "abcd1234xyz_en.txt")

    def test_json_filename(self):
        self.assertEqual(format_filename("abcd1234xyz", "ro", "json"), "abcd1234xyz_ro.json")

    def test_with_dash_lang(self):
        self.assertEqual(
            format_filename("abcd1234xyz", "de-DE", "json"), "abcd1234xyz_de-DE.json"
        )


class TestParser(unittest.TestCase):
    """Test argument parser."""

    def setUp(self):
        self.parser = build_parser()

    def test_transcript_defaults(self):
        args = self.parser.parse_args(["transcript", "dQw4w9WgXcQ"])
        self.assertEqual(args.url, "dQw4w9WgXcQ")
        self.assertEqual(args.lang, "en")
        self.assertEqual(args.format, "text")
        self.assertFalse(args.save)

    def test_transcript_custom_lang(self):
        args = self.parser.parse_args(["transcript", "url", "--lang", "ro,en"])
        self.assertEqual(args.lang, "ro,en")

    def test_transcript_json(self):
        args = self.parser.parse_args(["transcript", "url", "--format", "json"])
        self.assertEqual(args.format, "json")

    def test_transcript_save(self):
        args = self.parser.parse_args(["transcript", "url", "--save"])
        self.assertTrue(args.save)

    def test_languages(self):
        args = self.parser.parse_args(["languages", "dQw4w9WgXcQ"])
        self.assertEqual(args.url, "dQw4w9WgXcQ")


class TestLiveTranscript(unittest.TestCase):
    """Live tests against YouTube API. Skip if offline or API fails."""

    test_video = "dQw4w9WgXcQ"  # Rick Astley — stable, won't be taken down

    def test_list_languages(self):
        try:
            result = list_languages(self.test_video)
        except Exception as e:
            self.skipTest(f"API unavailable: {e}")

        self.assertTrue(result["ok"])
        self.assertEqual(result["video_id"], self.test_video)
        self.assertGreater(len(result["languages"]), 0)
        self.assertIn("en", [l["code"] for l in result["languages"]])

    def test_get_transcript_text(self):
        try:
            result = get_transcript(self.test_video, languages=("en",), fmt="text")
        except Exception as e:
            self.skipTest(f"API unavailable: {e}")

        self.assertTrue(result["ok"])
        self.assertEqual(result["lang"], "en")
        self.assertIsInstance(result["transcript"], str)
        self.assertGreater(len(result["transcript"]), 50)
        self.assertIn("Never gonna give you up", result["transcript"])

    def test_get_transcript_json(self):
        try:
            result = get_transcript(self.test_video, languages=("en",), fmt="json")
        except Exception as e:
            self.skipTest(f"API unavailable: {e}")

        self.assertTrue(result["ok"])
        self.assertIsInstance(result["transcript"], list)
        self.assertGreater(len(result["transcript"]), 0)
        self.assertIn("text", result["transcript"][0])
        self.assertIn("start", result["transcript"][0])
        self.assertIn("duration", result["transcript"][0])

    def test_language_fallback(self):
        """Should fall back to English when Romanian is not available."""
        try:
            result = get_transcript(self.test_video, languages=("ro", "en"), fmt="text")
        except Exception as e:
            self.skipTest(f"API unavailable: {e}")

        self.assertTrue(result["ok"])
        self.assertEqual(result["lang"], "en")


class TestErrorHandling(unittest.TestCase):
    """Test error handling without hitting the API."""

    def test_invalid_video_id_format(self):
        with self.assertRaises(ValueError):
            extract_video_id("bad-id!")


if __name__ == "__main__":
    unittest.main()
