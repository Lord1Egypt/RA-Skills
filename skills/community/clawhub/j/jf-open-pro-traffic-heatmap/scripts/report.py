"""交互式 HTML 报告生成器 — 聚合数据、渲染热力图、输出自包含 HTML"""

import os
import sys
import json
import base64
import argparse
from datetime import datetime
from typing import Dict, List, Any

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
TEMPLATE_PATH = os.path.join(SKILL_DIR, "assets", "report-template.html")

# 缩略图宽度
THUMB_WIDTH = 160


def _image_to_base64(image_path: str) -> str:
    """将图片文件转为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _thumbnail_base64(image_path: str, width: int = THUMB_WIDTH) -> str:
    """生成缩略图并返回 base64 JPEG 字符串，文件不存在返回空串"""
    if not image_path or not os.path.exists(image_path):
        return ""
    img = cv2.imread(image_path)
    if img is None:
        return ""
    h, w = img.shape[:2]
    new_h = int(h * width / w)
    thumb = cv2.resize(img, (width, new_h), interpolation=cv2.INTER_AREA)
    _, buf = cv2.imencode(".jpg", thumb, [cv2.IMWRITE_JPEG_QUALITY, 60])
    return base64.b64encode(buf.tobytes()).decode("utf-8")


def _render_heatmap_base64(background_path: str, grid_data: list,
                           grid_cols: int, grid_rows: int) -> str:
    """渲染热力图并返回 base64 PNG 字符串"""
    from heatmap import grid_to_heatmap_image

    bg = cv2.imread(background_path) if background_path and os.path.exists(background_path) else None
    if bg is None:
        bg = np.zeros((1080, 1920, 3), dtype=np.uint8)

    result = grid_to_heatmap_image(bg, grid_data, grid_cols, grid_rows)
    _, buf = cv2.imencode(".png", result)
    return base64.b64encode(buf.tobytes()).decode("utf-8")


def generate_summary(cameras_data: List[Dict[str, Any]], start: datetime, end: datetime) -> str:
    """根据所有摄像头数据生成简要总结文本"""
    grand_total = sum(c["stats"]["total_detections"] for c in cameras_data)
    total_rounds = sum(c["stats"]["capture_rounds"] for c in cameras_data)
    if grand_total == 0:
        return f"统计周期内共 {total_rounds} 轮采集，未检测到人员活动，区域处于空闲状态。"

    lines = []
    lines.append(f"统计周期内共 {total_rounds} 轮采集，累计检测 {grand_total} 人次。")

    for cam in cameras_data:
        stats = cam["stats"]
        if stats["total_detections"] == 0:
            continue
        peak_h = stats.get("peak_hour", 0)
        hot = stats.get("hottest_cell")
        avg = stats["total_detections"] / max(stats["capture_rounds"], 1)

        parts = [f"高峰时段 {peak_h}:00"]
        if hot and hot.get("count", 0) > 0:
            parts.append(f"最热区域 网格({hot['col']},{hot['row']})")
        parts.append(f"平均每轮 {avg:.1f} 人次")

        ts = cam.get("time_series", [])
        if len(ts) >= 2:
            first_half = ts[:len(ts) // 2]
            second_half = ts[len(ts) // 2:]
            first_sum = sum(d["count"] for d in first_half)
            second_sum = sum(d["count"] for d in second_half)
            if second_sum > first_sum * 1.2:
                parts.append("流量呈上升趋势")
            elif first_sum > second_sum * 1.2:
                parts.append("流量呈下降趋势")
            else:
                parts.append("流量基本平稳")

        if len(cameras_data) > 1:
            lines.append(f"{cam['name']}: " + "，".join(parts))
        else:
            lines.append("，".join(parts))

    return "\n".join(lines)


def generate_report(db_path: str, config: dict, start: datetime, end: datetime,
                    background_paths: Dict[str, str], output_path: str,
                    data_dir: str = None) -> str:
    """
    生成交互式 HTML 报告。

    Args:
        db_path: SQLite 数据库路径
        config: cameras.json 内容
        start/end: 时间范围
        background_paths: {camera_id: 背景图片路径}
        output_path: 输出 HTML 文件路径
        data_dir: 数据根目录，用于解析 DB 中的相对图片路径

    Returns:
        总结文本字符串
    """
    from db import query_grid, query_time_series, query_stats, query_history

    cameras_data = []
    for cam in config.get("cameras", []):
        cam_id = cam["id"]
        grid_cols = cam.get("grid_cols", 24)
        grid_rows = cam.get("grid_rows", 14)

        grid_data = query_grid(db_path, cam_id, start, end)
        time_series = query_time_series(db_path, cam_id, start, end)
        stats = query_stats(db_path, cam_id, start, end)

        bg_path = background_paths.get(cam_id, "")
        heatmap_b64 = _render_heatmap_base64(bg_path, grid_data, grid_cols, grid_rows)

        # 查询检测历史并生成缩略图
        history_records = query_history(db_path, cam_id, start, end)
        all_counts = [rec["person_count"] for rec in history_records]
        avg_count = sum(all_counts) / max(len(all_counts), 1)
        max_count = max(all_counts) if all_counts else 0

        history_with_thumbs = []
        for rec in history_records:
            img_path = rec.get("image_path", "")
            # 解析相对路径：基于 data_dir 拼接
            if img_path and not os.path.isabs(img_path) and data_dir:
                img_path = os.path.join(data_dir, img_path.replace("\\", "/"))
            thumb = _thumbnail_base64(img_path)
            count = rec["person_count"]
            if count == 0:
                rec_summary = "本轮未检测到人员活动"
            else:
                if count == max_count and max_count > 0:
                    level = "本时段峰值"
                elif count > avg_count * 1.3:
                    level = "高于平均"
                elif count < avg_count * 0.7:
                    level = "低于平均"
                else:
                    level = "正常水平"
                rec_summary = f"检测到 {count} 人，{level}"
            history_with_thumbs.append({
                "timestamp": rec["timestamp"],
                "person_count": count,
                "thumbnail": thumb,
                "summary": rec_summary
            })

        cameras_data.append({
            "id": cam_id,
            "name": cam.get("name", cam_id),
            "heatmap_base64": heatmap_b64,
            "time_series": time_series,
            "stats": stats,
            "history": history_with_thumbs
        })

    summary = generate_summary(cameras_data, start, end)

    report_data = {
        "cameras": cameras_data,
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": summary
    }

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("__REPORT_DATA__", json.dumps(report_data, ensure_ascii=False))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成热力图报告")
    parser.add_argument("--db", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--output", required=True)
    parser.add_argument("--backgrounds", default="{}", help="JSON: {cam_id: path}")
    parser.add_argument("--data-dir", default=None, help="数据根目录，用于解析相对图片路径")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    bg = json.loads(args.backgrounds)
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    summary = generate_report(args.db, config, start, end, bg, args.output, data_dir=args.data_dir)
    print(f"报告已生成: {args.output}")
    sys.stdout.buffer.write((summary + "\n").encode("utf-8", errors="replace"))
