"""
VSA (Vector Symbolic Architecture) Blender
===========================================
Optional VSA operations for dream consolidation.

Vector Symbolic Architecture (VSA) provides holographic memory binding:
  - Circular convolution creates emergent concepts from vector pairs
  - Superposition blends multiple vectors into unified representation
  - Dream vector generation via pairwise binding + superposition

This module gracefully handles numpy dependency:
  - If numpy is available: full VSA binding/superposition
  - If numpy is missing: returns None (dream consolidation continues)

Functions:
    blend_dream_vector: Main entry point for VSA dream blending
    has_numpy: Check if numpy-based VSA is available

Author: Lilu / nima-core
"""

from __future__ import annotations

import logging
from typing import List, Optional

__all__ = [
    "blend_dream_vector",
    "has_numpy",
]

logger = logging.getLogger(__name__)


# ── Optional numpy / VSA ──────────────────────────────────────────────────────
try:
    import numpy as np
    from numpy.fft import fft, ifft

    def _vsa_bind(a: "np.ndarray", b: "np.ndarray") -> "np.ndarray":
        """Circular convolution — creates emergent concept from two vectors."""
        return ifft(fft(a) * fft(b)).real

    def _vsa_superpose(vecs: List["np.ndarray"]) -> Optional["np.ndarray"]:
        """Superposition — blend multiple vectors."""
        if not vecs:
            return None
        s = np.sum(vecs, axis=0)
        n = np.linalg.norm(s)
        return s / n if n > 0 else s

    def blend_dream_vector(embeddings: List) -> Optional["np.ndarray"]:
        """Create emergent dream vector via VSA binding."""
        arrs = [np.asarray(e) for e in embeddings if e is not None]
        if not arrs:
            return None
        if len(arrs) == 1:
            return arrs[0]
        bindings = []
        for i in range(0, len(arrs) - 1, 2):
            bindings.append(_vsa_bind(arrs[i], arrs[i + 1]))
        if len(arrs) % 2 == 1:
            bindings.append(arrs[-1])
        return _vsa_superpose(bindings)

    _HAS_NUMPY = True

except ImportError:
    _HAS_NUMPY = False

    def blend_dream_vector(embeddings: List) -> None:  # type: ignore[misc]
        return None


def has_numpy() -> bool:
    """Check if numpy-based VSA is available."""
    return _HAS_NUMPY
