#!/usr/bin/env python3
"""
PanSclaw 模型管理器脚本
用于管理自定义模型接入和切换
"""

import sys
import json
import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw-pansclaw" / "openclaw.json"

# API 适配器映射
API_ADAPTERS = {
    "openai": "openai-completions",
    "anthropic": "anthropic-messages",
    "deepseek": "openai-completions",
    "moonshot": "openai-completions",
    "zhipu": "openai-completions",
    "qwen": "openai-completions",
    "ollama": "ollama",
    # 别名
    "anthropic-claude": "anthropic-messages",
    "claude": "anthropic-messages",
}

def load_config():
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        print(f"❌ 配置文件不存在: {CONFIG_PATH}")
        return None
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def add_model(provider, base_url, api_key, model_name):
    """添加模型"""
    config = load_config()
    if config is None:
        return False
    
    # 确保 models 结构存在
    if 'models' not in config:
        config['models'] = {'mode': 'merge', 'providers': {}}
    if 'providers' not in config['models']:
        config['models']['providers'] = {}
    
    # 添加/更新 provider
    api_adapter = API_ADAPTERS.get(provider, "openai-completions")
    config['models']['providers'][provider] = {
        "baseUrl": base_url,
        "apiKey": api_key,
        "api": api_adapter,
        "models": [{"id": model_name, "name": model_name}]
    }
    
    save_config(config)
    
    print(f"✅ 模型添加成功!")
    print(f"   厂商: {provider}")
    print(f"   地址: {base_url}")
    print(f"   模型: {model_name}")
    print(f"   适配器: {api_adapter}")
    return True

def switch_model(model_full_name):
    """切换默认模型"""
    config = load_config()
    if config is None:
        return False
    
    # 解析 model_full_name (provider/model)
    if '/' in model_full_name:
        provider, model_name = model_full_name.split('/', 1)
    else:
        print(f"❌ 格式错误，请使用 <厂商>/<模型名> 格式")
        return False
    
    # 检查 provider 是否存在
    providers = config.get('models', {}).get('providers', {})
    if provider not in providers:
        print(f"❌ 厂商 '{provider}' 不存在，请先添加模型")
        return False
    
    # 检查模型是否存在
    models = providers[provider].get('models', [])
    model_ids = [m.get('id') for m in models]
    if model_name not in model_ids:
        print(f"❌ 模型 '{model_name}' 不存在，可用模型: {model_ids}")
        return False
    
    # 更新默认模型
    if 'agents' not in config:
        config['agents'] = {}
    if 'defaults' not in config['agents']:
        config['agents']['defaults'] = {}
    if 'model' not in config['agents']['defaults']:
        config['agents']['defaults']['model'] = {}
    
    config['agents']['defaults']['model']['primary'] = model_full_name
    
    save_config(config)
    
    print(f"✅ 默认模型已切换为: {model_full_name}")
    return True

def list_models():
    """列出所有模型"""
    config = load_config()
    if config is None:
        return False
    
    providers = config.get('models', {}).get('providers', {})
    current = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '未设置')
    
    print(f"📋 当前默认模型: {current}")
    print(f"\n已配置的模型提供商:")
    print("-" * 50)
    
    if not providers:
        print("  (无)")
        return True
    
    for provider, info in providers.items():
        base_url = info.get('baseUrl', '')
        api = info.get('api', '')
        models = info.get('models', [])
        model_list = ', '.join([m.get('name', m.get('id')) for m in models])
        print(f"\n  【{provider}】")
        print(f"    地址: {base_url}")
        print(f"    API: {api}")
        print(f"    模型: {model_list}")
    
    print("\n" + "-" * 50)
    return True

def delete_model(provider):
    """删除模型配置"""
    config = load_config()
    if config is None:
        return False
    
    providers = config.get('models', {}).get('providers', {})
    
    if provider not in providers:
        print(f"❌ 厂商 '{provider}' 不存在")
        return False
    
    # 检查是否是当前默认模型
    current = config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '')
    if current.startswith(provider + '/'):
        print(f"⚠️  警告: 当前默认模型属于 {provider}，删除后请切换到其他模型")
    
    del providers[provider]
    
    save_config(config)
    
    print(f"✅ 已删除厂商: {provider}")
    return True

def help():
    """显示帮助"""
    print("""
🤖 PanSclaw 模型管理器

用法:
  model-manager.py <命令> [参数]

命令:
  add <厂商> <地址> <密钥> <模型名>
    添加新的模型提供商
    
  switch <厂商>/<模型名>
    切换默认模型
    
  list
    列出所有已配置的模型
    
  delete <厂商>
    删除模型提供商
    
  help
    显示帮助

示例:
  # 添加 DeepSeek 模型
  python3 model-manager.py add deepseek https://api.deepseek.com/v1 sk-xxx deepseek-chat
  
  # 切换到指定模型
  python3 model-manager.py switch deepseek/deepseek-chat
  
  # 列出所有模型
  python3 model-manager.py list
  
  # 删除厂商
  python3 model-manager.py delete deepseek
""")

def main():
    if len(sys.argv) < 2:
        help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        if len(sys.argv) < 6:
            print("❌ 用法: add <厂商> <地址> <密钥> <模型名>")
            sys.exit(1)
        provider, base_url, api_key, model_name = sys.argv[2:6]
        add_model(provider, base_url, api_key, model_name)
    
    elif command == 'switch':
        if len(sys.argv) < 3:
            print("❌ 用法: switch <厂商>/<模型名>")
            sys.exit(1)
        switch_model(sys.argv[2])
    
    elif command == 'list':
        list_models()
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("❌ 用法: delete <厂商>")
            sys.exit(1)
        delete_model(sys.argv[2])
    
    elif command in ('help', '--help', '-h'):
        help()
    
    else:
        print(f"❌ 未知命令: {command}")
        help()
        sys.exit(1)

if __name__ == "__main__":
    main()