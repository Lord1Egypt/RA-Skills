#!/usr/bin/env python3
"""
IT运维工具箱 - 实用工具集
功能: 密码生成、Cron解析、JSON/YAML格式化、Base64/JWT解码、
      正则测试、UUID生成、时间戳转换、文件MD5校验
用法: python utils.py <command> [args...]
"""

import sys
import os
import re
import json
import hashlib
import base64
import argparse
import secrets
import string
import time
import uuid
from datetime import datetime, timezone

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def ok(msg):    return color(f"✅ {msg}", "32")
def warn(msg):  return color(f"⚠️  {msg}", "33")
def err(msg):   return color(f"❌ {msg}", "31")
def info(msg):  return color(f"ℹ️  {msg}", "36")
def bold(msg):  return color(msg, "1")

def section(title):
    print(f"\n{bold('═' * 55)}")
    print(f"  {bold(title)}")
    print(bold('═' * 55))

# ─────────────────────────────────────────────
# 密码/Token 生成
# ─────────────────────────────────────────────

def cmd_genpass(length=20, count=5, mode="strong"):
    section(f"随机密码生成 (长度={length}, 数量={count}, 模式={mode})")
    if mode == "strong":
        charset = string.ascii_letters + string.digits + "!@#$%^&*-_=+?"
    elif mode == "alphanum":
        charset = string.ascii_letters + string.digits
    elif mode == "digits":
        charset = string.digits
    elif mode == "hex":
        charset = string.hexdigits[:16]
    else:
        charset = string.ascii_letters + string.digits

    for i in range(count):
        pwd = "".join(secrets.choice(charset) for _ in range(length))
        print(f"  {i+1:2}.  {bold(pwd)}")

def cmd_genuuid(count=5, version=4):
    section(f"UUID 生成 (v{version}, 数量={count})")
    for i in range(count):
        if version == 4:
            u = str(uuid.uuid4())
        elif version == 1:
            u = str(uuid.uuid1())
        else:
            u = str(uuid.uuid4())
        print(f"  {i+1:2}.  {bold(u)}")

def cmd_gentoken(length=32):
    section(f"随机 Token 生成 (hex, {length*2}字符)")
    for i in range(3):
        token = secrets.token_hex(length)
        print(f"  {i+1}.  {bold(token)}")

# ─────────────────────────────────────────────
# Cron 表达式解析
# ─────────────────────────────────────────────

CRON_FIELDS = ["分钟", "小时", "日", "月", "星期"]
WEEKDAYS    = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
MONTHS      = ["", "一月","二月","三月","四月","五月","六月",
               "七月","八月","九月","十月","十一月","十二月"]

def _parse_field(val, field, min_v, max_v, names=None):
    if val == "*":
        return f"每{field}"
    if val == "?":
        return f"不指定{field}"
    if "/" in val:
        parts = val.split("/")
        start = parts[0] if parts[0] != "*" else str(min_v)
        step  = parts[1]
        return f"从{field}{start}开始，每{step}{field}"
    if "-" in val and "," not in val:
        a, b = val.split("-")
        return f"{field} {a} 到 {b}"
    if "," in val:
        parts = val.split(",")
        if names:
            parts = [names[int(p)] if p.isdigit() and int(p) < len(names) else p for p in parts]
        return f"{field}的 {', '.join(parts)}"
    if val.isdigit():
        v = int(val)
        if names and v < len(names):
            return f"{field} {names[v]}"
        return f"{field} {val}"
    return f"{field} {val}"

