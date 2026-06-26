"""
Embedding Handler - Optional embedding model processing
"""
import sys
import hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from typing import List, Optional, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingCache:
    """Simple LRU cache for embedding results"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, np.ndarray] = {}
        self.access_order: List[str] = []
    
    def get(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding"""
        key = self._hash(text)
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, text: str, embedding: np.ndarray):
        """Cache embedding"""
        key = self._hash(text)
        
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        
        self.cache[key] = embedding
        self.access_order.append(key)
    
    @staticmethod
    def _hash(text: str) -> str:
        """Hash text for cache key"""
        return hashlib.md5(text.encode()).hexdigest()


class EmbeddingHandler:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        dim: int = 384,
        cache_size: int = 1000
    ):
        self.model_name = model_name
        self.dim = dim
        self.model = None
        self._loaded = False
        self.cache = EmbeddingCache(max_size=cache_size)
    
    def _load_model(self):
        """Lazy load the embedding model"""
        if self._loaded:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            self._loaded = True
            print(f"Embedding model loaded: {self.model_name}")
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        self._load_model()
        return self.model.encode(texts, convert_to_numpy=True)
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text with caching"""
        # Check cache first
        cached = self.cache.get(text)
        if cached is not None:
            return cached
        
        # Encode and cache
        embedding = self.encode([text])[0]
        self.cache.put(text, embedding)
        return embedding
    
    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        v1 = v1.reshape(1, -1)
        v2 = v2.reshape(1, -1)
        return float(cosine_similarity(v1, v2)[0][0])
    
    def search_similar(
        self,
        query: str,
        entries: List[Dict[str, Any]],
        top_k: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar entries using embeddings
        
        Args:
            query: Search query
            entries: List of entries with 'content' and 'embedding' keys
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            List of matching entries with similarity scores
        """
        if not entries:
            return []
        
        # Check which entries have embeddings
        entries_with_embedding = [e for e in entries if e.get('embedding') is not None]
        if not entries_with_embedding:
            # Fallback to text search
            query_lower = query.lower()
            return [
                {**e, 'similarity': 1.0 if query_lower in e.get('content', '').lower() else 0.0}
                for e in entries
            ][:top_k]
        
        # Encode query (with caching)
        query_embedding = self.encode_single(query)
        
        # Calculate similarities
        results = []
        for entry in entries_with_embedding:
            if entry.get('embedding') is not None:
                embedding = np.array(entry['embedding'])
                similarity = self.cosine_similarity(query_embedding, embedding)
                if similarity >= threshold:
                    results.append({**entry, 'similarity': similarity})
        
        # Sort by similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]


# Global embedding handler instance (per model name)
_embedding_handlers: Dict[str, EmbeddingHandler] = {}


def get_embedding_handler(
    use_embedding: bool = False,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    dim: int = 384
) -> Optional[EmbeddingHandler]:
    """Get or create the global embedding handler for the given model"""
    if not use_embedding:
        return None
    
    if model_name not in _embedding_handlers:
        _embedding_handlers[model_name] = EmbeddingHandler(model_name, dim)
    
    return _embedding_handlers[model_name]


def reset_embedding_handler():
    """Reset the global embedding handler (useful for testing)"""
    global _embedding_handlers
    _embedding_handlers = {}
