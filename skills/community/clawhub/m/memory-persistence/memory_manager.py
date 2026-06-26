"""
Memory Manager - Core memory management system
"""
import hashlib
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from memory_system.config import Config
from memory_system.storage import StorageBackend, MemoryEntry, create_storage
from memory_system.embedding import EmbeddingHandler, get_embedding_handler


class MemoryManager:
    def __init__(
        self,
        config_path: Optional[str] = None,
        backend: Optional[str] = None,
        use_embedding: Optional[bool] = None,
        base_path: Optional[str] = None,
        embedding_model: Optional[str] = None,
        **backend_kwargs
    ):
        """
        Initialize Memory Manager
        
        Args:
            config_path: Path to config.yaml
            backend: Storage backend type (local/github/gitee)
            use_embedding: Whether to use embedding model
            base_path: Override local storage base path
            embedding_model: Override embedding model name
            **backend_kwargs: Additional arguments for storage backend
        """
        self.config = Config(config_path) if config_path else Config()
        
        # Override config if provided
        if backend:
            self.config.update('STORAGE_BACKEND', backend)
        if use_embedding is not None:
            self.config.update('USE_EMBEDDING', use_embedding)
        if embedding_model:
            self.config.update('EMBEDDING_MODEL', embedding_model)
        
        # Initialize storage
        storage_type = self.config.get('STORAGE_BACKEND', 'local')
        storage_config = self.config.get_storage_config(storage_type)
        storage_config.update(backend_kwargs)
        
        # Override local storage path if provided
        if base_path:
            storage_config['base_path'] = base_path
        
        self.storage: StorageBackend = create_storage(storage_type, **storage_config)
        self.storage.init()
        
        # Initialize embedding handler
        if self.config.get('USE_EMBEDDING', False):
            self.embedding: Optional[EmbeddingHandler] = get_embedding_handler(
                use_embedding=True,
                model_name=self.config.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2'),
                dim=self.config.get('EMBEDDING_DIM', 384)
            )
        else:
            self.embedding = None
    
    def add(
        self,
        content: str,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        generate_embedding: bool = None,
        group: str = None
    ) -> MemoryEntry:
        """
        Add a new memory entry
        
        Args:
            content: Memory content
            tags: Optional tags for categorization
            metadata: Optional metadata dict
            generate_embedding: Force embedding generation (overrides config)
            group: Optional group name
        
        Returns:
            Created MemoryEntry
        """
        entry_id = self._generate_id(content)
        timestamp = datetime.now().isoformat()
        
        embedding = None
        # Auto-generate embedding if:
        # 1. explicitly requested (generate_embedding=True)
        # 2. not explicitly disabled AND manager has embedding enabled
        if generate_embedding or ((generate_embedding is None or generate_embedding is False) and self.embedding):
            if self.embedding is None:
                self.embedding = get_embedding_handler(use_embedding=True)
            embedding = self.embedding.encode_single(content).tolist()
        
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            timestamp=timestamp,
            tags=tags or [],
            embedding=embedding,
            metadata=metadata or {},
            group=group
        )
        
        self.storage.save(entry)
        return entry
    
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID"""
        return self.storage.load(entry_id)
    
    def delete(self, entry_id: str) -> bool:
        """Delete a memory entry"""
        return self.storage.delete(entry_id)
    
    def list(
        self,
        tags: List[str] = None,
        limit: int = None,
        offset: int = 0
    ) -> List[MemoryEntry]:
        """
        List memory entries with pagination
        
        Args:
            tags: Optional filter by tags
            limit: Maximum number of entries to return (None = all)
            offset: Number of entries to skip
        
        Returns:
            List of MemoryEntry objects
        """
        if tags:
            entries = self.storage.search_by_tags(tags)
        else:
            entries = self.storage.list_all()
        
        # Apply pagination
        if offset > 0:
            entries = entries[offset:]
        if limit is not None:
            entries = entries[:limit]
        
        return entries
    
    def count(self, tags: List[str] = None) -> int:
        """
        Count memory entries
        
        Args:
            tags: Optional filter by tags
        
        Returns:
            Number of matching entries
        """
        if tags:
            return len(self.storage.search_by_tags(tags))
        return len(self.storage.list_all())
    
    def batch_delete(self, entry_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple memory entries
        
        Args:
            entry_ids: List of entry IDs to delete
        
        Returns:
            Dict with results
        """
        deleted = []
        failed = []
        
        for entry_id in entry_ids:
            if self.storage.delete(entry_id):
                deleted.append(entry_id)
            else:
                failed.append(entry_id)
        
        return {
            "total": len(entry_ids),
            "deleted": len(deleted),
            "failed": len(failed),
            "deleted_ids": deleted,
            "failed_ids": failed
        }
    
    def batch_add_tags(self, entry_ids: List[str], tags: List[str]) -> Dict[str, Any]:
        """
        Add tags to multiple memories
        
        Args:
            entry_ids: List of entry IDs
            tags: Tags to add
        
        Returns:
            Dict with results
        """
        updated = []
        failed = []
        
        for entry_id in entry_ids:
            entry = self.storage.load(entry_id)
            if entry:
                # Add new tags (avoid duplicates)
                existing = set(entry.tags) if entry.tags else set()
                new_tags = set(tags)
                entry.tags = list(existing.union(new_tags))
                self.storage.save(entry)
                updated.append(entry_id)
            else:
                failed.append(entry_id)
        
        return {
            "total": len(entry_ids),
            "updated": len(updated),
            "failed": len(failed),
            "updated_ids": updated,
            "failed_ids": failed
        }
    
    def batch_remove_tags(self, entry_ids: List[str], tags: List[str]) -> Dict[str, Any]:
        """
        Remove tags from multiple memories
        
        Args:
            entry_ids: List of entry IDs
            tags: Tags to remove
        
        Returns:
            Dict with results
        """
        updated = []
        failed = []
        
        for entry_id in entry_ids:
            entry = self.storage.load(entry_id)
            if entry:
                # Remove specified tags
                tags_to_remove = set(tags)
                entry.tags = [t for t in (entry.tags or []) if t not in tags_to_remove]
                self.storage.save(entry)
                updated.append(entry_id)
            else:
                failed.append(entry_id)
        
        return {
            "total": len(entry_ids),
            "updated": len(updated),
            "failed": len(failed),
            "updated_ids": updated,
            "failed_ids": failed
        }
    
    def batch_update(
        self,
        updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch update multiple memories
        
        Args:
            updates: List of dicts with 'id' and fields to update (content, tags, metadata)
        
        Returns:
            Dict with results
        """
        updated = []
        failed = []
        
        for upd in updates:
            entry_id = upd.get('id')
            if not entry_id:
                failed.append({"error": "Missing ID", "data": upd})
                continue
            
            entry = self.storage.load(entry_id)
            if not entry:
                failed.append({"error": "Not found", "id": entry_id})
                continue
            
            # Update fields
            if 'content' in upd:
                entry.content = upd['content']
            if 'tags' in upd:
                entry.tags = upd['tags']
            if 'metadata' in upd:
                entry.metadata = upd['metadata']
            
            self.storage.save(entry)
            updated.append(entry_id)
        
        return {
            "total": len(updates),
            "updated": len(updated),
            "failed": len(failed),
            "updated_ids": updated,
            "failed": failed
        }
    
    # ============= Group Methods =============
    
    def list_groups(self) -> List[str]:
        """
        List all unique groups
        
        Returns:
            List of group names
        """
        all_entries = self.storage.list_all()
        groups = set()
        for entry in all_entries:
            if entry.group:
                groups.add(entry.group)
        return sorted(list(groups))
    
    def get_by_group(self, group: str) -> List[MemoryEntry]:
        """
        Get all memories in a group
        
        Args:
            group: Group name
        
        Returns:
            List of memories in the group
        """
        all_entries = self.storage.list_all()
        return [e for e in all_entries if e.group == group]
    
    def add_to_group(self, entry_ids: List[str], group: str) -> Dict[str, Any]:
        """
        Add memories to a group
        
        Args:
            entry_ids: List of entry IDs
            group: Group name
        
        Returns:
            Dict with results
        """
        updated = []
        failed = []
        
        for entry_id in entry_ids:
            entry = self.storage.load(entry_id)
            if entry:
                entry.group = group
                self.storage.save(entry)
                updated.append(entry_id)
            else:
                failed.append(entry_id)
        
        return {
            "total": len(entry_ids),
            "updated": len(updated),
            "failed": len(failed),
            "updated_ids": updated,
            "failed_ids": failed,
            "group": group
        }
    
    def remove_from_group(self, entry_ids: List[str]) -> Dict[str, Any]:
        """
        Remove memories from their groups
        
        Args:
            entry_ids: List of entry IDs
        
        Returns:
            Dict with results
        """
        updated = []
        failed = []
        
        for entry_id in entry_ids:
            entry = self.storage.load(entry_id)
            if entry:
                entry.group = None
                self.storage.save(entry)
                updated.append(entry_id)
            else:
                failed.append(entry_id)
        
        return {
            "total": len(entry_ids),
            "updated": len(updated),
            "failed": len(failed),
            "updated_ids": updated,
            "failed_ids": failed
        }
    
    def delete_group(self, group: str, delete_memories: bool = False) -> Dict[str, Any]:
        """
        Delete a group or remove all memories from it
        
        Args:
            group: Group name
            delete_memories: If True, delete all memories in the group
        
        Returns:
            Dict with results
        """
        entries = self.get_by_group(group)
        
        if delete_memories:
            deleted = []
            for entry in entries:
                if self.storage.delete(entry.id):
                    deleted.append(entry.id)
            return {
                "group": group,
                "deleted_memories": len(deleted),
                "deleted_ids": deleted
            }
        else:
            removed = self.remove_from_group([e.id for e in entries])
            return removed
    
    def search(
        self,
        query: str,
        tags: List[str] = None,
        top_k: int = None,
        threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Search memory entries
        
        Args:
            query: Search query
            tags: Optional filter by tags
            top_k: Number of results (default from config)
            threshold: Similarity threshold (default from config)
        
        Returns:
            List of matching entries with similarity scores
        """
        if top_k is None:
            top_k = self.config.get('DEFAULT_TOP_K', 5)
        if threshold is None:
            threshold = self.config.get('SIMILARITY_THRESHOLD', 0.7)
        
        # Get base entries
        if tags:
            entries = self.storage.search_by_tags(tags)
        else:
            entries = self.storage.list_all()
        
        if not entries:
            return []
        
        # Convert to dicts for embedding search
        entry_dicts = [e.to_dict() for e in entries]
        
        if self.embedding:
            return self.embedding.search_similar(
                query=query,
                entries=entry_dicts,
                top_k=top_k,
                threshold=threshold
            )
        else:
            # Text search fallback
            query_lower = query.lower()
            results = []
            for e in entry_dicts:
                content_lower = e.get('content', '').lower()
                # Check if query is substring of content
                if query_lower in content_lower:
                    # Score based on query length relative to content
                    score = len(query_lower) / len(content_lower)
                    results.append({
                        **e,
                        'similarity': min(score, 1.0)
                    })
            
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:top_k]
    
    def update_embedding(self, entry_id: str) -> Optional[MemoryEntry]:
        """Regenerate embedding for an existing entry"""
        entry = self.storage.load(entry_id)
        if not entry:
            return None
        
        if self.embedding is None:
            self.embedding = get_embedding_handler(use_embedding=True)
        
        entry.embedding = self.embedding.encode_single(entry.content).tolist()
        self.storage.save(entry)
        return entry
    
    def rebuild_all_embeddings(self, batch_size: int = 32) -> int:
        """Rebuild embeddings for all entries"""
        if self.embedding is None:
            self.embedding = get_embedding_handler(use_embedding=True)
        
        entries = self.storage.list_all()
        count = 0
        
        for entry in entries:
            if entry.content:
                entry.embedding = self.embedding.encode_single(entry.content).tolist()
                self.storage.save(entry)
                count += 1
        
        return count
    
    @staticmethod
    def _generate_id(content: str) -> str:
        """Generate unique ID from content"""
        timestamp = datetime.now().isoformat()
        combined = f"{content[:100]}{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def export_json(self, filepath: str = None) -> str:
        """Export all memories to JSON"""
        entries = self.storage.list_all()
        data = {
            "exported_at": datetime.now().isoformat(),
            "count": len(entries),
            "entries": [e.to_dict() for e in entries]
        }
        
        if filepath:
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        import json
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def import_json(self, filepath: str = None, json_str: str = None) -> int:
        """Import memories from JSON"""
        import json
        
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif json_str:
            data = json.loads(json_str)
        else:
            raise ValueError("Must provide filepath or json_str")
        
        count = 0
        for entry_data in data.get('entries', []):
            entry = MemoryEntry.from_dict(entry_data)
            # Don't regenerate embedding during import
            self.storage.save(entry)
            count += 1
        
        return count
