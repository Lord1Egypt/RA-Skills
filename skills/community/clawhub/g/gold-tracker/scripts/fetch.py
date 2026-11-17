#!/usr/bin/env python3
"""数据抓取 + 校验 + 缓存 + 状态更新（配置驱动，零第三方依赖）。

数据源、解析方式、校验范围全部来自 config.yaml；代码零硬编码。
失败时按「缓存 → 上次状态」降级，并在输出中披露「数据可能过期」（数据降级约束）。
每次运行追加一个采样点到价格序列，供趋势/波动率/EMA 计算。
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request

from common import paths, config, atomic, history, heartbeat, timeutil

OZ_TO_GRAM = 31.1034768

# 数据源名 → state.json 中的存量字段（降级取值用；gold 的金价在 state 里叫 current_price）
_STATE_FIELD = {"gold": "current_price", "fx": "usd_cny"}


def _cache_file(name, cfg):
    return paths.resolve(config.dig(cfg, "cache.dir", "cache")) / f"{name}.json"


def load_cache(name, cfg):
    ttl = config.dig(cfg, "cache.ttl_seconds", 300)
    f = _cache_file(name, cfg)
    if not f.exists():
        return {}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        if time.time() - data.get("_t", 0) < ttl:
            return data
    except Exception:
        pass
    return {}


def save_cache(name, cfg, data):
    f = _cache_file(name, cfg)
    data = dict(data)
    data["_t"] = time.time()
    atomic.atomic_write_json(f, data)


def fetch_url(url, timeout):
    # 用浏览器 UA：部分免费源会拒绝默认 UA（HTTP 403）
    req = urllib.request.Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0 Safari/537.36"),
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _parse_json_path(data, path):
    node = data
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return None
    return node


def parse_value(text, src_cfg):
    """根据 parser 配置从原始文本提取数值。失败返回 None。"""
    parser = src_cfg.get("parser", "regex")
    if parser == "json_path":
        try:
            data = json.loads(text)
        except Exception:
            return None
        v = _parse_json_path(data, src_cfg.get("json_path", ""))
        if v is None:
            return None
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    # 默认 regex
    pattern = src_cfg.get("pattern", "")
    if not pattern:
        return None
    m = re.search(pattern, text, re.IGNORECASE)
    if not m:
        return None
    raw = m.group(1) if m.lastindex else m.group(0)
    try:
        return float(str(raw).replace(",", ""))
    except ValueError:
        return None


def fetch_source(name, src_cfg, cfg, last_state):
    """抓取单个数据源，返回 (value, source_desc, stale, error)。"""
    timeout = int(src_cfg.get("timeout", 15))
    lo = float(src_cfg.get("min", 0))
    hi = float(src_cfg.get("max", float("inf")))

    # 1) 缓存
    cache = load_cache(name, cfg)
    if cache.get("value") is not None:
        return cache["value"], "cache", False, None

    # 2) 实时抓取
    url = src_cfg.get("url", "")
    if not url:
        # 无配置 URL：降级到上次状态
        prev = last_state.get(_STATE_FIELD.get(name))
        if prev:
            return float(prev), "state", True, "数据源 URL 未配置，使用上次状态"
        return None, None, True, "数据源 URL 未配置且无历史状态"

    try:
        text = fetch_url(url, timeout)
        value = parse_value(text, src_cfg)
        if value is None:
            return None, url, True, "解析失败"
        if not (lo <= value <= hi):
            return None, url, True, "数值超出范围 [{}, {}]: {}".format(lo, hi, value)
        save_cache(name, cfg, {"value": value})
        return value, url, False, None
    except Exception as e:  # noqa: BLE001
        prev = last_state.get(_STATE_FIELD.get(name))
        if prev:
            return float(prev), "state", True, "抓取失败({}), 使用上次状态".format(e)
        return None, None, True, "抓取失败: {}".format(e)


def fetch_all():
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")
    last_state = load_state()
    result = {
        "timestamp": timeutil.now_iso(tz),
        "price_usd": None,
        "usd_cny": None,
        "price_cny_per_gram": None,
        "sources": {},
        "errors": [],
        "stale": False,
    }

    field_map = {"gold": "price_usd", "fx": "usd_cny"}
    for name, src_cfg in (cfg.get("data_sources") or {}).items():
        if not isinstance(src_cfg, dict):
            continue
        value, source_desc, stale, error = fetch_source(name, src_cfg, cfg, last_state)
        field = src_cfg.get("field", field_map.get(name, name))
        if value is not None:
            result[field] = value
            result["sources"][name] = source_desc
            if stale:
                result["stale"] = True
                result["errors"].append("[{}] {}".format(name, error))
        else:
            result["errors"].append("[{}] {}".format(name, error))

    if result["price_usd"] and result["usd_cny"]:
        result["price_cny_per_gram"] = round(
            result["price_usd"] * result["usd_cny"] / OZ_TO_GRAM, 2
        )

    return result, cfg, tz


def load_state():
    f = paths.resolve("state.json")
    if not f.exists():
        return {}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def update_state(data, cfg, tz):
    state = load_state()
    last_price = state.get("current_price")
    current = data["price_usd"]

    max_points = config.dig(cfg, "cache.price_series_max_points", 2000)
    series = history.append_point(current, data["timestamp"], max_points) if current else history.load_series()

    # 昨日收盘：取今天之前最近一天的收盘价
    closes = history.daily_closes(series)
    prev_close = None
    today = timeutil.today_str(tz)
    prior = [c for c in closes if c["date"] < today]
    if prior:
        prev_close = prior[-1]["price"]

    state.update({
        "date": today,
        "last_update": data["timestamp"],
        "current_price": current,
        "price_cny_per_gram": data["price_cny_per_gram"],
        "usd_cny": data["usd_cny"],
        "sources": data["sources"],
        "prev_close": prev_close,
        "data_stale": bool(data["stale"]),
        "fetch_status": "degraded" if data["stale"] else ("error" if current is None else "ok"),
    })

    if last_price and current:
        change = current - last_price
        state["last_price"] = last_price
        state["change_pct"] = round((change / last_price) * 100, 2)
        state["change_abs"] = round(change, 2)
    elif current:
        state["last_price"] = current
        state["change_pct"] = 0.0
        state["change_abs"] = 0.0

    atomic.atomic_write_json(paths.resolve("state.json"), state)
    return state


def main():
    paths.ensure_env()
    data, cfg, tz = fetch_all()

    if data["price_usd"] is not None:
        update_state(data, cfg, tz)

    heartbeat.record("fetch")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if data["stale"]:
        print("[警告] 数据可能过期（部分来源已降级到缓存/上次状态）", file=sys.stderr)
    for e in data["errors"]:
        print("[警告] {}".format(e), file=sys.stderr)

    if data["price_usd"] is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
