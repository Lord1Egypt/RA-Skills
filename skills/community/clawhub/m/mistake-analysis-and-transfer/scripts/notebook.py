#!/usr/bin/env python3
"""错题整理巩固技能的本地错题本辅助脚本。"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any


DEFAULT_ROOT = "mistake-notebook"
CONFIG_NAME = ".mistake-notebook-config.json"
INDEX_NAME = "index.jsonl"
MISSING_LABEL = "未提供/未识别"
STUDENT_MISSING_LABEL = "未提供学生作答；仅保存题目解析，无法精准归因。"
REQUIRED_FIELD_GROUPS = {
    "题目": ("question", "problem", "题目", "原题", "原题关键信息"),
    "科目": ("subject", "学科", "科目"),
    "题型": ("problem_type", "题型"),
    "正确答案": ("correct_answer", "answer_key", "standard_answer", "正确答案", "标准答案", "答案"),
    "正确解析或关键步骤": (
        "solution",
        "answer_analysis",
        "analysis",
        "correction",
        "correct_path",
        "解析",
        "答案解析",
        "正确解法",
        "偏离位置与纠正",
    ),
    "核心知识点": ("knowledge_points", "core_knowledge", "knowledge", "核心知识点", "知识点"),
    "巩固建议": (
        "consolidation_advice",
        "consolidation",
        "巩固建议",
        "本题复盘重点",
        "同类题自查动作",
        "需要巩固的知识或步骤",
        "summary",
        "review_points",
        "self_check",
        "总结",
        "总结与知识点梳理",
        "下次自查点",
    ),
}
HEADING_TRANSLATIONS = {
    "Question": "题目",
    "Student Answer": "学生作答",
    "Correct Answer": "正确答案",
    "Root Cause": "错误根因",
    "Evidence": "证据",
    "Knowledge Points": "核心知识点",
    "Correction": "偏离位置与纠正",
    "Consolidation Advice": "巩固建议",
    "Summary": "总结与复盘",
    "Review Points": "下次自查点",
    "Source": "来源",
}
META_LABEL_TRANSLATIONS = {
    "ID": "错题 ID",
    "Date": "日期",
    "Subject": "科目",
    "Problem type": "题型",
    "Error type": "错误类型",
    "Confidence": "归因置信度",
    "Tags": "标签",
}


def now_iso() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def today_iso() -> str:
    return dt.date.today().isoformat()


def config_path() -> Path:
    return Path.cwd() / CONFIG_NAME


def read_config_root() -> Path | None:
    path = config_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    root = data.get("root")
    return Path(root).expanduser() if root else None


def resolve_root(value: str | None = None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    configured = read_config_root()
    if configured:
        return configured.resolve()
    return (Path.cwd() / DEFAULT_ROOT).resolve()


def ensure_notebook(root: Path) -> None:
    (root / "subjects").mkdir(parents=True, exist_ok=True)
    (root / INDEX_NAME).touch(exist_ok=True)


def write_config(root: Path) -> None:
    data = {"root": str(root), "updated_at": now_iso()}
    config_path().write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def clean_part(value: Any, fallback: str = "item", limit: int = 60) -> str:
    text = str(value or "").strip() or fallback
    text = re.sub(r'[\\/:*?"<>|\r\n\t]+', "-", text)
    text = re.sub(r"\s+", "-", text)
    text = text.strip(" .-_") or fallback
    return text[:limit]


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    return [item.strip() for item in re.split(r"[,;；、\n]+", text) if item.strip()]


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value).strip()


def display_text(value: Any, placeholder: str = MISSING_LABEL) -> str:
    text = as_text(value)
    return text if text else placeholder


def display_bullets(items: list[str], placeholder: str = MISSING_LABEL) -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {placeholder}"


def first_value(entry: dict[str, Any], names: tuple[str, ...]) -> Any:
    return field(entry, *names)


def missing_required(entry: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for label, names in REQUIRED_FIELD_GROUPS.items():
        value = first_value(entry, names)
        if label == "核心知识点":
            if not as_list(value):
                missing.append(label)
        elif not as_text(value):
            missing.append(label)
    return missing


def localize_markdown_text(text: str) -> str:
    localized = text
    for source, target in HEADING_TRANSLATIONS.items():
        localized = re.sub(rf"(?m)^## {re.escape(source)}\s*$", f"## {target}", localized)
    for source, target in META_LABEL_TRANSLATIONS.items():
        localized = re.sub(rf"(?m)^- {re.escape(source)}:\s*", f"- {target}: ", localized)
    return localized


def read_index(root: Path) -> list[dict[str, Any]]:
    path = root / INDEX_NAME
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def write_index(root: Path, rows: list[dict[str, Any]]) -> None:
    path = root / INDEX_NAME
    payload = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8")


def field(entry: dict[str, Any], *names: str, default: Any = "") -> Any:
    for name in names:
        if name in entry and entry[name] not in (None, ""):
            return entry[name]
    return default


def markdown_for(entry: dict[str, Any], index_row: dict[str, Any]) -> str:
    knowledge = as_list(field(entry, "knowledge_points", "core_knowledge", "knowledge", "核心知识点", "知识点"))
    error_types = as_list(field(entry, "error_types", "error_type", "主要类型", "主要错误类型", "错误类型"))
    tags = as_list(field(entry, "tags", "标签"))
    missing = missing_required(entry)
    correct_answer = field(entry, "correct_answer", "answer_key", "standard_answer", "正确答案", "标准答案", "答案")
    solution = field(
        entry,
        "solution",
        "answer_analysis",
        "analysis",
        "correction",
        "correct_path",
        "解析",
        "答案解析",
        "正确解法",
        "偏离位置与纠正",
    )
    student_answer = field(entry, "student_answer", "student_work", "我的作答", "学生作答")
    root_cause = field(entry, "root_cause", "主要类型", "主要错误类型", "错误根因")
    consolidation_advice = field(
        entry,
        "consolidation_advice",
        "consolidation",
        "巩固建议",
        "本题复盘重点",
        "同类题自查动作",
        "需要巩固的知识或步骤",
    )

    parts = [
        f"# {index_row['title']}",
        "",
        f"- 错题 ID: {index_row['id']}",
        f"- 日期: {index_row['date']}",
        f"- 科目: {index_row['subject']}",
        f"- 题型: {index_row.get('problem_type', '') or MISSING_LABEL}",
        f"- 错误类型: {', '.join(error_types) if error_types else MISSING_LABEL}",
        f"- 归因置信度: {display_text(field(entry, 'confidence', '置信度'))}",
        f"- 标签: {', '.join(tags) if tags else MISSING_LABEL}",
        f"- 保存完整性: {'完整' if not missing else '缺少：' + '、'.join(missing)}",
        "",
        "## 题目",
        display_text(field(entry, "question", "problem", "题目", "原题", "原题关键信息")),
        "",
        "## 学生作答",
        display_text(student_answer, STUDENT_MISSING_LABEL),
        "",
        "## 正确答案",
        display_text(correct_answer),
        "",
        "## 正确解析",
        display_text(solution),
        "",
        "## 错误根因",
        display_text(root_cause, "未提供学生作答，无法精准归因。" if not as_text(student_answer) else MISSING_LABEL),
        "",
        "## 证据",
        display_text(field(entry, "evidence", "证据")),
        "",
        "## 核心知识点",
        display_bullets(knowledge),
        "",
        "## 偏离位置与纠正",
        display_text(field(entry, "deviation", "correction", "偏离位置与纠正", "错误发生点")),
        "",
        "## 巩固建议",
        display_text(consolidation_advice),
        "",
        "## 总结与复盘",
        display_text(field(entry, "summary", "总结", "总结与知识点梳理")),
        "",
        "## 下次自查点",
        display_text(field(entry, "review_points", "self_check", "下次自查点")),
        "",
        "## 来源",
        display_text(field(entry, "source", "来源")),
        "",
    ]
    return "\n".join(parts)


def load_entry(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.json_file:
        return json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    raw = sys.stdin.read()
    if not raw.strip():
        raise SystemExit("请提供 --json、--json-file，或从标准输入传入 JSON。")
    return json.loads(raw)


def save_entry(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    ensure_notebook(root)
    entry = load_entry(args)
    missing = missing_required(entry)
    if missing and not args.allow_incomplete:
        raise SystemExit(
            "缺少错题本必备字段："
            + "、".join(missing)
            + "。请先补全分析后再保存；只有用户明确要求先保存草稿时，才使用 --allow-incomplete。"
        )
    date = str(field(entry, "date", "日期", default=today_iso()))[:10]
    subject = str(field(entry, "subject", "学科", default="unspecified")).strip() or "unspecified"
    title = str(field(entry, "title", "题型", "problem_type", default="mistake")).strip() or "mistake"
    entry_id = str(field(entry, "id", default=f"{date.replace('-', '')}-{uuid.uuid4().hex[:8]}"))
    problem_type = str(field(entry, "problem_type", "题型", default=""))
    knowledge = as_list(field(entry, "knowledge_points", "core_knowledge", "knowledge", "核心知识点", "知识点"))
    error_types = as_list(field(entry, "error_types", "error_type", "主要类型", "主要错误类型", "错误类型"))
    tags = as_list(field(entry, "tags", "标签"))
    correct_answer = as_text(field(entry, "correct_answer", "answer_key", "standard_answer", "正确答案", "标准答案", "答案"))

    rel_path = Path("subjects") / clean_part(subject, "subject") / date[:7] / (
        f"{date}-{clean_part(title, 'mistake', 48)}-{clean_part(entry_id, 'id', 32)}.md"
    )
    abs_path = root / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)

    index_row = {
        "id": entry_id,
        "date": date,
        "subject": subject,
        "title": title,
        "problem_type": problem_type,
        "knowledge_points": knowledge,
        "error_types": error_types,
        "answer_preview": correct_answer[:120],
        "confidence": str(field(entry, "confidence", "置信度", default="")),
        "tags": tags,
        "file": str(rel_path),
        "updated_at": now_iso(),
    }

    abs_path.write_text(markdown_for(entry, index_row), encoding="utf-8")
    rows = [row for row in read_index(root) if row.get("id") != entry_id]
    rows.append(index_row)
    rows.sort(key=lambda row: (row.get("subject", ""), row.get("date", ""), row.get("id", "")))
    write_index(root, rows)
    print(
        json.dumps(
            {"root": str(root), "entry": index_row, "file": str(abs_path), "missing_required": missing},
            ensure_ascii=False,
            indent=2,
        )
    )


def matches(row: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.subject and row.get("subject") != args.subject:
        return False
    if args.date and not str(row.get("date", "")).startswith(args.date):
        return False
    if args.error_type and args.error_type not in as_list(row.get("error_types")):
        return False
    if args.keyword:
        haystack = json.dumps(row, ensure_ascii=False).lower()
        if args.keyword.lower() not in haystack:
            return False
    return True


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("展示数量必须是正整数。")
    return number


def sort_entries(rows: list[dict[str, Any]], recent: bool = False) -> list[dict[str, Any]]:
    if recent:
        return sorted(
            rows,
            key=lambda item: (item.get("date", ""), item.get("updated_at", ""), item.get("id", "")),
            reverse=True,
        )
    return sorted(rows, key=lambda item: (item.get("subject", ""), item.get("date", ""), item.get("id", "")))


def list_entries(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    matched_rows = [row for row in read_index(root) if matches(row, args)]
    sorted_rows = sort_entries(matched_rows, args.recent)
    total = len(sorted_rows)
    rows = sorted_rows[: args.limit] if args.limit else sorted_rows
    truncated = len(rows) < total
    if args.json_output:
        print(
            json.dumps(
                {
                    "root": str(root),
                    "total": total,
                    "shown": len(rows),
                    "truncated": truncated,
                    "entries": rows,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print(f"错题本根目录：{root}")
    print(f"错题总数：{total}")
    if not sorted_rows:
        print("未找到符合条件的错题。")
        return
    if truncated:
        print(f"本次展示：{len(rows)} 条（按用户要求截断）")
    else:
        print(f"本次展示：全部 {total} 条")
    if args.recent:
        print("\n最近错题")
        for row in rows:
            errors = ", ".join(as_list(row.get("error_types"))) or MISSING_LABEL
            knowledge = ", ".join(as_list(row.get("knowledge_points"))) or MISSING_LABEL
            answer = row.get("answer_preview") or MISSING_LABEL
            print(
                f"  - {row.get('date')} | {row.get('subject')} | {row.get('id')} | "
                f"{row.get('title')} | {errors} | {knowledge} | 答案: {answer} | {row.get('file')}"
            )
        return
    current_subject = None
    current_date = None
    for row in rows:
        if row.get("subject") != current_subject:
            current_subject = row.get("subject")
            current_date = None
            print(f"\n{current_subject}")
        if row.get("date") != current_date:
            current_date = row.get("date")
            print(f"  {current_date}")
        errors = ", ".join(as_list(row.get("error_types"))) or MISSING_LABEL
        knowledge = ", ".join(as_list(row.get("knowledge_points"))) or MISSING_LABEL
        answer = row.get("answer_preview") or MISSING_LABEL
        print(f"    - {row.get('id')} | {row.get('title')} | {errors} | {knowledge} | 答案: {answer} | {row.get('file')}")


def show_entry(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    for row in read_index(root):
        if row.get("id") == args.id:
            path = root / row["file"]
            print(localize_markdown_text(path.read_text(encoding="utf-8")))
            return
    raise SystemExit(f"未找到错题：{args.id}")


def localize_entries(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    subject_root = root / "subjects"
    changed: list[str] = []
    if subject_root.exists():
        for path in subject_root.rglob("*.md"):
            original = path.read_text(encoding="utf-8")
            localized = localize_markdown_text(original)
            if localized != original:
                path.write_text(localized, encoding="utf-8")
                changed.append(str(path))

    if args.json_output:
        print(json.dumps({"root": str(root), "changed_files": changed}, ensure_ascii=False, indent=2))
        return
    print(f"错题本根目录：{root}")
    print(f"已转换文件数：{len(changed)}")
    for path in changed:
        print(f"- {path}")


def init_notebook(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    ensure_notebook(root)
    print(json.dumps({"root": str(root), "index": str(root / INDEX_NAME)}, ensure_ascii=False, indent=2))


def set_root(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    ensure_notebook(root)
    write_config(root)
    print(json.dumps({"root": str(root), "config": str(config_path())}, ensure_ascii=False, indent=2))


def print_root(args: argparse.Namespace) -> None:
    root = resolve_root(args.root)
    print(str(root))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理本地错题本。")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--root")
    init_parser.set_defaults(func=init_notebook)

    root_parser = subparsers.add_parser("root")
    root_parser.add_argument("--root")
    root_parser.set_defaults(func=print_root)

    set_root_parser = subparsers.add_parser("set-root")
    set_root_parser.add_argument("--root", required=True)
    set_root_parser.set_defaults(func=set_root)

    save_parser = subparsers.add_parser("save")
    save_parser.add_argument("--root")
    save_parser.add_argument("--json")
    save_parser.add_argument("--json-file")
    save_parser.add_argument("--allow-incomplete", action="store_true")
    save_parser.set_defaults(func=save_entry)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--root")
    list_parser.add_argument("--subject")
    list_parser.add_argument("--date", help="日期前缀：YYYY、YYYY-MM 或 YYYY-MM-DD")
    list_parser.add_argument("--error-type")
    list_parser.add_argument("--keyword")
    list_parser.add_argument("--limit", type=positive_int)
    list_parser.add_argument("--recent", action="store_true")
    list_parser.add_argument("--json-output", action="store_true")
    list_parser.set_defaults(func=list_entries)

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("--root")
    show_parser.add_argument("--id", required=True)
    show_parser.set_defaults(func=show_entry)

    localize_parser = subparsers.add_parser("localize")
    localize_parser.add_argument("--root")
    localize_parser.add_argument("--json-output", action="store_true")
    localize_parser.set_defaults(func=localize_entries)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
