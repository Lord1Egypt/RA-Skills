"""Tests for the MemoryStore core module and MCP memory tools."""

import json
import pytest
import aiosqlite
from pathlib import Path

from ghostclaw.core.memory import MemoryStore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _seed_db(db_path: Path, reports: list):
    """Insert test reports into a fresh SQLite database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                vibe_score INTEGER,
                stack TEXT,
                files_analyzed INTEGER,
                total_lines INTEGER,
                report_json TEXT,
                repo_path TEXT
            )
        """)
        for r in reports:
            await db.execute(
                "INSERT INTO reports (timestamp, vibe_score, stack, files_analyzed, total_lines, report_json, repo_path) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    r.get("timestamp", "2025-01-01T00:00:00"),
                    r.get("vibe_score", 50),
                    r.get("stack", "python"),
                    r.get("files_analyzed", 10),
                    r.get("total_lines", 500),
                    json.dumps(r.get("report", {})),
                    r.get("repo_path", "/test/repo"),
                ),
            )
        await db.commit()


def _make_report(**overrides):
    base = {
        "vibe_score": 75,
        "stack": "python",
        "files_analyzed": 20,
        "total_lines": 1000,
        "issues": ["Large file detected: app.py (450 lines)"],
        "architectural_ghosts": ["God Module: utils.py"],
        "red_flags": [],
        "coupling_metrics": {},
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# MemoryStore.list_runs
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_list_runs_empty(tmp_path):
    store = MemoryStore(db_path=tmp_path / "empty.db")
    runs = await store.list_runs()
    assert runs == []


@pytest.mark.asyncio
async def test_list_runs_returns_summaries(tmp_path):
    db_path = tmp_path / ".ghostclaw" / "storage" / "ghostclaw.db"
    await _seed_db(db_path, [
        {"vibe_score": 80, "stack": "python", "repo_path": "/repo/a"},
        {"vibe_score": 60, "stack": "node", "repo_path": "/repo/b"},
    ])
    store = MemoryStore(db_path=db_path)
    runs = await store.list_runs()
    assert len(runs) == 2
    assert "report_json" not in runs[0]  # summaries only
    assert runs[0]["vibe_score"] in (80, 60)


@pytest.mark.asyncio
async def test_list_runs_filter_by_repo(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"vibe_score": 80, "repo_path": "/repo/a"},
        {"vibe_score": 60, "repo_path": "/repo/b"},
        {"vibe_score": 90, "repo_path": "/repo/a"},
    ])
    store = MemoryStore(db_path=db_path)
    runs = await store.list_runs(repo_path="/repo/a")
    assert len(runs) == 2
    assert all(r["repo_path"] == "/repo/a" for r in runs)


@pytest.mark.asyncio
async def test_list_runs_respects_limit(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [{"vibe_score": i} for i in range(10)])
    store = MemoryStore(db_path=db_path)
    runs = await store.list_runs(limit=3)
    assert len(runs) == 3


# ---------------------------------------------------------------------------
# MemoryStore.get_run
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_run_not_found(tmp_path):
    store = MemoryStore(db_path=tmp_path / "empty.db")
    assert await store.get_run(999) is None


@pytest.mark.asyncio
async def test_get_run_returns_full_report(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    report = _make_report(vibe_score=85)
    await _seed_db(db_path, [{"vibe_score": 85, "report": report}])
    store = MemoryStore(db_path=db_path)
    run = await store.get_run(1)
    assert run is not None
    assert run["report"]["vibe_score"] == 85
    assert "God Module: utils.py" in run["report"]["architectural_ghosts"]


# ---------------------------------------------------------------------------
# MemoryStore.get_previous_run
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_previous_run_empty(tmp_path):
    store = MemoryStore(db_path=tmp_path / "empty.db")
    assert await store.get_previous_run() is None


@pytest.mark.asyncio
async def test_get_previous_run_returns_latest(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"timestamp": "2025-01-01T00:00:00", "vibe_score": 50, "report": _make_report(vibe_score=50)},
        {"timestamp": "2025-06-01T00:00:00", "vibe_score": 90, "report": _make_report(vibe_score=90)},
    ])
    store = MemoryStore(db_path=db_path)
    run = await store.get_previous_run()
    assert run is not None
    assert run["vibe_score"] == 90


