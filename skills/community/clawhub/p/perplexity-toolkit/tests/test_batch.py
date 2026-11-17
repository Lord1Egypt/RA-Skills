"""Tests for perplexity_toolkit.batch — query loading and the batch pipeline."""

import csv
import json

import pytest

from perplexity_toolkit import batch
from perplexity_toolkit.config import Config


class TestLoadQueries:
    def test_inline_string_when_path_does_not_exist(self):
        assert batch.load_queries("what is the meaning of life") == [
            {"query": "what is the meaning of life", "mode": "search"},
        ]

    def test_json_list_of_strings(self, tmp_path):
        p = tmp_path / "q.json"
        p.write_text(json.dumps(["q1", "q2"]))
        assert batch.load_queries(str(p)) == [
            {"query": "q1", "mode": "search"},
            {"query": "q2", "mode": "search"},
        ]

    def test_json_list_of_dicts(self, tmp_path):
        p = tmp_path / "q.json"
        p.write_text(json.dumps([
            {"query": "q1", "mode": "deep_research"},
            {"query": "q2"},
        ]))
        assert batch.load_queries(str(p)) == [
            {"query": "q1", "mode": "deep_research"},
            {"query": "q2", "mode": "search"},
        ]

    def test_json_single_dict(self, tmp_path):
        p = tmp_path / "q.json"
        p.write_text(json.dumps({"query": "q1", "mode": "model_council"}))
        assert batch.load_queries(str(p)) == [
            {"query": "q1", "mode": "model_council"},
        ]

    def test_json_empty_list_falls_back_to_inline(self, tmp_path):
        p = tmp_path / "q.json"
        p.write_text(json.dumps([]))
        assert batch.load_queries(str(p)) == [{"query": str(p), "mode": "search"}]

    def test_csv(self, tmp_path):
        p = tmp_path / "q.csv"
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["query", "mode"])
            w.writerow(["q1", "search"])
            w.writerow(["q2", "deep_research"])
        assert batch.load_queries(str(p)) == [
            {"query": "q1", "mode": "search"},
            {"query": "q2", "mode": "deep_research"},
        ]

    def test_csv_falls_back_to_q_column(self, tmp_path):
        p = tmp_path / "q.csv"
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["q", "mode"])
            w.writerow(["q1", "model_council"])
        assert batch.load_queries(str(p)) == [
            {"query": "q1", "mode": "model_council"},
        ]

    def test_csv_without_query_column_falls_back_to_inline(self, tmp_path):
        p = tmp_path / "q.csv"
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["mode"])
            w.writerow(["search"])
        assert batch.load_queries(str(p)) == [{"query": str(p), "mode": "search"}]

    def test_txt(self, tmp_path):
        p = tmp_path / "q.txt"
        p.write_text("q1\n\n  q2 with spaces  \n")
        assert batch.load_queries(str(p)) == [
            {"query": "q1", "mode": "search"},
            {"query": "q2 with spaces", "mode": "search"},
        ]

    def test_txt_empty_falls_back_to_inline(self, tmp_path):
        p = tmp_path / "q.txt"
        p.write_text("\n\n")
        assert batch.load_queries(str(p)) == [{"query": str(p), "mode": "search"}]


def _fake_search_factory(calls):
    """Return a fake mode function that records queries and returns canned data."""

    def fn(query, config=None):
        calls.append(query)
        return {
            "answer": f"answer for {query}",
            "sources": [{"text": "Src", "href": "https://example.com/x"}],
            "url": f"https://www.perplexity.ai/search/{query}",
            "title": "title",
            "follow_ups": [],
            "mode": "search",
        }

    return fn


