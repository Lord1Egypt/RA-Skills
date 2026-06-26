"""
Tests for OpenMemo ClawHub Skill.
"""

import pytest
from unittest.mock import patch, MagicMock

from openmemo_clawhub_skill.config import SkillConfig, MODE_BOOTSTRAP, MODE_MEMORY
from openmemo_clawhub_skill.detector import AdapterDetector, DetectionResult
from openmemo_clawhub_skill.bootstrap import get_install_guide, setup_wizard, check_environment
from openmemo_clawhub_skill.tools import (
    recall_memory, write_memory, check_task_memory, TOOL_DEFINITIONS,
)
from openmemo_clawhub_skill.rules import get_memory_rules, MEMORY_RULES
from openmemo_clawhub_skill.skill import OpenMemoSkill, SKILL_MANIFEST


class TestConfig:

    def test_defaults(self):
        cfg = SkillConfig()
        assert cfg.endpoint == "http://localhost:8765"
        assert cfg.health_timeout == 5
        assert cfg.request_timeout == 10
        assert cfg.auto_detect is True

    def test_custom_localhost_endpoint(self):
        cfg = SkillConfig(endpoint="http://localhost:9999")
        assert cfg.endpoint == "http://localhost:9999"

    def test_remote_endpoint_rejected(self):
        with pytest.raises(ValueError, match="not localhost"):
            SkillConfig(endpoint="http://example.com:9999")

    def test_remote_endpoint_allowed(self):
        cfg = SkillConfig(endpoint="http://example.com:9999", allow_remote=True)
        assert cfg.endpoint == "http://example.com:9999"

    def test_env_variable(self):
        with patch.dict("os.environ", {"OPENMEMO_ENDPOINT": "http://localhost:1234"}):
            cfg = SkillConfig()
            assert cfg.endpoint == "http://localhost:1234"


