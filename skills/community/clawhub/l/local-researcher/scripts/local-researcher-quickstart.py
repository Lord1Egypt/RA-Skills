#!/usr/bin/env python3
"""
local-researcher-quickstart.py - 本地研究助手快速启动脚本
"""

import subprocess
import sys
import os

def check_ollama():
    """检查 Ollama 是否安装运行"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_repo():
    """检查是否已克隆仓库"""
    return os.path.exists("./local-deep-researcher/src")

def main():
    print("🔍 本地研究助手快速启动器\n")
    
    # 检查 Ollama
    if not check_ollama():
        print("⚠️  Ollama 未安装或未运行")
        print("📥 安装指南:")
        print("   macOS: brew install ollama")
        print("   Linux: curl -fsSL https://ollama.com/install.sh | sh")
        print("")
        print("   然后拉取模型:")
        print("   ollama pull deepseek-r1:8b")
        print("   ollama pull llama3.2")
        return
    
    print("✅ Ollama 已安装")
    
    # 显示已安装模型
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True
    )
    print("\n📦 可用模型:")
    print(result.stdout)
    
    # 检查仓库
    if not check_repo():
        print("\n⚠️  未找到 local-deep-researcher 仓库")
        print("📥 克隆:")
        print("   git clone https://github.com/langchain-ai/local-deep-researcher.git")
        print("   cd local-deep-researcher")
        print("   python -m venv .venv")
        print("   source .venv/bin/activate")
        print("   pip install -e .")
        return
    
    print("✅ 仓库已就绪\n")
    
    # 显示使用指南
    print("📚 快速开始:\n")
    print("1. 配置环境变量:")
    print("   cp .env.example .env")
    print("   # 编辑 .env 文件")
    print("")
    print("2. 启动研究:")
    print("   langgraph dev")
    print("")
    print("3. 程序化使用:")
    print("   见 SKILL.md 中的 Python 示例")
    print("")
    print("📖 详细文档: cat SKILL.md")

if __name__ == "__main__":
    main()
