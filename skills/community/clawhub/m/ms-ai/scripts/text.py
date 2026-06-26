#!/usr/bin/env python3
"""
ModelScope 生文脚本 — 支持多模型聊天/文本生成，Key + 模型双重轮换
用法:
  单轮: python3 text.py --prompt "解释量子计算"
  多轮: python3 text.py --prompt "继续" --history history.json
  指定模型: python3 text.py --prompt "你好" --model kimi
  流式: python3 text.py --prompt "写一首诗" --stream
"""

import argparse
import json
import os
import sys

import requests

from common import load_api_keys, make_headers, try_with_key_rotation

# ============ 配置 ============
BASE_URL = "https://api-inference.modelscope.cn/v1/"

# 生文模型（按优先级排列）
MODELS_TEXT = [
    "moonshotai/Kimi-K2.5",
    "ZhipuAI/GLM-5",
    "MiniMax/MiniMax-M2.5",
    "Qwen/Qwen3.5-397B-A17B",
    "XiaomiMiMo/MiMo-V2-Flash",
]

# 别名映射
ALIASES = {
    "kimi":     "moonshotai/Kimi-K2.5",
    "glm":      "ZhipuAI/GLM-5",
    "minimax":  "MiniMax/MiniMax-M2.5",
    "qwen":     "Qwen/Qwen3.5-397B-A17B",
    "mimo":     "XiaomiMiMo/MiMo-V2-Flash",
}


def stream_response(resp) -> str:
    full_text = ""
    for line in resp.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8")
        if line.startswith("data: "):
            data = line[6:]
            if data.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(data)
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    print(content, end="", flush=True)
                    full_text += content
            except json.JSONDecodeError:
                continue
    print()
    return full_text


def _chat_one(api_key: str, model: str, messages: list, max_tokens: int,
              temperature: float, stream: bool) -> dict:
    """尝试用指定 key + model 调用聊天接口"""
    headers = make_headers(api_key)
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }

    try:
        resp = requests.post(
            f"{BASE_URL}chat/completions",
            headers=headers, json=payload, timeout=120, stream=stream,
        )

        if resp.status_code == 429:
            return {"status": "rate_limit"}
        elif resp.status_code != 200:
            return {"status": "error", "error": f"{resp.status_code}: {resp.text[:200]}"}

        if stream:
            print(f"    💬 ", end="", file=sys.stderr)
            content = stream_response(resp)
            return {
                "status": "success", "model": model, "content": content,
                "messages": messages + [{"role": "assistant", "content": content}],
            }
        else:
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            usage = data.get("usage", {})
            return {
                "status": "success", "model": model, "content": content,
                "usage": usage,
                "messages": messages + [{"role": "assistant", "content": content}],
            }

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            return {"status": "rate_limit"}
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="ModelScope 生文 — 多模型聊天，Key + 模型双重轮换",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt", required=True, help="用户输入")
    parser.add_argument("--model", default=None, help="指定模型（别名或完整ID）")
    parser.add_argument("--max-tokens", type=int, default=4096, help="最大输出 token 数")
    parser.add_argument("--temperature", type=float, default=0.7, help="温度（0-2）")
    parser.add_argument("--stream", action="store_true", help="流式输出")
    parser.add_argument("--history", default=None, help="历史消息 JSON 文件路径")
    parser.add_argument("--output", default=None, help="保存完整对话到 JSON 文件")
    args = parser.parse_args()

    keys = load_api_keys()

    messages = []
    if args.history and os.path.isfile(args.history):
        with open(args.history, "r", encoding="utf-8") as f:
            messages = json.load(f)
        print(f"📜 加载历史: {len(messages)} 条消息", file=sys.stderr)
    messages.append({"role": "user", "content": args.prompt})

    if args.model:
        specified = ALIASES.get(args.model, args.model)
        model_list = [specified] + [m for m in MODELS_TEXT if m != specified]
        print(f"📌 指定模型: {specified}", file=sys.stderr)
    else:
        model_list = MODELS_TEXT

    print(f"🔑 API Keys: {len(keys)} 个", file=sys.stderr)
    print(f"🤖 模型: {len(model_list)} 个", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    def _wrapper(api_key, model):
        return _chat_one(api_key, model, messages, args.max_tokens, args.temperature, args.stream)

    try:
        # 流式模式下直接换行输出
        if args.stream:
            print("", file=sys.stderr)

        result = try_with_key_rotation(_wrapper, model_list, keys)

        if not args.stream:
            usage = result.get("usage", {})
            print(f"\n{'='*50}", file=sys.stderr)
            print(f"  ✅ 成功（{usage.get('total_tokens', '?')} tokens）", file=sys.stderr)
            print(result["content"])

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result["messages"], f, ensure_ascii=False, indent=2)
            print(f"\n💾 对话已保存: {args.output}", file=sys.stderr)

    except Exception as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
