"""
Tests for the OKR Manager module.

Uses pytest + tempfile for temporary SQLite databases.
"""

import os
import tempfile
from pathlib import Path

import pytest

import sys
# Ensure the *parent* (personal-assistant) is on sys.path so that
# `from scripts.db import Database` and relative imports inside
# `okr` resolve correctly.
_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.db import Database
from scripts.okr import OKRManager


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def db():
    """Create a fresh Database + OKRManager on a temp file."""
    fd, path = tempfile.mkstemp(suffix=".db", prefix="pa_okr_test_")
    os.close(fd)
    database = Database(db_path=path)
    database.init_db()
    manager = OKRManager(database)
    yield manager
    database.close()
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def setup_tree(db):
    """Create a sample OKR tree: 1 Objective → 2 KRs → 1 Initiative each."""
    oid = db.add_objective("O1: Improve Product Quality", "Make it better")
    kr1 = db.add_key_result(oid, "KR1: Reduce bugs by 50%", "Focus on critical path")
    kr2 = db.add_key_result(oid, "KR2: Increase test coverage to 80%", "Add unit tests")
    i1 = db.add_initiative(kr1, "Init1: Fix top-10 crash bugs")
    i2 = db.add_initiative(kr2, "Init2: Write missing tests for core modules")
    return {
        "objective_id": oid,
        "kr1_id": kr1,
        "kr2_id": kr2,
        "ini1_id": i1,
        "ini2_id": i2,
    }


# ---------------------------------------------------------------------------
# 1. CRUD — Create
# ---------------------------------------------------------------------------

def test_add_objective(db):
    oid = db.add_objective("O1", "desc", "2026-01-01", "2026-06-30", weight=2.0)
    assert oid == 1

    obj = db.get(oid)
    assert obj is not None
    assert obj["title"] == "O1"
    assert obj["description"] == "desc"
    assert obj["obj_type"] == "objective"
    assert obj["start_date"] == "2026-01-01"
    assert obj["end_date"] == "2026-06-30"
    assert obj["weight"] == 2.0
    assert obj["status"] == "active"
    assert obj["progress"] == 0
    assert obj["parent_id"] is None


def test_add_objective_defaults(db):
    oid = db.add_objective("Minimal O")
    obj = db.get(oid)
    assert obj["description"] == ""
    assert obj["start_date"] is None
    assert obj["end_date"] is None
    assert obj["weight"] == 1.0


def test_add_key_result(db):
    oid = db.add_objective("O1")
    krid = db.add_key_result(oid, "KR1", "measure", weight=0.5)
    kr = db.get(krid)
    assert kr["obj_type"] == "key_result"
    assert kr["parent_id"] == oid
    assert kr["title"] == "KR1"
    assert kr["weight"] == 0.5


def test_add_key_result_invalid_parent(db):
    with pytest.raises(ValueError, match="not found"):
        db.add_key_result(999, "KR")


def test_add_key_result_parent_not_objective(db):
    oid = db.add_objective("O1")
    krid = db.add_key_result(oid, "KR1")
    # Try to add a KR under another KR (not an objective)
    with pytest.raises(ValueError, match="not found"):
        db.add_key_result(krid, "KR under KR")


def test_add_initiative(db):
    oid = db.add_objective("O1")
    krid = db.add_key_result(oid, "KR1")
    iid = db.add_initiative(krid, "Init1", "action item")
    ini = db.get(iid)
    assert ini["obj_type"] == "initiative"
    assert ini["parent_id"] == krid
    assert ini["title"] == "Init1"


def test_add_initiative_invalid_parent(db):
    with pytest.raises(ValueError, match="not found"):
        db.add_initiative(999, "Init")


def test_add_initiative_parent_not_kr(db):
    oid = db.add_objective("O1")
    with pytest.raises(ValueError, match="not found"):
        db.add_initiative(oid, "Init under Objective")


# ---------------------------------------------------------------------------
# 2. Query
# ---------------------------------------------------------------------------

def test_get_nonexistent(db):
    assert db.get(999) is None


def test_get(db):
    oid = db.add_objective("O1")
    obj = db.get(oid)
    assert obj["id"] == oid
    assert obj["title"] == "O1"


def test_list_objectives(db):
    db.add_objective("O1")
    db.add_objective("O2")
    # Create a completed objective — shouldn't appear in default list
    o3 = db.add_objective("O3")
    db.update_status(o3, "completed")

    active = db.list_objectives()
    assert len(active) == 2
    assert active[0]["title"] == "O1"
    assert active[1]["title"] == "O2"

    completed = db.list_objectives(status="completed")
    assert len(completed) == 1
    assert completed[0]["title"] == "O3"