class TestRunBatch:
    def test_runs_all_queries_and_writes_output_and_progress(self, tmp_path, monkeypatch):
        calls = []
        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": _fake_search_factory(calls)})
        out = tmp_path / "out.json"
        prog = tmp_path / "progress.txt"

        results = batch.run_batch(
            [{"query": "q1", "mode": "search"}, {"query": "q2", "mode": "search"}],
            output_file=str(out),
            config=Config(batch_delay=0.0),
            progress_file=str(prog),
        )

        assert calls == ["q1", "q2"]
        assert [r["query"] for r in results] == ["q1", "q2"]
        assert results[0]["mode"] == "search"
        assert "searched_at" in results[0]
        assert json.loads(out.read_text()) == results
        assert prog.read_text().splitlines() == ["q1|||search", "q2|||search"]

    def test_resume_skips_done_queries(self, tmp_path, monkeypatch):
        calls = []
        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": _fake_search_factory(calls)})
        prog = tmp_path / "progress.txt"
        prog.write_text("q1|||search\nq2|||search\n")
        out = tmp_path / "out.json"

        results = batch.run_batch(
            [{"query": "q1", "mode": "search"},
             {"query": "q2", "mode": "search"},
             {"query": "q3", "mode": "search"}],
            output_file=str(out),
            config=Config(batch_delay=0.0),
            progress_file=str(prog),
            resume=True,
        )

        assert calls == ["q3"]
        assert [r["query"] for r in results] == ["q3"]
        # completed queries stay in the file; the new one is appended
        assert prog.read_text().splitlines() == ["q1|||search", "q2|||search", "q3|||search"]

    def test_resume_ignored_without_progress_file(self, tmp_path, monkeypatch):
        calls = []
        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": _fake_search_factory(calls)})
        results = batch.run_batch(
            [{"query": "q1", "mode": "search"}, {"query": "q2", "mode": "search"}],
            output_file=str(tmp_path / "out.json"),
            config=Config(batch_delay=0.0),
            resume=True,
        )
        assert calls == ["q1", "q2"]
        assert len(results) == 2

    def test_failed_search_not_marked_done(self, tmp_path, monkeypatch):
        def failing(query, config=None):
            raise RuntimeError("network exploded")

        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": failing})
        prog = tmp_path / "progress.txt"
        out = tmp_path / "out.json"

        results = batch.run_batch(
            [{"query": "q1", "mode": "search"}],
            output_file=str(out),
            config=Config(batch_delay=0.0),
            progress_file=str(prog),
        )

        assert "error" in results[0]
        assert "network exploded" in results[0]["error"]
        assert results[0]["query"] == "q1"
        # failed searches must NOT be marked done, so resume retries them
        assert not prog.exists()

    def test_failed_search_rerun_on_resume(self, tmp_path, monkeypatch):
        calls = []

        def flaky(query, config=None):
            if not calls:
                calls.append(query)
                raise RuntimeError("first attempt fails")
            calls.append(query)
            return {"answer": "ok now", "sources": [], "url": "",
                    "title": "", "follow_ups": [], "mode": "search"}

        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": flaky})
        prog = tmp_path / "progress.txt"
        out = tmp_path / "out.json"
        cfg = Config(batch_delay=0.0)

        first = batch.run_batch(
            [{"query": "q1", "mode": "search"}],
            output_file=str(out), config=cfg, progress_file=str(prog),
        )
        assert "error" in first[0]

        second = batch.run_batch(
            [{"query": "q1", "mode": "search"}],
            output_file=str(out), config=cfg, progress_file=str(prog), resume=True,
        )
        assert calls == ["q1", "q1"]  # re-run, not skipped
        assert second[0]["answer"] == "ok now"
        assert prog.read_text().splitlines() == ["q1|||search"]

    def test_empty_query_skipped_as_invalid(self, tmp_path, monkeypatch):
        calls = []
        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": _fake_search_factory(calls)})
        out = tmp_path / "out.json"
        results = batch.run_batch(
            [{"query": "", "mode": "search"}],
            output_file=str(out), config=Config(batch_delay=0.0),
        )
        assert results == []
        assert calls == []
        assert json.loads(out.read_text()) == []

    def test_unknown_mode_skipped_as_invalid(self, tmp_path, monkeypatch):
        calls = []
        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": _fake_search_factory(calls)})
        out = tmp_path / "out.json"
        results = batch.run_batch(
            [{"query": "q1", "mode": "quantum_mode"}],
            output_file=str(out), config=Config(batch_delay=0.0),
        )
        assert results == []
        assert calls == []

    def test_all_skipped_still_writes_output(self, tmp_path, monkeypatch):
        monkeypatch.setattr(batch, "MODE_FUNCTIONS", {"search": _fake_search_factory([])})
        prog = tmp_path / "p"
        prog.write_text("q1|||search\n")
        out = tmp_path / "out.json"
        batch.run_batch(
            [{"query": "q1", "mode": "search"}],
            output_file=str(out), config=Config(batch_delay=0.0),
            progress_file=str(prog), resume=True,
        )
        assert json.loads(out.read_text()) == []