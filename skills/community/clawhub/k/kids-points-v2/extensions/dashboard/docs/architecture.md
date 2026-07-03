# 系统架构

## 3 层架构

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: 桌面 LED 看板 (ESP32 + HUB75)                            │
│   96×128 像素, 琥珀色, 桌面书桌摆放                              │
│   /home/wang/projects/kids-points-v2/extensions/dashboard/code/esp32/desktop/desktop.ino (v4.9)              │
│                                                                  │
│   职责:                                                          │
│     - 连 WiFi, 连 server                                         │
│     - 每 5s HTTP GET /api/dashboard                              │
│     - memcmp 比对 last_rendered, 没变就静默                       │
│     - 全 U8g2 渲染 (wqy12_t_gb2312b + 7x13_tr)                   │
│     - 出错用 last_good 缓存                                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP GET 5s/次 (主)
                               │ (未来可加 WS push 触发立即拉)
┌──────────────────────────────▼──────────────────────────────────┐
│ Layer 2: Dashboard server (Flask :8080)                          │
│   /home/wang/projects/kids-points-v2/extensions/dashboard/code/server/server.py                              │
│   /home/wang/projects/kids-points-v2/extensions/dashboard/code/server/data_source.py (V2 CLI 包装)           │
│                                                                  │
│   职责:                                                          │
│     - GET /api/dashboard → 调 V2 CLI → 返 JSON Schema           │
│     - GET /api/health → 健康检查                                 │
│     - 失败兜底: /tmp/dashboard_cache.json                         │
│     - systemd unit: dashboard.service                            │
└──────────────────────────────┬──────────────────────────────────┘
                               │ subprocess (5s timeout, 实际 < 100ms)
                               │ cli_call(["balance"])
                               │ cli_call(["today"])
                               │ cli_call(["history", "--days", "7", "--limit", "5"])
┌──────────────────────────────▼──────────────────────────────────┐
│ Layer 3: kids-points V2 CLI (上游项目, 独立维护)                  │
│   ~/桌面/龙虾工作区/StuAgent/New project/kids-points-runtime/    │
│                                                                  │
│   职责:                                                          │
│     - cli.py balance → 返当前余额                                │
│     - cli.py today → 返今日统计                                  │
│     - cli.py history → 返 N 天 / M 条历史                        │
│     - cli.py add → 加积分记录                                    │
│     - 数据存 kids_points.db (SQLite)                             │
└─────────────────────────────────────────────────────────────────┘
```

## 数据流 (正常态)

```
1. ESP32 loop: 每 5s 检查 millis() - last_fetch_ms > 5000
2. fetch_dashboard():
   a. WiFi.status() check (不连 → return false)
   b. HTTPClient.get("http://YOUR_SERVER_IP:8080/api/dashboard")
   c. ArduinoJson 解析 body 到 DashboardData struct
   d. current_data = d, last_good = d, has_last_good = true
3. render_frame():
   a. memcmp(&current_data, &last_rendered) == 0 → return (静默不闪)
   b. 否则重画: fillScreen → 标题 → 横线 → 5 行流水 → 底栏
4. last_rendered = current_data
```

## Dashboard JSON Schema (server → ESP32)

```json
{
  "title": "KID POINTS",
  "total_balance": 77,        // int, 当前总积分
  "today_count": 3,            // int, 今日交易笔数
  "today_net": 10,             // int, 今日净增 (server bug: 显示 +10 实际应该 = 0)
  "recent": [
    {
      "date": "06-19",         // str, "MM-DD" (V2 DB 返的 date 切前 5 字符去掉 20xx)
      "type": "+",             // str, "+" 或 "-"
      "amount": 2,             // int, 绝对值
      "description": "口算题 | 今天做了20道题"  // str, 可含 "|" 分隔符
    },
    ...
  ],
  "last_updated": "2026-06-19T16:20:30",  // str ISO8601
  "_error": null               // str|null, 错误时为字符串 (ESP32 走 last_good)
}
```

ESP32 端 fetch_dashboard() 处理:
- `_error` 为 string → `d.has_error = true`, 渲染时红色显示 error_msg
- `recent[i]` < 5 条 → 后面补空行显示 "-"
- `description` 含 "|" → ESP32 端按 "|" 切只取前半段 (例: "口算题 | 今天做了20道题" → "口算题")
- `description` 无 "|" → 切 6 个中文字 (skip ASCII)

## 数据流 (异常态)

### ESP32 端网络挂
- `WiFi.status() != WL_CONNECTED` → `fetch_dashboard` return false, 不更新 current_data
- 渲染时 `last_good` 仍存在 → 用 last_good 数据继续显示 (老数据, 但能看)
- `has_last_good = false` (从未成功) → 显示 "WAITING" 占位

### server 端 V2 CLI 挂
- `cli_call` 返 None (subprocess 失败)
- `data_source.fetch_data()` 读 `/tmp/dashboard_cache.json` 兜底
- 都没了 → 返全占位 + `_error`, server 200 但 body 标记错误
- ESP32 收到 → 红色显示 error_msg

### server 完全挂 (HTTP timeout)
- ESP32 `http.setTimeout(5000)` → 5s 后 disconnect
- current_data 不变 → 渲染时 memcmp == 0 → 静默 (屏保持)
- last_good 是上次成功拉的 → 屏仍能看, 但数据"冻住"

## 未来扩展点 (待 M1.5+)

| 扩展 | 位置 | 当前 | 未来 |
|------|------|------|------|
|| in-memory cache (v5.4 取代 WS) | server.py | watchdog 标 cache dirty, 命中 0 subprocess | O(1) cache, 99% 命中, V2 隔离 |
| OTA 更新 | desktop.ino | 关 (省 RAM) | 留 5 行中预留一行显示版本号 |
| 多看板 | server.py + desktop.ino | 单屏 | 加屏 ID, 路由不同数据 |
| 历史翻页 | desktop.ino | 只显示最近 5 条 | 加按钮翻页 / 自动滚动 |

## 时序图 (1 个完整周期)

```
t=0.0s   ESP32 loop 触发 render_frame()
t=0.0s   memcmp == 0 (数据未变) → return, 屏静默
t=5.0s   ESP32 loop 触发 fetch_dashboard()
t=5.0s   HTTP GET → server Flask route
t=5.05s  data_source.fetch_data() → cli_call("balance") etc
t=5.06s  V2 CLI 返 JSON (< 100ms)
t=5.07s  server 包装成 dashboard JSON, 返 200
t=5.1s   ESP32 deserializeJson → current_data 更新
t=5.1s   render_frame() → memcmp != 0 → 重画
t=5.15s  屏显示新数据
t=10s    重复
```

**关键**: memcmp 智能渲染让"数据没变 = 屏不闪", 这是 v4.8 核心改进.