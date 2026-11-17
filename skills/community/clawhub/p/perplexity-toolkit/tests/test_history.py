"""Tests for history module."""
import sys; sys.path.insert(0, "src")

from perplexity_toolkit.history import Conversation


class TestConversation:
    def test_typed_dict_structure(self):
        c: Conversation = {"href": "abc-123", "title": "Test query"}
        assert c["href"] == "abc-123"
        assert c["title"] == "Test query"

    def test_empty_conversation(self):
        c: Conversation = {"href": "", "title": ""}
        assert c["href"] == ""
        assert c["title"] == ""
