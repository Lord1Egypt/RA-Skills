"""kids-points CLI 交互入口。

用法：
    python3 cli.py                          # 交互模式
    python3 cli.py "口算加1分"               # 单条消息
    python3 cli.py --daily                  # 生成昨日日报
    python3 cli.py --monthly                # 生成上月月报
    python3 cli.py --replay [...]          # 回放历史消息到隔离 SQLite（见 replay.py）
    python3 cli.py balance                 # ⭐ dashboard: 当前余额 (JSON)
    python3 cli.py today                   # ⭐ dashboard: 今日积分 (JSON)
    python3 cli.py history --days 7        # ⭐ dashboard: 近期历史 (JSON)

⭐ dashboard CLI (2026-06-14 老王拍板, MVP for ESP32 dashboard):
    - 读 V2 SQLite, 跟 V1 永不动硬约束兼容
    - JSON 输出 (machine-readable, ESP32 直接 json.loads)
    - Exit codes: 0=ok, 1=db error, 2=invalid args
    - 不调 LLM (纯读, 0 token)
    - 不加认证 (本地部署家庭项目)
"""
import sys
import os
import json
from datetime import date, timedelta

# 确保能找到同目录的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .db import (
    init_db, get_current_balance, get_daily_stats,
    get_transactions_range, cents_to_display,
)
from .pipeline import process_message, call_llm as _call_llm
from reports import generate_daily_report, generate_monthly_report

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "kids_points.db")


# ─── ⭐ dashboard CLI commands (MVP, 2026-06-14) ─────────────────────────────

def _json_out(obj, pretty: bool = True) -> None:
    """统一 JSON 输出, ensure_ascii=False 让中文不转 \\uXXXX。"""
    indent = 2 if pretty else None
    print(json.dumps(obj, ensure_ascii=False, indent=indent))


def cmd_balance() -> int:
    """当前余额 (含 as_of 时间戳)。"""
    try:
        conn = init_db(DB_PATH)
        b = get_current_balance(conn)
        last_row = conn.execute(
            "SELECT created_at FROM transactions ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
        conn.close()
    except Exception as e:
        _json_out({"error": "db_error", "message": str(e)})
        return 1

    _json_out({
        "balance": b,
        "balance_display": cents_to_display(b),
        "as_of": last_row[0] if last_row else None,
        "source": "v2_sqlite",
    })
    return 0


def cmd_today() -> int:
    """今日积分 (date 自动取本地日期, MVP 锁定 GMT+8 由系统 tz 决定)。"""
    today_str = date.today().isoformat()
    try:
        conn = init_db(DB_PATH)
        stats = get_daily_stats(conn, today_str)
        conn.close()
    except Exception as e:
        _json_out({"error": "db_error", "message": str(e)})
        return 1

    _json_out({
        "date": stats["date"],
        "income": stats["income_total"],
        "expense": stats["expense_total"],
        "net": stats["net"],
        "tx_count": stats["income_count"] + stats["expense_count"],
        "balance": stats["balance"],
        "balance_display": cents_to_display(stats["balance"]),
    })
    return 0


def cmd_history(days: int = 7, limit: int = 50) -> int:
    """近期历史 (--days N 取最近 N 天, --limit M 取最多 M 条, 默认 7 天/50 条)。"""
    if days < 1 or days > 365:
        _json_out({"error": "invalid_args", "message": "--days 必须在 1-365"})
        return 2
    if limit < 1 or limit > 1000:
        _json_out({"error": "invalid_args", "message": "--limit 必须在 1-1000"})
        return 2

    end = date.today()
    start = end - timedelta(days=days - 1)
    try:
        conn = init_db(DB_PATH)
        txs = get_transactions_range(conn, start.isoformat(), end.isoformat())
        conn.close()
    except Exception as e:
        _json_out({"error": "db_error", "message": str(e)})
        return 1

    # 最近的 limit 条 (按时间倒序)
    txs_sorted = sorted(txs, key=lambda t: t["created_at"], reverse=True)[:limit]
    history = [
        {
            "date": t["created_at"][:10],
            "time": t["created_at"][11:19],
            "type": t["type"],
            "amount": t["amount"],
            "description": t["description"],
        }
        for t in txs_sorted
    ]
    _json_out({
        "from": start.isoformat(),
        "to": end.isoformat(),
        "days": days,
        "tx_count": len(history),
        "history": history,
    })
    return 0


# ─── 原有入口 ────────────────────────────────────────────────────────────────

def main():
    # ⭐ dashboard 子命令先匹配 (避免被当成"单条消息"误处理)
    if len(sys.argv) > 1 and sys.argv[1] in ("balance", "today", "history"):
        sub = sys.argv[1]
        if sub == "balance":
            sys.exit(cmd_balance())
        elif sub == "today":
            sys.exit(cmd_today())
        elif sub == "history":
            # 手写简单 --days / --limit 解析 (避免动 argparse 兼容老入口)
            days = 7
            limit = 50
            args = sys.argv[2:]
            i = 0
            while i < len(args):
                if args[i] == "--days" and i + 1 < len(args):
                    try:
                        days = int(args[i + 1])
                    except ValueError:
                        _json_out({"error": "invalid_args", "message": "--days 必须是整数"})
                        sys.exit(2)
                    i += 2
                elif args[i] == "--limit" and i + 1 < len(args):
                    try:
                        limit = int(args[i + 1])
                    except ValueError:
                        _json_out({"error": "invalid_args", "message": "--limit 必须是整数"})
                        sys.exit(2)
                    i += 2
                else:
                    _json_out({"error": "invalid_args", "message": f"未知参数: {args[i]}"})
                    sys.exit(2)
            sys.exit(cmd_history(days=days, limit=limit))

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--daily":
            print(generate_daily_report(DB_PATH))
            return
        elif arg == "--monthly":
            print(generate_monthly_report(DB_PATH))
            return
        elif arg == "--replay":
            # 把 --replay 之后的所有参数透传给 replay.main
            sys.argv = [sys.argv[0]] + sys.argv[2:]
            from replay import main as replay_main
            replay_main()
            return
        else:
            # 单条消息模式
            msg = " ".join(sys.argv[1:])
            run_once(msg)
            return

    # 交互模式
    print("kids-points CLI")
    print("输入积分变动（如「口算加1分」），或 /daily /monthly /balance /quit")
    print()

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not line:
            continue

        if line == "/quit":
            break
        elif line == "/daily":
            print(generate_daily_report(DB_PATH))
        elif line == "/monthly":
            print(generate_monthly_report(DB_PATH))
        elif line == "/balance":
            conn = init_db(DB_PATH)
            b = get_current_balance(conn)
            conn.close()
            print(f"当前余额：{cents_to_display(b)}分")
        else:
            run_once(line)


def run_once(msg: str):
    conn = init_db(DB_PATH)
    result = process_message(conn, f"cli-{os.urandom(4).hex()}", msg)
    conn.commit()
    conn.close()
    print(result["reply"])


if __name__ == "__main__":
    main()
