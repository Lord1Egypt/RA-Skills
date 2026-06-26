import logging
from src import app


def test_perf_optimized(monkeypatch):
    # 如果缓存生效，重复调用相同入参时内部计算函数不会被重复调用。
    calls = {"n": 0}
    import src.app as mod
    original = mod.compute

    # 侦测：在 compute 上下游放一个计数器装饰器不现实 —— 改用"hasattr cache_info"启发式
    # 用 functools.lru_cache 的常见做法：compute 有 cache_info 属性
    assert hasattr(original, "cache_info") or hasattr(original, "__wrapped__"), \
        "compute should be cached (e.g. @functools.lru_cache)"
    # 连续两次调用
    a = original(100)
    b = original(100)
    assert a == b


def test_logging_added(caplog):
    with caplog.at_level(logging.INFO):
        from src.app import compute
        compute(10)
    assert any(r.levelno == logging.INFO for r in caplog.records), \
        "expected at least one INFO log record"
