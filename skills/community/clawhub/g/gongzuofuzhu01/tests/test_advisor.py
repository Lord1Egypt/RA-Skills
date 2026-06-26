"""
Tests for the Advisor module.

Uses pytest + tempfile for temporary SQLite databases.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure the *parent* (personal-assistant) is on sys.path so that
# `from scripts.db import Database` and relative imports inside
# `task_manager` resolve correctly.
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.okr import OKRManager
from scripts.advisor import Advisor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    """Create a fresh Database on a temp file."""
    fd, path = tempfile.mkstemp(suffix=".db", prefix="pa_advisor_test_")
    os.close(fd)
    database = Database(db_path=path)
    database.init_db()
    yield database
    database.close()
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def tm(db):
    """TaskManager on temp DB."""
    return TaskManager(db)


@pytest.fixture
def okr(db):
    """OKRManager on temp DB."""
    return OKRManager(db)


@pytest.fixture
def advisor(db, tm, okr):
    """Advisor on temp DB with empty data."""
    return Advisor(db, tm, okr)


@pytest.fixture
def populated(advisor, tm, okr):
    """Populate DB with tasks and OKRs for realistic testing."""
    # --- Tasks ---
    # High priority with deadline
    tm.add("编写核心模块", category="开发", priority=1,
           deadline="2026-05-27T18:00:00", estimated_hours=8)
    tm.add("修复登录 Bug", category="开发", priority=2,
           deadline="2026-05-27T18:00:00", estimated_hours=3)
    tm.add("准备周会 PPT", category="会议", priority=2,
           deadline="2026-05-28T09:00:00", estimated_hours=2)

    # Medium priority
    tm.add("更新 API 文档", category="文档", priority=3,
           estimated_hours=4)
    tm.add("代码审查 PR #42", category="review", priority=3,
           deadline="2026-05-29T12:00:00", estimated_hours=1.5)

    # Low priority — no deadline (postpone candidate)
    tm.add("整理旧笔记", category="个人", priority=4, estimated_hours=1)
    tm.add("研究新技术栈", category="开发", priority=5, estimated_hours=6)

    # Overdue task
    tm.add("逾期未完成的测试", category="测试", priority=1,
           deadline="2026-05-20T18:00:00", estimated_hours=3)

    # Done task (should not appear in active counts)
    done_id = tm.add("已完成的文档", category="文档", priority=3,
                     deadline="2026-05-25T18:00:00", estimated_hours=2)
    tm.set_status(done_id, "done")

    # In-progress task
    prog_id = tm.add("正在进行的重构", category="开发", priority=2,
                     deadline="2026-05-30T18:00:00", estimated_hours=12)
    tm.set_status(prog_id, "in_progress")

    # --- OKRs ---
    oid = okr.add_objective("提升代码质量", "Focus on quality",
                            start_date="2026-05-01", end_date="2026-06-30")
    kr1 = okr.add_key_result(oid, "单元测试覆盖率达到 80%")
    kr2 = okr.add_key_result(oid, "Code Review 通过率 > 95%")

    # Set progress on KR1 (behind schedule)
    okr.update_progress(kr1, 10)  # ~30 days in, 60 total → should be ~50%

    # Link some tasks to OKRs
    okr.link_task(kr2, 5)  # Link "代码审查 PR #42" (task id 5) to kr2

    # Second objective without any tasks
    oid2 = okr.add_objective("学习 Rust", "Learn systems programming",
                             start_date="2026-05-01", end_date="2026-05-28")

    return {
        "task_ids": list(range(1, 11)),  # 10 tasks total (9 active + 1 done)
        "objective_id": oid,
        "objective2_id": oid2,
        "kr1_id": kr1,
        "kr2_id": kr2,
    }


# ---------------------------------------------------------------------------
# 1. analyze_workload
# ---------------------------------------------------------------------------

def test_analyze_workload(populated, advisor):
    """Analyse workload with a realistic mix of tasks and OKRs."""
    result = advisor.analyze_workload()

    # Counts
    assert result["active_tasks"] == 9  # 10 total, 1 done
    assert result["overdue_tasks"] == 1  # "逾期未完成的测试"
    assert result["high_priority_tasks"] == 5  # p1(x2), p2(x3)
    assert result["today_tasks"] >= 1      # includes overdue + no-deadline tasks
    assert result["this_week_tasks"] >= 1
    assert result["estimated_hours_remaining"] > 0

    # Busy categories
    assert "开发" in result["busy_categories"]

    # OKRs with no tasks
    assert len(result["okr_with_no_tasks"]) >= 1  # "学习 Rust" or "单元测试覆盖率..."

    # Suggestions should be non-empty
    assert isinstance(result["suggestions"], list)
    assert len(result["suggestions"]) > 0


def test_analyze_workload_empty(advisor):
    """Analyse workload on an empty database."""
    result = advisor.analyze_workload()

    assert result["active_tasks"] == 0
    assert result["overdue_tasks"] == 0
    assert result["high_priority_tasks"] == 0
    assert result["today_tasks"] == 0
    assert result["this_week_tasks"] == 0
    assert result["estimated_hours_remaining"] == 0
    assert result["busy_categories"] == []
    assert result["okr_with_no_tasks"] == []
    assert result["suggestions"] == []


def test_overdue_count(populated, advisor):
    """Overdue tasks should be counted correctly."""
    result = advisor.analyze_workload()
    assert result["overdue_tasks"] == 1  # Only "逾期未完成的测试" is overdue


# ---------------------------------------------------------------------------
# 2. suggest_delegation
# ---------------------------------------------------------------------------

def test_suggest_delegation(populated, advisor):
    """Delegation candidates found for meeting/doc categories."""
    suggestions = advisor.suggest_delegation()

    assert isinstance(suggestions, list)
    # Should find at least: "准备周会 PPT" (会议), "更新 API 文档" (文档),
    # "代码审查 PR #42" (review), "逾期未完成的测试" (测试)
    delegate_titles = [s["title"] for s in suggestions if s["suggested_action"] == "delegate"]
    postpone_titles = [s["title"] for s in suggestions if s["suggested_action"] == "postpone"]

    assert "准备周会 PPT" in delegate_titles
    assert "更新 API 文档" in delegate_titles
    assert "研究新技术栈" in postpone_titles  # p5, no deadline

    # Each suggestion has required fields
    for s in suggestions:
        assert "task_id" in s
        assert "title" in s
        assert "reason" in s
        assert "suggested_action" in s


def test_suggest_delegation_empty(advisor):
    """Empty DB returns empty delegation list."""
    assert advisor.suggest_delegation() == []


# ---------------------------------------------------------------------------
# 3. suggest_schedule
# ---------------------------------------------------------------------------

def test_suggest_schedule(populated, advisor):
    """Schedule markdown should contain priority sections."""
    md = advisor.suggest_schedule()

    assert "## 📅 日程建议" in md
    assert "### 🔴 高优先级" in md
    assert "### 🟡 中优先级" in md
    assert "### 🟢 低优先级" in md
    assert "总计" in md

    # Should mention high priority tasks
    assert "编写核心模块" in md
    assert "修复登录 Bug" in md

    # Conflict warning: need 3+ high-prio tasks on same day.
    # We have 2 on 2026-05-27 (p1 + p2) — below threshold, so no warning.
    # If we had 3+, the warning would appear.


def test_suggest_schedule_empty(advisor):
    """Empty DB produces valid markdown with no items."""
    md = advisor.suggest_schedule()
    assert "无高优先级任务" in md
    assert "无中优先级任务" in md
    assert "无低优先级任务" in md


# ---------------------------------------------------------------------------
# 4. okr_health_check
# ---------------------------------------------------------------------------

def test_okr_health_check(populated, advisor):
    """Health check should find OKR progress issues and untethered OKRs."""
    result = advisor.okr_health_check()

    assert "progress_behind" in result
    assert "no_tasks" in result
    assert "expiring_soon" in result

    # "单元测试覆盖率达到 80%" at 10% should be behind
    assert len(result["progress_behind"]) >= 1
    behind_titles = [p["title"] for p in result["progress_behind"]]
    assert "单元测试覆盖率达到 80%" in behind_titles

    # "学习 Rust" objective and its KR(s) have no tasks
    assert len(result["no_tasks"]) >= 1
    no_task_titles = [n["title"] for n in result["no_tasks"]]
    assert "学习 Rust" in no_task_titles


def test_okr_health_progress_behind(populated, advisor):
    """KR with 10% progress at ~50% elapsed time should be flagged."""
    result = advisor.okr_health_check()

    behind = [p for p in result["progress_behind"]
              if p["title"] == "单元测试覆盖率达到 80%"]

    assert len(behind) == 1
    kr = behind[0]
    assert kr["current_progress"] == 10
    assert kr["expected_progress"] > 30  # ~40-50% expected
    assert kr["gap"] > 0


def test_okr_health_check_empty(advisor):
    """Empty DB returns empty health check."""
    result = advisor.okr_health_check()
    assert result["progress_behind"] == []
    assert result["no_tasks"] == []
    assert result["expiring_soon"] == []


# ---------------------------------------------------------------------------
# 5. get_context_for_llm
# ---------------------------------------------------------------------------

def test_get_context_for_llm(populated, advisor):
    """Context text should aggregate all analysis sections."""
    text = advisor.get_context_for_llm()

    assert "PERSONAL ASSISTANT — WORKLOAD CONTEXT" in text
    assert "## 工作负载总览" in text
    assert "## 系统建议 (规则引擎)" in text
    assert "## 委派 / 延后建议" in text
    assert "## OKR 健康检查" in text
    assert "END OF CONTEXT" in text

    # Should contain actual data
    assert "活跃任务:" in text
    assert "逾期任务:" in text


def test_get_context_for_llm_empty(advisor):
    """Empty DB produces valid context text."""
    text = advisor.get_context_for_llm()
    assert "PERSONAL ASSISTANT — WORKLOAD CONTEXT" in text
    assert "活跃任务: 0" in text
    assert "无" in text  # Various "无" indicators
