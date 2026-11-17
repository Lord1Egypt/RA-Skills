"""
Compatibility helpers for different ChromaDB versions.
"""

from typing import Iterable, List, Any


def list_collection_names(collections: Iterable[Any]) -> List[str]:
    """
    Normalize Chroma list_collections() output across versions.

    ChromaDB < 0.6 may return collection objects.
    ChromaDB >= 0.6 returns collection names directly.
    """
    names = []
    for collection in collections:
        if isinstance(collection, str):
            names.append(collection)
        else:
            names.append(collection.name)
    return names
