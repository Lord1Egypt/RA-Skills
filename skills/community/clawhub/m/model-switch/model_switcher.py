#!/usr/bin/env python3
"""
model-switcher — 模型切换与管理工具（增强版 v3）

支持：
  switch <agent> <model>          — 切换单个 Agent 模型
  switch ALL <model>              — 批量切换所有 Agent
  add <provider> <model>          — 添加新模型到白名单
  remove <provider> <model>       — 从白名单移除模型
  list                            — 列出所有可用模型
  list-providers                  — 列出所有 provider 及 API key 状态
  compare                         — 模型对比（成本/速度/能力）
  diagnose                        — 诊断当前模型配置问题
  show                            — 显示当前会话模型状态
  reset                           — 清除所有 model override，回退默认

触发词：切换模型、换模型、model switch、model add、model list 等
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
HOME = Path.home()

# ── Provider → 环境变量映射（支持扩展） ──
PROVIDER_KEY_MAP = {
    "sensenova": "SENSENOVA_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "minimax": "MINIMAX_API_KEY",
    "xiaomi-coding": "MIMO_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "groq": "GROQ_API_KEY",
    "ollama": None,  # 本地模型，无 API key
    "lmstudio": None,
}

# ── 模型能力/成本参考（可扩展） ──
MODEL_PROFILE = {
    "sensenova/sensenova-6.7-flash-lite": {"tier": "L4", "cost": "极低", "speed": "快", "reasoning": "弱", "use": "日常调度、闲聊"},
    "sensenova/sensenova-u1-fast":        {"tier": "L4", "cost": "最低", "speed": "最快", "reasoning": "弱", "use": "自动化、规则匹配"},
    "sensenova/deepseek-v4-flash":        {"tier": "L2", "cost": "低", "speed": "中", "reasoning": "中", "use": "后端开发、批量处理"},
    "deepseek/deepseek-v4-pro":           {"tier": "L1", "cost": "中", "speed": "慢", "reasoning": "强", "use": "复杂推理、代码审查"},
    "minimax/MiniMax-M2.7-highspeed":     {"tier": "L3", "cost": "低", "speed": "快", "reasoning": "中", "use": "创意内容、文案"},
    "xiaomi-coding/mimo-v2.5-pro":        {"tier": "L1", "cost": "中", "speed": "中", "reasoning": "强", "use": "深度分析、战略"},
    "openai/gpt-4o":                      {"tier": "L1", "cost": "高", "speed": "中", "reasoning": "强", "use": "通用最强"},
    "openai/gpt-4o-mini":                 {"tier": "L3", "cost": "低", "speed": "快", "reasoning": "中", "use": "轻量任务"},
    "openai/gpt-5":                       {"tier": "L1", "cost": "高", "speed": "中", "reasoning": "极强", "use": "最复杂推理"},
    "anthropic/claude-3-7-sonnet":        {"tier": "L1", "cost": "高", "speed": "慢", "reasoning": "极强", "use": "代码、推理"},
    "anthropic/claude-3-5-haiku":         {"tier": "L3", "cost": "低", "speed": "快", "reasoning": "中", "use": "快速响应"},
    "google/gemini-2-5-pro":              {"tier": "L1", "cost": "高", "speed": "中", "reasoning": "强", "use": "多模态、长上下文"},
    "google/gemini-2-5-flash":            {"tier": "L2", "cost": "中", "speed": "快", "reasoning": "中", "use": "性价比平衡"},
    "groq/llama-3-3-70b":                 {"tier": "L2", "cost": "极低", "speed": "极快", "reasoning": "中", "use": "极速推理"},
    "ollama/llama3":                      {"tier": "L2", "cost": "免费", "speed": "取决于硬件", "reasoning": "中", "use": "本地离线"},
    "ollama/qwen2-5-72b":                 {"tier": "L2", "cost": "免费", "speed": "取决于硬件", "reasoning": "强", "use": "本地中文"},
}


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get_env_key(provider):
    return PROVIDER_KEY_MAP.get(provider)


def check_api_key(provider):
    """检查 provider 的 API key 是否配置（环境变量 + config）"""
    env_key = get_env_key(provider)
    env_val = os.environ.get(env_key, "") if env_key else ""
    
    cfg = load_config()
    prov_cfg = cfg.get("models", {}).get("providers", {}).get(provider, {})
    config_key = prov_cfg.get("apiKey", "")
    
    env_ok = bool(env_val)
    config_ok = bool(config_key)
    
    return {
        "provider": provider,
        "env_var": env_key,
        "env_set": env_ok,
        "config_set": config_ok,
        "ready": env_ok and config_ok,
    }


# ── 命令实现 ──

def cmd_switch(agent_id, target_model):
    """切换模型（4 层同步）"""
    print(f"\n🔧 Model Switcher v3 — 切换: {target_model}")
    print("=" * 50)
    
    # 解析 provider
    parts = target_model.split("/", 1)
    if len(parts) != 2:
        print(f"❌ 模型格式错误: 应为 'provider/model-name'，如 'openai/gpt-4o'")
        sys.exit(1)
    provider, short_name = parts
    auth_profile = f"{provider}:default"
    
    # Step 1: 验证/添加白名单
    print(f"\n📋 Step 1: 白名单检查...")
    cfg = load_config()
    models_dict = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    
    # models 可能是 dict (key=model_name) 或 list
    if isinstance(models_dict, dict):
        models_keys = set(models_dict.keys())
        is_list_style = False
    else:
        models_keys = set(models_dict)
        is_list_style = True
    
    if target_model not in models_keys:
        print(f"   ⚠️  {target_model} 不在白名单，正在添加...")
        if is_list_style:
            models_dict.append(target_model)
        else:
            models_dict[target_model] = {}
        cfg["agents"]["defaults"]["models"] = models_dict
        print(f"   ✅ 已添加到白名单")
    else:
        print(f"   ✅ 已在白名单中")
    
    # Step 2: 检查 API key
    print(f"\n🔑 Step 2: API key 检查...")
    key_status = check_api_key(provider)
    
    if not key_status["ready"]:
        print(f"   ⚠️  Provider '{provider}' 的 API key 未完全配置:")
        if not key_status["env_set"]:
            print(f"      - 环境变量 {key_status['env_var']} 未设置")
        if not key_status["config_set"]:
            print(f"      - models.providers.{provider}.apiKey 未配置")
        print(f"\n   💡 修复方法:")
        if key_status["env_var"]:
            print(f"      export {key_status['env_var']}='your-api-key'")
        print(f"      然后运行: model-switcher add-key {provider}")
        sys.exit(1)
    
    print(f"   ✅ API key 已配置")
    
    # Step 3: 更新 auth-profiles.json
    print(f"\n🔐 Step 3: 更新 auth-profiles.json...")
    agents_to_update = []
    if agent_id == "ALL":
        agents_to_update = [a["id"] for a in cfg.get("agents", {}).get("list", [])]
    else:
        agents_to_update = [agent_id]
    
    for aid in agents_to_update:
        apf_path = HOME / ".openclaw" / "agents" / aid / "agent" / "auth-profiles.json"
        if not apf_path.exists():
            print(f"   ⚠️  {aid}: auth-profiles.json 不存在，跳过")
            continue
        
        with open(apf_path) as f:
            apf = json.load(f)
        
        if auth_profile not in apf.get("profiles", {}):
            apf.setdefault("profiles", {})[auth_profile] = {
                "type": "api_key",
                "provider": provider,
                "key": cfg["models"]["providers"][provider].get("apiKey", "")
            }
            print(f"   ✅ {aid}: 添加 {auth_profile}")
        else:
            # 确保 key 是最新的
            apf["profiles"][auth_profile]["key"] = cfg["models"]["providers"][provider].get("apiKey", "")
            apf["profiles"][auth_profile]["provider"] = provider
            print(f"   ✅ {aid}: 更新 {auth_profile}")
        
        # 原子写入：先写临时文件，再 rename
        _atomic_write_json(apf_path, apf)
    
    # Step 4: 更新 openclaw.json
    print(f"\n✏️  Step 4: 更新 openclaw.json...")
    found = False
    for agent in cfg.get("agents", {}).get("list", []):
        if agent["id"] == agent_id or agent_id == "ALL":
            old = agent.get("model", "NOT SET")
            agent["model"] = target_model
            print(f"   {agent['id']}: {old} → {target_model}")
            found = True
    
    if agent_id == "ALL":
        old_default = cfg["agents"]["defaults"]["model"]["primary"]
        cfg["agents"]["defaults"]["model"]["primary"] = target_model
        print(f"   default: {old_default} → {target_model}")
    elif not found:
        print(f"   ❌ Agent '{agent_id}' 不在配置中")
        sys.exit(1)
    
    save_config(cfg)
    
    # Step 5: 总结
    print(f"\n{'=' * 50}")
    print(f"✅ 配置已更新！")
    print(f"\n   最后一步（在当前会话执行）:")
    print(f"   session_status(model=\"{target_model}\")")
    print(f"\n   或清除覆盖回退默认:")
    print(f"   session_status(model=\"default\")")
    print(f"{'=' * 50}\n")


def cmd_add(provider, model_name):
    """添加新模型到白名单"""
    full_model = f"{provider}/{model_name}"
    print(f"\n➕ 添加模型: {full_model}")
    
    cfg = load_config()
    models_dict = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    
    # models 可能是 dict 或 list
    if isinstance(models_dict, dict):
        models_keys = set(models_dict.keys())
        is_list_style = False
    else:
        models_keys = set(models_dict)
        is_list_style = True
    
    if full_model in models_keys:
        print(f"   ⚠️  已存在，跳过")
        return
    
    if is_list_style:
        models_dict.append(full_model)
    else:
        models_dict[full_model] = {}
    cfg["agents"]["defaults"]["models"] = models_dict
    save_config(cfg)
    print(f"   ✅ 已添加到白名单")
    
    # 检查 provider 配置
    providers = cfg.get("models", {}).get("providers", {})
    if provider not in providers:
        print(f"   ⚠️  Provider '{provider}' 未配置，需要:")
        print(f"      1. 在 openclaw.json 中添加 models.providers.{provider}")
        print(f"      2. 设置环境变量: export {get_env_key(provider)}='your-key'")
    else:
        key_status = check_api_key(provider)
        if key_status["ready"]:
            print(f"   ✅ Provider 配置完整")
        else:
            print(f"   ⚠️  Provider 配置不完整，API key 缺失")


def cmd_remove(provider, model_name):
    """从白名单移除模型"""
    full_model = f"{provider}/{model_name}"
    print(f"\n➖ 移除模型: {full_model}")
    
    cfg = load_config()
    models_dict = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    
    # models 可能是 dict 或 list
    if isinstance(models_dict, dict):
        models_keys = set(models_dict.keys())
        is_list_style = False
    else:
        models_keys = set(models_dict)
        is_list_style = True
    
    if full_model not in models_keys:
        print(f"   ⚠️  不在白名单中，跳过")
        return
    
    if is_list_style:
        models_dict.remove(full_model)
    else:
        del models_dict[full_model]
    cfg["agents"]["defaults"]["models"] = models_dict
    save_config(cfg)
    print(f"   ✅ 已从白名单移除")


def cmd_list():
    """列出所有可用模型"""
    cfg = load_config()
    models_raw = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    # 兼容 dict 和 list
    models = list(models_raw.keys()) if isinstance(models_raw, dict) else models_raw
    
    print(f"\n📋 可用模型列表 ({len(models)} 个):")
    print("-" * 50)
    for m in models:
        parts = m.split("/", 1)
        provider = parts[0]
        short = parts[1] if len(parts) > 1 else m
        profile = MODEL_PROFILE.get(m, {})
        tier = profile.get("tier", "?")
        cost = profile.get("cost", "?")
        use = profile.get("use", "?")
        print(f"  {m}")
        print(f"    Tier: {tier} | 成本: {cost} | 用途: {use}")
    
    print()


def cmd_list_providers():
    """列出所有 provider 及 API key 状态"""
    cfg = load_config()
    providers = cfg.get("models", {}).get("providers", {})
    
    print(f"\n🔑 Provider API Key 状态:")
    print("-" * 50)
    for prov in providers:
        status = check_api_key(prov)
        icon = "✅" if status["ready"] else "❌"
        print(f"  {icon} {prov}")
        if status["env_var"]:
            print(f"      环境变量: {status['env_var']} → {'已设置' if status['env_set'] else '未设置'}")
        if status["config_set"]:
            print(f"      config apiKey: 已配置")
        elif not status["config_set"] and status["env_set"]:
            print(f"      ⚠️  环境变量有值但 config 中未配置，建议运行: model-switcher add-key {prov}")


def cmd_compare():
    """模型对比"""
    print(f"\n📊 模型能力对比:")
    print("=" * 70)
    print(f"  {'模型':<40} {'Tier':<5} {'成本':<8} {'速度':<6} {'推理':<6} {'用途'}")
    print("-" * 70)
    
    cfg = load_config()
    models_raw = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    models = list(models_raw.keys()) if isinstance(models_raw, dict) else models_raw
    
    for m in sorted(models):
        profile = MODEL_PROFILE.get(m, {"tier": "?", "cost": "?", "speed": "?", "reasoning": "?", "use": "未知"})
        print(f"  {m:<40} {profile['tier']:<5} {profile['cost']:<8} {profile['speed']:<6} {profile['reasoning']:<6} {profile['use']}")
    
    print()


def cmd_diagnose():
    """诊断当前模型配置问题"""
    cfg = load_config()
    issues = []
    
    # 检查 1: 默认模型是否在白名单
    default_model = cfg.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
    models_raw = cfg.get("agents", {}).get("defaults", {}).get("models", {})
    models_keys = set(models_raw.keys()) if isinstance(models_raw, dict) else set(models_raw)
    if default_model and default_model not in models_keys:
        issues.append(f"❌ 默认模型 '{default_model}' 不在白名单中")
    
    # 检查 2: 每个 Agent 的模型
    for agent in cfg.get("agents", {}).get("list", []):
        aid = agent["id"]
        model = agent.get("model")
        if model and model not in models_keys:
            issues.append(f"❌ Agent '{aid}' 的模型 '{model}' 不在白名单中")
    
    # 检查 3: Provider API key
    for prov in cfg.get("models", {}).get("providers", {}):
        status = check_api_key(prov)
        if not status["ready"]:
            issues.append(f"❌ Provider '{prov}' API key 不完整 (env: {status['env_set']}, config: {status['config_set']})")
    
    # 检查 4: auth-profiles 完整性
    for agent in cfg.get("agents", {}).get("list", []):
        aid = agent["id"]
        model = agent.get("model", "")
        if model:
            provider = model.split("/")[0]
            apf_path = HOME / ".openclaw" / "agents" / aid / "agent" / "auth-profiles.json"
            if apf_path.exists():
                with open(apf_path) as f:
                    apf = json.load(f)
                auth_profile = f"{provider}:default"
                if auth_profile not in apf.get("profiles", {}):
                    issues.append(f"⚠️  Agent '{aid}' 缺少 auth-profile '{auth_profile}'")
    
    print(f"\n🔍 模型配置诊断:")
    print("=" * 50)
    if not issues:
        print("   ✅ 所有检查通过，配置正常")
    else:
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    print()


def cmd_show():
    """显示当前会话模型状态（通过调用 session_status）"""
    print(f"\n📊 当前会话模型状态:")
    print("=" * 50)
    print("   请在当前会话执行:")
    print("   session_status")
    print()


def cmd_reset():
    """清除 model override，回退默认"""
    print(f"\n🔄 清除 model override，回退默认模型...")
    print("   请在当前会话执行:")
    print("   session_status(model=\"default\")")
    print()


def cmd_add_key(provider):
    """从环境变量添加 provider API key 到 config"""
    print(f"\n🔑 添加 provider '{provider}' 的 API key...")
    
    env_key = get_env_key(provider)
    if not env_key:
        print(f"   ⚠️  Provider '{provider}' 无需 API key（本地模型）")
        return
    
    env_val = os.environ.get(env_key, "")
    if not env_val:
        print(f"   ❌ 环境变量 {env_key} 未设置")
        sys.exit(1)
    
    cfg = load_config()
    if provider not in cfg.get("models", {}).get("providers", {}):
        cfg.setdefault("models", {}).setdefault("providers", {})[provider] = {}
    
    cfg["models"]["providers"][provider]["apiKey"] = env_val
    save_config(cfg)
    print(f"   ✅ 已添加到 models.providers.{provider}.apiKey")
    
    # 同时更新所有 agent 的 auth-profiles
    for agent in cfg.get("agents", {}).get("list", []):
        aid = agent["id"]
        apf_path = HOME / ".openclaw" / "agents" / aid / "agent" / "auth-profiles.json"
        if apf_path.exists():
            with open(apf_path) as f:
                apf = json.load(f)
            profile = f"{provider}:default"
            apf.setdefault("profiles", {})[profile] = {
                "type": "api_key",
                "provider": provider,
                "key": env_val
            }
            _atomic_write_json(apf_path, apf)
            print(f"   ✅ {aid}: auth-profiles 已更新")


# ── 辅助函数 ──
def _atomic_write_json(path, data):
    """原子写入 JSON 文件：先写临时文件，再 rename，避免崩溃导致文件损坏"""
    path = Path(path)
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent),
        suffix=".tmp"
    )
    try:
        with os.fdopen(tmp_fd, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        shutil.move(tmp_path, str(path))
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


# ── 主入口 ──

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    commands = {
        "switch": lambda: cmd_switch(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("Usage: model-switcher switch <agent> <model>"),
        "add": lambda: cmd_add(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("Usage: model-switcher add <provider> <model-name>"),
        "remove": lambda: cmd_remove(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("Usage: model-switcher remove <provider> <model-name>"),
        "list": cmd_list,
        "list-providers": cmd_list_providers,
        "compare": cmd_compare,
        "diagnose": cmd_diagnose,
        "show": cmd_show,
        "reset": cmd_reset,
        "add-key": lambda: cmd_add_key(sys.argv[2]) if len(sys.argv) >= 3 else print("Usage: model-switcher add-key <provider>"),
    }
    
    handler = commands.get(cmd)
    if handler:
        handler()
    else:
        print(f"❌ 未知命令: {cmd}")
        print(f"   可用命令: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
