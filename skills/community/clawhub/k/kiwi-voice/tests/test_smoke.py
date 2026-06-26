"""Minimal smoke tests for Kiwi Voice modules."""

import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_import_utils():
    from kiwi.utils import kiwi_log, setup_crash_protection
    assert callable(kiwi_log)
    assert callable(setup_crash_protection)


def test_import_event_bus():
    from kiwi.event_bus import EventBus, EventType
    assert EventBus is not None
    assert hasattr(EventType, "WAKE_WORD_DETECTED") or len(EventType.__members__) > 0


def test_event_bus_lifecycle():
    from kiwi.event_bus import EventBus, EventType
    bus = EventBus()
    bus.start()
    received = []
    bus.subscribe(EventType.WAKE_WORD_DETECTED, lambda event: received.append(event))
    bus.publish(EventType.WAKE_WORD_DETECTED, {"text": "киви"}, source="test", wait=True)
    assert len(received) == 1
    assert received[0].payload["text"] == "киви"
    bus.stop()


def test_import_tts_client():
    from kiwi.tts.runpod import TTSClient, TTSConfig
    assert TTSClient is not None
    assert TTSConfig is not None


def test_import_elevenlabs_tts():
    from kiwi.tts.elevenlabs import ElevenLabsTTSClient, ElevenLabsTTSConfig
    assert ElevenLabsTTSClient is not None


def test_import_qwen_local_tts():
    from kiwi.tts.qwen_local import LocalQwenTTSConfig
    from kiwi.tts.base import normalize_voice as normalize_qwen_voice, normalize_model_size as normalize_qwen_model_size
    assert normalize_qwen_voice("ono_anna") == "Ono_Anna"
    assert normalize_qwen_model_size("0.6") == "0.6B"
    assert normalize_qwen_model_size("1.7") == "1.7B"


def test_import_speaker_manager():
    from kiwi.speaker_manager import SpeakerManager, VoicePriority
    assert VoicePriority.OWNER < VoicePriority.FRIEND < VoicePriority.GUEST < VoicePriority.BLOCKED


def test_import_voice_security():
    from kiwi.voice_security import VoiceSecurity
    assert VoiceSecurity is not None


def test_kiwi_config_parsing():
    from kiwi.config_loader import KiwiConfig
    config = KiwiConfig()
    assert config.wake_word_keyword == "киви"
    assert config.tts_provider in ("qwen3", "piper", "elevenlabs")


def test_kiwi_config_from_yaml():
    from kiwi.config_loader import KiwiConfig
    yaml_config = {
        "stt": {"model": "small", "device": "cpu"},
        "tts": {"provider": "piper", "voice": "Ono_Anna"},
        "wake_word": {"keyword": "алиса"},
    }
    config = KiwiConfig.from_yaml(yaml_config)
    assert config.stt_model == "small"
    assert config.tts_provider == "piper"
    assert config.wake_word_keyword == "алиса"
