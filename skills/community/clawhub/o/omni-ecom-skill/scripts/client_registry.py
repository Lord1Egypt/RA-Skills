#!/usr/bin/env python3
"""Resolve the client-name registry without shipping private names in the package."""

from __future__ import annotations

import os
from pathlib import Path


ENV_NAME = "OMNI_ECOM_CLIENT_REGISTRY"


def resolve_client_registry(package_root: Path) -> Path:
    """ClawHub distribution: explicit authorized path or package examples only."""
    explicit = os.environ.get(ENV_NAME, "").strip()
    if explicit:
        return Path(explicit).expanduser().resolve()

    return (package_root / "config" / "client-brand-registry.json").resolve()
