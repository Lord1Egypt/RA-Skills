#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding.lower().replace('-','') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer') and sys.stderr.encoding.lower().replace('-','') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
"""
venue-auth-tool v2.0.0
认证模块（pt-passport 体系）。
管理 device_token；Token 有效期由 pt-passport CLI 自动管理（30天）。

client_id: 578aafab312b44f1b76b0529b06bb0c6

用法示例：
  python auth.py get-device-token
  python auth.py logout
  python auth.py clear-device-token
"""

import argparse
import hashlib
import json
import random
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────────────────────
AUTH_KEY    = "meituan-venue-guide"
CLIENT_ID   = "578aafab312b44f1b76b0529b06bb0c6"

# 日志路径（与 bind.py 同目录，方便统一诊断）
_AUTH_LOG_FILE = Path(tempfile.gettempdir()) / "fenxiao" / "fenxiao_auth.log"


def _resolve_auth_file() -> Path:
    """
    跨平台确定 Token 存储路径，优先级：
    1. 环境变量 XIAOMEI_AUTH_FILE（显式指定，最高优先级）
    2. ~/.xiaomei-workspace/auth_tokens.json
    """
    import os
    env_path = os.environ.get("XIAOMEI_AUTH_FILE")
    if env_path:
        return Path(env_path)
    return Path.home() / ".xiaomei-workspace" / "auth_tokens.json"


AUTH_FILE = _resolve_auth_file()


# ── 日志工具 ──────────────────────────────────────────────────────────

def _get_device_token_raw() -> str:
    """直接从文件读取 device_token，避免递归调用"""
    try:
        if AUTH_FILE.exists():
            with open(AUTH_FILE, encoding="utf-8") as f:
                return json.load(f).get(AUTH_KEY, {}).get("device_token", "")
    except Exception:
        pass
    return ""


def _load_ai_scene() -> str:
    try:
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, encoding="utf-8") as f:
            return json.load(f).get("aiScene", "")
    except Exception:
        return ""


def _xor_encrypt(data: str, ai_scene: str) -> str:
    """XOR 加密，与 bind.py / diag_auth_log.py 使用完全相同的算法"""
    device_token = _get_device_token_raw()
    if device_token:
        seed = device_token + ai_scene
        flag = "1"
    else:
        seed = ai_scene
        flag = "0"
    key_bytes  = hashlib.sha256(seed.encode()).digest()
    data_bytes = data.encode("utf-8")
    result     = bytes(b ^ key_bytes[i % 32] for i, b in enumerate(data_bytes))
    return flag + ":" + result.hex()


def write_auth_log(entry: dict):
    """将认证操作记录加密后追加写入日志文件，任何异常静默跳过"""
    try:
        _AUTH_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        raw      = json.dumps(entry, ensure_ascii=False)
        ai_scene = _load_ai_scene()
        encrypted = _xor_encrypt(raw, ai_scene) if ai_scene else raw
        with open(_AUTH_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(encrypted + "\n")
    except Exception:
        pass


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── 存储操作 ──────────────────────────────────────────────────────────

def load_auth() -> dict:
    if AUTH_FILE.exists():
        try:
            with open(AUTH_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_auth(data: dict):
    import os, stat
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(AUTH_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def get_token_data() -> dict:
    return load_auth().get(AUTH_KEY, {})


def save_token_data(token_data: dict):
    auth = load_auth()
    auth[AUTH_KEY] = token_data
    save_auth(auth)


# ── 设备ID管理 ────────────────────────────────────────────────────────

def generate_device_token(seed: str) -> str:
    """
    生成设备唯一标识（device_token）。
    算法：MD5（seed + 毫秒时间戳 + 0~1000随机整数）
    device_token 与设备绑定，一旦生成后永不覆盖。
    """
    ts_ms    = int(time.time() * 1000)
    rand_int = random.randint(0, 1000)
    raw      = f"{seed}{ts_ms}{rand_int}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def _ensure_device_token(token_data: dict) -> str:
    """确保 device_token 存在，不存在则生成并持久化，返回 device_token"""
    dt = token_data.get("device_token", "")
    if not dt:
        dt = generate_device_token("meituan-venue-guide")
        token_data["device_token"] = dt
        save_token_data(token_data)
    return dt


# ── 命令：get-device-token ────────────────────────────────────────────

def cmd_get_device_token():
    """获取 device_token，不存在则自动生成"""
    token_data   = get_token_data()
    device_token = _ensure_device_token(token_data)

    write_auth_log({"time": _now(), "action": "get-device-token", "result": "ok"})
    print(json.dumps({
        "success":      True,
        "device_token": device_token,
    }, ensure_ascii=False))


# ── 命令：logout ──────────────────────────────────────────────────────

def cmd_logout():
    """
    退出登录：调用 pt-passport CLI 清除本地缓存的 Token。
    保留 device_token，不清除设备绑定。
    """
    cli_cleared = False
    try:
        result = subprocess.run(
            ["pt-passport", "logout", "--client_id", CLIENT_ID],
            capture_output=True, text=True, timeout=10,
        )
        cli_cleared = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass  # CLI 不存在或超时，忽略

    token_data   = get_token_data()
    device_token = token_data.get("device_token", "")

    write_auth_log({
        "time":   _now(),
        "action": "logout",
        "result": {"cli_cleared": cli_cleared, "device_token_preserved": bool(device_token)},
    })
    print(json.dumps({
        "success":               True,
        "message":               "已退出登录，下次需重新授权",
        "device_token_preserved": bool(device_token),
        "cli_cache_cleared":     cli_cleared,
    }, ensure_ascii=False))


# ── 命令：clear-device-token ──────────────────────────────────────────

def cmd_clear_device_token():
    """
    清除设备标识，仅在用户明确要求时调用。
    同时清除 device_token 和 pt-passport CLI 缓存。
    """
    token_data      = get_token_data()
    had_device_token = bool(token_data.get("device_token"))

    # 清除 device_token
    token_data["device_token"] = ""
    save_token_data(token_data)

    # 同时清除 pt-passport CLI 缓存
    try:
        subprocess.run(
            ["pt-passport", "logout", "--client_id", CLIENT_ID],
            capture_output=True, text=True, timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass

    write_auth_log({
        "time":   _now(),
        "action": "clear-device-token",
        "result": {"had_device_token": had_device_token},
    })
    print(json.dumps({
        "success":              True,
        "message":              "设备标识已清除，下次登录将生成新的 device_token",
        "device_token_cleared": had_device_token,
    }, ensure_ascii=False))


# ── 入口 ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="美团分销会场认证模块（pt-passport 体系）")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("get-device-token",
                          help="获取/生成 device_token")
    subparsers.add_parser("logout",
                          help="退出登录，清除 pt-passport CLI 缓存（保留 device_token）")
    subparsers.add_parser("clear-device-token",
                          help="清除设备标识，仅在用户明确要求时调用")

    args = parser.parse_args()

    if args.command == "get-device-token":
        cmd_get_device_token()
    elif args.command == "logout":
        cmd_logout()
    elif args.command == "clear-device-token":
        cmd_clear_device_token()


if __name__ == "__main__":
    main()
