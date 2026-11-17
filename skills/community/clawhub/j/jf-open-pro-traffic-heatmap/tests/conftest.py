import os
import sys
import json
import tempfile
import pytest
import numpy as np
import cv2

# 让测试能导入 scripts 目录的模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))


@pytest.fixture
def tmp_dir():
    """提供临时目录，测试结束后自动清理"""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def sample_config(tmp_dir):
    """创建示例摄像头配置"""
    config = {
        "cameras": [
            {
                "id": "cam-001",
                "sn": "JFTEST0001",
                "name": "入口",
                "password": "test123",
                "grid_cols": 48,
                "grid_rows": 27
            },
            {
                "id": "cam-002",
                "sn": "JFTEST0002",
                "name": "办公区",
                "password": "test456",
                "grid_cols": 48,
                "grid_rows": 27
            }
        ],
        "settings": {
            "capture_interval_minutes": 5,
            "confidence_threshold": 0.5,
            "image_retention_days": 7
        }
    }
    path = os.path.join(tmp_dir, "cameras.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False)
    return path


@pytest.fixture
def sample_image(tmp_dir):
    """创建一张 1920x1080 的测试图片"""
    img = np.zeros((1080, 1920, 3), dtype=np.uint8)
    cv2.rectangle(img, (300, 400), (360, 700), (200, 180, 160), -1)
    cv2.rectangle(img, (800, 350), (850, 680), (190, 170, 150), -1)
    cv2.rectangle(img, (1200, 500), (1240, 750), (180, 160, 140), -1)
    path = os.path.join(tmp_dir, "test_frame.jpg")
    cv2.imwrite(path, img)
    return path


@pytest.fixture
def sample_config_data():
    """返回配置字典（不写文件）"""
    return {
        "cameras": [
            {
                "id": "cam-001",
                "sn": "JFTEST0001",
                "name": "入口",
                "password": "test123",
                "grid_cols": 48,
                "grid_rows": 27
            }
        ],
        "settings": {
            "capture_interval_minutes": 5,
            "confidence_threshold": 0.5,
            "image_retention_days": 7
        }
    }
