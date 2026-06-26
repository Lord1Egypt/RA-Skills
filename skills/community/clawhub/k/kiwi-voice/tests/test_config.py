"""Tests for configuration loading and validation."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwi.config_loader import KiwiConfig


class TestKiwiConfig:
    def test_default_values(self):
        config = KiwiConfig()
        assert config.wake_word_keyword is not None
        assert config.tts_provider is not None
        assert config.stt_model is not None

    def test_from_yaml_overrides(self):
        yaml_config = {
            "stt": {"model": "small", "device": "cpu"},
            "tts": {"provider": "piper"},
            "wake_word": {"keyword": "jarvis"},
        }
        config = KiwiConfig.from_yaml(yaml_config)
        assert config.stt_model == "small"
        assert config.stt_device == "cpu"
        assert config.tts_provider == "piper"
        assert config.wake_word_keyword == "jarvis"

    def test_from_yaml_empty(self):
        config = KiwiConfig.from_yaml({})
        assert config.wake_word_keyword is not None

    def test_from_yaml_none(self):
        config = KiwiConfig.from_yaml({})
        assert config is not None

    def test_tts_provider_values(self):
        for provider in ("piper", "elevenlabs", "qwen3", "kokoro"):
            config = KiwiConfig.from_yaml({"tts": {"provider": provider}})
            assert config.tts_provider == provider

    def test_language_config(self):
        config = KiwiConfig.from_yaml({"language": "en"})
        assert config.language == "en"

    def test_api_config(self):
        config = KiwiConfig.from_yaml({
            "api": {"enabled": True, "port": 8080, "host": "0.0.0.0"}
        })
        assert config.api_enabled is True
        assert config.api_port == 8080

    def test_souls_config(self):
        config = KiwiConfig.from_yaml({
            "souls": {"default": "comedian"}
        })
        assert config.soul_default == "comedian"
