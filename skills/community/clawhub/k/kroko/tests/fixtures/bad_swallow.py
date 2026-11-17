"""Fixture: an exception caught without naming a type."""
def _parse(value):
    """Parse the value, falling back on failure."""
    try:
        return int(value)
    except Exception:
        return 0
