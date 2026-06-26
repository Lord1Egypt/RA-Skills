#!/usr/bin/env python3
"""
Add Model Guide - Optimized
Usage: python3 add-model-guide.py

Optimized flow: Single conversation for all model details with smart defaults.
"""

import json
import sys
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "../config/models.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw/openclaw.json"

# Pre-defined providers with smart defaults
MODEL_PROVIDERS = [
    {"name": "Google", "id": "google", "url": "https://makersuite.google.com/app/apikey", 
     "default_models": [{"id": "gemini-2.0-flash", "images": True, "reasoning": False, "ctx": 1048576, "tokens": 8192}]},
    {"name": "OpenAI", "id": "openai", "url": "https://platform.openai.com/api-keys",
     "default_models": [{"id": "gpt-4o", "images": True, "reasoning": False, "ctx": 128000, "tokens": 16384}]},
    {"name": "Anthropic", "id": "anthropic", "url": "https://console.anthropic.com/settings/keys",
     "default_models": [{"id": "claude-3-5-sonnet-20241022", "images": True, "reasoning": False, "ctx": 200000, "tokens": 8192}]},
    {"name": "Qwen (DashScope)", "id": "dashscope", "url": "https://dashscope.console.aliyun.com/apiKey",
     "default_models": [{"id": "qwen-max", "images": True, "reasoning": True, "ctx": 256000, "tokens": 30720}]},
    {"name": "Moonshot (Kimi)", "id": "moonshot", "url": "https://platform.moonshot.cn",
     "default_models": [{"id": "kimi-k2.5", "images": True, "reasoning": False, "ctx": 262144, "tokens": 32768}]},
    {"name": "MiniMax", "id": "minimax", "url": "https://platform.minimaxi.com",
     "default_models": [{"id": "MiniMax-M2.5", "images": False, "reasoning": False, "ctx": 196608, "tokens": 32768}]},
    {"name": "GLM (Zhipu)", "id": "glm", "url": "https://open.bigmodel.cn",
     "default_models": [{"id": "glm-5", "images": False, "reasoning": True, "ctx": 202752, "tokens": 16384}]},
    {"name": "DeepSeek", "id": "deepseek", "url": "https://platform.deepseek.com",
     "default_models": [{"id": "deepseek-chat", "images": False, "reasoning": True, "ctx": 128000, "tokens": 8192}]},
    {"name": "Custom Provider", "id": "custom", "url": "",
     "default_models": [{"id": "custom-model", "images": False, "reasoning": False, "ctx": 1000000, "tokens": 10000}]},
]

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print_header("🆕 新增模型向导（优化版）")
    
    # Step 1: Select provider
    print_header("📋 选择模型提供商")
    for idx, p in enumerate(MODEL_PROVIDERS, 1):
        print(f"{Colors.BOLD}{idx}. {p['name']}{Colors.NC}")
    print(f"\n{Colors.YELLOW}提示：输入编号或名称（如：7 或 google）{Colors.NC}\n")
    
    try:
        choice = input(f"{Colors.CYAN}> {Colors.NC}").strip()
        provider = None
        
        # Try number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(MODEL_PROVIDERS):
                provider = MODEL_PROVIDERS[idx]
        else:
            # Try name match
            choice_lower = choice.lower()
            for p in MODEL_PROVIDERS:
                if p['name'].lower() == choice_lower or p['id'].lower() == choice_lower:
                    provider = p
                    break
        
        if not provider:
            print(f"{Colors.RED}未找到：{choice}{Colors.NC}")
            return
            
    except (EOFError, ValueError):
        print(f"{Colors.RED}输入无效{Colors.NC}")
        return
    
    print(f"\n{Colors.GREEN}✓ 已选择：{provider['name']}{Colors.NC}")
    
    # Step 2: Get API Key
    print_header(f"🔑 配置 {provider['name']} API Key")
    
    if provider['url']:
        print(f"获取 API Key：{Colors.CYAN}{provider['url']}{Colors.NC}\n")
    
    try:
        api_key = input(f"{Colors.YELLOW}请输入 API Key（回车跳过）:{Colors.NC} ").strip()
    except EOFError:
        api_key = ""
    
    # Step 3: Select model (with smart defaults)
    print_header("⚙️  配置模型")
    
    default_model = provider['default_models'][0]
    print(f"{Colors.BOLD}推荐模型:{Colors.NC} {Colors.GREEN}{default_model['id']}{Colors.NC}")
    print(f"   支持图片：{'✅' if default_model['images'] else '❌'}")
    print(f"   支持推理：{'✅' if default_model['reasoning'] else '❌'}")
    print(f"   上下文窗口：{default_model['ctx']:,}")
    print(f"   最大输出：{default_model['tokens']:,}\n")
    
    try:
        model_id = input(f"{Colors.YELLOW}模型 ID（回车使用推荐）:{Colors.NC} ").strip()
        if not model_id:
            model_id = default_model['id']
        
        # Smart defaults based on model ID
        supports_images = default_model['images']
        supports_reasoning = default_model['reasoning']
        context_window = default_model['ctx']
        max_tokens = default_model['tokens']
        
        # Allow override
        print(f"\n{Colors.BOLD}模型特性（智能判断，可修改）:{Colors.NC}")
        print(f"   支持图片：{'✅' if supports_images else '❌'}")
        print(f"   支持推理：{'✅' if supports_reasoning else '❌'}")
        
        override = input(f"\n{Colors.YELLOW}是否需要修改特性？(y/N):{Colors.NC} ").strip().lower()
        if override == 'y':
            supports_images = input("支持图片？(y/n): ").strip().lower() == 'y'
            supports_reasoning = input("支持推理？(y/n): ").strip().lower() == 'y'
            try:
                context_window = int(input(f"上下文窗口（默认 {default_model['ctx']}）: ").strip() or default_model['ctx'])
                max_tokens = int(input(f"最大输出（默认 {default_model['tokens']}）: ").strip() or default_model['tokens'])
            except ValueError:
                pass
        
    except EOFError:
        model_id = default_model['id']
    
    # Step 4: Generate alias and description
    alias = model_id.split('-')[0].lower()  # Auto-generate alias
    description = f"{provider['name']} - {model_id}"
    
    print(f"\n{Colors.BOLD}模型别名:{Colors.NC} {Colors.CYAN}{alias}{Colors.NC}")
    print(f"{Colors.BOLD}模型描述:{Colors.NC} {Colors.CYAN}{description}{Colors.NC}")
    
    try:
        confirm = input(f"\n{Colors.YELLOW}确认配置？(y/N):{Colors.NC} ").strip().lower()
        if confirm != 'y':
            print(f"{Colors.YELLOW}已取消{Colors.NC}")
            return
    except EOFError:
        pass
    
    # Step 5: Save configuration
    print_header("💾 保存配置")
    
    # Update models.json
    config = load_json(CONFIG_FILE) if CONFIG_FILE.exists() else {"models": {}}
    
    model_key = f"{provider['id']}-{model_id.replace('.', '-')}"
    config['models'][model_key] = {
        'alias': [alias, provider['id'], model_id],
        'provider': provider['id'],
        'modelId': model_id,
        'supportsImages': supports_images,
        'supportsReasoning': supports_reasoning,
        'contextWindow': context_window,
        'maxTokens': max_tokens,
        'description': description
    }
    
    save_json(CONFIG_FILE, config)
    print(f"{Colors.GREEN}✅ 已添加到模型列表：{model_key}{Colors.NC}")
    
    # Update openclaw.json if API key provided
    if api_key:
        openclaw = load_json(OPENCLAW_CONFIG) if OPENCLAW_CONFIG.exists() else {}
        
        if 'models' not in openclaw:
            openclaw['models'] = {'mode': 'merge', 'providers': {}}
        if 'providers' not in openclaw['models']:
            openclaw['models']['providers'] = {}
        
        provider_id = provider['id']
        if provider_id not in openclaw['models']['providers']:
            openclaw['models']['providers'][provider_id] = {
                'baseUrl': f"https://api.{provider_id}.com/v1" if provider_id != 'custom' else "",
                'apiKey': api_key,
                'api': 'openai-completions',
                'models': []
            }
        else:
            openclaw['models']['providers'][provider_id]['apiKey'] = api_key
        
        save_json(OPENCLAW_CONFIG, openclaw)
        print(f"{Colors.GREEN}✅ 已更新 API Key: {provider_id}{Colors.NC}")
    
    # Step 6: Ask to switch
    print_header("🎯 设置为当前模型？")
    print(f"新模型已添加：{Colors.GREEN}{model_key}{Colors.NC}\n")
    
    try:
        switch = input(f"{Colors.YELLOW}要切换到这个模型吗？(y/N):{Colors.NC} ").strip().lower()
        if switch == 'y':
            print(f"\n{Colors.GREEN}✅ 正在切换到 {model_key}...{Colors.NC}")
            # Execute switch
            switch_script = SCRIPT_DIR / "switch-model.py"
            if switch_script.exists():
                import subprocess
                subprocess.run(['python3', str(switch_script), model_key])
            else:
                print(f"{Colors.YELLOW}⚠️  switch-model.py 不存在，请手动切换{Colors.NC}")
        else:
            print(f"\n{Colors.YELLOW}ℹ️  已添加模型，未切换{Colors.NC}")
            print(f"   需要切换时说：\"use {model_key}\"")
    except EOFError:
        pass
    
    # Done
    print_header("✅ 完成")
    print(f"{Colors.GREEN}模型配置完成！{Colors.NC}")
    print(f"\n新模型：{model_key}")
    print(f"提供商：{provider['name']}")
    print(f"模型 ID: {model_id}")
    print(f"\n{Colors.BOLD}下次切换模型:{Colors.NC}")
    print(f"   说 \"use {model_key}\"")
    print(f"   或说 \"切换模型\" 选择")

if __name__ == '__main__':
    main()
