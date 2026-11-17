import os
import numpy as np
import cv2
from heatmap import render_heatmap_overlay, grid_to_heatmap_image


class TestGridToHeatmapImage:
    def test_output_dimensions(self):
        """输出图片尺寸应与背景图一致"""
        bg = np.zeros((1080, 1920, 3), dtype=np.uint8)
        grid_data = [{"grid_row": 5, "grid_col": 10, "heat_count": 10}]

        result = grid_to_heatmap_image(
            background=bg,
            grid_data=grid_data,
            grid_cols=48,
            grid_rows=27
        )

        assert result.shape == (1080, 1920, 3)

    def test_hot_cells_differ_from_cold(self):
        """热度不同的格子应该呈现不同颜色"""
        bg = np.zeros((1080, 1920, 3), dtype=np.uint8)
        grid_data = [
            {"grid_row": 0, "grid_col": 0, "heat_count": 1},
            {"grid_row": 0, "grid_col": 1, "heat_count": 100},
        ]

        result = grid_to_heatmap_image(bg, grid_data, 48, 27)

        cell_h = 1080 // 27
        cell_w = 1920 // 48
        cold_pixel = result[cell_h // 2, cell_w // 2]
        hot_pixel = result[cell_h // 2, cell_w + cell_w // 2]

        # 两个格子的颜色应该不同
        assert not np.array_equal(cold_pixel, hot_pixel)
        # 两个格子都应该有颜色（不是纯黑背景）
        assert int(cold_pixel.sum()) > 0
        assert int(hot_pixel.sum()) > 0


class TestRenderHeatmapOverlay:
    def test_saves_png(self, sample_image, tmp_dir):
        """应输出有效的 PNG 文件"""
        grid_data = [
            {"grid_row": 5, "grid_col": 10, "heat_count": 50},
            {"grid_row": 15, "grid_col": 30, "heat_count": 20},
        ]
        output_path = os.path.join(tmp_dir, "heatmap.png")

        render_heatmap_overlay(
            background_path=sample_image,
            grid_data=grid_data,
            grid_cols=48,
            grid_rows=27,
            output_path=output_path
        )

        assert os.path.exists(output_path)
        img = cv2.imread(output_path)
        assert img is not None
        assert img.shape == (1080, 1920, 3)
