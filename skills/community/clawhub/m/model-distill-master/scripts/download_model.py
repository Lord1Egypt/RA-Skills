#!/usr/bin/env python3
"""
下载 gemma-4-E4B-it 模型
支持 ModelScope 和 HuggingFace 两种方式
"""

import argparse
from pathlib import Path
import os

def download_from_modelscope(cache_dir="./models"):
    """使用 ModelScope 下载（国内推荐）"""
    print("使用 ModelScope 下载 gemma-4-E4B-it...")

    try:
        from modelscope import snapshot_download
        model_dir = snapshot_download('google/gemma-4-E4B-it', cache_dir=cache_dir)
        print(f"✅ 模型下载完成: {model_dir}")
        return model_dir
    except ImportError:
        print("❌ 未安装 modelscope，请先安装: pip install modelscope")
        return None
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def download_from_huggingface(cache_dir="./models"):
    """使用 HuggingFace 下载"""
    print("使用 HuggingFace 下载 gemma-4-E4B-it...")

    try:
        from huggingface_hub import snapshot_download
        model_dir = snapshot_download('google/gemma-4-E4B-it', cache_dir=cache_dir)
        print(f"✅ 模型下载完成: {model_dir}")
        return model_dir
    except ImportError:
        print("❌ 未安装 huggingface_hub，请先安装: pip install huggingface_hub")
        return None
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="下载 gemma-4-E4B-it 模型")
    parser.add_argument("--source", type=str, default="modelscope",
                        choices=["modelscope", "huggingface"],
                        help="下载源: modelscope(国内快) 或 huggingface")
    parser.add_argument("--cache_dir", type=str, default="./models",
                        help="模型缓存目录")
    args = parser.parse_args()

    # 创建缓存目录
    Path(args.cache_dir).mkdir(parents=True, exist_ok=True)

    if args.source == "modelscope":
        model_dir = download_from_modelscope(args.cache_dir)
        if model_dir is None:
            print("\n尝试使用 HuggingFace...")
            model_dir = download_from_huggingface(args.cache_dir)
    else:
        model_dir = download_from_huggingface(args.cache_dir)
        if model_dir is None:
            print("\n尝试使用 ModelScope...")
            model_dir = download_from_modelscope(args.cache_dir)

    if model_dir:
        print(f"\n模型位置: {model_dir}")
        print(f"您可以在配置中使用: student: \"{model_dir}\"")
    else:
        print("\n❌ 所有下载方式都失败了，请检查网络连接")

if __name__ == "__main__":
    main()
