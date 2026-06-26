"""Tests for two-source World Cup group-winner discovery (scripts/discovery.py).

Covers the three diagnosed bugs:
  1. wrong source        -> discover() reads BOTH active venue and importable upstream pool;
  2. dead search kwargs  -> fetch_active_markets() uses only `limit` and degrades on error;
  3. regex misses titles -> extract_group_letter() matches the live "finish first ..." format.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "scripts"))

import discovery  # noqa: E402
from discovery import (  # noqa: E402
    discover,
    extract_group_letter,
    fetch_active_markets,
    fetch_importable_worldcup,
    find_group_sets,
    format_report,
    is_confirmed_exclusive,
)


# --- Test doubles -------------------------------------------------------------------------------
class Obj:
    """Market as an attribute object (one of the two shapes the SDK returns)."""
    def __init__(self, **kw):
        self.__dict__.update(kw)


def amarket(id, question, status="active", **kw):
    return Obj(id=id, question=question, status=status, **kw)


class FakeClient:
    def __init__(self, active=None, importable=None,
                 active_fail_limits=(), importable_max_limit=100, importable_fail_queries=()):
        self._active = list(active or [])
        self._importable = list(importable or [])
        self._active_fail_limits = set(active_fail_limits)
        self._importable_max_limit = importable_max_limit
        self._importable_fail_queries = set(importable_fail_queries)
        self.active_calls = []
        self.importable_calls = []

    # mirrors SDK 0.17.25: (status, import_source, limit, include) — note: NO search kwarg
    def get_markets(self, status="active", import_source=None, limit=50, include=None):
        self.active_calls.append(limit)
        if limit in self._active_fail_limits:
            raise RuntimeError(f"limit {limit} exceeds server cap")
        return list(self._active)

    def list_importable_markets(self, q=None, limit=50, min_volume=0):
        self.importable_calls.append((q, limit, min_volume))
        if q in self._importable_fail_queries:
            raise RuntimeError(f"422 on query {q!r}")
        if limit > self._importable_max_limit:
            raise ValueError(f"422: limit {limit} > {self._importable_max_limit}")
        return list(self._importable)


# === 1. extract_group_letter (10) ===============================================================
def test_extract_win_group():
    assert extract_group_letter("Will Spain win Group B?") == "B"


def test_extract_finish_first_world_cup():
    # the live title format that the old regex missed
    assert extract_group_letter("Will Mexico finish first in World Cup Group A?") == "A"


def test_extract_finishes_first_plain():
    assert extract_group_letter("England finishes first in Group C") == "C"


def test_extract_group_winner_suffix():
    assert extract_group_letter("Group D winner") == "D"


def test_extract_top_group():
    assert extract_group_letter("Brazil to top Group E") == "E"


def test_extract_case_insensitive():
    assert extract_group_letter("FINISH FIRST IN GROUP F") == "F"


def test_extract_rejects_advancement():
    assert extract_group_letter("Will Mexico advance from Group A?") is None


def test_extract_rejects_qualify():
    assert extract_group_letter("Will England qualify from Group B?") is None


def test_extract_rejects_runner_up():
    assert extract_group_letter("Will Spain finish runner-up in Group C?") is None


def test_extract_rejects_second_place_nongroup_range_and_empty():
    assert extract_group_letter("USA second place in Group D") is None
    assert extract_group_letter("Will Brazil win the World Cup?") is None
    assert extract_group_letter("Will X win Group M?") is None      # only A–L are valid
    assert extract_group_letter(None) is None
    assert extract_group_letter("") is None


# === 2. fetch_active_markets (3) ================================================================
def test_fetch_active_uses_limit_only():
    client = FakeClient(active=[amarket(1, "win Group A")])
    out = fetch_active_markets(client)
    assert len(out) == 1
    assert client.active_calls == [5000]                # wide fetch, single call, only `limit`


def test_fetch_active_degrades_on_error():
    client = FakeClient(active=[amarket(1, "win Group A")], active_fail_limits={5000, 1000})
    out = fetch_active_markets(client)
    assert len(out) == 1
    assert client.active_calls == [5000, 1000, 500]     # degraded down the ladder until success


def test_fetch_active_all_fail_returns_empty():
    client = FakeClient(active=[amarket(1, "win Group A")],
                        active_fail_limits={5000, 1000, 500, 200, 50})
    assert fetch_active_markets(client) == []


# === 3. fetch_importable_worldcup (4) ==========================================================
def test_importable_clamps_limit_over_100():
    # fake 422s on limit > 100; clamping must prevent the crash entirely
    client = FakeClient(importable=[amarket(1, "Mexico finish first in Group A")],
                        importable_max_limit=100)
    out = fetch_importable_worldcup(client, limit=200)
    assert len(out) == 1
    assert all(call[1] == 100 for call in client.importable_calls)


def test_importable_dedupes_across_queries():
    pool = [amarket(1, "Mexico finish first in Group A"),
            amarket(2, "Brazil finish first in Group B")]
    client = FakeClient(importable=pool)
    out = fetch_importable_worldcup(client)
    assert len(client.importable_calls) == 4            # all default queries attempted
    assert len(out) == 2                                # deduped by id despite 4 query passes


def test_importable_skips_failed_query():
    pool = [amarket(1, "Mexico finish first in Group A")]
    client = FakeClient(importable=pool, importable_fail_queries={"FIFA"})
    out = fetch_importable_worldcup(client)
    assert any(call[0] == "FIFA" for call in client.importable_calls)
    assert len(out) == 1                                # surviving queries still produce signal


def test_importable_handles_dict_and_object_shapes():
    pool = [
        {"id": 1, "question": "Mexico finish first in Group A"},      # dict shape
        amarket(2, "Brazil finish first in Group B"),                 # object shape
    ]
    client = FakeClient(importable=pool)
    out = fetch_importable_worldcup(client)
    questions = {discovery._question_of(m) for m in out}
    assert "Mexico finish first in Group A" in questions
    assert "Brazil finish first in Group B" in questions


# === 4. discover (5) ============================================================================
def test_discover_active_legs():
    client = FakeClient(active=[amarket(1, "Spain win Group A"),
                                amarket(2, "Mexico win Group A")])
    result = discover(client)
    assert len(result["groups"]["A"]["active"]) == 2
    assert result["counts"]["active_group_legs"] == 2


def test_discover_importable_only_candidate_missing_legs_4():
    client = FakeClient(
        active=[amarket(9, "Will it rain in London?")],                # active, but not a group leg
        importable=[amarket(1, "Will Mexico finish first in World Cup Group A?")],
    )
    result = discover(client)
    g = result["groups"]["A"]
    assert g["active"] == []
    assert len(g["importable"]) == 1
    assert g["missing_legs"] == 4
    assert g["complete_active_set"] is False
    assert result["counts"]["importable_group_candidates"] == 1


def test_discover_drops_importable_dup_of_active():
    client = FakeClient(
        active=[amarket(1, "Spain to win Group A")],
        importable=[amarket(2, "Spain to win Group A")],               # same question, upstream
    )
    result = discover(client)
    assert len(result["groups"]["A"]["active"]) == 1
    assert result["groups"]["A"]["importable"] == []                   # dropped as duplicate


def test_discover_complete_active_set():
    client = FakeClient(active=[amarket(i, f"Team{i} win Group A") for i in range(4)])
    result = discover(client)
    g = result["groups"]["A"]
    assert g["complete_active_set"] is True
    assert g["missing_legs"] == 0
    assert result["counts"]["complete_active_sets"] == 1


def test_discover_format_report_surfaces_importable_candidate():
    client = FakeClient(
        importable=[amarket(1, "Will Mexico finish first in World Cup Group A?")],
    )
    report = format_report(discover(client))
    assert isinstance(report, str)
    assert "Group A" in report
    assert "importable" in report.lower()
    assert "missing 4" in report


# === 5. find_group_sets (2) =====================================================================
def test_find_group_sets_active_only_deduped():
    client = FakeClient(active=[
        amarket(1, "win Group A"),
        amarket(1, "win Group A"),       # duplicate id -> collapses
        amarket(2, "win Group B"),
    ])
    groups = find_group_sets(client)
    assert len(groups["A"]) == 1
    assert "B" in groups


def test_find_group_sets_skips_inactive():
    client = FakeClient(active=[
        amarket(1, "win Group A", status="active"),
        amarket(2, "win Group A", status="closed"),
    ])
    groups = find_group_sets(client)
    assert len(groups["A"]) == 1


# === 6. is_confirmed_exclusive (2) ==============================================================
def test_is_confirmed_exclusive_clean_vs_broken_sets():
    clean = [amarket(i, f"Team{i} win Group A") for i in range(4)]
    assert is_confirmed_exclusive(clean) is True
    assert is_confirmed_exclusive(clean[:3]) is False                  # only 3 legs
    mixed = clean[:3] + [amarket(99, "Team99 win Group B")]
    assert is_confirmed_exclusive(mixed) is False                     # mixed letters


def test_is_confirmed_exclusive_rejects_advancement_leg():
    legs = [amarket(i, f"Team{i} win Group A") for i in range(3)]
    legs.append(amarket(99, "Team99 to advance from Group A"))        # non-winner family leg
    assert is_confirmed_exclusive(legs) is False
