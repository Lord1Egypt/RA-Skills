"""Mesh loading helpers for STL-based validation tools."""

from __future__ import annotations

import numpy as np
import trimesh


def load_mesh(path: str):
    """Load an STL mesh and reject obviously bad geometry."""
    try:
        mesh = trimesh.load(path, force="mesh")
    except Exception as exc:  # pragma: no cover - runtime dependency path
        raise ValueError(f"Failed to load mesh: {exc}") from exc

    if not hasattr(mesh, "vertices") or len(mesh.vertices) == 0:
        raise ValueError("Mesh contains no vertices")
    if not hasattr(mesh, "faces") or len(mesh.faces) == 0:
        raise ValueError("Mesh contains no faces")
    if not np.isfinite(mesh.vertices).all():
        raise ValueError("Mesh contains non-finite coordinates")
    return mesh
