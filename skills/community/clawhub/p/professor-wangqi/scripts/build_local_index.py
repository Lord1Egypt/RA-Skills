"""
构建本地向量索引（支持ChromaDB）

功能：
1. 递归扫描知识卡目录
2. 使用本地Embedding模型生成向量
3. 存入ChromaDB本地向量库
4. 支持手动覆盖合并

配置：
- 从项目根目录的.env读取配置
- EMBEDDING_MODEL: embedding模型名称
- EMBEDDING_BASE_URL: 本地embedding服务地址
- EMBEDDING_API_KEY: API密钥
- EMBEDDING_DIMENSIONS: 向量维度

依赖：
- chromadb: 本地向量数据库
- openai: 用于调用embedding API

使用：
    python build_local_index.py --cards data/cards/ --collection wangqi_knowledge
    python build_local_index.py --cards data/cards/ --overrides data/overrides/
"""

import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from runtime_paths import DEFAULT_CARDS_DIR, DEFAULT_PERSIST_DIR, load_runtime_env

# 加载.env配置
load_runtime_env()

try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    print("ERROR: chromadb is required. Install with: pip install chromadb")

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("ERROR: openai is required. Install with: pip install openai")

# Try to import card_merger for override support
try:
    from card_merger import CardMerger
    HAS_MERGER = True
except ImportError:
    HAS_MERGER = False