def test_list_by_status(db):
    oid = db.add_objective("O1")
    krid = db.add_key_result(oid, "KR1")
    db.update_status(krid, "completed")

    active = db.list_by_status("active")
    assert len(active) == 1
    assert active[0]["title"] == "O1"

    completed = db.list_by_status("completed")
    assert len(completed) == 1
    assert completed[0]["title"] == "KR1"

    cancelled = db.list_by_status("cancelled")
    assert len(cancelled) == 0


def test_get_tree_empty(db):
    tree = db.get_tree()
    assert tree == []


def test_get_tree(setup_tree, db):
    tree = db.get_tree()
    assert len(tree) == 1

    obj = tree[0]
    assert obj["title"] == "O1: Improve Product Quality"
    assert "key_results" in obj
    assert len(obj["key_results"]) == 2

    kr1 = obj["key_results"][0]
    assert kr1["title"] == "KR1: Reduce bugs by 50%"
    assert "initiatives" in kr1
    assert len(kr1["initiatives"]) == 1
    assert kr1["initiatives"][0]["title"] == "Init1: Fix top-10 crash bugs"

    kr2 = obj["key_results"][1]
    assert kr2["title"] == "KR2: Increase test coverage to 80%"
    assert len(kr2["initiatives"]) == 1
    assert kr2["initiatives"][0]["title"] == "Init2: Write missing tests for core modules"


def test_get_tree_objective_without_kr(db):
    db.add_objective("Solo O")
    tree = db.get_tree()
    assert len(tree) == 1
    assert tree[0]["key_results"] == []


# ---------------------------------------------------------------------------
# 3. Update — Progress
# ---------------------------------------------------------------------------

def test_update_progress_kr(db):
    oid = db.add_objective("O1")
    krid = db.add_key_result(oid, "KR1")

    db.update_progress(krid, 50)
    kr = db.get(krid)
    assert kr["progress"] == 50


def test_update_progress_propagates_to_objective(db):
    """When KR progress changes, Objective progress = average of all KRs."""
    oid = db.add_objective("O1")
    kr1 = db.add_key_result(oid, "KR1")
    kr2 = db.add_key_result(oid, "KR2")

    # Update one KR
    db.update_progress(kr1, 60)
    obj = db.get(oid)
    # Only one KR so far, but both exist — KR2 is at default 0
    # Average: (60 + 0) / 2 = 30
    assert obj["progress"] == 30

    # Update the other KR
    db.update_progress(kr2, 40)
    obj = db.get(oid)
    # Average: (60 + 40) / 2 = 50
    assert obj["progress"] == 50


def test_update_progress_objective_only(db):
    """Updating progress on an Objective directly should work (no propagation)."""
    oid = db.add_objective("O1")
    db.update_progress(oid, 75)
    obj = db.get(oid)
    assert obj["progress"] == 75


def test_update_progress_invalid_range(db):
    oid = db.add_objective("O1")
    with pytest.raises(ValueError, match="between 0 and 100"):
        db.update_progress(oid, 150)
    with pytest.raises(ValueError, match="between 0 and 100"):
        db.update_progress(oid, -5)


def test_update_progress_nonexistent(db):
    with pytest.raises(ValueError, match="not found"):
        db.update_progress(999, 50)


def test_update_progress_propagates_from_initiative(db):
    """Initiatives don't propagate — only KRs propagate to Objectives."""
    oid = db.add_objective("O1")
    krid = db.add_key_result(oid, "KR1")
    iid = db.add_initiative(krid, "Init1")

    db.update_progress(iid, 80)
    # Objective should still be 0 (KR wasn't updated)
    obj = db.get(oid)
    kr = db.get(krid)
    ini = db.get(iid)
    assert ini["progress"] == 80
    assert kr["progress"] == 0  # No propagation from initiative
    assert obj["progress"] == 0


# ---------------------------------------------------------------------------
# 4. Update — Status
# ---------------------------------------------------------------------------

def test_update_status(db):
    oid = db.add_objective("O1")
    db.update_status(oid, "completed")
    obj = db.get(oid)
    assert obj["status"] == "completed"


def test_update_status_all_values(db):
    oid = db.add_objective("O1")
    for status in ["active", "completed", "cancelled"]:
        db.update_status(oid, status)
        assert db.get(oid)["status"] == status


def test_update_status_invalid(db):
    oid = db.add_objective("O1")
    with pytest.raises(ValueError, match="must be one of"):
        db.update_status(oid, "archived")


def test_update_status_nonexistent(db):
    with pytest.raises(ValueError, match="not found"):
        db.update_status(999, "completed")


# ---------------------------------------------------------------------------
# 5. Delete — Cascade
# ---------------------------------------------------------------------------

