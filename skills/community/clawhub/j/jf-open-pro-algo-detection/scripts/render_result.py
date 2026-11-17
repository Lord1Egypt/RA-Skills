#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_result.py —— 检测结果结构化输出 + 取证图渲染

用法：
  python render_result.py --result <call输出JSON文件> --image <原图路径或URL>
      --algo-name 睡岗检测 --label-cn 疑似睡岗
      [--sn 设备SN] [--channel 0] [--conf-used 0.3] [--out-dir 输出目录]

功能：
  1. 解析 jf_client.py call 命令的输出（或其中 data 部分）
  2. 在原图上绘制红色 bbox + 中文标签 + 置信度，生成取证图
  3. 输出与前端检测报告一致的结构化摘要 JSON（stdout）：
     告警文案 / 检出目标数 / 检测项结果表 / 检测信息 / 取证图路径
无检出时不渲染图片，仅输出摘要（detected=false）。
"""
import argparse
import json
import os
import sys
from datetime import datetime

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]


def load_font(size):
    for fp in FONT_CANDIDATES:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def describe_position(bbox, w, h):
    """由 bbox 中心点推导画面位置描述"""
    cx = (bbox.get("xmin", 0) + bbox.get("xmax", 0)) / 2.0
    cy = (bbox.get("ymin", 0) + bbox.get("ymax", 0)) / 2.0
    px, py = cx / max(w, 1), cy / max(h, 1)
    col = "左侧" if px < 1 / 3 else ("中部" if px < 2 / 3 else "右侧")
    row = "上方" if py < 1 / 3 else ("中部" if py < 2 / 3 else "下方")
    if row == "中部" and col != "中部":
        return "%s区域" % col
    if col == "中部" and row != "中部":
        return "%s区域" % row
    if col == "中部" and row == "中部":
        return "画面中央"
    return "%s偏%s区域" % (col, row)


def render_evidence(image_path, objects, label_cn, out_path):
    """在原图上画红框+标签，保存取证图；返回 (成功?, 图宽, 图高)"""
    if not HAS_PIL:
        return False, 0, 0
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception:
        return False, 0, 0
    w, h = img.size
    draw = ImageDraw.Draw(img)
    lw = max(2, int(max(w, h) / 400))
    font = load_font(max(16, int(max(w, h) / 45)))
    for obj in objects:
        bbox = obj.get("bbox") or {}
        x1, y1 = int(bbox.get("xmin", 0)), int(bbox.get("ymin", 0))
        x2, y2 = int(bbox.get("xmax", 0)), int(bbox.get("ymax", 0))
        x1, x2 = max(0, min(x1, w)), max(0, min(x2, w))
        y1, y2 = max(0, min(y1, h)), max(0, min(y2, h))
        if x2 <= x1 or y2 <= y1:
            continue
        draw.rectangle([x1, y1, x2, y2], outline=(255, 0, 0), width=lw)
        conf = obj.get("confidence")
        text = label_cn if conf is None else "%s %d%%" % (label_cn, round(float(conf) * 100))
        tb = draw.textbbox((0, 0), text, font=font)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        ty = max(0, y1 - th - 8)
        draw.rectangle([x1, ty, x1 + tw + 10, ty + th + 8], fill=(255, 0, 0))
        draw.text((x1 + 5, ty + 3), text, fill=(255, 255, 255), font=font)
    img.save(out_path, quality=92)
    return True, w, h


def main():
    ap = argparse.ArgumentParser(description="检测结果结构化输出+取证图渲染")
    ap.add_argument("--result", required=True, help="jf_client.py call 输出JSON文件")
    ap.add_argument("--image", required=True, help="原图本地路径（本地图片才渲染取证图）")
    ap.add_argument("--algo-name", required=True, help="算法中文名，如 睡岗检测")
    ap.add_argument("--label-cn", required=True, help="业务标签中文，如 疑似睡岗 / 未戴口罩")
    ap.add_argument("--sn", default="—", help="设备序列号")
    ap.add_argument("--channel", type=int, default=0)
    ap.add_argument("--conf-used", type=float, default=0.3, help="本次调用使用的置信度阈值")
    ap.add_argument("--out-dir", default=".", help="取证图输出目录")
    args = ap.parse_args()

    try:
        raw = json.load(open(args.result, encoding="utf-8"))
    except Exception as e:
        print(json.dumps({"error": "结果文件解析失败: %s" % e}, ensure_ascii=False))
        sys.exit(1)

    code = raw.get("code")
    if code != 2000:
        print(json.dumps({"error": "调用失败", "code": code, "msg": raw.get("msg")},
                         ensure_ascii=False))
        sys.exit(2)

    objects = []
    source_url = None
    for item in raw.get("data") or []:
        objects.extend(item.get("objects") or [])
        source_url = source_url or item.get("image")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {
        "title": "检测结果",
        "algo": args.algo_name,
        "detected": len(objects) > 0,
        "target_count": len(objects),
        "confidence_threshold": args.conf_used,
        "analysis_time": now_str,
        "device": {"sn": args.sn, "channel": args.channel, "capability": args.algo_name},
        "source_image_url": source_url,
        "objects": [],
    }

    if not objects:
        summary["alert"] = None
        summary["table"] = []
        summary["evidence_image"] = None
        print(json.dumps(summary, ensure_ascii=False))
        return

    confs = [float(o["confidence"]) for o in objects if o.get("confidence") is not None]
    max_conf = max(confs) if confs else None
    summary["alert"] = "画面中检测到 %d 个「%s」目标，建议及时关注。" % (len(objects), args.label_cn)

    os.makedirs(args.out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ev_path = os.path.join(args.out_dir, "evidence_%s_%s.jpg" % (args.algo_name, stamp))
    ok, w, h = (False, 0, 0)
    if os.path.exists(args.image):
        ok, w, h = render_evidence(args.image, objects, args.label_cn, ev_path)
    summary["evidence_image"] = ev_path if ok else None

    for o in objects:
        row = {"label": o.get("label"), "confidence": o.get("confidence")}
        if o.get("bbox") and w and h:
            row["position"] = describe_position(o["bbox"], w, h)
        summary["objects"].append(row)

    conf_txt = ("%d%%" % round(max_conf * 100)) if max_conf is not None else "—"
    pos_txt = summary["objects"][0].get("position", "—") if summary["objects"] else "—"
    summary["table"] = [
        {"item": "行为/目标识别", "result": args.label_cn},
        {"item": "目标数量", "result": "%d 个" % len(objects)},
        {"item": "最高置信度", "result": conf_txt},
        {"item": "画面位置", "result": pos_txt},
        {"item": "分析时间", "result": now_str},
    ]
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
