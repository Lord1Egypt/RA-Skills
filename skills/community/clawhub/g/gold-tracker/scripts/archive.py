#!/usr/bin/env python3
"""日志归档、索引、保留策略、重建修复、日志标准化。

对照 P1-10：归档/日志/状态文件写操作原子化（临时文件 + rename）；提供索引重建修复。

用法:
    python3 scripts/archive.py archive           # 归档非当日日志
    python3 scripts/archive.py find <YYYY-MM-DD> # 查询某日历史
    python3 scripts/archive.py history [days]    # 价格历史
    python3 scripts/archive.py cleanup [days]    # 清理过期归档
    python3 scripts/archive.py rebuild           # 重建索引（自愈）
    python3 scripts/archive.py summary           # 索引摘要
    python3 scripts/archive.py normalize         # 标准化日志时间戳/impact
"""

import json
import sys
from datetime import datetime, timedelta

from common import paths, config, atomic, heartbeat, timeutil, yamlmini


def logs_dir():
    return paths.resolve("logs")


def archive_dir():
    d = paths.resolve("archive")
    d.mkdir(parents=True, exist_ok=True)
    return d


def index_file():
    return archive_dir() / "index.json"


def load_index():
    f = index_file()
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return {"runs": [], "months": {}}


def save_index(index):
    for m in index.get("months", {}).values():
        if isinstance(m.get("dates"), set):
            m["dates"] = sorted(list(m["dates"]))
    atomic.atomic_write_json(index_file(), index)


def extract_runs(text):
    """从多文档 YAML 提取 run 元数据。返回 [{run_id, timestamp, price_usd, content}]。"""
    runs = []
    for doc in yamlmini.load_all(text):
        if not isinstance(doc, dict):
            continue
        run_id = doc.get("run_id", "")
        timestamp = doc.get("timestamp", "")
        price_usd = None
        pd = doc.get("price_data")
        if isinstance(pd, dict) and isinstance(pd.get("gold"), dict):
            price_usd = pd["gold"].get("price_usd")
        if price_usd is None:
            price_usd = doc.get("price_usd")
        if run_id or timestamp:
            runs.append({
                "run_id": str(run_id or ""),
                "timestamp": str(timestamp or ""),
                "price_usd": float(price_usd) if price_usd is not None else None,
                "content": _serialize_doc(doc),
            })
    return runs


def _serialize_doc(doc):
    # 用紧凑但可读的 YAML 重新序列化单文档（保持字段结构，不依赖原始缩进）。
    return _dump(doc)


def _dump(obj, indent=0):
    pad = "  " * indent
    if isinstance(obj, dict):
        parts = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                parts.append("{}{}:".format(pad, k))
                parts.append(_dump(v, indent + 1))
            else:
                parts.append("{}{}: {}".format(pad, k, _scalar(v)))
        return "\n".join(parts)
    if isinstance(obj, list):
        parts = []
        for item in obj:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    if isinstance(v, (dict, list)):
                        parts.append("{}- {}:".format(pad, k))
                        parts.append(_dump(v, indent + 2))
                    else:
                        parts.append("{}- {}: {}".format(pad, k, _scalar(v)))
                    first = False
            elif isinstance(item, list):
                parts.append("{}-".format(pad))
                parts.append(_dump(item, indent + 1))
            else:
                parts.append("{}- {}".format(pad, _scalar(item)))
        return "\n".join(parts)
    return "{}{}".format(pad, _scalar(obj))


def _scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return json.dumps(str(v), ensure_ascii=False)


def get_month_dir(date_str):
    m = archive_dir() / date_str[:7]
    m.mkdir(parents=True, exist_ok=True)
    return m


def archive_filename(run_id, timestamp, tz):
    try:
        dt = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        dt = dt.astimezone(timeutil.get_tz(tz))
        return "{}-{}.yaml".format(dt.strftime("%Y-%m-%d"), dt.strftime("%H%M"))
    except Exception:
        return "{}.yaml".format(run_id or "unknown")


