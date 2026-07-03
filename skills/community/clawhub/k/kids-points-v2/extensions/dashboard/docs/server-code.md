# Dashboard Server 详解

## 文件位置
- `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/server.py` (Flask + watchdog + **in-memory cache v5.4**, ~256 行)
- `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/data_source.py` (V2 CLI 包装, ~125 行)
- `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/dashboard.service` (systemd unit, 21 行)
- `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/requirements.txt` (Python 依赖: flask + watchdog, **v5.4 删 flask-sock/websocket-client**)

## 架构 (server 端, v5.4 cache 模式)

```
V2 写 SQLite
   ↓
watchdog Observer (inotify) 检测 mtime 变化
   ↓
mark_cache_dirty("watchdog: ...") (微秒级, 不调 subprocess)
   ↓
ESP32 5s 拉 GET /api/dashboard
   ↓
server.py Flask route
   ↓
get_cached_data()  (双重检查锁)
   ├─ cache_data + !cache_dirty → 直接返 cache (0 subprocess, 1ms)
   └─ cache_dirty → fetch_data() → 3 个 subprocess → 更新 cache → 返
                  ↓ (失败)
                兜底: /tmp/dashboard_cache.json
```

**v5.4 关键改动**: 之前每次 GET 都调 fetch_data() (subprocess 720/小时). 现在 99% 走 cache, subprocess 每天几次.

**WS 删了**: 之前用 flask-sock WS 推 `{"type":"refresh"}` 给 ESP32, 但 ESP32 不接 WSClient (库 +50KB Flash 风险), 僵尸代码. v5.4 改用 in-memory cache, 可靠性更好.

## server.py 关键代码

### 路由
```python
@app.route("/api/dashboard")
def api_dashboard():
    try:
        data = data_source.fetch_data()
        return jsonify(data), 200
    except Exception as e:
        # 全失败兜底: 返 503 + 错误 JSON, 让 ESP32 用 last_good
        return jsonify({"_error": str(e), ...}), 503

@app.route("/api/health")
def api_health():
    return {"status": "ok", "ts": ...}
```

### 启动
```python
# v5.4: WS 已删, 纯 Flask + watchdog + in-memory cache
app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
```

## data_source.py 关键代码

### V2 CLI 路径
```python
V2_CLI = "/home/wang/projects/kids-points-v2/runtime/cli.py"
V2_DB = "/home/wang/projects/kids-points-v2/runtime/data/kids_points.db"
CACHE_FILE = "/tmp/dashboard_cache.json"
CLI_TIMEOUT = 5  # V2 CLI 纯读, 正常 < 100ms, 5s 兜底
```

### cli_call 包装
```python
def cli_call(subcmd: list, timeout: int = CLI_TIMEOUT) -> Optional[dict]:
    try:
        result = subprocess.run(
            ["python3", V2_CLI] + subcmd,
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None
```

### fetch_data 主逻辑
```python
def fetch_data() -> dict:
    balance_data = cli_call(["balance"])
    today_data = cli_call(["today"])
    history_data = cli_call(["history", "--days", "7", "--limit", "5"])  # v4.9

    # balance 或 today 任一失败 → 读 cache
    if not balance_data or not today_data:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                cached = json.load(f)
            balance_data = cached.get("balance")
            today_data = cached.get("today")
            history_data = history_data or cached.get("history")

    # 全部失败 → 返全占位 + _error
    if not balance_data or not today_data:
        return {
            "title": "KID POINTS",
            "total_balance": None,
            "today_count": 0,
            "today_net": 0,
            "recent": [],
            "last_updated": None,
            "_error": "V2 CLI 不可用, 显示占位",
        }

    # 组装 dashboard JSON
    recent = []
    for tx in (history_data or {}).get("history", []):
        recent.append({
            "date": tx["date"][5:] if tx.get("date", "").startswith("20") else tx.get("date", ""),
            "type": "+" if tx.get("type") == "income" else "-",
            "amount": abs(tx.get("amount", 0)),
            "description": tx.get("description", ""),
        })

    out = {
        "title": "KID POINTS",
        "total_balance": balance_data.get("balance"),
        "today_count": today_data.get("tx_count", 0),
        "today_net": today_data.get("net", 0),
        "recent": recent,
        "last_updated": balance_data.get("as_of"),
    }

    # 写 cache
    with open(CACHE_FILE, "w") as f:
        json.dump({"balance": balance_data, "today": today_data, "history": history_data}, f)

    return out
```

