"""
Meta Knowledge Base - Self-building knowledge management system
"""
import json
import os
import re
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
from pathlib import Path
import threading


@dataclass
class KnowledgeItem:
    """Single piece of knowledge"""
    id: str
    content: str
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0


@dataclass
class SearchResult:
    """Search result with score"""
    item: KnowledgeItem
    score: float
    highlights: List[str] = field(default_factory=list)


@dataclass
class Entity:
    """Knowledge graph entity"""
    name: str
    entity_type: str
    properties: Dict = field(default_factory=dict)
    connections: List[str] = field(default_factory=list)


class SimpleVectorStore:
    """Simple in-memory vector store with cosine similarity"""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectors: Dict[str, List[float]] = {}
        self.items: Dict[str, KnowledgeItem] = {}
        self._lock = threading.Lock()
    
    def add(self, item: KnowledgeItem):
        """Add item to store"""
        with self._lock:
            self.items[item.id] = item
            if item.embedding:
                self.vectors[item.id] = item.embedding
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        """Search by cosine similarity"""
        with self._lock:
            if not self.vectors:
                return []
            
            # Normalize query
            norm = sum(x**2 for x in query_embedding) ** 0.5
            if norm == 0:
                return []
            query_norm = [x / norm for x in query_embedding]
            
            # Calculate similarities
            results = []
            for item_id, vec in self.vectors.items():
                if len(vec) != len(query_norm):
                    continue
                v_norm = sum(x**2 for x in vec) ** 0.5
                if v_norm == 0:
                    continue
                vec_norm = [x / v_norm for x in vec]
                
                similarity = sum(a * b for a, b in zip(query_norm, vec_norm))
                results.append((item_id, similarity))
            
            # Sort by similarity
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]
    
    def delete(self, item_id: str):
        """Delete item"""
        with self._lock:
            self.items.pop(item_id, None)
            self.vectors.pop(item_id, None)
    
    def count(self) -> int:
        """Count items"""
        return len(self.items)


