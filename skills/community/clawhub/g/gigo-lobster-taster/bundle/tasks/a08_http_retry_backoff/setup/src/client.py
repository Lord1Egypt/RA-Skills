import time
import urllib.request
import urllib.error


class FetchError(Exception):
    pass


def fetch(url, max_retries=3, base_delay=0.01, sleep=time.sleep):
    """TODO: add retry with exponential backoff."""
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            if r.status >= 500:
                raise FetchError(f"server {r.status}")
            return r.read().decode()
    except urllib.error.HTTPError as e:
        raise FetchError(f"http {e.code}") from e
    except urllib.error.URLError as e:
        raise FetchError(str(e)) from e
