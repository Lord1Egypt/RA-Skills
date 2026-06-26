# 给 Flask 应用添加 /health 端点

`src/app.py` 中有一个 Flask 应用，目前只有 `/` 端点。请新增一个 `GET /health` 端点：

- 返回 JSON：`{"status": "ok", "service": "lobster-eval"}`
- HTTP 200

`tests/test_health.py` 包含三个测试：`test_index_ok`（已通过）、`test_health_ok`、`test_health_json_shape`（当前失败）。
请修改 `src/app.py` 让全部测试通过。

不要修改 `tests/` 下的任何文件。
