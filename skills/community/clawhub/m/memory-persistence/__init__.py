"""
Memory System

A flexible memory system with optional embedding support and multiple storage backends.
Also supports shared memories for inter-agent communication.

Usage:
    from memory_system import MemoryManager
    
    # Basic usage
    mm = MemoryManager(backend='local')
    mm.add("Remember that the user prefers dark mode")
    
    # With embedding
    mm = MemoryManager(backend='local', use_embedding=True)
    results = mm.search("user preferences")
    
    # Shared memory between agents
    from memory_system import SharedMemoryManager
    smm = SharedMemoryManager(shared_path='./shared_memory')
    smm.add("Shared info from agent A", agent_id='agent_a")
"""

__version__ = "1.5.0"

from .config import Config
from .memory_manager import MemoryManager
from .shared_memory import SharedMemoryManager
from .summarizer import MemorySummarizer, ConversationMemoryProcessor
from .maintenance import MemoryMaintenance
from .templates import MemoryTemplates, MemoryTemplate
from .exceptions import (
    MemoryError,
    StorageError,
    StorageNotFoundError,
    StorageConnectionError,
    ValidationError,
    EmbeddingError,
    SummarizerError,
    ConfigError,
)
from .storage import StorageBackend, MemoryEntry, create_storage
from .storage.local import LocalStorage
from .storage.github import GitHubStorage
from .storage.gitee import GiteeStorage
from .embedding import EmbeddingHandler, get_embedding_handler

__all__ = [
    'MemoryManager',
    'SharedMemoryManager',
    'MemorySummarizer',
    'ConversationMemoryProcessor',
    'MemoryMaintenance',
    'MemoryTemplates',
    'MemoryTemplate',
    'Config',
    'MemoryEntry',
    'MemoryError',
    'StorageError',
    'StorageNotFoundError',
    'StorageConnectionError',
    'ValidationError',
    'EmbeddingError',
    'SummarizerError',
    'ConfigError',
    'StorageBackend',
    'LocalStorage',
    'GitHubStorage',
    'GiteeStorage',
    'EmbeddingHandler',
    'create_storage',
    'get_embedding_handler',
]
