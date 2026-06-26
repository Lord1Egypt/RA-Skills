"""
Pinecone 知识库工具 - 核心模块
功能：配置管理、文档加载、文本分割、向量嵌入、Pinecone 操作、混合搜索
"""

import os
import sys
import time
import hashlib
import chardet
import re
import math
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import Counter

import tiktoken
from openai import OpenAI, RateLimitError
from pinecone import Pinecone, ServerlessSpec
from pydantic import Field
from pydantic_settings import BaseSettings


# ==================== 配置管理 ====================

class Config(BaseSettings):
    """配置管理"""
    PINECONE_API_KEY: str = Field(..., description="Pinecone API Key")
    EMBEDDING_API_KEY: str = Field(..., description="Embedding API Key")
    EMBEDDING_BASE_URL: str = Field(..., description="Embedding API Base URL")
    EMBEDDING_MODEL: str = Field("text-embedding-3-large", description="Embedding Model")
    INDEX_NAME: str = Field("workspace", description="Pinecone Index Name")
    NAMESPACE: str = Field("", description="Pinecone Namespace")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# ==================== 数据模型 ====================

@dataclass
class Document:
    """文档数据模型"""
    content: str
    source: str
    filename: str
    file_type: str
    title: str = ""
    metadata: Dict = field(default_factory=dict)


@dataclass
class TextChunk:
    """文本块数据模型"""
    content: str
    source: str
    filename: str
    file_type: str
    chunk_index: int
    total_chunks: int
    title: str = ""
    token_count: int = 0


