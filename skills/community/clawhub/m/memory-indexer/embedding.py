#!/usr/bin/env python3
"""
Memory Indexer - 向量语义搜索模块

支持多种向量生成方式：
1. HuggingFace 本地模型 (推荐)
2. Ollama 本地模型
3. MiniMax API

用法：
    from embedding import get_embedding, search_semantic
    
    # 获取单条文本向量
    vec = get_embedding("今天天气很好")
    
    # 语义搜索
    results = search_semantic("今天天气怎么样", top_k=5)
"""

import json
import os
import math
from pathlib import Path
from typing import Optional, List

# ============ 配置 ============
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "skills" / "memory-indexer" / "data"
VECTORS_FILE = MEMORY_DIR / "vectors.json"

# 向量模型配置
EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "huggingface")  # huggingface, ollama, minimax
HF_MODEL_NAME = os.environ.get("HF_MODEL_NAME", "BAAI/bge-base-zh-v1.5")  # HuggingFace 模型
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "bge-base-zh-v1.5")  # Ollama 模型
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")  # Ollama 地址
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_API_BASE = "https://api.minimax.chat/v1"

# 缓存模型实例
_model = None


def _get_hf_model():
    """获取或加载 HuggingFace 模型"""
    global _model
    if _model is not None:
        return _model
    
    try:
        from sentence_transformers import SentenceTransformer
        print(f"正在加载 HuggingFace 模型: {HF_MODEL_NAME} ...")
        # CPU 推理，use_gpu=False
        _model = SentenceTransformer(HF_MODEL_NAME, device='cpu')
        print(f"✓ 模型加载成功，向量维度: {_model.get_sentence_embedding_dimension()}")
        return _model
    except Exception as e:
        print(f"加载 HuggingFace 模型失败: {e}")
        return None


