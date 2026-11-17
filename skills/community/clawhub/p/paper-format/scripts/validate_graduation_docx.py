#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from docx import Document


def configure_utf8_console() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


configure_utf8_console()

GENERIC_CHECKS = (
    "check_docx_content.py",
    "check_black_text.py",
    "check_line_spacing.py",
    "check_paragraph_spacing.py",
)

LAYOUT_CHECKS = (
    "check_front_matter_pages.py",
    "check_toc_layout.py",
    "check_cover_layout.py",
    "check_heading_numbering.py",
    "check_page_numbering.py",
    "check_page_fields.py",
    "check_body_alignment.py",
)


def feature_flags(target: str) -> dict[str, bool]:
    """Detect whether adaptive checks have relevant source material."""
    try:
        doc = Document(target)
    except Exception:
        # The generic content check will report the actionable parse error.
        return {name: False for name in LAYOUT_CHECKS}
    paragraphs = [(p.text.strip(), p.style.name) for p in doc.paragraphs]
    compact = ["".join(text.split()).replace("　", "").upper() for text, _ in paragraphs]
    has_body = any(
        text in {"绪论", "引言"} or (text.startswith("第") and "章" in text[:8])
        for text in compact
    )
    return {
        "check_front_matter_pages.py": any(text in {"摘要", "中文摘要", "ABSTRACT", "目录"} for text in compact),
        "check_toc_layout.py": any(text == "目录" for text in compact),
        "check_cover_layout.py": any(text.startswith(label) for text in compact for label in ("姓名", "专业", "学校", "学号", "学院", "指导教师")),
        "check_heading_numbering.py": any(
            style.startswith(("Heading", "标题")) or text.startswith("第") and "章" in text[:8]
            for text, style in paragraphs
        ),
        "check_page_numbering.py": has_body,
        "check_page_fields.py": has_body,
        "check_body_alignment.py": has_body,
    }


def main():
    parser = argparse.ArgumentParser(description="毕业论文 DOCX 结构验收。")
    parser.add_argument("docx")
    parser.add_argument(
        "--references",
        choices=("auto", "required", "skip"),
        default="auto",
        help="auto=仅检查原稿已有参考文献；required=参考文献缺失即失败；skip=用户确认跳过",
    )
    parser.add_argument(
        "--fields",
        choices=("structure", "visible"),
        default="structure",
        help="structure=字段刷新工具不可用；visible=已刷新并要求可见数字结果",
    )
    parser.add_argument(
        "--layout",
        choices=("adaptive", "standard", "template"),
        default="adaptive",
        help="adaptive=仅检查已识别结构；standard=强制默认毕业论文布局；template=不套默认布局硬检查",
    )
    args = parser.parse_args()
    target = str(Path(args.docx).resolve())
    folder = Path(__file__).resolve().parent
    child_env = os.environ.copy()
    child_env["PYTHONUTF8"] = "1"
    child_env["PYTHONIOENCODING"] = "utf-8"
    results = []
    commands = [(name, [sys.executable, str(folder / name), target]) for name in GENERIC_CHECKS]
    skipped = []
    if args.layout == "standard":
        selected_layout_checks = LAYOUT_CHECKS
    elif args.layout == "template":
        selected_layout_checks = ()
        skipped.extend((name, "正式模板模式：默认毕业论文布局检查不适用。") for name in LAYOUT_CHECKS)
    else:
        flags = feature_flags(target)
        selected_layout_checks = tuple(name for name in LAYOUT_CHECKS if flags.get(name, False))
        skipped.extend((name, "自适应模式：原稿未识别到该结构。") for name in LAYOUT_CHECKS if not flags.get(name, False))
    for name in selected_layout_checks:
        command = [sys.executable, str(folder / name), target]
        if name == "check_front_matter_pages.py":
            command.extend(["--mode", "required" if args.layout == "standard" else "auto"])
        elif name == "check_page_fields.py":
            command.extend(["--mode", args.fields])
        commands.append((name, command))
    commands.append(
        (
            "check_gbt7714_2025.py",
            [sys.executable, str(folder / "check_gbt7714_2025.py"), target, "--mode", args.references],
        )
    )
    for name, command in commands:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=child_env,
        )
        try:
            detail = json.loads(process.stdout or "")
        except (json.JSONDecodeError, TypeError):
            detail = {"stdout": process.stdout.strip(), "stderr": process.stderr.strip()}
        result_status = "fail" if process.returncode else ("skipped" if detail.get("status") == "skipped" else "pass")
        results.append({"check": name, "status": result_status, "detail": detail})
    for name, reason in skipped:
        results.append({"check": name, "status": "skipped", "detail": {"reason": reason}})
    failed = [item["check"] for item in results if item["status"] == "fail"]
    report = {
        "status": "pass" if not failed else "fail",
        "file": target,
        "references_mode": args.references,
        "layout_mode": args.layout,
        "fields_mode": args.fields,
        "failed": failed,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