class KnowledgeBase:
    """
    Self-building knowledge base with semantic search
    
    Features:
    - Auto-capture from multiple sources
    - Semantic search with embeddings
    - Knowledge graph for relationships
    - RAG-based Q&A
    """
    
    def __init__(
        self,
        name: str = "default",
        embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
        storage_path: str = None,
        dimension: int = 384
    ):
        self.name = name
        self.embedding_model = embedding_model
        self.dimension = dimension
        
        # Storage
        storage_path = storage_path or f"~/.meta_knowledge/{name}"
        self.storage_path = os.path.expanduser(storage_path)
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Components
        self.vector_store = SimpleVectorStore(dimension=dimension)
        self.graph: Dict[str, Entity] = {}
        
        # Indexes
        self.tags_index: Dict[str, set] = defaultdict(set)
        self.content_index: Dict[str, List[str]] = defaultdict(list)
        
        # Load existing data
        self._load()
    
    def _load(self):
        """Load knowledge base from disk"""
        index_file = os.path.join(self.storage_path, "index.json")
        items_file = os.path.join(self.storage_path, "items")
        
        # Load index
        if os.path.exists(index_file):
            with open(index_file, 'r') as f:
                data = json.load(f)
                self.tags_index = defaultdict(set, data.get('tags', {}))
        
        # Load items
        if os.path.exists(items_file):
            for filename in os.listdir(items_file):
                if filename.endswith('.json'):
                    with open(os.path.join(items_file, filename), 'r') as f:
                        item_data = json.load(f)
                        item = KnowledgeItem(**item_data)
                        self.vector_store.add(item)
    
    def _save(self):
        """Save knowledge base to disk"""
        index_file = os.path.join(self.storage_path, "index.json")
        items_file = os.path.join(self.storage_path, "items")
        os.makedirs(items_file, exist_ok=True)
        
        # Save index
        with open(index_file, 'w') as f:
            json.dump({
                'tags': {k: list(v) for k, v in self.tags_index.items()},
                'name': self.name,
                'created': datetime.now().isoformat()
            }, f, indent=2)
        
        # Save all items
        for item_id, item in self.vector_store.items.items():
            item_file = os.path.join(items_file, f"{item_id}.json")
            with open(item_file, 'w') as f:
                json.dump(asdict(item), f, indent=2)
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID for content"""
        hash_input = f"{content[:100]}{time.time()}".encode()
        return hashlib.md5(hash_input).hexdigest()[:12]
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text (simplified)"""
        # Simple hash-based embedding for demo
        # In production, use actual embedding model
        hash_val = hash(text.encode()) % (2**32)
        import random
        random.seed(hash_val)
        return [random.uniform(-1, 1) for _ in range(self.dimension)]
    
    # ==================== Adding Knowledge ====================
    
    def add(
        self,
        content: str,
        tags: List[str] = None,
        metadata: Dict = None,
        generate_embedding: bool = True
    ) -> str:
        """
        Add a piece of knowledge
        
        Args:
            content: Text content
            tags: List of tags
            metadata: Additional metadata
            generate_embedding: Whether to generate embedding
            
        Returns:
            ID of added item
        """
        tags = tags or []
        metadata = metadata or {}
        
        # Generate ID
        item_id = self._generate_id(content)
        
        # Generate embedding
        embedding = None
        if generate_embedding:
            embedding = self._get_embedding(content)
        
        # Create item
        item = KnowledgeItem(
            id=item_id,
            content=content,
            tags=tags,
            metadata=metadata,
            embedding=embedding
        )
        
        # Add to vector store
        self.vector_store.add(item)
        
        # Update indexes
        for tag in tags:
            self.tags_index[tag].add(item_id)
        
        # Extract and index entities
        self._extract_entities(content, item_id)
        
        # Save
        self._save()
        
        return item_id
    
    def add_batch(self, items: List[Dict]) -> List[str]:
        """Add multiple items"""
        ids = []
        for item in items:
            item_id = self.add(
                content=item['content'],
                tags=item.get('tags', []),
                metadata=item.get('metadata', {})
            )
            ids.append(item_id)
        return ids
    
    def add_from_file(self, filepath: str, tags: List[str] = None, **kwargs) -> str:
        """Add content from file"""
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Read content based on extension
        if path.suffix == '.txt':
            content = path.read_text(encoding='utf-8')
        elif path.suffix == '.md':
            content = path.read_text(encoding='utf-8')
        elif path.suffix == '.json':
            content = json.dumps(json.loads(path.read_text()), indent=2)
        else:
            # For other files, just read as text (may need proper parser)
            try:
                content = path.read_text(encoding='utf-8')
            except:
                content = f"[Binary file: {filepath}]"
        
        # Add tags from filename
        file_tags = tags or []
        file_tags.append(f"file:{path.name}")
        
        return self.add(content=content, tags=file_tags, metadata={'source': 'file', 'path': str(filepath)})
    
    def add_from_url(self, url: str, tags: List[str] = None, **kwargs) -> str:
        """Add content from URL (simplified)"""
        # In production, would fetch and parse the URL
        content = f"[Content from {url}]"
        
        url_tags = tags or []
        url_tags.append('web')
        
        return self.add(
            content=content,
            tags=url_tags,
            metadata={'source': 'url', 'url': url}
        )
    
    def _extract_entities(self, content: str, item_id: str):
        """Extract entities from content for knowledge graph"""
        # Simple entity extraction
        # Look for capitalized words and numbers
        
        # Extract potential entities (simplified)
        words = content.split()
        for word in words:
            # Skip short words
            if len(word) < 3:
                continue
            
            # Add to graph if new
            if word not in self.graph:
                self.graph[word] = Entity(
                    name=word,
                    entity_type="concept",
                    properties={'mentions': 1}
                )
            else:
                self.graph[word].properties['mentions'] = \
                    self.graph[word].properties.get('mentions', 1) + 1
    
    # ==================== Searching ====================
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        tags: List[str] = None,
        min_score: float = 0.0
    ) -> List[SearchResult]:
        """
        Semantic search
        
        Args:
            query: Search query
            top_k: Number of results
            tags: Filter by tags
            min_score: Minimum similarity score
            
        Returns:
            List of SearchResult
        """
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, top_k * 2)
        
        search_results = []
        for item_id, score in results:
            if score < min_score:
                continue
            
            item = self.vector_store.items.get(item_id)
            if not item:
                continue
            
            # Filter by tags if specified
            if tags and not any(tag in item.tags for tag in tags):
                continue
            
            # Generate highlights
            highlights = self._generate_highlights(item.content, query)
            
            search_results.append(SearchResult(
                item=item,
                score=score,
                highlights=highlights
            ))
            
            if len(search_results) >= top_k:
                break
        
        return search_results
    
    def _generate_highlights(self, content: str, query: str) -> List[str]:
        """Generate highlights for content"""
        highlights = []
        query_words = query.lower().split()
        
        # Find sentences containing query words
        sentences = content.split('. ')
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in query_words):
                highlights.append(sentence.strip()[:200])
        
        return highlights[:3]
    
    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        keyword_weight: float = 0.3,
        semantic_weight: float = 0.7
    ) -> List[SearchResult]:
        """Hybrid search (keyword + semantic)"""
        # Get semantic results
        semantic_results = {r.item.id: r.score for r in self.search(query, top_k * 2)}
        
        # Keyword search
        query_words = query.lower().split()
        keyword_scores = {}
        
        for item_id, item in self.vector_store.items.items():
            content_lower = item.content.lower()
            score = sum(1 for word in query_words if word in content_lower)
            if score > 0:
                keyword_scores[item_id] = score / len(query_words)
        
        # Combine scores
        combined = {}
        all_ids = set(semantic_results.keys()) | set(keyword_scores.keys())
        
        for item_id in all_ids:
            sem_score = semantic_results.get(item_id, 0)
            key_score = keyword_scores.get(item_id, 0)
            
            combined[item_id] = sem_score * semantic_weight + key_score * keyword_weight
        
        # Sort and return top k
        sorted_ids = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for item_id, score in sorted_ids[:top_k]:
            item = self.vector_store.items.get(item_id)
            if item:
                results.append(SearchResult(item=item, score=score))
        
        return results
    
    def find_similar(self, content: str, top_k: int = 5) -> List[SearchResult]:
        """Find similar content"""
        return self.search(content, top_k=top_k)
    
    # ==================== Q&A ====================
    
    def ask(
        self,
        question: str,
        include_sources: bool = True,
        max_context: int = 3
    ) -> Dict:
        """
        Ask a question (RAG-style)
        
        Args:
            question: Question to ask
            include_sources: Include source references
            max_context: Number of context items
            
        Returns:
            Dict with answer and sources
        """
        # Retrieve relevant context
        context_results = self.search(question, top_k=max_context)
        
        # Build context
        context = "\n\n".join([
            f"[{r.score:.2f}] {r.item.content[:500]}"
            for r in context_results
        ])
        
        # Generate answer (simplified - in production would use LLM)
        answer = self._generate_answer(question, context)
        
        result = {
            'question': question,
            'answer': answer,
            'confidence': sum(r.score for r in context_results) / len(context_results) if context_results else 0
        }
        
        if include_sources:
            result['sources'] = [
                {
                    'id': r.item.id,
                    'content': r.item.content[:200],
                    'score': r.score,
                    'tags': r.item.tags
                }
                for r in context_results
            ]
        
        return result
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer from context (simplified)"""
        # In production, this would use an LLM
        # For now, return a simple response
        
        if not context:
            return "I don't have enough information to answer that question yet. Please add more knowledge to the base."
        
        # Extract relevant sentence
        question_words = set(question.lower().split())
        context_lines = context.split('\n\n')
        
        best_line = ""
        best_match = 0
        
        for line in context_lines:
            line_words = set(line.lower().split())
            matches = len(question_words & line_words)
            if matches > best_match:
                best_match = matches
                best_line = line
        
        if best_line:
            # Clean up the line
            answer = best_line
            if ']' in answer:
                answer = answer.split('] ', 1)[1] if len(answer.split('] ', 1)) > 1 else answer
            
            return answer + " [Based on knowledge base]"
        
        return "Based on my knowledge base: " + context_lines[0][:200] if context_lines else "I found some relevant information."
    
    def get_context(self, question: str, top_k: int = 3) -> List[str]:
        """Get relevant context for a question"""
        results = self.search(question, top_k=top_k)
        return [r.item.content for r in results]
    
    # ==================== Knowledge Graph ====================
    
    def get_knowledge_graph(self) -> Dict:
        """Get knowledge graph"""
        return {
            'entities': [
                {
                    'name': e.name,
                    'type': e.entity_type,
                    'properties': e.properties,
                    'connections': e.connections
                }
                for e in list(self.graph.values())[:50]  # Limit to 50
            ]
        }
    
    def find_related(self, entity: str, depth: int = 2) -> List[str]:
        """Find related entities"""
        if entity not in self.graph:
            return []
        
        related = set()
        current = {entity}
        
        for _ in range(depth):
            next_current = set()
            for e in current:
                if e in self.graph:
                    connections = self.graph[e].connections
                    related.update(connections)
                    next_current.update(connections)
            current = next_current
        
        return list(related)
    
    # ==================== Management ====================
    
    def list_tags(self) -> List[str]:
        """List all tags"""
        return list(self.tags_index.keys())
    
    def get_by_tag(self, tag: str) -> List[KnowledgeItem]:
        """Get items by tag"""
        item_ids = self.tags_index.get(tag, set())
        return [self.vector_store.items[i] for i in item_ids if i in self.vector_store.items]
    
    def export(self, format: str = 'json') -> str:
        """Export knowledge base"""
        data = {
            'name': self.name,
            'exported_at': datetime.now().isoformat(),
            'items': [
                asdict(item)
                for item in self.vector_store.items.values()
            ]
        }
        
        if format == 'json':
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            return str(data)
    
    def delete(self, item_id: str) -> bool:
        """Delete item"""
        item = self.vector_store.items.get(item_id)
        if not item:
            return False
        
        # Remove from tags index
        for tag in item.tags:
            if item_id in self.tags_index.get(tag, set()):
                self.tags_index[tag].discard(item_id)
        
        # Remove from vector store
        self.vector_store.delete(item_id)
        
        # Save
        self._save()
        
        return True
    
    def stats(self) -> Dict:
        """Get statistics"""
        return {
            'total_items': self.vector_store.count(),
            'total_tags': len(self.tags_index),
            'total_entities': len(self.graph),
            'tags': dict(self.tags_index)
        }


# Convenience function
def create_knowledge_base(name: str = "default", **kwargs) -> KnowledgeBase:
    """Create a knowledge base instance"""
    return KnowledgeBase(name=name, **kwargs)
