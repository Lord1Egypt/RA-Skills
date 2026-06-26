#!/usr/bin/env python3
"""
MiniMax 文本生成脚本
支持 MiniMax-M2.7, MiniMax-M2.5, MiniMax-M2.1, MiniMax-M2 等模型
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("MINIMAX_API_KEY")
if not API_KEY:
    print("Error: MINIMAX_API_KEY environment variable not set")
    print("Please set it with: export MINIMAX_API_KEY=\"your-api-key\"")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
API_HOST = "https://api.minimaxi.com"


def chat(model: str, prompt: str, system: str = None, messages: list = None,
         think: int = 0, temperature: float = 0.7, max_tokens: int = 8192) -> str:
    """调用 MiniMax 文本生成 API"""
    url = f"{API_HOST}/v1/text/chatcompletion_v2"

    if messages is not None:
        msgs = messages
    else:
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": msgs,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if think:
        payload["thinking"] = {"type": "enabled", "budget_tokens": 18000}

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    if data.get("base_resp", {}).get("status_code") != 0:
        raise Exception(f"API Error: {data['base_resp']['status_msg']}")

    choices = data.get("choices", [])
    if choices:
        return choices[0].get("messages", [{}])[0].get("content", "")
    return ""


def main():
    parser = argparse.ArgumentParser(description="MiniMax 文本生成")
    parser.add_argument("--model", default="MiniMax-M2.7",
                        help="模型名称: MiniMax-M2.7, MiniMax-M2.5, MiniMax-M2.1, MiniMax-M2, MiniMax-M2.5-highspeed")
    parser.add_argument("--prompt", required=True, help="用户输入提示")
    parser.add_argument("--system", help="系统提示词")
    parser.add_argument("--messages", help="JSON 格式历史消息列表")
    parser.add_argument("--think", type=int, default=0, help="启用思考模型 (0/1)")
    parser.add_argument("--temperature", type=float, default=0.7, help="温度参数")
    parser.add_argument("--max-tokens", type=int, default=8192, help="最大输出 token 数")
    parser.add_argument("--output", help="输出文件路径（默认打印到 stdout）")

    args = parser.parse_args()

    msgs = None
    if args.messages:
        msgs = json.loads(args.messages)

    result = chat(
        model=args.model,
        prompt=args.prompt,
        system=args.system,
        messages=msgs,
        think=args.think,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ 结果已保存至 {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
