import os
import json
from datetime import datetime
from db import init_db, accumulate_grid
from report import generate_report


class TestGenerateReport:
    def _seed_db(self, db_path):
        """向数据库写入测试数据"""
        init_db(db_path)
        accumulate_grid(
            db_path=db_path,
            camera_id="cam-001",
            detections=[{"col": 10, "row": 5}, {"col": 10, "row": 5}],
            window_start=datetime(2026, 5, 27, 10, 0, 0),
            window_end=datetime(2026, 5, 27, 10, 0, 5)
        )
        accumulate_grid(
            db_path=db_path,
            camera_id="cam-001",
            detections=[{"col": 20, "row": 15}] * 5,
            window_start=datetime(2026, 5, 27, 11, 0, 0),
            window_end=datetime(2026, 5, 27, 11, 0, 5)
        )

    def test_generates_html_file(self, tmp_dir, sample_image):
        db_path = os.path.join(tmp_dir, "test.db")
        self._seed_db(db_path)

        config = {
            "cameras": [{"id": "cam-001", "sn": "TEST", "name": "入口",
                         "password": "x", "grid_cols": 48, "grid_rows": 27}],
            "settings": {"confidence_threshold": 0.5}
        }

        output_path = os.path.join(tmp_dir, "report.html")
        generate_report(
            db_path=db_path,
            config=config,
            start=datetime(2026, 5, 27, 0, 0, 0),
            end=datetime(2026, 5, 28, 0, 0, 0),
            background_paths={"cam-001": sample_image},
            output_path=output_path
        )

        assert os.path.exists(output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "<!DOCTYPE html>" in content
        assert "__REPORT_DATA__" not in content

    def test_embeds_stats(self, tmp_dir, sample_image):
        db_path = os.path.join(tmp_dir, "test.db")
        self._seed_db(db_path)

        config = {
            "cameras": [{"id": "cam-001", "sn": "TEST", "name": "入口",
                         "password": "x", "grid_cols": 48, "grid_rows": 27}],
            "settings": {"confidence_threshold": 0.5}
        }

        output_path = os.path.join(tmp_dir, "report.html")
        generate_report(
            db_path=db_path,
            config=config,
            start=datetime(2026, 5, 27, 0, 0, 0),
            end=datetime(2026, 5, 28, 0, 0, 0),
            background_paths={"cam-001": sample_image},
            output_path=output_path
        )

        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()

        start_marker = "var REPORT_DATA = "
        idx = content.index(start_marker) + len(start_marker)
        end_idx = content.index(";", idx)
        data = json.loads(content[idx:end_idx])

        cam_data = data["cameras"][0]
        assert cam_data["stats"]["total_detections"] == 7
        assert cam_data["stats"]["peak_hour"] == 11
        assert cam_data["stats"]["capture_rounds"] == 2
