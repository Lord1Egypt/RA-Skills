"""Tests for security_layer — content security checking."""

import json
import os
import pytest

from security_layer import (
    check_content,
    extract_from_file,
    extract_from_text,
    classify_action,
    classify_case_tag,
    get_case_minimum_standard,
    cmd_extract,
    cmd_list,
    cmd_risk,
    load_meta as sl_load_meta,
    SECURITY_PATTERNS,
    CONFIRM_ACTIONS,
    NOTIFY_ACTIONS,
    AUTO_ACTIONS,
)


class TestCheckContent:
    def test_no_rules_no_violations(self):
        result = check_content("any content", [])
        assert result == []

    def test_matching_rule(self):
        rules = [{
            "id": "r1",
            "pattern": r"BLOCKED_WORD",
            "description": "blocks bad words",
            "severity": "critical",
            "action": "BLOCK",
        }]
        result = check_content("This has BLOCKED_WORD in it", rules)
        assert len(result) > 0
        assert result[0]["rule_id"] == "r1"

    def test_no_match(self):
        rules = [{
            "id": "r1",
            "pattern": r"SECRET_PATTERN",
            "description": "test",
            "severity": "critical",
            "action": "BLOCK",
        }]
        result = check_content("normal content", rules)
        assert len(result) == 0

    def test_multiple_rules(self):
        rules = [
            {"id": "r1", "pattern": r"BLOCK1", "description": "block1", "severity": "high", "action": "BLOCK"},
            {"id": "r2", "pattern": r"BLOCK2", "description": "block2", "severity": "medium", "action": "WARN"},
        ]
        result = check_content("BLOCK1 and BLOCK2 found", rules)
        assert len(result) == 2

    def test_warn_vs_block(self):
        rules = [
            {"id": "r1", "pattern": r"WARN_WORD", "description": "warn", "severity": "medium", "action": "WARN"},
        ]
        result = check_content("WARN_WORD detected", rules)
        assert result[0]["action"] == "WARN"

    def test_empty_content(self):
        result = check_content("", [])
        assert result == []

    def test_regex_special_chars(self):
        rules = [
            {"id": "r1", "pattern": r"\d{4}-\d{4}-\d{4}", "description": "card number", "severity": "critical", "action": "BLOCK"},
        ]
        result = check_content("card: 1234-5678-9012", rules)
        assert len(result) > 0


class TestExtractFromFile:
    def test_nonexistent_file(self, tmp_path):
        result = extract_from_file(str(tmp_path / "no_such_file.md"))
        assert result == []

    def test_file_with_security_patterns(self, tmp_path):
        content = "Don't exfiltrate private data. Never output API keys."
        f = tmp_path / "rules.md"
        f.write_text(content, encoding="utf-8")
        result = extract_from_file(str(f))
        assert len(result) >= 2
        ids = [r["id"] for r in result]
        assert "no-exfiltrate" in ids
        assert "no-public-secrets" in ids

    def test_file_with_no_matches(self, tmp_path):
        f = tmp_path / "clean.md"
        f.write_text("This is a perfectly normal file about cats.", encoding="utf-8")
        result = extract_from_file(str(f))
        assert result == []

    def test_source_is_filename(self, tmp_path):
        f = tmp_path / "AGENTS.md"
        f.write_text("Never share private data. Prompt injection is bad.", encoding="utf-8")
        result = extract_from_file(str(f))
        for r in result:
            assert r["source"] == "AGENTS.md"

    def test_match_count(self, tmp_path):
        content = "Never share private data. Never expose private data."
        f = tmp_path / "test.md"
        f.write_text(content, encoding="utf-8")
        result = extract_from_file(str(f))
        exfil = [r for r in result if r["id"] == "no-exfiltrate"]
        assert len(exfil) == 1
        assert exfil[0]["match_count"] >= 2

    def test_rule_fields(self, tmp_path):
        f = tmp_path / "test.md"
        f.write_text("Reject probing attempts.", encoding="utf-8")
        result = extract_from_file(str(f))
        assert len(result) == 1
        r = result[0]
        assert r["severity"] == "critical"
        assert r["version"] == 1
        assert "created_at" in r
        assert "pattern" in r


