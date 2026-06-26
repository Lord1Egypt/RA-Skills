"""Shared pytest fixtures for memory-health-check tests."""
import json, sqlite3, tempfile, time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
import pytest

SKILL_ROOT = Path(__file__).resolve().parent.parent
FAKE_HOME = Path("/tmp/fake_openclaw_mhc")

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def fake_mhc_home(tmp_path):
    """
    Replace Path.home() with a controlled temp directory for every test.
    This mirrors the approach used in dreaming-optimizer tests.
    """
    fake = tmp_path / "fake_openclaw_mhc"
    fake.mkdir(parents=True, exist_ok=True)

    workspace_dir = fake / ".openclaw" / "workspace"
    memory_dir = workspace_dir / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    (fake / ".openclaw" / "memory").mkdir(parents=True, exist_ok=True)

    reports_dir = fake / ".openclaw" / "workspace" / "memory-health-reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    with patch("pathlib.Path.home", return_value=fake):
        yield fake


@pytest.fixture
def memory_dir(fake_mhc_home):
    """Return the path to the (pre-created) A-layer memory directory."""
    return fake_mhc_home / ".openclaw" / "workspace" / "memory"


# ---------------------------------------------------------------------------
# Integrity scan helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def healthy_sqlite_db(memory_dir):
    """Create a clean, uncorrupted SQLite file."""
    db_path = memory_dir / "main.sqlite"
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, content TEXT)")
    conn.execute("INSERT INTO entries (content) VALUES ('healthy entry')")
    conn.commit()
    conn.close()
    return db_path


@pytest.fixture
def corrupted_sqlite_db(memory_dir):
    """Create a SQLite file with intentional corruption."""
    db_path = memory_dir / "corrupted.sqlite"
    conn = sqlite3.connect(str(db_path))
    # Write invalid data to simulate corruption
    with open(str(db_path), "wb") as f:
        f.write(b"SQLite format 3 XXX THIS IS CORRUPT XXX")
    return db_path


# ---------------------------------------------------------------------------
# Bloat detector helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def empty_memory(memory_dir):
    """memory_dir is already empty by default — just return it."""
    return memory_dir


@pytest.fixture
def large_memory_dir(memory_dir):
    """
    Create files totalling ~450 MB to trigger the "warning" threshold
    without consuming real disk space excessively.
    We write sparse-ish files to keep temp-space reasonable.
    """
    # Write 10 files of ~45 MB each (sparse files on macOS don't allocate fully)
    for i in range(10):
        f = memory_dir / f"big_file_{i}.md"
        # Write a pattern that compresses poorly but is fast to create
        f.write_bytes((f"chunk_{i}_" + "x" * 45 * 1024 * 1024).encode())
    return memory_dir


# ---------------------------------------------------------------------------
# Orphan finder helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def no_memory_files(memory_dir):
    """memory_dir has no files at all."""
    return memory_dir


@pytest.fixture
def mixed_orphan_files(memory_dir):
    """
    Create a mix of .md files where some are orphans (not cross-referenced)
    and one references another.
    """
    f1 = memory_dir / "note_A.md"
    f1.write_text("这是笔记A。")

    f2 = memory_dir / "note_B.md"
    f2.write_text("笔记B引用了 note_A。")  # references f1 via stem

    # A sqlite "entry" file
    db = memory_dir / "entries.sqlite"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE t (id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()

    return memory_dir


# ---------------------------------------------------------------------------
# Dedup scanner helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def all_unique_files(memory_dir):
    """Create a set of completely unique .md files."""
    contents = [
        "今天完成了数据库优化工作。",
        "学习了新的API设计模式。",
        "阅读了关于分布式系统的文档。",
        "解决了配置管理的难点问题。",
    ]
    for i, c in enumerate(contents):
        (memory_dir / f"unique_{i}.md").write_text(c)
    return memory_dir


@pytest.fixture
def duplicate_files(memory_dir):
    """Create .md files with high-similarity content to trigger dedup."""
    base = "今天完成了数据库API修复，测试通过，部署到生产环境。"
    for i in range(3):
        (memory_dir / f"dup_{i}.md").write_text(base + f" 额外信息{i}。")
    return memory_dir


# ---------------------------------------------------------------------------
# Freshness helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def all_recent_files(memory_dir):
    """Create .md files with very recent mtimes."""
    now = time.time()
    for i in range(5):
        f = memory_dir / f"recent_{i}.md"
        f.write_text(f"最近的文件 {i}")
        # Set mtime to 1 hour ago
        import os
        os.utime(f, (now - 3600, now - 3600))
    return memory_dir


@pytest.fixture
def all_old_files(memory_dir):
    """Create .md files with old mtimes (90+ days)."""
    now = time.time()
    for i in range(5):
        f = memory_dir / f"old_{i}.md"
        f.write_text(f"很旧的文件 {i}")
        # Set mtime to 100 days ago
        import os
        os.utime(f, (now - 100 * 86400, now - 100 * 86400))
    return memory_dir


@pytest.fixture
def mixed_age_files(memory_dir):
    """Create a mix of 7-day-old, 30-day-old, and 90-day-old files."""
    now = time.time()
    # 7-day-old (recent)
    f1 = memory_dir / "fresh.md"
    f1.write_text("7天前的文件")
    import os; os.utime(f1, (now - 7 * 86400, now - 7 * 86400))

    # 30-day-old (boundary)
    f2 = memory_dir / "boundary.md"
    f2.write_text("30天前的文件")
    os.utime(f2, (now - 30 * 86400, now - 30 * 86400))

    # 90-day-old (stale)
    f3 = memory_dir / "stale.md"
    f3.write_text("90天前的文件")
    os.utime(f3, (now - 90 * 86400, now - 90 * 86400))

    return memory_dir


# ---------------------------------------------------------------------------
# Health score helpers — pre-built dimension results
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_dimensions_healthy():
    return {
        "integrity":  {"status": "healthy", "score": 100},
        "bloat":      {"status": "healthy", "score": 100, "total_mb": 10},
        "orphans":    {"status": "healthy", "score": 100, "orphan_rate": 0.0},
        "dedup":      {"status": "healthy", "score": 100, "dup_rate": 0.0},
        "freshness":  {"status": "healthy", "score": 100, "freshness_rate": 90.0},
    }


@pytest.fixture
def mock_dimensions_critical():
    return {
        "integrity":  {"status": "critical", "score": 0},
        "bloat":      {"status": "critical", "score": 20, "total_mb": 3000},
        "orphans":    {"status": "critical", "score": 30, "orphan_rate": 10.0},
        "dedup":      {"status": "critical", "score": 20, "dup_rate": 15.0},
        "freshness":  {"status": "critical", "score": 20, "freshness_rate": 20.0},
    }
