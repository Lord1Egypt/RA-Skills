"""
KB Framework Exceptions
========================

Custom exception hierarchy for the knowledge base framework.

Usage:
    from kb.framework.exceptions import KBFrameworkError, ChromaConnectionError

    try:
        chroma = ChromaIntegration()
    except ChromaConnectionError as e:
        logger.error(f"ChromaDB not available: {e}")
"""


class KBFrameworkError(Exception):
    """Base exception for all KB framework errors."""
    pass


class ConfigError(KBFrameworkError):
    """Configuration-related errors."""
    pass


class ChromaConnectionError(KBFrameworkError):
    """ChromaDB connection or initialization errors."""
    pass


class SearchError(KBFrameworkError):
    """Search execution errors."""
    pass


class EmbeddingError(KBFrameworkError):
    """Embedding generation or model errors."""
    pass


class DatabaseError(KBFrameworkError):
    """SQLite database errors."""
    pass


class PluginError(KBFrameworkError):
    """Plugin lifecycle errors."""
    pass


class PipelineError(KBFrameworkError):
    """Pipeline processing errors."""
    pass


class ProviderError(KBFrameworkError):
    """Search provider errors."""
    pass