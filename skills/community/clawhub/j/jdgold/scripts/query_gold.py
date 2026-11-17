#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""金价查询助手：解析关键词或按 source 调用本地 gold 聚合服务。"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("GOLD_SERVICE_BASE", "http://localhost:3777").rstrip("/")

SUPPORTED = {
    "minsheng": {
        "name": "民生银行积存金",
        "patterns": [r"民生银行积存金", r"民生积存金", r"民生"],
    },
    "zheshang": {
        "name": "浙商银行账户金",
        "patterns": [r"浙商银行账户金", r"浙商账户金", r"浙商"],
    },
    "paxgusd": {
        "name": "PAXGUSD暗金",
        "patterns": [r"PAXGUSD暗金", r"PAXGUSD", r"PAXG", r"暗金"],
    },
}

UNIT_LABEL = {"CNY": "元", "USD": "美元", "gram": "克", "ounce": "盎司"}

GENERIC_GOLD = [
    r"查询金价",
    r"金价查询",
    r"查(?:一下|下)?(?:今天|当前|实时)?金价",
    r"黄金价格",
    r"黄金多少钱",
    r"^金价$",
]
UNSUPPORTED_HINTS = [
    r"工行", r"工商", r"伦敦", r"COMEX", r"沪金", r"期货", r"国际金", r"现货黄金",
]


def parse_source(text: str):
    text = text.strip()
    if not text:
        return None, "missing"
    hits = []
    for source, meta in SUPPORTED.items():
        for pat in meta["patterns"]:
            if re.search(pat, text, re.I):
                hits.append(source)
                break
    if hits:
        return hits[0], "ok"
    for pat in UNSUPPORTED_HINTS:
        if re.search(pat, text, re.I):
            return None, "unsupported"
    for pat in GENERIC_GOLD:
        if re.search(pat, text):
            return None, "missing"
    if re.search(r"金价|黄金", text):
        return None, "missing"
    return None, "unsupported"


def fmt_unit(currency: str, unit: str) -> str:
    cur = UNIT_LABEL.get(currency, currency)
    u = UNIT_LABEL.get(unit, unit)
    return f"{cur}/{u}"


def fmt_change(v):
    if v is None:
        return "—"
    sign = "+" if v > 0 else ""
    return f"{sign}{v}"


def fetch(source: str) -> dict:
    url = f"{BASE}/api/gold/{source}"
    headers = {"Accept": "application/json"}
    claw = os.environ.get("CLAW", "").strip()
    if claw:
        headers["x-claw"] = claw
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read().decode())
    if body.get("code") != 0 or not body.get("data"):
        raise RuntimeError(body.get("message") or "接口返回异常")
    return body["data"]


def render(data: dict) -> str:
    unit = fmt_unit(data.get("currency", ""), data.get("unit", ""))
    cp = data.get("changePercent")
    cp_str = "—" if cp is None else f"{fmt_change(cp)}%"
    return (
        f"【{data.get('sourceName', '')}】\n"
        f"实时金价：{data.get('last')} {unit}\n"
        f"涨跌幅：{fmt_change(data.get('change'))}\n"
        f"涨跌率：{cp_str}"
    )


def main(argv=None):
    p = argparse.ArgumentParser(description="查询本地 gold 聚合服务金价")
    p.add_argument("source", nargs="?", help="minsheng | zheshang | paxgusd")
    p.add_argument("--parse", "-p", metavar="TEXT", help="从用户原文解析标的")
    p.add_argument("--json", action="store_true", help="输出原始 JSON")
    p.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = p.parse_args(argv)
    if args.claw:
        os.environ["CLAW"] = args.claw.strip()

    if args.parse is not None:
        source, status = parse_source(args.parse)
        if status == "missing":
            print("请输入要查询的黄金标的")
            return 1
        if status == "unsupported":
            print("暂不支持您要查询的黄金标的")
            return 2
    elif args.source:
        source = args.source.lower()
        if source not in SUPPORTED:
            print("暂不支持您要查询的黄金标的", file=sys.stderr)
            return 2
    else:
        p.print_help()
        return 1

    try:
        data = fetch(source)
    except urllib.error.URLError as e:
        print(f"金价服务不可用 ({BASE})：{e}", file=sys.stderr)
        return 3
    except RuntimeError as e:
        if getattr(e, "code", None) == 403:
            print(e.message, file=sys.stderr)
            return 3
        print(str(e), file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
