#!/usr/bin/env python3
"""家长版小学作文成长档案管理脚本。

本脚本只管理最小化摘要，不保存作文全文、原图、完整 OCR 或无关个人信息。
所有输入文件必须位于 --store-dir 指定的数据目录内，避免脚本从任意位置读取隐私数据。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

# 数据协议版本。修改结构时必须升级版本，避免旧档案被误读。
SCHEMA_VERSION = "parent-growth-profile/1"

# 设置对象的严格字段白名单。
SETTINGS_FIELDS = {
    "profile_enabled",
    "privacy_notice_confirmed",
    "nickname",
    "grade_level",
    "default_mode",
    "child_facing_output",
    "advanced_review_offer",
}

# 单次批改摘要的严格字段白名单。
REVIEW_FIELDS = {
    "review_id",
    "date",
    "grade_level",
    "title",
    "composition_type",
    "strengths",
    "recurring_issues",
    "next_goals",
    "dimension_summaries",
    "teacher_requirements",
}

# 成长档案对象的严格字段白名单。record 哈希和派生字段由脚本维护。
PROFILE_FIELDS = {
    "schema_version",
    "created_date",
    "updated_date",
    "records",
    "used_review_id_hashes",
    "recurring_issues",
    "documented_progress",
    "current_goals",
}

# 四个固定分析维度，不允许添加或改名。
DIMENSION_FIELDS = {"content", "structure", "language", "conventions"}

# 支持的批改模式。
DEFAULT_MODES = {"full", "quick_check", "structure", "encouraging"}

# 进阶版提示偏好。declined 表示用户已拒绝，Skill 之后不应主动展示。
ADVANCED_REVIEW_OFFER_STATES = {"unoffered", "declined", "interested", "enabled"}

# 便携导出文件的严格字段。
PORTABLE_FIELDS = {"schema_version", "parent_settings", "growth_profile"}


def fail(message: str) -> None:
    """输出错误信息并以非零状态退出。"""
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False), file=sys.stderr)
    raise SystemExit(1)


def require_object(value: Any, name: str) -> dict[str, Any]:
    """确认 JSON 值是对象。"""
    if not isinstance(value, dict):
        fail(f"{name} 必须是 JSON 对象")
    return value


def require_exact_fields(value: dict[str, Any], allowed: set[str], name: str) -> None:
    """严格检查字段白名单，拒绝未知字段，避免未来隐私数据被意外写入。"""
    unknown = sorted(set(value) - allowed)
    if unknown:
        fail(f"{name} 包含未知字段: {', '.join(unknown)}")


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{name} 必须是布尔值")
    return value


def require_int(value: Any, name: str, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        fail(f"{name} 必须是 {minimum}-{maximum} 的整数")
    return value


def require_string(value: Any, name: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        fail(f"{name} 必须是非空字符串")
    return value


def require_nullable_string(value: Any, name: str) -> str | None:
    if value is None:
        return None
    return require_string(value, name)


def require_string_array(value: Any, name: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        fail(f"{name} 必须是非空字符串数组")
    for index, item in enumerate(value, start=1):
        require_string(item, f"{name}[{index}]")
    return value


def require_date(value: Any, name: str) -> str:
    text = require_string(value, name)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        fail(f"{name} 必须使用 YYYY-MM-DD 格式")
        raise
    if parsed.isoformat() != text:
        fail(f"{name} 必须使用 YYYY-MM-DD 格式")
    return text


def load_json_file(path: Path, name: str) -> dict[str, Any]:
    """读取并解析 JSON 文件。"""
    if not path.is_file():
        fail(f"{name} 不存在: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"无法读取 {name}: {exc}")
        raise
    return require_object(value, name)


def validate_settings(value: dict[str, Any]) -> dict[str, Any]:
    """校验家长设置。"""
    require_exact_fields(value, SETTINGS_FIELDS, "parent_settings")
    profile_enabled = require_bool(value["profile_enabled"], "profile_enabled")
    privacy_confirmed = require_bool(value["privacy_notice_confirmed"], "privacy_notice_confirmed")
    nickname = value["nickname"]
    if nickname is not None:
        nickname = require_string(nickname, "nickname")
    grade_level = require_int(value["grade_level"], "grade_level", 1, 6)
    default_mode = require_string(value["default_mode"], "default_mode")
    if default_mode not in DEFAULT_MODES:
        fail(f"default_mode 只能是: {', '.join(sorted(DEFAULT_MODES))}")
    child_facing = require_bool(value["child_facing_output"], "child_facing_output")
    advanced_offer = require_string(value["advanced_review_offer"], "advanced_review_offer")
    if advanced_offer not in ADVANCED_REVIEW_OFFER_STATES:
        fail(f"advanced_review_offer 只能是: {', '.join(sorted(ADVANCED_REVIEW_OFFER_STATES))}")

    # 只有家长明确确认隐私说明后，才允许开启成长档案。
    if profile_enabled and not privacy_confirmed:
        fail("开启成长档案前，privacy_notice_confirmed 必须为 true")

    return {
        "profile_enabled": profile_enabled,
        "privacy_notice_confirmed": privacy_confirmed,
        "nickname": nickname,
        "grade_level": grade_level,
        "default_mode": default_mode,
        "child_facing_output": child_facing,
        "advanced_review_offer": advanced_offer,
    }


def validate_review(value: dict[str, Any]) -> dict[str, Any]:
    """校验单次批改摘要。"""
    require_exact_fields(value, REVIEW_FIELDS, "review")
    review_id = require_string(value["review_id"], "review_id")
    review_date = require_date(value["date"], "review.date")
    grade_level = require_int(value["grade_level"], "grade_level", 1, 6)
    title = require_string(value["title"], "title")
    composition_type = require_string(value["composition_type"], "composition_type")
    strengths = require_string_array(value["strengths"], "strengths")
    recurring_issues = require_string_array(value["recurring_issues"], "recurring_issues", allow_empty=True)
    next_goals = require_string_array(value["next_goals"], "next_goals")
    if len(next_goals) > 2:
        fail("next_goals 最多只能有 2 项，避免训练目标过多")

    dimensions = require_object(value["dimension_summaries"], "dimension_summaries")
    require_exact_fields(dimensions, DIMENSION_FIELDS, "dimension_summaries")
    normalized_dimensions = {
        key: require_string(dimensions[key], f"dimension_summaries.{key}")
        for key in sorted(DIMENSION_FIELDS)
    }

    return {
        "review_id": review_id,
        "date": review_date,
        "grade_level": grade_level,
        "title": title,
        "composition_type": composition_type,
        "strengths": strengths,
        "recurring_issues": recurring_issues,
        "next_goals": next_goals,
        "dimension_summaries": normalized_dimensions,
        "teacher_requirements": require_nullable_string(value["teacher_requirements"], "teacher_requirements"),
    }


def validate_profile(value: dict[str, Any], require_records: bool = True) -> dict[str, Any]:
    """校验成长档案。"""
    require_exact_fields(value, PROFILE_FIELDS, "growth_profile")
    if value["schema_version"] != SCHEMA_VERSION:
        fail(f"growth_profile.schema_version 必须是 {SCHEMA_VERSION}")
    created_date = require_date(value["created_date"], "created_date")
    updated_date = require_date(value["updated_date"], "updated_date")
    records_value = value["records"]
    if not isinstance(records_value, list):
        fail("records 必须是数组")
    records = [validate_review(require_object(item, f"records[{index}]")) for index, item in enumerate(records_value, start=1)]
    if require_records and not records:
        fail("records 不能为空")

    ids = [record["review_id"] for record in records]
    if len(ids) != len(set(ids)):
        fail("records 中 review_id 重复")
    hashes = require_string_array(value["used_review_id_hashes"], "used_review_id_hashes", allow_empty=True)
    expected_hashes = [hashlib.sha256(item.encode("utf-8")).hexdigest() for item in ids]
    # 已删除记录的哈希也会保留，因此这里只检查所有现存记录均已登记。
    missing = set(expected_hashes) - set(hashes)
    if missing:
        fail("used_review_id_hashes 缺少现存记录的编号指纹")

    recurring_issues = require_string_array(value["recurring_issues"], "recurring_issues", allow_empty=True)
    documented_progress = require_string_array(value["documented_progress"], "documented_progress", allow_empty=True)
    current_goals = require_string_array(value["current_goals"], "current_goals", allow_empty=True)
    if len(current_goals) > 2:
        fail("current_goals 最多只能有 2 项")

    return {
        "schema_version": SCHEMA_VERSION,
        "created_date": created_date,
        "updated_date": updated_date,
        "records": records,
        "used_review_id_hashes": hashes,
        "recurring_issues": recurring_issues,
        "documented_progress": documented_progress,
        "current_goals": current_goals,
    }


def validate_portable(value: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """校验便携档案。"""
    require_exact_fields(value, PORTABLE_FIELDS, "portable")
    if value["schema_version"] != SCHEMA_VERSION:
        fail(f"schema_version 必须是 {SCHEMA_VERSION}")
    settings = validate_settings(require_object(value["parent_settings"], "parent_settings"))
    if not settings["profile_enabled"]:
        fail("导入的 parent_settings.profile_enabled 必须为 true")
    profile = validate_profile(require_object(value["growth_profile"], "growth_profile"))
    return settings, profile


def store_path(store_dir: Path, relative: str, name: str) -> Path:
    """把输入文件解析到数据目录内，禁止路径穿越。"""
    path = Path(relative)
    if path.is_absolute():
        fail(f"{name} 必须是 --store-dir 内的相对路径")
    resolved = (store_dir / path).resolve()
    try:
        resolved.relative_to(store_dir)
    except ValueError:
        fail(f"{name} 不能位于 --store-dir 外")
    return resolved


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    """原子写入 JSON，避免写入中断造成档案损坏。"""
    # 导出文件可能位于 store-dir 内的子目录，例如 exports/profile.json。
    # 先创建父目录，确保临时文件和最终文件处于同一文件系统，便于原子替换。
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.tmp")
    try:
        temp_path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temp_path, path)
    except OSError as exc:
        fail(f"写入文件失败: {exc}")
        raise
    finally:
        if temp_path.exists():
            temp_path.unlink()


def read_settings(store_dir: Path) -> dict[str, Any] | None:
    path = store_dir / "settings.json"
    if not path.exists():
        return None
    return validate_settings(load_json_file(path, "parent_settings"))


def write_settings(store_dir: Path, settings: dict[str, Any]) -> None:
    atomic_write_json(store_dir / "settings.json", settings)


def read_profile(store_dir: Path) -> dict[str, Any] | None:
    path = store_dir / "growth-profile.json"
    if not path.exists():
        return None
    return validate_profile(load_json_file(path, "growth_profile"))


def require_enabled_settings(settings: dict[str, Any] | None) -> dict[str, Any]:
    if settings is None:
        fail("尚未设置家长偏好，请先执行 settings-set")
    if not settings["profile_enabled"]:
        fail("成长档案未启用，不能执行档案操作")
    return settings


def review_hash(review_id: str) -> str:
    """生成批改编号指纹，删除后仍可防止编号重用。"""
    return hashlib.sha256(review_id.encode("utf-8")).hexdigest()


def rebuild_profile(old: dict[str, Any], records: list[dict[str, Any]], today: str) -> dict[str, Any]:
    """根据详细记录重建派生字段，保持数据一致。"""
    # 详细记录最多保留 20 条，更早记录直接不再保存，符合第一版最小化设计。
    records = records[-20:]

    issue_counter: dict[str, int] = {}
    progress_counter: dict[str, int] = {}
    for record in records:
        for issue in record["recurring_issues"]:
            issue_counter[issue] = issue_counter.get(issue, 0) + 1
        for strength in record["strengths"]:
            progress_counter[strength] = progress_counter.get(strength, 0) + 1

    # 只有最近 5 次仍出现的问题才作为持续问题，避免历史问题永远占据当前目标。
    recent_issues = {issue for record in records[-5:] for issue in record["recurring_issues"]}

    current_goals: list[str] = []
    if records:
        for goal in records[-1]["next_goals"]:
            if goal not in current_goals:
                current_goals.append(goal)
    current_goals = current_goals[:2]

    old_hashes = list(old.get("used_review_id_hashes", []))
    hashes = old_hashes + [review_hash(record["review_id"]) for record in records]
    # 去重但保持顺序。
    seen = set()
    unique_hashes = []
    for item in hashes:
        if item not in seen:
            seen.add(item)
            unique_hashes.append(item)

    return {
        "schema_version": SCHEMA_VERSION,
        "created_date": old.get("created_date", today),
        "updated_date": today,
        "records": records,
        "used_review_id_hashes": unique_hashes,
        "recurring_issues": sorted(recent_issues),
        "documented_progress": sorted(progress_counter),
        "current_goals": current_goals,
    }


def print_json(value: dict[str, Any]) -> None:
    print(json.dumps({"ok": True, **value}, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理家长版小学作文成长档案")
    parser.add_argument("--store-dir", required=True, help="档案数据目录，所有输入输出均须位于其中")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("settings-get", help="读取家长设置")
    settings_set = subparsers.add_parser("settings-set", help="写入家长设置")
    settings_set.add_argument("--settings", required=True, help="settings.json 的相对路径")
    subparsers.add_parser("get", help="读取成长档案")

    append = subparsers.add_parser("append", help="追加单次批改摘要")
    append.add_argument("--review", required=True, help="review.json 的相对路径")
    append.add_argument("--confirmed", action="store_true", help="确认写入")

    update = subparsers.add_parser("update-review", help="修正单次批改摘要")
    update.add_argument("--review-id", required=True, help="要修正的批改编号")
    update.add_argument("--review", required=True, help="替换后的 review.json 相对路径")
    update.add_argument("--confirmed", action="store_true", help="确认修正")

    delete_review = subparsers.add_parser("delete-review", help="删除单次批改摘要")
    delete_review.add_argument("--review-id", required=True, help="要删除的批改编号")

    delete_profile = subparsers.add_parser("delete-profile", help="删除整个成长档案")
    delete_profile.add_argument("--confirm-delete", action="store_true", help="确认整档删除")

    export = subparsers.add_parser("export", help="导出便携档案")
    export.add_argument("--output", required=True, help="导出 JSON 的相对路径")

    import_profile = subparsers.add_parser("import", help="导入便携档案")
    import_profile.add_argument("--input", required=True, help="便携 JSON 的相对路径")
    import_profile.add_argument("--confirmed", action="store_true", help="确认导入")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    store_dir = Path(args.store_dir).resolve()
    try:
        store_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        fail(f"无法创建数据目录: {exc}")
        raise

    today = date.today().isoformat()
    settings_path = store_dir / "settings.json"
    profile_path = store_dir / "growth-profile.json"

    if args.command == "settings-get":
        settings = read_settings(store_dir)
        if settings is None:
            fail("尚未设置家长偏好")
        print_json({"settings": settings})
        return

    if args.command == "settings-set":
        value = load_json_file(store_path(store_dir, args.settings, "settings"), "parent_settings")
        settings = validate_settings(value)
        write_settings(store_dir, settings)
        print_json({"settings": settings})
        return

    # import 会写入完整的设置和档案，因此不能要求目标目录已经存在设置。
    # 其他档案操作必须先确认设置已启用。
    if args.command == "import":
        if not args.confirmed:
            fail("家长尚未确认导入，不能执行 import")
        if settings_path.exists() or profile_path.exists():
            fail("当前数据目录已有设置或档案，导入不会覆盖既有数据")
        portable = load_json_file(store_path(store_dir, args.input, "input"), "portable")
        imported_settings, imported_profile = validate_portable(portable)
        write_settings(store_dir, imported_settings)
        atomic_write_json(profile_path, imported_profile)
        print_json({"growth_profile": imported_profile})
        return

    settings = require_enabled_settings(read_settings(store_dir))

    if args.command == "get":
        profile = read_profile(store_dir)
        if profile is None:
            fail("成长档案不存在")
        print_json({"growth_profile": profile})
        return

    if args.command == "append":
        if not args.confirmed:
            fail("家长尚未确认写入，不能执行 append")
        review = validate_review(load_json_file(store_path(store_dir, args.review, "review"), "review"))
        profile = read_profile(store_dir) or {
            "schema_version": SCHEMA_VERSION,
            "created_date": today,
            "updated_date": today,
            "records": [],
            "used_review_id_hashes": [],
            "recurring_issues": [],
            "documented_progress": [],
            "current_goals": [],
        }
        if review_hash(review["review_id"]) in profile["used_review_id_hashes"]:
            fail("该 review_id 已使用过，不能重复写入")
        records = profile["records"] + [review]
        updated = rebuild_profile(profile, records, today)
        atomic_write_json(profile_path, updated)
        print_json({"growth_profile": updated})
        return

    if args.command == "update-review":
        if not args.confirmed:
            fail("家长尚未确认修正，不能执行 update-review")
        review = validate_review(load_json_file(store_path(store_dir, args.review, "review"), "review"))
        if review["review_id"] != args.review_id:
            fail("替换记录的 review_id 必须与 --review-id 一致")
        profile = read_profile(store_dir)
        if profile is None:
            fail("成长档案不存在")
        index = next((i for i, item in enumerate(profile["records"]) if item["review_id"] == args.review_id), None)
        if index is None:
            fail("指定的 review_id 不存在或已被压缩删除")
        records = profile["records"].copy()
        records[index] = review
        updated = rebuild_profile(profile, records, today)
        atomic_write_json(profile_path, updated)
        print_json({"growth_profile": updated})
        return

    if args.command == "delete-review":
        profile = read_profile(store_dir)
        if profile is None:
            fail("成长档案不存在")
        if args.review_id not in {item["review_id"] for item in profile["records"]}:
            fail("指定的 review_id 不存在")
        records = [item for item in profile["records"] if item["review_id"] != args.review_id]
        updated = rebuild_profile(profile, records, today)
        atomic_write_json(profile_path, updated)
        print_json({"growth_profile": updated})
        return

    if args.command == "delete-profile":
        if not args.confirm_delete:
            fail("整档删除必须加 --confirm-delete")
        if profile_path.exists():
            profile_path.unlink()
        print_json({"deleted": True})
        return

    if args.command == "export":
        profile = read_profile(store_dir)
        if profile is None:
            fail("成长档案不存在")
        output = store_path(store_dir, args.output, "output")
        portable = {
            "schema_version": SCHEMA_VERSION,
            "parent_settings": settings,
            "growth_profile": profile,
        }
        if output.exists():
            fail("导出文件已存在，请先更换文件名或删除旧文件")
        atomic_write_json(output, portable)
        print_json({"output": str(output)})
        return

if __name__ == "__main__":
    main()
