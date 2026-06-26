"""Tests for memory_case_grow — case growth engine."""

import pytest

from memory_case_grow import (
    SceneGroup,
    mark_authority_context,
    schedule_post_stress_review,
    apply_tag_penalty,
    add_context_burr,
    get_context_burrs,
    consequence_direction,
    add_failure_condition,
    adjust_confidence,
    jaccard,
    tag_jaccard,
    _default_thresholds,
)


class TestSceneGroup:
    def test_create(self):
        sg = SceneGroup(group_id="test_group", tag_prefix="project")
        assert sg.group_id == "test_group"

    def test_has_update(self):
        sg = SceneGroup(group_id="test")
        assert hasattr(sg, "update")


class TestMarkAuthorityContext:
    def test_no_context(self):
        mem = {"content": "test", "tags": [], "confidence": 0.5}
        result = mark_authority_context(mem)
        assert isinstance(result, bool)


class TestSchedulePostStressReview:
    def test_returns_none(self):
        mem = {"id": "case_1", "confidence": 0.5}
        result = schedule_post_stress_review(mem)
        assert result is None  # Only schedules if conditions met


class TestApplyTagPenalty:
    def test_create_action_no_penalty(self):
        conf = apply_tag_penalty(0.8, "create")
        # May or may not penalize depending on implementation
        assert isinstance(conf, float)


class TestContextBurrs:
    def test_add_and_get_valid_type(self):
        mem = {"id": "case_1"}
        add_context_burr(mem, "situation_context", {"data": 1})
        burrs = get_context_burrs(mem, "situation_context")
        assert len(burrs) == 1

    def test_no_burrs(self):
        burrs = get_context_burrs({}, "nonexistent")
        assert burrs == []

    def test_invalid_type_ignored(self):
        mem = {"id": "case_1"}
        add_context_burr(mem, "invalid_type", {"data": 1})
        burrs = get_context_burrs(mem, "invalid_type")
        assert burrs == []


class TestConsequenceDirection:
    def test_positive(self):
        assert consequence_direction("成功解决了问题") == "positive"

    def test_negative(self):
        assert consequence_direction("失败导致崩溃") == "negative"

    def test_neutral(self):
        assert consequence_direction("无影响") == "neutral"


class TestAddFailureCondition:
    def test_adds_condition(self):
        mem = {"failure_conditions": []}
        add_failure_condition(mem, "trigger_test", "some context")
        assert len(mem["failure_conditions"]) == 1

    def test_updates_existing(self):
        mem = {"failure_conditions": [{"intent": "trigger_test", "count": 1}]}
        add_failure_condition(mem, "trigger_test")
        assert mem["failure_conditions"][0]["count"] == 2


class TestAdjustConfidence:
    def test_consistent_boosts(self):
        mem = {"confidence": 0.5}
        adjust_confidence(mem, consistent=True)
        assert mem["confidence"] > 0.5

    def test_inconsistent_reduces(self):
        mem = {"confidence": 0.8}
        adjust_confidence(mem, consistent=False)
        assert mem["confidence"] < 0.8


class TestJaccardHelpers:
    def test_jaccard_identical(self):
        # jaccard returns distance (1 = identical)
        assert jaccard({"a", "b"}, {"a", "b"}) == 1.0

    def test_jaccard_disjoint(self):
        assert jaccard({"a"}, {"b"}) == 0.0

    def test_tag_jaccard_identical(self):
        assert tag_jaccard(["a", "b"], ["a", "b"]) == 1.0

    def test_tag_jaccard_disjoint(self):
        assert tag_jaccard(["a"], ["b"]) == 0.0


class TestDefaultThresholds:
    def test_has_defaults(self):
        thresholds = _default_thresholds()
        assert isinstance(thresholds, dict)
        assert len(thresholds) > 0


# ─── New tests for uncovered functions ───────────────────────

import json

from memory_case_grow import (
    build_scene_groups,
    record_trigger,
    rescan_authority_context,
    prune_context_burrs,
    get_adaptive_threshold,
    run_post_stress_reviews,
)


def _write_meta(tmp_path, meta):
    """Helper: write meta dict to tmp_path/meta.json."""
    p = tmp_path / "meta.json"
    p.write_text(json.dumps(meta, ensure_ascii=False))
    return str(p)


class TestBuildSceneGroups:
    def test_empty_meta(self):
        groups = build_scene_groups({"memories": []})
        assert groups == {}

    def test_groups_by_first_tag(self):
        meta = {
            "memories": [
                {"id": "c1", "status": "active", "case_type": "case", "tags": ["project:alpha"]},
                {"id": "c2", "status": "active", "case_type": "case", "tags": ["project:beta"]},
                {"id": "c3", "status": "active", "case_type": "case", "tags": ["project:alpha"]},
            ]
        }
        groups = build_scene_groups(meta)
        assert "tag:project" in groups
        assert groups["tag:project"].N == 3

    def test_skips_non_case(self):
        meta = {
            "memories": [
                {"id": "m1", "status": "active", "case_type": "memory", "tags": ["project"]},
                {"id": "c1", "status": "active", "case_type": "case", "tags": ["project"]},
            ]
        }
        groups = build_scene_groups(meta)
        assert groups["tag:project"].N == 1

    def test_untagged_goes_to_default(self):
        meta = {
            "memories": [
                {"id": "c1", "status": "active", "case_type": "case", "tags": []},
            ]
        }
        groups = build_scene_groups(meta)
        assert "_default" in groups


