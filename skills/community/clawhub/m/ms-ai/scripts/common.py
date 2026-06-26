#!/usr/bin/env python3
"""
共享工具模块 — API Key 轮换 + 模型轮换
"""

import os
import sys
import time
import json
import requests


def load_api_keys() -> list:
    """从环境变量读取 API Key（支持逗号分隔多个）"""
    raw = os.environ.get("MODELSCOPE_API_KEY", "")
    if not raw:
        print("❌ 未设置 MODELSCOPE_API_KEY", file=sys.stderr)
        print("   配置方式: openclaw.json → skills.entries.ms-ai.env.MODELSCOPE_API_KEY", file=sys.stderr)
        print("   多个 key 用逗号分隔: key1,key2,key3", file=sys.stderr)
        sys.exit(1)
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    return keys if keys else [raw.strip()]


def make_headers(api_key: str) -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def try_with_key_rotation(func, model_list: list, keys: list, *args, **kwargs):
    """
    通用 key + model 轮换封装
    
    轮换策略: 先换 key，每个 key 试完所有模型，再换下一个 key
    总共最多尝试 n_keys × n_models 次
    
    func(api_key, model, *args, **kwargs) -> dict
      返回 {"status": "success", ...} 表示成功
      返回 {"status": "rate_limit"} 表示限速
      返回 {"status": "error", "error": "..."} 表示失败
    """
    RATE_LIMIT_WAIT = 10

    total_keys = len(keys)
    total_models = len(model_list)

    for key_idx, api_key in enumerate(keys):
        key_label = f"Key{key_idx+1}/{total_keys} ({api_key[:12]}...)"
        print(f"\n🔑 使用 {key_label}", file=sys.stderr)

        for model_idx, model in enumerate(model_list):
            model_label = f"模型 {model_idx+1}/{total_models}: {model}"
            print(f"  🤖 尝试 {model_label}", file=sys.stderr)

            try:
                result = func(api_key, model, *args, **kwargs)

                if result.get("status") == "success":
                    result["key_index"] = key_idx
                    return result
                elif result.get("status") == "rate_limit":
                    print(f"  ⏳ 限速，等待 {RATE_LIMIT_WAIT}s 换下一个模型...", file=sys.stderr)
                    time.sleep(RATE_LIMIT_WAIT)
                    continue
                else:
                    print(f"  ❌ 错误: {result.get('error', 'unknown')}", file=sys.stderr)
                    continue

            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 429:
                    print(f"  ⚠️ 限速 (429)，等待 {RATE_LIMIT_WAIT}s 换下一个模型...", file=sys.stderr)
                    time.sleep(RATE_LIMIT_WAIT)
                    continue
                else:
                    print(f"  ❌ 请求错误: {e}", file=sys.stderr)
                    continue

            except Exception as e:
                print(f"  ❌ 失败: {e}", file=sys.stderr)
                continue

        # 当前 key 的所有模型都失败，换下一个 key
        if key_idx < total_keys - 1:
            print(f"\n  🔄 {key_label} 所有模型都失败，切换到下一个 Key...", file=sys.stderr)

    raise Exception(f"所有 Key × 所有模型都失败！共尝试 {total_keys} 个 Key × {total_models} 个模型")
