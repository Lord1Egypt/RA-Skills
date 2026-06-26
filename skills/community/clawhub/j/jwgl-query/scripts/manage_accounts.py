#!/usr/bin/env python3
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Any

MASK = "******"
DEFAULT_LOGIN_PATH = "/jsxsd/framework/jsMain.jsp"
LEGACY_SCHOOL_NAME = "默认学校"
CONFIG_EXAMPLE_PATH = Path(__file__).resolve().parent.parent / "config.example.json"


def print_json(payload: dict[str, Any], exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    bootstrap_legacy_school(config)
    apply_runtime_defaults(config)
    return config


def save_config(path: Path, config: dict[str, Any]) -> None:
    apply_runtime_defaults(config)
    sync_legacy_urls(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_url(url: str | None) -> str:
    return (url or "").strip().rstrip("/")


def derive_login_url(base_url: str) -> str:
    cleaned = normalize_url(base_url)
    if not cleaned:
        return ""
    return f"{cleaned}{DEFAULT_LOGIN_PATH}"


def bootstrap_legacy_school(config: dict[str, Any]) -> None:
    schools = config.get("schools")
    if schools is not None and not isinstance(schools, dict):
        print_json(
            {
                "ok": False,
                "error_code": "INVALID_CONFIG",
                "message": "config.json 中的 schools 必须是对象",
            },
            exit_code=2,
        )
    if schools:
        return

    base_url = normalize_url(config.get("base_url"))
    login_url = normalize_url(config.get("login_url")) or derive_login_url(base_url)
    if not base_url and not login_url:
        config.setdefault("schools", {})
        return

    school_name = (config.get("current_school") or LEGACY_SCHOOL_NAME).strip() or LEGACY_SCHOOL_NAME
    config["schools"] = {
        school_name: {
            "base_url": base_url,
            "login_url": login_url,
        }
    }
    config["current_school"] = school_name


def load_default_runtime_config() -> dict[str, Any]:
    if not CONFIG_EXAMPLE_PATH.exists():
        return {}
    with CONFIG_EXAMPLE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def merge_missing_dict_values(current: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(current)
    for key, default_value in defaults.items():
        current_value = merged.get(key)
        if isinstance(current_value, dict) and isinstance(default_value, dict):
            merged[key] = merge_missing_dict_values(current_value, default_value)
        elif key not in merged:
            merged[key] = deepcopy(default_value)
    return merged


def apply_runtime_defaults(config: dict[str, Any]) -> None:
    defaults = load_default_runtime_config()
    selector_defaults = defaults.get("selectors")
    if isinstance(selector_defaults, dict):
        current_selectors = config.get("selectors")
        if not isinstance(current_selectors, dict):
            current_selectors = {}
        config["selectors"] = merge_missing_dict_values(current_selectors, selector_defaults)


def sync_legacy_urls(config: dict[str, Any]) -> None:
    schools = config.get("schools", {})
    if not isinstance(schools, dict) or not schools:
        config.pop("base_url", None)
        config.pop("login_url", None)
        return

    current_school = (config.get("current_school") or "").strip()
    if current_school not in schools:
        current_school = next(iter(schools.keys()))
        config["current_school"] = current_school

    current = schools.get(current_school, {})
    config["base_url"] = normalize_url(current.get("base_url"))
    config["login_url"] = normalize_url(current.get("login_url")) or derive_login_url(config["base_url"])


def ensure_teachers(config: dict[str, Any]) -> dict[str, Any]:
    teachers = config.setdefault("teachers", {})
    if not isinstance(teachers, dict):
        print_json(
            {
                "ok": False,
                "error_code": "INVALID_CONFIG",
                "message": "config.json 中的 teachers 必须是对象",
            },
            exit_code=2,
        )
    return teachers


def ensure_schools(config: dict[str, Any]) -> dict[str, Any]:
    bootstrap_legacy_school(config)
    schools = config.setdefault("schools", {})
    if not isinstance(schools, dict):
        print_json(
            {
                "ok": False,
                "error_code": "INVALID_CONFIG",
                "message": "config.json 中的 schools 必须是对象",
            },
            exit_code=2,
        )
    return schools


def mask_teacher(teacher: dict[str, Any]) -> dict[str, Any]:
    masked = dict(teacher)
    if masked.get("password"):
        masked["password"] = MASK
    return masked


def normalize_teacher_fields(previous: dict[str, Any] | None = None, *, username: str | None = None, password: str | None = None, email: str | None = None, phone: str | None = None) -> dict[str, Any]:
    teacher = dict(previous or {})
    if username is not None:
        teacher["username"] = username
    if password is not None:
        teacher["password"] = password
    if email is not None:
        teacher["email"] = email
    if phone is not None:
        teacher["phone"] = phone
    if not teacher.get("username") or not teacher.get("password"):
        print_json(
            {
                "ok": False,
                "error_code": "MISSING_REQUIRED_FIELDS",
                "message": "老师账号或密码为空，无法保存",
                "required": ["teacher", "username", "password"],
            },
            exit_code=2,
        )
    return teacher


def normalize_school_fields(previous: dict[str, Any] | None = None, *, base_url: str | None = None, login_url: str | None = None) -> dict[str, Any]:
    school = dict(previous or {})
    if base_url is not None:
        school["base_url"] = normalize_url(base_url)
    if login_url is not None:
        school["login_url"] = normalize_url(login_url)

    resolved_base_url = normalize_url(school.get("base_url"))
    resolved_login_url = normalize_url(school.get("login_url")) or derive_login_url(resolved_base_url)
    if not resolved_base_url:
        print_json(
            {
                "ok": False,
                "error_code": "MISSING_REQUIRED_FIELDS",
                "message": "学校 URL 为空，无法保存",
                "required": ["school", "base_url"],
            },
            exit_code=2,
        )
    school["base_url"] = resolved_base_url
    school["login_url"] = resolved_login_url
    return school


def require_teacher_name(teacher: str | None, *, action: str) -> str:
    name = (teacher or "").strip()
    if not name:
        print_json(
            {
                "ok": False,
                "error_code": "MISSING_TEACHER_NAME",
                "message": f"缺少老师名称，无法执行{action}",
                "required": ["teacher"],
                "action": action,
            },
            exit_code=2,
        )
    return name


def require_existing_teacher(teachers: dict[str, Any], teacher: str, *, action: str) -> dict[str, Any]:
    if teacher not in teachers:
        print_json(
            {
                "ok": False,
                "error_code": "TEACHER_NOT_FOUND",
                "message": f"老师 {teacher} 不存在，无法执行{action}",
                "teacher": teacher,
                "action": action,
            },
            exit_code=3,
        )
    return teachers[teacher]


def require_school_name(school: str | None, *, action: str) -> str:
    name = (school or "").strip()
    if not name:
        print_json(
            {
                "ok": False,
                "error_code": "MISSING_SCHOOL_NAME",
                "message": f"缺少学校名称，无法执行{action}",
                "required": ["school"],
                "action": action,
            },
            exit_code=2,
        )
    return name


def require_existing_school(schools: dict[str, Any], school: str, *, action: str) -> dict[str, Any]:
    if school not in schools:
        print_json(
            {
                "ok": False,
                "error_code": "SCHOOL_NOT_FOUND",
                "message": f"学校 {school} 不存在，无法执行{action}",
                "school": school,
                "action": action,
            },
            exit_code=3,
        )
    return schools[school]


def resolve_teacher_school(config: dict[str, Any], school: str | None, *, previous: dict[str, Any] | None = None) -> str:
    schools = ensure_schools(config)
    explicit_school = (school or "").strip()
    if explicit_school:
        require_existing_school(schools, explicit_school, action="bind-teacher-school")
        return explicit_school

    previous_school = (previous or {}).get("school", "").strip()
    if previous_school:
        require_existing_school(schools, previous_school, action="bind-teacher-school")
        return previous_school

    current_school = (config.get("current_school") or "").strip()
    if current_school:
        require_existing_school(schools, current_school, action="bind-teacher-school")
        return current_school

    return ""


def cmd_list(args: argparse.Namespace) -> None:
    config = load_config(Path(args.config))
    teachers = ensure_teachers(config)
    schools = ensure_schools(config)
    print_json(
        {
            "ok": True,
            "action": "list",
            "current_teacher": config.get("current_teacher"),
            "current_school": config.get("current_school"),
            "count": len(teachers),
            "school_count": len(schools),
            "teachers": {name: mask_teacher(info if isinstance(info, dict) else {}) for name, info in teachers.items()},
            "schools": schools,
        }
    )


def cmd_add(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    teachers = ensure_teachers(config)
    teacher_name = require_teacher_name(args.teacher, action="add")
    previous = teachers.get(teacher_name)
    if previous and not args.force:
        print_json(
            {
                "ok": False,
                "error_code": "TEACHER_ALREADY_EXISTS",
                "message": f"老师 {teacher_name} 已存在",
                "teacher": teacher_name,
                "action": "add",
            },
            exit_code=3,
        )
    school_name = resolve_teacher_school(config, args.school, previous=previous)
    teacher = normalize_teacher_fields(
        previous,
        username=args.username,
        password=args.password,
        email=args.email if args.email is not None else (previous or {}).get("email", ""),
        phone=args.phone if args.phone is not None else (previous or {}).get("phone", ""),
    )
    if school_name:
        teacher["school"] = school_name
    teachers[teacher_name] = teacher
    if args.set_current or not config.get("current_teacher"):
        config["current_teacher"] = teacher_name
    save_config(path, config)
    print_json({"ok": True, "action": "add", "teacher": teacher_name, "school": school_name, "set_current": config.get("current_teacher") == teacher_name})


def cmd_update(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    teachers = ensure_teachers(config)
    teacher_name = require_teacher_name(args.teacher, action="update")
    previous = require_existing_teacher(teachers, teacher_name, action="update")
    school_name = resolve_teacher_school(config, args.school, previous=previous)
    teacher = normalize_teacher_fields(
        previous,
        username=args.username if args.username is not None else previous.get("username"),
        password=args.password if args.password is not None else previous.get("password"),
        email=args.email if args.email is not None else previous.get("email", ""),
        phone=args.phone if args.phone is not None else previous.get("phone", ""),
    )
    if school_name:
        teacher["school"] = school_name
    else:
        teacher.pop("school", None)
    teachers[teacher_name] = teacher
    if args.set_current:
        config["current_teacher"] = teacher_name
    save_config(path, config)
    print_json({"ok": True, "action": "update", "teacher": teacher_name, "school": school_name, "set_current": config.get("current_teacher") == teacher_name})


def cmd_remove(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    teachers = ensure_teachers(config)
    teacher_name = require_teacher_name(args.teacher, action="remove")
    require_existing_teacher(teachers, teacher_name, action="remove")
    del teachers[teacher_name]
    if config.get("current_teacher") == teacher_name:
        config["current_teacher"] = next(iter(teachers.keys()), "")
    save_config(path, config)
    print_json({"ok": True, "action": "remove", "teacher": teacher_name, "current_teacher": config.get("current_teacher", "")})


def cmd_set_current(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    teachers = ensure_teachers(config)
    teacher_name = require_teacher_name(args.teacher, action="set-current")
    require_existing_teacher(teachers, teacher_name, action="set-current")
    config["current_teacher"] = teacher_name
    save_config(path, config)
    print_json({"ok": True, "action": "set_current", "teacher": teacher_name})


def cmd_school_list(args: argparse.Namespace) -> None:
    config = load_config(Path(args.config))
    schools = ensure_schools(config)
    print_json(
        {
            "ok": True,
            "action": "school_list",
            "current_school": config.get("current_school"),
            "count": len(schools),
            "schools": schools,
        }
    )


def cmd_school_add(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    schools = ensure_schools(config)
    school_name = require_school_name(args.school, action="school-add")
    previous = schools.get(school_name)
    if previous and not args.force:
        print_json(
            {
                "ok": False,
                "error_code": "SCHOOL_ALREADY_EXISTS",
                "message": f"学校 {school_name} 已存在",
                "school": school_name,
                "action": "school-add",
            },
            exit_code=3,
        )
    schools[school_name] = normalize_school_fields(previous, base_url=args.base_url, login_url=args.login_url)
    if args.set_current or not config.get("current_school"):
        config["current_school"] = school_name
    save_config(path, config)
    print_json({"ok": True, "action": "school_add", "school": school_name, "set_current": config.get("current_school") == school_name})


def cmd_school_update(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    schools = ensure_schools(config)
    school_name = require_school_name(args.school, action="school-update")
    previous = require_existing_school(schools, school_name, action="school-update")
    schools[school_name] = normalize_school_fields(
        previous,
        base_url=args.base_url if args.base_url is not None else previous.get("base_url"),
        login_url=args.login_url if args.login_url is not None else previous.get("login_url"),
    )
    if args.set_current:
        config["current_school"] = school_name
    save_config(path, config)
    print_json({"ok": True, "action": "school_update", "school": school_name, "set_current": config.get("current_school") == school_name})


def cmd_school_remove(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    schools = ensure_schools(config)
    teachers = ensure_teachers(config)
    school_name = require_school_name(args.school, action="school-remove")
    require_existing_school(schools, school_name, action="school-remove")

    linked_teachers = sorted(name for name, info in teachers.items() if isinstance(info, dict) and info.get("school") == school_name)
    if linked_teachers and not args.force:
        print_json(
            {
                "ok": False,
                "error_code": "SCHOOL_IN_USE",
                "message": f"学校 {school_name} 仍被老师账号引用，无法删除",
                "school": school_name,
                "teachers": linked_teachers,
                "action": "school-remove",
            },
            exit_code=3,
        )

    del schools[school_name]
    for teacher_name in linked_teachers:
        if isinstance(teachers.get(teacher_name), dict):
            teachers[teacher_name].pop("school", None)

    if config.get("current_school") == school_name:
        config["current_school"] = next(iter(schools.keys()), "")

    save_config(path, config)
    print_json(
        {
            "ok": True,
            "action": "school_remove",
            "school": school_name,
            "current_school": config.get("current_school", ""),
            "detached_teachers": linked_teachers,
        }
    )


def cmd_school_set_current(args: argparse.Namespace) -> None:
    path = Path(args.config)
    config = load_config(path)
    schools = ensure_schools(config)
    school_name = require_school_name(args.school, action="school-set-current")
    require_existing_school(schools, school_name, action="school-set-current")
    config["current_school"] = school_name
    save_config(path, config)
    print_json({"ok": True, "action": "school_set_current", "school": school_name})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理 jwgl-query 的老师账号与学校 URL 配置（执行接口）")
    parser.add_argument("--config", default="config.json")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_list = subparsers.add_parser("list", help="列出已保存的老师账号")
    p_list.set_defaults(func=cmd_list)

    def add_common_fields(p: argparse.ArgumentParser, require_teacher: bool = False) -> None:
        p.add_argument("--teacher", "--name", dest="teacher", required=require_teacher, help="老师名称（兼容旧写法：--name）")
        p.add_argument("--username", "--user", "--account", dest="username", help="登录账号（兼容旧写法：--user/--account）")
        p.add_argument("--password", "--pass", dest="password", help="登录密码（兼容旧写法：--pass）")
        p.add_argument("--email", help="邮箱（可选）")
        p.add_argument("--phone", help="手机号（可选）")
        p.add_argument("--school", help="所属学校名称（可选；默认沿用当前学校）")
        p.add_argument("--set-current", action="store_true", help="保存后设为当前老师")

    p_add = subparsers.add_parser("add", help="新增老师账号")
    add_common_fields(p_add)
    p_add.add_argument("--force", action="store_true", help="老师已存在时允许覆盖")
    p_add.set_defaults(func=cmd_add)

    p_update = subparsers.add_parser("update", help="更新老师账号")
    add_common_fields(p_update)
    p_update.set_defaults(func=cmd_update)

    p_remove = subparsers.add_parser("remove", help="删除老师账号")
    p_remove.add_argument("--teacher", "--name", dest="teacher", required=False, help="老师名称（兼容旧写法：--name）")
    p_remove.set_defaults(func=cmd_remove)

    p_set = subparsers.add_parser("set-current", help="设置当前老师")
    p_set.add_argument("--teacher", "--name", dest="teacher", required=False, help="老师名称（兼容旧写法：--name）")
    p_set.set_defaults(func=cmd_set_current)

    def add_school_fields(p: argparse.ArgumentParser) -> None:
        p.add_argument("--school", "--name", dest="school", required=False, help="学校名称（兼容旧写法：--name）")
        p.add_argument("--base-url", help="学校教务系统基础 URL，例如 https://jwgl.example.edu.cn")
        p.add_argument("--login-url", help="登录页 URL；不传时默认使用 /jsxsd/framework/jsMain.jsp")
        p.add_argument("--set-current", action="store_true", help="保存后设为当前学校")

    p_school_list = subparsers.add_parser("school-list", help="列出已保存的学校 URL")
    p_school_list.set_defaults(func=cmd_school_list)

    p_school_add = subparsers.add_parser("school-add", help="新增学校 URL")
    add_school_fields(p_school_add)
    p_school_add.add_argument("--force", action="store_true", help="学校已存在时允许覆盖")
    p_school_add.set_defaults(func=cmd_school_add)

    p_school_update = subparsers.add_parser("school-update", help="更新学校 URL")
    add_school_fields(p_school_update)
    p_school_update.set_defaults(func=cmd_school_update)

    p_school_remove = subparsers.add_parser("school-remove", help="删除学校 URL")
    p_school_remove.add_argument("--school", "--name", dest="school", required=False, help="学校名称（兼容旧写法：--name）")
    p_school_remove.add_argument("--force", action="store_true", help="若有老师绑定该学校，则解绑后继续删除")
    p_school_remove.set_defaults(func=cmd_school_remove)

    p_school_set = subparsers.add_parser("school-set-current", help="设置当前学校")
    p_school_set.add_argument("--school", "--name", dest="school", required=False, help="学校名称（兼容旧写法：--name）")
    p_school_set.set_defaults(func=cmd_school_set_current)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