class LocalEmbeddingFunction:
    """
    本地Embedding函数（调用LM Studio的embedding接口）
    """
    
    def __init__(self):
        api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        self.batch_size = int(os.getenv("EMBEDDING_BATCH_SIZE", "16"))
        self.max_retries = int(os.getenv("EMBEDDING_MAX_RETRIES", "2"))
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        print(f"Embedding model: {self.model}")
        print(f"Embedding service: {base_url}")

    def _embed_batch(self, batch: List[str], depth: int = 0) -> List[List[float]]:
        """Embed a batch, recursively splitting it when the service rejects larger payloads."""
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    wait_seconds = attempt + 1
                    print(
                        f"WARNING: Embedding batch of {len(batch)} failed "
                        f"(attempt {attempt + 1}/{self.max_retries + 1}): {e}"
                    )
                    print(f"Retrying in {wait_seconds}s...")
                    time.sleep(wait_seconds)

        if len(batch) > 1:
            midpoint = max(1, len(batch) // 2)
            print(
                f"WARNING: Splitting embedding batch of {len(batch)} into "
                f"{midpoint} + {len(batch) - midpoint} after repeated failures"
            )
            return self._embed_batch(batch[:midpoint], depth + 1) + self._embed_batch(batch[midpoint:], depth + 1)

        raise RuntimeError(f"Embedding service unavailable: {last_error}")
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """ChromaDB要求的接口"""
        embeddings = []
        
        for i in range(0, len(input), self.batch_size):
            batch = input[i:i + self.batch_size]
            try:
                embeddings.extend(self._embed_batch(batch))
            except Exception as last_error:
                print(f"ERROR: Failed to generate embeddings: {last_error}")
                print(f"ERROR: Embedding service at {self.client.base_url} is not reachable")
                print(f"ERROR: Cannot continue without embeddings. Please check:")
                print(f"  1. LM Studio server is running at the configured BASE_URL")
                print(f"  2. The embedding model '{self.model}' is loaded")
                print(f"  3. EMBEDDING_API_KEY and EMBEDDING_BASE_URL are correctly set in .env")
                print(f"  4. EMBEDDING_BATCH_SIZE can be reduced if the service is unstable")
                raise RuntimeError(f"Embedding service unavailable: {last_error}")
        
        return embeddings


def load_cards(cards_dir: str, overrides_dir: str = None, use_overrides: bool = True) -> List[Dict]:
    """
    递归加载知识卡，可选应用手动覆盖
    
    Args:
        cards_dir: 知识卡目录
        overrides_dir: 覆盖文件目录
        use_overrides: 是否应用覆盖
    
    Returns:
        知识卡列表（已合并覆盖）
    """
    cards_path = Path(cards_dir)
    cards = []
    
    # Initialize merger if overrides are enabled
    merger = None
    if use_overrides and overrides_dir and HAS_MERGER:
        merger = CardMerger(overrides_dir=overrides_dir, cards_dir=cards_dir)
        print(f"Using overrides from: {overrides_dir}")
    
    for json_file in cards_path.rglob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                card = json.load(f)
                card["_source_path"] = str(json_file)
                
                # Apply override if available
                if merger:
                    card = merger.merge_card(card)
                
                cards.append(card)
        except Exception as e:
            print(f"Warning: Failed to load {json_file}: {e}")
    
    print(f"Loaded {len(cards)} knowledge cards")
    
    # Report override stats
    if merger:
        override_count = sum(1 for c in cards if c.get("_merge_info", {}).get("has_override"))
        if override_count > 0:
            print(f"  - {override_count} cards with manual overrides applied")
    
    return cards


def extract_content(card: Dict) -> str:
    """提取知识卡内容用于索引"""
    parts = []
    
    # 标题
    if card.get("title"):
        parts.append(f"【标题】{card['title']}")
    
    # 摘要/结论
    if card.get("abstract"):
        parts.append(f"【摘要】{card['abstract']}")
    if card.get("conclusions"):
        parts.append(f"【结论】{card['conclusions']}")
    
    # 知识点
    for kp in card.get("knowledge_points", []):
        content = kp.get("content", "")
        if content:
            parts.append(f"【知识点】{content}")
    
    # 临床见解
    if card.get("clinical_insights"):
        parts.append(f"【临床见解】{card['clinical_insights']}")
    
    # 诊疗经验特有字段
    diag = card.get("diagnostic_approach", {})
    if diag.get("key_points"):
        parts.append(f"【辨证要点】{diag['key_points']}")
    
    treat = card.get("treatment_approach", {})
    if treat.get("principle"):
        parts.append(f"【治则】{treat['principle']}")
    if treat.get("main_formula"):
        parts.append(f"【主方】{treat['main_formula']}")
    
    # 相关体质/疾病
    if card.get("related_constitutions"):
        parts.append(f"【相关体质】{', '.join(card['related_constitutions'])}")
    if card.get("related_diseases"):
        parts.append(f"【相关疾病】{', '.join(card['related_diseases'])}")
    
    # 研究焦点
    focus = card.get("research_focus", {})
    if focus.get("constitution_type"):
        parts.append(f"【研究体质】{', '.join(focus['constitution_type'])}")
    if focus.get("disease"):
        parts.append(f"【研究疾病】{', '.join(focus['disease'])}")
    
    # 结果
    results = card.get("results", {})
    if results.get("main_findings"):
        parts.append(f"【主要发现】{results['main_findings']}")
    
    return "\n".join(parts)


def build_index(
    cards_dir: str = None,
    collection_name: str = "wangqi_knowledge",
    persist_dir: str = None,
    overrides_dir: str = None,
    use_overrides: bool = True
):
    """
    构建ChromaDB向量索引
    
    Args:
        cards_dir: 知识卡目录
        collection_name: 集合名称
        persist_dir: 持久化目录
        overrides_dir: 覆盖文件目录
        use_overrides: 是否应用覆盖
    """
    # Set defaults
    if cards_dir is None:
        cards_dir = DEFAULT_CARDS_DIR
    if persist_dir is None:
        persist_dir = DEFAULT_PERSIST_DIR
    
    if not HAS_CHROMA:
        raise RuntimeError("chromadb is required")
    
    # 1. 初始化ChromaDB
    print(f"Initializing ChromaDB at {persist_dir}")
    client = chromadb.PersistentClient(path=persist_dir)
    
    # 2. 创建或获取集合
    embedding_func = LocalEmbeddingFunction()
    
    # 删除已存在的集合
    try:
        client.delete_collection(collection_name)
        print(f"Deleted existing collection: {collection_name}")
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "王琦教授中医体质知识库"}
    )
    print(f"Created collection: {collection_name}")
    
    # 3. 加载知识卡（带覆盖支持）
    cards = load_cards(cards_dir, overrides_dir, use_overrides)
    
    if not cards:
        print("No cards found. Exiting.")
        return
    
    # 4. 准备数据
    ids = []
    documents = []
    metadatas = []
    
    for card in cards:
        card_id = card.get("card_id", card["_source_path"])
        content = extract_content(card)
        
        if len(content) < 50:
            print(f"Warning: card {card_id} has short content, skipping")
            continue
        
        ids.append(card_id)
        documents.append(content)
        
        # Build metadata (use merged values, no confidence info)
        metadatas.append({
            "source_type": card.get("source_type", ""),
            "title": card.get("title", "")[:200],
            "language": card.get("language", "zh"),
            "source_file": card.get("source_file", ""),
            "year": str(card.get("year", "")),
            "has_override": str(card.get("_merge_info", {}).get("has_override", False)),
        })
    
    # 5. 批量插入（手动生成embeddings）
    batch_size = 100
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_docs = documents[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]

        # 手动生成embeddings
        batch_embeddings = embedding_func(batch_docs)

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            embeddings=batch_embeddings,
            metadatas=batch_meta
        )
        print(f"Added {i + len(batch_ids)}/{len(ids)} documents")
    
    print(f"\nIndex built successfully!")
    print(f"  Collection: {collection_name}")
    print(f"  Documents: {len(ids)}")
    print(f"  Persist dir: {persist_dir}")


