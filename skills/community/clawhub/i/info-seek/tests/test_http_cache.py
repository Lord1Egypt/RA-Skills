#!/usr/bin/env python3
"""test_http_cache.py — 全网络 HTTP 抓取缓存测试（缺口① · LRU + TTL + 容量上限）

覆盖：
  S1  基本写读（put→get 命中 / content·title·raw 透传 / 返回路径）
  S2  边界拒绝（空 url / 空 content / file:// / 未命中）
  S3  TTL（默认命中 / 过期删除 / ttl=0 永不过期 / 非法 env 兜底）
  S4  LRU touch（命中刷新 mtime）
  S5  原子写（无 .tmp 残留）
  S6  容量上限 LRU 淘汰（超限收敛 / mtime 最旧优先）
  S7  cleanup（only_capacity 语义）
  S8  stats（空目录 / 计数 / 字节 / oldest-newest）
  S9  容错（损坏 json / 目录不可用 → 返回 None 且绝不抛）
  S10 url 截断（≤512）
  S11 CLI（stats → exit 0）

设计约束：http_cache._CACHE_DIR 为模块级常量，测试以临时目录覆盖之，
写后即弃；不触碰真实 ~/.infoseek/http_cache。
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import http_cache as hc

_PASS = 0
_FAIL = 0
_TMP = None

_orig_ttl = hc._ttl
_orig_max_bytes = hc._max_bytes


def check(label: str, cond: bool) -> None:
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print(f'  ✅ {label}')
    else:
        _FAIL += 1
        print(f'  ❌ {label}')


def _fresh() -> Path:
    """重置：新临时缓存目录 + 清 env + 还原 env 读取钩子。"""
    global _TMP
    if _TMP and Path(_TMP).exists():
        shutil.rmtree(_TMP, ignore_errors=True)
    _TMP = tempfile.mkdtemp(prefix='hc_test_')
    hc._CACHE_DIR = Path(_TMP)
    for k in ('INFOSEEK_HTTP_CACHE_DIR', 'INFOSEEK_HTTP_CACHE_TTL',
              'INFOSEEK_HTTP_CACHE_MAX_MB'):
        os.environ.pop(k, None)
    hc._ttl = _orig_ttl
    hc._max_bytes = _orig_max_bytes
    return Path(_TMP)


# ---------------------------------------------------------------------------
# S1 基本写读
# ---------------------------------------------------------------------------

def test_s1_basic_roundtrip() -> None:
    _fresh()
    p = hc.put_http_cache('https://a.dev', 'TitleA', 'ContentA', raw='<html>A</html>')
    check('put 返回路径字符串', isinstance(p, str) and Path(p).exists())
    got = hc.get_http_cache('https://a.dev')
    check('get 命中返回 dict', isinstance(got, dict))
    check('content 一致', got['content'] == 'ContentA')
    check('title 一致', got['title'] == 'TitleA')
    check('raw 透传', got['raw'] == '<html>A</html>')


# ---------------------------------------------------------------------------
# S2 边界拒绝
# ---------------------------------------------------------------------------

def test_s2_reject_boundaries() -> None:
    _fresh()
    check('空 url → put None', hc.put_http_cache('', 'T', 'c') is None)
    check('空 content → put None', hc.put_http_cache('https://a.dev', 'T', '') is None)
    check('file:// → put None', hc.put_http_cache('file:///tmp/x', 'T', 'c') is None)
    check('空 url → get None', hc.get_http_cache('') is None)
    check('file:// → get None', hc.get_http_cache('file:///tmp/x') is None)
    check('未命中 → get None', hc.get_http_cache('https://nope.dev') is None)


# ---------------------------------------------------------------------------
# S3 TTL
# ---------------------------------------------------------------------------

def test_s3_ttl() -> None:
    _fresh()
    hc.put_http_cache('https://a.dev', 'A', 'c' * 20)
    check('默认 TTL 内命中', hc.get_http_cache('https://a.dev') is not None)

    p = hc.put_http_cache('https://old.dev', 'O', 'c' * 20)
    old = time.time() - 10000
    os.utime(p, (old, old))
    check('过期 → get None', hc.get_http_cache('https://old.dev', ttl=1) is None)
    check('过期文件已被删除', not Path(p).exists())

    p2 = hc.put_http_cache('https://keep.dev', 'K', 'c' * 20)
    os.utime(p2, (old, old))
    check('ttl=0 永不过期 → 命中', hc.get_http_cache('https://keep.dev', ttl=0) is not None)

    os.environ['INFOSEEK_HTTP_CACHE_TTL'] = 'abc'
    check('非法 TTL → 兜底 600', hc._ttl() == 600.0)
    os.environ['INFOSEEK_HTTP_CACHE_MAX_MB'] = 'xyz'
    check('非法 MAX_MB → 兜底 200MB', hc._max_bytes() == 200 * 1024 * 1024)
    os.environ['INFOSEEK_HTTP_CACHE_TTL'] = '0'
    check('TTL=0 env → 0.0', hc._ttl() == 0.0)


# ---------------------------------------------------------------------------
# S4 LRU touch
# ---------------------------------------------------------------------------

def test_s4_touch_on_hit() -> None:
    _fresh()
    p = hc.put_http_cache('https://x.dev', 'X', 'c' * 20)
    before = time.time() - 500
    os.utime(p, (before, before))
    hc.get_http_cache('https://x.dev')  # 命中 → touch
    check('命中刷新 mtime（LRU）', Path(p).stat().st_mtime > before)


# ---------------------------------------------------------------------------
# S5 原子写
# ---------------------------------------------------------------------------

def test_s5_atomic_no_tmp() -> None:
    _fresh()
    hc.put_http_cache('https://a.dev', 'A', 'c' * 50)
    hc.put_http_cache('https://b.dev', 'B', 'c' * 50)
    check('写后无 .tmp 残留', len(list(Path(_TMP).glob('*.tmp'))) == 0)
    check('两个 .json 落盘', len(list(Path(_TMP).glob('*.json'))) == 2)


# ---------------------------------------------------------------------------
# S6 容量上限 LRU 淘汰
# ---------------------------------------------------------------------------

def test_s6_capacity_lru() -> None:
    _fresh()
    hc.put_http_cache('https://a.dev', 'A', 'a' * 200)
    time.sleep(0.03)
    hc.put_http_cache('https://b.dev', 'B', 'b' * 200)
    time.sleep(0.03)
    hc.put_http_cache('https://c.dev', 'C', 'c' * 200)
    st = hc.get_http_cache_stats()
    check('3 文件就位', st['files'] == 3)
    total = st['bytes']
    hc._max_bytes = lambda: max(1, total // 2)
    r = hc.cleanup_http_cache(only_capacity=True)
    st2 = hc.get_http_cache_stats()
    check('超限删除计数 > 0', r['deleted'] >= 1)
    check('容量收敛（bytes ≤ 上限）', st2['bytes'] <= total // 2)

    # LRU 精确性：touch 最旧的 a → 应删 b（真正最旧），保留 a/c
    _fresh()
    hc.put_http_cache('https://old.dev', 'OLD', 'o' * 200)
    time.sleep(0.05)
    hc.put_http_cache('https://mid.dev', 'MID', 'm' * 200)
    time.sleep(0.05)
    hc.put_http_cache('https://new.dev', 'NEW', 'n' * 200)
    time.sleep(0.05)
    hc.get_http_cache('https://old.dev')  # touch → old 变最新
    tot = hc.get_http_cache_stats()['bytes']
    hc._max_bytes = lambda: tot - 1  # 仅容得下少一个
    hc.cleanup_http_cache(only_capacity=True)
    check('真正最旧(mid)被淘汰', hc.get_http_cache('https://mid.dev') is None)
    check('被 touch 的 old 保留', hc.get_http_cache('https://old.dev') is not None)
    check('new 保留', hc.get_http_cache('https://new.dev') is not None)


# ---------------------------------------------------------------------------
# S7 cleanup 语义
# ---------------------------------------------------------------------------

def test_s7_cleanup_semantics() -> None:
    _fresh()
    p = hc.put_http_cache('https://exp.dev', 'E', 'c' * 20)
    old = time.time() - 10000
    os.utime(p, (old, old))
    hc.cleanup_http_cache(only_capacity=True)
    check('only_capacity=True 不删过期文件', Path(p).exists())
    r = hc.cleanup_http_cache()
    check('全量 cleanup 删除过期', r['deleted'] == 1 and not Path(p).exists())

    _fresh()
    hc._CACHE_DIR = Path(_TMP) / 'nonexistent'
    r2 = hc.cleanup_http_cache()
    check('目录不存在 cleanup 返回 no_dir', r2.get('reason') == 'no_dir')


# ---------------------------------------------------------------------------
# S8 stats
# ---------------------------------------------------------------------------

def test_s8_stats() -> None:
    _fresh()
    st = hc.get_http_cache_stats()
    check('空目录 files=0', st['files'] == 0)
    hc.put_http_cache('https://a.dev', 'A', 'a' * 50)
    time.sleep(0.02)
    hc.put_http_cache('https://b.dev', 'B', 'b' * 50)
    st2 = hc.get_http_cache_stats()
    check('files 计数=2', st2['files'] == 2)
    check('bytes > 0', st2['bytes'] > 0)
    check('oldest/newest 非空且 newest ≥ oldest',
          st2['oldest_ts'] is not None and st2['newest_ts'] >= st2['oldest_ts'])


# ---------------------------------------------------------------------------
# S9 容错（异常吞没，绝不抛）
# ---------------------------------------------------------------------------

def test_s9_fault_tolerant() -> None:
    _fresh()
    bad = hc._path_for('https://bad.dev')
    Path(_TMP).mkdir(parents=True, exist_ok=True)
    bad.write_text('{not-json', encoding='utf-8')
    check('损坏 json → get None', hc.get_http_cache('https://bad.dev') is None)

    blk = Path(_TMP) / 'blocked'
    blk.write_text('x', encoding='utf-8')
    hc._CACHE_DIR = blk  # 目录位被文件占据
    try:
        check('目录不可用 → put None', hc.put_http_cache('https://z.dev', 'Z', 'c') is None)
    except Exception:
        check('目录不可用 → put None', False)
    try:
        check('目录不可用 → get None', hc.get_http_cache('https://z.dev') is None)
        hc.cleanup_http_cache()
        hc.get_http_cache_stats()
        check('目录不可用 → cleanup/stats 不抛', True)
    except Exception:
        check('目录不可用 → cleanup/stats 不抛', False)


# ---------------------------------------------------------------------------
# S10 url 截断
# ---------------------------------------------------------------------------

def test_s10_url_truncate() -> None:
    _fresh()
    p = hc.put_http_cache('https://t.dev/' + 'a' * 1000, 'L', 'c' * 10)
    data = json.loads(Path(p).read_text(encoding='utf-8'))
    check('落盘 url 截断 ≤512', len(data['url']) <= 512)
    check('落盘含 ts 字段', isinstance(data.get('ts'), float))


# ---------------------------------------------------------------------------
# S11 CLI
# ---------------------------------------------------------------------------

def test_s11_cli() -> None:
    r = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'http_cache.py'), 'stats'],
                       capture_output=True, text=True, timeout=30)
    check('CLI stats 退出码 0', r.returncode == 0)
    check('CLI 输出含 files 字段', '"files"' in r.stdout)


def main() -> int:
    print('=== http_cache 测试（缺口① · LRU + TTL + 容量上限）===')
    tests = [
        test_s1_basic_roundtrip, test_s2_reject_boundaries, test_s3_ttl,
        test_s4_touch_on_hit, test_s5_atomic_no_tmp, test_s6_capacity_lru,
        test_s7_cleanup_semantics, test_s8_stats, test_s9_fault_tolerant,
        test_s10_url_truncate, test_s11_cli,
    ]
    for fn in tests:
        print(f'\n{fn.__name__}')
        try:
            fn()
        except Exception as e:  # 测试自身异常 → 记为失败，不中断
            check(f'{fn.__name__} 未抛异常', False)
            print(f'    ! {type(e).__name__}: {e}')
    if _TMP and Path(_TMP).exists():
        shutil.rmtree(_TMP, ignore_errors=True)
    print(f'\nPASS={_PASS} FAIL={_FAIL}')
    return 0 if _FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