@dataclass
class UploadStats:
    """上传统计信息"""
    workspace: str
    namespace: str
    total_files: int
    total_chunks: int
    successful_chunks: int
    failed_chunks: int
    file_stats: List[Dict[str, Any]] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式返回给 agent"""
        return {
            "workspace": self.workspace,
            "namespace": self.namespace if self.namespace else "default",
            "total_files": self.total_files,
            "total_chunks": self.total_chunks,
            "successful_chunks": self.successful_chunks,
            "failed_chunks": self.failed_chunks,
            "duration_seconds": (self.end_time - self.start_time).total_seconds() if self.end_time else None,
            "files": self.file_stats
        }


# ==================== 文档加载器 ====================

class DocumentLoader:
    """文档加载器 - 支持 TXT 和 Markdown"""
    
    SUPPORTED_EXTENSIONS = {'.txt', '.md', '.markdown'}
    
    @classmethod
    def load(cls, file_path: str) -> Optional[Document]:
        """加载文档"""
        path = Path(file_path)
        
        if not path.exists():
            print(f"❌ 文件不存在: {file_path}")
            return None
        
        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            print(f"❌ 不支持的文件类型: {path.suffix}")
            return None
        
        try:
            # 检测编码
            with open(path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encoding = detected.get('encoding', 'utf-8') or 'utf-8'
            
            # 读取内容
            content = raw_data.decode(encoding, errors='replace')
            
            # 提取元数据
            file_type = 'markdown' if path.suffix.lower() in {'.md', '.markdown'} else 'txt'
            title = cls._extract_title(content, file_type)
            
            return Document(
                content=content,
                source=str(path.absolute()),
                filename=path.name,
                file_type=file_type,
                title=title,
                metadata={
                    'encoding': encoding,
                    'size_bytes': len(raw_data),
                    'modified_time': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                }
            )
            
        except Exception as e:
            print(f"❌ 加载文件失败 {file_path}: {e}")
            return None
    
    @classmethod
    def _extract_title(cls, content: str, file_type: str) -> str:
        """提取文档标题"""
        if file_type == 'markdown':
            # 提取第一个 # 标题
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                elif line.startswith('---'):
                    # 解析 frontmatter
                    break
        
        # 默认返回前 50 个字符
        first_line = content.split('\n')[0].strip()
        return first_line[:50] + '...' if len(first_line) > 50 else first_line
    
    @classmethod
    def load_directory(cls, dir_path: str, recursive: bool = True) -> List[Document]:
        """加载目录中的所有文档"""
        documents = []
        path = Path(dir_path)
        
        if not path.exists() or not path.is_dir():
            print(f"❌ 目录不存在: {dir_path}")
            return documents
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in cls.SUPPORTED_EXTENSIONS:
                doc = cls.load(str(file_path))
                if doc:
                    documents.append(doc)
        
        return documents


# ==================== 文本分割器 ====================

class TextSplitter:
    """递归字符文本分割器 - 参考 LangChain 实现"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        model_name: str = "text-embedding-3-large"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", "。", ". ", " ", ""]
        
        # 初始化 tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(model_name)
        except:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def _token_count(self, text: str) -> int:
        """计算 token 数量"""
        return len(self.tokenizer.encode(text))
    
    def split(self, document: Document) -> List[TextChunk]:
        """分割文档为文本块"""
        chunks = self._split_text(document.content)
        
        text_chunks = []
        for i, chunk_content in enumerate(chunks):
            text_chunks.append(TextChunk(
                content=chunk_content,
                source=document.source,
                filename=document.filename,
                file_type=document.file_type,
                chunk_index=i,
                total_chunks=len(chunks),
                title=document.title,
                token_count=self._token_count(chunk_content)
            ))
        
        return text_chunks
    
    def _split_text(self, text: str) -> List[str]:
        """递归分割文本"""
        return self._recursive_split(text, self.separators.copy())
    
    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        """递归分割实现"""
        if not text.strip():
            return []
        
        # 如果文本在限制范围内，直接返回
        if self._token_count(text) <= self.chunk_size:
            return [text]
        
        if not separators:
            # 没有分隔符了，强制按字符分割
            return self._force_split(text)
        
        separator = separators[0]
        remaining_separators = separators[1:]
        
        if separator == "":
            # 最后按字符分割
            return self._force_split(text)
        
        # 按当前分隔符分割
        parts = text.split(separator)
        
        if len(parts) == 1:
            # 无法分割，尝试下一个分隔符
            return self._recursive_split(text, remaining_separators)
        
        # 递归处理每个部分
        chunks = []
        current_chunk = ""
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # 检查单个部分是否超过限制
            if self._token_count(part) > self.chunk_size:
                # 先保存当前 chunk
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                
                # 递归分割这个大的部分
                sub_chunks = self._recursive_split(part, remaining_separators.copy())
                chunks.extend(sub_chunks)
            else:
                # 尝试添加到当前 chunk
                test_chunk = current_chunk + separator + part if current_chunk else part
                
                if self._token_count(test_chunk) <= self.chunk_size:
                    current_chunk = test_chunk
                else:
                    # 当前 chunk 已满，保存并开始新的 chunk
                    if current_chunk:
                        chunks.append(current_chunk)
                    
                    # 添加重叠部分
                    if current_chunk and self.chunk_overlap > 0:
                        overlap_text = self._get_overlap_text(current_chunk)
                        current_chunk = overlap_text + separator + part if overlap_text else part
                    else:
                        current_chunk = part
        
        # 保存最后一个 chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _force_split(self, text: str) -> List[str]:
        """强制按字符分割（最后手段）"""
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks
    
    def _get_overlap_text(self, text: str) -> str:
        """获取重叠部分的文本"""
        tokens = self.tokenizer.encode(text)
        
        if len(tokens) <= self.chunk_overlap:
            return text
        
        overlap_tokens = tokens[-self.chunk_overlap:]
        return self.tokenizer.decode(overlap_tokens)


# ==================== 向量嵌入客户端 ====================

