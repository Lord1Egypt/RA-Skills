"""YOLOv8 头部检测 — 检测、锚点计算、网格映射"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

# 模型权重查找路径（优先级从高到低）
MODEL_PATHS = [
    os.path.join(SKILL_DIR, "models", "head-yolov8m.pt"),
    os.path.join(SKILL_DIR, "models", "head-yolov8s.pt"),
    os.path.join(SKILL_DIR, "data", "models", "head-yolov8m.pt"),
    os.path.join(SKILL_DIR, "data", "models", "head-yolov8s.pt"),
]

# 模型下载地址（GitHub 仓库原始文件）
MODEL_DOWNLOAD_URLS = [
    ("head-yolov8m.pt", "https://github.com/Abcfsa/YOLOv8_head_detector/raw/main/medium.pt"),
    ("head-yolov8s.pt", "https://github.com/Abcfsa/YOLOv8_head_detector/raw/main/nano.pt"),
]


def _download_model(save_dir: str, max_retries: int = 3) -> bool:
    """从 GitHub 下载模型权重文件，失败自动重试，返回是否成功"""
    import urllib.request
    import time

    os.makedirs(save_dir, exist_ok=True)

    for filename, url in MODEL_DOWNLOAD_URLS:
        target = os.path.join(save_dir, filename)
        if os.path.exists(target):
            return True
        for attempt in range(1, max_retries + 1):
            print(f"正在下载模型 {filename}（第 {attempt}/{max_retries} 次）...", file=sys.stderr)
            try:
                urllib.request.urlretrieve(url, target)
                print(f"模型已下载: {target}", file=sys.stderr)
                return True
            except Exception as e:
                print(f"下载失败: {e}", file=sys.stderr)
                if os.path.exists(target):
                    os.remove(target)
                if attempt < max_retries:
                    wait = attempt * 5
                    print(f"等待 {wait} 秒后重试...", file=sys.stderr)
                    time.sleep(wait)

    return False


def load_model(model_path: Optional[str] = None, data_dir: Optional[str] = None):
    """
    加载 YOLOv8 模型。

    模型文件全局共享（始终在 SKILL_DIR/models/），不随 data_dir 隔离。
    按优先级查找: 指定路径 -> 打包路径 -> 自动下载到 SKILL_DIR/models。
    下载失败抛出异常，不回退到 COCO 检测器。
    返回 (model, is_fallback)，is_fallback 始终为 False。
    """
    from ultralytics import YOLO

    if model_path and os.path.exists(model_path):
        return YOLO(model_path), False

    for path in MODEL_PATHS:
        if os.path.exists(path):
            return YOLO(path), False

    # 自动下载到技能目录（全局共享）
    models_dir = os.path.join(SKILL_DIR, "models")
    if _download_model(models_dir):
        for path in MODEL_PATHS:
            if os.path.exists(path):
                return YOLO(path), False

    urls = "\n".join(f"  - {name}: {url}" for name, url in MODEL_DOWNLOAD_URLS)
    raise RuntimeError(
        f"未找到头部检测模型，自动下载也失败了。\n"
        f"请手动下载后放入 {models_dir}/ 目录：\n{urls}"
    )


def compute_anchor(bbox: List[float]) -> Tuple[float, float]:
    """
    计算头部 bbox 的锚点（底部中心）。

    bbox: [x1, y1, x2, y2]
    返回: (cx, y2)
    """
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2.0
    return (cx, float(y2))


def map_to_grid(anchor_x: float, anchor_y: float,
                image_width: int, image_height: int,
                grid_cols: int, grid_rows: int) -> Optional[Tuple[int, int]]:
    """
    将锚点坐标映射到网格坐标。

    返回 (col, row)，超出范围返回 None。
    """
    cell_w = image_width / grid_cols
    cell_h = image_height / grid_rows

    col = int(anchor_x / cell_w)
    row = int(anchor_y / cell_h)

    if col < 0 or col >= grid_cols or row < 0 or row >= grid_rows:
        return None

    return (col, row)


def detect_heads(image_path: str, model, confidence: float,
                 grid_cols: int, grid_rows: int) -> List[Dict[str, Any]]:
    """
    对一张图片执行头部检测并映射到网格坐标。

    返回: [{"col": int, "row": int, "confidence": float}, ...]
    """
    img = cv2.imread(image_path)
    if img is None:
        return []

    h, w = img.shape[:2]
    results = model(image_path, conf=confidence, verbose=False)

    detections = []
    for result in results:
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            continue

        xyxy = boxes.xyxy.cpu().numpy()
        confs = boxes.conf.cpu().numpy()

        for i in range(len(xyxy)):
            if confs[i] < confidence:
                continue

            anchor = compute_anchor(xyxy[i].tolist())
            grid_pos = map_to_grid(anchor[0], anchor[1], w, h, grid_cols, grid_rows)

            if grid_pos is not None:
                col, row = grid_pos
                detections.append({
                    "col": col,
                    "row": row,
                    "confidence": float(confs[i])
                })

    return detections


def _parse_capture_time(filename: str) -> Optional[datetime]:
    """从文件名解析抓拍时间，支持多种命名格式"""
    import re
    name = os.path.splitext(filename)[0]
    # 尝试匹配 YYYYMMDDHHMMSS（连续14位数字）
    m = re.search(r'(\d{14})', name)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y%m%d%H%M%S")
        except ValueError:
            pass
    # 尝试匹配 YYYYMMDD_HHMMSS（下划线分隔）
    m = re.search(r'(\d{8})_(\d{6})', name)
    if m:
        try:
            return datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
        except ValueError:
            pass
    return None


def process_images(image_dir: str, config: dict, db_path: str,
                   data_dir: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    处理一个目录下所有抓拍图片（跳过已处理过的）。

    每张图片使用文件名中的抓拍时间作为 window_start，
    确保不同时间的抓拍有独立的采集轮次。

    data_dir: 会话数据目录，用于模型查找和下载。
    返回每个摄像头的检测结果摘要。
    """
    from db import init_db, insert_detections, accumulate_grid, get_processed_images

    init_db(db_path)
    model, is_fallback = load_model(data_dir=data_dir)
    confidence = config.get("settings", {}).get("confidence_threshold", 0.5)
    cameras = {c["id"]: c for c in config.get("cameras", [])}

    # 获取已处理的图片路径，避免重复处理
    processed = get_processed_images(db_path)

    summaries = []

    for filename in sorted(os.listdir(image_dir)):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        parts = filename.rsplit('_', 1)
        if len(parts) < 2:
            continue
        cam_id = parts[0]

        if cam_id not in cameras:
            continue

        cam = cameras[cam_id]
        image_path = os.path.join(image_dir, filename)

        # 跳过已处理的图片
        if image_path in processed:
            continue

        # 从文件名解析抓拍时间
        capture_time = _parse_capture_time(filename)
        if capture_time is None:
            capture_time = datetime.now()

        detections = detect_heads(
            image_path=image_path,
            model=model,
            confidence=confidence,
            grid_cols=cam.get("grid_cols", 24),
            grid_rows=cam.get("grid_rows", 14)
        )

        insert_detections(db_path, cam_id, capture_time, len(detections), image_path)
        accumulate_grid(db_path, cam_id, detections, capture_time, capture_time)

        summaries.append({
            "camera_id": cam_id,
            "person_count": len(detections),
            "capture_time": capture_time.isoformat(),
            "detections": detections
        })

    if not summaries:
        print("所有图片已处理过，无新增数据。", file=sys.stderr)

    return summaries


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="头部检测与网格映射")
    parser.add_argument("--images", required=True, help="抓拍图片目录")
    parser.add_argument("--config", required=True, help="cameras.json 路径")
    parser.add_argument("--db", required=True, help="SQLite 数据库路径")
    parser.add_argument("--data-dir", default=None, help="会话数据目录（用于模型查找和下载）")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    results = process_images(args.images, config, args.db, data_dir=args.data_dir)
    print(json.dumps(results, ensure_ascii=False, indent=2))
