"""Tests for llm_adapter module - TDD approach."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from scripts.llm_adapter import LLMClient, resolve_config


class TestResolveConfig:
    """Test resolve_config() function."""

    def test_resolve_from_env(self, monkeypatch):
        """Test resolving config from MQS_ prefixed env vars."""
        monkeypatch.setenv("MQS_BASE_URL", "https://api.example.com/v1")
        monkeypatch.setenv("MQS_API_KEY", "test-key-123")
        monkeypatch.setenv("MQS_MODEL", "gpt-4")
        monkeypatch.setenv("MQS_TIMEOUT", "90")

        config = resolve_config()

        assert config["base_url"] == "https://api.example.com/v1"
        assert config["api_key"] == "test-key-123"
        assert config["model"] == "gpt-4"
        assert config["timeout"] == 90

    def test_resolve_from_file(self, monkeypatch, tmp_path):
        """Test resolving config from YAML file."""
        # Clear env vars
        for key in ["MQS_BASE_URL", "MQS_API_KEY", "MQS_MODEL", "MQS_TIMEOUT"]:
            monkeypatch.delenv(key, raising=False)

        # Create temp config file
        config_file = tmp_path / "config.yaml"
        config_data = {
            "base_url": "https://file.example.com/v1",
            "api_key": "file-key-456",
            "model": "gpt-3.5-turbo",
            "timeout": 120
        }
        config_file.write_text(yaml.dump(config_data))

        config = resolve_config(config_path=str(config_file))

        assert config["base_url"] == "https://file.example.com/v1"
        assert config["api_key"] == "file-key-456"
        assert config["model"] == "gpt-3.5-turbo"
        assert config["timeout"] == 120

    def test_resolve_env_overrides_file(self, monkeypatch, tmp_path):
        """Test that env vars override file config."""
        # Set env vars
        monkeypatch.setenv("MQS_BASE_URL", "https://env.example.com/v1")
        monkeypatch.setenv("MQS_API_KEY", "env-key-789")

        # Create config file with different values
        config_file = tmp_path / "config.yaml"
        config_data = {
            "base_url": "https://file.example.com/v1",
            "api_key": "file-key-456",
            "model": "gpt-3.5-turbo",
            "timeout": 120
        }
        config_file.write_text(yaml.dump(config_data))

        config = resolve_config(config_path=str(config_file))

        # Env should win
        assert config["base_url"] == "https://env.example.com/v1"
        assert config["api_key"] == "env-key-789"
        # File should provide missing values
        assert config["model"] == "gpt-3.5-turbo"
        assert config["timeout"] == 120

    def test_resolve_missing_all(self, monkeypatch, tmp_path):
        """Test that missing config raises SystemExit."""
        # Clear all env vars
        for key in ["MQS_BASE_URL", "MQS_API_KEY", "MQS_MODEL", "MQS_TIMEOUT"]:
            monkeypatch.delenv(key, raising=False)

        # Point to non-existent file
        non_existent = tmp_path / "does_not_exist.yaml"

        with pytest.raises(SystemExit) as exc_info:
            resolve_config(config_path=str(non_existent))

        assert exc_info.value.code == 2


class TestLLMClient:
    """Test LLMClient class."""

    def test_chat_success(self, monkeypatch):
        """Test successful chat call returning parsed JSON."""
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"result": "success", "score": 85}'
        mock_client.chat.completions.create.return_value = mock_response

        with patch("scripts.llm_adapter.openai.OpenAI") as mock_openai:
            mock_openai.return_value = mock_client

            client = LLMClient(
                base_url="https://api.example.com/v1",
                api_key="test-key",
                model="gpt-4",
                timeout=60
            )

            messages = [{"role": "user", "content": "Test message"}]
            result = client.chat(messages)

            assert result == {"result": "success", "score": 85}
            mock_client.chat.completions.create.assert_called_once()

    def test_chat_retry_5xx(self, monkeypatch):
        """Test retry logic for 5xx errors."""
        mock_client = MagicMock()

        # First two calls raise 5xx error, third succeeds
        error_response = MagicMock()
        error_response.status_code = 503

        from openai import APIStatusError

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"result": "success"}'

        mock_client.chat.completions.create.side_effect = [
            APIStatusError("Service unavailable", response=error_response, body=None),
            APIStatusError("Service unavailable", response=error_response, body=None),
            mock_response
        ]

        with patch("scripts.llm_adapter.openai.OpenAI") as mock_openai:
            mock_openai.return_value = mock_client

            client = LLMClient(
                base_url="https://api.example.com/v1",
                api_key="test-key",
                model="gpt-4",
                timeout=60
            )

            messages = [{"role": "user", "content": "Test message"}]
            result = client.chat(messages)

            assert result == {"result": "success"}
            assert mock_client.chat.completions.create.call_count == 3

    def test_chat_malformed_json(self, monkeypatch):
        """Test that malformed JSON raises ValueError."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'This is not JSON at all'
        mock_client.chat.completions.create.return_value = mock_response

        with patch("scripts.llm_adapter.openai.OpenAI") as mock_openai:
            mock_openai.return_value = mock_client

            client = LLMClient(
                base_url="https://api.example.com/v1",
                api_key="test-key",
                model="gpt-4",
                timeout=60
            )

            messages = [{"role": "user", "content": "Test message"}]

            with pytest.raises(ValueError, match="Failed to parse LLM response as JSON"):
                client.chat(messages)
