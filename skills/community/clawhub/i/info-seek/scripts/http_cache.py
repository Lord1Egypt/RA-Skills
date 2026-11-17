#!/usr/bin/env python3
"""http_cache.py — 全网络 HTTP 抓取缓存（缺口①, 2026-09-10）

搜索/抓取层此前全网络无缓存（每次抓取都重复下载），本模块提供
LRU + TTL + 容量上限 的磁盘缓存，命中即免网络。

存储：~/.infoseek/http_cache/<sha256(url)>.json（env INFOSEEK_DATA_DIR 可改）
行为：
  - get_http_cache(url, ttl=None) -> dict|None：命中且未过期返回
    {"content","title"}；命中时 touch mtime（LRU 最近使用）；过期自动删除。
  - put_http_cache(url, title, content) -> str|None：原子写（tmp+rename），
    写后按容量上限做 LRU 淘汰（mtime 最旧优先删）。
  - cleanup_http_cache() -> dict：TTL 过期清理 + 容量超限 LRU 淘汰，返回统计。
  - get_http_cache_stats() -> dict：{files, bytes, oldest_ts, newest_ts}

配置（全部 env 可覆盖，默认即用）：
  INFOSEEK_HTTP_CACHE_DIR   缓存目录（默认 ~/.infoseek/http_cache）
  INFOSEEK_HTTP_CACHE_TTL   缓存 TTL 秒（默认 600；0 = 永久不过期）
  INFOSEEK_HTTP_CACHE_MAX_MB 容量上限 MB（默认 200；0 = 不限）

失败语义：所有 IO 异常吞掉返回 None/不抛——缓存只是加速层，绝不阻塞主流程。
"""
import hashlib
import json
import os
import time
from pathlib import Path

_DEFAULT_DIR = Path(os.environ.get('INFOSEEK_DATA_DIR', str(Path.home() / '.infoseek'))) / 'http_cache'
_CACHE_DIR = Path(os.environ.get('INFOSEEK_HTTP_CACHE_DIR', str(_DEFAULT_DIR)))


def _ttl() -> float:
    try:
        return max(0.0, float(os.environ.get('INFOSEEK_HTTP_CACHE_TTL', '600')))
    except ValueError:
        return 600.0


def _max_bytes() -> int:
    try:
        mb = float(os.environ.get('INFOSEEK_HTTP_CACHE_MAX_MB', '200'))
        return int(max(0, mb) * 1024 * 1024)
    except ValueError:
        return 200 * 1024 * 1024


def _path_for(url: str) -> Path:
    key = hashlib.sha256(url.encode('utf-8')).hexdigest()
    return _CACHE_DIR / f"{key}.json"


def _safe_read(p: Path) -> dict | None:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _safe_write(p: Path, data: dict) -> bool:
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix('.json.tmp')
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, p)  # 原子写
        return True
    except Exception:
        return False


def get_http_cache(url: str, ttl: float | None = None) -> dict | None:
    """命中返回 {"content","title"}（并 touch mtime 维持 LRU），未命中/过期返回 None。"""
    if not url or url.startswith('file://'):
        return None
    if ttl is None:
        ttl = _ttl()
    p = _path_for(url)
    if not p.exists():
        return None
    try:
        age = time.time() - p.stat().st_mtime
    except OSError:
        return None
    if 0 < ttl < age:
        try:
            p.unlink()
        except OSError:
            pass
        return None
    data = _safe_read(p)
    if not data or 'content' not in data:
        return None
    try:
        os.utime(p, None)  # touch：最近使用
    except OSError:
        pass
    return {"content": data.get('content', ''), "title": data.get('title', ''), "raw": data.get('raw')}


def put_http_cache(url: str, title: str, content: str, raw: str = "") -> str | None:
    """写缓存并触发容量 LRU 淘汰，返回缓存文件路径（失败返回 None）。raw=原始HTML（follow_links/v2/v3 链路复用）。"""
    if not url or url.startswith('file://') or not content:
        return None
    p = _path_for(url)
    if not _safe_write(p, {"url": url[:512], "title": title or '', "content": content, "raw": raw or '', "ts": time.time()}):
        return None
    cleanup_http_cache(only_capacity=True)  # 只在写入后做容量收敛，不阻塞
    return str(p)


def cleanup_http_cache(only_capacity: bool = False) -> dict:
    """TTL 过期清理 + 容量超限 LRU 淘汰（mtime 最旧优先）。"""
    if not _CACHE_DIR.exists():
        return {"deleted": 0, "bytes": 0, "reason": "no_dir"}
    ttl = _ttl()
    max_bytes = _max_bytes()
    now = time.time()
    deleted = 0
    files = []
    total = 0
    try:
        for p in _CACHE_DIR.glob('*.json'):
            try:
                st = p.stat()
                age = now - st.st_mtime
            except OSError:
                continue
            if not only_capacity and 0 < ttl < age:
                try:
                    p.unlink()
                except OSError:
                    pass
                deleted += 1
                continue
            files.append((st.st_mtime, st.st_size, p))
            total += st.st_size
        # 容量超限：按 mtime 升序删到容量内
        if max_bytes > 0 and total > max_bytes:
            files.sort(key=lambda x: x[0])
            for _mtime, _size, p in files:
                if total <= max_bytes:
                    break
                try:
                    sz = p.stat().st_size
                    p.unlink()
                    total -= sz
                    deleted += 1
                except OSError:
                    continue
    except OSError:
        pass
    return {"deleted": deleted, "bytes": total}


def get_http_cache_stats() -> dict:
    """缓存统计（调试/审计用）。"""
    if not _CACHE_DIR.exists():
        return {"files": 0, "bytes": 0, "dir": str(_CACHE_DIR)}
    files, total, oldest, newest = 0, 0, None, None
    try:
        for p in _CACHE_DIR.glob('*.json'):
            try:
                st = p.stat()
            except OSError:
                continue
            files += 1
            total += st.st_size
            oldest = st.st_mtime if oldest is None else min(oldest, st.st_mtime)
            newest = st.st_mtime if newest is None else max(newest, st.st_mtime)
    except OSError:
        pass
    return {
        "files": files, "bytes": total,
        "oldest_ts": oldest, "newest_ts": newest,
        "dir": str(_CACHE_DIR),
    }


if __name__ == '__main__':
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if cmd == 'stats':
        print(json.dumps(get_http_cache_stats(), ensure_ascii=False))
    elif cmd == 'clean':
        print(json.dumps(cleanup_http_cache(), ensure_ascii=False))
    else:
        print("usage: http_cache.py [stats|clean]")