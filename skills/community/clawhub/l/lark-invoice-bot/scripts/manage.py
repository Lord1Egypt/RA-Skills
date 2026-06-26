#!/usr/bin/env python3
"""
飞书发票报销机器人管理脚本

用法：
  python manage.py start          # 启动机器人
  python manage.py stop           # 停止机器人
  python manage.py restart        # 重启机器人
  python manage.py status         # 检查运行状态
  python manage.py logs [-n N]    # 查看最近 N 行日志
  python manage.py config [key]   # 查看/修改配置
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

# ── 路径配置（优先使用环境变量 BOT_DIR） ──
_DEFAULT_BOT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "invoice-approval-bot"
BOT_DIR = Path(os.environ.get("BOT_DIR", str(_DEFAULT_BOT_DIR)))
PID_FILE = BOT_DIR / ".invoice_bot.pid"
LOG_FILE = BOT_DIR / "invoice_bot.log"
TMUX_SESSION = "invoice-bot"
ORCHESTRATOR = "invoice_orchestrator.py"
ENV_FILE = BOT_DIR / ".env"


def _ensure_tmux():
    """检查 tmux 是否可用，不可用时尝试安装"""
    if subprocess.run(["which", "tmux"], capture_output=True).returncode == 0:
        return True
    print("⏳ tmux 未安装，正在尝试安装...")
    result = subprocess.run(
        ["brew", "install", "tmux"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print("✅ tmux 安装成功")
        return True
    else:
        print(f"❌ tmux 安装失败: {result.stderr}")
        return False


def cmd_start():
    """在 tmux 中后台启动机器人"""
    if not _ensure_tmux():
        return

    # 先检查是否已经在运行
    is_running = check_running()
    if is_running:
        print(f"✅ 机器人已在运行 (PID: {get_pid() or 'unknown'})")
        return

    # 在 tmux 中启动
    cmd = (
        f"cd {BOT_DIR} && "
        f"python3 {ORCHESTRATOR} >> {LOG_FILE} 2>&1"
    )
    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", TMUX_SESSION, cmd],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        print(f"❌ 启动失败: {result.stderr}")
        return

    # 等待进程启动
    time.sleep(3)

    pid = get_pid()
    if pid:
        with open(PID_FILE, "w") as f:
            f.write(str(pid))
        print(f"✅ 机器人已启动 (tmux session: {TMUX_SESSION}, PID: {pid})")
    else:
        print("⚠️ tmux 已创建，但未能获取进程 PID（可能正在初始化）")


def cmd_stop():
    """停止机器人"""
    if not check_running():
        print("⚠️ 机器人未在运行")
        _cleanup_pid()
        return

    # 先尝试优雅关闭
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"📤 发送 SIGTERM 信号给进程 {pid}...")
            time.sleep(2)
        except ProcessLookupError:
            pass

    # 强制关闭 tmux session
    subprocess.run(
        ["tmux", "kill-session", "-t", TMUX_SESSION],
        capture_output=True,
    )

    _cleanup_pid()
    print("✅ 机器人已停止")


def cmd_restart():
    """重启机器人"""
    cmd_stop()
    time.sleep(1)
    cmd_start()


def cmd_status():
    """检查运行状态"""
    # 1. 进程检查
    pid = get_pid()
    running = check_running()

    print("=" * 50)
    print("飞书发票报销机器人 状态报告")
    print("=" * 50)

    if running and pid:
        print(f"✅ 机器人运行中 (PID: {pid})")
        print(f"   tmux session: {TMUX_SESSION}")
    else:
        print("❌ 机器人未运行")

    # 2. 飞书 CLI 连接
    result = subprocess.run(
        ["lark-cli", "auth", "status"],
        capture_output=True, text=True, timeout=10,
    )
    stdout = result.stdout.strip()
    if "bot" in stdout and "ready" in stdout:
        print("✅ 飞书 CLI bot 认证正常")
    else:
        print(f"⚠️ 飞书 CLI 状态: {stdout[:100]}")

    # 3. 最近日志
    if LOG_FILE.exists():
        print(f"\n📋 最近 10 行日志 ({LOG_FILE}):")
        lines = LOG_FILE.read_text().splitlines()
        for line in lines[-10:]:
            print(f"   {line}")

    print("=" * 50)


def cmd_logs(lines: int = 50):
    """查看日志"""
    if not LOG_FILE.exists():
        print(f"⚠️ 日志文件不存在: {LOG_FILE}")
        return

    with open(LOG_FILE) as f:
        all_lines = f.readlines()

    for line in all_lines[-lines:]:
        print(line.rstrip())


def cmd_config(key: str = None, value: str = None):
    """查看或修改 .env 配置"""
    if not ENV_FILE.exists():
        print(f"⚠️ .env 文件不存在: {ENV_FILE}")
        return

    if key and value:
        # 修改配置
        content = ENV_FILE.read_text()
        lines = content.splitlines()
        new_lines = []
        found = False
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"\n{key}={value}")

        ENV_FILE.write_text("\n".join(new_lines) + "\n")
        print(f"✅ 已更新: {key}={value}")
    elif key:
        # 查看单个配置
        content = ENV_FILE.read_text()
        for line in content.splitlines():
            if line.startswith(f"{key}="):
                print(line)
                return
        print(f"⚠️ 未找到配置项: {key}")
    else:
        # 查看所有配置（隐藏密钥）
        content = ENV_FILE.read_text()
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "SECRET" in line:
                parts = line.split("=", 1)
                print(f"{parts[0]}=****")
            else:
                print(line)


# ── 辅助函数 ──

def get_pid() -> int | None:
    """从 PID 文件读取进程 ID"""
    if PID_FILE.exists():
        try:
            return int(PID_FILE.read_text().strip())
        except ValueError:
            return None
    return None


def check_running() -> bool:
    """检查机器人是否在运行"""
    # 检查 tmux session
    result = subprocess.run(
        ["tmux", "has-session", "-t", TMUX_SESSION],
        capture_output=True,
    )
    if result.returncode == 0:
        return True

    # 检查 PID 文件
    pid = get_pid()
    if pid:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            pass

    return False


def _cleanup_pid():
    """清理 PID 文件"""
    PID_FILE.unlink(missing_ok=True)


# ── 入口 ──

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发票机器人管理工具")
    parser.add_argument("action", choices=["start", "stop", "restart", "status", "logs", "config"])
    parser.add_argument("extra", nargs="*", help="额外参数")

    args = parser.parse_args()

    action_map = {
        "start": cmd_start,
        "stop": cmd_stop,
        "restart": cmd_restart,
        "status": cmd_status,
        "logs": lambda: cmd_logs(int(args.extra[0]) if args.extra else 50),
        "config": lambda: cmd_config(
            args.extra[0] if args.extra else None,
            args.extra[1] if len(args.extra) > 1 else None,
        ),
    }

    action_map[args.action]()
