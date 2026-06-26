"""
PC Controller - 电脑控制统一入口
提供命令行接口用于控制电脑的各种功能
包括截图、剪贴板、键盘、鼠标、进程、窗口、系统、文件、Shell 命令执行等
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath("pc.py")))
import json
import argparse
from typing import Any, Dict

from modules.screenshot import take_screenshot, get_screen_info
from modules.clipboard import clipboard_read, clipboard_write
from modules.keyboard import key_press, key_type, key_hotkey, key_down, key_up
from modules.mouse import mouse_move, mouse_click, mouse_double_click, mouse_right_click, mouse_drag, mouse_scroll, get_mouse_position
from modules.process import process_list, process_kill, process_get
from modules.window import window_list, window_minimize, window_maximize, window_close, window_focus
from modules.system import get_system_info, get_displays
from modules.file import file_read, file_write, file_list, file_exists
from modules.shell import shell_run, shell_run_file, get_shell_info


def make_response(success: bool, data: Any = None, error: str = None) -> Dict:
    return {
        "success": success,
        "data": data,
        "error": error
    }


def main():
    parser = argparse.ArgumentParser(prog="pc", description="PC Controller - 电脑控制统一入口")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    ss_parser = subparsers.add_parser("screenshot", help="截取屏幕截图")
    ss_parser.add_argument("--path", "-p", default="screenshot.png", help="保存路径")

    subparsers.add_parser("screen-info", help="获取屏幕信息")

    cb_parser = subparsers.add_parser("clipboard", help="剪贴板操作")
    cb_parser.add_argument("action", choices=["read", "write"], help="操作类型")
    cb_parser.add_argument("--text", "-t", help="写入的文本")

    key_parser = subparsers.add_parser("key", help="键盘操作")
    key_parser.add_argument("action", choices=["press", "type", "hotkey", "down", "up"], help="操作类型")
    key_parser.add_argument("key", nargs="?", help="按键名称")
    key_parser.add_argument("--text", "-t", help="输入的文本")
    key_parser.add_argument("--keys", "-k", nargs="+", help="快捷键组合")

    mouse_parser = subparsers.add_parser("mouse", help="鼠标操作")
    mouse_parser.add_argument("action", choices=["move", "click", "double", "right", "drag", "scroll", "position"], help="操作类型")
    mouse_parser.add_argument("x", nargs="?", type=int, help="X坐标")
    mouse_parser.add_argument("y", nargs="?", type=int, help="Y坐标")
    mouse_parser.add_argument("--clicks", "-c", type=int, default=1, help="点击次数")
    mouse_parser.add_argument("--duration", "-d", type=float, default=0, help="移动持续时间")

    proc_parser = subparsers.add_parser("process", help="进程管理")
    proc_parser.add_argument("action", choices=["list", "kill", "get"], help="操作类型")
    proc_parser.add_argument("name", nargs="?", help="进程名")

    win_parser = subparsers.add_parser("window", help="窗口管理")
    win_parser.add_argument("action", choices=["list", "minimize", "maximize", "close", "focus"], help="操作类型")
    win_parser.add_argument("name", nargs="?", help="窗口标题")

    sys_parser = subparsers.add_parser("system", help="系统信息")
    sys_parser.add_argument("action", choices=["info", "displays"], help="操作类型")

    file_parser = subparsers.add_parser("file", help="文件操作")
    file_parser.add_argument("action", choices=["read", "write", "list", "exists"], help="操作类型")
    file_parser.add_argument("path", help="文件路径")
    file_parser.add_argument("--content", "-c", help="写入的内容")

    shell_parser = subparsers.add_parser("shell", help="Shell 命令执行")
    shell_parser.add_argument("action", choices=["run", "run-file", "info"], help="操作类型")
    shell_parser.add_argument("command", nargs="?", help="要执行的命令(用于run)")
    shell_parser.add_argument("script", nargs="?", help="脚本文件路径(用于run-file)")
    shell_parser.add_argument("--shell", "-s", default="powershell", choices=["powershell", "cmd", "pwsh"], help="Shell类型")
    shell_parser.add_argument("--timeout", "-t", type=int, default=30, help="超时时间(秒)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print(json.dumps(make_response(False, error="未指定命令"), ensure_ascii=False))
        sys.exit(1)

    try:
        if args.command == "screenshot":
            result = take_screenshot(args.path)
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "screen-info":
            result = get_screen_info()
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "clipboard":
            if args.action == "read":
                result = clipboard_read()
            else:
                if not args.text:
                    print(json.dumps(make_response(False, error="缺少文本内容"), ensure_ascii=False))
                    sys.exit(1)
                result = clipboard_write(args.text)
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "key":
            if args.action == "press":
                if not args.key:
                    print(json.dumps(make_response(False, error="缺少按键名称"), ensure_ascii=False))
                    sys.exit(1)
                result = key_press(args.key)
            elif args.action == "type":
                if not args.text:
                    print(json.dumps(make_response(False, error="缺少文本内容"), ensure_ascii=False))
                    sys.exit(1)
                result = key_type(args.text)
            elif args.action == "hotkey":
                if not args.keys:
                    print(json.dumps(make_response(False, error="缺少快捷键"), ensure_ascii=False))
                    sys.exit(1)
                result = key_hotkey(args.keys)
            elif args.action == "down":
                if not args.key:
                    print(json.dumps(make_response(False, error="缺少按键名称"), ensure_ascii=False))
                    sys.exit(1)
                result = key_down(args.key)
            elif args.action == "up":
                if not args.key:
                    print(json.dumps(make_response(False, error="缺少按键名称"), ensure_ascii=False))
                    sys.exit(1)
                result = key_up(args.key)
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "mouse":
            if args.action == "move":
                if args.x is None or args.y is None:
                    print(json.dumps(make_response(False, error="缺少坐标"), ensure_ascii=False))
                    sys.exit(1)
                result = mouse_move(args.x, args.y, args.duration)
            elif args.action == "click":
                result = mouse_click(args.x, args.y, args.clicks)
            elif args.action == "double":
                result = mouse_double_click(args.x, args.y)
            elif args.action == "right":
                result = mouse_right_click(args.x, args.y)
            elif args.action == "drag":
                if args.x is None or args.y is None:
                    print(json.dumps(make_response(False, error="缺少坐标"), ensure_ascii=False))
                    sys.exit(1)
                result = mouse_drag(args.x, args.y, args.duration)
            elif args.action == "scroll":
                if args.x is None:
                    args.x = -1
                if args.y is None:
                    args.y = -1
                result = mouse_scroll(args.x, args.y, args.clicks if hasattr(args, 'clicks') else 1)
            elif args.action == "position":
                result = get_mouse_position()
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "process":
            if args.action == "list":
                result = process_list()
            elif args.action == "kill":
                if not args.name:
                    print(json.dumps(make_response(False, error="缺少进程名"), ensure_ascii=False))
                    sys.exit(1)
                result = process_kill(args.name)
            elif args.action == "get":
                if not args.name:
                    print(json.dumps(make_response(False, error="缺少进程名"), ensure_ascii=False))
                    sys.exit(1)
                result = process_get(args.name)
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "window":
            if args.action == "list":
                result = window_list()
            elif args.action == "minimize":
                if not args.name:
                    print(json.dumps(make_response(False, error="缺少窗口标题"), ensure_ascii=False))
                    sys.exit(1)
                result = window_minimize(args.name)
            elif args.action == "maximize":
                if not args.name:
                    print(json.dumps(make_response(False, error="缺少窗口标题"), ensure_ascii=False))
                    sys.exit(1)
                result = window_maximize(args.name)
            elif args.action == "close":
                if not args.name:
                    print(json.dumps(make_response(False, error="缺少窗口标题"), ensure_ascii=False))
                    sys.exit(1)
                result = window_close(args.name)
            elif args.action == "focus":
                if not args.name:
                    print(json.dumps(make_response(False, error="缺少窗口标题"), ensure_ascii=False))
                    sys.exit(1)
                result = window_focus(args.name)
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "system":
            if args.action == "info":
                result = get_system_info()
            elif args.action == "displays":
                result = get_displays()
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "file":
            if args.action == "read":
                result = file_read(args.path)
            elif args.action == "write":
                if not args.content:
                    print(json.dumps(make_response(False, error="缺少内容"), ensure_ascii=False))
                    sys.exit(1)
                result = file_write(args.path, args.content)
            elif args.action == "list":
                result = file_list(args.path)
            elif args.action == "exists":
                result = file_exists(args.path)
            print(json.dumps(result, ensure_ascii=False))

        elif args.command == "shell":
            if args.action == "run":
                if not args.command:
                    print(json.dumps(make_response(False, error="缺少命令"), ensure_ascii=False))
                    sys.exit(1)
                result = shell_run(args.command, args.shell, args.timeout)
            elif args.action == "run-file":
                if not args.script:
                    print(json.dumps(make_response(False, error="缺少脚本路径"), ensure_ascii=False))
                    sys.exit(1)
                result = shell_run_file(args.script, args.shell, args.timeout)
            elif args.action == "info":
                result = get_shell_info()
            print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        print(json.dumps(make_response(False, error=str(e)), ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
