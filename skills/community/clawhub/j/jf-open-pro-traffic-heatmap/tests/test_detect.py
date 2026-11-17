import os
import numpy as np
import cv2
from unittest.mock import patch, MagicMock
from detect import compute_anchor, map_to_grid, detect_heads


class TestComputeAnchor:
    def test_bottom_center(self):
        """锚点 = 头部 bbox 底部中心"""
        bbox = [100, 200, 160, 280]  # x1, y1, x2, y2
        anchor = compute_anchor(bbox)
        assert anchor == (130.0, 280.0)

    def test_small_bbox(self):
        bbox = [500, 300, 520, 320]
        anchor = compute_anchor(bbox)
        assert anchor == (510.0, 320.0)


class TestMapToGrid:
    def test_maps_to_correct_cell(self):
        """1920x1080 画面, 48x27 网格, 每格 40x40"""
        col, row = map_to_grid(
            anchor_x=130.0, anchor_y=280.0,
            image_width=1920, image_height=1080,
            grid_cols=48, grid_rows=27
        )
        assert col == 3   # 130 / 40 = 3.25 -> 3
        assert row == 7   # 280 / 40 = 7.0 -> 7

    def test_out_of_bounds_returns_none(self):
        result = map_to_grid(
            anchor_x=2000.0, anchor_y=280.0,
            image_width=1920, image_height=1080,
            grid_cols=48, grid_rows=27
        )
        assert result is None

    def test_edge_of_image(self):
        col, row = map_to_grid(
            anchor_x=1919.0, anchor_y=1079.0,
            image_width=1920, image_height=1080,
            grid_cols=48, grid_rows=27
        )
        assert col == 47
        assert row == 26


class TestDetectHeads:
    def test_with_mock_model(self, sample_image):
        """使用 mock 模型测试完整检测流程"""
        mock_model = MagicMock()

        mock_results = MagicMock()
        mock_box = MagicMock()
        mock_box.__len__ = lambda self: 3
        mock_box.xyxy = MagicMock()
        mock_box.xyxy.cpu.return_value.numpy.return_value = np.array([
            [290, 380, 370, 430],
            [790, 330, 860, 380],
            [1190, 480, 1250, 530]
        ])
        mock_box.conf = MagicMock()
        mock_box.conf.cpu.return_value.numpy.return_value = np.array([0.9, 0.85, 0.7])

        mock_result_item = MagicMock()
        mock_result_item.boxes = mock_box
        mock_results.__iter__ = lambda self: iter([mock_result_item])
        mock_model.return_value = mock_results

        detections = detect_heads(
            image_path=sample_image,
            model=mock_model,
            confidence=0.5,
            grid_cols=48,
            grid_rows=27
        )

        assert len(detections) == 3
        for d in detections:
            assert "col" in d
            assert "row" in d
            assert "confidence" in d

    def test_filters_low_confidence(self, sample_image):
        """低于置信度阈值的检测应被过滤"""
        mock_model = MagicMock()
        mock_box = MagicMock()
        mock_box.__len__ = lambda self: 1
        mock_box.xyxy.cpu.return_value.numpy.return_value = np.array([
            [100, 100, 150, 150]
        ])
        mock_box.conf.cpu.return_value.numpy.return_value = np.array([0.3])

        mock_result_item = MagicMock()
        mock_result_item.boxes = mock_box
        mock_model.return_value = [mock_result_item]

        detections = detect_heads(
            image_path=sample_image,
            model=mock_model,
            confidence=0.5,
            grid_cols=48,
            grid_rows=27
        )

        assert len(detections) == 0
