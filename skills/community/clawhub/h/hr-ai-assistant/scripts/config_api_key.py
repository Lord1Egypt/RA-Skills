#!/usr/bin/env python3
"""
HR AI Assistant - 配置脚本

这个脚本帮助用户配置 API Key
"""
import os
import sys
import json
from pathlib import Path

def get_config_path():
    """获取配置文件路径"""
    home_dir = Path.home()
    config_dir = home_dir / '.workbuddy' / 'skills' / 'hr-ai-assistant'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.json'

def load_config():
    """加载现有配置"""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "api_key": "",
        "model": "deepseek-ai/DeepSeek-R1",
        "timeout": 120,
        "verbose": True
    }

def save_config(config):
    """保存配置"""
    config_path = get_config_path()
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return config_path

def detect_api_key(user_input):
    """检测用户输入中是否包含 API Key"""
    import re
    
    # 常见的 API Key 格式
    patterns = [
        r'sk-[a-zA-Z0-9]{32,}',           # sk- 开头的格式
        r'[a-zA-Z0-9]{40,}',             # 40+ 字符的格式
        r'hrrule-[a-zA-Z0-9]{32,}',      # hrrule- 开头的格式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_input)
        if match:
            return match.group(0)
    
    return None

def interactive_config():
    """交互式配置"""
    print("=" * 60)
    print("  HR AI Assistant - 配置向导")
    print("=" * 60)
    print()
    
    # 显示当前配置
    config = load_config()
    print("当前配置：")
    print(f"  API Key: {config['api_key'][:10]}..." if config['api_key'] else "  API Key: 未配置")
    print(f"  Model: {config['model']}")
    print(f"  Timeout: {config['timeout']}秒")
    print(f"  Verbose: {config['verbose']}")
    print()
    
    # 询问是否配置 API Key
    print("请选择操作：")
    print("  1. 配置 API Key")
    print("  2. 查看配置文件路径")
    print("  3. 清除 API Key")
    print("  4. 退出")
    print()
    
    choice = input("请输入选项 (1-4): ").strip()
    
    if choice == '1':
        # 配置 API Key
        print()
        print("请输入您的 API Key（可以粘贴完整的文本，我们会自动提取）")
        print()
        api_key_input = input("API Key: ").strip()
        
        # 自动检测
        api_key = detect_api_key(api_key_input)
        if not api_key:
            print()
            print("❌ 未检测到有效的 API Key 格式")
            print()
            print("API Key 格式示例：")
            print("  - sk-abc123xyz456... (以 sk- 开头)")
            print("  - hrrule-abc123xyz456... (以 hrrule- 开头)")
            print("  - abc123xyz456def789... (40+ 字符)")
            print()
            print("如果您的 API Key 格式不同，请尝试直接粘贴完整文本")
            print()
            # 使用用户输入的原始内容
            if len(api_key_input) > 10:
                api_key = api_key_input
            else:
                print("已取消配置。")
                return False
        else:
            print()
            print(f"✅ 检测到 API Key: {api_key[:10]}...")
        
        # 确认保存
        print()
        confirm = input("确认保存此 API Key? (y/n): ").strip().lower()
        if confirm == 'y' or confirm == 'yes':
            config['api_key'] = api_key
            save_config(config)
            print()
            print("✅ 配置已保存！")
            print()
            print("配置文件路径：")
            print(f"  {get_config_path()}")
            print()
            return True
        else:
            print("已取消配置。")
            return False
    
    elif choice == '2':
        # 查看配置文件路径
        print()
        print("配置文件路径：")
        print(f"  {get_config_path()}")
        print()
        return False
    
    elif choice == '3':
        # 清除 API Key
        print()
        confirm = input("确认清除 API Key? (y/n): ").strip().lower()
        if confirm == 'y' or confirm == 'yes':
            config['api_key'] = ""
            save_config(config)
            print()
            print("✅ API Key 已清除！")
            print()
            return True
        else:
            print("已取消操作。")
            return False
    
    elif choice == '4':
        # 退出
        print("再见！")
        return False
    
    else:
        print("无效选项，请重新运行脚本。")
        return False

def main():
    """主函数"""
    try:
        interactive_config()
    except KeyboardInterrupt:
        print()
        print()
        print("已取消配置。")
    except Exception as e:
        print()
        print(f"❌ 配置出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