def query_index(
    query: str,
    collection_name: str = "wangqi_knowledge",
    persist_dir: str = None,
    n_results: int = 5
):
    """
    查询向量索引
    
    Args:
        query: 查询文本
        collection_name: 集合名称
        persist_dir: 持久化目录
        n_results: 返回结果数量
    """
    # Set default
    if persist_dir is None:
        persist_dir = DEFAULT_PERSIST_DIR
    
    client = chromadb.PersistentClient(path=persist_dir)
    embedding_func = LocalEmbeddingFunction()
    
    collection = client.get_collection(
        name=collection_name,
        embedding_function=embedding_func
    )
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    print(f"\nQuery: {query}")
    print("=" * 50)
    
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ), 1):
        print(f"\n[{i}] Score: {1 - dist:.4f}")
        print(f"    Title: {meta.get('title', 'N/A')}")
        print(f"    Type: {meta.get('source_type', 'N/A')}")
        print(f"    Content: {doc[:200]}...")


def main():
    parser = argparse.ArgumentParser(description="Build local vector index with ChromaDB")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Knowledge cards directory")
    parser.add_argument("--collection", default="wangqi_knowledge", help="Collection name")
    parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR, help="Persist directory")
    parser.add_argument("--overrides", default=None, help="Overrides directory (default: data/overrides)")
    parser.add_argument("--no-overrides", action="store_true", help="Disable override merging")
    parser.add_argument("--query", help="Test query after building index")
    
    args = parser.parse_args()
    
    # Set default overrides directory
    overrides_dir = args.overrides
    if overrides_dir is None and not args.no_overrides:
        # Default to data/overrides relative to cards dir
        cards_path = Path(args.cards)
        if "cards" in str(cards_path):
            overrides_dir = str(cards_path.parent / "overrides")
    
    # 构建索引
    build_index(
        cards_dir=args.cards,
        collection_name=args.collection,
        persist_dir=args.persist_dir,
        overrides_dir=overrides_dir,
        use_overrides=not args.no_overrides
    )
    
    # 测试查询
    if args.query:
        query_index(
            query=args.query,
            collection_name=args.collection,
            persist_dir=args.persist_dir
        )


if __name__ == "__main__":
    main()
