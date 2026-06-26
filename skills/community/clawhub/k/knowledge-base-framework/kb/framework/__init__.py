"""
KB Framework Library
=====================

Core components for vector search and knowledge retrieval.

Architecture:
-------------
- ChromaIntegration: Vector DB connection (ChromaDB + sentence-transformers)
- HybridSearch: Unified search combining vector + keyword search
- EmbeddingPipeline: Text embedding with caching
- Reranker: Result scoring and reordering

Sub-Namespaces:
----------------
- kb.framework.search      → HybridSearch, SearchConfig, SearchResult, providers, reranker
- kb.framework.embeddings  → EmbeddingPipeline, ChromaIntegration, embedding utilities
- kb.framework.text        → build_embedding_text, parse_keywords, text utilities

Top-level re-exports (backward-compatible):
-------------------------------------------
HybridSearch, SearchResult, SearchConfig, ChromaIntegration,
EmbeddingPipeline, Reranker, SentenceChunker, StopwordHandler, etc.

Usage:
------
    # Sub-namespace (recommended for new code)
    from kb.framework import search
    results = search.HybridSearch().query("query", limit=5)

    # Top-level (backward-compatible)
    from kb.framework import HybridSearch
    search = HybridSearch()
    results = search.search("query", limit=5)
"""

__version__ = "0.1.0"

# Stable API symbols (backward-compatible across minor releases)
STABLE_API = [
    "HybridSearch",
    "SearchResult",
    "SearchConfig",
    "ChromaIntegration",
    "EmbeddingPipeline",
    "get_chroma",
    "StopwordHandler",
    "SynonymExpander",
    "Reranker",
    "ChromaSemanticProvider",
    "FTS5KeywordProvider",
    "SentenceChunker",
    "KBFrameworkError",
    "ChromaDBPlugin",
]

# ChromaDB Integration
from .chroma_integration import (
    ChromaIntegration,
    ChromaIntegrationV2,
    get_chroma,
    embed_text,
    embed_batch,
)

# Hybrid Search
from .hybrid_search import (
    HybridSearch,
    SearchResult,
    SearchConfig,
    get_search,
)

# Embedding Pipeline
from .embedding_pipeline import (
    EmbeddingPipeline,
    SectionRecord,
    EmbeddingJob,
)

# Reranker
from .reranker import (
    Reranker,
    get_reranker,
    rerank,
    RerankResult,
)

# Chunker
from .chunker import (
    Chunk,
    SentenceChunker,
    SimpleChunker,
    chunk_document,
)

# FTS5 Setup
from .fts5_setup import (
    check_fts5_available,
    setup_fts5,
    rebuild_fts5_index,
    get_fts5_stats,
)

# Stopwords
from .stopwords import (
    StopwordHandler,
    get_stopword_handler,
)

# Synonyms
from .synonyms import (
    SynonymExpander,
    get_expander,
    expand_query,
)

# Chroma Plugin
from .chroma_plugin import (
    ChromaDBPlugin,
    EmbeddingTask,
)

# ─── Sub-Module Namespaces ────────────────────────────────────────────
# Import sub-modules as objects so they can be accessed as namespaces:
#   kb.framework.search.HybridSearch
#   kb.framework.embeddings.EmbeddingPipeline
#   kb.framework.text.build_embedding_text

from . import hybrid_search as _search_modul
from . import embedding_pipeline as _embedding_modul
from . import chroma_integration as _chroma_modul
from . import text as _text_modul
from . import reranker as _reranker_modul
from . import search_providers as _providers_modul

search = _search_modul
"""Sub-namespace for search: HybridSearch, SearchConfig, SearchResult, providers."""

embeddings = _embedding_modul
"""Sub-namespace for embeddings: EmbeddingPipeline, ChromaIntegration, embed helpers."""

text = _text_modul
"""Sub-namespace for text utilities: build_embedding_text, parse_keywords."""

# Search Providers (DG-2: Interface-Extraktion)
from .search_providers import (
    ProviderResult,
    SemanticSearchProvider,
    KeywordSearchProvider,
)
from .providers import (
    ChromaSemanticProvider,
    FTS5KeywordProvider,
    get_semantic_provider,
    get_keyword_provider,
)

# Exceptions
from .exceptions import (
    KBFrameworkError,
    ConfigError,
    ChromaConnectionError,
    SearchError,
    EmbeddingError,
    DatabaseError,
    PluginError,
    PipelineError,
    ProviderError,
)

# Path utilities
from .paths import (
    get_default_db_path,
    get_default_chroma_path,
    get_default_library_path,
    get_default_workspace_path,
    get_default_cache_path,
)

# ─── Backward-Compat Note ──────────────────────────────────────────
# SearchResult is the canonical class from hybrid_search (imported above).
# ProviderResult (from search_providers) is the simplified provider-interface class.
# Both are re-exported; SearchResult remains in __all__ for compat.

__all__ = [
    # Version
    '__version__',
    'STABLE_API',
    # Sub-module namespaces
    'search',
    'embeddings',
    'text',
    # Core classes (backward-compatible top-level re-exports)
    'ChromaIntegration',
    'HybridSearch',
    'SearchResult',
    'ProviderResult',
    'SearchConfig',
    'EmbeddingPipeline',
    'Reranker',
    'StopwordHandler',
    'SynonymExpander',
    # Providers
    'ChromaSemanticProvider',
    'FTS5KeywordProvider',
    # Chunker (public convenience)
    'SentenceChunker',
    # Plugin
    'ChromaDBPlugin',
    # Exceptions (base only; subtypes available via kb.framework.exceptions)
    'KBFrameworkError',
]