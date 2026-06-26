"""Sentence-transformers embedding with optional dependency handling."""

from __future__ import annotations

import sys
import threading
from enum import Enum
from typing import ClassVar


class EmbedderState(Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    READY = "ready"
    ERROR = "error"


class Embedder:
    """Singleton embedder using sentence-transformers (optional dependency)."""

    _instance: ClassVar[Embedder | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    def __init__(self, model_name: str):
        self._model_name = model_name
        self._model = None
        self._state = EmbedderState.IDLE
        self._error: str | None = None

    @classmethod
    def get_instance(cls, model_name: str | None = None) -> Embedder:
        """Return the singleton Embedder instance."""
        with cls._lock:
            if cls._instance is None:
                if not model_name:
                    from lucid_skill.config import get_config
                    model_name = get_config().embedding.model
                cls._instance = cls(model_name)
            return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (for testing)."""
        with cls._lock:
            cls._instance = None

    def init(self) -> None:
        """Load the sentence-transformers model. Handles ImportError gracefully."""
        if self._state in (EmbedderState.READY, EmbedderState.INITIALIZING):
            return

        self._state = EmbedderState.INITIALIZING
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
            self._state = EmbedderState.READY
            print(
                f"[lucid-skill] embedder: loaded model {self._model_name}",
                file=sys.stderr,
            )
        except ImportError:
            self._state = EmbedderState.ERROR
            self._error = (
                "sentence-transformers is not installed. "
                "Install with: pip install sentence-transformers"
            )
            print(f"[lucid-skill] embedder: {self._error}", file=sys.stderr)
        except Exception as exc:
            self._state = EmbedderState.ERROR
            self._error = str(exc)
            print(f"[lucid-skill] embedder: failed to load model: {exc}", file=sys.stderr)

    def is_ready(self) -> bool:
        return self._state == EmbedderState.READY

    def get_state(self) -> EmbedderState:
        return self._state

    def get_model_id(self) -> str:
        return self._model_name

    def embed(self, text: str) -> bytes:
        """Embed text and return the vector as raw bytes (numpy tobytes)."""
        if not self.is_ready() or self._model is None:
            raise RuntimeError("Embedder is not ready")
        import numpy as np

        vector = self._model.encode(text, normalize_embeddings=True)
        return np.array(vector, dtype=np.float32).tobytes()

    @staticmethod
    def cosine_similarity(a: bytes, b: bytes) -> float:
        """Compute cosine similarity between two byte-encoded vectors."""
        import numpy as np

        va = np.frombuffer(a, dtype=np.float32)
        vb = np.frombuffer(b, dtype=np.float32)
        dot = np.dot(va, vb)
        norm_a = np.linalg.norm(va)
        norm_b = np.linalg.norm(vb)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot / (norm_a * norm_b))
