#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCode Free Models - 自动配置 opencode.ai 免费模型到 OpenClaw/QClaw
"""

import json
import os
import ssl
import urllib.request
import urllib.error
from pathlib import Path


OPENCLAW_PATH = Path.home() / ".openclaw" / "openclaw.json"
QCLAW_PATH = Path.home() / ".qclaw" / "openclaw.json"
OPENCODEL_API = "https://opencode.ai/zen/v1/models"


def get_models_file():
    """获取配置文件路径"""
    if OPENCLAW_PATH.exists():
        return OPENCLAW_PATH
    elif QCLAW_PATH.exists():
        return QCLAW_PATH
    else:
        return OPENCLAW_PATH


def fetch_free_models():
    """从 opencode.ai 获取免费模型"""
    try:
        req = urllib.request.Request(OPENCODEL_API)
        req.add_header("User-Agent", "OpenClaw-Free-Models/1.0")
        
        context = ssl.create_default_context()
        
        with urllib.request.urlopen(req, timeout=10, context=context) as response:
            data = json.loads(response.read().decode("utf-8"))
        
        free_models = []
        for m in data.get("data", []):
            model_id = m.get("id", "")
            if "free" in model_id.lower():
                free_models.append({
                    "id": model_id,
                    "name": m.get("name", model_id),
                    "reasoning": m.get("reasoning", False),
                    "input": m.get("input", ["text"]),
                    "contextWindow": m.get("max_tokens", 131072),
                    "maxTokens": 8192,
                    "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
                })
        
        return free_models
    
    except Exception as e:
        print(f"❌ 获取模型失败: {e}")
        return []


def load_config(config_file):
    """加载现有配置"""
    if not config_file.exists():
        return {"models": {"providers": {}}}
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        return {"models": {"providers": {}}}


def save_config(config_file, config):
    """保存配置"""
    try:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ 配置已保存: {config_file}")
        return True
    except Exception as e:
        print(f"❌ 保存配置失败: {e}")
        return False


def add_models(config_file, free_models):
    """添加免费模型到配置"""
    config = load_config(config_file)
    
    if "models" not in config:
        config["models"] = {}
    if "providers" not in config["models"]:
        config["models"]["providers"] = {}
    
    provider_key = "opencode-free"
    if provider_key not in config["models"]["providers"]:
        config["models"]["providers"][provider_key] = {
            "baseUrl": "https://opencode.ai/zen/v1",
            "apiKey": "public",
            "api": "openai-completions",
            "models": []
        }
    
    existing_ids = {m["id"] for m in config["models"]["providers"][provider_key].get("models", [])}
    
    added_count = 0
    for model in free_models:
        if model["id"] not in existing_ids:
            config["models"]["providers"][provider_key]["models"].append(model)
            added_count += 1
            print(f"✅ 添加: {model['id']}")
    
    if added_count > 0:
        save_config(config_file, config)
    
    return added_count


def main():
    print("=" * 50)
    print("OpenCode Free Models 配置工具")
    print("=" * 50)
    
    config_file = get_models_file()
    print(f"📁 配置文件: {config_file}")
    
    print("🔍 正在查询 opencode.ai 免费模型...")
    free_models = fetch_free_models()
    
    if not free_models:
        print("❌ 未找到免费模型")
        return 1
    
    print(f"✅ 找到 {len(free_models)} 个免费模型:")
    for m in free_models:
        print(f"   - {m['id']}")
    
    added = add_models(config_file, free_models)
    print(f"\n✨ 新增模型: {added}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())