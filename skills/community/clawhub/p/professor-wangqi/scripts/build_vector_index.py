"""
向量索引构建脚本

功能：
1. 加载知识卡JSON文件
2. 生成文本嵌入向量
3. 存入向量数据库（支持Milvus/Weaviate/ChromaDB）

配置：
- 从.env读取配置
- 支持本地LM Studio embedding服务

使用：
    python build_vector_index.py --cards data/cards/ --db chroma --collection wangqi_knowledge
"""

import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from runtime_paths import DEFAULT_CARDS_DIR, DEFAULT_PERSIST_DIR, load_runtime_env

# 加载.env配置
load_runtime_env()

# 尝试导入向量数据库客户端
HAS_MILVUS = False
HAS_WEAVIATE = False
HAS_CHROMA = False

try:
    from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
    HAS_MILVUS = True
except ImportError:
    pass

try:
    import weaviate
    HAS_WEAVIATE = True
except ImportError:
    pass

try:
    import chromadb
    HAS_CHROMA = True
except ImportError:
    pass

# 尝试导入OpenAI
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class EmbeddingGenerator:
    """文本嵌入生成器（支持本地LM Studio）"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Args:
            api_key: API密钥（从.env读取）
            model: 嵌入模型名称（从.env读取）
        """
        if not HAS_OPENAI:
            raise RuntimeError("openai library is required for embeddings")
        
        # 从.env读取配置
        self.api_key = api_key or os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        self.base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        self.model = model or os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        self.batch_size = int(os.getenv("EMBEDDING_BATCH_SIZE", "16"))
        self.max_retries = int(os.getenv("EMBEDDING_MAX_RETRIES", "2"))
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        print(f"Embedding model: {self.model}")
        if self.base_url:
            print(f"Embedding service: {self.base_url}")

    def _embed_batch(self, batch: List[str]) -> List[List[float]]:
        """Embed a batch, recursively splitting it after repeated failures."""
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
            return self._embed_batch(batch[:midpoint]) + self._embed_batch(batch[midpoint:])

        raise RuntimeError(f"Embedding batch failed after retries: {last_error}")
    
    def generate(self, text: str) -> List[float]:
        """生成文本嵌入向量"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """批量生成嵌入向量"""
        embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings.extend(self._embed_batch(batch))
        
        return embeddings


class MilvusIndexer:
    """Milvus向量索引器"""
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 19530,
                 collection_name: str = "wangqi_knowledge"):
        """
        Args:
            host: Milvus服务地址
            port: Milvus服务端口
            collection_name: 集合名称
        """
        if not HAS_MILVUS:
            raise RuntimeError("pymilvus is required for Milvus indexing")
        
        self.collection_name = collection_name
        self.host = host
        self.port = port
        self.collection = None
    
    def connect(self):
        """连接到Milvus服务"""
        connections.connect(
            alias="default",
            host=self.host,
            port=self.port
        )
        print(f"Connected to Milvus at {self.host}:{self.port}")
    
    def create_collection(self, dimension: int = 1536):
        """
        创建集合
        
        Args:
            dimension: 向量维度（OpenAI text-embedding-3-small为1536）
        """
        # 如果集合已存在，先删除
        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)
        
        # 定义字段
        fields = [
            FieldSchema(name="card_id", dtype=DataType.VARCHAR, max_length=100, is_primary=True),
            FieldSchema(name="source_type", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=10),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        ]
        
        # 创建集合
        schema = CollectionSchema(fields=fields, description="王琦教授知识库")
        self.collection = Collection(name=self.collection_name, schema=schema)
        
        # 创建索引
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        self.collection.create_index(field_name="embedding", index_params=index_params)
        
        print(f"Created collection: {self.collection_name}")
    
    def insert(self, cards: List[Dict], embeddings: List[List[float]]):
        """
        插入知识卡和嵌入向量
        
        Args:
            cards: 知识卡列表
            embeddings: 嵌入向量列表
        """
        if not self.collection:
            self.collection = Collection(self.collection_name)
        
        # 准备数据
        data = [
            [card["card_id"] for card in cards],
            [card.get("source_type", "") for card in cards],
            [card.get("title", "")[:500] for card in cards],
            [self._extract_content(card)[:5000] for card in cards],
            [card.get("language", "zh") for card in cards],
            embeddings
        ]
        
        # 插入数据
        self.collection.insert(data)
        self.collection.flush()
        
        print(f"Inserted {len(cards)} records")
    
    def search(self, 
               query_embedding: List[float],
               top_k: int = 5,
               filter_expr: Optional[str] = None) -> List[Dict]:
        """
        向量检索
        
        Args:
            query_embedding: 查询向量
            top_k: 返回结果数量
            filter_expr: 过滤表达式
        
        Returns:
            检索结果列表
        """
        if not self.collection:
            self.collection = Collection(self.collection_name)
        
        self.collection.load()
        
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 16}}
        
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=filter_expr,
            output_fields=["card_id", "source_type", "title", "content", "language"]
        )
        
        return [
            {
                "card_id": hit.entity.get("card_id"),
                "source_type": hit.entity.get("source_type"),
                "title": hit.entity.get("title"),
                "content": hit.entity.get("content"),
                "language": hit.entity.get("language"),
                "score": hit.distance
            }
            for hit in results[0]
        ]
    
    def _extract_content(self, card: Dict) -> str:
        """
        提取知识卡的主要内容用于索引
        
        改进：从多个字段提取内容，确保诊疗经验卡也能有足够内容
        """
        parts = []
        
        # 1. 标题（始终包含）
        if card.get("title"):
            parts.append(f"【标题】{card['title']}")
        
        # 2. 摘要/结论
        if card.get("abstract"):
            parts.append(f"【摘要】{card['abstract']}")
        if card.get("conclusions"):
            parts.append(f"【结论】{card['conclusions']}")
        
        # 3. 知识点
        for kp in card.get("knowledge_points", []):
            content = kp.get("content", "")
            if content:
                parts.append(f"【知识点】{content}")
        
        # 4. 临床见解
        if card.get("clinical_insights"):
            parts.append(f"【临床见解】{card['clinical_insights']}")
        
        # 5. 诊疗经验特有字段
        # 诊断要点
        diag = card.get("diagnostic_approach", {})
        if diag.get("key_points"):
            parts.append(f"【辨证要点】{diag['key_points']}")
        
        # 治疗方案
        treat = card.get("treatment_approach", {})
        if treat.get("principle"):
            parts.append(f"【治则】{treat['principle']}")
        if treat.get("main_formula"):
            parts.append(f"【主方】{treat['main_formula']}")
        
        # 案例摘要
        for case in card.get("case_studies", [])[:2]:  # 最多取2个案例
            if case.get("diagnosis"):
                parts.append(f"【案例】{case.get('patient_info', '')} {case.get('diagnosis', '')}")
        
        # 6. 相关体质/疾病（用于检索匹配）
        if card.get("related_constitutions"):
            parts.append(f"【相关体质】{', '.join(card['related_constitutions'])}")
        if card.get("related_diseases"):
            parts.append(f"【相关疾病】{', '.join(card['related_diseases'])}")
        
        # 7. 研究焦点（论文特有）
        focus = card.get("research_focus", {})
        if focus.get("constitution_type"):
            parts.append(f"【研究体质】{', '.join(focus['constitution_type'])}")
        if focus.get("disease"):
            parts.append(f"【研究疾病】{', '.join(focus['disease'])}")
        
        # 8. 结果摘要（论文特有）
        results = card.get("results", {})
        if results.get("main_findings"):
            parts.append(f"【主要发现】{results['main_findings']}")
        
        # 合并并返回
        content = "\n".join(parts)
        
        # 如果内容过短，记录警告
        if len(content) < 100:
            print(f"Warning: card {card.get('card_id', 'unknown')} has very short content ({len(content)} chars)")
        
        return content


class WeaviateIndexer:
    """Weaviate向量索引器"""
    
    def __init__(self, 
                 url: str = "http://localhost:8080",
                 class_name: str = "WangQiKnowledge"):
        """
        Args:
            url: Weaviate服务地址
            class_name: 类名称
        """
        if not HAS_WEAVIATE:
            raise RuntimeError("weaviate-client is required for Weaviate indexing")
        
        self.url = url
        self.class_name = class_name
        self.client = None
    
    def connect(self):
        """连接到Weaviate服务"""
        # 使用传入的URL，而不是硬编码
        import weaviate
        from weaviate.connect import ConnectionParams
        
        # 解析URL
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 8080
        
        self.client = weaviate.WeaviateClient(
            connection=ConnectionParams.from_params(
                http_host=host,
                http_port=port,
                grpc_host=host,
                grpc_port=50051
            )
        )
        self.client.connect()
        print(f"Connected to Weaviate at {self.url}")
    
    def create_schema(self):
        """创建schema"""
        # 删除已存在的类
        if self.client.collections.exists(self.class_name):
            self.client.collections.delete(self.class_name)
        
        # 创建类
        from weaviate.classes.config import Configure, Property, DataType
        
        self.client.collections.create(
            name=self.class_name,
            properties=[
                Property(name="card_id", data_type=DataType.TEXT),
                Property(name="source_type", data_type=DataType.TEXT),
                Property(name="title", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
                Property(name="language", data_type=DataType.TEXT),
            ],
            # 使用OpenAI嵌入
            vectorizer_config=Configure.Vectorizer.text2vec_openai()
        )
        
        print(f"Created class: {self.class_name}")
    
    def insert(self, cards: List[Dict]):
        """插入知识卡"""
        collection = self.client.collections.get(self.class_name)
        
        with collection.batch.dynamic() as batch:
            for card in cards:
                batch.add_object(
                    properties={
                        "card_id": card["card_id"],
                        "source_type": card.get("source_type", ""),
                        "title": card.get("title", ""),
                        "content": self._extract_content(card),
                        "language": card.get("language", "zh"),
                    }
                )
        
        print(f"Inserted {len(cards)} records")
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        语义检索
        
        Args:
            query: 查询文本
            limit: 返回结果数量
        
        Returns:
            检索结果列表
        """
        collection = self.client.collections.get(self.class_name)
        
        response = collection.query.near_text(
            query=query,
            limit=limit
        )
        
        return [
            {
                "card_id": obj.properties.get("card_id"),
                "source_type": obj.properties.get("source_type"),
                "title": obj.properties.get("title"),
                "content": obj.properties.get("content"),
                "language": obj.properties.get("language"),
                "score": obj.metadata.score if obj.metadata else None
            }
            for obj in response.objects
        ]
    
    def _extract_content(self, card: Dict) -> str:
        """提取知识卡主要内容（复用统一逻辑）"""
        return extract_content_for_index(card)