def archive_log_file(log_path, tz):
    if not log_path.exists():
        return 0
    text = log_path.read_text(encoding="utf-8")
    runs = extract_runs(text)
    if not runs:
        return 0
    index = load_index()
    archived = 0
    for run in runs:
        timestamp = run["timestamp"]
        if not timestamp:
            continue
        month_dir = get_month_dir(timestamp)
        filename = archive_filename(run["run_id"], timestamp, tz)
        target = month_dir / filename
        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if run["content"] in existing:
                continue
        atomic.atomic_write_text(target, run["content"] + "\n")
        if run["run_id"] and run["run_id"] not in index["runs"]:
            index["runs"].append(run["run_id"])
        ym = timestamp[:7]
        if ym not in index["months"]:
            index["months"][ym] = {"count": 0, "dates": []}
        index["months"][ym]["count"] += 1
        if timestamp[:10] not in index["months"][ym]["dates"]:
            index["months"][ym]["dates"].append(timestamp[:10])
        archived += 1
    if archived:
        save_index(index)
    return archived


def archive_all():
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")
    total = 0
    today = timeutil.today_str(tz)
    d = logs_dir()
    if not d.exists():
        return 0
    for f in sorted(d.iterdir()):
        if f.suffix not in (".yaml", ".yml"):
            continue
        if today in f.name:
            continue
        n = archive_log_file(f, tz)
        if n:
            f.unlink()
            print("[已归档] {} → {} 条".format(f.name, n))
            total += n
    heartbeat.record("archive")
    return total


def find_by_date(date_str):
    month_dir = get_month_dir(date_str)
    results = []
    if not month_dir.exists():
        return results
    for f in sorted(month_dir.iterdir()):
        if f.suffix not in (".yaml", ".yml"):
            continue
        if not f.stem.startswith(date_str):
            continue
        for run in extract_runs(f.read_text(encoding="utf-8")):
            results.append({"file": f.name, **run})
    return sorted(results, key=lambda x: x.get("timestamp", ""))


def history(days):
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")
    out = []
    now = timeutil.now(tz)
    for i in range(days):
        date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        logs = find_by_date(date)
        prices = [l["price_usd"] for l in logs if l["price_usd"]]
        if prices:
            out.append({
                "date": date,
                "price_usd": round(sum(prices) / len(prices), 2),
                "count": len(prices),
                "high": max(prices),
                "low": min(prices),
            })
    return sorted(out, key=lambda x: x["date"])


def cleanup(retention_days):
    import datetime as _dt
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")
    now = timeutil.now(tz)
    removed_files = removed_dirs = 0
    for month_dir in sorted(archive_dir().iterdir()):
        if not month_dir.is_dir() or month_dir.name.startswith("."):
            continue
        try:
            month_dt = _dt.datetime.strptime(month_dir.name + "-01", "%Y-%m-%d").replace(tzinfo=now.tzinfo)
            if (now - month_dt).days > retention_days:
                for f in month_dir.iterdir():
                    if f.is_file():
                        f.unlink()
                        removed_files += 1
                month_dir.rmdir()
                removed_dirs += 1
        except Exception:
            pass
    index = load_index()
    for ym in list(index.get("months", {}).keys()):
        try:
            month_dt = _dt.datetime.strptime(ym + "-01", "%Y-%m-%d").replace(tzinfo=now.tzinfo)
            if (now - month_dt).days > retention_days:
                index["months"].pop(ym, None)
        except Exception:
            pass
    save_index(index)
    heartbeat.record("archive_cleanup")
    return removed_files, removed_dirs


def rebuild_index():
    index = {"runs": [], "months": {}}
    for month_dir in sorted(archive_dir().iterdir()):
        if not month_dir.is_dir() or month_dir.name.startswith("."):
            continue
        ym = month_dir.name
        if ym not in index["months"]:
            index["months"][ym] = {"count": 0, "dates": []}
        for f in month_dir.iterdir():
            if f.suffix not in (".yaml", ".yml"):
                continue
            for run in extract_runs(f.read_text(encoding="utf-8")):
                if run["run_id"] and run["run_id"] not in index["runs"]:
                    index["runs"].append(run["run_id"])
                if run["timestamp"]:
                    if run["timestamp"][:10] not in index["months"][ym]["dates"]:
                        index["months"][ym]["dates"].append(run["timestamp"][:10])
                index["months"][ym]["count"] += 1
    save_index(index)
    heartbeat.record("archive_rebuild")
    return len(index["runs"]), len(index["months"])


def show_summary():
    index = load_index()
    print("## 归档索引摘要")
    print("- 总记录数: {}".format(len(index.get("runs", []))))
    print("- 覆盖月份: {}".format(len(index.get("months", {}))))
    for month in sorted(index.get("months", {}).keys()):
        info = index["months"][month]
        print("- {}: {} 条 ({} 天)".format(month, info.get("count", 0), len(info.get("dates", []))))


