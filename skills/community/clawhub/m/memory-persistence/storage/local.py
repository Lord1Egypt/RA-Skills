"""
Local File Storage Backend
"""
import os
import json
from pathlib import Path
from typing import List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from memory_system.storage.base import StorageBackend, MemoryEntry


class LocalStorage(StorageBackend):
    def __init__(self, base_path: str = "./memory_data"):
        self.base_path = Path(base_path)
    
    def init(self):
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_entry_path(self, entry_id: str) -> Path:
        return self.base_path / f"{entry_id}.json"
    
    def save(self, entry: MemoryEntry) -> bool:
        try:
            path = self._get_entry_path(entry.id)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving entry {entry.id}: {e}")
            return False
    
    def load(self, entry_id: str) -> Optional[MemoryEntry]:
        try:
            path = self._get_entry_path(entry_id)
            if not path.exists():
                return None
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return MemoryEntry.from_dict(data)
        except Exception as e:
            print(f"Error loading entry {entry_id}: {e}")
            return None
    
    def delete(self, entry_id: str) -> bool:
        try:
            path = self._get_entry_path(entry_id)
            if path.exists():
                path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting entry {entry_id}: {e}")
            return False
    
    def list_all(self) -> List[MemoryEntry]:
        entries = []
        if not self.base_path.exists():
            return entries
        
        for file_path in self.base_path.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                entries.append(MemoryEntry.from_dict(data))
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue
        
        # Sort by timestamp descending (newest first)
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        return entries
    
    def search_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        all_entries = self.list_all()
        if not tags:
            return all_entries
        
        tag_set = set(t.lower() for t in tags)
        return [
            entry for entry in all_entries
            if tag_set.intersection(set(t.lower() for t in entry.tags))
        ]
