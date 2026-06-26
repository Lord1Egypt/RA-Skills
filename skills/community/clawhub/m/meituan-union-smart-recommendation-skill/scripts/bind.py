#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
if hasattr(sys.stdout, 'buffer') and sys.stdout.encoding.lower().replace('-','') != 'utf8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer') and sys.stderr.encoding.lower().replace('-','') != 'utf8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
venue-bind-tool v1.0.1
口令绑定模块，负责用户口令与媒体绑定、本地绑定状态管理、会场链接读取。

用法示例：
  python bind.py bind --token <user_token> --code-word <口令>
  python bind.py status
  python bind.py get-links
  python bind.py get-code-word
  python bind.py clear
"""

import argparse
import hashlib
import json
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────────────────────

# 绑定接口
BIND_API_URL   = "https://click.meituan.com/cps/skill/user/code/bind"
BIND_FILE      = Path.home() / ".xiaomei-workspace" / "venue_bind.json"
AUTH_FILE      = Path.home() / ".xiaomei-workspace" / "auth_tokens.json"
AUTH_KEY       = "meituan-venue-guide"

# 绑定日志路径：与认证日志同目录，方便统一管理
_BIND_LOG_FILE = Path(tempfile.gettempdir()) / "fenxiao" / "venue_bind.log"


# ── 日志工具 ──────────────────────────────────────────────────────────

def _get_device_token() -> str:
    """从 auth_tokens.json 读取 device_token，读取失败返回空字符串"""
    try:
        if AUTH_FILE.exists():
            with open(AUTH_FILE, encoding="utf-8") as f:
                return json.load(f).get(AUTH_KEY, {}).get("device_token", "")
    except Exception:
        pass
    return ""


def _load_ai_scene() -> str:
    """从 config.json 读取 aiScene，读取失败返回空字符串"""
    try:
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, encoding="utf-8") as f:
            return json.load(f).get("aiScene", "")
    except Exception:
        return ""


def _xor_encrypt(data: str, ai_scene: str) -> str:
    """XOR 加密，返回带 flag 前缀的 hex 字符串。
    前缀 '1:' = key 用 sha256(device_token + aiScene)
    前缀 '0:' = 降级，key 用 sha256(aiScene)
    与 auth.py / diag_bind_log.py 加密方式完全一致，可用同一个解密工具查看。
    """
    device_token = _get_device_token()
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


def write_bind_log(entry: dict):
    """将绑定操作记录加密后追加写入日志文件，任何异常静默跳过。
    加密方式与 auth.py write_auth_log 完全一致：sha256(device_token + aiScene)
    """
    try:
        _BIND_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        raw      = json.dumps(entry, ensure_ascii=False)
        ai_scene = _load_ai_scene()
        encrypted = _xor_encrypt(raw, ai_scene) if ai_scene else raw
        with open(_BIND_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(encrypted + "\n")
    except Exception:
        pass


# ── 存储操作 ──────────────────────────────────────────────────────────

def load_bind() -> dict:
    """读取本地口令绑定数据"""
    if BIND_FILE.exists():
        try:
            with open(BIND_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_bind(data: dict):
    """写入本地口令绑定数据，仅当前用户可读写（0600）"""
    import os, stat
    BIND_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BIND_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(BIND_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass  # Windows 不支持 chmod，静默跳过


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── 命令：bind ────────────────────────────────────────────────────────

def cmd_bind(token: str, code_word: str):
    """
    调用口令绑定接口，成功后将 expireTime、skillActLinkInfoList、codeWord 写入本地。
    """
    import httpx

    url  = BIND_API_URL
    body = {
        "token":    token,
        "codeWord": code_word,
    }

    log_entry = {
        "time":   _now(),
        "action": "bind",
        "request": {
            "url":             url,
            "token_masked":    token[:8] + "****" if token else "",
            "code_word_masked": code_word[:2] + "****" if len(code_word) > 2 else "****",
        },
    }

    try:
        resp      = httpx.post(
            url,
            json=body,
            headers={
                "Content-Type": "application/json",
            },
            timeout=10,
            verify=True,
            trust_env=False,
        )
        log_entry["response"] = {"http_status": resp.status_code, "body": resp.text[:500]}
        resp_data = resp.json()
        code      = resp_data.get("code")

        if code == 0:
            expire_time          = resp_data.get("expireTime", 0)
            skill_act_link_infos = resp_data.get("skillActLinkInfoList", [])

            # 写入本地存储
            bind_data = {
                "codeWord":             code_word,
                "expireTime":           expire_time,
                "skillActLinkInfoList": skill_act_link_infos,
                "boundAt":              int(time.time()),
            }
            save_bind(bind_data)

            log_entry["result"] = {
                "success":    True,
                "expireTime": expire_time,
                "link_count": len(skill_act_link_infos),
            }
            write_bind_log(log_entry)

            print(json.dumps({
                "success":              True,
                "expireTime":           expire_time,
                "skillActLinkInfoList": skill_act_link_infos,
                "message":              "口令绑定成功",
            }, ensure_ascii=False))

        else:
            # 非 0 均视为失败，透传 code 和 msg 供调用方判断
            log_entry["result"] = {
                "success": False,
                "code":    code,
                "message": resp_data.get("msg", "绑定失败"),
            }
            write_bind_log(log_entry)

            print(json.dumps({
                "success": False,
                "code":    code,
                "message": resp_data.get("msg", "绑定失败"),
            }, ensure_ascii=False))
            sys.exit(1)

    except Exception as e:
        log_entry["result"] = {"success": False, "error": "NETWORK_ERROR", "message": str(e)}
        write_bind_log(log_entry)

        print(json.dumps({
            "success": False,
            "error":   "NETWORK_ERROR",
            "message": str(e),
        }, ensure_ascii=False))
        sys.exit(1)


# ── 命令：status ──────────────────────────────────────────────────────

def cmd_status():
    """
    检查本地口令绑定状态。
    - 无绑定记录      → valid: false, reason: no_bind
    - 有记录但已过期  → valid: false, reason: expired
    - 有记录且未过期  → valid: true
    注意：expireTime=0 表示永不过期，视为有效。
    """
    data = load_bind()

    if not data or "expireTime" not in data:
        write_bind_log({"time": _now(), "action": "status", "result": {"valid": False, "reason": "no_bind"}})
        print(json.dumps({
            "valid":  False,
            "reason": "no_bind",
        }, ensure_ascii=False))
        return

    expire_time = data.get("expireTime", 0)

    # expireTime=0 表示永不过期
    if expire_time != 0 and int(time.time()) > expire_time:
        write_bind_log({"time": _now(), "action": "status", "result": {"valid": False, "reason": "expired", "expireTime": expire_time}})
        print(json.dumps({
            "valid":      False,
            "reason":     "expired",
            "expireTime": expire_time,
        }, ensure_ascii=False))
        return

    # valid:true 是正常状态，不写日志，避免每次对话准入都落日志
    print(json.dumps({
        "valid":      True,
        "expireTime": expire_time,
        "reason":     "",
    }, ensure_ascii=False))


# ── 命令：get-links ───────────────────────────────────────────────────

def cmd_get_links():
    """
    读取本地缓存的会场链接列表。
    返回 skillActLinkInfoList，每项包含 tenantName 和 link。
    """
    data  = load_bind()
    links = data.get("skillActLinkInfoList", [])

    if not links:
        write_bind_log({"time": _now(), "action": "get-links", "result": {"success": False, "error": "NO_LINKS"}})
        print(json.dumps({
            "success": False,
            "error":   "NO_LINKS",
            "message": "本地暂无会场链接，请先完成口令绑定",
        }, ensure_ascii=False))
        sys.exit(1)

    write_bind_log({"time": _now(), "action": "get-links", "result": {"success": True, "link_count": len(links)}})
    print(json.dumps({
        "success": True,
        "links":   links,
    }, ensure_ascii=False))


# ── 命令：get-code-word ───────────────────────────────────────────────

def cmd_get_code_word():
    """
    读取本地存储的口令（codeWord），用于口令过期时自动重试绑定。
    """
    data      = load_bind()
    code_word = data.get("codeWord", "")

    if not code_word:
        write_bind_log({"time": _now(), "action": "get-code-word", "result": {"success": False, "error": "NO_CODE_WORD"}})
        print(json.dumps({
            "success":  False,
            "error":    "NO_CODE_WORD",
            "message":  "本地暂无口令记录",
        }, ensure_ascii=False))
        sys.exit(1)

    write_bind_log({"time": _now(), "action": "get-code-word", "result": {"success": True}})
    print(json.dumps({
        "success":   True,
        "codeWord":  code_word,
    }, ensure_ascii=False))


# ── 命令：clear ───────────────────────────────────────────────────────

def cmd_clear():
    """
    清除本地所有口令绑定数据（expireTime、skillActLinkInfoList、codeWord）。
    通常在用户退出登录或清除设备标识时调用。
    """
    if BIND_FILE.exists():
        save_bind({})

    write_bind_log({"time": _now(), "action": "clear", "result": {"success": True}})
    print(json.dumps({
        "success": True,
        "message": "本地口令绑定数据已清除",
    }, ensure_ascii=False))


# ── 入口 ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="美团分销会场口令绑定工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # bind
    p_bind = subparsers.add_parser("bind", help="调用口令绑定接口")
    p_bind.add_argument("--token",     required=True, help="用户 Token（user_token）")
    p_bind.add_argument("--code-word", required=True, help="媒体口令（codeWord）")

    # status
    subparsers.add_parser("status", help="检查本地口令绑定状态")

    # get-links
    subparsers.add_parser("get-links", help="读取本地缓存的会场链接列表")

    # get-code-word
    subparsers.add_parser("get-code-word", help="读取本地存储的口令（用于自动续期）")

    # clear
    subparsers.add_parser("clear", help="清除本地所有口令绑定数据")

    args = parser.parse_args()

    if args.command == "bind":
        cmd_bind(args.token, args.code_word)
    elif args.command == "status":
        cmd_status()
    elif args.command == "get-links":
        cmd_get_links()
    elif args.command == "get-code-word":
        cmd_get_code_word()
    elif args.command == "clear":
        cmd_clear()


if __name__ == "__main__":
    main()
