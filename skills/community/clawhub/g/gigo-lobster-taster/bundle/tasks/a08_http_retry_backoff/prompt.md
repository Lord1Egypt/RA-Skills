# HTTP 客户端加 retry 与指数退避

`src/client.py` 中有一个 `fetch(url, max_retries=3, base_delay=0.01, sleep=time.sleep)` 函数，目前调用一次失败就抛异常。请改为：

- 5xx 响应或网络异常时重试，最多 `max_retries` 次。
- 重试间隔为指数退避：第 i 次重试 sleep `base_delay * (2 ** i)`（i 从 0 开始）。
- 重试用完仍失败则抛异常。
- 通过传入的 `sleep` 回调而非 `time.sleep` 直接调用，方便测试断言退避序列。

`tests/test_client.py` 用 `http.server` 起一个本地 mock server，前 N 次返回 500，之后返回 200，并断言重试次数与退避序列。
