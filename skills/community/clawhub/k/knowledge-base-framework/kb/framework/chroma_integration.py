"""
ChromaDB Integration for Lumens Knowledge Base
===============================================

Phase 1: Vector Search Foundation
Local ChromaDB instance with SQLite as primary store.

Embedding model: sentence-transformers/all-MiniLM-L6-v2
Dimensionality: 384

Source: KB_Erweiterungs_Plan.md (Phase 1)

Singleton Pattern (Fix 3):
    One ChromaDB PersistentClient per process, thread-safe.
    Use `get_chroma()` or `ChromaIntegration.get_instance()` — NOT the
    constructor directly.  Direct constructor calls are redirected to the
    singleton so accidental `ChromaIntegration(path)` calls still share
    the same underlying client.

Lifecycle:
    - `get_chroma()` / `ChromaIntegration.get_instance()` → lazy init
    - `ChromaIntegration.shutdown()` → graceful cleanup (release client,
      unload model, reset singleton)
    - `ChromaIntegration.reset_instance()` → reset for tests (no cleanup)
"""

import atexit
import chromadb
import threading
import warnings
from chromadb.config import Settings
from chromadb.errors import NotFoundError as ChromaNotFoundError
from pathlib import Path
import logging
from typing import Optional
from contextlib import contextmanager

# Import config - lazy initialization to avoid module-level side effects
from .paths import get_default_base_path, get_default_chroma_path
from .exceptions import DatabaseError

logger = logging.getLogger(__name__)


def _validate_chroma_path(path: Path) -> Path:
    """Validate chroma path is within allowed KB directory."""
    base = get_default_base_path()
    try:
        path.resolve().relative_to(base.resolve())
    except ValueError:
        raise ValueError(f"Chroma path {path} is outside allowed directory {base}")
    return path