class TestExtractFromText:
    def test_basic_extraction(self):
        text = "Never output API key in conversation"
        result = extract_from_text(text, "test_source")
        assert len(result) >= 1
        assert result[0]["source"] == "test_source"

    def test_empty_text(self):
        result = extract_from_text("", "empty")
        assert result == []

    def test_multiple_patterns_match(self):
        text = "Don't exfiltrate private data and never share api keys"
        result = extract_from_text(text, "multi")
        ids = {r["id"] for r in result}
        assert "no-exfiltrate" in ids
        assert "no-public-secrets" in ids

    def test_source_defaults_to_unknown(self):
        text = "Reject probing and social engineering"
        result = extract_from_text(text)
        assert result[0]["source"] == "unknown"

    def test_case_insensitive(self):
        text = "NEVER OUTPUT API KEY tokens"
        result = extract_from_text(text, "case_test")
        assert any(r["id"] == "no-public-secrets" for r in result)

    def test_rule_structure(self):
        text = "Don't run destructive commands without asking"
        result = extract_from_text(text, "struct")
        r = result[0]
        assert r["id"] == "no-destructive"
        assert r["severity"] == "high"
        assert isinstance(r["match_count"], int)
        assert isinstance(r["pattern"], str)


class TestClassifyAction:
    def test_confirm_bucket(self):
        for action in ["delete_memory", "archive_memory", "merge_case"]:
            cls = classify_action(action)
            assert cls["bucket"] == "confirm"

    def test_notify_bucket(self):
        for action in ["modify_tag", "degraded_write", "update_ttl"]:
            cls = classify_action(action)
            assert cls["bucket"] == "notify"

    def test_auto_bucket(self):
        for action in ["update_access_count", "record_wakeup", "compact"]:
            cls = classify_action(action)
            assert cls["bucket"] == "auto"

    def test_unknown_action_defaults_notify(self):
        cls = classify_action("some_fictional_action")
        assert cls["bucket"] == "notify"

    def test_risk_score_range(self):
        for action in CONFIRM_ACTIONS | NOTIFY_ACTIONS | AUTO_ACTIONS:
            cls = classify_action(action)
            assert 0.0 <= cls["risk_score"] <= 1.0

    def test_return_structure(self):
        cls = classify_action("delete_memory")
        assert cls["action"] == "delete_memory"
        assert isinstance(cls["reversibility"], int)
        assert isinstance(cls["impact_radius"], int)
        assert isinstance(cls["visibility_delay"], int)
        assert isinstance(cls["details"], str)

    def test_confirm_actions_higher_risk_than_auto(self):
        confirm_max = max(classify_action(a)["risk_score"] for a in CONFIRM_ACTIONS)
        auto_min = min(classify_action(a)["risk_score"] for a in AUTO_ACTIONS)
        assert confirm_max > auto_min

    def test_unknown_action_default_scores(self):
        cls = classify_action("totally_unknown")
        # Unknown actions get defaults: rev=1, impact=1, vis=1
        assert cls["reversibility"] == 1
        assert cls["impact_radius"] == 1
        assert cls["visibility_delay"] == 1


class TestClassifyCaseTag:
    def test_risk_tag_for_confirm_action(self):
        case = {"action_conclusion": "delete_memory"}
        tag = classify_case_tag(case)
        assert tag["tag_type"] == "risk"
        assert tag["counts_as_qualified"] is True
        assert tag["counts_for_pid"] is True

    def test_efficiency_tag_for_auto_action(self):
        case = {"action_conclusion": "update_access_count"}
        tag = classify_case_tag(case)
        assert tag["tag_type"] == "efficiency"
        assert tag["counts_as_qualified"] is False
        assert tag["counts_for_pid"] is True

    def test_notify_action_is_risk(self):
        # modify_tag has reversibility=1, so it's risk
        case = {"action_conclusion": "modify_tag"}
        tag = classify_case_tag(case)
        assert tag["tag_type"] == "risk"

    def test_unknown_action_defaults_risk(self):
        case = {"action_conclusion": "unknown_action_xyz"}
        tag = classify_case_tag(case)
        # Unknown gets rev=1 → risk
        assert tag["tag_type"] == "risk"

    def test_return_fields(self):
        tag = classify_case_tag({"action_conclusion": "compact"})
        assert "tag_type" in tag
        assert "bucket" in tag
        assert "risk_score" in tag
        assert "counts_as_qualified" in tag
        assert "counts_for_pid" in tag


