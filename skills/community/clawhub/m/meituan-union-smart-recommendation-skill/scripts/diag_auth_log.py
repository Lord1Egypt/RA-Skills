#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diag_auth_log.py — 认证日志诊断工具

解密并展示 auth.py 写入的加密认证日志，方便排查登录、pt-passport 授权、Token 相关问题。

用法：
  python diag_auth_log.py              # 展示最近 100 条
  python diag_auth_log.py --tail 20    # 展示最近 20 条
  python diag_auth_log.py --all        # 展示全部日志
"""

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

# ── 路径常量 ──────────────────────────────────────────────────────────
AUTH_LOG_FILE = Path(tempfile.gettempdir()) / "fenxiao" / "fenxiao_auth.log"
AUTH_FILE     = Path.home() / ".xiaomei-workspace" / "auth_tokens.json"
AUTH_KEY      = "meituan-venue-guide"


# ── 解密工具 ──────────────────────────────────────────────────────────

def _get_device_token() -> str:
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


def _xor_decrypt(encrypted: str, ai_scene: str) -> str:
    """
    解密 XOR 加密的日志行。
    格式：<flag>:<hex_data>
      flag=1 → key = sha256(device_token + aiScene)
      flag=0 → key = sha256(aiScene)
    若格式不符（未加密的旧日志），直接返回原文。
    """
    if ":" not in encrypted:
        return encrypted  # 未加密格式（旧日志），直接返回

    flag, hex_data = encrypted.split(":", 1)

    try:
        data_bytes = bytes.fromhex(hex_data)
    except ValueError:
        return encrypted  # 不是合法 hex，直接返回原文

    device_token = _get_device_token()

    if flag == "1" and device_token:
        seed = device_token + ai_scene
    else:
        # flag=0 或 device_token 丢失，降级用 aiScene
        seed = ai_scene

    key_bytes = hashlib.sha256(seed.encode()).digest()
    result    = bytes(b ^ key_bytes[i % 32] for i, b in enumerate(data_bytes))
    return result.decode("utf-8", errors="replace")


def decrypt_line(line: str, ai_scene: str) -> str:
    """解密单行日志，返回可读字符串"""
    line = line.rstrip("\n")
    if not line:
        return ""
    try:
        return _xor_decrypt(line, ai_scene)
    except Exception as e:
        return f"[解密失败: {e}] {line}"


# ── 主逻辑 ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="解密并展示 auth.py 认证日志"
    )
    parser.add_argument("--tail", type=int, default=100, metavar="N",
                        help="展示最近 N 条日志（默认 100）")
    parser.add_argument("--all",  action="store_true",
                        help="展示全部日志（忽略 --tail）")
    args = parser.parse_args()

    if not AUTH_LOG_FILE.exists():
        print(f"[INFO] 日志文件不存在：{AUTH_LOG_FILE}")
        print("       尚未产生任何认证操作记录，或日志路径已更改。")
        sys.exit(0)

    ai_scene = _load_ai_scene()
    if not ai_scene:
        print("[WARN] 未找到 config.json / aiScene 配置，将尝试使用空 key 解密（可能乱码）")

    with open(AUTH_LOG_FILE, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    if not lines:
        print("[INFO] 日志文件为空。")
        sys.exit(0)

    # 取最后 N 条
    if not args.all:
        lines = lines[-args.tail:]

    print(f"{'─' * 60}")
    print(f"  认证日志诊断  |  文件：{AUTH_LOG_FILE}")
    print(f"  共 {len(lines)} 条（{'全部' if args.all else f'最近 {args.tail} 条'}）")
    print(f"{'─' * 60}")

    for i, raw_line in enumerate(lines, 1):
        decrypted = decrypt_line(raw_line, ai_scene)
        if not decrypted:
            continue
        # 尝试格式化 JSON
        try:
            obj = json.loads(decrypted)
            pretty = json.dumps(obj, ensure_ascii=False, indent=2)
        except Exception:
            pretty = decrypted

        print(f"\n[{i}] {pretty}")

    print(f"\n{'─' * 60}")
    print(f"  诊断完成，共展示 {len(lines)} 条记录")
    print(f"{'─' * 60}")


if __name__ == "__main__":
    main()