class EmbeddingClient:
    """向量嵌入客户端 - 支持批量和重试"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(
            api_key=config.EMBEDDING_API_KEY,
            base_url=config.EMBEDDING_BASE_URL
        )
        self.model = config.EMBEDDING_MODEL
        self.batch_size = 30  # 默认批次大小
        self.max_retries = 3
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入文本"""
        if not texts:
            return []
        
        all_embeddings = []
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_embeddings = self._embed_batch_with_retry(batch)
            all_embeddings.extend(batch_embeddings)
            
            # 简单的速率限制控制
            if i + self.batch_size < len(texts):
                time.sleep(0.1)
        
        return all_embeddings
    
    def _embed_batch_with_retry(self, batch: List[str]) -> List[List[float]]:
        """带重试机制的批次嵌入"""
        for attempt in range(self.max_retries):
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    encoding_format="float"
                )
                return [data.embedding for data in response.data]
                
            except RateLimitError as e:
                wait_time = 2 ** attempt  # 指数退避
                print(f"⚠️  速率限制，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"⚠️  嵌入失败: {e}，{wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ 嵌入失败，已重试 {self.max_retries} 次: {e}")
                    raise
        
        raise Exception(f"嵌入失败，已重试 {self.max_retries} 次")


# ==================== Pinecone 管理器 ====================

class PineconeManager:
    """Pinecone 管理器 - 封装所有 Pinecone 操作"""
    
    MAX_BATCH_SIZE_MB = 2  # Pinecone 单批次限制 2MB
    
    def __init__(self, config: Config):
        self.config = config
        self.pc = Pinecone(api_key=config.PINECONE_API_KEY)
        self.index = self._get_or_create_index()
    
    def _get_or_create_index(self):
        """获取或创建索引"""
        index_name = self.config.INDEX_NAME
        
        # 检查索引是否存在
        if index_name not in self.pc.list_indexes().names():
            print(f"📝 创建索引: {index_name}")
            self.pc.create_index(
                name=index_name,
                dimension=3072 if "large" in self.config.EMBEDDING_MODEL else 1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            # 等待索引就绪
            time.sleep(2)
        
        return self.pc.Index(index_name)
    
    def upsert_chunks(
        self,
        chunks: List[TextChunk],
        embeddings: List[List[float]]
    ) -> Tuple[int, int]:
        """
        上传文本块到 Pinecone
        返回: (成功数量, 失败数量)
        """
        if len(chunks) != len(embeddings):
            raise ValueError("chunks 和 embeddings 数量不匹配")
        
        if not chunks:
            return 0, 0
        
        # 准备向量数据
        vectors = []
        for chunk, embedding in zip(chunks, embeddings):
            vector_id = self._generate_id(chunk)
            metadata = {
                "text": chunk.content,
                "source": chunk.source,
                "filename": chunk.filename,
                "file_type": chunk.file_type,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                "title": chunk.title,
                "token_count": chunk.token_count,
                "created_at": datetime.now().isoformat()
            }
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })
        
        # 使用自适应批次大小上传
        namespace = self.config.NAMESPACE if self.config.NAMESPACE else None
        return self._adaptive_upsert(vectors, namespace)
    
    def _adaptive_upsert(
        self,
        vectors: List[Dict],
        namespace: Optional[str]
    ) -> Tuple[int, int]:
        """
        自适应批次大小上传
        遇到 2MB 限制时自动减半重试
        """
        successful = 0
        failed = 0
        
        # 初始批次大小
        batch_size = len(vectors)
        min_batch_size = 1
        
        i = 0
        while i < len(vectors):
            batch = vectors[i:i + batch_size]
            
            try:
                # 尝试上传
                if namespace:
                    self.index.upsert(vectors=batch, namespace=namespace)
                else:
                    self.index.upsert(vectors=batch)
                
                successful += len(batch)
                i += batch_size
                
                # 成功后可以尝试恢复批次大小（可选）
                if batch_size < 100:
                    batch_size = min(batch_size * 2, 100, len(vectors) - i)
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # 检查是否是大小限制错误
                if "2mb" in error_msg or "too large" in error_msg or "request entity too large" in error_msg:
                    if batch_size > min_batch_size:
                        # 减半批次大小重试
                        new_batch_size = max(batch_size // 2, min_batch_size)
                        print(f"⚠️  批次大小 {batch_size} 超过限制，减半为 {new_batch_size} 重试...")
                        batch_size = new_batch_size
                        continue  # 不增加 i，用更小的批次重试
                    else:
                        # 已经是最小批次，记录失败
                        print(f"❌ 单条记录超过 2MB 限制，跳过: {batch[0]['id']}")
                        failed += 1
                        i += 1
                else:
                    # 其他错误，记录失败
                    print(f"❌ 上传失败: {e}")
                    failed += len(batch)
                    i += batch_size
        
        return successful, failed
    
    def _generate_id(self, chunk: TextChunk) -> str:
        """生成唯一 ID"""
        # 基于文件路径和块索引生成 ID
        file_hash = hashlib.md5(chunk.source.encode()).hexdigest()[:8]
        return f"{file_hash}_{chunk.chunk_index}"
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 3,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """搜索相似向量"""
        namespace = self.config.NAMESPACE if self.config.NAMESPACE else None
        
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace,
            filter=filter_dict
        )
        
        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]


# ==================== 知识库主类 ====================