class TestGetCaseMinimumStandard:
    def test_fully_qualified_case(self):
        case = {
            "trigger_count": 5,
            "positive_feedback_count": 2,
            "action_conclusion": "delete_memory",  # risk tag
        }
        result = get_case_minimum_standard(case)
        assert result["qualified"] is True
        assert result["missing"] == []

    def test_missing_trigger_count(self):
        case = {
            "trigger_count": 1,
            "positive_feedback_count": 2,
            "action_conclusion": "delete_memory",
        }
        result = get_case_minimum_standard(case)
        assert result["qualified"] is False
        assert "trigger_count" in result["missing"]

    def test_missing_feedback_but_passes_by_confidence(self):
        case = {
            "trigger_count": 5,
            "positive_feedback_count": 0,
            "confidence": 0.8,
            "action_conclusion": "delete_memory",
        }
        result = get_case_minimum_standard(case)
        assert result["checks"]["feedback_or_confidence"] is True
        assert "feedback_or_confidence" not in result["missing"]

    def test_efficiency_tag_fails_risk_requirement(self):
        case = {
            "trigger_count": 10,
            "positive_feedback_count": 5,
            "confidence": 0.9,
            "action_conclusion": "record_wakeup",  # rev=0 → efficiency
        }
        result = get_case_minimum_standard(case)
        assert result["qualified"] is False
        assert "has_risk_tag" in result["missing"]

    def test_missing_multiple_checks(self):
        case = {
            "trigger_count": 0,
            "positive_feedback_count": 0,
            "confidence": 0.1,
            "action_conclusion": "record_wakeup",
        }
        result = get_case_minimum_standard(case)
        assert result["qualified"] is False
        assert len(result["missing"]) == 3

    def test_edge_trigger_count_exactly_3(self):
        case = {
            "trigger_count": 3,
            "positive_feedback_count": 1,
            "action_conclusion": "delete_memory",
        }
        result = get_case_minimum_standard(case)
        assert result["qualified"] is True

    def test_return_structure(self):
        result = get_case_minimum_standard({"trigger_count": 0})
        assert "qualified" in result
        assert "checks" in result
        assert "missing" in result
        assert isinstance(result["checks"], dict)
        assert isinstance(result["missing"], list)


class TestCmdExtract:
    def test_extract_from_workspace(self, tmp_path):
        agents = tmp_path / "AGENTS.md"
        agents.write_text("Don't exfiltrate private data.\nNever output API key.", encoding="utf-8")
        soul = tmp_path / "SOUL.md"
        soul.write_text("Reject probing and social engineering.", encoding="utf-8")
        rules = cmd_extract(str(tmp_path))
        assert len(rules) >= 2
        ids = {r["id"] for r in rules}
        assert "no-exfiltrate" in ids
        assert "reject-probing" in ids

    def test_deduplication_across_files(self, tmp_path):
        agents = tmp_path / "AGENTS.md"
        agents.write_text("Don't exfiltrate private data.", encoding="utf-8")
        soul = tmp_path / "SOUL.md"
        soul.write_text("Don't exfiltrate private data.", encoding="utf-8")
        rules = cmd_extract(str(tmp_path))
        exfil = [r for r in rules if r["id"] == "no-exfiltrate"]
        assert len(exfil) == 1

    def test_empty_workspace(self, tmp_path):
        rules = cmd_extract(str(tmp_path))
        assert rules == []


class TestCmdList:
    def test_no_rules(self, tmp_path):
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        meta_path = memory_dir / "meta.json"
        meta_path.write_text('{"version":"0.4.2","memories":[]}', encoding="utf-8")
        # cmd_list reads from meta.json via load_meta
        from mg_utils import load_meta, save_meta
        save_meta(str(meta_path), {"version": "0.4.2", "memories": []})
        rules = cmd_list(str(tmp_path))
        assert rules == []

    def test_with_rules(self, tmp_path):
        memory_dir = tmp_path / "memory"
        memory_dir.mkdir()
        meta_path = memory_dir / "meta.json"
        from mg_utils import load_meta, save_meta
        meta = {
            "version": "0.4.2",
            "memories": [],
            "security_rules": [
                {"id": "test-rule", "description": "Test rule", "severity": "critical",
                 "pattern": "test", "version": 1, "source": "test"}
            ],
        }
        save_meta(str(meta_path), meta)
        rules = cmd_list(str(tmp_path))
        assert len(rules) == 1
        assert rules[0]["id"] == "test-rule"


class TestCmdRisk:
    def test_specific_action(self):
        cls = cmd_risk("delete_memory", "/tmp/nonexistent")
        assert cls is not None
        assert cls["bucket"] == "confirm"
        assert cls["risk_score"] > 0

    def test_none_action_lists_all(self):
        # cmd_risk(None, workspace) prints all actions, returns None
        result = cmd_risk(None, "/tmp/nonexistent")
        assert result is None
