#!/usr/bin/env python3
"""Check basic GB/T 7714—2025 invariants in a DOCX reference list."""

from __future__ import annotations

import json
import argparse
import re
import sys
from pathlib import Path

from docx import Document


ALLOWED_TYPES = {"A", "C", "CM", "D", "DB", "DS", "EB", "J", "M", "N", "P", "PP", "R", "S", "Z"}
NUMBERED = re.compile(r"^\s*[\[［](\d+)[\]］]\s*(.+)$")
TYPE_MARK = re.compile(r"[\[［]([A-Z]{1,3})(?:/([A-Z]{2}))?[\]］]")


def emit(payload: dict, code: int) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)


def main() -> None:
    parser = argparse.ArgumentParser(description="检查 DOCX 中已有的 GB/T 7714 参考文献。")
    parser.add_argument("docx", type=Path)
    parser.add_argument(
        "--mode",
        choices=("auto", "required", "skip"),
        default="auto",
        help="auto=有参考文献标题时检查；required=缺失也失败；skip=按用户要求跳过且不创建内容",
    )
    args = parser.parse_args()
    path = args.docx
    if not path.is_file() or path.suffix.lower() != ".docx":
        emit({"status": "error", "message": "输入必须是存在的 .docx 文件。"}, 2)

    try:
        doc = Document(path)
    except Exception as exc:
        emit({"status": "error", "message": f"无法解析 DOCX: {exc}"}, 2)

    if args.mode == "skip":
        emit(
            {
                "status": "skipped",
                "mode": "skip",
                "reason": "用户已确认跳过参考文献；检查器不会要求或生成参考文献。",
            },
            0,
        )

    paragraphs = [p.text.strip() for p in doc.paragraphs]
    try:
        start = next(i for i, text in enumerate(paragraphs) if text in {"参考文献", "References", "REFERENCES"})
    except StopIteration:
        if args.mode == "auto":
            emit(
                {
                    "status": "skipped",
                    "mode": "auto",
                    "reason": "原稿未包含参考文献标题；未执行参考文献格式检查，也未生成参考文献。",
                },
                0,
            )
        emit({"status": "fail", "mode": "required", "errors": ["未找到参考文献标题。"], "warnings": []}, 1)

    entries = []
    for text in paragraphs[start + 1 :]:
        if not text:
            continue
        match = NUMBERED.match(text)
        if match:
            entries.append((int(match.group(1)), match.group(2), text))
        elif entries:
            break

    errors: list[str] = []
    warnings: list[str] = []
    if not entries:
        errors.append("参考文献标题后未找到形如 [1] 的独立条目。")
    numbers = [n for n, _, _ in entries]
    expected = list(range(1, len(entries) + 1))
    if numbers != expected:
        errors.append(f"编号不连续或未从 1 开始：{numbers}。")

    for number, body, _ in entries:
        marks = TYPE_MARK.findall(body)
        if not marks:
            errors.append(f"[{number}] 缺少文献类型标识。")
        else:
            kind, carrier = marks[-1]
            if kind not in ALLOWED_TYPES:
                errors.append(f"[{number}] 文献类型标识 {kind} 不在检查器允许集合中。")
            if carrier and carrier != "OL":
                warnings.append(f"[{number}] 载体标识 /{carrier} 请人工核验。")
        if "." not in body and "．" not in body:
            errors.append(f"[{number}] 未检测到责任者与题名之间的分隔标点。")
        if re.search(r"https?://", body, re.I) and not re.search(r"[\[［]\d{4}[-/.]\d{1,2}[-/.]\d{1,2}[\]］]", body):
            warnings.append(f"[{number}] 含 URL，但未检测到完整引用日期。")
        if not re.search(r"\b(?:19|20)\d{2}\b", body):
            warnings.append(f"[{number}] 未检测到四位年份，请核验日期字段。")

    emit(
        {
            "status": "pass" if not errors else "fail",
            "standard": "GB/T 7714—2025",
            "entries": len(entries),
            "errors": errors,
            "warnings": warnings,
            "note": "本检查仅验证可自动判断的形式规则；首次引用顺序、来源真实性和字段完整性仍需人工复核。",
        },
        0 if not errors else 1,
    )


if __name__ == "__main__":
    main()
