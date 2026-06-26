# Implement a concurrent LRU cache decorator

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 实现一个简单的 LRU 缓存装饰器

## Chinese source prompt

# 实现一个简单的 LRU 缓存装饰器

`src/lru.py` 中有 `lru(maxsize)` 装饰器的骨架，但功能未完成。请实现它，要求：

- 按参数组合缓存返回值；命中缓存时不再调用原函数。
- 当缓存项数超过 `maxsize` 时，淘汰最久未使用的一项（LRU）。
- 同一参数再次访问会被视为最近使用。
- **不允许** 直接 `from functools import lru_cache` 偷懒。

`tests/test_lru.py` 覆盖了以上需求。不要修改 `tests/`。
