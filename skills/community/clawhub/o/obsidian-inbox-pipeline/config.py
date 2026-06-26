#!/usr/bin/env python3
"""统一配置读取模块 — 所有脚本通过 get_config() 获取配置"""
import os
import re

# ── Env Var ────────────────────────────────────────────
def get_vault() -> str:
    """Obsidian Vault 根目录"""
    path = os.environ.get("OBSIDIAN_VAULT_PATH", "").strip()
    if path:
        return path
    # fallback: 尝试 obsidian-cli
    import subprocess
    try:
        result = subprocess.run(
            ["obsidian-cli", "print-default", "--path-only"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    raise RuntimeError(
        "OBSIDIAN_VAULT_PATH 未设置，且 obsidian-cli 不可用。"
        "请设置环境变量或安装 obsidian-cli。"
    )


def get_telegram_config() -> dict:
    """Telegram Bot 配置（可选）"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return {"enabled": False}
    return {"enabled": True, "token": token, "chat_id": chat_id}


def get_feishu_config() -> dict:
    """飞书 Bot 配置（可选）"""
    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    receive_id = os.environ.get("FEISHU_RECEIVE_ID", "").strip()
    if not app_id or not app_secret:
        return {"enabled": False}
    return {"enabled": True, "app_id": app_id, "app_secret": app_secret, "receive_id": receive_id}


# ── 工具函数 ────────────────────────────────────────────
def sanitize_filename(title: str) -> str:
    """标题 → 安全文件名"""
    name = re.sub(r'[<>:"/\\|?*]', '', title)
    name = name[:60].strip()
    return name or "untitled"


def slugify(s: str) -> str:
    """字符串 → URL-safe slug"""
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s).strip('-')
    return s[:40]
