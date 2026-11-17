"""Fixture: state held at module scope."""
CACHE = {}


def _lookup(key):
    """Return a cached entry."""
    return CACHE.get(key)
