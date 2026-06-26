"""
Storage Backend Base Class
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MemoryEntry:
    id: str
    content: str
    timestamp: str
    tags: List[str] = None
    embedding: List[float] = None
    metadata: Dict[str, Any] = None
    is_shared: bool = False
    group: str = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        return cls(**data)


class StorageBackend(ABC):
    """Abstract base class for storage backends"""
    
    @abstractmethod
    def init(self):
        """Initialize the storage"""
        pass
    
    @abstractmethod
    def save(self, entry: MemoryEntry) -> bool:
        """Save a memory entry"""
        pass
    
    @abstractmethod
    def load(self, entry_id: str) -> Optional[MemoryEntry]:
        """Load a memory entry by ID"""
        pass
    
    @abstractmethod
    def delete(self, entry_id: str) -> bool:
        """Delete a memory entry"""
        pass
    
    @abstractmethod
    def list_all(self) -> List[MemoryEntry]:
        """List all memory entries"""
        pass
    
    @abstractmethod
    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        """Search entries by tags"""
        pass
    
    def _entry_to_file(self, entry: MemoryEntry) -> str:
        return f"{entry.id}.json"
    
    def _serialize(self, entry: MemoryEntry) -> str:
        return json.dumps(entry.to_dict(), ensure_ascii=False, indent=2)
    
    def _deserialize(self, data: str) -> MemoryEntry:
        return MemoryEntry.from_dict(json.loads(data))
