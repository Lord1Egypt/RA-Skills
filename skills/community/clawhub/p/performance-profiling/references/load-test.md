# Web 压测工具

## Apache Bench (ab)

```bash
ab -n 1000 -c 10 https://example.com/
ab -n 100 -c 10 -p data.json -T application/json https://example.com/api

# 参数
# -n: 总请求数
# -c: 并发数
# -t: 超时时间
# -k: Keep-Alive
```

## wrk

```bash
wrk -t4 -c100 -d30s https://example.com

# 参数
# -t: 线程数
# -c: 连接数
# -d: 持续时间

# 使用 Lua 脚本
wrk -t4 -c100 -d30s -s script.lua https://example.com
```

```lua
-- script.lua
wrk.method = "POST"
wrk.body = '{"key":"value"}'
wrk.headers["Content-Type"] = "application/json"
```

## hey

```bash
go install github.com/rakyll/hey@latest

hey -n 1000 -c 50 https://example.com
hey -n 100 -m POST -H "Content-Type: application/json" -d '{"key":"value"}' https://example.com/api

# 参数
# -n: 总请求数
# -c: 并发数
# -q: 每个 worker 的 QPS 限制
# -z: 持续时间
```