### V2 CLI 子命令契约

| 子命令 | 返 JSON | 字段 |
|--------|---------|------|
| `cli.py balance` | `{"balance": int, "as_of": "ISO8601"}` | 当前余额 |
| `cli.py today` | `{"tx_count": int, "net": int, ...}` | 今日统计 |
| `cli.py history --days N --limit M` | `{"history": [{date, type, amount, description}, ...]}` | 最近历史 |
| `cli.py add ...` | - | 加积分 (ESP32 不调, V2 CLI 独立) |

V2 type 字段: `"income"` → "+", `"expense"` → "-" (dashboard schema 用单字符)

## systemd service

### 文件: `/home/wang/projects/kids-points-v2/extensions/dashboard/code/server/dashboard.service`
```ini
[Unit]
Description=Dashboard LED Matrix Server (Flask + watchdog + in-memory cache)  # v5.4
Documentation=/home/wang/projects/kids-points-v2/extensions/dashboard/docs/plan.md
After=network.target

[Service]
Type=simple
User=wang
WorkingDirectory=/home/wang/projects/kids-points-v2/extensions/dashboard/code/server
ExecStart=python3 /home/wang/projects/kids-points-v2/extensions/dashboard/code/server/server.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

MemoryMax=256M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
```

### 安装 (M1.5 待办)
```bash
# 1. 安装 service
sudo cp /home/wang/projects/kids-points-v2/extensions/dashboard/code/server/dashboard.service /etc/systemd/system/dashboard.service
sudo systemctl daemon-reload

# 2. 开机自启 + 立即启动
sudo systemctl enable --now dashboard

# 3. 看状态
sudo systemctl status dashboard
sudo journalctl -u dashboard -f
```

**注意**: ExecStart 用 hermes-agent 的 venv Python (里面有 flask / watchdog, **v5.4 删 flask-sock**)。**不是** 系统 Python (`/usr/bin/python3`)。如果 hermes-agent venv 路径变了, service 也要改。

## 启动方式 (3 种)

### 1. 前台手动 (调试用)
```bash
cd /home/wang/projects/kids-points-v2/extensions/dashboard/code/server
python3 server.py
# Ctrl+C 停止, 日志直接看 stdout
```

### 2. systemd (生产)
```bash
sudo systemctl start dashboard
```

### 3. 后台 nohup (老王之前用)
```bash
cd /home/wang/projects/kids-points-v2/extensions/dashboard/code/server
nohup python3 server.py > /tmp/dashboard.log 2>&1 &
# 杀: pkill -f "server.py"
```

## requirements.txt (v5.4 删 flask-sock)
```
flask>=3.0
watchdog>=4.0  # 监 V2 SQLite mtime, 标 in-memory cache dirty
```

## 已知 bug (M1.5 待修)

### today_net 显示 +10 实际 = 0
- **现象**: 屏底栏显示 `T+10 ALL:77`, 但今天实际没有 +10 的交易 (最近 5 条都是 +2/+3/-5)
- **根因 (推测)**: V2 CLI `today` 子命令的 `net` 字段计算逻辑有 bug, 可能没按日期过滤或累加错了
- **影响**: 仅显示问题, balance 正确 (77)
- **修复方向**: 查 V2 CLI `cli.py today` 实现, 或在 data_source.py 里手动按 recent 重算 net

## 验证
```bash
# 服务端
curl http://YOUR_SERVER_IP:8080/api/dashboard | python3 -m json.tool

# 健康检查
curl http://YOUR_SERVER_IP:8080/api/health

# 直接调 V2 CLI (排除 server 问题)
python3 \
  "/home/wang/projects/kids-points-v2/runtime/cli.py" today
```

## V2 CLI 集成说明

V2 CLI 是**独立上游项目**, 单独维护, 不属于本看板项目。本看板只**消费** V2 CLI 的输出。

依赖:
- V2 CLI 必须能跑 (`python3 cli.py balance` 不报错)
- V2 DB 路径正确 (`kids_points.db` 存在可读)
- V2 CLI Python 依赖装了 (V2 项目自己的 requirements.txt)

**修改 V2 CLI 时**: 需确保 `balance` / `today` / `history` 子命令的 JSON 输出 schema 不变, 否则本看板 server 会解析失败。