# ---- normalize（从旧 normalize.py 折叠） ----
IMPACT_MAP = {
    # 旧英文枚举 → 新中文
    "bullish": "利多", "bearish": "利空", "neutral": "中性", "mixed": "多空交织",
    "slightly_bullish": "偏多", "slightly_bearish": "偏空",
    # 中文变体 → 新中文
    "看涨": "利多", "看跌": "利空", "利多": "利多", "利空": "利空",
    "中性": "中性", "双向": "多空交织", "多空交织": "多空交织",
    "中性偏多": "偏多", "中性偏空": "偏空", "偏多": "偏多", "偏空": "偏空",
}
ALLOWED = {"利多", "利空", "偏多", "偏空", "中性", "多空交织"}


def _norm_ts(ts):
    ts = ts.strip().strip('"')
    if not ts or "+08:00" in ts:
        return ts
    try:
        if ts.endswith("Z"):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return dt.astimezone(timeutil.get_tz()).isoformat()
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timeutil.get_tz())
        return dt.astimezone(timeutil.get_tz()).isoformat()
    except Exception:
        return ts


def _norm_impact(imp):
    imp = imp.strip().strip('"')
    if imp in IMPACT_MAP:
        return IMPACT_MAP[imp]
    if imp in ALLOWED:
        return imp
    return "neutral"


def _normalize_text(text):
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        indent = line[: len(line) - len(stripped)]
        if stripped.startswith("timestamp:"):
            _, _, val = stripped.partition(":")
            line = '{}timestamp: "{}"'.format(indent, _norm_ts(val))
        elif stripped.startswith("impact:"):
            _, _, val = stripped.partition(":")
            line = '{}impact: "{}"'.format(indent, _norm_impact(val))
        out.append(line)
    return "\n".join(out)


def _normalize_file(f):
    original = f.read_text(encoding="utf-8")
    normalized = _normalize_text(original)
    if normalized == original:
        return False
    atomic.atomic_write_text(f.with_suffix(f.suffix + ".bak"), original)
    atomic.atomic_write_text(f, normalized)
    return True


def _normalize_dir(d, count=0):
    if not d.exists():
        return count
    for f in sorted(d.iterdir()):
        if f.is_dir():
            count = _normalize_dir(f, count)
        elif f.suffix in (".yaml", ".yml") and not f.name.endswith(".bak"):
            if _normalize_file(f):
                print("[已修复] {}".format(f.relative_to(paths.ROOT)))
                count += 1
    return count


def main():
    paths.ensure_env()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    action = sys.argv[1]
    cfg = config.load()

    if action == "archive":
        print("[完成] 共归档 {} 条".format(archive_all()))
    elif action == "find":
        if len(sys.argv) < 3:
            print("用法: archive.py find <YYYY-MM-DD>")
            sys.exit(1)
        for log in find_by_date(sys.argv[2]):
            print("\n--- {} ---".format(log["file"]))
            print("Run ID: {}".format(log.get("run_id", "N/A")))
            print("时间: {}".format(log.get("timestamp", "N/A")))
            print("价格: ${}".format(log.get("price_usd", "N/A")))
    elif action == "history":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        h = history(days)
        if h:
            print("{:<12} {:>10} {:>6} {:>10} {:>10}".format("日期", "价格", "数量", "最高", "最低"))
            print("-" * 56)
            for x in h:
                print("{:<12} ${:>9.2f} {:>6} ${:>9.2f} ${:>9.2f}".format(
                    x["date"], x["price_usd"], x["count"], x["high"], x["low"]))
        else:
            print("无历史数据")
    elif action == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else int(cfg["archive"].get("retention_days", 365))
        files, dirs = cleanup(days)
        print("[完成] 清理 {} 个文件, {} 个目录".format(files, dirs))
    elif action == "rebuild":
        runs, months = rebuild_index()
        print("[完成] 重建索引: {} 条记录, {} 个月份".format(runs, months))
    elif action == "summary":
        show_summary()
    elif action == "normalize":
        total = 0
        for sub in ["logs", "archive"]:
            total = _normalize_dir(paths.resolve(sub), total)
        print("[完成] 标准化 {} 个文件".format(total))
    else:
        print("未知操作: {}".format(action))
        sys.exit(1)


if __name__ == "__main__":
    main()