class TestDetector:

    def test_detect_not_running(self):
        with patch("openmemo_clawhub_skill.detector.requests.get") as mock_get:
            mock_get.side_effect = ConnectionError("refused")
            detector = AdapterDetector()
            result = detector.detect()
            assert not result.available
            assert not result.server_running

    def test_detect_healthy(self):
        with patch("openmemo_clawhub_skill.detector.requests.get") as mock_get, \
             patch("openmemo_clawhub_skill.detector.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"status": "ok", "service": "openmemo"}
            mock_get.return_value = mock_resp

            mock_post_resp = MagicMock()
            mock_post_resp.status_code = 200
            mock_post.return_value = mock_post_resp

            detector = AdapterDetector()
            result = detector.detect()
            assert result.available
            assert result.server_running
            assert result.adapter_installed

    def test_detect_health_bad_status(self):
        with patch("openmemo_clawhub_skill.detector.requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"status": "error"}
            mock_get.return_value = mock_resp

            detector = AdapterDetector()
            result = detector.detect()
            assert not result.available

    def test_detect_installed_but_not_running(self):
        with patch("openmemo_clawhub_skill.detector.requests.get") as mock_get, \
             patch.object(AdapterDetector, "_check_package_installed", return_value=True):
            mock_get.side_effect = ConnectionError("refused")
            detector = AdapterDetector()
            result = detector.detect()
            assert not result.available
            assert not result.server_running
            assert result.adapter_installed

    def test_detect_4xx_fails(self):
        with patch("openmemo_clawhub_skill.detector.requests.get") as mock_get, \
             patch("openmemo_clawhub_skill.detector.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"status": "ok"}
            mock_get.return_value = mock_resp

            mock_post_resp = MagicMock()
            mock_post_resp.status_code = 404
            mock_post.return_value = mock_post_resp

            detector = AdapterDetector()
            result = detector.detect()
            assert not result.available

    def test_detection_result_summary(self):
        r = DetectionResult(checks=[
            ("health", True, "ok"),
            ("recall", False, "failed"),
        ])
        summary = r.summary()
        assert "health: OK" in summary
        assert "recall: FAIL" in summary


class TestBootstrap:

    def test_install_guide_not_installed(self):
        guide = get_install_guide(adapter_installed=False, server_running=False)
        assert "pip install" in guide
        assert "openmemo serve" in guide

    def test_install_guide_server_not_running(self):
        guide = get_install_guide(adapter_installed=True, server_running=False)
        assert "not running" in guide
        assert "openmemo serve" in guide

    def test_check_environment(self):
        env = check_environment()
        assert "python" in env
        assert "pip" in env
        assert "openmemo_package" in env
        assert "openclaw_package" in env

    def test_setup_wizard(self):
        wizard = setup_wizard()
        assert "Python:" in wizard
        assert "pip:" in wizard
        assert "openmemo:" in wizard


class TestTools:

    def test_tool_definitions_count(self):
        assert len(TOOL_DEFINITIONS) == 3

    def test_tool_names(self):
        names = {t["name"] for t in TOOL_DEFINITIONS}
        assert names == {"recall_memory", "write_memory", "check_task_memory"}

    def test_recall_memory_connection_error(self):
        with patch("openmemo_clawhub_skill.tools.requests.post") as mock_post:
            mock_post.side_effect = ConnectionError("refused")
            result = recall_memory("test query")
            assert "error" in result

    def test_write_memory_connection_error(self):
        with patch("openmemo_clawhub_skill.tools.requests.post") as mock_post:
            mock_post.side_effect = ConnectionError("refused")
            result = write_memory("test content")
            assert "error" in result

    def test_check_task_no_match(self):
        with patch("openmemo_clawhub_skill.tools.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"results": []}
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = check_task_memory("deploy the app")
            assert not result["matched"]
            assert result["recommended_action"] == "proceed"

    def test_check_task_high_confidence_match(self):
        with patch("openmemo_clawhub_skill.tools.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "results": [
                    {"content": "deployed app successfully", "score": 0.95}
                ]
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = check_task_memory("deploy the app")
            assert result["matched"]
            assert result["recommended_action"] == "reuse_or_skip"

    def test_check_task_medium_confidence(self):
        with patch("openmemo_clawhub_skill.tools.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "results": [
                    {"content": "built app pipeline", "score": 0.6}
                ]
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = check_task_memory("deploy the app")
            assert result["matched"]
            assert result["recommended_action"] == "adapt"

    def test_check_task_low_score(self):
        with patch("openmemo_clawhub_skill.tools.requests.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {
                "results": [
                    {"content": "unrelated content", "score": 0.2}
                ]
            }
            mock_resp.raise_for_status = MagicMock()
            mock_post.return_value = mock_resp

            result = check_task_memory("deploy the app")
            assert not result["matched"]
            assert result["recommended_action"] == "proceed"


class TestRules:

    def test_memory_rules_content(self):
        rules = get_memory_rules()
        assert "check_task_memory" in rules
        assert "recall_memory" in rules
        assert "write_memory" in rules

    def test_rules_not_empty(self):
        assert len(MEMORY_RULES) > 100


class TestSkill:

    def test_bootstrap_mode(self):
        with patch.object(AdapterDetector, "detect") as mock_detect:
            mock_detect.return_value = DetectionResult(available=False)
            skill = OpenMemoSkill()
            result = skill.run()
            assert result["mode"] == MODE_BOOTSTRAP
            assert result["status"] == "setup_required"
            assert "pip install" in result["message"]
            assert len(result["tools"]) == 0

    def test_memory_mode(self):
        with patch.object(AdapterDetector, "detect") as mock_detect:
            mock_detect.return_value = DetectionResult(available=True, server_running=True, adapter_installed=True)
            skill = OpenMemoSkill()
            result = skill.run()
            assert result["mode"] == MODE_MEMORY
            assert result["status"] == "ready"
            assert len(result["tools"]) == 3
            assert len(result["rules"]) > 0

    def test_skill_properties(self):
        with patch.object(AdapterDetector, "detect") as mock_detect:
            mock_detect.return_value = DetectionResult(available=True, server_running=True)
            skill = OpenMemoSkill()
            assert skill.is_memory_mode
            assert not skill.is_bootstrap_mode

    def test_recall_in_bootstrap_mode(self):
        with patch.object(AdapterDetector, "detect") as mock_detect:
            mock_detect.return_value = DetectionResult(available=False)
            skill = OpenMemoSkill()
            result = skill.recall("test")
            assert "error" in result

    def test_manifest(self):
        skill = OpenMemoSkill()
        manifest = skill.get_manifest()
        assert manifest["name"] == "openmemo-memory"
        assert manifest["version"] == "1.0.0"
        assert "recall_memory" in manifest["tools"]

    def test_get_setup_wizard(self):
        skill = OpenMemoSkill()
        wizard = skill.get_setup_wizard()
        assert "Python:" in wizard
