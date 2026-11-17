"""Journal tests — the accounting that underpins the financial caps.

Each test here corresponds to a bug found in the 2.0.0 code review. These are
ACCOUNTING bugs, not validation bugs: the guard-rail was correct, but it was
being fed the wrong numbers.
"""
from __future__ import annotations

import os
import tempfile
import time
import unittest
from pathlib import Path

os.environ.setdefault("POLYMARKET_AGENT_HOME", tempfile.mkdtemp(prefix="polyjournal-"))

from polymarket_agent import journal  # noqa: E402
from polymarket_agent.paths import journal_path  # noqa: E402


class JournalAccountingTest(unittest.TestCase):
    def setUp(self) -> None:
        home = Path(os.environ["POLYMARKET_AGENT_HOME"])
        for name in ("journal.jsonl", "journal.jsonl.1"):
            (home / name).unlink(missing_ok=True)

    # ── Rotation must not zero the budget ──────────────────────────────────
    def test_rotation_does_not_reset_daily_spend(self):
        """BUG: rotating the journal freed the entire daily cap."""
        journal.record(
            journal.Entry(status="submitted", side="BUY", notional=80.0, token_id="1")
        )
        self.assertEqual(journal.spend_since(86400), 80.0)

        # Simulate rotation by size.
        journal_path().replace(journal_path().with_suffix(".jsonl.1"))
        journal.record(
            journal.Entry(status="submitted", side="BUY", notional=5.0, token_id="2")
        )

        self.assertEqual(
            journal.spend_since(86400), 85.0,
            "spend from the rotated file must keep counting",
        )

    # ── first_ts preserved ─────────────────────────────────────────────────
    def test_status_update_does_not_move_order_into_window(self):
        """BUG: updating the status rewrote `ts`, dragging old orders into the
        24h window (and inflating the day's spend)."""
        old = journal.Entry(status="submitted", side="BUY", notional=50.0, token_id="1")
        old.ts = time.time() - (48 * 3600)  # 2 days ago
        journal.record(old)
        self.assertEqual(journal.spend_since(86400), 0.0)

        journal.update_status(old.id, "filled")  # update NOW

        self.assertEqual(
            journal.spend_since(86400), 0.0,
            "an order from 2 days ago must not enter the window because of an update",
        )

    def test_first_ts_is_recorded(self):
        entry = journal.record(journal.Entry(status="submitted", side="BUY", notional=1.0))
        journal.update_status(entry.id, "filled")
        row = journal.latest_by_id()[entry.id]
        self.assertIn("first_ts", row)
        self.assertEqual(row["status"], "filled")
        self.assertAlmostEqual(row["first_ts"], entry.ts, places=3)

    # ── Open order count ───────────────────────────────────────────────────
    def test_open_count_ignores_stale_entries(self):
        """BUG (P0): the counter only ever grew. On hitting max_open_orders the
        skill blocked all trading permanently."""
        stale = journal.Entry(status="submitted", side="BUY", notional=1.0, token_id="1")
        stale.ts = time.time() - (journal.STALE_OPEN_SECONDS + 60)
        journal.record(stale)
        self.assertEqual(journal.open_order_count(), 0)

        fresh = journal.Entry(status="submitted", side="BUY", notional=1.0, token_id="2")
        journal.record(fresh)
        self.assertEqual(journal.open_order_count(), 1)

    def test_terminal_statuses_are_not_open(self):
        for status in ("filled", "rejected", "failed", "cancelled", "closed", "dry_run"):
            journal.record(
                journal.Entry(status=status, side="BUY", notional=1.0, token_id="x")
            )
        self.assertEqual(journal.open_order_count(), 0)

    # ── Reconciliation with the exchange ───────────────────────────────────
    def test_reconcile_closes_orders_absent_from_exchange(self):
        alive = journal.record(
            journal.Entry(status="submitted", side="BUY", notional=1.0, order_id="AAA")
        )
        dead = journal.record(
            journal.Entry(status="submitted", side="BUY", notional=1.0, order_id="BBB")
        )
        self.assertEqual(journal.open_order_count(), 2)

        closed = journal.reconcile_open_orders(["AAA"])

        self.assertEqual(closed, 1)
        self.assertEqual(journal.open_order_count(), 1)
        self.assertEqual(journal.latest_by_id()[dead.id]["status"], "closed")
        self.assertEqual(journal.latest_by_id()[alive.id]["status"], "submitted")

    def test_reconcile_keeps_entries_without_order_id(self):
        """With no order_id we cannot assert the order died — it may have failed
        before the exchange answered. Closing it would lose the trail."""
        entry = journal.record(
            journal.Entry(status="submitted", side="BUY", notional=1.0, order_id="")
        )
        journal.reconcile_open_orders(["OTHER"])
        self.assertEqual(journal.latest_by_id()[entry.id]["status"], "submitted")

    def test_reconcile_does_not_reopen_daily_budget(self):
        """Reconciling closes the order, but the money was already spent."""
        journal.record(
            journal.Entry(status="submitted", side="BUY", notional=40.0, order_id="XYZ")
        )
        journal.reconcile_open_orders([])
        self.assertEqual(
            journal.spend_since(86400), 40.0,
            "an order closed by reconciliation still consumed capital",
        )

    # ── Cancellation ───────────────────────────────────────────────────────
    def test_cancel_closes_original_entry(self):
        """BUG: cancelling wrote a new line; the original stayed `submitted`."""
        entry = journal.record(
            journal.Entry(status="submitted", side="BUY", notional=1.0, order_id="C1")
        )
        self.assertTrue(journal.close_by_order_id("C1", "cancelled"))
        self.assertEqual(journal.latest_by_id()[entry.id]["status"], "cancelled")
        self.assertEqual(journal.open_order_count(), 0)

    def test_cancel_unknown_order_id_reports_false(self):
        self.assertFalse(journal.close_by_order_id("DOES-NOT-EXIST"))

    def test_close_all_open_closes_everything(self):
        for i in range(3):
            journal.record(
                journal.Entry(status="submitted", side="BUY", notional=1.0, order_id=f"O{i}")
            )
        self.assertEqual(journal.close_all_open("cancelled"), 3)
        self.assertEqual(journal.open_order_count(), 0)

    # ── Robustness ─────────────────────────────────────────────────────────
    def test_corrupt_lines_are_skipped(self):
        journal.record(journal.Entry(status="submitted", side="BUY", notional=7.0))
        with open(journal_path(), "a", encoding="utf-8") as fh:
            fh.write("{ this is not json\n\n")
        journal.record(journal.Entry(status="submitted", side="BUY", notional=3.0))
        self.assertEqual(journal.spend_since(86400), 10.0)


