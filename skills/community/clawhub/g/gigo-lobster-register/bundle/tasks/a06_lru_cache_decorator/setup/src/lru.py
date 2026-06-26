def lru(maxsize=128):
    """TODO: implement a real LRU cache decorator."""
    def deco(fn):
        def wrapper(*args, **kwargs):
            # 目前没缓存，直接透传
            return fn(*args, **kwargs)
        return wrapper
    return deco
