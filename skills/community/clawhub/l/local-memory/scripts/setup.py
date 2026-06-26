# -*- coding: utf-8 -*-
"""一键安装 local-memory 依赖：torch CPU + chromadb + sentence-transformers + certifi，并预下载 BGE-small-zh-v1.5 模型。"""

import subprocess
import sys
import json


def run(cmd, desc):
    print(json.dumps({"step": desc, "status": "running"}, ensure_ascii=False))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(json.dumps({"step": desc, "status": "error", "message": result.stderr.strip()}, ensure_ascii=False))
        sys.exit(1)
    print(json.dumps({"step": desc, "status": "ok"}, ensure_ascii=False))


def main():
    py = sys.executable

    # 1. torch CPU
    run(
        [py, "-m", "pip", "install", "torch", "--index-url", "https://download.pytorch.org/whl/cpu"],
        "安装 torch (CPU)",
    )

    # 2. chromadb + sentence-transformers + certifi
    run(
        [py, "-m", "pip", "install", "chromadb", "sentence-transformers", "certifi"],
        "安装 chromadb、sentence-transformers 和 certifi",
    )

    # 3. 预下载模型
    print(json.dumps({"step": "预下载 BGE-small-zh-v1.5 模型", "status": "running"}, ensure_ascii=False))
    try:
        from sentence_transformers import SentenceTransformer
        SentenceTransformer("BAAI/bge-small-zh-v1.5")
        print(json.dumps({"step": "预下载 BGE-small-zh-v1.5 模型", "status": "ok"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"step": "预下载 BGE-small-zh-v1.5 模型", "status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps({"status": "ok", "message": "所有依赖安装完成，模型已下载"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
