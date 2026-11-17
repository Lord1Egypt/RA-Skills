# -*- coding: utf-8 -*-
"""
检验气泡标注 —— 一键全自动流水线（极速模式）
收到一张图纸 PDF 后，一条命令产出全部交付物，无需手工逐步操作。

流程：渲染 → 多方向OCR → 自动抽取尺寸(初稿) → 气泡标注图(PDF/PNG)
      → 检验表A(18列) → 检验表B(3表式) → 覆盖性自检 + 交付前10项。

用法:
  python auto_run.py --pdf <图纸.pdf> --base <输出根目录> [--name 输出名]
        [--dims 已有dims_table.py]   # 若提供则跳过自动抽取（复用人工精修数据）
        [--meta work/drawing_meta.json]
        [--cp 控制计划编号]
        [--force-render] [--force-ocr]

约定：
  --base 下需有 work/ 与 outputs/ 两个目录（脚本在此工作；若无则自动创建）。
  输出文件名以 --name 或 PDF 主名为准：
    <名>_气泡标注图_p1.pdf / .png、<名>_尺寸明细检验表.xlsx、<名>_检验记录表.xlsx
  自动抽取的 dims_table.py 为 AI 初筛，CC/SC/NC 均带【待复核】，正式下发前须工程师确认。
"""
import os, sys, json, shutil, argparse, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable  # 当前解释器（已含 pymupdf/PIL/numpy/rapidocr/openpyxl）

ap = argparse.ArgumentParser()
ap.add_argument("--pdf", required=True)
ap.add_argument("--base", required=True, help="工作根目录（含/将建 work、outputs）")
ap.add_argument("--name", default=None, help="输出主名（默认用 PDF 主名）")
ap.add_argument("--dims", default=None, help="已有 dims_table.py（跳过自动抽取）")
ap.add_argument("--meta", default=None, help="drawing_meta.json 路径")
ap.add_argument("--cp", default="MEST/Q/CP-（按控制计划填写）")
ap.add_argument("--force-render", action="store_true")
ap.add_argument("--force-ocr", action="store_true")
ap.add_argument("--render-dpi", type=int, default=300,
                help="底图渲染 dpi（仅用于障碍检测/OCR 输入，标注图仍以 300dpi 矢量出图，清晰度不受影响）。"
                     "默认 300：配合白边裁切已足够且快；调高(400)可提升极小字识别率但更慢，调低(200)更快但可能漏标小尺寸。")
ap.add_argument("--no-pdf", action="store_true",
                help="气泡标注图跳过 PDF 输出，仅输出 PNG（省去 deflate 时间）")
ap.add_argument("--no-png", action="store_true",
                help="气泡标注图跳过 PNG 输出，仅输出 PDF；注意：表B的内嵌气泡图将无图可嵌（被跳过）")
a = ap.parse_args()

PDF = os.path.abspath(a.pdf)
BASE = os.path.abspath(a.base)
WORK = os.path.join(BASE, "work")
OUT = os.path.join(BASE, "outputs")
os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)

stem = a.name or os.path.splitext(os.path.basename(PDF))[0]
RENDER = os.path.join(WORK, "render.png")
LABELS = os.path.join(WORK, "labels.json")
OCR2  = os.path.join(WORK, "ocr_master.json")
DIMS  = os.path.join(WORK, "dims_table.py")
META  = a.meta or os.path.join(WORK, "drawing_meta.json")
BALL  = os.path.join(WORK, "balloons.json")
COV   = os.path.join(WORK, "coverage_report.json")

import time
timings = {}
T0 = time.perf_counter()
def run(script, args, step):
    cmd = [PY, os.path.join(HERE, script)] + args
    print(f"\n=== [{step}] {script} ===")
    t0 = time.perf_counter()
    r = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True, encoding="utf-8")
    dt = time.perf_counter() - t0
    timings[step] = dt
    out = (r.stdout or "") + (r.stderr or "")
    # 只打印每步尾部摘要，完整日志见 work/auto_run.log
    tail = "\n".join(out.strip().splitlines()[-8:]) if out.strip() else "(无输出)"
    print(tail)
    print(f"[{step}] 耗时 {dt:.1f}s")
    if r.returncode != 0:
        print(f"!!! {step} 失败 (exit={r.returncode})，详见 work/auto_run.log")
    return r.returncode == 0