def cmd_cron(expr):
    section(f"Cron 表达式解析: {expr}")
    parts = expr.strip().split()
    if len(parts) not in (5, 6):
        print(err("Cron 表达式应为 5 或 6 个字段"))
        print(info("格式: 分 时 日 月 周 [年]（标准5字段或含年份的6字段）"))
        return

    if len(parts) == 6:
        minute, hour, day, month, weekday, year = parts
    else:
        minute, hour, day, month, weekday = parts
        year = None

    descriptions = [
        _parse_field(minute,  "分钟", 0, 59),
        _parse_field(hour,    "小时", 0, 23),
        _parse_field(day,     "日",   1, 31),
        _parse_field(month,   "月",   1, 12, MONTHS),
        _parse_field(weekday, "星期", 0, 6,  WEEKDAYS),
    ]

    print(f"\n  {'字段':<6} {'原始值':<12} 解释")
    print(f"  {'─'*6} {'─'*12} {'─'*20}")
    raw = [minute, hour, day, month, weekday]
    for i, (desc, r) in enumerate(zip(descriptions, raw)):
        print(f"  {CRON_FIELDS[i]:<6} {r:<12} {desc}")

    if year:
        print(f"  {'年份':<6} {year:<12} 年份 {year}")

    # 生成人类可读描述
    print(f"\n  {bold('可读描述:')}")
    readable_parts = []
    if minute == "0" and hour != "*":
        readable_parts.append(f"每天{hour}点整")
    elif "/" in minute:
        step = minute.split("/")[1]
        readable_parts.append(f"每{step}分钟")
    else:
        readable_parts.append(descriptions[0])
        readable_parts.append(descriptions[1])

    if day != "*" and day != "?":
        readable_parts.append(descriptions[2])
    if month != "*":
        readable_parts.append(descriptions[3])
    if weekday != "*" and weekday != "?":
        readable_parts.append(descriptions[4])

    print(f"  → {bold('，'.join(readable_parts))}执行一次")

    # 常见表达式对照
    PRESETS = {
        "* * * * *":     "每分钟",
        "0 * * * *":     "每小时整点",
        "0 0 * * *":     "每天午夜",
        "0 0 * * 0":     "每周日午夜",
        "0 0 1 * *":     "每月1日午夜",
        "0 0 1 1 *":     "每年元旦午夜",
        "*/5 * * * *":   "每5分钟",
        "*/15 * * * *":  "每15分钟",
        "0 9-18 * * 1-5":"工作日9-18时整点",
    }
    expr_key = " ".join(parts[:5])
    if expr_key in PRESETS:
        print(f"  {ok('匹配常见模式')}: {PRESETS[expr_key]}")

# ─────────────────────────────────────────────
# JSON 格式化/验证
# ─────────────────────────────────────────────

def cmd_json(source, compact=False):
    section("JSON 格式化")
    # 从文件或字符串
    if os.path.exists(source):
        try:
            with open(source, "r", encoding="utf-8") as f:
                raw = f.read()
            print(info(f"从文件读取: {source}"))
        except Exception as e:
            print(err(f"读取失败: {e}")); return
    else:
        raw = source

    try:
        data = json.loads(raw)
        if compact:
            formatted = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        else:
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
        print(ok("JSON 格式有效"))
        print(f"\n{formatted}")

        # 统计
        def count_keys(obj):
            if isinstance(obj, dict):
                return len(obj) + sum(count_keys(v) for v in obj.values())
            elif isinstance(obj, list):
                return sum(count_keys(v) for v in obj)
            return 0
        nkeys = count_keys(data)
        depth = 0
        def max_depth(o, d=0):
            if isinstance(o, dict):  return max((max_depth(v, d+1) for v in o.values()), default=d)
            if isinstance(o, list):  return max((max_depth(v, d)   for v in o),          default=d)
            return d
        print(f"\n  {info(f'键总数: {nkeys}')}  {info(f'最大深度: {max_depth(data)}')}  {info(f'原始大小: {len(raw)} 字节')}")
    except json.JSONDecodeError as e:
        print(err(f"JSON 格式错误: {e}"))

# ─────────────────────────────────────────────
# Base64 编解码
# ─────────────────────────────────────────────

