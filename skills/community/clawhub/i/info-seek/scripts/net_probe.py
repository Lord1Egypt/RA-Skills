#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/net_probe.py — Infoseek 网络探测唯一真源（GA12 / v2.2.0）

收口此前两处重复实现（engine_router.probe_http / search_engine_health.probe_http），
并为「网络边界门控」（boundary_gate）提供 host 级可达性判定。

设计原则（见 references/P3-设计方案评估简报-GA11GA12.md §2）：
  - 不绕过网络边界（不做代理/VPN/反爬对抗）；
  - 不把受限能力伪装为可用（显式声明 + 留痕）；
  - 零第三方硬依赖（仅 urllib 标准库）；
  - 探测幂等 + 正/负项差异化 TTL 缓存（进程内 + 磁盘），避免重复探测拖垮调研链；
  - 正项支持 stale-while-revalidate（过 TTL 后陈旧值短暂沿用 + 后台异步重验），
    探测异常 fail-open（ok=None 放行），不把瞬态抖动误杀为端点不可达。

核心 API：
  probe_http(url, timeout=5.0, *, reject_status=True) -> (ok, elapsed, err)
      与历史两处 probe_http 同构（reject_status=True 时严格 200）。
  probe_host(host, timeout=5.0, *, force=False, ttl=None) -> dict
      host 级可达性：能拿到任一 HTTP 响应（含 3xx/4xx）即视为「网络可达」；
      仅 DNS 失败 / 连接拒绝 / 超时 才判不可达。
  check_hosts(hosts, timeout=5.0, *, force=False) -> {host: result}
      批量并发探测（线程池）。
  reset_cache() / 边界测试用
