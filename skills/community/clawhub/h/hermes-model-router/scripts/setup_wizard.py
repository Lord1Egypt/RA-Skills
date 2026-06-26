#!/usr/bin/env python3
"""
Model Router - 配置向导
引导用户配置本地模型和服务商模型
"""

import json
import os
import sys

CONFIG_DIR = os.path.expanduser("~/.model-router")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config() -> dict:
    """加载现有配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "local": {
            "provider": "ollama",
            "endpoint": "http://localhost:11434",
            "model": "qwen2.5-coder:7b"
        },
        "cloud": {
            "provider": "minmax",
            "endpoint": "https://api.minimax.chat",
            "model": "MiniMax-Text-01"
        }
    }


def save_config(config: dict):
    """保存配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"\n✅ 配置已保存到: {CONFIG_FILE}")


def setup_local_model(config: dict):
    """配置本地模型"""
    print("\n" + "=" * 50)
    print("🔧 本地模型配置")
    print("=" * 50)
    
    print("\n支持的本地模型提供商:")
    print("  1. Ollama (默认)")
    print("  2. llama.cpp")
    
    provider = input("\n选择提供商 [1]: ").strip() or "1"
    
    if provider == "2":
        config["local"]["provider"] = "llama.cpp"
        config["local"]["endpoint"] = input("endpoint [http://localhost:8080]: ").strip() or "http://localhost:8080"
        config["local"]["model"] = input("模型名 [qwen2.5-coder-7b-q4]: ").strip() or "qwen2.5-coder-7b-q4"
    else:
        config["local"]["provider"] = "ollama"
        config["local"]["endpoint"] = input("endpoint [http://localhost:11434]: ").strip() or "http://localhost:11434"
        config["local"]["model"] = input("模型名 [qwen2.5-coder:7b]: ").strip() or "qwen2.5-coder:7b"
    
    print(f"\n✅ 本地模型配置完成:")
    print(f"   提供商: {config['local']['provider']}")
    print(f"   endpoint: {config['local']['endpoint']}")
    print(f"   模型: {config['local']['model']}")


def setup_cloud_model(config: dict):
    """配置服务商模型"""
    print("\n" + "=" * 50)
    print("☁️ 服务商模型配置")
    print("=" * 50)
    
    print("\n支持的服务商:")
    print("  1. MiniMax (默认)")
    print("  2. OpenRouter")
    print("  3. 其他")
    
    provider = input("\n选择服务商 [1]: ").strip() or "1"
    
    if provider == "2":
        config["cloud"]["provider"] = "openrouter"
        config["cloud"]["endpoint"] = "https://openrouter.ai/api/v1"
        config["cloud"]["model"] = input("模型 (如 anthropic/claude-sonnet-4-5) [anthropic/claude-sonnet-4-5]: ").strip() or "anthropic/claude-sonnet-4-5"
    elif provider == "3":
        config["cloud"]["provider"] = input("服务商名称: ").strip()
        config["cloud"]["endpoint"] = input("API endpoint: ").strip()
        config["cloud"]["model"] = input("默认模型: ").strip()
    else:
        config["cloud"]["provider"] = "minmax"
        config["cloud"]["endpoint"] = "https://api.minimax.chat"
        config["cloud"]["model"] = input("模型 [MiniMax-Text-01]: ").strip() or "MiniMax-Text-01"
    
    print(f"\n✅ 服务商模型配置完成:")
    print(f"   提供商: {config['cloud']['provider']}")
    print(f"   endpoint: {config['cloud']['endpoint']}")
    print(f"   模型: {config['cloud']['model']}")


def main():
    print("=" * 50)
    print("🧠 Model Router 配置向导")
    print("=" * 50)
    print("\n本向导将帮助你配置:")
    print("  1. 本地模型 (用于简单任务)")
    print("  2. 服务商模型 (用于复杂任务)")
    
    config = load_config()
    print("\n当前配置:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    print("\n" + "-" * 50)
    print("选择要配置的项目:")
    print("  1. 配置本地模型")
    print("  2. 配置服务商模型")
    print("  3. 全部配置")
    print("  4. 保存当前配置并退出")
    print("  5. 仅测试连接")
    
    choice = input("\n选择 [3]: ").strip() or "3"
    
    if choice == "1":
        setup_local_model(config)
    elif choice == "2":
        setup_cloud_model(config)
    elif choice == "3":
        setup_local_model(config)
        setup_cloud_model(config)
    elif choice == "4":
        save_config(config)
        sys.exit(0)
    elif choice == "5":
        print("\n🔍 测试连接...")
        # TODO: 实现连接测试
        print("连接测试功能待实现")
        sys.exit(0)
    else:
        print("无效选择")
        sys.exit(1)
    
    save_config(config)
    
    print("\n" + "=" * 50)
    print("🎉 配置完成！")
    print("=" * 50)
    print("\n使用示例:")
    print("  python3 scripts/classify_task.py \"翻译成英文\"")
    print("  python3 scripts/classify_task.py \"分析市场策略\" --verbose")
    print()


if __name__ == "__main__":
    main()
