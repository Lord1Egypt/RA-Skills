#!/usr/bin/env python3
"""
macOS 系统通知封装。

支持：
- 纯提醒通知（T-5min）
- 交互式通知（T-0min，带按钮）
- 确认对话框（自动停止提示）

依赖：
- terminal-notifier: brew install terminal-notifier
"""

import subprocess
import sys
from pathlib import Path


def _has_terminal_notifier():
    return subprocess.run(
        ["which", "terminal-notifier"],
        capture_output=True,
    ).returncode == 0


def _fallback_notify(title, message, subtitle=""):
    """fallback 到 osascript display notification。"""
    script = f'display notification "{message}" with title "{title}"'
    if subtitle:
        script += f' subtitle "{subtitle}"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def _fallback_dialog(message, buttons, default_button, timeout=60):
    """fallback 到 osascript display dialog。"""
    btn_str = ",".join(f'"{b}"' for b in buttons)
    script = (
        f'display dialog "{message}" '
        f'buttons {{{btn_str}}} '
        f'default button "{default_button}" '
        f'giving up after {timeout}'
    )
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    # 解析返回: button returned:xxx, gave up:false
    for line in result.stdout.split(","):
        if "button returned:" in line:
            return line.split(":")[1].strip()
        if "gave up:true" in line:
            return "timeout"
    return ""


def remind(title, message, subtitle=""):
    """发送纯提醒通知（会议前5分钟）。"""
    if _has_terminal_notifier():
        cmd = [
            "terminal-notifier",
            "-title", title,
            "-message", message,
            "-sound", "Glass",
        ]
        if subtitle:
            cmd += ["-subtitle", subtitle]
        subprocess.run(cmd, capture_output=True)
    else:
        _fallback_notify(title, message, subtitle)


def ask_record(meeting_title, timeout=60):
    """
    会议开始时询问是否录制。
    使用 osascript display dialog（真正的弹窗，按钮清晰可见）。
    返回: "开始录制" | "忽略" | "timeout"
    """
    return _fallback_dialog(
        f"会议「{meeting_title}」开始了\n\n是否开始录制音频？",
        buttons=["忽略", "开始录制"],
        default_button="开始录制",
        timeout=timeout,
    )


def ask_stop(meeting_title, timeout=60):
    """
    检测到静默时询问是否停止录制。
    使用 osascript display dialog（真正的弹窗，按钮清晰可见）。
    返回: "停止" | "继续" | "timeout"
    """
    return _fallback_dialog(
        f"会议「{meeting_title}」\n已连续 5 分钟无声音\n\n是否停止录制？",
        buttons=["继续录制", "停止录制"],
        default_button="停止录制",
        timeout=timeout,
    )


def notify_stop_auto(meeting_title):
    """自动停止录制后的通知。"""
    message = f"会议「{meeting_title}」\n已自动停止录制，正在生成纪要..."
    remind("Meeting Assistant", message, subtitle="自动停止")


def notify_summary_sent(meeting_title, channel):
    """纪要发送后的通知。"""
    message = f"会议「{meeting_title}」\n纪要已发送到 {channel}"
    remind("Meeting Assistant", message, subtitle="纪要完成")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: notify.py <remind|ask_record|ask_stop|notify_stop|notify_sent> ...")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == "remind":
        remind(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif action == "ask_record":
        print(ask_record(sys.argv[2]))
    elif action == "ask_stop":
        print(ask_stop(sys.argv[2]))
    elif action == "notify_stop":
        notify_stop_auto(sys.argv[2])
    elif action == "notify_sent":
        notify_summary_sent(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown action: {action}")
