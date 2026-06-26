# 同步代码改写为 asyncio

`src/fetcher.py` 中有一段同步代码 `fetch_one(url_id)` 用 `time.sleep(0.05)` 模拟 IO，`fetch_all(ids)` 串行调用。

请把它重构为 asyncio 版本：

- 提供 `async def fetch_one(url_id) -> str`，用 `await asyncio.sleep(0.05)` 模拟 IO。
- 提供 `async def fetch_all(ids) -> list[str]`，用 `asyncio.gather` 并发执行所有 `fetch_one`。
- `fetch_one(i)` 返回 `f"item-{i}"`。

`tests/test_async.py` 用 `asyncio.run` 跑你的实现，并通过 AST 检查至少存在一个 `async def`。
