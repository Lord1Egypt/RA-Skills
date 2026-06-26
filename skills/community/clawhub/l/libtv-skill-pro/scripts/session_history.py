#!/usr/bin/env python3
"""
会话历史管理脚本 - 管理和查看会话历史
"""

import argparse
import json
import sys
import os
from datetime import datetime


HISTORY_FILE = os.path.expanduser("~/.libtv_session_history.json")


def load_history() -> dict:
    """加载历史记录"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sessions": [], "last_accessed": None}


def save_history(data: dict):
    """保存历史记录"""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_session(session_id: str, project_id: str = "", description: str = ""):
    """添加会话到历史"""
    data = load_history()
    
    # 检查是否已存在
    for s in data["sessions"]:
        if s["session_id"] == session_id:
            s["last_accessed"] = datetime.now().isoformat()
            s["access_count"] = s.get("access_count", 0) + 1
            save_history(data)
            print(f"[*] 更新会话记录: {session_id[:30]}...")
            return
    
    # 添加新记录
    session = {
        "session_id": session_id,
        "project_id": project_id,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "last_accessed": datetime.now().isoformat(),
        "access_count": 1,
    }
    data["sessions"].append(session)
    save_history(data)
    print(f"[*] 添加会话记录: {session_id[:30]}...")


def list_sessions():
    """列出所有会话"""
    data = load_history()
    sessions = data.get("sessions", [])
    
    if not sessions:
        print("暂无会话记录")
        return
    
    # 按最后访问时间排序
    sessions.sort(key=lambda x: x.get("last_accessed", ""), reverse=True)
    
    print(f"{'#':<4} {'会话 ID':<40} {'项目 ID':<40} {'描述':<20} {'访问次数':<8} {'最后访问'}")
    print("-" * 130)
    
    for i, s in enumerate(sessions, 1):
        sid = s.get("session_id", "N/A")[:38]
        pid = s.get("project_id", "N/A")[:38]
        desc = s.get("description", "")[:18]
        count = s.get("access_count", 0)
        last = s.get("last_accessed", "")[:16]
        print(f"{i:<4} {sid:<40} {pid:<40} {desc:<20} {count:<8} {last}")


def show_session_detail(index: int):
    """显示会话详情"""
    data = load_history()
    sessions = data.get("sessions", [])
    
    if index < 1 or index > len(sessions):
        print(f"错误：无效的序号 {index}", file=sys.stderr)
        sys.exit(1)
    
    session = sessions[index - 1]
    print(f"会话详情 [{index}]:")
    print("-" * 60)
    print(f"会话 ID:    {session.get('session_id', 'N/A')}")
    print(f"项目 ID:    {session.get('project_id', 'N/A')}")
    print(f"描述:       {session.get('description', 'N/A')}")
    print(f"创建时间:   {session.get('created_at', 'N/A')}")
    print(f"最后访问:   {session.get('last_accessed', 'N/A')}")
    print(f"访问次数:   {session.get('access_count', 0)}")


def remove_session(index: int = None, session_id: str = None):
    """删除会话记录"""
    data = load_history()
    sessions = data.get("sessions", [])
    
    if index is not None:
        if index < 1 or index > len(sessions):
            print(f"错误：无效的序号 {index}", file=sys.stderr)
            sys.exit(1)
        removed = sessions.pop(index - 1)
        print(f"[*] 删除会话: {removed.get('session_id', 'N/A')[:30]}...")
    elif session_id:
        data["sessions"] = [s for s in sessions if s["session_id"] != session_id]
        print(f"[*] 删除会话: {session_id[:30]}...")
    
    save_history(data)


def clear_history():
    """清空历史"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("[*] 历史记录已清空")
    else:
        print("[*] 历史记录为空")


def get_session_by_index(index: int) -> dict:
    """通过序号获取会话"""
    data = load_history()
    sessions = data.get("sessions", [])
    
    if index < 1 or index > len(sessions):
        return None
    
    return sessions[index - 1]


def main():
    parser = argparse.ArgumentParser(
        description="会话历史管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  可选

示例:
  # 列出所有会话
  python3 session_history.py list

  # 添加会话记录
  python3 session_history.py add <session_id> --project-id <pid> --desc "描述"

  # 查看会话详情
  python3 session_history.py show <index>

  # 获取会话 ID（用于脚本）
  python3 session_history.py get <index>

  # 删除会话记录
  python3 session_history.py remove <index>

  # 清空历史
  python3 session_history.py clear
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # list
    subparsers.add_parser("list", help="列出所有会话")
    
    # add
    add_parser = subparsers.add_parser("add", help="添加会话")
    add_parser.add_argument("session_id", help="会话 ID")
    add_parser.add_argument("--project-id", default="", help="项目 ID")
    add_parser.add_argument("--desc", default="", help="描述")
    
    # show
    show_parser = subparsers.add_parser("show", help="显示会话详情")
    show_parser.add_argument("index", type=int, help="会话序号")
    
    # get
    get_parser = subparsers.add_parser("get", help="获取会话 ID（用于脚本）")
    get_parser.add_argument("index", type=int, help="会话序号")
    
    # remove
    remove_parser = subparsers.add_parser("remove", help="删除会话")
    remove_parser.add_argument("index", type=int, help="会话序号")
    
    # clear
    subparsers.add_parser("clear", help="清空历史")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "list":
        list_sessions()
    elif args.command == "add":
        add_session(args.session_id, args.project_id, args.desc)
    elif args.command == "show":
        show_session_detail(args.index)
    elif args.command == "get":
        session = get_session_by_index(args.index)
        if session:
            print(session.get("session_id", ""))
        else:
            sys.exit(1)
    elif args.command == "remove":
        remove_session(index=args.index)
    elif args.command == "clear":
        clear_history()


if __name__ == "__main__":
    main()
