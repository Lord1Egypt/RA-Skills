#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Vision 环境检查脚本
"""

import subprocess
import sys


def check_environment():
    """检查 Ollama 环境状态"""
    results = []
    
    # 1. 检查 Ollama 安装
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            results.append(f"✅ Ollama 已安装: {version}")
        else:
            results.append("❌ Ollama 未正确安装")
            return results
    except FileNotFoundError:
        results.append("❌ Ollama 未安装")
        results.append("   安装命令: winget install Ollama.Ollama")
        return results
    except Exception as e:
        results.append(f"❌ 检查 Ollama 失败: {e}")
        return results
    
    # 2. 检查可用模型
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            models = result.stdout.strip()
            if models:
                results.append(f"✅ 已安装模型:\n{models}")
            else:
                results.append("⚠️  未安装任何模型")
            
            # 检查 qwen3-vl:4b
            if "qwen3-vl" in models:
                results.append("✅ qwen3-vl:4b 模型已安装")
            else:
                results.append("⚠️  qwen3-vl:4b 模型未安装")
                results.append("   安装命令: ollama pull qwen3-vl:4b")
        else:
            results.append("❌ 无法获取模型列表")
    except Exception as e:
        results.append(f"❌ 检查模型失败: {e}")
    
    return results


if __name__ == "__main__":
    print("正在检查 Ollama Vision 环境...\n")
    results = check_environment()
    for r in results:
        print(r)
    
    # 返回退出码
    has_error = any("❌" in r for r in results)
    sys.exit(1 if has_error else 0)