def load_cards(cards_dir: str) -> List[Dict]:
    """
    加载知识卡JSON文件（递归扫描子目录）
    
    Args:
        cards_dir: 知识卡目录，会递归扫描所有子目录中的*.json文件
    
    Returns:
        知识卡列表
    """
    cards_path = Path(cards_dir)
    cards = []
    
    # 递归扫描所有子目录
    for json_file in cards_path.rglob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                card = json.load(f)
                card["_source_path"] = str(json_file)  # 记录来源路径
                cards.append(card)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse {json_file}: {e}")
            continue
    
    print(f"Loaded {len(cards)} knowledge cards from {cards_dir}")
    return cards


def build_index(cards_dir: str,
               db_type: str = "chroma",
               host: str = "localhost",
               port: int = 19530,
               collection: str = "wangqi_knowledge",
               persist_dir: str = DEFAULT_PERSIST_DIR,
               embedding_api_key: Optional[str] = None):
    """
    构建向量索引
    
    Args:
        cards_dir: 知识卡目录
        db_type: 数据库类型 (chroma/milvus/weaviate)
        host: 服务地址
        port: 服务端口
        collection: 集合/类名称
        persist_dir: ChromaDB持久化目录
        embedding_api_key: API密钥
    """
    # 加载知识卡
    cards = load_cards(cards_dir)
    
    if not cards:
        print("No cards found. Exiting.")
        return
    
    if db_type == "chroma":
        # ChromaDB索引（推荐，无需额外服务）
        if not HAS_CHROMA:
            raise RuntimeError("chromadb is required. Install with: pip install chromadb")
        
        print(f"Building ChromaDB index at {persist_dir}")
        client = chromadb.PersistentClient(path=persist_dir)
        
        embedder = EmbeddingGenerator(api_key=embedding_api_key)
        
        # 删除已存在的集合
        try:
            client.delete_collection(collection)
        except:
            pass
        
        # 创建集合
        coll = client.create_collection(
            name=collection,
            metadata={"description": "王琦教授中医体质知识库"}
        )
        
        # 准备数据
        ids = []
        documents = []
        metadatas = []
        
        for card in cards:
            card_id = card.get("card_id", card.get("_source_path", ""))
            content = extract_content_for_index(card)
            
            if len(content) < 50:
                continue
            
            ids.append(card_id)
            documents.append(content)
            metadatas.append({
                "source_type": card.get("source_type", ""),
                "title": card.get("title", "")[:200],
                "language": card.get("language", "zh"),
                "source_file": card.get("source_file", ""),
                "year": str(card.get("year", "")),
            })
        
        # 批量插入
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_embeddings = embedder.generate_batch(batch_docs)
            coll.add(
                ids=ids[i:i+batch_size],
                documents=batch_docs,
                embeddings=batch_embeddings,
                metadatas=metadatas[i:i+batch_size]
            )
            print(f"Added {min(i+batch_size, len(ids))}/{len(ids)} documents")
        
        print(f"\nChromaDB index built successfully!")
        print(f"  Collection: {collection}")
        print(f"  Documents: {len(ids)}")
        print(f"  Persist dir: {persist_dir}")
        
    elif db_type == "milvus":
        # Milvus索引
        if not HAS_MILVUS:
            raise RuntimeError("pymilvus is required. Install with: pip install pymilvus")
        
        indexer = MilvusIndexer(host=host, port=port, collection_name=collection)
        indexer.connect()
        indexer.create_collection()
        
        embedder = EmbeddingGenerator(api_key=embedding_api_key)
        texts = [indexer._extract_content(card) for card in cards]
        embeddings = embedder.generate_batch(texts)
        
        indexer.insert(cards, embeddings)
        
    elif db_type == "weaviate":
        # Weaviate索引
        if not HAS_WEAVIATE:
            raise RuntimeError("weaviate-client is required. Install with: pip install weaviate-client")
        
        indexer = WeaviateIndexer(url=f"http://{host}:{port}", class_name=collection)
        indexer.connect()
        indexer.create_schema()
        indexer.insert(cards)
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def extract_content_for_index(card: Dict) -> str:
    """提取知识卡内容用于索引（复用已有逻辑）"""
    parts = []
    
    if card.get("title"):
        parts.append(f"【标题】{card['title']}")
    if card.get("abstract"):
        parts.append(f"【摘要】{card['abstract']}")
    if card.get("conclusions"):
        parts.append(f"【结论】{card['conclusions']}")
    
    for kp in card.get("knowledge_points", []):
        content = kp.get("content", "")
        if content:
            parts.append(f"【知识点】{content}")
    
    if card.get("clinical_insights"):
        parts.append(f"【临床见解】{card['clinical_insights']}")
    
    diag = card.get("diagnostic_approach", {})
    if diag.get("key_points"):
        parts.append(f"【辨证要点】{diag['key_points']}")
    
    treat = card.get("treatment_approach", {})
    if treat.get("principle"):
        parts.append(f"【治则】{treat['principle']}")
    if treat.get("main_formula"):
        parts.append(f"【主方】{treat['main_formula']}")
    
    if card.get("related_constitutions"):
        parts.append(f"【相关体质】{', '.join(card['related_constitutions'])}")
    if card.get("related_diseases"):
        parts.append(f"【相关疾病】{', '.join(card['related_diseases'])}")
    
    focus = card.get("research_focus", {})
    if focus.get("constitution_type"):
        parts.append(f"【研究体质】{', '.join(focus['constitution_type'])}")
    if focus.get("disease"):
        parts.append(f"【研究疾病】{', '.join(focus['disease'])}")
    
    results = card.get("results", {})
    if results.get("main_findings"):
        parts.append(f"【主要发现】{results['main_findings']}")
    
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Build vector index for knowledge cards")
    parser.add_argument("--cards", default=DEFAULT_CARDS_DIR, help="Knowledge cards directory")
    parser.add_argument("--db", choices=["chroma", "milvus", "weaviate"], default="chroma", help="Vector database type")
    parser.add_argument("--host", default="localhost", help="Database host")
    parser.add_argument("--port", type=int, default=19530, help="Database port")
    parser.add_argument("--collection", default="wangqi_knowledge", help="Collection/Class name")
    parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR, help="ChromaDB persist directory")
    parser.add_argument("--api-key", help="API key for embeddings (or use .env)")
    
    args = parser.parse_args()
    
    build_index(
        cards_dir=args.cards,
        db_type=args.db,
        host=args.host,
        port=args.port,
        collection=args.collection,
        persist_dir=args.persist_dir,
        embedding_api_key=args.api_key
    )


if __name__ == "__main__":
    main()
