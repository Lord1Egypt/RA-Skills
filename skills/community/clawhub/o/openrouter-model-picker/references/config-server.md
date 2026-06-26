# config_server.py 参考

## 参数

```
--port PORT      监听端口，默认 18790
--idle SECONDS   空闲超时自动退出秒数，默认 600，0 = 永不自动退出
```

## 生命周期

| 事件 | 行为 |
|------|------|
| 启动 | 绑定 `127.0.0.1:<PORT>`，进入 `handle_request` 循环 |
| 任意请求（GET/POST/OPTIONS） | 重置 idle 计时器 |
| POST /apply 成功 | 设 shutdown flag → 下一个循环退出 |
| idle 超过 `--idle` 秒 | 自动退出 |
| SIGINT / SIGTERM | 正常退出 |

## API

### GET /health

```json
{"status": "ok", "idle_seconds": 0.0}
```

### GET /data

实时拉取 fetch_models.py 输出，返回完整 JSON（含 groups、current config）。

### POST /apply

```json
// Request
{"primary": "deepseek/deepseek-v3.2", "enabled": ["auto", "free", "deepseek/deepseek-v3.2"], "fallbacks": ["free", "auto"]}

// Response (success)
{"success": true, "primary": "openrouter/deepseek/deepseek-v3.2", "enabled_count": 3, "removed_count": 0, "hot_reloaded": true}

// Response (failure)
{"success": false, "error": "..."}
```

## 安全

- 仅绑定 loopback (`127.0.0.1`)
- CORS 允许所有来源（同机 Canvas 需要）
- 无认证（同机 localhost 不暴露）