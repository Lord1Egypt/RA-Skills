#!/usr/bin/env python3
"""
jisuai-auto: 配置 OpenClaw 对接 aicodee.com MiniMax 中转 API
"""

import json
import os
import sys
import argparse


OPENCLAW_PATH = r"C:\Users\Rice\.openclaw\openclaw.json"


def load_openclaw(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_openclaw(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def configure(base_url, api_key, provider_name="jisuaivauto", model_id="MiniMax-M2.7-highspeed"):
    data = load_openclaw(OPENCLAW_PATH)

    # 确保 models.providers 存在
    if "models" not in data:
        data["models"] = {}
    if "providers" not in data["models"]:
        data["models"]["providers"] = {}

    # 添加提供商配置
    provider_config = {
        "baseUrl": base_url,
        "apiKey": api_key,
        "api": "anthropic-messages",
        "models": [
            {
                "id": model_id,
                "name": f"{model_id} (Custom Provider)",
                "reasoning": False,
                "input": ["text"],
                "cost": {
                    "input": 0,
                    "output": 0,
                    "cacheRead": 0,
                    "cacheWrite": 0
                },
                "contextWindow": 130000,
                "maxTokens": 64000
            }
        ]
    }

    data["models"]["providers"][provider_name] = provider_config

    # 更新默认模型
    if "agents" not in data:
        data["agents"] = {}
    if "defaults" not in data["agents"]:
        data["agents"]["defaults"] = {}
    data["agents"]["defaults"]["model"] = {
        "primary": f"{provider_name}/{model_id}"
    }

    save_openclaw(OPENCLAW_PATH, data)
    print(f"[OK] configure done!")
    print(f"   provider: {provider_name}")
    print(f"   model: {provider_name}/{model_id}")
    print(f"   config file: {OPENCLAW_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="配置 OpenClaw MiniMax 中转 API")
    parser.add_argument("--base-url", required=True, help="API Base URL（必填）")
    parser.add_argument("--api-key", required=True, help="API Key（必填）")
    parser.add_argument("--provider-name", default="jisuaivauto", help="提供商名称")
    parser.add_argument("--model-id", default="MiniMax-M2.7-highspeed", help="模型 ID")

    args = parser.parse_args()
    configure(args.base_url, args.api_key, args.provider_name, args.model_id)
