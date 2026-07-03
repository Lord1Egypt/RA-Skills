"""
Family Dashboard - Flask Server (M1.5+ cache mode, 2026-06-20)
====================================================
状态: ✅ M1.5+ 完成 (Flask + watchdog V2 SQLite inotify + in-memory cache)

职责:
  - GET  /api/dashboard  → ESP32 拉取看板数据 (走 cache, dirty 才 fetch)
  - GET  /health         → 健康检查 (含 cache age + watchdog alive)
  - POST /api/push       → 手动标 cache dirty (debug 用, watchdog 漏触发时手动)
  - watchdog Observer    → 监听 V2 SQLite (IN_MODIFY/MOVED), 变化时标 cache_dirty
  - in-memory cache      → fetch_data() 结果缓存, 99% 请求走 cache (0 subprocess)

部署:
  - /home/wang/.hermes/hermes-agent/venv/bin/pip install flask watchdog
  - python server.py (默认端口 8080, 冲突改 8088 — 改代码顶部 PORT)
  - systemd: /etc/systemd/system/dashboard.service (见同目录 dashboard.service, M1.5 落地)

数据源: V2 SQLite via data_source.py (M1.2 包装层)

可靠性 (v5.4 老王决策):
  - subprocess 调用从 720/小时 → 每天几次 (V2 写 SQLite 才触发)
  - V2 / cli.py 挂掉时屏显示最后正常数据 (cache 命中, 零影响)
  - /tmp/dashboard_cache.json 兜底 (subprocess 全失败时)
  - watchdog 死掉 → /health 报 watchdog_alive=false, /api/push 手动恢复
"""
import os
import sys
import json
import time
import threading

from flask import Flask, jsonify
from flask_sock import Sock

from data_source import fetch_data, V2_DB, CACHE_FILE, DataSourceError

# watchdog 监听 V2 SQLite 变化 → 标 cache dirty
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ==================== CONFIG ====================

PORT = 8080  # 端口冲突改 8088
HOST = "0.0.0.0"
V2_DB_DIR = os.path.dirname(V2_DB)  # watchdog 监听目录 (inotify 单文件 on dir)

# ==================== in-memory cache (v5.4 引入) ====================
# 设计: watchdog 监听 V2 SQLite, 变化时标 cache_dirty=True.
#       下次 GET /api/dashboard 时, dirty → fetch_data() → 更新 cache.
#       干净 → 返回 cache_data (0 subprocess, 0 延迟).
# 收益: subprocess 调用从 720/小时 → 每天几次 (V2 写时才触发).
#       V2/cli 挂掉时屏显示最后正常数据, 可靠性显著提升.

cache_lock = threading.Lock()
cache_data = None            # 最近一次 fetch_data() 结果 (dict)
cache_dirty = True           # True = 需要 fetch; 启动时 True 强制首 fetch
cache_last_fetch = 0.0       # epoch time of last successful fetch
cache_fetching = False       # True = 当前有线程在 fetch (防重复)
watchdog_observer = None     # watchdog Observer 实例 (/health 查 is_alive)
_warmup_in_progress = True   # main 启动预热期间, watchdog 静默不响应事件 (防 race) ← 2026-06-28 B1 修复
ws_clients = set()           # WebSocket 客户端集合 (flask-sock)
ws_clients_lock = threading.Lock()


def mark_cache_dirty(reason: str = ""):
    """标 cache 为脏, 下次 GET 触发 fetch. watchdog + /api/push 都用."""
    global cache_dirty
    with cache_lock:
        cache_dirty = True
    if reason:
        print(f"[server.cache] dirty: {reason}", file=sys.stderr)
    # WS 广播 refresh 通知
    ws_broadcast({"type": "refresh", "reason": reason})


