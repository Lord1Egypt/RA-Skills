"""生成移动端友好的热力图摘要 PNG — 热力图 + 关键统计文字"""
import sys, os, glob, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from datetime import datetime, timedelta
import json

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from db import query_grid, query_stats, query_time_series
from heatmap import grid_to_heatmap_image

skill_dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="生成移动端热力图摘要")
parser.add_argument("--data-dir", required=True, help="数据目录")
parser.add_argument("--daily", action="store_true", help="日报模式（全天数据）")
args = parser.parse_args()

data_dir = args.data_dir
date_str = datetime.now().strftime("%Y%m%d")

with open(os.path.join(skill_dir, "config", "cameras.json"), "r", encoding="utf-8") as f:
    config = json.load(f)

db_path = os.path.join(data_dir, "data", "traffic_heatmap.db")
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow = today + timedelta(days=1)
outputs_dir = os.path.join(data_dir, "data", "outputs")
os.makedirs(outputs_dir, exist_ok=True)

cam = config["cameras"][0]
cam_id = cam["id"]
grid_cols = cam.get("grid_cols", 24)
grid_rows = cam.get("grid_rows", 14)

# 查询数据
grid_data = query_grid(db_path, cam_id, today, tomorrow)
stats = query_stats(db_path, cam_id, today, tomorrow)
time_series = query_time_series(db_path, cam_id, today, tomorrow, interval_minutes=10)

# 找最新背景图
background_path = None
captures_dir = os.path.join(data_dir, "data", "captures")
today_dir = os.path.join(captures_dir, date_str)
if os.path.isdir(today_dir):
    files = sorted(glob.glob(os.path.join(today_dir, cam_id + "_*.png")), reverse=True)
    if files:
        background_path = files[0]

bg = cv2.imread(background_path) if background_path else None
if bg is None:
    bg = np.zeros((1080, 1920, 3), dtype=np.uint8)

# 1. 渲染热力图
heatmap_img = grid_to_heatmap_image(bg, grid_data, grid_cols, grid_rows)
# 缩放到适合拼接的宽度 (1080px)
target_w = 1080
scale = target_w / heatmap_img.shape[1]
target_h = int(heatmap_img.shape[0] * scale)
heatmap_resized = cv2.resize(heatmap_img, (target_w, target_h), interpolation=cv2.INTER_AREA)

# 2. 用 matplotlib 绘制统计摘要图
fig_w, fig_h = 1080 / 100, 400 / 100  # 100 DPI
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)
fig.patch.set_facecolor("#1a1a2e")
ax.set_facecolor("#1a1a2e")
ax.axis("off")

# 尝试中文字体
font_candidates = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
]
font_prop = None
for fp in font_candidates:
    if os.path.exists(fp):
        font_prop = FontProperties(fname=fp, size=14)
        break

total = stats.get("total_detections", 0)
peak = stats.get("peak_hour", 0)
hottest_cell = stats.get("hottest_cell")
hottest_str = f"({hottest_cell['row']},{hottest_cell['col']})" if hottest_cell else "-"
rounds = stats.get("capture_rounds", 0)
avg = total / rounds if rounds > 0 else 0

# 统计文字
lines = [
    f"{today.strftime('%Y-%m-%d')} 办公室人流日报",
    f"",
    f"采集轮次: {rounds}    累计检测: {total} 人次    平均每轮: {avg:.1f} 人",
    f"高峰时段: {peak}:00    最热区域: 网格{hottest_str}",
    f"流量趋势: {'下降' if avg < 3 else '平稳' if avg < 5 else '上升'}",
]

y_pos = 0.95
for line in lines:
    color = "#ffffff" if y_pos > 0.7 else "#aaaaaa"
    kwargs = {"color": color, "fontsize": 16 if y_pos > 0.7 else 13, "ha": "left"}
    if font_prop:
        kwargs["fontproperties"] = font_prop
    ax.text(0.03, y_pos, line, transform=ax.transAxes, **kwargs)
    y_pos -= 0.18

# 简单流量柱状图
if time_series:
    labels = [t["time"] for t in time_series]
    counts = [t["count"] for t in time_series]
    ax2 = ax.inset_axes([0.03, 0.05, 0.94, 0.35])
    ax2.set_facecolor("#1a1a2e")
    ax2.bar(range(len(counts)), counts, color="#4fc3f7", alpha=0.8, width=0.7)
    ax2.set_xticks(range(len(labels)))
    ax2.set_xticklabels(labels, fontsize=8, color="#888888", rotation=-30, ha="right")
    ax2.tick_params(axis="y", colors="#888888", labelsize=8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#333333")
    ax2.spines["bottom"].set_color("#333333")

plt.tight_layout(pad=0.5)
stats_path = os.path.join(outputs_dir, "_stats_tmp.png")
fig.savefig(stats_path, facecolor=fig.get_facecolor())
plt.close(fig)

# 3. 拼接热力图 + 统计图
stats_img = cv2.imread(stats_path)
if stats_img is not None:
    # 统一宽度
    if stats_img.shape[1] != target_w:
        s = target_w / stats_img.shape[1]
        stats_img = cv2.resize(stats_img, (target_w, int(stats_img.shape[0] * s)))
    combined = np.vstack([heatmap_resized, stats_img])
else:
    combined = heatmap_resized

# 保存
if args.daily:
    out_name = f"daily_summary_{date_str}.png"
else:
    out_name = f"summary_{date_str}.png"

out_path = os.path.join(outputs_dir, out_name)
cv2.imwrite(out_path, combined, [cv2.IMWRITE_PNG_COMPRESSION, 6])
print(out_path)

# 清理临时文件
if os.path.exists(stats_path):
    os.remove(stats_path)
