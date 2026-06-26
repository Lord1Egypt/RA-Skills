#!/usr/bin/env python3
"""项目管理：列出/切换/查看本地项目，及调用服务端 change-project API"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import (
    change_project,
    build_project_url,
    load_projects,
    save_projects,
    record_project,
    safe_run,
    APIError,
)


def cmd_list() -> None:
    data = load_projects()
    projects = data.get("projects", {})
    current = data.get("current", "")

    if not projects:
        print("暂无本地项目记录（先用 switch/use/create_session 触发一次记录）")
        return

    items = sorted(
        projects.items(),
        key=lambda kv: kv[1].get("lastUsedAt", ""),
        reverse=True,
    )

    print(f"{'当前':<4} {'项目 UUID':<36} {'描述':<20} {'最后使用'}")
    print("-" * 90)
    for uuid, info in items:
        mark = "*" if uuid == current else ""
        desc = (info.get("desc") or "")[:18]
        last = (info.get("lastUsedAt") or "")[:19]
        print(f"{mark:<4} {uuid:<36} {desc:<20} {last}")


def cmd_current() -> None:
    data = load_projects()
    current = data.get("current", "")
    if not current:
        print(json.dumps({"current": "", "projectUrl": ""}, ensure_ascii=False, indent=2))
        return
    info = data.get("projects", {}).get(current, {})
    out = {
        "current": current,
        "projectUrl": build_project_url(current),
        "desc": info.get("desc", ""),
        "lastUsedAt": info.get("lastUsedAt", ""),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_switch(desc: str = "") -> None:
    """调用 API 创建新项目并切换。"""
    data = change_project()
    project_uuid = data.get("projectUuid", "")
    if not project_uuid:
        print("错误：未返回 projectUuid", file=sys.stderr)
        sys.exit(1)
    record_project(project_uuid, set_current=True, desc=desc)
    out = {
        "projectUuid": project_uuid,
        "projectUrl": build_project_url(project_uuid),
        "action": "switched_new",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_use(project_uuid: str, desc: str = "") -> None:
    """尝试通过 API 切换到指定项目；若服务端不接受参数则仅本地标记。"""
    if not project_uuid:
        print("错误：缺少 projectUuid", file=sys.stderr)
        sys.exit(1)
    try:
        data = change_project(project_uuid=project_uuid)
        returned = data.get("projectUuid", "") or project_uuid
        record_project(returned, set_current=True, desc=desc)
        action = "switched_existing" if returned == project_uuid else "switched_new"
        out = {
            "projectUuid": returned,
            "projectUrl": build_project_url(returned),
            "action": action,
        }
        if action == "switched_new":
            out["note"] = "服务端忽略了 projectUuid 参数并返回了新项目"
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except APIError as e:
        record_project(project_uuid, set_current=True, desc=desc)
        out = {
            "projectUuid": project_uuid,
            "projectUrl": build_project_url(project_uuid),
            "action": "marked_local_only",
            "note": f"服务端 change-project 失败（{e.kind}），仅在本地记录为当前项目",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_remove(project_uuid: str) -> None:
    if not project_uuid:
        print("错误：缺少 projectUuid", file=sys.stderr)
        sys.exit(1)
    data = load_projects()
    projects = data.get("projects", {})
    if project_uuid not in projects:
        print(f"未找到本地记录：{project_uuid}", file=sys.stderr)
        sys.exit(1)
    del projects[project_uuid]
    if data.get("current") == project_uuid:
        data["current"] = ""
    save_projects(data)
    print(json.dumps({"removed": project_uuid}, ensure_ascii=False, indent=2))


def cmd_describe(project_uuid: str, desc: str) -> None:
    data = load_projects()
    projects = data.get("projects", {})
    if project_uuid not in projects:
        record_project(project_uuid, set_current=False, desc=desc)
    else:
        projects[project_uuid]["desc"] = desc
        save_projects(data)
    print(json.dumps({"projectUuid": project_uuid, "desc": desc}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="项目管理：列出/切换/记录本地项目，并桥接服务端 change-project API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权

示例:
  # 列出本地记录的所有项目
  python3 manage_project.py list

  # 显示当前项目
  python3 manage_project.py current

  # 调 API 创建新项目并切换
  python3 manage_project.py switch --desc "短剧 A"

  # 调 API 切换到指定项目（服务端支持时）
  python3 manage_project.py use PROJECT_UUID

  # 给项目加备注
  python3 manage_project.py describe PROJECT_UUID "MV 项目"

  # 删除本地记录
  python3 manage_project.py remove PROJECT_UUID

数据存储：~/.libtv_projects.json
        """,
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="列出本地项目记录")
    sub.add_parser("current", help="显示当前项目")

    p_switch = sub.add_parser("switch", help="调 API 创建新项目并切换")
    p_switch.add_argument("--desc", default="", help="项目备注")

    p_use = sub.add_parser("use", help="切换到指定项目")
    p_use.add_argument("project_uuid", help="目标 projectUuid")
    p_use.add_argument("--desc", default="", help="项目备注")

    p_remove = sub.add_parser("remove", help="删除本地项目记录")
    p_remove.add_argument("project_uuid", help="目标 projectUuid")

    p_describe = sub.add_parser("describe", help="给项目添加/更新备注")
    p_describe.add_argument("project_uuid", help="目标 projectUuid")
    p_describe.add_argument("desc", help="备注内容")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        cmd_list()
    elif args.command == "current":
        cmd_current()
    elif args.command == "switch":
        cmd_switch(desc=args.desc)
    elif args.command == "use":
        cmd_use(project_uuid=args.project_uuid, desc=args.desc)
    elif args.command == "remove":
        cmd_remove(project_uuid=args.project_uuid)
    elif args.command == "describe":
        cmd_describe(project_uuid=args.project_uuid, desc=args.desc)


if __name__ == "__main__":
    safe_run(main)
