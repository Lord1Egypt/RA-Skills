"""Fixture: mutual recursion between two helpers."""
def _ping(count):
    """Call the other half of the cycle."""
    return _pong(count)


def _pong(count):
    """Call back into the cycle."""
    return _ping(count)
