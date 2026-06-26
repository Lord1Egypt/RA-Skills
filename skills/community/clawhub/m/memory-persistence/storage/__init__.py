"""
Storage Backends
"""
from memory_system.storage.base import StorageBackend, MemoryEntry
from memory_system.storage.local import LocalStorage
from memory_system.storage.github import GitHubStorage
from memory_system.storage.gitee import GiteeStorage
from memory_system.storage.sqlite import SQLiteStorage

__all__ = ['StorageBackend', 'MemoryEntry', 'LocalStorage', 'GitHubStorage', 'GiteeStorage', 'SQLiteStorage']


def create_storage(backend_type: str, **kwargs) -> StorageBackend:
    """Factory function to create storage backend"""
    backends = {
        'local': LocalStorage,
        'github': GitHubStorage,
        'gitee': GiteeStorage,
        'sqlite': SQLiteStorage,
    }
    
    if backend_type not in backends:
        raise ValueError(f"Unknown backend type: {backend_type}. Available: {list(backends.keys())}")
    
    return backends[backend_type](**kwargs)
