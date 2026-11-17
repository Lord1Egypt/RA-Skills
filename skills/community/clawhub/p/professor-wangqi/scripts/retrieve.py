"""
检索服务 - 供外部LLM调用的纯检索接口

这个脚本只负责检索，不调用LLM生成回答。
外部LLM（如Claude Code）调用此脚本获取相关知识片段，然后自己生成回答。

Usage:
    # 命令行调用
    python retrieve.py "痰湿质与肥胖"
    python retrieve.py "痰湿质与肥胖" --n-results 10
    
    # 输出JSON格式
    python retrieve.py "痰湿质与肥胖" --format json
    
    # 作为模块导入
    from retrieve import retrieve
    results = retrieve("痰湿质与肥胖")
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from chroma_compat import list_collection_names
from runtime_paths import DEFAULT_PERSIST_DIR, load_runtime_env

# Load environment
load_runtime_env()

try:
    import chromadb
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False
    print("ERROR: chromadb is required. Install with: pip install chromadb")

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class LocalEmbeddingFunction:
    """Local Embedding Function for ChromaDB"""
    
    def __init__(self):
        api_key = os.getenv("EMBEDDING_API_KEY") or os.getenv("API_KEY")
        base_url = os.getenv("EMBEDDING_BASE_URL") or os.getenv("BASE_URL")
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5")
        self.max_retries = int(os.getenv("EMBEDDING_MAX_RETRIES", "2"))
        
        if not api_key or not base_url:
            raise ValueError("EMBEDDING_API_KEY and EMBEDDING_BASE_URL must be set")
        
        self.client = OpenAI(api_key=api_key, base_url=base_url)
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = []
        for text in input:
            last_error = None
            for attempt in range(self.max_retries + 1):
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=[text]
                    )
                    embeddings.append(response.data[0].embedding)
                    last_error = None
                    break
                except Exception as e:
                    last_error = e
                    if attempt < self.max_retries:
                        time.sleep(attempt + 1)
            if last_error is not None:
                # Fail loudly - don't silently return zero vectors
                # This prevents the system from giving seemingly valid but 
                # actually irrelevant answers when embedding service is down
                raise RuntimeError(
                    f"Embedding service failed: {last_error}\n"
                    f"Please check:\n"
                    f"  1. Is the embedding service running at {self.client.base_url}?\n"
                    f"  2. Is the model '{self.model}' available?\n"
                    f"  3. Check EMBEDDING_BASE_URL and EMBEDDING_API_KEY in .env"
                )
        return embeddings


# Default paths relative to script directory
def retrieve(
    query: str,
    collection_name: str = "wangqi_knowledge",
    persist_dir: str = None,
    n_results: int = 5
) -> List[Dict]:
    """
    检索相关知识片段
    
    Args:
        query: 查询文本
        collection_name: ChromaDB集合名称
        persist_dir: ChromaDB持久化目录
        n_results: 返回结果数量
    
    Returns:
        检索结果列表，每个元素包含:
        - content: 文档内容
        - source_type: 来源类型 (paper/clinical_experience)
        - title: 文献标题
        - source_file: 原始文件名
        - distance: 相似度距离（越小越相似）
    """
    # Set default
    if persist_dir is None:
        persist_dir = DEFAULT_PERSIST_DIR
    
    if not HAS_CHROMA:
        raise RuntimeError("chromadb is required")
    
    # 检查目录是否存在
    if not Path(persist_dir).exists():
        raise FileNotFoundError(f"ChromaDB directory not found: {persist_dir}")
    
    # 连接ChromaDB
    client = chromadb.PersistentClient(path=persist_dir)
    
    # 检查集合是否存在
    collections = list_collection_names(client.list_collections())
    if collection_name not in collections:
        raise ValueError(f"Collection '{collection_name}' not found. Available: {collections}")
    
    collection = client.get_collection(name=collection_name)
    
    # 检查是否有文档
    if collection.count() == 0:
        return []
    
    # 生成查询向量
    embedding_func = LocalEmbeddingFunction()
    query_embedding = embedding_func([query])[0]
    
    # 执行检索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    # 格式化结果
    formatted_results = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        formatted_results.append({
            "content": doc,
            "source_type": meta.get("source_type", "unknown"),
            "title": meta.get("title", ""),
            "source_file": meta.get("source_file", ""),
            "year": meta.get("year", ""),
            "language": meta.get("language", "zh"),
            "distance": dist,
            "relevance_score": 1 - dist  # 相似度分数
        })
    
    return formatted_results


def format_as_context(results: List[Dict], include_metadata: bool = True) -> str:
    """
    将检索结果格式化为上下文字符串，供LLM使用
    
    Args:
        results: retrieve()返回的结果列表
        include_metadata: 是否包含元数据
    
    Returns:
        格式化的上下文字符串
    """
    if not results:
        return "(未找到相关参考资料)"
    
    contexts = []
    for i, r in enumerate(results, 1):
        # 证据标签
        if r["source_type"] == "paper":
            tag = "[论文]"
            credibility = "研究证据"
        elif r["source_type"] == "clinical_experience":
            tag = "[诊疗经验]"
            credibility = "临床经验"
        else:
            tag = "[资料]"
            credibility = "参考资料"
        
        # 构建上下文片段
        if include_metadata:
            header = f"{tag} {r['title']}"
            if r.get("year"):
                header += f" ({r['year']})"
            # 添加相关度信息
            relevance = r.get("relevance_score", 0)
            if relevance > 0.5:
                header += f" [高相关度]"
            elif relevance > 0.3:
                header += f" [中等相关度]"
            contexts.append(f"{header}\n{r['content']}")
        else:
            contexts.append(f"{tag}\n{r['content']}")
    
    return "\n\n---\n\n".join(contexts)


def format_for_skill(results: List[Dict]) -> str:
    """
    格式化为适合Skill使用的上下文，包含人格模拟提示
    
    这个格式强调：
    1. 证据来源的可追溯性
    2. 区分教授原文和模型推断
    3. 适合学术回答的结构
    """
    if not results:
        return """(未找到直接相关的参考资料)

