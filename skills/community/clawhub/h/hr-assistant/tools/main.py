#!/usr/bin/env python3
"""
HR 智能体 - 统一入口脚本
供 WorkBuddy SKILL.md 调用

用法:
    # 自然语言模式（默认）
    python3 main.py "<自然语言指令>"
    python3 main.py "帮助"
    python3 main.py "查看配置"
    python3 main.py "计算本月薪资"

    # 子命令模式（精确操作）
    python3 main.py bind <table_type> <file_path> [sheet_name]
    python3 main.py analyze <file_path> [sheet_name]
    python3 main.py status
"""

import sys
import os
import json

# 确保可以导入同目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def cmd_bind(args):
    """绑定表格：分析 Excel + 自动列映射 + 完成绑定"""
    if len(args) < 2:
        print(json.dumps({
            "success": False,
            "message": "用法: python3 main.py bind <table_type> <file_path> [sheet_name]\n"
                       "table_type: organization / employee / salary"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    table_type = args[0]
    file_path = os.path.abspath(args[1])
    sheet_name = args[2] if len(args) > 2 else None

    if table_type not in ("organization", "employee", "salary"):
        print(json.dumps({
            "success": False,
            "message": f"无效的表格类型: {table_type}，请使用 organization / employee / salary"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        from onboarding import analyze_and_bind
        result = analyze_and_bind(table_type, file_path, sheet_name)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": f"绑定失败: {e}"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


def cmd_analyze(args):
    """分析 Excel 文件结构"""
    if len(args) < 1:
        print(json.dumps({
            "success": False,
            "message": "用法: python3 main.py analyze <file_path> [sheet_name]"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    file_path = os.path.abspath(args[0])
    sheet_name = args[1] if len(args) > 1 else None

    try:
        from excel_adapter import analyze_excel_structure
        result = analyze_excel_structure(file_path, sheet_name)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": f"分析失败: {e}"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


def cmd_status():
    """查看当前配置状态"""
    try:
        from onboarding import get_configuration_summary
        result = get_configuration_summary()
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": f"获取状态失败: {e}"
        }, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "message": "用法: python3 main.py \"<指令>\" | python3 main.py bind <type> <file> | python3 main.py status"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 子命令模式
    subcmd = sys.argv[1].lower()

    if subcmd == "bind":
        cmd_bind(sys.argv[2:])
        return
    elif subcmd == "analyze":
        cmd_analyze(sys.argv[2:])
        return
    elif subcmd == "status":
        cmd_status()
        return

    # 默认：自然语言模式
    user_input = " ".join(sys.argv[1:])

    try:
        from intent_router import process_user_input
        result = process_user_input(user_input)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except ImportError as e:
        print(json.dumps({
            "success": False,
            "message": f"模块导入失败: {e}\n请确保 tools/ 目录下所有 .py 文件完整"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "message": f"处理出错: {e}"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
