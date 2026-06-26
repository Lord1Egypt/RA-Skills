#!/usr/bin/env python3
"""
ModelScope 视觉理解脚本 — 支持图片分析，Key + 模型双重轮换
用法:
  python3 vision.py --image photo.jpg --prompt "描述这张图片"
  python3 vision.py --image photo.jpg --prompt "图片里有什么文字？"
  cat image.b64 | python3 vision.py --prompt "分析图片" --stdin-b64
"""

import argparse
import base64
import json
import os
import sys

import requests

from common import load_api_keys, make_headers, try_with_key_rotation

# ============ 配置 ============
BASE_URL = "https://api-inference.modelscope.cn/"

# 视觉理解模型（按优先级排列）
MODELS_VISION = [
    "moonshotai/Kimi-K2.5",
    "ZhipuAI/GLM-5",
    "MiniMax/MiniMax-M2.5",
    "Qwen/Qwen3.5-397B-A17B",
]

# 别名映射
ALIASES = {
    "kimi":     "moonshotai/Kimi-K2.5",
    "glm":      "ZhipuAI/GLM-5",
    "minimax":  "MiniMax/MiniMax-M2.5",
    "qwen":     "Qwen/Qwen3.5-397B-A17B",
}


def encode_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    ext = os.path.splitext(image_path)[1].lower()
    mime = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif",
        ".webp": "image/webp", ".bmp": "image/bmp",
    }.get(ext, "image/png")
    return f"data:{mime};base64,{data}"


def _call_vision(api_key: str, model: str, prompt: str, image_b64: str) -> dict:
    """尝试用指定 key + model 调用视觉 API"""
    headers = make_headers(api_key)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_b64}},
                    {"type": "text", "text": prompt}
                ]
            }
        ],
        "max_tokens": 4096,
    }

    try:
        resp = requests.post(f"{BASE_URL}v1/chat/completions", headers=headers, json=payload, timeout=120)

        if resp.status_code == 429:
            return {"status": "rate_limit"}
        elif resp.status_code != 200:
            return {"status": "error", "error": f"{resp.status_code}: {resp.text[:200]}"}

        data = resp.json()
        choices = data.get("choices")
        if not choices or not isinstance(choices, list) or len(choices) == 0:
            return {"status": "error", "error": f"API返回格式异常: {json.dumps(data, ensure_ascii=False)[:200]}"}

        content = choices[0].get("message", {}).get("content", "")
        if not content:
            return {"status": "error", "error": f"返回内容为空"}

        return {"status": "success", "content": content, "model": model}

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            return {"status": "rate_limit"}
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="ModelScope 视觉理解 — Key + 模型双重轮换")
    parser.add_argument("--image", "-i", help="输入图片路径")
    parser.add_argument("--prompt", "-p", required=True, help="分析提示词")
    parser.add_argument("--model", "-m", help="指定模型（别名或完整ID）")
    parser.add_argument("--stdin-b64", action="store_true", help="从 stdin 读取 base64 图片")
    parser.add_argument("--output", "-o", help="输出文件路径（可选）")
    args = parser.parse_args()

    keys = load_api_keys()

    # 获取图片 base64
    if args.stdin_b64:
        raw = sys.stdin.read().strip()
        image_b64 = raw if raw.startswith("data:") else f"data:image/png;base64,{raw}"
    elif args.image:
        if not os.path.exists(args.image):
            print(f"❌ 图片不存在: {args.image}", file=sys.stderr)
            sys.exit(1)
        image_b64 = encode_image_base64(args.image)
    else:
        print("❌ 需要 --image 或 --stdin-b64", file=sys.stderr)
        sys.exit(1)

    if args.model:
        model_id = ALIASES.get(args.model.lower(), args.model)
        model_list = [model_id]
    else:
        model_list = MODELS_VISION[:]

    print(f"👁️  视觉理解", file=sys.stderr)
    print(f"💬 提示词: {args.prompt}", file=sys.stderr)
    print(f"🔑 API Keys: {len(keys)} 个", file=sys.stderr)
    print(f"🤖 模型: {' → '.join(model_list)}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    try:
        result = try_with_key_rotation(
            _call_vision, model_list, keys, args.prompt, image_b64,
        )
        output = {
            "status": "success",
            "model": result.get("model"),
            "prompt": args.prompt,
            "content": result["content"],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result["content"])
            print(f"\n📄 结果已保存到: {args.output}", file=sys.stderr)

    except Exception as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
