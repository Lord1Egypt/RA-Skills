#!/usr/bin/env python3
"""
记忆系统语义索引构建器
使用 all-MiniLM-L6-v2 模型构建 FAISS 索引，实现真正的语义搜索
"""

import os
import sys
import json
import glob
from pathlib import Path

# 添加 local-memory 的 venv 到路径
venv_path = Path.home() / ".openclaw" / "workspace" / "skills" / "local-memory" / "venv"
if (venv_path / "bin" / "activate").exists():
    sys.path.insert(0, str(venv_path / "lib" / "python3.11" / "site-packages"))

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    from datetime import datetime
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    print("请运行：pip install sentence-transformers faiss-cpu numpy")
    sys.exit(1)

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = WORKSPACE / "MEMORY.md"
INDEX_DIR = WORKSPACE / "index"
MODEL_PATH = Path.home() / ".openclaw" / "workspace" / "skills" / "local-memory" / "models" / "all-MiniLM-L6-v2"

def load_memory_documents():
    """加载所有记忆文档"""
    documents = []
    metadata = []
    
    # 加载 MEMORY.md
    if MEMORY_MD.exists():
        content = MEMORY_MD.read_text(encoding='utf-8')
        documents.append(content)
        metadata.append({
            "source": "MEMORY.md",
            "type": "long_term",
            "timestamp": datetime.now().isoformat()
        })
    
    # 加载 daily logs
    if MEMORY_DIR.exists():
        for daily_file in sorted(MEMORY_DIR.glob("*.md")):
            content = daily_file.read_text(encoding='utf-8')
            documents.append(content)
            metadata.append({
                "source": daily_file.name,
                "type": "daily",
                "timestamp": datetime.now().isoformat()
            })
    
    return documents, metadata

def build_index(documents):
    """构建 FAISS 索引"""
    print(f"📚 加载模型：{MODEL_PATH}")
    model = SentenceTransformer(str(MODEL_PATH))
    
    print(f"📝 处理 {len(documents)} 个文档...")
    embeddings = model.encode(documents, show_progress_bar=True)
    
    # 构建 FAISS 索引
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    
    return index, model

def save_index(index, model, metadata):
    """保存索引和元数据"""
    INDEX_DIR.mkdir(exist_ok=True)
    
    # 保存 FAISS 索引
    faiss.write_index(index, str(INDEX_DIR / "memory_index.faiss"))
    
    # 保存元数据
    with open(INDEX_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # 保存模型配置（可选，用于后续加载）
    with open(INDEX_DIR / "config.json", "w", encoding="utf-8") as f:
        json.dump({
            "model_path": str(MODEL_PATH),
            "created_at": datetime.now().isoformat(),
            "num_documents": len(metadata)
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 索引已保存到 {INDEX_DIR}")
    print(f"   - memory_index.faiss: FAISS 索引")
    print(f"   - metadata.json: 文档元数据")
    print(f"   - config.json: 配置信息")

def main():
    print("🚀 开始构建记忆系统语义索引...")
    print("=" * 50)
    
    # 加载文档
    documents, metadata = load_memory_documents()
    if not documents:
        print("❌ 未找到任何记忆文档")
        sys.exit(1)
    
    print(f"📄 找到 {len(documents)} 个文档:")
    for meta in metadata:
        print(f"   - {meta['source']} ({meta['type']})")
    
    # 构建索引
    index, model = build_index(documents)
    
    # 保存索引
    save_index(index, model, metadata)
    
    print("=" * 50)
    print("✅ 记忆索引构建完成！")
    print("🎯 现在可以使用 memory_search 进行语义搜索了！")

if __name__ == "__main__":
    main()