def test_delete_objective_cascades(setup_tree, db):
    ids = setup_tree

    db.delete(ids["objective_id"])

    # Everything should be gone
    assert db.get(ids["objective_id"]) is None
    assert db.get(ids["kr1_id"]) is None
    assert db.get(ids["kr2_id"]) is None
    assert db.get(ids["ini1_id"]) is None
    assert db.get(ids["ini2_id"]) is None


def test_delete_kr_cascades_initiatives(setup_tree, db):
    ids = setup_tree

    db.delete(ids["kr1_id"])

    # KR1 and its initiative should be gone
    assert db.get(ids["kr1_id"]) is None
    assert db.get(ids["ini1_id"]) is None

    # Objective and KR2 + its initiative should remain
    assert db.get(ids["objective_id"]) is not None
    assert db.get(ids["kr2_id"]) is not None
    assert db.get(ids["ini2_id"]) is not None


def test_delete_initiative_no_cascade(setup_tree, db):
    ids = setup_tree

    db.delete(ids["ini1_id"])

    # Only the initiative should be gone
    assert db.get(ids["ini1_id"]) is None
    assert db.get(ids["kr1_id"]) is not None
    assert db.get(ids["kr2_id"]) is not None
    assert db.get(ids["objective_id"]) is not None


def test_delete_nonexistent(db):
    # Should not raise
    db.delete(999)


def test_delete_idempotent(db):
    oid = db.add_objective("O")
    db.delete(oid)
    db.delete(oid)  # Second delete shouldn't raise
    assert db.get(oid) is None


# ---------------------------------------------------------------------------
# 6. Sync from Markdown doc
# ---------------------------------------------------------------------------

SAMPLE_MD = """\
## 提升产品质量

进度: 60%

### 减少线上 Bug 50%

progress: 30%

#### 修复 Top-10 崩溃

进度: 100%

#### 建立回归测试套件

progress: 20%

### 提高测试覆盖率到 80%

进度: 40%

#### 为核心模块编写单元测试

进度: 50%
"""


def test_parse_markdown_okr(db):
    parsed = db._parse_markdown_okr(SAMPLE_MD)
    assert len(parsed) == 6

    types = [p["obj_type"] for p in parsed]
    assert types == ["objective", "key_result", "initiative", "initiative",
                     "key_result", "initiative"]

    # Objective
    assert parsed[0]["title"] == "提升产品质量"
    assert parsed[0]["progress"] == 60
    assert parsed[0]["_doc_parent_index"] is None

    # First KR
    assert parsed[1]["title"] == "减少线上 Bug 50%"
    assert parsed[1]["progress"] == 30
    assert parsed[1]["_doc_parent_index"] == parsed[0]["_doc_index"]

    # Initiatives under first KR
    assert parsed[2]["title"] == "修复 Top-10 崩溃"
    assert parsed[2]["progress"] == 100
    assert parsed[2]["_doc_parent_index"] == parsed[1]["_doc_index"]

    assert parsed[3]["title"] == "建立回归测试套件"
    assert parsed[3]["progress"] == 20
    assert parsed[3]["_doc_parent_index"] == parsed[1]["_doc_index"]

    # Second KR
    assert parsed[4]["title"] == "提高测试覆盖率到 80%"
    assert parsed[4]["progress"] == 40
    assert parsed[4]["_doc_parent_index"] == parsed[0]["_doc_index"]

    # Initiative under second KR
    assert parsed[5]["title"] == "为核心模块编写单元测试"
    assert parsed[5]["progress"] == 50
    assert parsed[5]["_doc_parent_index"] == parsed[4]["_doc_index"]


def test_sync_from_doc_adds_all_items(db):
    result = db.sync_from_doc("doc_123", SAMPLE_MD)
    assert result["added"] == 6
    assert result["updated"] == 0
    assert result["removed"] == 0

    tree = db.get_tree()
    assert len(tree) == 1
    obj = tree[0]
    assert obj["title"] == "提升产品质量"
    assert obj["source_doc_token"] == "doc_123"
    assert len(obj["key_results"]) == 2

    kr1 = obj["key_results"][0]
    assert kr1["title"] == "减少线上 Bug 50%"
    assert kr1["progress"] == 30
    assert len(kr1["initiatives"]) == 2

    kr2 = obj["key_results"][1]
    assert kr2["title"] == "提高测试覆盖率到 80%"
    assert kr2["progress"] == 40
    assert len(kr2["initiatives"]) == 1


def test_sync_from_doc_updates_existing(db):
    # First sync
    db.sync_from_doc("doc_123", SAMPLE_MD)

    # Second sync with updated progress
    updated_md = SAMPLE_MD.replace("progress: 30%", "progress: 75%")
    result = db.sync_from_doc("doc_123", updated_md)

    assert result["added"] == 0
    assert result["updated"] == 6
    assert result["removed"] == 0

    # Verify the progress was updated
    tree = db.get_tree()
    kr1 = tree[0]["key_results"][0]
    assert kr1["progress"] == 75


