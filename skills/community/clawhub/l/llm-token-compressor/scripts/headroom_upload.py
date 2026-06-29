#!/usr/bin/env python3
"""
headroom_upload.py — headroom 压缩数据自动上报脚本

功能：
1. 解析 headroom perf 输出，提取压缩统计数据
2. 计算节省 token 数和节省金额（CNY）
3. 上报到 https://mrkjai.com/api/ingest/headroom

使用方法：
  # 方式1：直接解析 headroom perf 输出
  headroom perf 2>&1 | python headroom_upload.py --model claude-sonnet-4 --pricing 0.015

  # 方式2：手动指定数据
  python headroom_upload.py --model claude-sonnet-4 --input-tokens 2840 --output-tokens 1820 --saved-tokens 1020 --saved-cny 0.108 --compression-rate 0.36

  # 方式3：批量上报（从 JSON 文件）
  python headroom_upload.py --batch events.json

依赖：
  pip install requests  # 如果未安装

环境变量：
  MRKJAI_API_KEY — 必填，从 https://mrkjai.com/tools/headroom-dashboard 获取
  MRKJAI_API_BASE — 可选，默认 https://mrkjai.com
"""

import argparse
import json
import os
import re
import sys
from typing import Optional

import requests

# ──────────────────────────────────
# 配置
# ──────────────────────────────────

API_BASE = os.environ.get("MRKJAI_API_BASE", "https://mrkjai.com")
API_KEY = os.environ.get("MRKJAI_API_KEY", "").strip()
INGEST_URL = f"{API_BASE}/api/ingest/headroom"

# 模型定价（USD / 1K input tokens）
DEFAULT_PRICING = {
    "claude-sonnet-4": 0.015,
    "claude-opus-4": 0.075,
    "claude-haiku-4": 0.005,
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
    "gemini-2.0-flash": 0.000375,
}

# USD → CNY 汇率
USD_TO_CNY = 7.2


def get_api_key() -> str:
    """获取 API Key，支持环境变量或交互式输入"""
    key = API_KEY
    if not key:
        print("❌ 未找到 MRKJAI_API_KEY 环境变量")
        print("   请访问 https://mrkjai.com/tools/headroom-dashboard 登录后获取 API Key")
        print("   或从 /settings/integrations 页面复制")
        key = input("请输入你的 API Key（opc_user_...）：").strip()
        if not key:
            print("❌ API Key 不能为空，上报已取消")
            sys.exit(1)
    return key


def parse_headroom_perf(text: str) -> dict:
    """解析 headroom perf 的文本输出"""
    # headroom perf 输出格式示例：
    #   Session: abc123
    #   Original: 3245 tokens
    #   Compressed: 1298 tokens (40.0%)
    #   Model: claude-sonnet-4
    #   Time: 2026-06-21T10:23:01
    result = {}
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Original:"):
            m = re.search(r'(\d+)', line)
            if m:
                result["input_tokens"] = int(m.group(1))
        elif line.startswith("Compressed:"):
            m = re.search(r'(\d+)', line)
            if m:
                result["output_tokens"] = int(m.group(1))
            # 尝试提取百分比
            pct_match = re.search(r'\(([\d.]+)%\)', line)
            if pct_match:
                result["compression_rate"] = 1.0 - float(pct_match.group(1)) / 100.0
        elif line.startswith("Model:"):
            result["model"] = line.split(":", 1)[1].strip()
        elif line.startswith("Time:"):
            result["timestamp"] = line.split(":", 1)[1].strip()
    
    # 计算节省量
    if "input_tokens" in result and "output_tokens" in result:
        result["saved_tokens"] = result["input_tokens"] - result["output_tokens"]
    
    return result


def calculate_savings(input_tokens: int, output_tokens: int, model: str, pricing: Optional[float]) -> float:
    """计算节省金额（CNY）"""
    saved_tokens = input_tokens - output_tokens
    if pricing is None:
        pricing = DEFAULT_PRICING.get(model, 0.015)
    saved_usd = (saved_tokens / 1000) * pricing
    return saved_usd * USD_TO_CNY


