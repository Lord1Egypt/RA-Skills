#!/usr/bin/env python3
"""调用 OpenAI 兼容模型接口，将输入法口语文本整理成适合发送的自然书面语。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少 openai 依赖，请先安装 openai：pip install openai") from exc

DEFAULT_BASE_URL = os.environ.get("IME_MODEL_BASE_URL", "https://models.audiozen.cn/v1")
DEFAULT_MODEL_NAME = os.environ.get("IME_MODEL_NAME", "doubao-seed-2-0-lite-260215")
DEFAULT_API_KEY = os.environ.get("IME_MODEL_API_KEY", "")
DEFAULT_TEMPERATURE = float(os.environ.get("IME_MODEL_TEMPERATURE", "0.2"))
DEFAULT_TIMEOUT = float(os.environ.get("IME_MODEL_TIMEOUT", "30"))
DEFAULT_INSTRUCTION = (
    "将口语输入整理成适合即时通讯发送的自然书面语，保留原意，"
    "去掉语气词和重复，不要过度正式。"
)
SYSTEM_PROMPT = (
    "你是输入法语音消息书面化助手。"
    "你的任务是把输入法语音识别后的口语文本整理成适合即时通讯发送的自然书面语。"
    "保留原意和语气，去掉口头禅、重复和明显口误。"
    "不要扩写，不要总结，不要补充事实，不要解释过程。"
    "除非用户要求翻译，否则保持原语言。"
    "只输出最终文本，不要输出引号、说明或 JSON。"
)


def build_user_prompt(original_text: str, rewrite_instruction: str) -> str:
    return f"原文：{original_text}\n要求：{rewrite_instruction}"


def extract_text_from_response(response: Any) -> str:
    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, KeyError, TypeError) as exc:
        raise ValueError("无法从模型响应中提取文本，请检查响应格式") from exc

    if isinstance(content, str):
        text = content.strip()
        if text:
            return text

    if isinstance(content, list):
        parts = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                parts.append(text)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        text = "".join(parts).strip()
        if text:
            return text

    raise ValueError("模型返回了空内容")


def rewrite_text(
    original_text: str,
    rewrite_instruction: str = DEFAULT_INSTRUCTION,
    *,
    base_url: str = DEFAULT_BASE_URL,
    model_name: str = DEFAULT_MODEL_NAME,
    api_key: str = DEFAULT_API_KEY,
    temperature: float = DEFAULT_TEMPERATURE,
    timeout: float = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    if not original_text or not original_text.strip():
        raise ValueError("original_text 不能为空")
    if not api_key:
        raise ValueError("缺少 API token，请设置 IME_MODEL_API_KEY 或通过 --api-key 传入")

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(original_text, rewrite_instruction)},
        ],
        temperature=temperature,
        timeout=timeout,
    )
    rewritten_text = extract_text_from_response(response)
    return {
        "success": True,
        "base_url": base_url,
        "model": model_name,
        "rewritten_text": rewritten_text,
        "raw": response.model_dump(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将口语文本整理成适合发送消息的自然书面语")
    parser.add_argument("original_text", nargs="?", help="要处理的原始文本；未提供时从标准输入读取")
    parser.add_argument(
        "--instruction",
        default=DEFAULT_INSTRUCTION,
        help="改写指令，默认适用于即时通讯消息书面化",
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="模型服务基础地址，默认 https://models.audiozen.cn/v1")
    parser.add_argument("--model", default=DEFAULT_MODEL_NAME, help="模型名称")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="调用 token")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE, help="采样温度")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="请求超时时间（秒）")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    return parser.parse_args()


def read_original_text(args: argparse.Namespace) -> str:
    if args.original_text:
        return args.original_text
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("请提供 original_text 参数，或通过标准输入传入文本")


def main() -> None:
    args = parse_args()
    original_text = read_original_text(args)
    result = rewrite_text(
        original_text,
        args.instruction,
        base_url=args.base_url,
        model_name=args.model,
        api_key=args.api_key,
        temperature=args.temperature,
        timeout=args.timeout,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(result["rewritten_text"])


if __name__ == "__main__":
    main()