def test_sync_from_doc_removes_items(db):
    db.sync_from_doc("doc_123", SAMPLE_MD)

    # New doc with only the objective and first KR
    reduced_md = """\
## 提升产品质量

### 减少线上 Bug 50%
"""
    result = db.sync_from_doc("doc_123", reduced_md)

    assert result["added"] == 0
    assert result["updated"] == 2  # The two items that still exist
    assert result["removed"] == 4  # The other 4 items

    # Removed items should be marked completed
    completed = db.list_by_status("completed")
    assert len(completed) == 4


def test_sync_from_doc_empty(db):
    """Syncing empty content should mark everything as completed."""
    db.add_objective("O1")
    result = db.sync_from_doc("doc_new", "")
    assert result["added"] == 0
    assert result["updated"] == 0
    assert result["removed"] == 0  # No previous items for this doc_token


def test_sync_from_doc_multiple_objectives(db):
    md = """\
## O1

### KR1

## O2

### KR2
"""
    result = db.sync_from_doc("doc_multi", md)
    assert result["added"] == 4

    tree = db.get_tree()
    assert len(tree) == 2
    assert tree[0]["title"] == "O1"
    assert tree[1]["title"] == "O2"


def test_sync_from_doc_progress_patterns(db):
    """Test all progress extraction patterns."""
    md = """\
## O1

(75%)

### KR1

进度: 80%

### KR2

progress: 60%

### KR3

进度 90%
"""
    result = db.sync_from_doc("doc_pat", md)
    assert result["added"] == 4

    tree = db.get_tree()
    obj = tree[0]
    assert obj["progress"] == 75  # (75%)

    krs = obj["key_results"]
    assert krs[0]["progress"] == 80  # 进度: 80%
    assert krs[1]["progress"] == 60  # progress: 60%
    assert krs[2]["progress"] == 90  # 进度 90%


# ---------------------------------------------------------------------------
# 7. Task linking
# ---------------------------------------------------------------------------

def test_link_task(db):
    oid = db.add_objective("O1")
    task_id = db.db.insert("tasks", {"title": "Task A", "status": "todo", "priority": 3})

    db.link_task(oid, task_id)
    task = db.db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
    assert task["okr_id"] == oid


def test_unlink_task(db):
    oid = db.add_objective("O1")
    task_id = db.db.insert("tasks", {"title": "Task B", "status": "todo", "priority": 3})

    db.link_task(oid, task_id)
    db.unlink_task(task_id)
    task = db.db.fetch_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
    assert task["okr_id"] is None


def test_get_linked_tasks(db):
    oid = db.add_objective("O1")
    t1 = db.db.insert("tasks", {"title": "T1", "status": "todo", "priority": 3})
    t2 = db.db.insert("tasks", {"title": "T2", "status": "todo", "priority": 3})

    db.link_task(oid, t1)
    db.link_task(oid, t2)

    linked = db.get_linked_tasks(oid)
    assert len(linked) == 2
    titles = {t["title"] for t in linked}
    assert titles == {"T1", "T2"}


def test_get_linked_tasks_no_links(db):
    oid = db.add_objective("O1")
    linked = db.get_linked_tasks(oid)
    assert linked == []


# ---------------------------------------------------------------------------
# 8. Progress summary
# ---------------------------------------------------------------------------

def test_progress_summary_empty(db):
    summary = db.progress_summary()
    assert summary["total_objectives"] == 0
    assert summary["total_key_results"] == 0
    assert summary["total_initiatives"] == 0
    assert summary["objectives"] == []


def test_progress_summary(setup_tree, db):
    ids = setup_tree

    # Set some progress
    db.update_progress(ids["kr1_id"], 50)
    db.update_progress(ids["kr2_id"], 70)

    # Link a task to KR1
    task_id = db.db.insert("tasks", {"title": "Bug fix", "status": "todo", "priority": 2})
    db.link_task(ids["kr1_id"], task_id)

    summary = db.progress_summary()
    assert summary["total_objectives"] == 1
    assert summary["total_key_results"] == 2
    assert summary["total_initiatives"] == 2

    obj = summary["objectives"][0]
    assert obj["title"] == "O1: Improve Product Quality"
    assert obj["progress"] == 60  # (50 + 70) / 2

    kr1_summary = obj["key_results"][0]
    assert kr1_summary["progress"] == 50
    assert kr1_summary["linked_task_count"] == 1

    kr2_summary = obj["key_results"][1]
    assert kr2_summary["progress"] == 70
    assert kr2_summary["linked_task_count"] == 0
