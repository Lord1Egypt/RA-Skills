#!/usr/bin/env python3
"""
memory-booster 语义索引构建器
首次运行：对所有日记文件 + MEMORY.md 建向量索引
后续运行：增量更新（只索引新文件/新内容）
"""
import os
import re
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# 国内 HuggingFace 镜像（加速模型下载）
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# 从 config_loader 获取路径
from config_loader import load_config, get_memory_files
MEMORY_DIRS_RAW, CHROMA_DB_DIR = load_config()
MEMORY_DIRS = [Path(d) for d in MEMORY_DIRS_RAW]
INDEX_DIR = Path(CHROMA_DB_DIR)

# ---- Helpers (get_memory_files 已迁移到 config_loader) ----


def split_into_chunks(text, max_chars=500):
    """按段落拆分文本为 chunks"""
    # 按双换行拆分段落
    paragraphs = re.split(r'\n\n+', text)
    chunks = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para) <= max_chars:
            chunks.append(para)
        else:
            # 长段落按句子拆分
            sentences = re.split(r'(?<=[。！？.!?])\s*', para)
            current = ""
            for sent in sentences:
                if len(current) + len(sent) <= max_chars:
                    current += sent
                else:
                    if current.strip():
                        chunks.append(current.strip())
                    current = sent
            if current.strip():
                chunks.append(current.strip())
    return chunks


def file_hash(filepath):
    """计算文件内容哈希，用于增量检测"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---- ChromaDB Index ----

def build_index(force=False):
    """构建/更新语义索引"""
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError:
        print("⚠️ chromadb 未安装，运行: pip3 install chromadb")
        return None

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("⚠️ sentence-transformers 未安装，运行: pip3 install sentence-transformers")
        return None

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    # 初始化 ChromaDB
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    collection_name = "workbuddy_memory"

    # 检查是否需要重建
    try:
        collection = client.get_collection(collection_name)
        existing_count = collection.count()
        if existing_count > 0 and not force:
            print(f"✅ 索引已存在 ({existing_count} 条)，跳过。使用 --force 强制重建。")
            return collection
    except Exception:
        pass

    # 删除旧 collection（如果存在）
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    # 加载嵌入模型
    print("📥 加载嵌入模型 (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 扫描文件
    files = get_memory_files()
    print(f"📂 找到 {len(files)} 个记忆文件")

    if not files:
        print("⚠️ 没有找到记忆文件")
        return None

    # 创建新 collection（使用 cosine 距离）
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    # 逐文件索引
    total_chunks = 0
    for fpath in files:
        fname = fpath.name
        try:
            with open(fpath, "r") as f:
                content = f.read()
        except Exception as e:
            print(f"  ⚠️ 跳过 {fname}: {e}")
            continue

        chunks = split_into_chunks(content)
        if not chunks:
            continue

        # 批量嵌入
        embeddings = model.encode(chunks, show_progress_bar=False)

        # 提取日期（从文件名）
        try:
            date_str = fname.replace(".md", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            file_date = "unknown"

        chunk_ids = [f"{fname}_c{i}" for i in range(len(chunks))]
        metadatas = [{"file": fname, "date": file_date, "chunk_idx": i, "dir": str(fpath.parent)}
                     for i in range(len(chunks))]

        collection.add(
            ids=chunk_ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        total_chunks += len(chunks)
        print(f"  ✅ {fname}: {len(chunks)} chunks")

    print(f"\n🎉 索引完成！共 {total_chunks} 个 chunks，{len(files)} 个文件")
    return collection


if __name__ == "__main__":
    force = "--force" in sys.argv
    build_index(force=force)
