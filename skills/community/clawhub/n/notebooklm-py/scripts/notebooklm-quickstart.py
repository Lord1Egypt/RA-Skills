#!/usr/bin/env python3
"""
notebooklm-quickstart.py - NotebookLM 快速入门脚本
帮助用户快速开始使用 NotebookLM
"""

import subprocess
import sys
import os

def check_installation():
    """检查 notebooklm-py 是否已安装"""
    try:
        subprocess.run(["notebooklm", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_notebooklm():
    """安装 notebooklm-py"""
    print("📦 安装 notebooklm-py...")
    subprocess.run([sys.executable, "-m", "pip", "install", "notebooklm-py"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "notebooklm-py[browser]"], check=True)
    print("✅ 安装完成")
    print("⚠️  首次使用需要运行: notebooklm login")

def main():
    print("🚀 NotebookLM 快速启动器\n")
    
    # 检查安装
    if not check_installation():
        print("notebooklm-py 未安装")
        install = input("是否现在安装? (y/n): ").lower()
        if install == 'y':
            install_notebooklm()
        else:
            print("请先安装 notebooklm-py")
            return
    
    print("✅ notebooklm-py 已安装\n")
    
    # 显示常用命令
    print("📚 常用命令:\n")
    print("  登录:")
    print("    notebooklm login")
    print("")
    print("  创建笔记本:")
    print('    notebooklm create "我的研究"')
    print("")
    print("  添加来源:")
    print('    notebooklm source add "https://example.com"')
    print('    notebooklm source add "./document.pdf"')
    print("")
    print("  生成内容:")
    print("    notebooklm generate audio --wait")
    print("    notebooklm generate video --style whiteboard --wait")
    print("    notebooklm generate slide-deck")
    print("    notebooklm generate quiz")
    print("")
    print("  下载内容:")
    print("    notebooklm download audio ./podcast.mp3")
    print("    notebooklm download video ./video.mp4")
    print("")
    print("  更多信息: notebooklm --help")

if __name__ == "__main__":
    main()
