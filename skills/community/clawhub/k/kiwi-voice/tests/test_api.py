"""Tests for API server endpoint definitions."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_import_api_server():
    from kiwi.api.server import KiwiAPI
    assert KiwiAPI is not None


def test_api_server_has_required_methods():
    from kiwi.api.server import KiwiAPI
    required = [
        "_handle_status",
        "_handle_get_config",
        "_handle_get_speakers",
        "_handle_get_languages",
        "_handle_get_souls",
        "_handle_get_current_soul",
        "_handle_stop",
        "_handle_reset_context",
    ]
    for method in required:
        assert hasattr(KiwiAPI, method), f"Missing method: {method}"
