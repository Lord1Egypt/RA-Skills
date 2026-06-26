#!/usr/bin/env python3
"""
下载 Vosk 中文语音模型
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

# 模型信息
MODEL_NAME = "vosk-model-small-zh-cn-0.22"
# 使用 HuggingFace 镜像（更可靠）
MODEL_URL = f"https://huggingface.co/vosk-community/{MODEL_NAME}/resolve/main/{MODEL_NAME}.zip"
MODEL_SIZE = "~50MB"
DOWNLOAD_PATH = Path.home() / ".openclaw" / "vosk-models"

def download_model():
    """下载模型"""
    print_color(Colors.BLUE, "📥 下载 Vosk 中文语音模型")
    print("")
    print(f"模型名称：{MODEL_NAME}")
    print(f"模型大小：{MODEL_SIZE}")
    print(f"下载链接：{MODEL_URL}")
    print("")
    
    # 创建目录
    DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
    
    zip_file = DOWNLOAD_PATH / f"{MODEL_NAME}.zip"
    
    # 检查是否已下载
    if zip_file.exists():
        print_color(Colors.YELLOW, "⚠️  模型已下载，是否重新下载？(y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            # 直接解压
            extract_model(zip_file)
            return
    
    # 下载
    print_color(Colors.BLUE, "开始下载...")
    print("")
    
    def progress_hook(count, block_size, total_size):
        percent = min(100, count * block_size * 100 // total_size)
        downloaded = count * block_size / 1024 / 1024
        total = total_size / 1024 / 1024
        print(f"\r   进度：{percent:3d}% ({downloaded:.1f}/{total:.1f} MB)", end='', flush=True)
    
    try:
        urllib.request.urlretrieve(MODEL_URL, zip_file, progress_hook)
        print()  # 换行
        print_color(Colors.GREEN, "✅ 下载完成")
        print("")
        
        # 解压
        extract_model(zip_file)
        
    except Exception as e:
        print()
        print_color(Colors.RED, f"❌ 下载失败：{e}")
        sys.exit(1)

def extract_model(zip_file):
    """解压模型"""
    print_color(Colors.BLUE, "📦 解压模型...")
    print("")
    
    extract_path = DOWNLOAD_PATH / MODEL_NAME
    
    # 检查是否已解压
    if extract_path.exists():
        print_color(Colors.YELLOW, "⚠️  模型已解压")
        print("")
        print(f"模型位置：{extract_path}")
        return
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(DOWNLOAD_PATH)
        
        print_color(Colors.GREEN, "✅ 解压完成")
        print("")
        print(f"模型位置：{extract_path}")
        print("")
        print("🎉 模型已就绪！可以开始使用语音控制了！")
        print("")
        print("使用命令:")
        print("  python3 scripts/voice_recognition_vosk.py")
        
    except Exception as e:
        print_color(Colors.RED, f"❌ 解压失败：{e}")
        sys.exit(1)

def main():
    print_color(Colors.BLUE, "🎤 Vosk 模型下载工具")
    print("")
    print("这将下载中文语音识别模型（约 50MB）")
    print("")
    print("⚠️  注意:")
    print("  - 首次下载需要几分钟（取决于网络）")
    print("  - 下载后无需重复下载")
    print("  - 模型完全离线使用，无需网络")
    print("")
    
    choice = input("是否继续下载？(y/n): ").strip().lower()
    
    if choice == 'y':
        download_model()
    else:
        print("已取消")

if __name__ == "__main__":
    main()