def _get_ollama_embedding(text: str) -> Optional[List[float]]:
    """从 Ollama 获取向量"""
    try:
        import urllib.request
        import urllib.error
        
        url = f"{OLLAMA_HOST}/api/embeddings"
        data = {
            "model": OLLAMA_MODEL,
            "prompt": text
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("embedding")
    except Exception as e:
        print(f"Ollama 请求失败: {e}")
        return None


def _get_minimax_embedding(text: str) -> Optional[List[float]]:
    """从 MiniMax API 获取向量"""
    if not MINIMAX_API_KEY:
        print("警告: MINIMAX_API_KEY 未设置")
        return None
    
    try:
        import urllib.request
        import urllib.error
        
        url = f"{MINIMAX_API_BASE}/text/embeddings"
        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "emba-01",
            "input": text
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            if "data" in result and len(result["data"]) > 0:
                return result["data"][0]["embedding"]
            return None
    except Exception as e:
        print(f"MiniMax API 请求失败: {e}")
        return None


def get_embedding(text: str) -> Optional[List[float]]:
    """
    获取文本向量
    
    Args:
        text: 输入文本
        
    Returns:
        向量列表，失败返回 None
    """
    if EMBEDDING_PROVIDER == "huggingface":
        model = _get_hf_model()
        if model:
            return model.encode(text, convert_to_numpy=True).tolist()
        return None
    
    elif EMBEDDING_PROVIDER == "ollama":
        return _get_ollama_embedding(text)
    
    elif EMBEDDING_PROVIDER == "minimax":
        return _get_minimax_embedding(text)
    
    else:
        print(f"未知的向量提供者: {EMBEDDING_PROVIDER}")
        return None


def get_embeddings_batch(texts: List[str]) -> Optional[List[List[float]]]:
    """
    批量获取文本向量
    
    Args:
        texts: 输入文本列表
        
    Returns:
        向量列表，失败返回 None
    """
    if not texts:
        return []
    
    if EMBEDDING_PROVIDER == "huggingface":
        model = _get_hf_model()
        if model:
            # 批量编码
            embeddings = model.encode(texts, convert_to_numpy=True, batch_size=32)
            return embeddings.tolist()
        return None
    
    elif EMBEDDING_PROVIDER == "ollama":
        results = []
        for text in texts:
            vec = _get_ollama_embedding(text)
            if vec:
                results.append(vec)
            else:
                results.append(None)
        return results
    
    elif EMBEDDING_PROVIDER == "minimax":
        # MiniMax 支持批量
        if not MINIMAX_API_KEY:
            print("警告: MINIMAX_API_KEY 未设置")
            return None
        # TODO: 实现 MiniMax 批量接口
        results = []
        for text in texts:
            vec = _get_minimax_embedding(text)
            results.append(vec)
        return results
    
    return None


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算余弦相似度
    """
    if len(vec1) != len(vec2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def ensure_vectors_file():
    """确保向量存储文件存在"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not VECTORS_FILE.exists():
        with open(VECTORS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def load_vectors() -> dict:
    """加载向量索引"""
    ensure_vectors_file()
    with open(VECTORS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_vectors(vectors: dict):
    """保存向量索引"""
    ensure_vectors_file()
    with open(VECTORS_FILE, "w", encoding="utf-8") as f:
        json.dump(vectors, f, ensure_ascii=False, indent=2)


def search_semantic(query: str, top_k: int = 10, min_score: float = 0.3) -> list:
    """
    语义向量搜索
    
    Args:
        query: 查询文本
        top_k: 返回结果数量
        min_score: 最小相似度阈值
        
    Returns:
        搜索结果列表
    """
    # 获取查询向量
    print(f"🔍 向量搜索 (provider: {EMBEDDING_PROVIDER})...")
    query_vec = get_embedding(query)
    if not query_vec:
        print("获取查询向量失败")
        return []
    
    # 加载向量索引
    vectors = load_vectors()
    if not vectors:
        print("向量索引为空")
        return []
    
    # 计算相似度
    results = []
    for filename, data in vectors.items():
        if "vector" not in data:
            continue
        
        score = cosine_similarity(query_vec, data["vector"])
        if score >= min_score:
            results.append({
                "file": filename,
                "score": round(score, 4),
                "preview": data.get("preview", ""),
                "time": data.get("time", "")
            })
    
    # 按相似度降序排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:top_k]


def add_vector(filename: str, content: str, preview: str = "", time: str = ""):
    """
    为记忆添加向量
    """
    vec = get_embedding(content)
    if not vec:
        print(f"为 {filename} 生成向量失败")
        return False
    
    vectors = load_vectors()
    vectors[filename] = {
        "vector": vec,
        "preview": preview[:200] if preview else content[:200],
        "time": time,
        "content": content  # 可选：存储原文
    }
    save_vectors(vectors)
    print(f"✓ 已为 {filename} 生成向量")
    return True


def add_vectors_batch(files: List[str], contents: List[str]):
    """
    批量为记忆添加向量
    """
    if len(files) != len(contents):
        print("错误: 文件列表和内容列表长度不一致")
        return
    
    # 批量获取向量
    vectors = get_embeddings_batch(contents)
    if not vectors:
        print("批量获取向量失败")
        return
    
    # 保存向量
    vectors_data = load_vectors()
    success_count = 0
    for filename, vec, content in zip(files, vectors, contents):
        if vec:
            preview = content[:200]
            vectors_data[filename] = {
                "vector": vec,
                "preview": preview,
                "time": ""
            }
            success_count += 1
    
    save_vectors(vectors_data)
    print(f"✓ 批量生成向量完成，成功 {success_count}/{len(files)} 条")


def get_vector_status() -> dict:
    """获取向量索引状态"""
    vectors = load_vectors()
    return {
        "total": len(vectors),
        "provider": EMBEDDING_PROVIDER,
        "model": HF_MODEL_NAME if EMBEDDING_PROVIDER == "huggingface" else (OLLAMA_MODEL if EMBEDDING_PROVIDER == "ollama" else "minimax"),
        "files": list(vectors.keys())[:10]
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="向量语义搜索模块")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # test 命令
    subparsers.add_parser("test", help="测试向量生成")
    
    # status 命令
    subparsers.add_parser("status", help="查看向量索引状态")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="语义搜索")
    search_parser.add_argument("query", help="查询文本")
    search_parser.add_argument("--top-k", type=int, default=10, help="返回结果数量")
    
    # reindex 命令
    reindex_parser = subparsers.add_parser("reindex", help="批量重新生成向量")
    reindex_parser.add_argument("--memory-dir", help="记忆目录路径")
    
    args = parser.parse_args()
    
    if args.command == "test":
        print("测试向量生成...")
        print(f"Provider: {EMBEDDING_PROVIDER}")
        vec = get_embedding("今天天气很好")
        if vec:
            print(f"✓ 向量生成成功，维度: {len(vec)}")
            print(f"前5维: {vec[:5]}")
        else:
            print("✗ 向量生成失败")
            
    elif args.command == "status":
        status = get_vector_status()
        print(f"向量索引: {status['total']} 条")
        print(f"Provider: {status['provider']}")
        print(f"Model: {status['model']}")
        if status['files']:
            print(f"示例文件: {status['files'][:5]}")
            
    elif args.command == "search":
        results = search_semantic(args.query, top_k=args.top_k)
        if results:
            print(f"\n找到 {len(results)} 条相关记忆:\n")
            for r in results:
                print(f"  {r['file']} (相似度: {r['score']})")
                if r['preview']:
                    print(f"    摘要: {r['preview'][:80]}...")
                print()
        else:
            print("未找到相关内容")
            
    elif args.command == "reindex":
        memory_dir = Path(args.memory_dir) if args.memory_dir else WORKSPACE / "memory"
        print(f"从 {memory_dir} 重新生成向量...")
        
        files = []
        contents = []
        for f in Path(memory_dir).glob("*.md"):
            files.append(f.name)
            try:
                contents.append(f.read_text(encoding="utf-8")[:1000])
            except:
                contents.append("")
        
        print(f"找到 {len(files)} 个记忆文件")
        add_vectors_batch(files, contents)
        
    else:
        parser.print_help()
