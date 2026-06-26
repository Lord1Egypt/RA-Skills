#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw HTTP API Caller / OpenClaw HTTP API 调用器

Call a remote OpenClaw Gateway via its OpenAI-compatible /v1/chat/completions endpoint.
Session persistence is handled purely by the x-openclaw-session-key HTTP header.

通过 x-openclaw-session-key HTTP header 保持会话上下文，无需本地历史文件。

Usage / 用法:
    python oc_call.py "Your question"    Call OpenClaw / 调用 OpenClaw
    python oc_call.py /clear            Clear session / 清除会话
    python oc_call.py /new              New session / 新建会话
"""

import os
import sys
import json
import uuid
import urllib.request
import urllib.error

# Windows-safe stdout / Windows 安全输出（处理控制台编码问题）
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def safe_print(s):
    """Print string safely, replacing unencodable chars on Windows."""
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf-8", errors="replace").decode("utf-8"))

# ─────────────────────────────────────────────────────────────
# Configuration / 配置
# Override via environment variables if needed.
# 如需修改请通过环境变量覆盖以下默认值。
# ─────────────────────────────────────────────────────────────
OC_URL = "http://192.168.123.106:28789/v1/chat/completions"  # Remote Gateway URL / 远程 Gateway 地址
OC_TOKEN = "87654321"                                          # Auth token / 认证 Token
SESSION_FILE = os.path.expanduser("~/.oc_session")             # Session key storage / Session Key 存储路径


# ─────────────────────────────────────────────────────────────
# Session Management / 会话管理
# ─────────────────────────────────────────────────────────────

def load_session():
    """
    Load existing session key from disk.
    从磁盘加载已保存的 session key。
    Returns empty string if file doesn't exist or is corrupted.
    文件不存在或损坏时返回空字符串。
    """
    if os.path.exists(SESSION_FILE):
        try:
            return json.load(open(SESSION_FILE)).get("session_key", "")
        except Exception:
            return ""
    return ""


def save_session(session_key):
    """Save session key to disk. / 将 session key 写入磁盘。"""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"session_key": session_key}, f, ensure_ascii=False, indent=2)


def get_or_create_session():
    """
    Return existing session key or create a new one.
    返回已存在的 session key，或创建新的。
    """
    key = load_session()
    if not key:
        key = "oc-" + uuid.uuid4().hex[:12]
        save_session(key)
    return key


def clear_session():
    """Delete session file to clear current session. / 删除会话文件以清除当前会话。"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    safe_print("Session cleared. / 会话已清除。")


def new_session():
    """Generate and save a brand new session key. / 生成并保存全新的 session key。"""
    key = "oc-" + uuid.uuid4().hex[:12]
    save_session(key)
    safe_print(f"New session created: {key} / 新会话已创建: {key}")


# ─────────────────────────────────────────────────────────────
# API Call / API 调用
# ─────────────────────────────────────────────────────────────

def call_openclaw(question, session_key):
    """
    Send a single question to OpenClaw Gateway and return the response.
    向 OpenClaw Gateway 发送单个问题并返回回复。

    Args:
        question: The user's question / 用户问题
        session_key: x-openclaw-session-key header value / 会话标识

    Returns:
        Assistant's reply text, or error message / 助手回复文本，或错误信息
    """
    payload = {
        "model": "openclaw/default",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 4096
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {OC_TOKEN}",
        "Content-Type": "application/json",
        "x-openclaw-session-key": session_key   # Session persistence key / 会话保持关键
    }
    req = urllib.request.Request(OC_URL, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        return f"HTTP Error {e.code}: {body}"
    except Exception as e:
        return f"Error: {str(e)}"


# ─────────────────────────────────────────────────────────────
# Main Entry / 主入口
# ─────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        safe_print("Usage / 用法:")
        safe_print("  oc_call.py \"Your question\"    Call OpenClaw / 调用 OpenClaw")
        safe_print("  oc_call.py /clear              Clear session / 清除会话")
        safe_print("  oc_call.py /new                New session / 新建会话")
        sys.exit(1)

    cmd = sys.argv[1]

    # /clear — wipe session key and start fresh
    if cmd == "/clear":
        clear_session()
        return

    # /new — force a new session key
    if cmd == "/new":
        new_session()
        return

    # Normal question — reuse or create session key, then call API
    question = cmd
    session_key = get_or_create_session()
    response = call_openclaw(question, session_key)
    safe_print(response)


if __name__ == "__main__":
    main()