"""

from __future__ import annotations

import json
import os
import socket
import ssl
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_UA = "Mozilla/5.0 (compatible; infoseek-net-probe/2.0)"

# ── TTL（正/负项差异化，v2.1.0） ──────────────────────────
_DEFAULT_TTL = 600      # 正项（明确可达）缓存 TTL
_DEFAULT_NEG_TTL = 30   # 负项（明确不可达）短 TTL：瞬态故障快速恢复，不把抖动固化成长期不可达
# stale-while-revalidate：正项过 TTL 后仍可临时沿用陈旧值的额外窗口（仅正项）
_DEFAULT_STALE_TTL = 3600


def _env_int(name: str, default: int) -> int:
    v = os.environ.get(name, "")
    if v:
        try:
            return max(0, int(v))
        except ValueError:
            pass
    return default


def _probe_ttl() -> int:
    """正项（可达）缓存 TTL：env INFOSEEK_NET_PROBE_TTL > 默认 600s。"""
    return _env_int("INFOSEEK_NET_PROBE_TTL", _DEFAULT_TTL)


def _probe_neg_ttl() -> int:
    """负项（明确不可达）缓存 TTL：env INFOSEEK_NET_PROBE_NEG_TTL > 默认 30s。

    负项多为超时 / 拒绝等瞬态故障，TTL 必须远短于正项，避免临时网络抖动
    被缓存成「长期不可达」而在 netguard 中误杀端点。
    """
    return _env_int("INFOSEEK_NET_PROBE_NEG_TTL", _DEFAULT_NEG_TTL)


def _stale_ttl() -> int:
    """正项 SWR 陈旧窗口：env INFOSEEK_NET_PROBE_STALE_TTL > 默认 3600s。

    仅对正项（明确可达）生效：正项过 TTL 后，在 TTL+stale 窗口内仍立即沿用
    陈旧结果并后台异步重验（stale-while-revalidate），避免探测抖动 / 超时
    阻塞主链。负项不做 SWR——陈旧的「不可达」若被沿用会误杀端点。
    设为 0 即关闭 SWR（恢复过期即同步重探语义）。
    """
    return max(0, _env_int("INFOSEEK_NET_PROBE_STALE_TTL", _DEFAULT_STALE_TTL))


def _stale_fresh(entry: dict, now: float) -> bool:
    """正项陈旧条目是否仍处于 SWR 可用窗口内。"""
    if entry.get("ok") is not True:
        return False
    age = now - entry.get("ts", 0)
    return _probe_ttl() < age <= _probe_ttl() + _stale_ttl()


def _entry_ttl(entry: dict, override: Optional[int] = None) -> int:
    """按缓存条目的判定结果选择 TTL：

    - 可达（ok is True）→ 正项 TTL（600s）；
    - 不可达（ok is False）/ 未知（ok is None）→ 负项短 TTL（30s）；
    - override 为调用方显式传入的 TTL（probe_host(ttl=...)），优先采用。
    """
    if override is not None:
        return max(0, override)
    return _probe_ttl() if entry.get("ok") is True else _probe_neg_ttl()


# ── 磁盘缓存目录（复用 state_dir，失败则退到 ~/.infoseek） ─
def _data_dir() -> Path:
    try:
        from core.state_dir import get_data_dir  # type: ignore
    except Exception:
        try:
            from state_dir import get_data_dir  # type: ignore
        except Exception:
            return Path(os.path.expanduser("~/.infoseek"))
    try:
        return Path(get_data_dir())
    except Exception:
        return Path(os.path.expanduser("~/.infoseek"))


_CACHE_PATH = _data_dir() / "net_probe_cache.json"

# 进程内缓存：{host: {"ts": float, "ok": bool, "elapsed": float, "err": str}}
_MEM: Dict[str, dict] = {}


# ═══════════════════════════════════════════════════════════
# 基础探测
# ═══════════════════════════════════════════════════════════

def probe_http(url: str, timeout: float = 5.0, *,
               reject_status: bool = True) -> Tuple[bool, float, str]:
    """HTTP GET 连通探测，返回 (ok, elapsed_seconds, err)。

    reject_status=True（默认，保持历史语义）：仅 HTTP 200 判 ok；
    reject_status=False：拿到任意 HTTP 响应（含 3xx/4xx/5xx）即判 ok，
        用于 host 级可达性判定（握手成功 ⇒ 网络层可达）。
    """
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ok = (resp.status == 200) if reject_status else True
            return ok, round(time.time() - t0, 2), ""
    except urllib.error.HTTPError as e:
        # 已收到服务器响应：reject_status=False 时视为可达
        if not reject_status:
            return True, round(time.time() - t0, 2), ""
        return False, round(time.time() - t0, 2), f"HTTP {e.code}"
    except Exception as e:
        return False, round(time.time() - t0, 2), str(e)[:120]


def _normalize_host(host: str) -> str:
    """规整 host：去 scheme / 路径 / 端口外空白，小写。"""
    h = (host or "").strip().lower()
    for scheme in ("https://", "http://"):
        if h.startswith(scheme):
            h = h[len(scheme):]
    h = h.split("/", 1)[0].split("?", 1)[0]
    return h


def probe_host(host: str, timeout: float = 5.0, *,
               force: bool = False, ttl: Optional[int] = None) -> dict:
    """探测单个 host 的网络可达性（带 TTL 缓存）。

    返回 {"host", "ok", "elapsed", "err", "ts", "cached"}。
    """
    h = _normalize_host(host)
    if not h:
        return {"host": h, "ok": False, "elapsed": 0.0, "err": "empty host",
                "ts": time.time(), "cached": False}

    ttl_override = ttl
    now = time.time()

    if not force:
        cached = _MEM.get(h)
        if cached is None:
            disk = _load_disk().get(h)
            if disk:
                _MEM[h] = disk
                cached = disk
        if cached is not None:
            age = now - cached.get("ts", 0)
            if age <= _entry_ttl(cached, ttl_override):
                return dict(cached, cached=True)
            # stale-while-revalidate：仅正项。陈旧但仍在窗口内 → 立即沿用 + 后台重验
            if _stale_fresh(cached, now):
                _revalidate_async(h, timeout)
                return dict(cached, cached=True, stale=True)

    # 真实探测：先 https，握手拿到响应（含错误码）即可；https 失败且非超时/拒绝再退 http
    ok, elapsed, err = _reach(f"https://{h}/", timeout)
    if not ok and _may_retry_http(err):
        ok2, elapsed2, err2 = _reach(f"http://{h}/", min(timeout, 4.0))
        if ok2:
            ok, elapsed, err = True, elapsed2, ""
        else:
            err = err or err2

    res = {"host": h, "ok": bool(ok), "elapsed": float(elapsed),
           "err": err, "ts": now, "cached": False}
    _MEM[h] = res
    _save_disk(h, res)
    return dict(res)


_REVALIDATING: set = set()


def _revalidate_async(host: str, timeout: float) -> None:
    """后台守护线程重探（SWR）。同一 host 重验进行中则跳过，避免并发抖动。"""
    if host in _REVALIDATING:
        return
    _REVALIDATING.add(host)

    def _job() -> None:
        try:
            probe_host(host, timeout, force=True)
        except Exception:
            pass  # 后台重验失败保留陈旧值，下轮再试
        finally:
            _REVALIDATING.discard(host)

    import threading
    t = threading.Thread(target=_job, name=f"netprobe-swr-{host}", daemon=True)
    t.start()


def _reach(url: str, timeout: float) -> Tuple[bool, float, str]:
    """host 可达性：任意 HTTP 响应（含 3xx/4xx）⇒ 可达；仅网络层错误 ⇒ 不可达。"""
    return probe_http(url, timeout, reject_status=False)


def _may_retry_http(err: str) -> bool:
    """https 失败时是否值得退 http：SSL/协议错误可退；DNS/拒绝/超时不退（http 同样不通）。"""
    e = (err or "").lower()
    if not e:
        return False
    network_dead = ("timed out" in e or "timeout" in e or "refused" in e
                    or "name or service not known" in e or "getaddrinfo" in e
                    or "no route" in e or "unreachable" in e)
    return not network_dead


def check_hosts(hosts: List[str], timeout: float = 5.0, *,
                force: bool = False, workers: int = 8) -> Dict[str, dict]:
    """批量并发探测多个 host，返回 {host: result}。"""
    uniq = []
    for h in hosts:
        nh = _normalize_host(h)
        if nh and nh not in uniq:
            uniq.append(nh)
    if not uniq:
        return {}
    results: Dict[str, dict] = {}
    # 全部命中缓存时不起线程
    if not force:
        miss = []
        now = time.time()
        disk = _load_disk()
        for h in uniq:
            c = _MEM.get(h)
            if c is None and disk.get(h):
                c = disk[h]
                _MEM[h] = c
            if c is not None:
                age = now - c.get("ts", 0)
                if age <= _entry_ttl(c):
                    results[h] = dict(c, cached=True)
                elif _stale_fresh(c, now):
                    # SWR：立即沿用陈旧正项，后台重验
                    _revalidate_async(h, timeout)
                    results[h] = dict(c, cached=True, stale=True)
                else:
                    miss.append(h)
            else:
                miss.append(h)
    else:
        miss = uniq
    if miss:
        with ThreadPoolExecutor(max_workers=min(workers, max(1, len(miss)))) as ex:
            futs = {ex.submit(probe_host, h, timeout, force=True): h for h in miss}
            for fut in futs:
                h = futs[fut]
                try:
                    results[h] = fut.result()
                except Exception as e:  # 探测自身异常不炸调用方（fail-OPEN）
                    # 未知态：ok=None（非 False）。可达性未证实也未证伪，
                    # 调用方应「放行由实际抓取裁决」，而非据此屏蔽端点。
                    results[h] = {"host": h, "ok": None, "elapsed": 0.0,
                                  "err": f"probe_error:{type(e).__name__}",
                                  "ts": time.time(), "cached": False}
    return results


# ═══════════════════════════════════════════════════════════
# 磁盘缓存（崩溃 / 跨进程复用）
# ═══════════════════════════════════════════════════════════

def _load_disk() -> Dict[str, dict]:
    try:
        if _CACHE_PATH.exists():
            data = json.loads(_CACHE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _save_disk(host: str, res: dict) -> None:
    try:
        data = _load_disk()
        data[host] = res
        # 控制缓存体积：仅保留最近 200 条
        if len(data) > 200:
            keep = sorted(data.items(), key=lambda kv: kv[1].get("ts", 0))[-200:]
            data = dict(keep)
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = _CACHE_PATH.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        tmp.replace(_CACHE_PATH)
    except Exception:
        pass  # 缓存写失败不影响判定


def reset_cache() -> None:
    """清空进程内缓存（测试隔离用；不清磁盘）。"""
    _MEM.clear()


def clear_disk_cache() -> None:
    """删除磁盘缓存（测试 / 强制刷新用）。"""
    _MEM.clear()
    try:
        if _CACHE_PATH.exists():
            _CACHE_PATH.unlink()
    except Exception:
        pass


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="infoseek host 网络可达性探测（GA12）")
    ap.add_argument("hosts", nargs="*", help="待探测 host（可多个）")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--force", action="store_true", help="忽略缓存强制探测")
    args = ap.parse_args()
    targets = args.hosts or ["www.wikidata.org", "cn.bing.com", "api.github.com"]
    out = check_hosts(targets, timeout=args.timeout, force=args.force)
    print(json.dumps(out, ensure_ascii=False, indent=2))
