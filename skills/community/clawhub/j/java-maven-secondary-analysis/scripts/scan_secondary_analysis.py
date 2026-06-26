#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

TEXT_EXTS = {".java", ".xml", ".yml", ".yaml", ".properties", ".sh", ".sql", ".json", ".conf"}
LAYER_MARKERS = {
    "controller": ["Controller"],
    "service": ["Service"],
    "mapper": ["Mapper", "Repository", "Dao"],
    "config": ["Config"],
}
TRACE_KEYWORDS = ["tenant", "customer", "brand", "logo", "theme", "custom", "override"]


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""


def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def count_java(root: Path) -> int:
    return sum(1 for _ in root.rglob("*.java"))


def detect_layers(root: Path) -> dict:
    stats = {k: 0 for k in LAYER_MARKERS}
    for p in root.rglob("*.java"):
        for layer, markers in LAYER_MARKERS.items():
            if any(p.stem.endswith(m) for m in markers):
                stats[layer] += 1
    return stats


def trace_hits(root: Path) -> list[dict]:
    hits = []
    for p in iter_files(root):
        if p.suffix.lower() not in TEXT_EXTS and p.name != "pom.xml":
            continue
        text = safe_read(p)
        if not text:
            continue
        matched = [kw for kw in TRACE_KEYWORDS if kw.lower() in text.lower()]
        if matched:
            hits.append({"path": str(p.relative_to(root)), "hits": matched[:10]})
    return hits[:300]


def render_report(summary: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    modules = ", ".join(summary.get("modules", [])) or "无"
    lines = [
        f"# {summary.get('projectName', 'java-maven-project')} 二开分析报告",
        "",
        "## 1. 项目概况",
        f"- 项目名称：{summary.get('projectName', 'java-maven-project')}",
        f"- 扫描时间：{now}",
        f"- 输入方式：{summary.get('mode', '')}",
        "",
    ]
    if summary.get("scanLimited"):
        lines += [
            "## 2. 扫描受限说明",
            f"- {summary.get('limitedReason', '扫描受限')}",
            "",
            "## 3. 总体结论",
            "- 当前无法形成完整二开分析结论，建议先修复输入或补全项目结构后重新扫描。",
        ]
        return "\n".join(lines)

    lines += [
        "## 2. 模块与结构概览",
        f"- 模块数量：{summary.get('moduleCount', 0)}",
        f"- 模块列表：{modules}",
        f"- 类数量：{summary.get('javaClassCount', 0)}",
        f"- 分层分布：{summary.get('layerDistribution', {})}",
        "",
        "## 3. 二开范围识别",
    ]
    trace_hits_list = summary.get("traceHits", [])
    if not trace_hits_list:
        lines += ["- 本轮未通过关键词扫描发现明显客户化、品牌化或产品化痕迹；建议结合业务背景做人审复核。"]
    else:
        for idx, item in enumerate(trace_hits_list[:50], 1):
            lines += [f"{idx}. 位置：`{item['path']}`  ", f"   - 证据：{', '.join(item.get('hits', []))}  ", "   - 判断：存在二开痕迹候选，需要结合上下文确认具体改造类型。"]
    lines += ["", "## 4. 产品二开信息", "- 客户化/品牌化特征：可参考上方命中记录。", "- 配置改造特征：建议重点复核 resources 与配置文件。", "- 侵入式改造特征：建议结合核心业务类人工确认。", "", "## 5. 总体结论", "- 本报告基于结构与关键词扫描结果生成，适合作为第一轮二开分析依据。"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-json", required=True)
    ap.add_argument("--json", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    prepare = json.loads(Path(args.prepare_json).read_text(encoding="utf-8"))
    out_json = Path(args.json)
    out_report = Path(args.report)

    java_class_count = 0
    layer_distribution = {}
    trace_hits_list = []
    if prepare.get("ok") and not prepare.get("scanLimited") and prepare.get("root"):
        root = Path(prepare["root"])
        java_class_count = count_java(root)
        layer_distribution = detect_layers(root)
        trace_hits_list = trace_hits(root)

    result = {
        "projectName": prepare.get("projectName"),
        "mode": prepare.get("mode"),
        "root": prepare.get("root"),
        "modules": prepare.get("modules", []),
        "moduleCount": prepare.get("moduleCount", 0),
        "javaClassCount": java_class_count,
        "layerDistribution": layer_distribution,
        "traceHits": trace_hits_list,
        "scanLimited": prepare.get("scanLimited", True) or (not prepare.get("ok", False)),
        "limitedReason": prepare.get("limitedReason", ""),
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text(render_report(result), encoding="utf-8")
    print(out_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