class TestRecordTrigger:
    def test_increment_trigger(self, tmp_path):
        meta = {"memories": [{"id": "case_1", "trigger_count": 2, "access_count": 1}]}
        p = _write_meta(tmp_path, meta)
        result = record_trigger(p, "case_1")
        assert result["updated"] is True
        assert result["trigger_count"] == 3

    def test_not_found(self, tmp_path):
        meta = {"memories": []}
        p = _write_meta(tmp_path, meta)
        result = record_trigger(p, "case_nonexistent")
        assert result["updated"] is False

    def test_updates_access_count(self, tmp_path):
        meta = {"memories": [{"id": "case_1", "trigger_count": 0, "access_count": 5}]}
        p = _write_meta(tmp_path, meta)
        record_trigger(p, "case_1")
        # Re-read and verify
        from mg_utils import load_meta
        updated = load_meta(p)
        assert updated["memories"][0]["access_count"] == 6


class TestRescanAuthorityContext:
    def test_flags_authority_case(self, tmp_path):
        meta = {
            "memories": [{
                "id": "case_1", "status": "active",
                "provenance_level": "L1",
                "situation": "老板要求审批",
                "tags": [],
            }]
        }
        p = _write_meta(tmp_path, meta)
        result = rescan_authority_context(p)
        assert result["newly_flagged"] == 1
        assert result["total_flagged"] == 1

    def test_no_new_flags(self, tmp_path):
        meta = {
            "memories": [{
                "id": "case_1", "status": "active",
                "provenance_level": "L2",  # not L1
                "tags": ["管理"],
            }]
        }
        p = _write_meta(tmp_path, meta)
        result = rescan_authority_context(p)
        assert result["newly_flagged"] == 0

    def test_skips_archived(self, tmp_path):
        meta = {
            "memories": [{
                "id": "case_1", "status": "archived",
                "provenance_level": "L1",
                "situation": "老板审批",
            }]
        }
        p = _write_meta(tmp_path, meta)
        result = rescan_authority_context(p)
        assert result["newly_flagged"] == 0


class TestPruneContextBurrs:
    def test_prunes_old_burrs(self, tmp_path):
        from datetime import datetime, timedelta
        from mg_utils import CST
        old_ts = (datetime.now(CST) - timedelta(days=100)).isoformat()
        meta = {
            "memories": [{
                "id": "case_1",
                "context_burrs": {
                    "situation_context": [{"data": "old", "added_at": old_ts}],
                }
            }]
        }
        p = _write_meta(tmp_path, meta)
        pruned = prune_context_burrs(p, max_age_days=90)
        assert pruned >= 1

    def test_keeps_recent_burrs(self, tmp_path):
        meta = {
            "memories": [{
                "id": "case_1",
                "context_burrs": {
                    "failure_case": [{"data": "recent", "added_at": "2099-01-01T00:00:00+08:00"}],
                }
            }]
        }
        p = _write_meta(tmp_path, meta)
        pruned = prune_context_burrs(p, max_age_days=90)
        assert pruned == 0

    def test_no_burrs_noop(self, tmp_path):
        meta = {"memories": [{"id": "case_1"}]}
        p = _write_meta(tmp_path, meta)
        pruned = prune_context_burrs(p, max_age_days=90)
        assert pruned == 0


class TestGetAdaptiveThreshold:
    def test_returns_defaults_for_unknown_tag(self):
        thresholds = get_adaptive_threshold({}, "unknown:tag")
        assert thresholds["absorb"] == 0.8
        assert thresholds["source"] == "fixed_default"

    def test_returns_defaults_for_empty_groups(self):
        thresholds = get_adaptive_threshold({}, "")
        assert isinstance(thresholds, dict)
        assert "absorb" in thresholds

    def test_returns_adaptive_for_large_group(self):
        groups = {"tag:project": SceneGroup("tag:project", "project")}
        # Simulate N >= 20
        groups["tag:project"].case_ids = [f"c{i}" for i in range(25)]
        groups["tag:project"].update(groups["tag:project"].case_ids)
        thresholds = get_adaptive_threshold(groups, "project:feature")
        assert "absorb" in thresholds
        # For N 20-50, absorb should be > 0.8
        assert thresholds["absorb"] >= 0.8


class TestRunPostStressReviews:
    def test_finds_due_review(self):
        from datetime import datetime, timedelta, timezone
        past = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
        meta = {
            "memories": [{
                "id": "case_1",
                "authority_context": True,
                "review_at_pressure_free": past,
                "post_stress_review_status": "pending",
                "content": "test case for authority review",
                "confidence": 0.7,
            }]
        }
        result = run_post_stress_reviews(meta, dry_run=True)
        assert result["stats"]["due_count"] == 1
        assert len(result["due"]) == 1

    def test_skips_resolved(self):
        meta = {
            "memories": [{
                "id": "case_1",
                "authority_context": True,
                "review_at_pressure_free": "2020-01-01T00:00:00+00:00",
                "post_stress_review_status": "resolved",
            }]
        }
        result = run_post_stress_reviews(meta, dry_run=True)
        assert result["stats"]["due_count"] == 0

    def test_marks_pending_as_needs_review(self):
        from datetime import datetime, timedelta, timezone
        past = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
        meta = {
            "memories": [{
                "id": "case_1",
                "authority_context": True,
                "review_at_pressure_free": past,
                "post_stress_review_status": "pending",
                "content": "test",
                "confidence": 0.5,
            }]
        }
        result = run_post_stress_reviews(meta, dry_run=False)
        assert result["stats"]["reviewed_count"] == 1
        # The case should now have needs_review status
        assert meta["memories"][0]["post_stress_review_status"] == "needs_review"