def cmd_b64(data, decode=False):
    section("Base64 " + ("解码" if decode else "编码"))
    try:
        if decode:
            # 补全 padding
            data += "=" * (4 - len(data) % 4) if len(data) % 4 else ""
            result = base64.b64decode(data).decode("utf-8", errors="replace")
            print(f"  {ok('解码结果:')}")
            print(f"  {result}")
        else:
            result = base64.b64encode(data.encode("utf-8")).decode()
            print(f"  {ok('编码结果:')}")
            print(f"  {bold(result)}")
    except Exception as e:
        print(err(f"操作失败: {e}"))

# ─────────────────────────────────────────────
# JWT 解码
# ─────────────────────────────────────────────

def cmd_jwt(token):
    section("JWT Token 解码")
    parts = token.split(".")
    if len(parts) != 3:
        print(err("不是有效的 JWT Token (需要3段，用.分隔)"))
        return

    def b64_decode_part(s):
        s += "=" * (4 - len(s) % 4) if len(s) % 4 else ""
        return json.loads(base64.urlsafe_b64decode(s).decode("utf-8"))

    try:
        header  = b64_decode_part(parts[0])
        payload = b64_decode_part(parts[1])

        print(f"  {bold('Header:')}")
        print(json.dumps(header, ensure_ascii=False, indent=4))

        print(f"\n  {bold('Payload:')}")
        print(json.dumps(payload, ensure_ascii=False, indent=4))

        # 解析 exp/iat/nbf
        now = int(time.time())
        if "exp" in payload:
            exp_dt = datetime.fromtimestamp(payload["exp"])
            left   = payload["exp"] - now
            if left > 0:
                print(ok(f"\n  Token 有效，剩余 {left//3600}小时{(left%3600)//60}分钟 (到期: {exp_dt})"))
            else:
                print(err(f"\n  Token 已过期! 过期时间: {exp_dt}"))
        if "iat" in payload:
            iat_dt = datetime.fromtimestamp(payload["iat"])
            print(info(f"  签发时间: {iat_dt}"))
        print(f"\n  {warn('注意: 此工具仅解码不验证签名，请勿在生产环境暴露 Token')}")
    except Exception as e:
        print(err(f"解码失败: {e}"))

# ─────────────────────────────────────────────
# 时间戳转换
# ─────────────────────────────────────────────

def cmd_ts(value=None, to_unix=False):
    section("时间戳转换")
    now_ts = int(time.time())
    now_ms = int(time.time() * 1000)

    if value is None:
        print(f"  当前 Unix 时间戳 (秒) : {bold(str(now_ts))}")
        print(f"  当前 Unix 时间戳 (毫秒): {bold(str(now_ms))}")
        dt = datetime.now()
        print(f"  本地时间              : {bold(dt.strftime('%Y-%m-%d %H:%M:%S'))}")
        utc = datetime.utcnow()
        print(f"  UTC 时间              : {bold(utc.strftime('%Y-%m-%d %H:%M:%S'))} UTC")
        return

    # 毫秒 → 秒
    v = int(value)
    if v > 1e12:
        print(info(f"输入看起来是毫秒时间戳，自动转换"))
        v = v // 1000

    try:
        dt_local = datetime.fromtimestamp(v)
        dt_utc   = datetime.utcfromtimestamp(v)
        print(f"  Unix 时间戳 : {bold(str(v))}")
        print(f"  本地时间    : {bold(dt_local.strftime('%Y-%m-%d %H:%M:%S'))}")
        print(f"  UTC 时间    : {bold(dt_utc.strftime('%Y-%m-%d %H:%M:%S'))} UTC")
        diff = now_ts - v
        if diff > 0:
            print(info(f"  距今       : {diff//86400}天 前"))
        else:
            print(info(f"  距今       : {abs(diff)//86400}天 后"))
    except Exception as e:
        print(err(f"转换失败: {e}"))

# ─────────────────────────────────────────────
# 文件 MD5/SHA256 校验
# ─────────────────────────────────────────────

