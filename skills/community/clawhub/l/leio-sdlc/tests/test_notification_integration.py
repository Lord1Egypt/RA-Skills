import sys
import os
import subprocess
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import orchestrator

def test_notify_channel_integration(monkeypatch):
    monkeypatch.delenv("SDLC_TEST_MODE", raising=False)
    calls = []
    def mock_run(*args, **kwargs):
        calls.append(args[0])
        class DummyRes:
            returncode = 0
            stdout = ""
            stderr = ""
        return DummyRes()

    monkeypatch.setattr(orchestrator.subprocess, 'run', mock_run)
    
    # Test with a simple channel ID
    orchestrator.notify_channel("C123", "", "sdlc_start", {"prd_id": "PRD_081_test.md"})
    
    assert len(calls) == 1
    called_args = calls[0]
    # Verify the command structure for a simple channel ID
    assert called_args[0:5] == ["openclaw", "message", "send", "-t", "C123"]
    assert "🚀 1. [prd-081] SDLC 启动" in called_args[6]

    # Test with a complex routing key
    calls.clear()
    orchestrator.notify_channel("slack:channel:C456", "test message")
    assert len(calls) == 1
    called_args = calls[0]
    assert called_args[0:7] == ["openclaw", "message", "send", "--channel", "slack", "-t", "channel:C456"]
    assert "test message" in called_args[8]
