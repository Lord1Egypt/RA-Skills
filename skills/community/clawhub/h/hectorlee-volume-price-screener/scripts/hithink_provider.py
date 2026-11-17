#!/usr/bin/env python3
"""
Hithink 本地库数据源（V3.7 修复增强）
=====================================
从 hithink-finance 本地 DuckDB（全市场前复权日K）读取 K 线，
作为腾讯 ifzq.gtimg.cn 的替代/优先数据源。

为什么需要：
- 腾讯 K 线公开接口（ifzq.gtimg.cn / web.ifzq.gtimg.cn）有腾讯云 WAF 反爬，
  高频抓取（全市场 5000+ 只）会触发 501 拦截，导致 K 线获取失败。
- hithink 本地库是官方同花顺数据（前复权），本地文件读取，无网络、无 WAF、无限流。

返回格式与 data_provider 兼容: [{date, open, close, high, low, volume}, ...]（升序）
"""
import os
import time
from collections import defaultdict
from typing import Dict, List, Optional

DB_PATH = os.path.expanduser(
    "~/Library/Application Support/hithink-finance/data/market.duckdb")

_cache: Optional[Dict[str, List[dict]]] = None
_cache_count = 0


def _code_to_ths(code: str) -> str:
    """sh600519 -> 600519.SH / sz000001 -> 000001.SZ / bj920169 -> 920169.BJ"""
    code = code.strip().lower()
    if "." in code:
        return code.upper()
    prefix = code[:2]
    num = code[2:]
    ex = {"sh": "SH", "sz": "SZ", "bj": "BJ"}.get(prefix)
    if ex is None:
        # 纯数字代码（920 是北交所新段，须先于 "9" 判断）
        if code.startswith("920"):
            return f"{code}.BJ"
        if code.startswith(("6", "9")):
            return f"{code}.SH"
        elif code.startswith(("4", "8")):
            return f"{code}.BJ"
        return f"{code}.SZ"
    return f"{num}.{ex}"


def available() -> bool:
    """本地库是否存在且可读"""
    return os.path.exists(DB_PATH)


def load_cache(count: int = 90, force: bool = False) -> Dict[str, List[dict]]:
    """一次性把全市场最近 count 个交易日的 K 线载入内存（约 50MB / 54万行）"""
    global _cache, _cache_count
    if _cache is not None and _cache_count >= count and not force:
        return _cache

    import duckdb
    t0 = time.time()
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        dates = [r[0] for r in con.execute(
            "SELECT DISTINCT date FROM v_daily_qfq ORDER BY date DESC LIMIT ?",
            [count]).fetchall()]
        if not dates:
            return {}
        start = dates[-1]
        rows = con.execute(
            "SELECT thscode, date, open, high, low, close, volume "
            "FROM v_daily_qfq WHERE date >= ?", [str(start)]).fetchall()
    finally:
        con.close()

    cache: Dict[str, List[dict]] = defaultdict(list)
    for ths, d, o, h, l, c, v in rows:
        cache[ths].append({
            "date": str(d),
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
            "volume": int(float(v)) if v is not None else 0,
        })
    for ths in cache:
        cache[ths].sort(key=lambda x: x["date"])

    _cache = dict(cache)
    _cache_count = count
    print(f"[Hithink] 本地库载入 {len(_cache)} 只 / {len(rows)} 行 K线，耗时 {time.time()-t0:.1f}s")
    return _cache


def get_hithink_kline(code: str, count: int = 90) -> Optional[List[dict]]:
    """单只 K 线（升序，前复权），兼容 data_provider 返回格式"""
    if not available():
        return None
    try:
        cache = load_cache(count)
    except Exception as e:
        print(f"[Hithink] 本地库读取失败: {e}")
        return None
    ths = _code_to_ths(code)
    klines = cache.get(ths)
    if not klines:
        return None
    return klines[-count:]


