import os
import sqlite3
from datetime import datetime
from db import init_db, insert_detections, accumulate_grid
from db import query_grid, query_time_series, query_stats


class TestInitDb:
    def test_creates_tables(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        conn = sqlite3.connect(db_path)
        tables = {row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        conn.close()

        assert "cameras" in tables
        assert "detections" in tables
        assert "grid_heat" in tables

    def test_idempotent(self, tmp_dir):
        """重复调用 init_db 不报错"""
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)
        init_db(db_path)  # 不应抛异常


class TestInsertDetections:
    def test_inserts_record(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        insert_detections(
            db_path=db_path,
            camera_id="cam-001",
            timestamp=datetime(2026, 5, 27, 10, 0, 0),
            person_count=5,
            image_path="captures/cam001_20260527.jpg"
        )

        conn = sqlite3.connect(db_path)
        rows = conn.execute("SELECT * FROM detections").fetchall()
        conn.close()

        assert len(rows) == 1
        assert rows[0][1] == "cam-001"
        assert rows[0][3] == 5


class TestAccumulateGrid:
    def test_accumulates_counts(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        detections = [
            {"col": 10, "row": 5},
            {"col": 10, "row": 5},  # 同一格子第二次
            {"col": 20, "row": 15},
        ]
        window_start = datetime(2026, 5, 27, 10, 0, 0)
        window_end = datetime(2026, 5, 27, 10, 0, 5)

        accumulate_grid(
            db_path=db_path,
            camera_id="cam-001",
            detections=detections,
            window_start=window_start,
            window_end=window_end
        )

        conn = sqlite3.connect(db_path)
        rows = conn.execute(
            "SELECT grid_row, grid_col, heat_count FROM grid_heat "
            "ORDER BY grid_row, grid_col"
        ).fetchall()
        conn.close()

        assert len(rows) == 2
        assert rows[0] == (5, 10, 2)
        assert rows[1] == (15, 20, 1)

    def test_empty_detections_no_rows(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        accumulate_grid(
            db_path=db_path,
            camera_id="cam-001",
            detections=[],
            window_start=datetime(2026, 5, 27, 10, 0, 0),
            window_end=datetime(2026, 5, 27, 10, 0, 5)
        )

        conn = sqlite3.connect(db_path)
        rows = conn.execute("SELECT * FROM grid_heat").fetchall()
        conn.close()

        assert len(rows) == 0


class TestQueryGrid:
    def test_aggregates_across_windows(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        for minute in [0, 5]:
            accumulate_grid(
                db_path=db_path,
                camera_id="cam-001",
                detections=[{"col": 10, "row": 5}],
                window_start=datetime(2026, 5, 27, 10, minute, 0),
                window_end=datetime(2026, 5, 27, 10, minute, 5)
            )

        result = query_grid(
            db_path=db_path,
            camera_id="cam-001",
            start=datetime(2026, 5, 27, 0, 0, 0),
            end=datetime(2026, 5, 28, 0, 0, 0)
        )

        assert len(result) == 1
        assert result[0]["grid_row"] == 5
        assert result[0]["grid_col"] == 10
        assert result[0]["heat_count"] == 2

    def test_filters_by_time_range(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        accumulate_grid(
            db_path=db_path,
            camera_id="cam-001",
            detections=[{"col": 10, "row": 5}],
            window_start=datetime(2026, 5, 20, 10, 0, 0),
            window_end=datetime(2026, 5, 20, 10, 0, 5)
        )

        result = query_grid(
            db_path=db_path,
            camera_id="cam-001",
            start=datetime(2026, 5, 27, 0, 0, 0),
            end=datetime(2026, 5, 28, 0, 0, 0)
        )

        assert len(result) == 0


class TestQueryTimeSeries:
    def test_groups_by_interval(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        for count, hour in [(3, 10), (5, 11)]:
            accumulate_grid(
                db_path=db_path,
                camera_id="cam-001",
                detections=[{"col": i, "row": 0} for i in range(count)],
                window_start=datetime(2026, 5, 27, hour, 0, 0),
                window_end=datetime(2026, 5, 27, hour, 0, 5)
            )

        result = query_time_series(
            db_path=db_path,
            camera_id="cam-001",
            start=datetime(2026, 5, 27, 0, 0, 0),
            end=datetime(2026, 5, 28, 0, 0, 0)
        )

        by_time = {r["time"]: r["count"] for r in result}
        assert by_time.get("10:00") == 3
        assert by_time.get("11:00") == 5


class TestQueryStats:
    def test_returns_summary(self, tmp_dir):
        db_path = os.path.join(tmp_dir, "test.db")
        init_db(db_path)

        accumulate_grid(
            db_path=db_path,
            camera_id="cam-001",
            detections=[{"col": 10, "row": 5}, {"col": 10, "row": 5}, {"col": 20, "row": 15}],
            window_start=datetime(2026, 5, 27, 11, 0, 0),
            window_end=datetime(2026, 5, 27, 11, 0, 5)
        )

        stats = query_stats(
            db_path=db_path,
            camera_id="cam-001",
            start=datetime(2026, 5, 27, 0, 0, 0),
            end=datetime(2026, 5, 28, 0, 0, 0)
        )

        assert stats["total_detections"] == 3
        assert stats["peak_hour"] == 11
        assert stats["hottest_cell"] == {"row": 5, "col": 10, "count": 2}
        assert stats["capture_rounds"] == 1
