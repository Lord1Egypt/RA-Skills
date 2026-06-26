from src.lru import lru


def test_calls_once():
    calls = {"n": 0}

    @lru(maxsize=2)
    def f(x):
        calls["n"] += 1
        return x * 2

    assert f(3) == 6
    assert calls["n"] == 1


def test_cache_hit():
    calls = {"n": 0}

    @lru(maxsize=2)
    def f(x):
        calls["n"] += 1
        return x * 2

    f(3)
    f(3)
    f(3)
    assert calls["n"] == 1


def test_different_args():
    calls = {"n": 0}

    @lru(maxsize=4)
    def f(x, y):
        calls["n"] += 1
        return x + y

    f(1, 2)
    f(1, 3)
    f(1, 2)
    assert calls["n"] == 2


def test_cache_evicts_oldest():
    calls = {"n": 0}

    @lru(maxsize=2)
    def f(x):
        calls["n"] += 1
        return x

    f(1)  # cache=[1]
    f(2)  # cache=[1,2]
    f(2)  # hit, marks 2 as MRU -> order [1, 2]
    f(3)  # add, evict LRU (1) -> cache=[2,3]
    assert calls["n"] == 3
    # 2 should still be cached
    f(2)
    assert calls["n"] == 3
    # 1 was evicted, miss again
    f(1)
    assert calls["n"] == 4
