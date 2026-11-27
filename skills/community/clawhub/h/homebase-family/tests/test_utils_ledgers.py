"""
test_utils_ledgers.py — the bounded, ordered ID ledger helper.

append_capped_id is shared infrastructure behind three dedup ledgers (school
processed, school calendar-synced, bills processed) and had no direct test.
The invariant that matters is ORDER: the cap must be applied to the ordered
on-disk list, never to a set. `list(some_set)[-500:]` reads as "keep the newest
500" and is not — which 500 survive is a hash-ordering accident, and a dropped
id means an already-handled email comes back as a duplicate school calendar
proposal or a bill posted to the family group twice.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import append_capped_id


class TestAppendCappedId:
    def test_it_keeps_the_newest_ids_at_the_cap(self):
        ids = []
        for i in range(12):
            ids = append_capped_id(ids, f"m{i}", cap=10)
        assert ids == [f"m{i}" for i in range(2, 12)]

    def test_it_preserves_insertion_order(self):
        assert append_capped_id(["a", "b"], "c") == ["a", "b", "c"]

    def test_it_appends_to_an_empty_ledger(self):
        assert append_capped_id([], "only") == ["only"]

    def test_it_does_not_duplicate_a_known_id(self):
        assert append_capped_id(["a", "b"], "a") == ["a", "b"]

    def test_re_marking_an_old_id_does_not_refresh_its_recency(self):
        """dict.fromkeys keeps the FIRST occurrence's position, so an id near
        the head stays near the head and is evicted at the cap even though it
        was just handled again. Defensible, but pin it: the alternative
        (refreshing recency) is what a reader would assume."""
        ids = ["a", "b", "c"]
        assert append_capped_id(ids, "a", cap=3) == ["a", "b", "c"]

    def test_the_cap_is_exact(self):
        ids = [f"m{i}" for i in range(500)]
        out = append_capped_id(ids, "new", cap=500)
        assert len(out) == 500
        assert out[-1] == "new"
        assert out[0] == "m1"


class TestLockedFileIsBounded:
    """The lock guards read-modify-write on state files, and this diff put it
    on the 6:05 AM briefing path. A blocking flock with no deadline means a
    stuck holder stops the briefing from ever sending — strictly worse than
    sending without the bookkeeping the lock protects."""

    def test_the_acquire_gives_up_rather_than_waiting_forever(self, tmp_path):
        import fcntl
        import time
        import pytest
        from utils import locked_file

        target = str(tmp_path / "state.json")
        with open(target + ".lock", "a") as holder:
            fcntl.flock(holder, fcntl.LOCK_EX)
            started = time.monotonic()
            with pytest.raises(TimeoutError):
                with locked_file(target, timeout=0.3):
                    pass
            assert time.monotonic() - started < 5, "the acquire was unbounded"

    def test_an_uncontended_lock_still_works(self, tmp_path):
        from utils import locked_file, write_json_atomic
        target = str(tmp_path / "state.json")
        with locked_file(target, timeout=1.0):
            write_json_atomic(target, {"ok": True})
        with locked_file(target, timeout=1.0):
            pass


class TestLedgerWritesAreCrossProcessSafe:
    """The real property: two processes marking ids at the same time must not
    lose one. A dropped school id re-proposes events to the shared family
    calendar; a dropped bill id posts the bill to the group twice."""

    def test_concurrent_markers_all_survive(self, tmp_path):
        import json
        import subprocess
        import sys as _sys
        from pathlib import Path as _P

        skill_dir = str(_P(__file__).parent.parent)
        ledger = tmp_path / "processed.json"
        ledger.write_text("[]")

        prog = (
            "import sys, json;"
            "sys.path.insert(0, sys.argv[1]);"
            "from utils import locked_file, append_capped_id, read_id_list, write_json_atomic;"
            "p = sys.argv[2];"
            "\n"
            "with locked_file(p, timeout=30):\n"
            "    ids = append_capped_id(read_id_list(p), sys.argv[3])\n"
            "    write_json_atomic(p, ids)\n"
        )
        procs = [
            subprocess.Popen([_sys.executable, "-c", prog, skill_dir, str(ledger), f"m{i}"])
            for i in range(8)
        ]
        for p in procs:
            assert p.wait(timeout=60) == 0

        ids = json.loads(ledger.read_text())
        assert sorted(ids) == sorted(f"m{i}" for i in range(8)), \
            f"a concurrent marker was lost: {ids}"
