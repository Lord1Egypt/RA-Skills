"""
V2 CLI 包装层 — M1.2 (2026-06-15)

职责:
  - 调 V2 CLI 子命令 (balance / today / history), 返 dashboard JSON Schema (§ 4)
  - 失败兜底: 读 /tmp/dashboard_cache.json (上次成功拉的)
  - 全部失败 → 返全占位 {"_error": "V2 CLI 不可用", ...}
  - DataSourceError 异常类 (server.py 兜底用)

跟 code/sim/desktop_sim.py 顶部 cli_call / fetch_data 同款 (复制改路径),
本文件是 M1.2 服务端版本, 仿真端继续用 desktop_sim 内部版 (避免 sim → server 反向依赖).
"""
import json
import os
import subprocess
import sys
from typing import Optional

# ==================== V2 CLI 路径配置 ====================

V2_CLI = "/home/wang/projects/kids-points-v2/runtime/cli.py"
V2_DB = "/home/wang/projects/kids-points-v2/runtime/data/kids_points.db"
CACHE_FILE = "/tmp/dashboard_cache.json"
CLI_TIMEOUT = 5  # V2 CLI 纯读, 正常 < 0.1s, 5s 足够

# ==================== 异常类 ====================


class DataSourceError(Exception):
    """V2 CLI 调失败 / 输出非合法 JSON / DB 不存在等. server.py catch 后返 503 + 缓存."""


# ==================== V2 CLI 包装 ====================


def cli_call(subcmd: list, timeout: int = CLI_TIMEOUT) -> Optional[dict]:
    """调 V2 CLI 子命令, 返 dict. 失败返 None (不抛, 让 fetch_data 统一兜底).

    Args:
        subcmd: 例 ["balance"] 或 ["history", "--days", "1", "--limit", "3"]
        timeout: subprocess timeout (秒)

    Returns:
        解析后的 dict, 或 None (调失败 / exit 非 0 / 非合法 JSON / 超时)
    """
    try:
        result = subprocess.run(
            ["python3", V2_CLI] + subcmd,
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode != 0:
            print(f"[data_source.cli_call] {subcmd} exit {result.returncode}: {result.stderr[:200]}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[data_source.cli_call] {subcmd} 失败: {e}", file=sys.stderr)
        return None


def fetch_data() -> dict:
    """拉 V2 数据组装成 § 4 dashboard JSON Schema.

    V2 production DB 数据稀疏 (V2 promotion 前) → today/history 可能返 0, 板显示"等待" 占位.
    失败兜底: 读 CACHE_FILE (上次成功拉的), 都没有 → 返全占位 + _error.

    Returns:
        dict: dashboard JSON schema (title / total_balance / today_count / today_net / recent / last_updated)
    """
    balance_data = cli_call(["balance"])
    today_data = cli_call(["today"])
    history_data = cli_call(["history", "--days", "7", "--limit", "5"])  # v4.9: 7 天 / 5 条 (老王要 5 行流水, 当天不足时跨天补)

    # 失败兜底: 读 cache (balance 或 today 至少一个失败就走 cache)
    if not balance_data or not today_data:
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE) as f:
                    cached = json.load(f)
                if cached.get("balance") is not None and cached.get("today") is not None:
                    print(f"[data_source.fetch_data] V2 CLI 失败, 用 cache {CACHE_FILE}", file=sys.stderr)
                    balance_data = cached["balance"]
                    today_data = cached["today"]
                    history_data = history_data or cached.get("history") or {"history": []}
            except Exception as e:
                print(f"[data_source.fetch_data] cache 读失败: {e}", file=sys.stderr)

    # 全部失败 → 返全占位
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

    # 类型符号映射 (V2 type → dashboard +/-)
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

    # v5.0: 加固 — 今日没交易时 today_net 必须为 0 (防止 V2 CLI bug 复发)
    #   之前观察到 today_count=0 时 today_net=+10 的 bug, 屏显示错误
    #   今日无数据 → net 一定是 0, 数学上不可能有 +10
    if out["today_count"] == 0:
        out["today_net"] = 0

    # 写 cache (下次失败兜底)
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"balance": balance_data, "today": today_data, "history": history_data}, f)
    except Exception as e:
        print(f"[data_source.fetch_data] cache 写失败: {e}", file=sys.stderr)

    return out