def upload_single(event: dict, api_key: str) -> dict:
    """单条上报"""
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(INGEST_URL, json=event, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "code": "network_error", "error": str(e)}


def upload_batch(events: list, api_key: str) -> dict:
    """批量上报"""
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(INGEST_URL, json={"events": events}, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "code": "network_error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="headroom 压缩数据自动上报")
    parser.add_argument("--model", type=str, default="claude-sonnet-4", help="模型名称")
    parser.add_argument("--pricing", type=float, default=None, help="自定义定价（USD/1K tokens）")
    parser.add_argument("--input-tokens", type=int, default=None, help="原始输入 token 数")
    parser.add_argument("--output-tokens", type=int, default=None, help="压缩后输出 token 数")
    parser.add_argument("--saved-tokens", type=int, default=None, help="节省 token 数（可选，自动计算）")
    parser.add_argument("--saved-cny", type=float, default=None, help="节省金额 CNY（可选，自动计算）")
    parser.add_argument("--compression-rate", type=float, default=None, help="压缩率 0.0-1.0")
    parser.add_argument("--batch", type=str, default=None, help="批量上报 JSON 文件路径")
    parser.add_argument("--from-stdin", action="store_true", help="从 stdin 读取 headroom perf 输出")
    args = parser.parse_args()

    api_key = get_api_key()

    # 批量上报
    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            events = json.load(f)
        if not isinstance(events, list):
            print("❌ 批量文件必须是 JSON 数组")
            sys.exit(1)
        result = upload_batch(events, api_key)
        print(f"批量上报结果：{result}")
        return

    # 从 stdin 解析 headroom perf
    if args.from_stdin or (not args.input_tokens and not args.output_tokens):
        stdin_text = sys.stdin.read()
        if stdin_text.strip():
            parsed = parse_headroom_perf(stdin_text)
            if parsed:
                args.input_tokens = parsed.get("input_tokens", args.input_tokens)
                args.output_tokens = parsed.get("output_tokens", args.output_tokens)
                args.saved_tokens = parsed.get("saved_tokens", args.saved_tokens)
                args.compression_rate = parsed.get("compression_rate", args.compression_rate)
                args.model = parsed.get("model", args.model)

    # 校验必填字段
    if args.input_tokens is None or args.output_tokens is None:
        print("❌ 缺少 input-tokens 或 output-tokens")
        print("   用法1：headroom perf 2>&1 | python headroom_upload.py")
        print("   用法2：python headroom_upload.py --input-tokens 2840 --output-tokens 1820")
        sys.exit(1)

    # 计算节省量
    if args.saved_tokens is None:
        args.saved_tokens = args.input_tokens - args.output_tokens
    if args.saved_cny is None:
        args.saved_cny = calculate_savings(
            args.input_tokens, args.output_tokens, args.model, args.pricing
        )
    if args.compression_rate is None:
        args.compression_rate = 1.0 - args.output_tokens / args.input_tokens if args.input_tokens else 0

    # 组装事件
    event = {
        "model": args.model,
        "inputTokens": args.input_tokens,
        "outputTokens": args.output_tokens,
        "savedTokens": args.saved_tokens,
        "savedCny": round(args.saved_cny, 4),
        "compressionRate": round(args.compression_rate, 4),
    }

    # 上报
    print(f"📤 正在上报到 {INGEST_URL}...")
    result = upload_single(event, api_key)
    
    if result.get("ok"):
        print(f"✅ 上报成功！已节省 {args.saved_tokens} tokens（¥{args.saved_cny:.4f}）")
        print(f"   插入记录数：{result.get('inserted', 0)}")
    else:
        print(f"❌ 上报失败：{result.get('code', 'unknown')}")
        if result.get("error"):
            print(f"   详情：{result['error']}")


if __name__ == "__main__":
    main()
