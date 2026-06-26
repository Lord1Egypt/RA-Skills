import os
import sys
import unittest
from unittest.mock import patch


SCRIPT_DIR = os.path.join("D:\\skill", "meeting-minutes-qa-tts", "scripts")
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from generate_meeting_audio import resolve_senseaudio_api_key


class SenseAudioApiKeyResolutionTests(unittest.TestCase):
    def test_prefers_explicit_api_key_after_trimming(self) -> None:
        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": "env-key"}, clear=False):
            self.assertEqual(resolve_senseaudio_api_key("  user-key  "), "user-key")

    def test_uses_env_api_key_when_explicit_key_is_missing(self) -> None:
        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": "  env-key  "}, clear=False):
            self.assertEqual(resolve_senseaudio_api_key(None), "env-key")

    def test_treats_blank_explicit_key_as_missing_and_falls_back_to_env(self) -> None:
        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": "env-key"}, clear=False):
            self.assertEqual(resolve_senseaudio_api_key("   "), "env-key")

    def test_returns_none_when_no_usable_key_is_available(self) -> None:
        with patch.dict(os.environ, {"SENSEAUDIO_API_KEY": "   "}, clear=False):
            self.assertIsNone(resolve_senseaudio_api_key(None))


if __name__ == "__main__":
    unittest.main()
