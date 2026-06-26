#!/usr/bin/env python3
# NOTE: 需要 Pillow。如果系统 Python 没有 Pillow，使用 venv:
#   cd {baseDir} && python3 -m venv venv && venv/bin/pip install Pillow
#   venv/bin/python3 scripts/split_screenshot.py <image>
"""将即刻游长截图切成多段，方便 vision 模型逐段识别。

用法:
  split_screenshot.py <image_path> [--output-dir <dir>]

输出:
  将图片按区域切割，保存到输出目录，打印 JSON 结果。
  默认输出目录为图片同目录下的 split_<basename>/ 文件夹。
"""

import json
import os
import sys
from pathlib import Path

from PIL import Image

# 即刻游截图从上到下 11 个区域（按高度百分比）
# 基于 1179x8823 / 1179x8691 的典型布局分析
SEGMENTS = [
    {
        "name": "01_header",
        "label": "日期、总距离、次数、趟数、泳姿距离、六宫格核心指标（时长/配速/划水/心率/卡路里/SWOLF）",
        "start_pct": 0.0,
        "end_pct": 0.18,
    },
    {
        "name": "02_segments",
        "label": "分段数据表格（距离、用时、划水、休息）",
        "start_pct": 0.18,
        "end_pct": 0.30,
    },
    {
        "name": "03_auto_sets",
        "label": "自动组合表格（泳姿、距离、用时、SWOLF）",
        "start_pct": 0.30,
        "end_pct": 0.42,
    },
    {
        "name": "04_trend",
        "label": "趋势柱状图（平均配速、最快配速）",
        "start_pct": 0.42,
        "end_pct": 0.52,
    },
    {
        "name": "05_compare",
        "label": "比较板块（与历史某天的对比数据）",
        "start_pct": 0.52,
        "end_pct": 0.60,
    },
    {
        "name": "06_best_pace",
        "label": "最快配速表格（各距离的用时和配速）",
        "start_pct": 0.60,
        "end_pct": 0.70,
    },
    {
        "name": "07_heart_rate",
        "label": "心率板块（平均心率、最大心率大数字 + 心率曲线图）",
        "start_pct": 0.70,
        "end_pct": 0.80,
    },
    {
        "name": "08_heart_rate_zones",
        "label": "心率区间表（zone 5/4/3/2/1 的 BPM 范围、时长、百分比）",
        "start_pct": 0.80,
        "end_pct": 0.87,
    },
    {
        "name": "09_training_load",
        "label": "训练负荷数值",
        "start_pct": 0.87,
        "end_pct": 0.91,
    },
    {
        "name": "10_metabolic",
        "label": "代谢当量数值",
        "start_pct": 0.91,
        "end_pct": 0.95,
    },
    {
        "name": "11_heart_rate_recovery",
        "label": "心率恢复数据",
        "start_pct": 0.95,
        "end_pct": 1.0,
    },
]


def split_image(image_path: str, output_dir: str | None = None) -> dict:
    img = Image.open(image_path)
    width, height = img.size

    if output_dir is None:
        stem = Path(image_path).stem
        output_dir = str(Path(image_path).parent / f"split_{stem}")

    os.makedirs(output_dir, exist_ok=True)

    results = []
    for seg in SEGMENTS:
        y_start = int(height * seg["start_pct"])
        y_end = int(height * seg["end_pct"])
        cropped = img.crop((0, y_start, width, y_end))

        filename = f"{seg['name']}.jpg"
        out_path = os.path.join(output_dir, filename)
        cropped.save(out_path, "JPEG", quality=95)

        results.append({
            "name": seg["name"],
            "label": seg["label"],
            "path": out_path,
            "size": f"{cropped.width}x{cropped.height}",
        })

    return {
        "status": "ok",
        "original": f"{width}x{height}",
        "output_dir": output_dir,
        "segments": results,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: split_screenshot.py <image_path> [--output-dir <dir>]", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    output_dir = None
    if "--output-dir" in sys.argv:
        idx = sys.argv.index("--output-dir")
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[idx + 1]

    result = split_image(image_path, output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
