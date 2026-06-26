#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable

TEXT_EXTS = {".java", ".xml", ".yml", ".yaml", ".properties", ".sh", ".sql", ".json", ".conf"}
RULE_KEYWORDS = {
    "硬编码配置": ["localhost", "127.0.0.1", "jdbc:", "password", "secret", "token"],
    "待清理标记": ["TODO", "FIXME"],
    "疑似重复/临时实现": ["temp", "tmp", "hack", "mock"]
}


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


def collect_findings(root: Path) -> list[dict]:
    findings = []
    for p in iter_files(root):
        if p.suffix.lower() not in TEXT_EXTS and p.name != "pom.xml":
            continue
        text = safe_read(p)
        if not text:
            continue
        for rule, kws in RULE_KEYWORDS.items():
            hits = [kw for kw in kws if kw.lower() in text.lower()]
            if hits:
                findings.append({
                    "rule": rule,
                    "path": str(p.relative_to(root)),
                    "hits": hits[:10]
                })
    return findings[:300]


def render_report(summary: dict, findings: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    modules = ", ".join(summary.get("modules", [])) or "无"
    lines = [
        f"# {summary.get('projectName', 'java-maven-project')} 代码规范检查报告",
        "",
        "## 1. 项目概况",
        f"- 项目名称：{summary.get('projectName', 'java-maven-project')}",
        f"- 扫描时间：{now}",
        f"- 输入方式：{summary.get('mode', '')}",
        "",
        "## 2. 扫描范围",
        f"- 根目录：{summary.get('root', '')}",
        f"- 模块列表：{modules}",
        "",
    ]
    if summary.get("scanLimited"):
        lines += [
            "## 3. 扫描受限说明",
            f"- {summary.get('limitedReason', '扫描受限')}",
            "",
            "## 4. 结论",
            "- 当前无法形成完整规范检查结论，建议先修复输入或补全项目结构后重新扫描。",
        ]
        return "\n".join(lines)

    lines += ["## 3. 规范问题清单"]
    if not findings:
        lines += ["- 本轮未通过规则扫描发现明显规范关键词问题；仍建议结合人工审查进一步确认结构与设计质量。"]
    else:
        for idx, item in enumerate(findings[:50], 1):
            hits = ", ".join(item.get("hits", []))
            lines += [f"{idx}. **{item['rule']}**  ", f"   - 位置：`{item['path']}`  ", f"   - 证据：{hits}  ", "   - 建议：结合上下文核查并按规范整改。"]
    lines += ["", "## 4. 总体建议", "- 先处理硬编码与待清理标记，再复查结构问题和重复逻辑。", "", "## 5. 结论", "- 本报告基于规则扫描结果生成，适合作为第一轮规范检查依据。"]
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

    findings = []
    if prepare.get("ok") and not prepare.get("scanLimited") and prepare.get("root"):
        findings = collect_findings(Path(prepare["root"]))

    result = {
        "projectName": prepare.get("projectName"),
        "mode": prepare.get("mode"),
        "root": prepare.get("root"),
        "modules": prepare.get("modules", []),
        "scanLimited": prepare.get("scanLimited", True) or (not prepare.get("ok", False)),
        "limitedReason": prepare.get("limitedReason", ""),
        "findings": findings,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text(render_report(result, findings), encoding="utf-8")
    print(out_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