def cmd_hash(filepath, algo="sha256"):
    section(f"文件哈希校验 ({algo.upper()}): {filepath}")
    try:
        h = hashlib.new(algo)
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        digest = h.hexdigest()
        size   = os.path.getsize(filepath)
        print(f"  文件    : {filepath}")
        print(f"  大小    : {size:,} 字节")
        print(f"  {algo.upper():<8}: {bold(digest)}")
        return digest
    except FileNotFoundError:
        print(err(f"文件不存在: {filepath}"))
    except Exception as e:
        print(err(f"计算失败: {e}"))

# ─────────────────────────────────────────────
# 正则测试
# ─────────────────────────────────────────────

def cmd_regex(pattern, text):
    section("正则表达式测试")
    print(f"  Pattern : {bold(pattern)}")
    print(f"  Text    : {text[:200]}")
    try:
        rx = re.compile(pattern)
        matches = list(rx.finditer(text))
        if matches:
            print(f"\n  {ok(f'找到 {len(matches)} 处匹配:')}")
            for i, m in enumerate(matches, 1):
                print(f"  {i}. 位置[{m.start()}:{m.end()}] = {bold(repr(m.group()))}")
                if m.groups():
                    for j, g in enumerate(m.groups(), 1):
                        print(f"     捕获组{j}: {repr(g)}")
        else:
            print(f"\n  {warn('未找到匹配')}")
    except re.error as e:
        print(err(f"正则语法错误: {e}"))

# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(description="IT运维工具箱 - 实用工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("genpass",   help="生成随机密码")
    p.add_argument("-l","--length", type=int, default=20)
    p.add_argument("-n","--count",  type=int, default=5)
    p.add_argument("-m","--mode",   choices=["strong","alphanum","digits","hex"], default="strong")

    p = sub.add_parser("uuid",      help="生成UUID")
    p.add_argument("-n","--count",  type=int, default=5)
    p.add_argument("-v","--version",type=int, choices=[1,4], default=4)

    p = sub.add_parser("token",     help="生成随机Token")
    p.add_argument("-l","--length", type=int, default=32)

    p = sub.add_parser("cron",      help="解析Cron表达式")
    p.add_argument("expr")

    p = sub.add_parser("json",      help="JSON格式化/验证")
    p.add_argument("source", help="JSON字符串或文件路径")
    p.add_argument("-c","--compact", action="store_true")

    p = sub.add_parser("b64",       help="Base64编解码")
    p.add_argument("data")
    p.add_argument("-d","--decode", action="store_true")

    p = sub.add_parser("jwt",       help="JWT Token解码")
    p.add_argument("token")

    p = sub.add_parser("ts",        help="时间戳转换")
    p.add_argument("value", nargs="?", type=int, default=None)

    p = sub.add_parser("hash",      help="文件哈希校验")
    p.add_argument("filepath")
    p.add_argument("-a","--algo",   choices=["md5","sha1","sha256","sha512"], default="sha256")

    p = sub.add_parser("regex",     help="正则表达式测试")
    p.add_argument("pattern")
    p.add_argument("text")

    args = parser.parse_args()
    dispatch = {
        "genpass": lambda: cmd_genpass(args.length, args.count, args.mode),
        "uuid":    lambda: cmd_genuuid(args.count, args.version),
        "token":   lambda: cmd_gentoken(args.length),
        "cron":    lambda: cmd_cron(args.expr),
        "json":    lambda: cmd_json(args.source, args.compact),
        "b64":     lambda: cmd_b64(args.data, args.decode),
        "jwt":     lambda: cmd_jwt(args.token),
        "ts":      lambda: cmd_ts(args.value),
        "hash":    lambda: cmd_hash(args.filepath, args.algo),
        "regex":   lambda: cmd_regex(args.pattern, args.text),
    }
    dispatch[args.cmd]()

if __name__ == "__main__":
    main()
