#!/usr/bin/env python3
"""
检查 Ollama 状态和模型占用
"""

import os
import sys
import json
import shutil
from pathlib import Path

def get_ollama_path() -> Path:
    """获取 Ollama 模型路径"""
    # 检查环境变量
    env_path = os.environ.get("OLLAMA_MODELS")
    if env_path:
        return Path(env_path)
    
    # 默认路径
    user_home = Path.home()
    default_path = user_home / ".ollama" / "models"
    return default_path

def get_disk_free_space(drive: str) -> dict:
    """获取磁盘可用空间"""
    total, used, free = shutil.disk_usage(drive)
    return {
        "drive": drive,
        "total_gb": round(total / (1024**3), 2),
        "used_gb": round(used / (1024**3), 2),
        "free_gb": round(free / (1024**3), 2),
        "free_percent": round((free / total) * 100, 1)
    }

def scan_model_size(path: Path) -> int:
    """扫描模型目录大小"""
    total_size = 0
    if path.exists():
        for item in path.rglob("*"):
            try:
                if item.is_file():
                    total_size += item.stat().st_size
            except (PermissionError, OSError):
                continue
    return total_size

def check_ollama_status():
    """检查 Ollama 状态"""
    print("\n" + "="*60)
    print("  Ollama 状态检查")
    print("="*60)
    
    # 当前模型路径
    model_path = get_ollama_path()
    print(f"\n【模型路径】")
    print(f"  位置：{model_path}")
    print(f"  存在：{'是' if model_path.exists() else '否'}")
    
    # 环境变量
    env_path = os.environ.get("OLLAMA_MODELS")
    print(f"\n【环境变量】")
    if env_path:
        print(f"  OLLAMA_MODELS = {env_path}")
    else:
        print(f"  OLLAMA_MODELS = (未设置，使用默认路径)")
    
    # 模型大小
    if model_path.exists():
        size = scan_model_size(model_path)
        size_gb = round(size / (1024**3), 2)
        print(f"\n【模型占用】")
        print(f"  总大小：{size_gb} GB")
        
        # 统计模型文件
        model_files = list(model_path.glob("blobs/*"))
        print(f"  模型文件数：{len(model_files)}")
    else:
        print(f"\n  警告：模型目录不存在")
    
    # 磁盘空间
    drive = model_path.drive if model_path.drive else "C:"
    if not drive:
        drive = "C:"
    
    disk_info = get_disk_free_space(drive)
    print(f"\n【磁盘空间】({drive})")
    print(f"  总容量：{disk_info['total_gb']} GB")
    print(f"  已使用：{disk_info['used_gb']} GB")
    print(f"  剩余：{disk_info['free_gb']} GB ({disk_info['free_percent']}%)")
    
    # 建议
    print(f"\n【建议】")
    if disk_info['free_gb'] < 20:
        print(f"  ⚠️  {drive}盘空间紧张，建议迁移模型到其他盘")
    elif disk_info['free_gb'] < 50:
        print(f"  🟡 {drive}盘空间一般，可以考虑迁移")
    else:
        print(f"  ✅ {drive}盘空间充足")
    
    print("\n" + "="*60)
    
    return {
        "model_path": str(model_path),
        "env_path": env_path,
        "exists": model_path.exists(),
        "size_gb": round(size / (1024**3), 2) if model_path.exists() else 0,
        "disk_info": disk_info
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="检查 Ollama 状态")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    result = check_ollama_status()
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
