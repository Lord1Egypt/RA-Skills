#!/usr/bin/env python3
"""
IP归属地查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询IPv4地址的国家、省份、城市、运营商信息

用法:
    python ip_lookup.py <IP地址>
    python ip_lookup.py 58.215.154.11
    python ip_lookup.py 8.8.8.8 1.1.1.1   # 批量查询

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_IP_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_IP_KEY=your_api_key
    3. 直接传参: python ip_lookup.py --key your_api_key <IP>

免费申请 API Key: https://www.juhe.cn/docs/api/id/1
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

API_URL = "http://apis.juhe.cn/ip/ipNewV3"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/1"

# 私有/保留IP段（RFC 1918 + 特殊用途）
PRIVATE_RANGES = [
    ("10.", "A类私有地址 (RFC 1918)"),
    ("172.16.", "B类私有地址 (RFC 1918)"), ("172.17.", "B类私有地址 (RFC 1918)"),
    ("172.18.", "B类私有地址 (RFC 1918)"), ("172.19.", "B类私有地址 (RFC 1918)"),
    ("172.20.", "B类私有地址 (RFC 1918)"), ("172.21.", "B类私有地址 (RFC 1918)"),
    ("172.22.", "B类私有地址 (RFC 1918)"), ("172.23.", "B类私有地址 (RFC 1918)"),
    ("172.24.", "B类私有地址 (RFC 1918)"), ("172.25.", "B类私有地址 (RFC 1918)"),
    ("172.26.", "B类私有地址 (RFC 1918)"), ("172.27.", "B类私有地址 (RFC 1918)"),
    ("172.28.", "B类私有地址 (RFC 1918)"), ("172.29.", "B类私有地址 (RFC 1918)"),
    ("172.30.", "B类私有地址 (RFC 1918)"), ("172.31.", "B类私有地址 (RFC 1918)"),
    ("192.168.", "C类私有地址 (RFC 1918)"),
    ("127.", "本地回环地址"),
    ("0.", "保留地址"),
    ("169.254.", "链路本地地址 (APIPA)"),
    ("100.64.", "运营商级NAT地址 (RFC 6598)"),
    ("198.51.100.", "文档示例地址 (RFC 5737)"),
    ("203.0.113.", "文档示例地址 (RFC 5737)"),
    ("192.0.2.", "文档示例地址 (RFC 5737)"),
    ("240.", "保留地址 (RFC 1112)"),
    ("255.255.255.255", "广播地址"),
]


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_IP_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_IP_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def is_ipv6(ip: str) -> bool:
    return ":" in ip


def is_private_ip(ip: str) -> str | None:
    """检查是否为私有/保留IP，返回描述或 None"""
    for prefix, desc in PRIVATE_RANGES:
        if ip.startswith(prefix):
            return desc
    return None


def query_ip(ip: str, api_key: str) -> dict:
    """查询单个IP归属地"""
    ip = ip.strip()

    if is_ipv6(ip):
        return {
            "ip": ip,
            "success": False,
            "error": "暂不支持 IPv6 地址，聚合数据 IP 查询 API 仅支持 IPv4",
        }

    private = is_private_ip(ip)
    if private:
        return {
            "ip": ip,
            "success": True,
            "private": True,
            "message": f"{ip} 是{private}（内网/保留地址），无法查询归属地",
        }

    params = urllib.parse.urlencode({"key": api_key, "ip": ip})
    url = f"{API_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"ip": ip, "success": False, "error": f"网络请求失败: {e}"}

    if data.get("resultcode") == "200":
        r = data.get("result", {})
        return {
            "ip": ip,
            "success": True,
            "private": False,
            "country": r.get("Country", ""),
            "province": r.get("Province", ""),
            "city": r.get("City", ""),
            "isp": r.get("Isp", ""),
        }

    error_code = data.get("error_code", -1)
    reason = data.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"
    return {
        "ip": ip,
        "success": False,
        "error": f"{reason}{hint}",
        "error_code": error_code,
    }


def format_result_line(result: dict) -> str:
    """格式化单条查询结果（单行）"""
    ip = result["ip"]
    if not result["success"]:
        return f"❌ {ip}  {result.get('error', '未知错误')}"
    if result.get("private"):
        return f"🏠 {ip}  {result['message']}"

    parts = [result["country"], result["province"], result["city"]]
    location = " ".join(p for p in parts if p) or "未知地区"
    isp = result.get("isp", "")
    isp_str = f"  运营商: {isp}" if isp else ""
    return f"🌐 {ip}  {location}{isp_str}"


def print_table(results: list) -> None:
    """以表格形式输出批量查询结果"""
    headers = ["IP地址", "国家", "省份", "城市", "运营商", "备注"]

    rows = []
    for r in results:
        if not r["success"]:
            rows.append([r["ip"], "-", "-", "-", "-", r.get("error", "查询失败")])
        elif r.get("private"):
            rows.append([r["ip"], "-", "-", "-", "-", r["message"]])
        else:
            rows.append([
                r["ip"],
                r.get("country", ""),
                r.get("province", ""),
                r.get("city", ""),
                r.get("isp", ""),
                "✓",
            ])

    col_widths = [len(h) * 2 for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            # 粗略估算中文字符宽度
            width = sum(2 if ord(c) > 127 else 1 for c in str(cell))
            col_widths[i] = max(col_widths[i], width)

    def pad(text, width):
        actual = sum(2 if ord(c) > 127 else 1 for c in str(text))
        return str(text) + " " * max(0, width - actual)

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_row = "| " + " | ".join(pad(h, col_widths[i]) for i, h in enumerate(headers)) + " |"

    print(sep)
    print(header_row)
    print(sep)
    for row in rows:
        print("| " + " | ".join(pad(cell, col_widths[i]) for i, cell in enumerate(row)) + " |")
    print(sep)


def main():
    args = sys.argv[1:]
    cli_key = None

    if "--key" in args:
        idx = args.index("--key")
        if idx + 1 < len(args):
            cli_key = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print("错误: --key 后需要提供 API Key 值")
            sys.exit(1)

    if not args:
        print("用法: python ip_lookup.py [--key YOUR_KEY] <IP地址> [IP地址2 ...]")
        print("示例: python ip_lookup.py 58.215.154.11")
        print(f"\n免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_IP_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_IP_KEY=your_api_key")
        print("   3. 命令行参数: python ip_lookup.py --key your_api_key <IP>")
        print(f"\n免费申请 Key（每天50次免费调用）: {REGISTER_URL}")
        sys.exit(1)

    results = [query_ip(ip, api_key) for ip in args]

    if len(results) == 1:
        print(format_result_line(results[0]))
        print()
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print(f"共查询 {len(results)} 个IP地址:\n")
        print_table(results)
        print()
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
