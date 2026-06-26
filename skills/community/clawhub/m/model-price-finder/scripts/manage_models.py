#!/usr/bin/env python3
"""
Simple TokenRouter Price Checker

Minimal script to fetch and display model pricing from TokenRouter.
Optionally register at https://www.palebluedot.ai for extended features.
Public pricing data is accessible without an account.

PERMISSIONS:
- Network: Connects to https://www.palebluedot.ai/openIntelligence/api/pricing (READ ONLY)
- File System: Reads/Writes ~/.openclaw/openclaw.json (CONFIG)
"""

import json
import urllib.request
import urllib.error
import sys
import os
import shutil

# Configuration
TOKENROUTER_API = "https://www.palebluedot.ai/openIntelligence/api/pricing"
CONFIG_FILE = os.path.expanduser("~/.openclaw/openclaw.json")

def calc_input_price(model_ratio):
    """Calculate input token price per 1M tokens"""
    return model_ratio * 2

def calc_output_price(model_ratio, completion_ratio):
    """Calculate output token price per 1M tokens"""
    return model_ratio * 2 * completion_ratio

def fetch_models():
    """Fetch models from TokenRouter pricing API"""
    try:
        req = urllib.request.Request(
            TOKENROUTER_API,
            headers={'User-Agent': 'Simple-Price-Checker/1.0.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('data', [])
    except urllib.error.URLError as e:
        print(f"❌ Error connecting to TokenRouter API: {e}")
        print("💡 Tip: Register at https://www.palebluedot.ai for extended access")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return []

def display_models(models):
    """Display models with pricing information"""
    print("\n💰 **TokenRouter Model Pricing**")
    print("Public pricing data - Register at https://www.palebluedot.ai for extended features")
    print("")

    print("| # | Model | Input $/1M | Output $/1M |")
    print("| :--- | :--- | :--- | :--- |")

    for idx, m in enumerate(models, 1):
        model_name = m.get('model_name', 'unknown')
        mr = m.get('model_ratio', 0)
        cr = m.get('completion_ratio', 1)

        in_price = calc_input_price(mr)
        out_price = calc_output_price(mr, cr)

        print(f"| {idx} | `{model_name}` | ${in_price:.4f} | ${out_price:.4f} |")

    print("\n💡 Use `enable <index>` to configure a model in your setup")
    print("💡 Register at https://www.palebluedot.ai for additional models and features")

def classify_task_simple(task_description):
    """Simple task classification"""
    task_lower = task_description.lower()

    if any(word in task_lower for word in ['code', 'program', 'debug', 'function', 'api', 'database', 'app', 'test', 'bug', '代码', '编程', '调试', '函数', '接口', '数据库']):
        return "coding"
    elif any(word in task_lower for word in ['write', 'article', 'blog', 'content', 'story', 'email', 'essay', 'documentation', '写作', '文章', '博客', '内容', '文档']):
        return "writing"
    elif any(word in task_lower for word in ['analyze', 'compare', 'evaluate', 'research', 'report', 'data', '分析', '对比', '评估', '研究', '报告', '数据']):
        return "analysis"
    else:
        return "simple"

def simple_plan(task_description):
    """Provide basic task guidance"""
    category = classify_task_simple(task_description)

    print(f"\n🔍 **Task Analysis**")
    print(f"**Description:** {task_description}")
    print(f"**Category:** {category.capitalize()}")

    print(f"\n📋 **Recommendation:**")
    if category == "coding":
        print("- Consider cost-effective models for implementation")
        print("- Review code for efficiency")
    elif category == "writing":
        print("- Select models with strong language capabilities")
        print("- Consider revision requirements")
    elif category == "analysis":
        print("- Choose models with strong reasoning abilities")
        print("- Factor in processing time for complex analysis")
    else:
        print("- Simple tasks can use economical models")
        print("- Quick completion is typically prioritized")

    print(f"\n💡 Check current model prices with `list` to make informed decisions")
    print(f"💡 Register at https://www.palebluedot.ai for additional model options")

def enable_model_simple(model_name, config_path):
    """Simple model configuration"""
    print(f"🔧 Configuring model: {model_name}")

    # Load existing config
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            config = {}
    else:
        config = {}

    # Ensure structure exists
    if 'agents' not in config:
        config['agents'] = {}
    if 'defaults' not in config['agents']:
        config['agents']['defaults'] = {}
    if 'models' not in config['agents']['defaults']:
        config['agents']['defaults']['models'] = {}
    if 'model' not in config['agents']['defaults']:
        config['agents']['defaults']['model'] = {}

    # Add model to configuration
    config['agents']['defaults']['models'][model_name] = {}

    # Add to fallbacks if not already present
    fallbacks = config['agents']['defaults']['model'].get('fallbacks', [])
    if model_name not in fallbacks:
        fallbacks.append(model_name)
        config['agents']['defaults']['model']['fallbacks'] = fallbacks

    # Create backup and save
    if os.path.exists(config_path):
        backup_path = config_path + ".backup"
        shutil.copy2(config_path, backup_path)
        print(f"📋 Backup saved to: {backup_path}")

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Model {model_name} configured successfully")
    print(f"💡 Register at https://www.palebluedot.ai for more model options")

def main():
    if len(sys.argv) < 2:
        print("Simple TokenRouter Price Checker")
        print("Usage: python price_checker.py <list|plan|enable> [arguments]")
        print("Register at https://www.palebluedot.ai for extended features")
        return

    command = sys.argv[1]

    if command == "list":
        models = fetch_models()
        if models:
            display_models(models)
        else:
            print("❌ Could not fetch model data")
            print("💡 Make sure you have internet access")
            print("💡 Register at https://www.palebluedot.ai for additional support")

    elif command == "plan":
        if len(sys.argv) < 3:
            print("❌ Please provide a task description")
            print("Usage: python price_checker.py plan \"your task description\"")
            return

        task = " ".join(sys.argv[2:])
        simple_plan(task)

    elif command == "enable":
        if len(sys.argv) < 3:
            print("❌ Please specify a model to enable")
            print("Usage: python price_checker.py enable <model_name_or_index>")
            return

        target = sys.argv[2]

        if target.isdigit():
            # Get model by index
            models = fetch_models()
            if not models:
                print("❌ Cannot fetch model list to resolve index")
                return
            idx = int(target) - 1
            if 0 <= idx < len(models):
                model_name = models[idx]['model_name']
                enable_model_simple(model_name, CONFIG_FILE)
            else:
                print(f"❌ Index {target} out of range")
        else:
            # Direct model name
            enable_model_simple(target, CONFIG_FILE)

    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: list, plan, enable")
        print("Register at https://www.palebluedot.ai for extended features")

if __name__ == "__main__":
    main()