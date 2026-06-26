#!/usr/bin/env python3
"""Предзагрузка модели Qwen3-TTS."""

import argparse
from huggingface_hub import snapshot_download

MODEL_TYPES = ["Base", "CustomVoice"]
MODEL_SIZES = ["0.6B", "1.7B"]

def download_models(size: str = "0.6B"):
    """Загрузка моделей нужного размера."""
    for model_type in MODEL_TYPES:
        repo_id = f"Qwen/Qwen3-TTS-12Hz-{size}-{model_type}"
        print(f"Downloading {repo_id}...")
        snapshot_download(repo_id)
        print(f"Done: {repo_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", default="0.6B", choices=MODEL_SIZES)
    args = parser.parse_args()
    download_models(args.size)
