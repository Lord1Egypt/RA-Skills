#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenViking Korean - 벡터 검색 모듈

sentence-transformers 기반 의미 검색
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import hashlib
import pickle

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False


@dataclass
class VectorDocument:
    """벡터 문서"""
    uri: str
    content: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class VectorStore:
    """벡터 저장소 - 의미 기반 검색"""
    
    def __init__(self, 
                 cache_dir: str = "~/.openviking/vectors",
                 model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Args:
            cache_dir: 벡터 캐시 디렉토리
            model_name: 한국어 지원 모델
        """
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.model_name = model_name
        self.model = None
        self.documents: List[VectorDocument] = []
        self.embeddings_cache: Dict[str, np.ndarray] = {}
        
        # 캐시 로드
        self._load_cache()
    
    def _load_cache(self):
        """캐시 로드"""
        cache_file = self.cache_dir / "embeddings.pkl"
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
                self.documents = data.get('documents', [])
                self.embeddings_cache = data.get('embeddings', {})
    
    def _save_cache(self):
        """캐시 저장"""
        cache_file = self.cache_dir / "embeddings.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'embeddings': self.embeddings_cache
            }, f)
    
    def _get_model(self):
        """모델 로드 (지연 로딩)"""
        if self.model is None and EMBEDDING_AVAILABLE:
            self.model = SentenceTransformer(self.model_name)
        return self.model
    
    def _get_content_hash(self, content: str) -> str:
        """내용 해시 생성"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def add_document(self, uri: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """문서 추가"""
        # 이미 존재하는지 확인
        for doc in self.documents:
            if doc.uri == uri:
                # 내용이 같으면 스킵
                if doc.content == content:
                    return False
                # 내용이 다르면 업데이트
                doc.content = content
                doc.metadata = metadata or {}
                # 임베딩 갱신
                if uri in self.embeddings_cache:
                    del self.embeddings_cache[uri]
                self._save_cache()
                return True
        
        # 새 문서 추가
        doc = VectorDocument(
            uri=uri,
            content=content,
            metadata=metadata or {}
        )
        self.documents.append(doc)
        self._save_cache()
        return True
    
    def remove_document(self, uri: str) -> bool:
        """문서 삭제"""
        for i, doc in enumerate(self.documents):
            if doc.uri == uri:
                self.documents.pop(i)
                if uri in self.embeddings_cache:
                    del self.embeddings_cache[uri]
                self._save_cache()
                return True
        return False
    
    def get_embedding(self, content: str) -> Optional[np.ndarray]:
        """임베딩 생성/조회"""
        model = self._get_model()
        if model is None:
            return None
        
        content_hash = self._get_content_hash(content)
        
        # 캐시 확인
        if content_hash in self.embeddings_cache:
            return self.embeddings_cache[content_hash]
        
        # 새 임베딩 생성
        embedding = model.encode(content, convert_to_numpy=True)
        self.embeddings_cache[content_hash] = embedding
        
        return embedding
    
    def search(self, 
               query: str, 
               top_k: int = 5,
               min_score: float = 0.3) -> List[Dict[str, Any]]:
        """의미 기반 검색"""
        if not EMBEDDING_AVAILABLE or not self.documents:
            return []
        
        # 쿼리 임베딩
        model = self._get_model()
        if model is None:
            return []
        
        query_embedding = model.encode(query, convert_to_numpy=True)
        
        # 모든 문서와 유사도 계산
        scores: List[Tuple[float, VectorDocument]] = []
        
        for doc in self.documents:
            doc_embedding = self.get_embedding(doc.content)
            if doc_embedding is None:
                continue
            
            # 코사인 유사도
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            
            if similarity >= min_score:
                scores.append((similarity, doc))
        
        # 점수순 정렬
        scores.sort(key=lambda x: x[0], reverse=True)
        
        # 상위 k개 반환
        results = []
        for score, doc in scores[:top_k]:
            results.append({
                "uri": doc.uri,
                "content": doc.content[:500],  # 미리보기
                "score": float(score),
                "metadata": doc.metadata
            })
        
        return results
    
    def batch_index(self, documents: List[Tuple[str, str, Dict]]):
        """일괄 인덱싱"""
        for uri, content, metadata in documents:
            self.add_document(uri, content, metadata)
        
        # 모든 임베딩 미리 생성
        if EMBEDDING_AVAILABLE:
            model = self._get_model()
            contents = [doc.content for doc in self.documents]
            embeddings = model.encode(contents, convert_to_numpy=True)
            
            for doc, emb in zip(self.documents, embeddings):
                content_hash = self._get_content_hash(doc.content)
                self.embeddings_cache[content_hash] = emb
            
            self._save_cache()
    
    def clear(self):
        """모든 데이터 삭제"""
        self.documents = []
        self.embeddings_cache = {}
        self._save_cache()
    
    def stats(self) -> Dict[str, Any]:
        """통계 정보"""
        return {
            "document_count": len(self.documents),
            "cache_size": len(self.embeddings_cache),
            "model": self.model_name if EMBEDDING_AVAILABLE else None
        }


def create_vector_store(workspace_path: str = "~/.openclaw/workspace") -> VectorStore:
    """워크스페이스에서 벡터 저장소 생성"""
    store = VectorStore()
    
    # 워크스페이스의 주요 파일들 인덱싱
    workspace = Path(workspace_path).expanduser()
    
    documents = []
    
    # MEMORY.md
    memory_file = workspace / "MEMORY.md"
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            documents.append(("MEMORY.md", f.read(), {"type": "long_term_memory"}))
    
    # context-summary.md (L0)
    summary_file = workspace / "context-summary.md"
    if summary_file.exists():
        with open(summary_file, 'r', encoding='utf-8') as f:
            documents.append(("context-summary.md", f.read(), {"type": "l0_summary"}))
    
    # memory/*.md
    memory_dir = workspace / "memory"
    if memory_dir.exists():
        for md_file in memory_dir.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    documents.append((str(md_file.name), f.read(), {"type": "daily_log"}))
            except UnicodeDecodeError:
                # UTF-8이 아니면 스킵
                pass
    
    # 일괄 인덱싱
    store.batch_index(documents)
    
    return store


if __name__ == "__main__":
    # 테스트
    store = create_vector_store()
    print("통계:", store.stats())
    
    # 검색 테스트
    results = store.search("마케팅", top_k=3)
    for r in results:
        print(f"[{r['score']:.2f}] {r['uri']}")
        print(f"  {r['content'][:100]}...")