class ChromaIntegration:
    """
    ChromaDB wrapper for knowledge base integration — singleton per process.

    Thread-safe singleton: only one PersistentClient is ever created,
    regardless of how many times code calls `ChromaIntegration(...)` or
    `get_chroma()`.  All call-sites share the same client, model, and
    collections.

    Responsibility:
    - Connection management to ChromaDB (single PersistentClient)
    - Collection creation/retrieval
    - Embedding function (all-MiniLM-L6-v2)

    Usage:
        # Recommended — module-level convenience
        from kb.framework.chroma_integration import get_chroma
        chroma = get_chroma()

        # Or class-level
        from kb.framework.chroma_integration import ChromaIntegration
        chroma = ChromaIntegration.get_instance()

        # Graceful shutdown at end of process
        ChromaIntegration.shutdown()

        # For tests only — reset without cleanup
        ChromaIntegration.reset_instance()
    """

    # Class-level singleton state (NOT inherited by subclasses)
    _instance: Optional['ChromaIntegration'] = None
    _lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        """Enforce singleton — constructor redirects to get_instance().

        This ensures that legacy code writing `ChromaIntegration(path)`
        still gets the shared singleton instead of creating a duplicate.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                # Mark as needing __init__ on first creation
                cls._instance._needs_init = True  # type: ignore[attr-defined]
            else:
                # Subsequent constructor calls: skip __init__
                cls._instance._needs_init = False  # type: ignore[attr-defined]
        return cls._instance

    def __init__(
        self,
        chroma_path: str = None,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize ChromaDB connection (once only).

        Uses singleton pattern — subsequent calls with different args
        are silently ignored after first initialization.

        Args:
            chroma_path: Path for persistent ChromaDB instance
            model_name: Embedding model (Hugging Face model name)
        """
        # Guard: only init on first construction
        if not getattr(self, '_needs_init', False):
            return

        if chroma_path is None:
            self.chroma_path = get_default_chroma_path()
        else:
            self.chroma_path = _validate_chroma_path(Path(chroma_path).expanduser())
        self.chroma_path.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name
        self._model = None
        self._client = None
        self._needs_init = False

        logger.info(f"ChromaIntegration init: path={self.chroma_path}, model={model_name}")

    # =========================================================================
    # Client & Model (lazy, single-instance)
    # =========================================================================

    @property
    def client(self) -> chromadb.PersistentClient:
        """Lazy-load ChromaDB PersistentClient (one per process)."""
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=str(self.chroma_path),
                settings=Settings(anonymized_telemetry=False)
            )
            logger.info("ChromaDB PersistentClient initialized (singleton)")
        return self._client

    @property
    def model(self):
        """Lazy-load Sentence Transformer Model."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            logger.info(f"Sentence Transformer loaded: {self.model_name}")
        return self._model

    # =========================================================================
    # Embedding Methods
    # =========================================================================

    def embed_text(self, text: str) -> list[float]:
        """
        Converts text to vector embedding.

        Args:
            text: Input text

        Returns:
            Normalized embedding vector (384 dimensions)
        """
        if not text or not text.strip():
            return [0.0] * 384
        return self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()

    def embed_batch(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """
        Batch embedding for multiple texts.

        Args:
            texts: List of texts
            batch_size: Batch size for inference

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        return self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=batch_size,
            show_progress_bar=True
        ).tolist()

    # -------------------------------------------------------------------------
    # Phase 4: Alternative Embedding Model
    # -------------------------------------------------------------------------

    @property
    def alternative_model_name(self) -> str:
        """Phase 4: Alternative model name for better multilingual support."""
        return "paraphrase-multilingual-MiniLM-L12-v2"

    def embed_text_v2(self, text: str) -> list[float]:
        """
        Embed text using the alternative multilingual model.

        Phase 4: paraphrase-multilingual-MiniLM-L12-v2
        Better for mixed German/English content.

        Args:
            text: Input text

        Returns:
            Normalized embedding vector (384 dimensions)
        """
        if not text or not text.strip():
            return [0.0] * 384

        # Cache the V2 model on the instance so we don't reload every call
        if not hasattr(self, '_v2_model') or self._v2_model is None:
            from sentence_transformers import SentenceTransformer
            self._v2_model = SentenceTransformer(self.alternative_model_name)
            logger.info(f"V2 Sentence Transformer loaded: {self.alternative_model_name}")

        return self._v2_model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False
        ).tolist()

    def embed_batch_v2(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """
        Batch embedding using the alternative multilingual model.

        Phase 4: paraphrase-multilingual-MiniLM-L12-v2

        Args:
            texts: List of texts
            batch_size: Batch size for inference

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        if not hasattr(self, '_v2_model') or self._v2_model is None:
            from sentence_transformers import SentenceTransformer
            self._v2_model = SentenceTransformer(self.alternative_model_name)
            logger.info(f"V2 Sentence Transformer loaded: {self.alternative_model_name}")

        return self._v2_model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=batch_size,
            show_progress_bar=True
        ).tolist()

    def switch_to_v2_model(self) -> 'ChromaIntegrationV2':
        """
        Create a separate instance with the V2 (multilingual) model.

        Phase 4: Returns a ChromaIntegrationV2 (non-singleton) with
        paraphrase-multilingual-MiniLM-L12-v2.
        Does NOT modify the singleton instance.

        Returns:
            New ChromaIntegrationV2 with V2 model
        """
        v2 = ChromaIntegrationV2(chroma_path=str(self.chroma_path))
        logger.info(f"Switched to V2 model: {self.alternative_model_name}")
        return v2

    # -------------------------------------------------------------------------
    # Collection Management
    # -------------------------------------------------------------------------

    def get_or_create_collection(
        self,
        name: str,
        metadata: Optional[dict] = None
    ) -> chromadb.Collection:
        """
        Creates or retrieves a collection.

        Args:
            name: Collection name
            metadata: Optional metadata

        Returns:
            ChromaDB collection
        """
        try:
            collection = self.client.get_collection(name=name)
            logger.info(f"Collection retrieved: {name}")
        except ChromaNotFoundError:
            collection = self.client.create_collection(
                name=name,
                metadata=metadata or {"description": f"Collection: {name}"}
            )
            logger.info(f"Collection created: {name}")

        return collection

    def delete_collection(self, name: str) -> bool:
        """
        Deletes a collection.

        Args:
            name: Collection name

        Returns:
            True if deleted
        """
        try:
            self.client.delete_collection(name=name)
            logger.info(f"Collection deleted: {name}")
            return True
        except (chromadb.errors.ChromaError, ConnectionError) as e:
            logger.warning(f"Could not delete collection {name}: {e}")
            return False

    # -------------------------------------------------------------------------
    # Pre-configured Collections
    # -------------------------------------------------------------------------

    # Alternative embedding models
    # Phase 4: paraphrase-multilingual-MiniLM-L12-v2 (better multilingual, 384 dim)
    ALTERNATIVE_MODELS = {
        "paraphrase-multilingual-MiniLM-L12-v2": {
            "dimension": 384,
            "description": "Better multilingual support, recommended for mixed DE/EN content"
        }
    }

    @property
    def sections_collection(self) -> chromadb.Collection:
        """Collection for file_sections embeddings (original model)."""
        return self.get_or_create_collection(
            name="kb_sections",
            metadata={
                "description": "Knowledge Base Sections Embeddings",
                "embedding_model": self.model_name,
                "dimension": 384
            }
        )

    @property
    def sections_collection_v2(self) -> chromadb.Collection:
        """
        Collection for file_sections embeddings using paraphrase-multilingual-MiniLM-L12-v2.

        Phase 4: New embedding model with better multilingual support.
        768 → 384 dimensions (MiniLM-L12-v2 is 384, not 768 as sometimes stated).
        """
        model_key = "paraphrase-multilingual-MiniLM-L12-v2"
        dim = self.ALTERNATIVE_MODELS[model_key]["dimension"]

        return self.get_or_create_collection(
            name="kb_sections_v2",
            metadata={
                "description": "Knowledge Base Sections Embeddings V2 (multilingual)",
                "embedding_model": model_key,
                "dimension": dim
            }
        )

    @property
    def entities_collection(self) -> chromadb.Collection:
        """Collection for knowledge graph entities."""
        return self.get_or_create_collection(
            name="kg_entities",
            metadata={
                "description": "Knowledge Graph Entities Embeddings",
                "embedding_model": self.model_name,
                "dimension": 384
            }
        )

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def get_collection_stats(self, collection_name: str) -> dict:
        """Retrieves statistics for a collection."""
        collection = self.client.get_collection(collection_name)
        return {
            "name": collection.name,
            "count": collection.count(),
            "metadata": collection.metadata
        }

    def delete_by_file_id(self, file_id: str, collection_name: str = "kb_sections") -> int:
        """
        Deletes all embeddings for a file_id from ChromaDB.

        ChromaDB does not support DELETE with WHERE, so:
        1. Query all IDs with matching file_id via metadata
        2. Delete via delete_by_ids()

        Args:
            file_id: UUID of the file
            collection_name: ChromaDB collection name

        Returns:
            Number of deleted entries
        """
        try:
            collection = self.client.get_collection(name=collection_name)

            # Query all IDs with matching file_id in metadata
            results = collection.get(where={"file_id": file_id})

            if not results or not results.get('ids'):
                logger.debug(f"No ChromaDB entries found for file_id: {file_id}")
                return 0

            ids_to_delete = results['ids']
            collection.delete(ids=ids_to_delete)

            logger.info(f"Deleted {len(ids_to_delete)} entries from ChromaDB for file_id: {file_id}")
            return len(ids_to_delete)

        except (chromadb.errors.ChromaError, ConnectionError) as e:
            logger.error(f"Error deleting from ChromaDB for file_id {file_id}: {e}")
            self._last_delete_error = DatabaseError(f"ChromaDB delete failed: {e}")
            self._last_delete_error.__cause__ = e
            return 0

    def list_collections(self) -> list[dict]:
        """Lists all collections with statistics."""
        collections = self.client.list_collections()
        return [
            {
                "name": c.name,
                "count": c.count(),
                "metadata": c.metadata
            }
            for c in collections
        ]

    def reset_all(self) -> None:
        """Reset all collections (dangerous!)."""
        self.client.reset()
        logger.warning("All ChromaDB collections reset!")

    # =========================================================================
    # Singleton Access & Lifecycle
    # =========================================================================

    @classmethod
    def get_instance(cls, **kwargs) -> 'ChromaIntegration':
        """Thread-safe singleton access for connection sharing.

        Always returns the same instance; first call initializes it.
        Subsequent calls ignore kwargs (singleton is already initialized).
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(**kwargs)
        return cls._instance

    @classmethod
    def shutdown(cls) -> None:
        """Gracefully shut down the singleton: release client and model.

        Safe to call multiple times.  After shutdown, the next call to
        `get_instance()` or `get_chroma()` will create a fresh instance.
        """
        with cls._lock:
            if cls._instance is not None:
                inst = cls._instance
                # Release ChromaDB client (PersistentClient has no explicit
                # close, but dropping the reference lets GC reclaim SQLite
                # file handles)
                inst._client = None
                inst._model = None
                if hasattr(inst, '_v2_model'):
                    inst._v2_model = None
                cls._instance = None
                logger.info("ChromaIntegration singleton shut down")

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton for tests (no cleanup, just drops reference).

        Prefer `shutdown()` in production.  Use this only in test fixtures
        where you want a clean slate without waiting for GC.
        """
        with cls._lock:
            if cls._instance is not None:
                cls._instance._client = None
                cls._instance._model = None
                if hasattr(cls._instance, '_v2_model'):
                    cls._instance._v2_model = None
            cls._instance = None


# =============================================================================
# ChromaIntegrationV2 - Non-singleton variant for V2 multilingual model
# =============================================================================

def deprecated(reason: str):
    """Decorator to mark functions/classes as deprecated."""
    def decorator(obj):
        if isinstance(obj, type):
            # Class decorator
            original_init = obj.__init__
            def __init__(self, *args, **kwargs):
                warnings.warn(reason, DeprecationWarning, stacklevel=2)
                original_init(self, *args, **kwargs)
            obj.__init__ = __init__
            obj.__doc__ = (obj.__doc__ or "") + f"\n\n    .. deprecated::\n        {reason}"
            obj._deprecated_reason = reason
            return obj
        else:
            # Function decorator
            import functools
            @functools.wraps(obj)
            def wrapper(*args, **kwargs):
                warnings.warn(reason, DeprecationWarning, stacklevel=2)
                return obj(*args, **kwargs)
            wrapper.__doc__ = (wrapper.__doc__ or "") + f"\n\n    .. deprecated::\n        {reason}"
            return wrapper
    return decorator


@deprecated("ChromaIntegrationV2 is deprecated. Use ChromaIntegration with reset_instance() instead. Will be removed in v0.2.0.")
class ChromaIntegrationV2(ChromaIntegration):
    """
    ChromaDB integration using the V2 multilingual embedding model.

    .. deprecated:: 0.1.0
        Use ChromaIntegration directly (it now supports non-singleton mode via reset_instance).
        Will be removed in v0.2.0.

    Non-singleton - each call creates a fresh instance.
    Use when you need the paraphrase-multilingual-MiniLM-L12-v2 model
    instead of the default all-MiniLM-L6-v2.

    Shares the same PersistentClient as the singleton via get_shared_client().
    """

    # V2 has its own class-level state — does NOT share _instance with parent
    _instance = None
    _lock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        """Non-singleton: always creates a new V2 instance."""
        # Bypass ChromaIntegration.__new__ singleton logic entirely
        instance = object.__new__(cls)
        instance._needs_init = True  # type: ignore[attr-defined]
        return instance

    def __init__(self, chroma_path: str = None, **kwargs):
        """Initialize with V2 multilingual model."""
        if not getattr(self, '_needs_init', False):
            return

        model_name = kwargs.pop('model_name', 'paraphrase-multilingual-MiniLM-L12-v2')
        if chroma_path is None:
            self.chroma_path = get_default_chroma_path()
        else:
            self.chroma_path = _validate_chroma_path(Path(chroma_path).expanduser())
        self.chroma_path.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name
        self._model = None
        self._client = None
        self._needs_init = False
        logger.info(f"ChromaIntegrationV2 init: path={self.chroma_path}, model={model_name}")

    @property
    def client(self) -> chromadb.PersistentClient:
        """Reuse the singleton's PersistentClient if available, else create one.

        This prevents V2 instances from opening redundant SQLite connections.
        """
        if self._client is None:
            # Try to borrow from the singleton first
            singleton = ChromaIntegration._instance
            if singleton is not None and singleton._client is not None:
                self._client = singleton._client
                logger.info("ChromaIntegrationV2 reusing singleton PersistentClient")
            else:
                self._client = chromadb.PersistentClient(
                    path=str(self.chroma_path),
                    settings=Settings(anonymized_telemetry=False)
                )
                logger.info("ChromaIntegrationV2 created own PersistentClient")
        return self._client


# =============================================================================
# Convenience Functions (Module-Level API)
# =============================================================================

def get_chroma(**kwargs) -> ChromaIntegration:
    """Gets or creates global ChromaIntegration instance (thread-safe singleton).

    This is the canonical entry point for all ChromaDB access.
    Delegates to ChromaIntegration.get_instance() — there is no separate
    module-level global instance that could diverge.
    """
    return ChromaIntegration.get_instance(**kwargs)

def embed_text(text: str) -> list[float]:
    """Convenience: Single text embedding via the singleton."""
    return get_chroma().embed_text(text)

def embed_batch(texts: list[str], **kwargs) -> list[list[float]]:
    """Convenience: Batch text embedding via the singleton."""
    return get_chroma().embed_batch(texts, **kwargs)


# =============================================================================
# At-exit cleanup: release ChromaDB resources on process shutdown
# =============================================================================

def _atexit_cleanup():
    """Release ChromaDB singleton on interpreter exit."""
    try:
        ChromaIntegration.shutdown()
    except (chromadb.errors.ChromaError, ConnectionError) as e:
        logger.debug(f"At-exit cleanup failed: {e}")

atexit.register(_atexit_cleanup)


# =============================================================================
# Main: Quick Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ChromaDB Integration - Quick Test")
    print("=" * 60)

    # --- Singleton verification ---
    a = ChromaIntegration()
    b = ChromaIntegration()
    print(f"\n[Singleton Check]")
    print(f"  a is b: {a is b}")
    print(f"  id(a) == id(b): {id(a) == id(b)}")
    print(f"  a.client is b.client: {a.client is b.client}")

    # --- Module-level function check ---
    c = get_chroma()
    print(f"  get_chroma() is a: {c is a}")

    chroma = a

    # Test embedding
    test_texts = [
        "MTHFR Genmutation C677T Behandlung mit 5-MTHF",
        "BSV Blockchain Semantic Verification für KI-Agenten",
        "LDL Cholesterin Zielwert unter 100 mg/dL"
    ]

    print("\n[1] Testing Embedding...")
    embeddings = chroma.embed_batch(test_texts)
    print(f"   Generated {len(embeddings)} embeddings")
    print(f"   Dimension: {len(embeddings[0]) if embeddings else 0}")

    print("\n[2] Testing Collection Management...")
    collection = chroma.sections_collection
    print(f"   Collection: {collection.name}")
    print(f"   Count: {collection.count()}")

    print("\n[3] Listing Collections...")
    for col in chroma.list_collections():
        print(f"   - {col['name']}: {col['count']} items")

    print("\n[4] Testing Query (semantic search)...")
    test_query = "Genetische Behandlung Methylierung"
    query_emb = chroma.embed_text(test_query)

    # Add some test data first
    test_ids = ["test1", "test2", "test3"]
    test_metadatas = [
        {"source": "gesundheit", "type": "fact"},
        {"source": "projekte", "type": "fact"},
        {"source": "gesundheit", "type": "advice"}
    ]

    collection.upsert(
        ids=test_ids,
        embeddings=embeddings,
        metadatas=test_metadatas,
        documents=test_texts
    )
    print(f"   Upserted {len(test_ids)} test documents")

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=3
    )
    print(f"   Query: '{test_query}'")
    print(f"   Results: {len(results['ids'][0])} matches")

    # --- Shutdown test ---
    print("\n[5] Testing shutdown...")
    ChromaIntegration.shutdown()
    after = ChromaIntegration.get_instance()
    print(f"   After reset, new instance: {id(after) != id(a)}")

    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)