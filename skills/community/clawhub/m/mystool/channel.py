"""
mystool 渠道接入层

OpenClaw 的 Telegram / QQBot 消息到达时，
在 SKILL.md 或 agent 系统提示中调用此模块处理。

用法（在 agent 处理消息时）：
    import asyncio, sys
    sys.path.insert(0, str(Path(__file__).parent))
    from channel import dispatch
    reply = asyncio.run(dispatch(message_text, sender_id, channel))
    # reply 为 None 表示不是 mystool 指令，忽略即可
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from plugin import handle


def _log_command(user_id: str, command: str, result: str):
    """记录用户命令日志（仅记录错误）"""
    if not result:
        return
    
    # 判断是否为错误
    is_error = "❌" in result or "失败" in result or "错误" in result or "异常" in result
    if not is_error:
        return
    
    log_dir = Path(__file__).parent / "log"
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}.log"
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 完整记录错误信息
    result_line = result.replace("\n", " | ").replace("\r", "")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ❌ user={user_id} cmd={command[:50]} → {result_line}\n")


def _log_error(user_id: str, command: str, error: Exception):
    """记录 Python 运行时异常"""
    import traceback
    
    log_dir = Path(__file__).parent / "log"
    log_dir.mkdir(exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}.log"
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    tb = traceback.format_exc()
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}] 💥 RUNTIME ERROR user={user_id} cmd={command[:50]}\n")
        f.write(f"Error: {error}\n")
        f.write(f"{tb}\n")


async def dispatch(message: str, sender_id: str = "", channel: str = "") -> Optional[str]:
    """
    分发消息到 mystool 处理器。

    :param message:   用户发送的原始文本
    :param sender_id: 发送者 ID（Telegram chat_id / QQ openid 等）
    :param channel:   渠道标识（telegram / qqbot）
    :return: 回复文本，None 表示不是 mystool 指令
    """
    # 用 sender_id 作为账号隔离 key
    user_key = sender_id or f"{channel}_default"
    
    try:
        reply = await handle(message, user_id=user_key)
    except Exception as e:
        # 记录运行时异常
        _log_error(user_key, message.strip(), e)
        reply = f"❌ 程序异常: {type(e).__name__}: {e}"
    
    # 记录错误日志
    if reply:
        _log_command(user_key, message.strip(), reply)
    
    return reply


# ── 快捷函数（供 cron agentTurn 直接 import 使用）────────────────────────────

async def push_to_channels(text: str):
    """
    将文本同时推送到 Telegram 和 QQBot。
    在 cron agentTurn 中通过 exec 调用此函数。
    """
    # 这里只是占位，实际推送由 cron agentTurn 中的 message 工具完成
    # 此函数供 runner.py 调用后打印结果，由 agent 负责发送
    print(text)
