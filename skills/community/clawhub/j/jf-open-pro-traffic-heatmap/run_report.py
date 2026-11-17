"""生成报告脚本 — 支持实时报告和日报模式，自动取最新背景图"""
import sys, os, glob, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from datetime import datetime, timedelta
from report import generate_report
import json

skill_dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="生成热力图报告")
parser.add_argument("--data-dir", default=None,
                    help="会话数据目录（数据库/抓拍/输出的根目录）。不指定则使用技能目录。")
parser.add_argument("--daily", action="store_true",
                    help="日报模式：输出带日期命名的文件（daily_report_YYYYMMDD.html）")
args = parser.parse_args()

# data_dir: 会话独立的数据目录; 默认回退到技能目录（向后兼容）
data_dir = args.data_dir if args.data_dir else skill_dir

with open(os.path.join(skill_dir, "config", "cameras.json"), "r", encoding="utf-8") as f:
    config = json.load(f)

db_path = os.path.join(data_dir, "data", "traffic_heatmap.db")

# 自动取今天日期
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow = today + timedelta(days=1)

# 自动查找每个摄像头最新的抓拍图（按文件修改时间排序）
backgrounds = {}
for cam in config.get("cameras", []):
    cam_id = cam["id"]
    captures_dir = os.path.join(data_dir, "data", "captures")
    latest = None
    latest_mtime = 0
    for date_dir in sorted(glob.glob(os.path.join(captures_dir, "*")), reverse=True):
        matches = glob.glob(os.path.join(date_dir, cam_id + "_*.png"))
        for f in matches:
            mtime = os.path.getmtime(f)
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest = f
    if latest:
        backgrounds[cam_id] = latest
        print("背景图: " + os.path.basename(latest))

# 输出目录
outputs_dir = os.path.join(data_dir, "data", "outputs")
os.makedirs(outputs_dir, exist_ok=True)

# 日报模式用日期命名，否则覆盖 report.html
date_str = datetime.now().strftime("%Y%m%d")
if args.daily:
    report_name = f"daily_report_{date_str}.html"
    summary_name = "daily_summary.txt"
else:
    report_name = "report.html"
    summary_name = "summary.txt"

output_path = os.path.join(outputs_dir, report_name)

summary = generate_report(db_path, config, today, tomorrow, backgrounds, output_path, data_dir=data_dir)
print("报告已生成: " + output_path)

# 保存总结文本到文件，供后续推送使用
summary_path = os.path.join(outputs_dir, summary_name)
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)
print("总结已保存: " + summary_path)
print()
# 兼容 Windows 控制台编码
sys.stdout.buffer.write((summary + "\n").encode("utf-8", errors="replace"))
