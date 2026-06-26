"""
Tests for report.py — ReportGenerator monthly and semi-annual reports.

Uses temporary SQLite databases via pytest fixtures. No side effects.
"""

import tempfile
import sys
from pathlib import Path

import pytest

# Ensure the *parent* (personal-assistant) is on sys.path so that
# `from scripts.db import Database` and relative imports resolve correctly.
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.task_manager import TaskManager
from scripts.progress import ProgressTracker
from scripts.okr import OKRManager
from scripts.report import ReportGenerator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db():
    """Fresh temporary database initialised with schema.sql."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()

    database = Database(db_path=tmp.name)
    import scripts.db as db_mod

    db_mod.SCHEMA_FILE = (
        Path(__file__).resolve().parent.parent / "scripts" / "schema.sql"
    )
    database.init_db()
    yield database
    try:
        Path(tmp.name).unlink()
    except FileNotFoundError:
        pass


@pytest.fixture
def tm(db):
    """TaskManager wired to the test database."""
    return TaskManager(db)


@pytest.fixture
def pt(db, tm):
    """ProgressTracker wired to the test database."""
    return ProgressTracker(db, tm)


@pytest.fixture
def okr(db):
    """OKRManager wired to the test database."""
    return OKRManager(db)


@pytest.fixture
def rg(db, tm, pt, okr):
    """ReportGenerator with all dependencies."""
    return ReportGenerator(db, tm, pt, okr)


@pytest.fixture
def populated_db(tm, pt, okr, db):
    """Populate the database with realistic test data for report generation.

    Creates:
        - Completed tasks (3) set to 'done' this month
        - In-progress tasks (2)
        - New tasks created this month (4)
        - Tasks with different categories
        - Progress logs with hours
        - OKR items
    """
    from datetime import date
    from calendar import monthrange

    today = date.today()
    year = today.year
    month = today.month
    _, last_day = monthrange(year, month)

    month_str = f"{year}-{month:02d}"
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    # --- Completed tasks (done this month) ---
    tid1 = tm.add(
        "完成项目 A 开发",
        category="开发",
        priority=2,
        estimated_hours=40,
        actual_hours=38.5,
    )
    tm.set_status(tid1, "done")
    # Manually set updated_at to this month (since set_status sets it to now)
    db.execute(
        "UPDATE tasks SET updated_at = ? WHERE id = ?",
        (f"{month_str}-15T18:00:00", tid1),
    )

    tid2 = tm.add(
        "撰写技术文档",
        category="文档",
        priority=3,
        estimated_hours=10,
        actual_hours=12,
    )
    tm.set_status(tid2, "done")
    db.execute(
        "UPDATE tasks SET updated_at = ? WHERE id = ?",
        (f"{month_str}-10T14:00:00", tid2),
    )

    tid3 = tm.add(
        "修复登录 Bug",
        category="开发",
        priority=1,
        estimated_hours=4,
        actual_hours=3,
    )
    tm.set_status(tid3, "done")
    db.execute(
        "UPDATE tasks SET updated_at = ? WHERE id = ?",
        (f"{month_str}-05T09:00:00", tid3),
    )

    # --- In-progress tasks ---
    tid4 = tm.add(
        "重构用户模块",
        category="开发",
        priority=2,
        deadline=f"{next_year}-{next_month:02d}-20T18:00:00",
    )
    tm.set_status(tid4, "in_progress")

    tid5 = tm.add(
        "准备 Q2 汇报 PPT",
        category="会议",
        priority=3,
        deadline=f"{next_year}-{next_month:02d}-05T10:00:00",
    )
    tm.set_status(tid5, "in_progress")

    # --- New tasks created this month ---
    # Tasks tid4 and tid5 were also created this month (via set_status which
    # touches updated_at, but created_at stays at insertion time).
    # Add more explicit new tasks:
    tid6 = tm.add("新需求评审", category="会议", priority=4)
    tid7 = tm.add("代码审查", category="开发", priority=3)

    # --- Progress logs with hours (this month) ---
    pt.log(tid1, "完成核心模块", hours_spent=20, new_progress=50)
    pt.log(tid1, "完成测试", hours_spent=18.5, new_progress=100)
    pt.log(tid2, "完成初稿", hours_spent=8, new_progress=70)
    pt.log(tid2, "终稿完成", hours_spent=4, new_progress=100)
    pt.log(tid3, "修复 Bug", hours_spent=3, new_progress=100)
    # Hours for in-progress task
    pt.log(tid4, "重构开始", hours_spent=15, new_progress=30)

    # Manually set progress_log dates to this month
    db.execute(
        """UPDATE progress_logs SET logged_at = ? WHERE task_id = ? AND content = ?""",
        (f"{month_str}-12T10:00:00", tid1, "完成核心模块"),
    )
    db.execute(
        """UPDATE progress_logs SET logged_at = ? WHERE task_id = ? AND content = ?""",
        (f"{month_str}-14T16:00:00", tid1, "完成测试"),
    )
    db.execute(
        """UPDATE progress_logs SET logged_at = ? WHERE task_id = ? AND content = ?""",
        (f"{month_str}-08T11:00:00", tid2, "完成初稿"),
    )
    db.execute(
        """UPDATE progress_logs SET logged_at = ? WHERE task_id = ? AND content = ?""",
        (f"{month_str}-10T14:00:00", tid2, "终稿完成"),
    )
    db.execute(
        """UPDATE progress_logs SET logged_at = ? WHERE task_id = ? AND content = ?""",
        (f"{month_str}-05T09:00:00", tid3, "修复 Bug"),
    )
    db.execute(
        """UPDATE progress_logs SET logged_at = ? WHERE task_id = ? AND content = ?""",
        (f"{month_str}-18T09:00:00", tid4, "重构开始"),
    )

    # --- OKR items ---
    obj_id = okr.add_objective(
        "提升产品质量",
        description="减少 Bug 数量，提升代码覆盖率",
        start_date=f"{year}-01-01",
        end_date=f"{year}-12-31",
    )
    kr1_id = okr.add_key_result(obj_id, "单元测试覆盖率达到 80%")
    kr2_id = okr.add_key_result(obj_id, "用户报告 Bug 减少 50%")
    okr.update_progress(kr1_id, 60)
    okr.update_progress(kr2_id, 40)

    # Link tasks to OKR
    okr.link_task(kr1_id, tid1)
    okr.link_task(kr2_id, tid3)

    return {
        "completed_ids": [tid1, tid2, tid3],
        "in_progress_ids": [tid4, tid5],
        "new_ids": [tid4, tid5, tid6, tid7],
        "year": year,
        "month": month,
    }


# ---------------------------------------------------------------------------
# Tests — Monthly
# ---------------------------------------------------------------------------


class TestMonthly:
    def test_monthly_generates_file(self, rg):
        """The monthly() call should create a file and return a path."""
        path = rg.monthly(year=2025, month=6)
        assert Path(path).exists()
        content = Path(path).read_text(encoding="utf-8")
        assert "# 月度工作报告" in content

    def test_monthly_content(self, populated_db, tm, pt, okr, db, rg):
        """Report content should contain the expected sections."""
        path = rg.monthly(year=populated_db["year"], month=populated_db["month"])
        content = Path(path).read_text(encoding="utf-8")

        assert "# 月度工作报告" in content
        assert "## 📊 概览" in content
        assert "完成项目 A 开发" in content
        assert "撰写技术文档" in content
        assert "修复登录 Bug" in content
        assert "## ✅ 本月完成" in content
        assert "## 🔄 活跃任务" in content
        assert "重构用户模块" in content
        assert "## 📈 分类统计" in content
        assert "## 🎯 OKR 进展" in content
        assert "## 💡 关键产出" in content
        assert "## 📅 下月展望" in content

    def test_empty_month(self, rg):
        """A month with no data should produce a valid report without crashing."""
        path = rg.monthly(year=2000, month=1)
        content = Path(path).read_text(encoding="utf-8")

        assert "# 月度工作报告" in content
        assert "本月无完成任务" in content
        assert "暂无活跃任务" in content
        assert "0 项" in content  # zero counts
        assert Path(path).exists()

    def test_report_contains_completed_tasks(self, populated_db, rg):
        """Completed tasks should be listed in the report with details."""
        path = rg.monthly(year=populated_db["year"], month=populated_db["month"])
        content = Path(path).read_text(encoding="utf-8")

        # All three completed tasks should appear
        assert "完成项目 A 开发" in content
        assert "撰写技术文档" in content
        assert "修复登录 Bug" in content

        # Category and priority should appear in table
        assert "开发" in content
        assert "文档" in content
        assert "P1" in content
        assert "P2" in content

    def test_report_contains_okr_progress(self, populated_db, rg):
        """OKR progress data should appear in the report."""
        path = rg.monthly(year=populated_db["year"], month=populated_db["month"])
        content = Path(path).read_text(encoding="utf-8")

        assert "提升产品质量" in content
        # Progress should be 50% (average of 60% and 40%)
        assert "50%" in content

    def test_report_contains_category_stats(self, populated_db, rg):
        """Category statistics should be present in the report."""
        path = rg.monthly(year=populated_db["year"], month=populated_db["month"])
        content = Path(path).read_text(encoding="utf-8")

        assert "## 📈 分类统计" in content
        assert "开发" in content
        assert "文档" in content

    def test_output_path_custom(self, rg, tmp_path):
        """Custom output_path should write the report to the specified location."""
        custom_path = tmp_path / "custom_report.md"
        result = rg.monthly(year=2025, month=5, output_path=str(custom_path))
        assert result == str(custom_path.resolve())
        assert custom_path.exists()
        assert "# 月度工作报告" in custom_path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests — Semi-annual
# ---------------------------------------------------------------------------


class TestSemiannual:
    def test_semiannual(self, populated_db, rg):
        """Semiannual report should generate a file with trend data."""
        half = 1 if populated_db["month"] <= 6 else 2
        path = rg.semiannual(year=populated_db["year"], half=half)
        content = Path(path).read_text(encoding="utf-8")

        assert "# 半年度工作报告" in content
        assert "## 📊 概览" in content
        assert "## 📈 月度趋势" in content
        assert "## 📊 分类统计" in content
        assert "## 🎯 OKR 进展" in content

        # Should have monthly trend table
        assert "月份 | 完成数" in content

    def test_semiannual_empty(self, rg):
        """Semiannual report for a year with no data should not crash."""
        path = rg.semiannual(year=1999, half=1)
        content = Path(path).read_text(encoding="utf-8")

        assert "# 半年度工作报告" in content
        assert "0 项" in content
        assert Path(path).exists()

    def test_semiannual_output_path_custom(self, rg, tmp_path):
        """Custom output_path for semiannual should write correctly."""
        custom_path = tmp_path / "half_year.md"
        result = rg.semiannual(year=2025, half=1, output_path=str(custom_path))
        assert result == str(custom_path.resolve())
        assert custom_path.exists()
        assert "# 半年度工作报告" in custom_path.read_text(encoding="utf-8")

    def test_semiannual_half1_months(self, rg):
        """Half 1 should cover months 1-6."""
        path = rg.semiannual(year=2025, half=1)
        content = Path(path).read_text(encoding="utf-8")

        assert "上半年" in content
        # Monthly detail sections should include months 1-6
        for m in range(1, 7):
            assert f"## {m}月" in content

    def test_semiannual_half2_months(self, rg):
        """Half 2 should cover months 7-12."""
        path = rg.semiannual(year=2025, half=2)
        content = Path(path).read_text(encoding="utf-8")

        assert "下半年" in content
        for m in range(7, 13):
            assert f"## {m}月" in content


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_default_month_is_current(self, rg):
        """Calling monthly() without args should use current year/month."""
        from datetime import date

        today = date.today()
        path = rg.monthly()
        content = Path(path).read_text(encoding="utf-8")

        assert f"{today.year}年{today.month}月" in content
        assert Path(path).exists()

    def test_year_boundary_monthly(self, rg):
        """December should handle next-month tasks in January of next year."""
        path = rg.monthly(year=2025, month=12)
        content = Path(path).read_text(encoding="utf-8")

        # Should not crash; next-month section should reference January
        assert Path(path).exists()
        assert "# 月度工作报告" in content

    def test_year_boundary_semiannual_h2(self, rg):
        """Half 2 should handle Dec → Jan boundary correctly for per-month queries."""
        path = rg.semiannual(year=2025, half=2)
        content = Path(path).read_text(encoding="utf-8")

        assert Path(path).exists()
        assert "10月" in content
        assert "11月" in content
        assert "12月" in content

    def test_invalid_half_raises(self, rg):
        """Half parameter must be 1 or 2."""
        with pytest.raises(ValueError):
            rg.semiannual(year=2025, half=3)
