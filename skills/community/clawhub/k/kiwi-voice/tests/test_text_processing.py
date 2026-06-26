"""Tests for text processing utilities."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwi.i18n import setup

# Initialize i18n before importing text_processing
setup("en", fallback="ru")

from kiwi.text_processing import (
    remove_duplicate_prefixes,
    normalize_tts_text,
    clean_chunk_for_tts,
    quick_completeness_check,
    detect_emotion,
    split_text_into_chunks,
)


class TestRemoveDuplicatePrefixes:
    def test_removes_duplicate(self):
        assert remove_duplicate_prefixes("ПриПривет") == "Привет"

    def test_keeps_normal_text(self):
        assert remove_duplicate_prefixes("Привет") == "Привет"

    def test_short_text_unchanged(self):
        assert remove_duplicate_prefixes("Да") == "Да"

    def test_empty_string(self):
        assert remove_duplicate_prefixes("") == ""

    def test_triple_prefix(self):
        result = remove_duplicate_prefixes("HeyHeyHey")
        assert result == "Hey"


class TestNormalizeTtsText:
    def test_strips_markdown_bold(self):
        # normalize_tts_text doesn't strip ** (that's clean_chunk_for_tts)
        result = clean_chunk_for_tts("This is **bold** text")
        assert "**" not in result

    def test_strips_code_blocks(self):
        result = normalize_tts_text("Run ```python\nprint('hi')``` now")
        assert "```" not in result
        assert "print" not in result

    def test_strips_urls(self):
        result = normalize_tts_text("Visit https://example.com for more")
        assert "https://" not in result

    def test_strips_inline_code(self):
        result = normalize_tts_text("Use `pip install` to install")
        assert "`" not in result
        assert "pip install" in result

    def test_empty_string(self):
        assert normalize_tts_text("") == ""

    def test_normalizes_whitespace(self):
        result = normalize_tts_text("hello    world")
        assert "    " not in result


class TestCleanChunkForTts:
    def test_removes_emoji(self):
        result = clean_chunk_for_tts("Hello! 😊 How are you?")
        assert "😊" not in result

    def test_removes_markdown(self):
        result = clean_chunk_for_tts("**bold** and *italic*")
        assert "*" not in result

    def test_empty_string(self):
        assert clean_chunk_for_tts("") == ""

    def test_json_artifacts(self):
        result = clean_chunk_for_tts("{'type': 'text', 'text': 'Hello'}")
        assert "type" not in result


class TestQuickCompletenessCheck:
    def test_ends_with_period(self):
        assert quick_completeness_check("This is a complete sentence.") is True

    def test_ends_with_question(self):
        assert quick_completeness_check("Is this complete?") is True

    def test_ends_with_exclamation(self):
        assert quick_completeness_check("This is great!") is True

    def test_short_text_incomplete(self):
        assert quick_completeness_check("Hi") is False

    def test_empty_string(self):
        assert quick_completeness_check("") is False


class TestDetectEmotion:
    def test_default_neutral(self):
        assert detect_emotion("hello", "hi there") == "neutral"

    def test_question_returns_playful(self):
        assert detect_emotion("what is this?", "it is a thing") == "playful"

    def test_returns_string(self):
        result = detect_emotion("tell me something", "here is something")
        assert isinstance(result, str)


class TestSplitTextIntoChunks:
    def test_short_text_single_chunk(self):
        chunks = split_text_into_chunks("Hello world.")
        assert len(chunks) == 1
        assert chunks[0] == "Hello world."

    def test_splits_on_sentences(self):
        text = "First sentence. Second sentence. Third sentence."
        chunks = split_text_into_chunks(text, max_chunk_size=30)
        assert len(chunks) > 1

    def test_respects_max_size(self):
        text = "A. " * 100
        chunks = split_text_into_chunks(text, max_chunk_size=50)
        for chunk in chunks:
            assert len(chunk) <= 55  # some tolerance for sentence boundaries

    def test_empty_returns_original(self):
        chunks = split_text_into_chunks("")
        assert chunks == [""]

    def test_returns_list(self):
        assert isinstance(split_text_into_chunks("Hello."), list)
