#!/usr/bin/env python3
"""
Switch Model Script
Usage: python3 switch-model.py <model-alias>
"""

import json
import sys
import os
import subprocess
import time
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "../config/models.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw/openclaw.json"

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_model_by_alias(models, alias):
    alias_lower = alias.lower()
    for key, info in models.items():
        if key.lower() == alias_lower:
            return key
        for model_alias in info.get('alias', []):
            if model_alias.lower() == alias_lower:
                return key
    return None

def restart_gateway():
    log_info("重启网关中...")
    os.system('openclaw gateway restart > /dev/null 2>&1')
    time.sleep(3)
    for i in range(10):
        result = subprocess.run(['openclaw', 'gateway', 'status'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        if 'running' in result.stdout.lower():
            log_success("网关已重启完成")
            return True
        time.sleep(1)
    log_warning("网关重启超时，但配置已更新")
    return False

def main():
    if len(sys.argv) < 2:
        print("用法：python3 switch-model.py <model-alias>")
        print("示例：python3 switch-model.py gemini")
        print("\n可用模型:")
        config = load_json(CONFIG_FILE) if CONFIG_FILE.exists() else {}
        for key, info in config.get('models', {}).items():
            marker = " (当前)" if key == config.get('current') else ""
            print(f"  - {key}:{marker} {info.get('description', '')}")
        sys.exit(1)
    
    model_alias = sys.argv[1]
    config = load_json(CONFIG_FILE)
    models = config.get('models', {})
    
    model_key = find_model_by_alias(models, model_alias)
    
    if not model_key:
        log_error(f"未找到模型：{model_alias}")
        print("\n可用模型及别名：")
        for key, info in models.items():
            print(f"  - {key}: {', '.join(info.get('alias', []))}")
        sys.exit(1)
    
    model_info = models[model_key]
    provider = model_info.get('provider', 'unknown')
    model_id = model_info.get('modelId', model_key)
    supports_images = "✅" if model_info.get('supportsImages', False) else "❌"
    description = model_info.get('description', '')
    
    log_info(f"找到模型：{model_key}")
    log_info(f"提供商：{provider}")
    log_info(f"模型 ID: {model_id}")
    log_info(f"支持图片：{supports_images}")
    log_info(f"描述：{description}")
    
    current_model = config.get('current')
    if current_model == model_key:
        log_warning(f"已经是当前模型：{model_key}")
        sys.exit(0)
    
    # Backup config
    import shutil
    backup_file = f"{OPENCLAW_CONFIG}.bak.model-switch.{time.strftime('%Y%m%d%H%M%S')}"
    shutil.copy(OPENCLAW_CONFIG, backup_file)
    log_info(f"配置已备份：{backup_file}")
    
    # Update models.json
    config['current'] = model_key
    save_json(CONFIG_FILE, config)
    log_success("已更新 models.json")
    
    # Update openclaw.json
    primary_model = f"{provider}/{model_id}"
    openclaw_config = load_json(OPENCLAW_CONFIG)
    
    providers = openclaw_config.get('models', {}).get('providers', {})
    if provider in providers:
        log_success(f"提供商 {provider} 已配置")
    else:
        log_warning(f"提供商 {provider} 在 openclaw.json 中未配置，需要手动添加 API Key")
    
    if 'agents' not in openclaw_config:
        openclaw_config['agents'] = {}
    if 'defaults' not in openclaw_config['agents']:
        openclaw_config['agents']['defaults'] = {}
    if 'model' not in openclaw_config['agents']['defaults']:
        openclaw_config['agents']['defaults']['model'] = {}
    
    openclaw_config['agents']['defaults']['model']['primary'] = primary_model
    save_json(OPENCLAW_CONFIG, openclaw_config)
    log_success(f"已更新 openclaw.json 主模型为：{primary_model}")
    
    # Restart gateway
    restart_gateway()
    
    # Final status
    print("")
    log_success("✅ 模型切换完成")
    print("")
    print("┌─────────────────────────────────────────")
    print("│  切换摘要")
    print("├─────────────────────────────────────────")
    print(f"│  原模型：{current_model}")
    print(f"│  新模型：{model_key} ({primary_model})")
    print(f"│  支持图片：{supports_images}")
    print(f"│  描述：{description}")
    print("└─────────────────────────────────────────")

if __name__ == '__main__':
    main()
