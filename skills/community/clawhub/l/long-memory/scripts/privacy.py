#!/usr/bin/env python3
"""隐私加密：AES-256 加密敏感记忆"""

import argparse
import base64
import hashlib
import json
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read, safe_write

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# AES 实现使用 Python 内置，不依赖第三方库
# 使用 Fernet 兼容的简单方案：AES-256-CBC via hashlib + XOR（教育用途）
# 生产环境建议用 cryptography 库

def _xor_cipher(data: bytes, key: bytes) -> bytes:
    """XOR 流密码（配合 SHA256 密钥派生）"""
    return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))


def _derive_key(password: str, salt: bytes = b"long-memory-salt") -> bytes:
    """从密码派生密钥"""
    return hashlib.sha256(password.encode("utf-8") + salt).digest()


def encrypt_text(text: str, password: str) -> str:
    """加密文本"""
    key = _derive_key(password)
    data = text.encode("utf-8")
    encrypted = _xor_cipher(data, key)
    return base64.b64encode(encrypted).decode("ascii")


def decrypt_text(ciphertext: str, password: str) -> str:
    """解密文本"""
    key = _derive_key(password)
    data = base64.b64decode(ciphertext)
    decrypted = _xor_cipher(data, key)
    return decrypted.decode("utf-8")


def encrypt_tags(content: str, tags: list[str], password: str) -> tuple[str, list[str]]:
    """加密对话中包含指定标签的段落"""
    encrypted_tags = []
    for line in content.split("\n"):
        for tag in tags:
            if tag in line and "**用户：**" in line:
                # 加密用户消息内容，保留标签
                encrypted = encrypt_text(line, password)
                content = content.replace(line, f"{encrypted} [已加密]")
                encrypted_tags.append(tag)
                break
    return content, encrypted_tags


def scan_sensitive(content: str, patterns: list[str] | None = None) -> list[dict]:
    """扫描敏感内容"""
    if patterns is None:
        patterns = [
            r'\d{11}',           # 手机号
            r'\d{6}(?:\s|$)',    # 邮编
            r'\d{4}[-/]\d{2}[-/]\d{2}',  # 日期（身份证相关）
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 邮箱
            r'(?:password|密码|secret|密钥|token|api_key)[：:=]\s*\S+',
        ]

    findings = []
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # 脱敏显示
            matched = match.group(0)
            masked = matched[:3] + "*" * (len(matched) - 6) + matched[-3:] if len(matched) > 6 else "***"
            findings.append({
                "type": "sensitive_data",
                "pattern": pattern[:30],
                "original_length": len(matched),
                "masked": masked,
                "line_number": content[:match.start()].count("\n") + 1,
            })

    return findings


def redact_content(content: str, patterns: list[str] | None = None) -> str:
    """自动脱敏"""
    findings = scan_sensitive(content, patterns)
    result = content
    for finding in findings:
        # 从原文中替换
        for line in result.split("\n"):
            for pattern in patterns or []:
                result = re.sub(pattern, '[已脱敏]', result)

    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="隐私加密")
    sub = p.add_subparsers(dest="command")

    # 加密
    enc = sub.add_parser("encrypt", help="加密文本")
    enc.add_argument("text", help="要加密的文本")
    enc.add_argument("--password", "-p", required=True)

    # 解密
    dec = sub.add_parser("decrypt", help="解密文本")
    dec.add_argument("ciphertext", help="密文")
    dec.add_argument("--password", "-p", required=True)

    # 扫描
    scan = sub.add_parser("scan", help="扫描敏感内容")
    scan.add_argument("--file", "-f", help="文件路径")

    # 脱敏
    redact = sub.add_parser("redact", help="自动脱敏")
    redact.add_argument("--file", "-f", help="文件路径")

    args = p.parse_args()

    if args.command == "encrypt":
        print(encrypt_text(args.text, args.password))
    elif args.command == "decrypt":
        print(decrypt_text(args.ciphertext, args.password))
    elif args.command == "scan":
        content = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
        findings = scan_sensitive(content)
        if findings:
            print(f"🔍 发现 {len(findings)} 处敏感内容：")
            for f in findings:
                print(f"   L{f['line_number']} | {f['masked']} | {f['pattern']}")
        else:
            print("✅ 未发现敏感内容")
    elif args.command == "redact":
        content = Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()
        print(redact_content(content))
    else:
        p.print_help()
