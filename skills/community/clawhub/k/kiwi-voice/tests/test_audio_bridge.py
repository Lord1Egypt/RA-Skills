"""Tests for WebSocket audio bridge."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np


def test_import_audio_bridge():
    from kiwi.api.audio_bridge import WebAudioBridge, WebAudioClient
    assert WebAudioBridge is not None
    assert WebAudioClient is not None


def test_web_audio_client_init():
    from kiwi.api.audio_bridge import WebAudioClient

    class FakeWs:
        closed = False
    ws = FakeWs()
    client = WebAudioClient(ws, "test-123", sample_rate=16000)
    assert client.client_id == "test-123"
    assert client.sample_rate == 16000
    assert client.is_active is True
    assert client.is_muted is False
    assert client.is_speaking is False
    assert client.speech_buffer == []
    assert client.silence_counter == 0


def test_web_audio_client_repr():
    from kiwi.api.audio_bridge import WebAudioClient

    class FakeWs:
        closed = False
    ws = FakeWs()
    client = WebAudioClient(ws, "abcdefgh-1234")
    assert "abcdefgh" in repr(client)


def test_silence_detection_constants():
    from kiwi.api.audio_bridge import (
        _SILENCE_THRESHOLD,
        _SILENCE_CHUNKS_TO_END,
        _MIN_SPEECH_CHUNKS,
        _MAX_SPEECH_SECONDS,
    )
    assert 0 < _SILENCE_THRESHOLD < 1.0
    assert _SILENCE_CHUNKS_TO_END > 0
    assert _MIN_SPEECH_CHUNKS > 0
    assert _MAX_SPEECH_SECONDS > 0


def test_bridge_has_required_methods():
    from kiwi.api.audio_bridge import WebAudioBridge
    required = [
        "handle_audio_ws",
        "send_tts_audio",
        "send_control",
        "send_control_sync",
        "has_clients",
    ]
    for method in required:
        assert hasattr(WebAudioBridge, method), f"Missing method: {method}"


def test_config_has_web_audio_fields():
    from kiwi.config_loader import KiwiConfig
    config = KiwiConfig()
    assert hasattr(config, "web_audio_enabled")
    assert hasattr(config, "web_audio_sample_rate")
    assert hasattr(config, "web_audio_max_clients")
    assert config.web_audio_enabled is True
    assert config.web_audio_sample_rate == 16000
    assert config.web_audio_max_clients == 3


def test_config_web_audio_from_yaml():
    from kiwi.config_loader import KiwiConfig
    cfg = KiwiConfig.from_yaml({
        "web_audio": {
            "enabled": False,
            "sample_rate": 44100,
            "max_clients": 5,
        }
    })
    assert cfg.web_audio_enabled is False
    assert cfg.web_audio_sample_rate == 44100
    assert cfg.web_audio_max_clients == 5


def test_event_types_include_web_audio():
    from kiwi.event_bus import EventType
    assert hasattr(EventType, "WEB_CLIENT_CONNECTED")
    assert hasattr(EventType, "WEB_CLIENT_DISCONNECTED")


def test_listener_has_submit_external_audio():
    pytest = __import__("pytest")
    try:
        from kiwi.listener import KiwiListener
    except ImportError:
        pytest.skip("sounddevice not available in CI")
    assert hasattr(KiwiListener, "submit_external_audio")
