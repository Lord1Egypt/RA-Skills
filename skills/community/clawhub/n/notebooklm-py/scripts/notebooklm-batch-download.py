#!/usr/bin/env python3
"""
notebooklm-batch-download.py - 批量下载笔记本中的所有内容
"""

import subprocess
import sys
import json
import os
import argparse

def get_notebook_metadata():
    """获取笔记本元数据"""
    result = subprocess.run(
        ["notebooklm", "metadata", "--json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ 错误: {result.stderr}")
        return None
    return json.loads(result.stdout)

def download_all_artifacts(output_dir: str):
    """下载所有类型的内容"""
    os.makedirs(output_dir, exist_ok=True)
    
    artifact_types = [
        ("audio", "mp3", "audio"),
        ("video", "mp4", "video"),
        ("cinematic-video", "mp4", "cinematic"),
        ("slide-deck", "pdf", "slides"),
        ("infographic", "png", "infographic"),
        ("mind-map", "json", "mindmap"),
        ("data-table", "csv", "data"),
    ]
    
    downloaded = []
    
    for artifact_type, ext, folder in artifact_types:
        try:
            output_path = os.path.join(output_dir, f"{folder}.{ext}")
            result = subprocess.run(
                ["notebooklm", "download", artifact_type, output_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                downloaded.append(output_path)
                print(f"✅ 已下载: {output_path}")
            else:
                print(f"⚠️  {artifact_type} 不可用")
        except Exception as e:
            print(f"⚠️  下载 {artifact_type} 失败: {e}")
    
    # 下载测验和记忆卡片（多格式）
    for artifact_type in ["quiz", "flashcards"]:
        for fmt in ["json", "markdown"]:
            try:
                output_path = os.path.join(output_dir, f"{artifact_type}.{fmt}")
                result = subprocess.run(
                    ["notebooklm", "download", artifact_type, "--format", fmt, output_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    downloaded.append(output_path)
                    print(f"✅ 已下载: {output_path}")
            except Exception as e:
                pass
    
    return downloaded

def main():
    parser = argparse.ArgumentParser(description="批量下载 NotebookLM 内容")
    parser.add_argument("-o", "--output", default="./notebooklm-output", help="输出目录")
    args = parser.parse_args()
    
    print("📦 NotebookLM 批量下载工具\n")
    
    # 获取元数据
    print("📋 获取笔记本信息...")
    metadata = get_notebook_metadata()
    if metadata:
        print(f"笔记本: {metadata.get('name', 'Unknown')}")
        print(f"来源数量: {len(metadata.get('sources', []))}\n")
    
    # 下载内容
    print("⬇️  开始下载...\n")
    downloaded = download_all_artifacts(args.output)
    
    print(f"\n✅ 完成！共下载 {len(downloaded)} 个文件到 {args.output}/")

if __name__ == "__main__":
    main()