def fetch_hithink_klines_batch(codes: List[str], count: int = 90
                               ) -> Dict[str, Optional[List[dict]]]:
    """批量读取（内存缓存，全市场一次载入后按需取）"""
    if not available():
        return {}
    try:
        cache = load_cache(count)
    except Exception as e:
        print(f"[Hithink] 本地库批量读取失败: {e}")
        return {}
    results: Dict[str, Optional[List[dict]]] = {}
    for code in codes:
        ths = _code_to_ths(code)
        klines = cache.get(ths)
        results[code] = (klines[-count:] if klines else None)
    return results


def _ths_to_code(thscode: str) -> str:
    """600519.SH -> sh600519 / 000001.SZ -> sz000001 / 920169.BJ -> bj920169"""
    if "." in thscode:
        num, ex = thscode.split(".")
        prefix = {"SH": "sh", "SZ": "sz", "BJ": "bj"}.get(ex.upper(), "sh")
        return f"{prefix}{num}"
    return thscode.lower()


def get_all_hithink_stocks() -> List[dict]:
    """从本地库取全市场真实股票代码列表（含主板/创业板/科创板/北交所）

    返回: [{code: 'sh600519', pure_code: '600519', name: ''}, ...]
    name 为空，由调用方用腾讯行情补齐。
    """
    if not available():
        return []
    try:
        import duckdb
        con = duckdb.connect(DB_PATH, read_only=True)
        try:
            rows = con.execute(
                "SELECT DISTINCT thscode FROM v_daily_qfq").fetchall()
        finally:
            con.close()
    except Exception as e:
        print(f"[Hithink] 股票列表读取失败: {e}")
        return []

    stocks = []
    for (ths,) in rows:
        code = _ths_to_code(ths)
        pure = code[2:]
        stocks.append({"code": code, "pure_code": pure, "name": ""})
    return stocks


def get_hithink_weekly(code: str, want_num: int = 30) -> Optional[List[dict]]:
    """从本地库日线聚合周线（ISO 周），替代 TDX 周线。

    周线 OHLCV 聚合规则：open=周首日开盘、close=周末日收盘、
    high/low=周内极值、volume=周内累加。返回 data_provider 兼容格式（升序）。
    """
    if not available():
        return None
    import duckdb
    ths = _code_to_ths(code)
    con = duckdb.connect(DB_PATH, read_only=True)
    try:
        rows = con.execute(
            "SELECT date, open, high, low, close, volume FROM v_daily_qfq "
            "WHERE thscode=? ORDER BY date DESC LIMIT ?",
            [ths, want_num * 6 + 10]).fetchall()
    except Exception as e:
        print(f"[Hithink] 周线聚合失败 {code}: {e}")
        con.close()
        return None
    finally:
        if con is not None:
            try:
                con.close()
            except Exception:
                pass
    if not rows:
        return None
    rows.reverse()  # 升序

    weekly: List[dict] = []
    cur_week = None
    cur = None
    for r in rows:
        d = r[0]
        iso = d.isocalendar()[:2]
        if iso != cur_week:
            if cur is not None:
                weekly.append(cur)
            cur_week = iso
            cur = {"date": str(d), "open": float(r[1]), "high": float(r[2]),
                   "low": float(r[3]), "close": float(r[4]), "volume": int(float(r[5]))}
        else:
            cur["high"] = max(cur["high"], float(r[2]))
            cur["low"] = min(cur["low"], float(r[3]))
            cur["close"] = float(r[4])
            cur["volume"] += int(float(r[5]))
            cur["date"] = str(d)
    if cur is not None:
        weekly.append(cur)
    return weekly[-want_num:]


if __name__ == "__main__":
    print("=== Hithink 本地库自检 ===")
    if not available():
        print("本地库不存在，请先运行 hithink-finance data sync")
    else:
        t0 = time.time()
        kl = get_hithink_kline("sh688981", 5)
        print(f"中芯国际(688981) 前复权K线 {len(kl) if kl else 0} 根，耗时 {time.time()-t0:.1f}s")
        if kl:
            for k in kl:
                print(f"  {k['date']} close={k['close']} vol={k['volume']}")
        # 批量测试
        t0 = time.time()
        res = fetch_hithink_klines_batch(["sh600519", "sz000001", "sh688981"], 90)
        ok = sum(1 for v in res.values() if v)
        print(f"批量 3 只：成功 {ok}/3，耗时 {time.time()-t0:.1f}s")
