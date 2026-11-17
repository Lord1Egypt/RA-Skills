"""Fixture: positional-only parameters must count towards arity."""
def _f(a, b, c, d, e, /, f):
    """Take six parameters, five of them positional-only."""
    return a
