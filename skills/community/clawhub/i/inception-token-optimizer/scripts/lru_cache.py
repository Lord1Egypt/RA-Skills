"""Simple LRU cache for prompt→response pairs."""

from collections import OrderedDict


class LRUCache:
    def __init__(self, maxsize: int = 256):
        self.maxsize = maxsize
        self.cache: OrderedDict = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)

    def clear(self):
        self.cache.clear()


if __name__ == "__main__":
    c = LRUCache(maxsize=3)
    c.set("a", 1)
    c.set("b", 2)
    c.set("c", 3)
    c.set("d", 4)  # evicts "a"
    assert c.get("a") is None, "a should be evicted"
    assert c.get("b") == 2
    print("LRU cache OK")
