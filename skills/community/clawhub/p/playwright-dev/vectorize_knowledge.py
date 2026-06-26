#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量化 knowledge/ 目录文档脚本
- 读取 knowledge/**/**/*.md 文件
- 调用阿里云 Embedding API 生成向量
- 存入 ChromaDB 独立集合（openclaw_knowledge）
"""

import os
import sys
import hashlib
from pathlib import Path
from openai import OpenAI
import chromadb
from chromadb.config import Settings
import chardet

# 设置控制台编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 配置
WORKSPACE = Path(r"C:\Users\Xiabi\.openclaw\workspace")
CHROMA_PATH = WORKSPACE / "chroma_db"
API_KEY = 'sk-1f3847debc3e492e81f64115b20c6d82'
BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
MODEL = 'text-embedding-v3'
CHUNK_SIZE = 800  # 每段字符数
CHUNK_OVERLAP = 100  # 重叠字符数

# 初始化 OpenAI 客户端（阿里云兼容）
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 初始化 ChromaDB
chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))

# 创建独立的 knowledge 集合
collection = chroma_client.get_or_create_collection(
    name="openclaw_knowledge",
    metadata={"hnsw:space": "cosine"}
)

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding'] or 'utf-8'

def read_file_safe(file_path):
    """安全读取文件，自动检测编码"""
    try:
        # 先尝试 UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 检测编码并重试
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """将文本分块"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start >= len(text):
            break
    return chunks

def get_embedding(text):
    """获取文本的向量嵌入"""
    try:
        response = client.embeddings.create(
            model=MODEL,
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding 错误：{e}")
        return None

def generate_id(text):
    """生成唯一 ID"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def vectorize_file(file_path, doc_type, sub_type=""):
    """向量化单个文件"""
    print(f"处理：{file_path}")
    
    try:
        content = read_file_safe(file_path)
        if not content or len(content.strip()) == 0:
            print(f"  ⚠️ 空文件，跳过")
            return 0
        
        chunks = chunk_text(content)
        print(f"  分成 {len(chunks)} 个片段")
        
        count = 0
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # 跳过太短的片段
                continue
            
            embedding = get_embedding(chunk)
            if embedding:
                doc_id = generate_id(f"{file_path}:{i}")
                collection.upsert(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "source": str(file_path),
                        "doc_type": doc_type,
                        "sub_type": sub_type,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }]
                )
                count += 1
        
        print(f"  ✅ 向量化 {count} 个片段")
        return count
    except Exception as e:
        print(f"  ❌ 错误：{e}")
        return 0

def search_knowledge(query, k=3):
    """搜索知识库"""
    print(f"\n🔍 搜索：'{query}' (top {k})")
    
    query_embedding = get_embedding(query)
    if not query_embedding:
        print("  ❌ 无法生成查询向量")
        return []
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    if results and results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            source = results['metadatas'][0][i]['source']
            doc_type = results['metadatas'][0][i]['doc_type']
            print(f"\n  [{i+1}] 来源：{source}")
            print(f"      类型：{doc_type}")
            print(f"      内容：{doc[:200]}...")
        
        return results
    else:
        print("  ⚠️ 未找到结果")
        return []

def main():
    print("🦞 虾虾的 Knowledge 向量化工作开始！✨")
    print("=" * 60)
    
    total_chunks = 0
    files_processed = 0
    
    # 检查 knowledge/ 目录
    knowledge_dir = WORKSPACE / "knowledge"
    if not knowledge_dir.exists():
        print("❌ knowledge/ 目录不存在！")
        return
    
    print(f"\n📂 Knowledge 目录：{knowledge_dir}")
    print("-" * 60)
    
    # 列出所有子目录
    subdirs = [d for d in knowledge_dir.iterdir() if d.is_dir()]
    print(f"找到 {len(subdirs)} 个子目录:")
    for subdir in subdirs:
        print(f"  - {subdir.name}")
    
    # 向量化所有 Markdown 文件
    print("\n📚 开始向量化 knowledge 文档...")
    print("-" * 60)
    
    md_files = list(knowledge_dir.rglob("*.md"))
    print(f"找到 {len(md_files)} 个 Markdown 文件:")
    
    for file_path in md_files:
        # 确定文档类型
        relative_path = file_path.relative_to(knowledge_dir)
        parts = relative_path.parts
        
        if len(parts) > 1:
            doc_type = f"knowledge_{parts[0]}"
            sub_type = parts[1] if len(parts) > 2 else ""
        else:
            doc_type = "knowledge_root"
            sub_type = ""
        
        chunks = vectorize_file(file_path, doc_type, sub_type)
        total_chunks += chunks
        files_processed += 1
    
    # 统计
    print("\n" + "=" * 60)
    print("🎉 Knowledge 向量化完成！")
    print(f"  处理文件数：{files_processed}")
    print(f"  总片段数：{total_chunks}")
    print(f"  向量维度：1024")
    print(f"  集合名称：openclaw_knowledge")
    print(f"  存储位置：{CHROMA_PATH}")
    print("=" * 60)
    
    # 测试查询
    print("\n🧪 测试知识库搜索...")
    test_queries = [
        "技能配置",
        "AI Agent",
        "云GPU 设置"
    ]
    
    for query in test_queries:
        search_knowledge(query, k=3)
    
    print("\n✨ 虾虾的 Knowledge 向量化工作全部完成！哼～")

if __name__ == "__main__":
    main()
