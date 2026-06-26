#!/usr/bin/env python3
"""macOS WeChat 文件/消息自动发送工具

依赖:
  - macOS 系统 (AppleScript)
  - cliclick (brew install cliclick)
  - WeChat 桌面版已登录

用法:
  python3 wechat_sender.py --contact "老婆" --file /path/to/video.mp4
  python3 wechat_sender.py --contact "老婆" --message "你好"
  python3 wechat_sender.py --contact "群名" --message "大家好" --group
"""

import argparse
import os
import subprocess
import sys
import time


def _run_osascript(script: str) -> tuple[int, str]:
    """执行 AppleScript, 返回 (returncode, output)"""
    p = subprocess.run(["osascript", "-e", script],
                       capture_output=True, text=True, timeout=30)
    return p.returncode, p.stdout.strip()


def _cliclick(coord: str):
    """执行 cliclick 点击"""
    subprocess.run(["cliclick", coord], capture_output=True, timeout=10)


def ensure_wechat_active() -> bool:
    """确保微信在前台运行, 返回是否成功"""
    rc, _ = _run_osascript('''
        tell application "System Events"
            set wechatRunning to exists (process "WeChat")
        end tell
        return wechatRunning
    ''')
    if rc != 0:
        # 尝试打开微信
        subprocess.run(["open", "-a", "WeChat"], capture_output=True, timeout=30)
        time.sleep(3)
        return True
    return True


def search_contact(contact: str):
    """搜索并打开联系人聊天窗口"""
    script = f'''
    tell application "System Events"
        tell process "WeChat"
            set frontmost to true
        end tell
    end tell
    delay 0.3
    tell application "System Events"
        tell process "WeChat"
            keystroke "f" using {{command down, shift down}}
        end tell
    end tell
    delay 0.5
    tell application "System Events"
        keystroke "{contact}"
    end tell
    delay 0.8
    tell application "System Events"
        keystroke return
    end tell
    delay 1
    '''
    _run_osascript(script)


def send_file(file_path: str, contact: str = "老婆"):
    """发送文件到指定微信联系人"""
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        print(f"❌ 文件不存在: {abs_path}")
        return False

    print(f"📤 发送文件到 [{contact}]: {abs_path}")

    # 1. 激活微信
    ensure_wechat_active()
    time.sleep(0.5)

    # 2. Finder 选中文件并复制
    apple_script = f'''
    tell application "Finder"
        set theFile to POSIX file "{abs_path}" as alias
        select theFile
        activate
    end tell
    delay 0.3
    tell application "System Events"
        keystroke "c" using {{command down}}
    end tell
    '''
    _run_osascript(apple_script)
    time.sleep(0.5)

    # 3. 搜索联系人并打开聊天
    search_contact(contact)

    # 4. 点击输入框区域
    _cliclick("c:600,750")
    time.sleep(0.5)

    # 5. 粘贴文件
    _run_osascript('tell application "System Events" to keystroke "v" using {command down}')
    time.sleep(3)

    # 6. 发送
    _run_osascript('tell application "System Events" to keystroke return')
    time.sleep(3)

    print("✅ 发送完成")
    return True


def send_message(message: str, contact: str = "老婆"):
    """发送文字消息到指定微信联系人"""
    print(f"💬 发送消息到 [{contact}]: {message}")

    ensure_wechat_active()
    time.sleep(0.5)
    search_contact(contact)
    time.sleep(0.5)

    # AppleScript 直接输入文本 (处理中文)
    escaped_msg = message.replace('"', '\\"')
    script = f'''
    tell application "System Events"
        tell process "WeChat"
            set frontmost to true
        end tell
    end tell
    delay 0.3
    tell application "System Events"
        keystroke "{escaped_msg}"
    end tell
    delay 0.3
    tell application "System Events"
        keystroke return
    end tell
    '''
    _run_osascript(script)
    time.sleep(2)
    print("✅ 消息已发送")
    return True


def main():
    parser = argparse.ArgumentParser(description="macOS WeChat 自动发送工具")
    parser.add_argument("--contact", default="老婆", help="联系人名称 (默认: 老婆)")
    parser.add_argument("--file", help="要发送的文件路径")
    parser.add_argument("--message", help="要发送的文字消息")
    parser.add_argument("--group", action="store_true", help="发送到群聊")

    args = parser.parse_args()

    if not args.file and not args.message:
        parser.print_help()
        print("\n⚠ 请提供 --file 或 --message")
        return 1

    if args.file:
        send_file(args.file, args.contact)
    if args.message:
        send_message(args.message, args.contact)

    return 0


if __name__ == "__main__":
    sys.exit(main())
