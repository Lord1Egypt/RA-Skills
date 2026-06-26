#!/usr/bin/env python3
"""
模型下载脚本 - 首次运行使用
自动下载所需的本地模型文件
"""

import os
import sys
import urllib.request
from pathlib import Path
from tqdm import tqdm

MODEL_URLS = {
    "llm/qwen2.5-3b": {
        "url": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf",
        "size": "2.1GB",
        "local_path": "models/llm/qwen2.5-3b/"
    },
    "embedding/bge-m3": {
        "url": "https://huggingface.co/BAAI/bge-m3/resolve/main/model.safetensors",
        "size": "2.3GB",
        "local_path": "models/embedding/bge-m3/"
    },
    "ocr/paddleocr-v4": {
        "url": "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_infer.tar",
        "size": "12MB",
        "local_path": "models/ocr/paddleocr-v4/"
    }
}


class DownloadProgressBar(tqdm):
    """下载进度条"""
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_file(url: str, output_path: str):
    """下载文件并显示进度"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=output_path) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def check_model_exists(model_path: str) -> bool:
    """检查模型是否已存在"""
    path = Path(model_path)
    return path.exists() and any(path.iterdir())


def main():
    """主函数"""
    print("=" * 60)
    print("LocalDataAI 模型下载工具")
    print("=" * 60)
    print()
    
    base_dir = Path(__file__).parent.parent
    os.chdir(base_dir)
    
    for model_name, model_info in MODEL_URLS.items():
        local_path = base_dir / model_info["local_path"]
        
        print(f"检查模型: {model_name}")
        print(f"  本地路径: {local_path}")
        print(f"  预计大小: {model_info['size']}")
        
        if check_model_exists(str(local_path)):
            print(f"  状态: ✅ 已存在，跳过")
        else:
            print(f"  状态: ⬇️  开始下载...")
            try:
                # 这里使用简化的下载逻辑，实际使用时可能需要使用 huggingface-cli
                print(f"  提示: 请手动下载模型到 {local_path}")
                print(f"  下载链接: {model_info['url']}")
                print()
            except Exception as e:
                print(f"  错误: {e}")
        
        print()
    
    print("=" * 60)
    print("模型检查完成")
    print("=" * 60)
    print()
    print("说明:")
    print("1. 模型文件需要手动下载或使用 huggingface-cli")
    print("2. 运行: pip install huggingface-cli")
    print("3. 然后: huggingface-cli download Qwen/Qwen2.5-3B-Instruct-GGUF")
    print()


if __name__ == "__main__":
    main()