【回答建议】
- 请基于王琦教授中医体质学的一般理论框架回答
- 明确标注为 [模型推断]
- 说明"根据现有材料未找到直接依据"
- 提供相关思路供用户参考"""
    
    contexts = []
    contexts.append("【检索到的参考资料】")
    contexts.append("=" * 50)
    
    for i, r in enumerate(results, 1):
        # 证据标签和可信度
        if r["source_type"] == "paper":
            tag = "[论文]"
            credibility_note = "此为研究证据，有数据支撑"
        elif r["source_type"] == "clinical_experience":
            tag = "[诊疗经验]"
            credibility_note = "此为临床经验总结"
        else:
            tag = "[资料]"
            credibility_note = ""
        
        # 构建引用块
        block = []
        block.append(f"\n[{i}] {tag}")
        
        # 标题和来源
        title = r.get("title", "")
        if title:
            block.append(f"标题: {title}")
        
        source_file = r.get("source_file", "")
        if source_file:
            block.append(f"来源: {source_file}")
        
        year = r.get("year", "")
        if year:
            block.append(f"年份: {year}")
        
        # 相关度
        relevance = r.get("relevance_score", 0)
        block.append(f"相关度: {relevance:.1%}")
        
        if credibility_note:
            block.append(f"证据性质: {credibility_note}")
        
        # 内容
        block.append(f"\n内容摘要:")
        content = r.get("content", "")
        # 截取前500字符作为摘要
        if len(content) > 500:
            block.append(f"{content[:500]}...")
        else:
            block.append(content)
        
        contexts.append("\n".join(block))
    
    # 添加使用指南
    contexts.append("\n" + "=" * 50)
    contexts.append("【回答格式要求】")
    contexts.append("""
1. 教授观点：基于检索结果的核心回答
2. 依据出处：列出引用的文献，格式如：
   - [论文] 《文献标题》- 年份
   - [诊疗经验] 《文献标题》
3. 适用边界：说明观点的适用范围和限制
4. 信息层级：标注证据强度
   - [论文] > [诊疗经验] > [知识归纳] > [模型推断]

【人格表达建议】
- 学术严谨但不刻板，循循善诱
- 区分"教授明确论述"与"基于材料的合理归纳"
- 不确定时坦诚说明
- 涉及诊断/剂量时添加安全警示
""")
    
    return "\n".join(contexts)


def format_as_json(results: List[Dict]) -> str:
    """将检索结果格式化为JSON字符串"""
    return json.dumps(results, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="检索王琦教授中医体质知识库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 基本检索
    python retrieve.py "痰湿质与肥胖"
    
    # 指定结果数量
    python retrieve.py "痰湿质与肥胖" --n-results 10
    
    # JSON格式输出
    python retrieve.py "痰湿质与肥胖" --format json
    
    # Skill专用格式（包含人格模拟提示）
    python retrieve.py "痰湿质与肥胖" --format skill
    
    # 只输出内容（用于管道）
    python retrieve.py "痰湿质与肥胖" --format context
        """
    )
    parser.add_argument("query", help="查询文本")
    parser.add_argument("--collection", default="wangqi_knowledge", help="集合名称")
    parser.add_argument("--persist-dir", default=DEFAULT_PERSIST_DIR, help="ChromaDB目录")
    parser.add_argument("--n-results", "-n", type=int, default=5, help="返回结果数量")
    parser.add_argument("--format", "-f", choices=["json", "context", "skill", "simple"], 
                       default="simple", help="输出格式: json(结构化), context(纯文本), skill(含人格提示), simple(易读)")
    
    args = parser.parse_args()
    
    try:
        # 执行检索
        results = retrieve(
            query=args.query,
            collection_name=args.collection,
            persist_dir=args.persist_dir,
            n_results=args.n_results
        )
        
        # 格式化输出
        if args.format == "json":
            print(format_as_json(results))
        
        elif args.format == "skill":
            print(format_for_skill(results))
        
        elif args.format == "context":
            print(format_as_context(results))
        
        else:  # simple
            print(f"找到 {len(results)} 条相关资料:\n")
            for i, r in enumerate(results, 1):
                tag = "[论文]" if r["source_type"] == "paper" else "[诊疗经验]"
                print(f"[{i}] {tag} {r['title']}")
                print(f"    相关度: {r['relevance_score']:.2%}")
                print(f"    来源: {r['source_file']}")
                print(f"    内容: {r['content'][:200]}...")
                print()
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    main()
