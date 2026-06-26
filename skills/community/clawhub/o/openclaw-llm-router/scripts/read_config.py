#!/usr/bin/env python3
"""
read_config.py — 读取 OpenClaw 本地配置，输出已激活模型及三档套餐归类
用法：python scripts/read_config.py
"""
import json, os, urllib.request
from pathlib import Path

CONFIG_PATHS = [
    Path.home() / ".openclaw" / "openclaw.json",
    Path.home() / ".openclaw" / "models.json",
    Path.home() / ".clawdbot" / "clawdbot.json",
    Path.cwd() / "openclaw.json",
]

PROVIDER_KEYS = {
    "anthropic": ["ANTHROPIC_API_KEY", "ANTHROPIC_API_KEYS"],
    "openai": ["OPENAI_API_KEY"],
    "openai-codex": [],   # OAuth，检测 token 文件
    "google": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
    "deepseek": ["DEEPSEEK_API_KEY"],
    "xai": ["XAI_API_KEY"],
    "moonshot": ["MOONSHOT_API_KEY"],
    "minimax": ["MINIMAX_API_KEY"],
    "zai": ["ZAI_API_KEY"],
    "openrouter": ["OPENROUTER_API_KEY"],
    "kilocode": ["KILOCODE_API_KEY"],
    "mistral": ["MISTRAL_API_KEY"],
}

# 三档套餐映射（按 provider 细分）
TIER_MAP = {
    "premium": {
        "anthropic": ["claude-opus-4-6"],
        "openai": ["gpt-5.1-codex", "gpt-5.4"],
        "openai-codex": ["gpt-5.3-codex"],
        "google": ["gemini-3.1-pro-preview", "gemini-3-pro-preview", "gemini-2.5-pro"],
        "xai": ["grok-4.20", "grok-4"],
        "moonshot": ["kimi-k2.5"],
        "mistral": ["mistral-large-2"],
    },
    "balanced": {
        "anthropic": ["claude-sonnet-4-6", "claude-sonnet-4-5"],
        "openai": ["gpt-4o", "gpt-5.2"],
        "google": ["gemini-3-flash-preview", "gemini-2.5-pro", "gemini-2.5-flash"],
        "xai": ["grok-4-fast", "grok-4.1-fast", "grok-code-fast"],
        "deepseek": ["deepseek-r1", "deepseek-v3.2", "deepseek-v3.1"],
        "moonshot": ["kimi-k2"],
        "minimax": ["m2.5", "m2.1"],
        "zai": ["glm-5", "glm-4.7"],
        "qwen": ["qwen3-max", "qwen3-coder", "qwen3.5-397b"],
        "ollama": ["llama-3.3-70b", "qwen3-coder", "mistral-large"],
    },
    "economy": {
        "anthropic": ["claude-haiku-4-5", "claude-haiku-3-5"],
        "openai": ["gpt-4o-mini", "gpt-4.1-mini"],
        "google": ["gemini-3.1-flash-lite-preview", "gemini-2.5-flash", "gemini-2.0-flash"],
        "xai": ["grok-4.1-mini", "grok-3-mini", "grok-3-mini-fast"],
        "deepseek": ["deepseek-v3.2", "deepseek-v3"],
        "minimax": ["m2.5-lightning", "m2.1-lightning"],
        "zai": ["glm-4.7-flash"],
        "kilocode": ["glm-5-free", "minimax-m2.5-free"],
        "qwen": ["qwen3-coder-plus", "qwen2.5-coder-32b"],
        "ollama": ["llama-3.2-3b", "llama-3.1-8b", "deepseek-coder-v2", "qwen2.5-coder-7b"],
    }
}

def load_config():
    env_path = os.environ.get("OPENCLAW_CONFIG")
    if env_path:
        CONFIG_PATHS.insert(0, Path(env_path))
    for p in CONFIG_PATHS:
        if p.exists():
            try:
                return json.loads(p.read_text()), str(p)
            except Exception as e:
                print(f"  ⚠️  读取失败 {p}: {e}")
    return {}, None

def detect_active_providers(config):
    env = config.get("env", {})
    active = []
    for provider, keys in PROVIDER_KEYS.items():
        for k in keys:
            if env.get(k) or os.environ.get(k):
                active.append(provider)
                break
    # 检测 Ollama
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        active.append("ollama")
    except:
        pass
    return active

def get_allowlist(config):
    models_cfg = config.get("agents", {}).get("defaults", {}).get("models", {})
    return list(models_cfg.keys()) if models_cfg else None

def classify_to_tiers(active_providers, allowlist=None):
    result = {"premium": [], "balanced": [], "economy": []}
    for tier, providers in TIER_MAP.items():
        for provider, models in providers.items():
            if provider not in active_providers:
                continue
            for model in models:
                full_id = f"{provider}/{model}"
                if allowlist and full_id not in allowlist:
                    continue
                result[tier].append(full_id)
    return result

def main():
    print("\n🦞 OpenClaw LLM Router — 配置读取")
    print("━" * 45)
    config, path = load_config()
    if not path:
        print("❌ 未找到 OpenClaw 配置文件")
        print("   请先运行: openclaw onboard")
        return
    print(f"✅ 配置文件: {path}")
    active = detect_active_providers(config)
    allowlist = get_allowlist(config)
    tiers = classify_to_tiers(active, allowlist)
    print(f"\n已激活 Providers（{len(active)}）: {', '.join(active)}")
    if allowlist:
        print(f"模型 Allowlist 限制（{len(allowlist)} 个）")
    tier_labels = {"premium": "🏆 高质量", "balanced": "⚖️ 平衡", "economy": "💰 经济"}
    for tier, label in tier_labels.items():
        models = tiers[tier]
        print(f"\n{label} 套餐（{len(models)} 个可用）:")
        for m in models[:8]:
            print(f"  • {m}")
        if len(models) > 8:
            print(f"  ... 共 {len(models)} 个")
    print("\n" + "━" * 45)
    current = config.get("agents", {}).get("defaults", {}).get("model", {})
    if current:
        print(f"当前默认模型: {current.get('primary', '未设置')}")

if __name__ == "__main__":
    main()
