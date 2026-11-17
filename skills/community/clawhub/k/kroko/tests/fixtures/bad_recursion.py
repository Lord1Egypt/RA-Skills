"""Fixture: a function that calls itself."""
def _countdown(number):
    """Count down to zero."""
    if number <= 0:
        return 0
    return _countdown(number - 1)