@pytest.mark.asyncio
async def test_get_previous_run_filter_by_repo(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"timestamp": "2025-01-01T00:00:00", "vibe_score": 50, "repo_path": "/repo/a", "report": _make_report()},
        {"timestamp": "2025-06-01T00:00:00", "vibe_score": 90, "repo_path": "/repo/b", "report": _make_report()},
    ])
    store = MemoryStore(db_path=db_path)
    run = await store.get_previous_run(repo_path="/repo/a")
    assert run is not None
    assert run["repo_path"] == "/repo/a"


# ---------------------------------------------------------------------------
# MemoryStore.search
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_search_empty_db(tmp_path):
    store = MemoryStore(db_path=tmp_path / "empty.db")
    results = await store.search("anything")
    assert results == []


@pytest.mark.asyncio
async def test_search_finds_matching_issues(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    report = _make_report(issues=["circular dependency in auth module"])
    await _seed_db(db_path, [{"vibe_score": 60, "report": report}])
    store = MemoryStore(db_path=db_path)
    results = await store.search("circular dependency")
    assert len(results) == 1
    assert any("circular dependency" in s for s in results[0]["matched_snippets"])


@pytest.mark.asyncio
async def test_search_filters_by_stack(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"vibe_score": 70, "stack": "python", "report": _make_report(issues=["issue A"])},
        {"vibe_score": 80, "stack": "node", "report": _make_report(issues=["issue A"])},
    ])
    store = MemoryStore(db_path=db_path)
    results = await store.search("issue A", stack="python")
    assert len(results) == 1
    assert results[0]["stack"] == "python"


@pytest.mark.asyncio
async def test_search_filters_by_score_range(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"vibe_score": 30, "report": _make_report(issues=["problem"])},
        {"vibe_score": 70, "report": _make_report(issues=["problem"])},
        {"vibe_score": 90, "report": _make_report(issues=["problem"])},
    ])
    store = MemoryStore(db_path=db_path)
    results = await store.search("problem", min_score=50, max_score=80)
    assert len(results) == 1
    assert results[0]["vibe_score"] == 70


# ---------------------------------------------------------------------------
# MemoryStore.diff_runs
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_diff_runs_not_found(tmp_path):
    store = MemoryStore(db_path=tmp_path / "empty.db")
    assert await store.diff_runs(1, 2) is None