class TradeLockTest(unittest.TestCase):
    """BUG: two processes could bust the daily cap simultaneously."""

    def test_lock_is_exclusive_across_processes(self):
        import subprocess
        import sys

        script = (
            "import os,sys,time;"
            "from polymarket_agent.paths import trade_lock;"
            "lock=trade_lock(timeout=30);lock.__enter__();"
            "print('LOCKED',flush=True);time.sleep(3);lock.__exit__()"
        )
        holder = subprocess.Popen(
            [sys.executable, "-c", script],
            stdout=subprocess.PIPE, text=True, env=dict(os.environ),
        )
        try:
            self.assertEqual(holder.stdout.readline().strip(), "LOCKED")
            start = time.monotonic()
            with self.assertRaises(TimeoutError):
                with trade_lock_short():
                    pass
            self.assertLess(time.monotonic() - start, 3.0)
        finally:
            holder.kill()
            holder.wait()
            if holder.stdout:
                holder.stdout.close()

    def test_lock_is_reentrant_after_release(self):
        from polymarket_agent.paths import trade_lock

        with trade_lock(timeout=5):
            pass
        with trade_lock(timeout=5):
            pass  # must not block


def trade_lock_short():
    from polymarket_agent.paths import trade_lock

    return trade_lock(timeout=0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
