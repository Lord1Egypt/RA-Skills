"""
Memory System Exceptions
"""


class MemoryError(Exception):
    """Base exception for memory system"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "MEMORY_ERROR"
        super().__init__(self.message)


class StorageError(MemoryError):
    """Storage related errors"""
    def __init__(self, message: str, code: str = "STORAGE_ERROR"):
        super().__init__(message, code)


class StorageNotFoundError(StorageError):
    """Memory entry not found"""
    def __init__(self, entry_id: str):
        super().__init__(f"Memory not found: {entry_id}", "NOT_FOUND")
        self.entry_id = entry_id


class StorageConnectionError(StorageError):
    """Cannot connect to storage backend"""
    def __init__(self, message: str):
        super().__init__(f"Connection error: {message}", "CONNECTION_ERROR")


class ValidationError(MemoryError):
    """Validation errors"""
    def __init__(self, message: str, field: str = None):
        code = f"VALIDATION_ERROR"
        super().__init__(message, code)
        self.field = field


class EmbeddingError(MemoryError):
    """Embedding related errors"""
    def __init__(self, message: str):
        super().__init__(message, "EMBEDDING_ERROR")


class SummarizerError(MemoryError):
    """LLM summarization errors"""
    def __init__(self, message: str):
        super().__init__(message, "SUMMARIZER_ERROR")


class ConfigError(MemoryError):
    """Configuration errors"""
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")