log_lines = []
def log(msg):
    line = f"[{datetime.datetime.now():%H:%M:%S}] {msg}"
    print(line); log_lines.append(line)

# ---- 0) 渲染 ----
if a.force_render or not os.path.exists(RENDER):
    run("render_pdf.py", [PDF, RENDER, "--dpi", str(a.render_dpi)], "渲染")
else:
    log("渲染图已存在，跳过 (--force-render 可强制)")

# ---- 1) OCR ----
if a.force_ocr or (not os.path.exists(LABELS) and not os.path.exists(OCR2)):
    run("ocr_labels.py", [RENDER, LABELS, "--min-conf", "0.4"], "OCR")
else:
    log("OCR 已存在，跳过 (--force-ocr 可强制)")
OCR_FILE = LABELS if os.path.exists(LABELS) else OCR2

# ---- 2) 尺寸主数据 ----
if a.dims:
    src = os.path.abspath(a.dims)
    if os.path.abspath(src) != os.path.abspath(DIMS):
        shutil.copy(src, DIMS)
    log(f"复用已有尺寸主数据: {a.dims}")
elif not os.path.exists(DIMS):
    run("auto_extract_dims.py", ["--labels", OCR_FILE, "--png", RENDER,
        "--out", DIMS, "--meta", META if os.path.exists(META) else "none"], "自动抽取尺寸")
else:
    log("dims_table.py 已存在，跳过自动抽取（删除它可重新生成）")

# ---- 3) 气泡标注图 ----
bb_args = ["--dims", DIMS, "--pdf", PDF, "--png", RENDER,
           "--ocr", OCR_FILE, "--out", OUT, "--work", WORK, "--name", stem]
if a.no_pdf:
    bb_args.append("--no-pdf")
if a.no_png:
    bb_args.append("--no-png")
ok = run("build_balloons.py", bb_args, "气泡标注图")
if not ok:
    open(os.path.join(WORK, "auto_run.log"), "w", encoding="utf-8").write("\n".join(log_lines))
    sys.exit(1)

# ---- 4) 合并检验表（检验记录表 + 内嵌气泡图 + 未注公差基准 + 汇总 + 关键特性专项；尺寸明细不输出）----
run("gen_combined.py", ["--balloons", BALL,
    "--png", os.path.join(OUT, f"{stem}_气泡标注图_p1.png"),
    "--meta", META if os.path.exists(META) else "none",
    "--cp", a.cp,
    "--out", os.path.join(OUT, f"{stem}_检验记录表.xlsx")], "合并检验表")

# ---- 5) 自检 ----
run("validate_layout.py", ["--balloons", BALL, "--ocr", OCR_FILE, "--pdf", PDF,
    "--png", RENDER, "--out", COV], "布局自检")
run("finalize_report.py", ["--report", COV], "交付前校验")

# ---- 汇总 ----
summary = {
    "图纸": stem,
    "气泡标注图PDF": os.path.join(OUT, f"{stem}_气泡标注图_p1.pdf"),
    "气泡标注图PNG": os.path.join(OUT, f"{stem}_气泡标注图_p1.png"),
    "检验记录表(合并)": os.path.join(OUT, f"{stem}_检验记录表.xlsx"),
    "自检报告": COV,
}
try:
    cov = json.load(open(COV, encoding="utf-8"))
    summary["气泡数"] = len(json.load(open(BALL, encoding="utf-8")))
    summary["布局结论"] = cov.get("verdict") or cov.get("layout_quality", {}).get("verdict", "见报告")
except Exception as e:
    summary["自检读取"] = f"跳过({e})"

log("===== 交付物 =====")
for k, v in summary.items():
    log(f"  {k}: {v}")
total = time.perf_counter() - T0
log("===== 各步耗时 =====")
for s, dt in timings.items():
    log(f"  {s}: {dt:.1f}s")
log(f"  总耗时: {total:.1f}s")
slow = max(timings.items(), key=lambda kv: kv[1]) if timings else ("-", 0)
log(f"  最慢步骤: {slow[0]} ({slow[1]:.1f}s) —— 若需进一步加速优先优化此处")
log("提示：自动抽取为 AI 初筛，CC/SC/NC 与待确认项请工程师复核后再正式下发。")

open(os.path.join(WORK, "auto_run.log"), "w", encoding="utf-8").write("\n".join(log_lines))
print("\n全部完成。详细日志: work/auto_run.log")