@pytest.mark.asyncio
async def test_diff_runs_shows_changes(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    report_a = _make_report(
        vibe_score=60,
        issues=["issue A", "issue B"],
        architectural_ghosts=["ghost X"],
    )
    report_b = _make_report(
        vibe_score=80,
        issues=["issue B", "issue C"],
        architectural_ghosts=["ghost X", "ghost Y"],
    )
    await _seed_db(db_path, [
        {"vibe_score": 60, "report": report_a},
        {"vibe_score": 80, "report": report_b},
    ])
    store = MemoryStore(db_path=db_path)
    diff = await store.diff_runs(1, 2)
    assert diff is not None
    assert diff["vibe_score_delta"] == 20
    assert "issue C" in diff["new_issues"]
    assert "issue A" in diff["resolved_issues"]
    assert "ghost Y" in diff["new_ghosts"]


# ---------------------------------------------------------------------------
# MemoryStore.get_knowledge_graph
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_knowledge_graph_empty(tmp_path):
    store = MemoryStore(db_path=tmp_path / "empty.db")
    graph = await store.get_knowledge_graph()
    assert graph["total_runs"] == 0
    assert graph["recurring_issues"] == []


@pytest.mark.asyncio
async def test_knowledge_graph_aggregates_data(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    reports = [
        {
            "timestamp": "2025-01-01T00:00:00",
            "vibe_score": 60,
            "stack": "python",
            "report": _make_report(
                vibe_score=60,
                issues=["Large file", "Missing tests"],
                architectural_ghosts=["God Module"],
                coupling_metrics={"auth": {"instability": 0.9}},
            ),
        },
        {
            "timestamp": "2025-02-01T00:00:00",
            "vibe_score": 70,
            "stack": "python",
            "report": _make_report(
                vibe_score=70,
                issues=["Large file"],
                architectural_ghosts=["God Module", "Circular Import"],
                coupling_metrics={"auth": {"instability": 0.85}},
            ),
        },
        {
            "timestamp": "2025-03-01T00:00:00",
            "vibe_score": 80,
            "stack": "python",
            "report": _make_report(
                vibe_score=80,
                issues=["Large file"],
                architectural_ghosts=["Circular Import"],
                coupling_metrics={"auth": {"instability": 0.8}},
            ),
        },
    ]
    await _seed_db(db_path, reports)
    store = MemoryStore(db_path=db_path)
    graph = await store.get_knowledge_graph()

    assert graph["total_runs"] == 3
    assert "python" in graph["stacks_seen"]

    # Score trend should be chronological
    assert len(graph["score_trend"]) == 3
    assert graph["score_trend"][0]["vibe_score"] == 60
    assert graph["score_trend"][-1]["vibe_score"] == 80

    # "Large file" appears 3 times, should be top recurring issue
    issue_items = {item["item"]: item["count"] for item in graph["recurring_issues"]}
    assert issue_items["Large file"] == 3
    assert issue_items.get("Missing tests", 0) == 1

    # "God Module" appears 2 times
    ghost_items = {item["item"]: item["count"] for item in graph["recurring_ghosts"]}
    assert ghost_items["God Module"] == 2

    # auth module with avg instability ~0.85 should be a hotspot
    hotspot_modules = [h["module"] for h in graph["coupling_hotspots"]]
    assert "auth" in hotspot_modules


# ---------------------------------------------------------------------------
# MCP tool wrappers (integration-style via the actual functions)
# ---------------------------------------------------------------------------

from ghostclaw_mcp.server import (
    ghostclaw_memory_search,
    ghostclaw_memory_get_run,
    ghostclaw_memory_list_runs,
    ghostclaw_memory_diff_runs,
    ghostclaw_knowledge_graph,
    ghostclaw_memory_get_previous_run,
)
from unittest.mock import patch


@pytest.mark.asyncio
async def test_mcp_memory_list_runs(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [{"vibe_score": 77}])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_list_runs())
        assert result["count"] == 1
        assert result["runs"][0]["vibe_score"] == 77


@pytest.mark.asyncio
async def test_mcp_memory_get_run(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    report = _make_report(vibe_score=65)
    await _seed_db(db_path, [{"vibe_score": 65, "report": report}])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_get_run(run_id=1))
        assert result["report"]["vibe_score"] == 65


@pytest.mark.asyncio
async def test_mcp_memory_get_run_not_found(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_get_run(run_id=999))
        assert "error" in result


@pytest.mark.asyncio
async def test_mcp_memory_search(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    report = _make_report(issues=["circular dependency found"])
    await _seed_db(db_path, [{"vibe_score": 55, "report": report}])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_search(query="circular"))
        assert result["count"] == 1


@pytest.mark.asyncio
async def test_mcp_memory_diff_runs(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"vibe_score": 50, "report": _make_report(vibe_score=50, issues=["A"])},
        {"vibe_score": 80, "report": _make_report(vibe_score=80, issues=["B"])},
    ])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_diff_runs(run_id_a=1, run_id_b=2))
        assert result["vibe_score_delta"] == 30


@pytest.mark.asyncio
async def test_mcp_knowledge_graph(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"vibe_score": 60, "report": _make_report(issues=["issue X"])},
        {"vibe_score": 70, "report": _make_report(issues=["issue X"])},
    ])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_knowledge_graph())
        assert result["total_runs"] == 2
        issue_items = {i["item"]: i["count"] for i in result["recurring_issues"]}
        assert issue_items["issue X"] == 2


@pytest.mark.asyncio
async def test_mcp_memory_get_previous_run(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [
        {"timestamp": "2025-01-01T00:00:00", "vibe_score": 40, "report": _make_report(vibe_score=40)},
        {"timestamp": "2025-06-01T00:00:00", "vibe_score": 88, "report": _make_report(vibe_score=88)},
    ])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_get_previous_run())
        assert result["vibe_score"] == 88


@pytest.mark.asyncio
async def test_mcp_memory_get_previous_run_empty(tmp_path):
    db_path = tmp_path / "ghostclaw.db"
    await _seed_db(db_path, [])
    with patch("ghostclaw_mcp.server.get_memory_store", return_value=MemoryStore(db_path=db_path)):
        result = json.loads(await ghostclaw_memory_get_previous_run())
        assert "error" in result
