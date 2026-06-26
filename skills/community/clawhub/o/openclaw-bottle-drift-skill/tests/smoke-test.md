# Smoke Test

## 本地验证

### 1. 启动 relay
```bash
python3 scripts/relay_server.py --host 127.0.0.1 --port 8765 --db /tmp/bottle-drift-test.sqlite3
```

预期：
- 输出包含 `dashboard_url`
- 浏览器访问 `http://127.0.0.1:8765/` 返回 200

### 2. Alice / Bob 心跳
```bash
python3 scripts/bottle_drift.py heartbeat --relay http://127.0.0.1:8765 --user-id alice --name "Alice"
python3 scripts/bottle_drift.py heartbeat --relay http://127.0.0.1:8765 --user-id bob --name "Bob"
```

预期：
- 两次命令均返回 `ok: true`

### 3. Alice 发送漂流瓶
```bash
python3 scripts/bottle_drift.py send --relay http://127.0.0.1:8765 --user-id alice --name "Alice" --message "测试烟雾验证消息"
```

预期：
- 返回 `bottle_id`
- `deliveries` 非空
- 每条记录包含 `reply_url`

### 4. Bob 查询 inbox
```bash
python3 scripts/bottle_drift.py inbox --relay http://127.0.0.1:8765 --user-id bob
```

预期：
- `received_bottles` 非空
- 每条记录包含 `reply_token` 和 `reply_url`

### 5. Bob 回信
可用两种方式：

#### 方式 A：浏览器打开 `reply_url`
- 输入昵称与回信内容
- 页面返回成功提示

#### 方式 B：CLI 直接回信
```bash
python3 scripts/bottle_drift.py reply --relay http://127.0.0.1:8765 --token <reply_token> --name "Bob" --reply "测试回信"
```

预期：
- 返回 `reply_id`
- 再次回同一个 token 会被拒绝

### 6. Alice 再查 inbox
```bash
python3 scripts/bottle_drift.py inbox --relay http://127.0.0.1:8765 --user-id alice
```

预期：
- `replies_received` 非空
- `reply_text` 与测试内容一致
- `sent_bottles[].reply_count` 变为 1

## 失败排查
- 若发送失败，确认至少有另一个用户在 120 秒内执行过 heartbeat
- 若回信页面打不开，确认 relay 正在运行且监听地址可访问
- 若返回 429，说明触发了频控，稍后重试
- 若网页中看不到数据，先点击“保存并上线”并检查浏览器 Console
