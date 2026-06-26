"""
Meta-Skill Generator - 向量嵌入搜索 (镜像版)
"""
import os
import json
from pathlib import Path

# 设置镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

try:
    from sentence_transformers import SentenceTransformer
    print("[OK] Import success!")
    
    # 加载模型
    print("[OK] Loading model from mirror...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("[OK] Model loaded!")
    
    # 测试
    print("\n=== Test ===")
    embeddings = model.encode(["truthfulness skill", "skill manager", "weather"])
    print(f"Embeddings shape: {embeddings.shape}")
    print("[OK] Vector search ready!")
    
except Exception as e:
    print(f"[ERROR] {e}")
