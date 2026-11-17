"""Fixture: code that satisfies every gate in both modes."""
MAX_ATTEMPTS = 3


def retry_delay(attempt):
    """Return the backoff delay in seconds for one attempt."""
    # Caps are deliberate: the upstream stalls under sustained load.
    return min(2 ** attempt, MAX_ATTEMPTS)