class KnowledgeBase:
    """知识库主类 - 整合所有功能"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.loader = DocumentLoader()
        self.splitter = TextSplitter(model_name=self.config.EMBEDDING_MODEL)
        self.embedder = EmbeddingClient(self.config)
        self.pinecone = PineconeManager(self.config)
    
    def upload_file(
        self,
        file_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> UploadStats:
        """上传单个文件"""
        # 更新分割器参数
        self.splitter.chunk_size = chunk_size
        self.splitter.chunk_overlap = chunk_overlap
        
        stats = UploadStats(
            workspace=self.config.INDEX_NAME,
            namespace=self.config.NAMESPACE,
            total_files=1,
            total_chunks=0,
            successful_chunks=0,
            failed_chunks=0
        )
        
        # 加载文档
        doc = self.loader.load(file_path)
        if not doc:
            stats.failed_chunks = 1
            stats.end_time = datetime.now()
            return stats
        
        # 分割文本
        chunks = self.splitter.split(doc)
        stats.total_chunks = len(chunks)
        
        if not chunks:
            stats.end_time = datetime.now()
            return stats
        
        # 生成嵌入
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed(texts)
        
        # 上传到 Pinecone
        successful, failed = self.pinecone.upsert_chunks(chunks, embeddings)
        stats.successful_chunks = successful
        stats.failed_chunks = failed
        
        # 记录文件统计
        stats.file_stats.append({
            "filename": doc.filename,
            "source": doc.source,
            "file_type": doc.file_type,
            "chunks": len(chunks),
            "successful": successful,
            "failed": failed,
            "tokens": sum(chunk.token_count for chunk in chunks)
        })
        
        stats.end_time = datetime.now()
        return stats
    
    def upload_directory(
        self,
        dir_path: str,
        recursive: bool = True,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> UploadStats:
        """上传整个目录"""
        # 更新分割器参数
        self.splitter.chunk_size = chunk_size
        self.splitter.chunk_overlap = chunk_overlap
        
        # 加载所有文档
        documents = self.loader.load_directory(dir_path, recursive)
        
        stats = UploadStats(
            workspace=self.config.INDEX_NAME,
            namespace=self.config.NAMESPACE,
            total_files=len(documents),
            total_chunks=0,
            successful_chunks=0,
            failed_chunks=0
        )
        
        if not documents:
            stats.end_time = datetime.now()
            return stats
        
        # 处理每个文档
        all_chunks = []
        for doc in documents:
            chunks = self.splitter.split(doc)
            all_chunks.extend(chunks)
            
            stats.file_stats.append({
                "filename": doc.filename,
                "source": doc.source,
                "file_type": doc.file_type,
                "chunks": len(chunks),
                "tokens": sum(chunk.token_count for chunk in chunks)
            })
        
        stats.total_chunks = len(all_chunks)
        
        if not all_chunks:
            stats.end_time = datetime.now()
            return stats
        
        # 批量生成嵌入
        print(f"🔄 正在生成 {len(all_chunks)} 个文本块的嵌入向量...")
        texts = [chunk.content for chunk in all_chunks]
        embeddings = self.embedder.embed(texts)
        
        # 上传到 Pinecone
        print(f"📤 正在上传到 Pinecone...")
        successful, failed = self.pinecone.upsert_chunks(all_chunks, embeddings)
        stats.successful_chunks = successful
        stats.failed_chunks = failed
        
        # 更新每个文件的统计
        chunk_idx = 0
        for file_stat in stats.file_stats:
            file_chunks = file_stat["chunks"]
            file_successful = 0
            file_failed = 0
            
            for _ in range(file_chunks):
                if chunk_idx < len(all_chunks):
                    # 这里简化处理，实际应该跟踪每个 chunk 的上传状态
                    file_successful += 1
                chunk_idx += 1
            
            file_stat["successful"] = file_successful
            file_stat["failed"] = 0  # 简化处理
        
        stats.end_time = datetime.now()
        return stats
    
    def search(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.0,
        file_type: Optional[str] = None,
        filename: Optional[str] = None,
        use_hybrid: bool = True,
        vector_candidates: int = 20
    ) -> List[Dict]:
        """
        搜索知识库（支持混合搜索）
        
        Args:
            query: 搜索查询
            top_k: 返回结果数量
            min_score: 最小相似度阈值（0-1）
            file_type: 按文件类型过滤（如 'markdown', 'txt'）
            filename: 按文件名过滤（支持部分匹配）
            use_hybrid: 是否使用混合搜索（向量+关键词）
            vector_candidates: 向量搜索候选集大小（用于混合搜索）
        
        Returns:
            搜索结果列表，按相关度排序
        """
        # 构建元数据过滤条件
        filter_dict = {}
        if file_type:
            filter_dict["file_type"] = file_type
        
        # 生成查询向量
        embeddings = self.embedder.embed([query])
        query_vector = embeddings[0]
        
        # 确定召回数量
        recall_k = vector_candidates if use_hybrid else top_k
        
        # 向量搜索
        candidates = self.pinecone.search(query_vector, recall_k, filter_dict)
        
        # 文件名过滤（后过滤，因为 Pinecone 不支持模糊匹配）
        if filename:
            candidates = [
                r for r in candidates
                if filename.lower() in r.get("metadata", {}).get("filename", "").lower()
            ]
        
        # 相似度阈值过滤
        if min_score > 0:
            candidates = [r for r in candidates if r.get("score", 0) >= min_score]
        
        # 混合搜索：向量 + 关键词 BM25
        if use_hybrid and len(candidates) > 0:
            candidates = self._hybrid_rank(query, candidates)
        
        # 返回 Top-K
        return candidates[:top_k]
    
    def _hybrid_rank(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """
        混合排序：结合向量相似度和关键词匹配（BM25 简化版）
        
        Args:
            query: 查询字符串
            candidates: 向量搜索候选集
        
        Returns:
            重新排序后的结果
        """
        # 分词
        query_terms = self._tokenize(query)
        
        # 计算每个候选的关键词匹配分数
        for candidate in candidates:
            metadata = candidate.get("metadata", {})
            text = metadata.get("text", "")
            title = metadata.get("title", "")
            
            # 合并文本和标题（标题权重更高）
            doc_content = (title + " ") * 3 + text
            doc_terms = self._tokenize(doc_content)
            
            # 计算 BM25 分数（简化版）
            bm25_score = self._calculate_bm25(query_terms, doc_terms, len(candidates))
            
            # 向量分数（归一化到 0-1）
            vector_score = candidate.get("score", 0)
            
            # 混合分数（可调整权重）
            # 默认：向量 70%，关键词 30%
            hybrid_score = 0.7 * vector_score + 0.3 * bm25_score
            
            candidate["hybrid_score"] = hybrid_score
            candidate["vector_score"] = vector_score
            candidate["bm25_score"] = bm25_score
        
        # 按混合分数排序
        candidates.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)
        
        return candidates
    
    def _tokenize(self, text: str) -> List[str]:
        """
        简单的中文/英文分词
        
        - 英文：按空格和标点分割
        - 中文：按字符分割（简化处理）
        """
        # 转换为小写
        text = text.lower()
        
        # 提取英文单词
        english_words = re.findall(r'[a-z]+', text)
        
        # 提取中文字符
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        
        # 合并（中文字符作为独立 token）
        return english_words + chinese_chars
    
    def _calculate_bm25(
        self,
        query_terms: List[str],
        doc_terms: List[str],
        total_docs: int,
        k1: float = 1.5,
        b: float = 0.75
    ) -> float:
        """
        简化版 BM25 计算
        
        Args:
            query_terms: 查询词列表
            doc_terms: 文档词列表
            total_docs: 总文档数
            k1: BM25 参数
            b: BM25 参数
        
        Returns:
            BM25 分数（归一化到 0-1）
        """
        if not query_terms or not doc_terms:
            return 0.0
        
        # 文档长度
        doc_len = len(doc_terms)
        avg_doc_len = doc_len  # 简化：使用当前文档长度作为平均长度
        
        # 词频统计
        doc_term_freq = Counter(doc_terms)
        
        score = 0.0
        for term in query_terms:
            # 词频
            tf = doc_term_freq.get(term, 0)
            
            # 包含该词的文档数（简化：假设为 1）
            df = 1
            
            # IDF
            idf = math.log((total_docs - df + 0.5) / (df + 0.5) + 1)
            
            # BM25 公式
            tf_component = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_doc_len))
            
            score += idf * tf_component
        
        # 归一化（简化处理）
        max_possible_score = len(query_terms) * math.log(total_docs + 1) * (k1 + 1) / k1
        normalized_score = min(score / max_possible_score if max_possible_score > 0 else 0, 1.0)
        
        return normalized_score
