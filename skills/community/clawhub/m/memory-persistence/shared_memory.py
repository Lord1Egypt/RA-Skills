"""
Shared Memory Manager - For sharing memories between agents
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from memory_system.memory_manager import MemoryManager
from memory_system.storage import MemoryEntry
from typing import List, Dict, Any, Optional


class SharedMemoryManager:
    """
    Manages shared memories accessible by multiple agents.
    
    Shared memories are stored in a separate repository/location and can be:
    - Read by any agent with access
    - Written by authorized agents
    - Tagged with source agent info
    
    Supports the same backends as MemoryManager:
    - local: Local file system
    - github: GitHub repository
    - gitee: Gitee repository
    """
    
    def __init__(
        self,
        backend: str = "local",
        shared_path: str = "./shared_memory",
        use_embedding: bool = False,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        **backend_kwargs
    ):
        """
        Initialize Shared Memory Manager
        
        Args:
            backend: Storage backend type (local/github/gitee)
            shared_path: Base path for local storage (or repo path for remote)
            use_embedding: Whether to use embedding for shared memories
            embedding_model: Embedding model name
            **backend_kwargs: Additional arguments for the backend
        """
        self.use_embedding = use_embedding
        self.embedding_model = embedding_model
        
        # Create MemoryManager for shared storage with specified backend
        self._manager = MemoryManager(
            backend=backend,
            base_path=shared_path,
            use_embedding=use_embedding,
            embedding_model=embedding_model,
            **backend_kwargs
        )
    
    @property
    def backend(self) -> str:
        """Get current backend type"""
        return self._manager.config.get('STORAGE_BACKEND', 'local')
    
    def add(
        self,
        content: str,
        agent_id: str = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> MemoryEntry:
        """
        Add a shared memory
        
        Args:
            content: Memory content
            agent_id: ID of the agent sharing this memory
            tags: Optional tags
            metadata: Optional metadata
        
        Returns:
            Created MemoryEntry
        """
        if tags is None:
            tags = []
        if agent_id:
            tags.append(f"agent:{agent_id}")
        
        if metadata is None:
            metadata = {}
        metadata['shared_by'] = agent_id or 'unknown'
        
        entry = self._manager.add(
            content=content,
            tags=tags,
            metadata=metadata,
            generate_embedding=True  # Shared memories always get embedding if enabled
        )
        return entry
    
    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a shared memory by ID"""
        return self._manager.get(entry_id)
    
    def delete(self, entry_id: str) -> bool:
        """Delete a shared memory"""
        return self._manager.delete(entry_id)
    
    def list(
        self,
        tags: List[str] = None,
        limit: int = None,
        offset: int = 0
    ) -> List[MemoryEntry]:
        """List shared memories with pagination"""
        return self._manager.list(tags=tags, limit=limit, offset=offset)
    
    def search(
        self,
        query: str,
        tags: List[str] = None,
        top_k: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search shared memories
        
        Args:
            query: Search query
            tags: Optional filter by tags
            top_k: Number of results
            threshold: Similarity threshold
        
        Returns:
            List of matching entries with similarity scores
        """
        return self._manager.search(
            query=query,
            tags=tags,
            top_k=top_k,
            threshold=threshold
        )
    
    def get_by_agent(self, agent_id: str) -> List[MemoryEntry]:
        """Get all shared memories from a specific agent"""
        return self._manager.list(tags=[f"agent:{agent_id}"])
    
    def export_all(self) -> str:
        """Export all shared memories as JSON"""
        return self._manager.export_json()
    
    def import_from(self, filepath: str) -> int:
        """Import shared memories from JSON file"""
        return self._manager.import_json(filepath=filepath)