def get_cached_data() -> dict:
    """返回看板数据. 优先 cache; dirty 才 fetch (双重检查锁防重复 fetch)."""
    global cache_data, cache_dirty, cache_last_fetch, cache_fetching

    # 快速路径: 命中 (无锁读, 几乎免费)
    with cache_lock:
        if cache_data is not None and not cache_dirty:
            return cache_data

    # 慢路径: dirty 或 cache 空, 需要 fetch
    with cache_lock:
        # 双重检查: 另一线程可能已 fetch 完
        if cache_data is not None and not cache_dirty:
            return cache_data
        if cache_fetching:
            # 另一线程正在 fetch, 返回旧数据 (降级) 或报"首次 fetch 中"
            if cache_data is not None:
                return cache_data
            raise DataSourceError("首次 fetch 还在进行中, 稍后重试")
        cache_fetching = True

    # 锁外 fetch (避免长持锁, watchdog 标 dirty 可并发)
    try:
        new_data = fetch_data()
        with cache_lock:
            cache_data = new_data
            cache_dirty = False
            cache_last_fetch = time.time()
        return new_data
    finally:
        with cache_lock:
            cache_fetching = False


# ==================== watchdog V2 SQLite 监听 ====================


class V2DBHandler(FileSystemEventHandler):
    """V2 SQLite 文件变化 → 标 cache dirty (下次 GET 触发 fetch)."""

    def __init__(self):
        super().__init__()
        self._last_emit = 0.0
        self._cooldown = 0.5  # 500ms 防抖 (V2 写入可能触发多次 mtime 变化)

    def _maybe_emit(self, path: str):
        # 启动预热期间 watchdog 静默 (防 inotify 假事件触发 cache_dirty → 启动 race) ← 2026-06-28 B1 修复
        if _warmup_in_progress:
            return
        if not path or not path.endswith("kids_points.db"):
            return
        now = time.time()
        if now - self._last_emit < self._cooldown:
            return
        self._last_emit = now
        print(f"[server.watchdog] V2 DB 变化: {path}, 标 cache dirty")
        mark_cache_dirty(f"watchdog: {path}")

    def on_modified(self, event):
        if event.is_directory:
            return
        self._maybe_emit(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self._maybe_emit(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        self._maybe_emit(event.dest_path)


def start_watchdog():
    """启动 watchdog Observer 监听 V2 SQLite 目录. daemon 线程, 进程退出自动停."""
    global watchdog_observer
    handler = V2DBHandler()
    observer = Observer()
    observer.schedule(handler, V2_DB_DIR, recursive=False)
    observer.daemon = True
    observer.start()
    watchdog_observer = observer
    print(f"[server.watchdog] 启动监听 {V2_DB_DIR} (V2 DB: {V2_DB})")
    return observer


# ==================== WebSocket 广播 ====================


def ws_broadcast(msg: dict):
    """向所有连接的 WebSocket 客户端广播消息."""
    msg_str = json.dumps(msg)
    dead_clients = set()
    with ws_clients_lock:
        for ws in ws_clients:
            try:
                ws.send(msg_str)
            except Exception:
                dead_clients.add(ws)
        ws_clients.difference_update(dead_clients)
    if dead_clients:
        print(f"[server.ws] 移除 {len(dead_clients)} 个死连接", file=sys.stderr)


# ==================== Flask app ====================

app = Flask(__name__)
sock = Sock(app)


@app.route("/health", methods=["GET"])
def health():
    """健康检查. 返 cache 状态 (dirty / age / watchdog alive) + last_updated."""
    with cache_lock:
        last_updated = (cache_data or {}).get("last_updated")
        cache_age = (time.time() - cache_last_fetch) if cache_last_fetch else None
        cache_dirty_now = cache_dirty
    return jsonify({
        "ok": True,
        "v2_db": V2_DB,
        "last_updated": last_updated,
        "cache": {
            "dirty": cache_dirty_now,
            "age_sec": round(cache_age, 1) if cache_age is not None else None,
            "watchdog_alive": watchdog_observer.is_alive() if watchdog_observer else False,
        },
        "ws_clients": len(ws_clients),
    })


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """ESP32 5s 拉取看板数据. 走 cache (99% 命中), dirty 才 fetch."""
    try:
        data = get_cached_data()
        return jsonify(data)
    except DataSourceError as e:
        print(f"[server.get_dashboard] cache + fetch 全失败: {e}", file=sys.stderr)
        # 兜底: /tmp/dashboard_cache.json (data_source.fetch_data 失败时写过的快照)
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE) as f:
                    cached = json.load(f)
                balance = cached.get("balance", {}) or {}
                today = cached.get("today", {}) or {}
                return jsonify({
                    "title": "KID POINTS",
                    "total_balance": balance.get("balance"),
                    "today_count": today.get("tx_count", 0),
                    "today_net": today.get("net", 0),
                    "recent": [],
                    "last_updated": balance.get("as_of"),
                    "_warning": "V2 CLI 不可用, 显示上次 file cache",
                })
            except Exception as e2:
                print(f"[server.get_dashboard] file cache 也读失败: {e2}", file=sys.stderr)
        return jsonify({"_error": str(e), "title": "KID POINTS", "recent": []}), 503


@app.route("/api/push", methods=["POST"])
def push():
    """手动标 cache dirty. 老王: curl -X POST http://localhost:8080/api/push.
    下次 GET /api/dashboard 时会重新 fetch (V2 写完但 watchdog 没触发时手动)."""
    mark_cache_dirty("manual /api/push")
    return jsonify({"ok": True, "cache_marked_dirty": True})


@sock.route("/ws")
def ws_handler(ws):
    """WebSocket 端点. 客户端连上后加入广播列表, 收到 refresh 通知.
    连接断开自动清理.

    v5.4.1 增强: 新客户端连入后立即推 1 次 refresh (覆盖"启动时推 1 次"
    的旧行为 — 旧行为是 server 启动时推, 那时还没 client 接, 等于白推).
    新 client 立即收到信号, 主动 GET /api/dashboard 拿最新 (vs 等下次 inotify).
    """
    with ws_clients_lock:
        ws_clients.add(ws)
    print(f"[server.ws] 新客户端连入, 当前 {len(ws_clients)} 个", file=sys.stderr)
    # 推 1 次 refresh 给新 client (v5.4.1 增强)
    try:
        ws.send(json.dumps({"type": "refresh", "reason": "ws_connect"}))
    except Exception as e:
        print(f"[server.ws] 推初始 refresh 失败: {e}", file=sys.stderr)
    try:
        # 阻塞接收, 直到客户端断开
        while True:
            data = ws.receive(timeout=30)
            if data is None:
                break
    except Exception:
        pass
    finally:
        with ws_clients_lock:
            ws_clients.discard(ws)
        print(f"[server.ws] 客户端断开, 剩余 {len(ws_clients)} 个", file=sys.stderr)


# ==================== 启动 ====================


def main():
    print(f"[server] 启动 dashboard server (host={HOST}, port={PORT}, cache 模式 v5.4)")

    # 启动 watchdog (daemon 线程, 监听 V2 SQLite 标 cache_dirty)
    observer = start_watchdog()

    # 启动时预热 cache (避免首次 GET 走 subprocess, 加速首屏)
    try:
        data = fetch_data()
        with cache_lock:
            cache_data = data
            cache_dirty = False
            cache_last_fetch = time.time()
        # 开门: watchdog 从现在起才响应事件 (B1 修复: 防启动 race) ← 2026-06-28
        global _warmup_in_progress
        _warmup_in_progress = False
        print(f"[server] cache 预热: balance={data.get('total_balance')}, recent={len(data.get('recent', []))} 行, "
              f"last_updated={data.get('last_updated')}")
        # 预热完成后 WS 广播 1 次 (通知所有客户端初始数据已就绪)
        ws_broadcast({"type": "refresh", "reason": "startup_cache_warm"})
    except DataSourceError as e:
        print(f"[server] cache 预热失败 (但 server 继续跑, 首次 GET 会再试): {e}", file=sys.stderr)

    # 端口冲突提示 (加 SO_REUSEADDR 避 TIME_WAIT 误判)
    import socket as _sock
    s = _sock.socket(_sock.AF_INET, _sock.SOCK_STREAM)
    s.setsockopt(_sock.SOL_SOCKET, _sock.SO_REUSEADDR, 1)
    try:
        s.bind(("0.0.0.0", PORT))
        s.close()
    except OSError as e:
        print(f"[server] ⚠️ 端口 {PORT} 冲突: {e}. 改 PORT 顶部常量 (默认 8080 → 8088) 重启.", file=sys.stderr)
        observer.stop()
        sys.exit(1)

    # Flask 开发服务器跑 (production 用 gunicorn / waitress 替代, M3 可选)
    try:
        app.run(host=HOST, port=PORT, debug=False, use_reloader=False, threaded=True)
    finally:
        observer.stop()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()
