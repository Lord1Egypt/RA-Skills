#!/usr/bin/env python3
"""engine_router.py — 引擎路由（策略② · 可用性探测 + 白名单路由）

配置级即生效，无新依赖：
  - 白名单：env INFOSEEK_ENGINE_WHITELIST（逗号分隔引擎名，如 "exa,tavily,duckduckgo-html"）
            优先于 references/engine-routes.json 的 whitelist 字段；空 = 全部放行。
  - 可用性探测：INFOSEEK_ENGINE_PROBE=1 启用（默认 off，避免搜索首查变慢）。
    免费引擎做 HTTP 连通探测（复用 probe_http 逻辑），剔除不可达引擎；
    结果落盘 ~/.infoseek/engine_routes.json（TTL=INFOSEEK_PROBE_TTL，默认 600s），
    TTL 内复用缓存，探测仅首次或过期时发生。
  - 键控引擎：白名单过滤 + key 存在性检查（无 key 直接剔除，零网络开销）。

用法（pipeline 自动调用）：
  from engine_router import route_engines
  engines = route_engines([("Exa", fn), ...])
"""
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
_CACHE_PATH = Path(os.environ.get(
    'INFOSEEK_ROUTE_CACHE', str(Path.home() / '.infoseek' / 'engine_routes.json')))

# 免费引擎 → 探测 URL（配置文件可覆盖）
_DEFAULT_PROBE_URLS = {
    'DuckDuckGo-HTML': 'https://duckduckgo.com/html/?q=test',
    'Bing-RSS': 'https://www.bing.com/search?q=test&format=rss',
    'Jina-AI': 'https://r.jina.ai/http://example.com',
    'Wikipedia': 'https://zh.wikipedia.org/wiki/Special:Search?search=test',
}

_mem_cache = {'ts': 0.0, 'data': None}  # 进程内探测结果缓存


def _load_config() -> dict:
    """读取 references/engine-routes.json（不存在 → 默认配置）。"""
    try:
        with open(ROOT / 'references' / 'engine-routes.json', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'whitelist': [], 'probe': {}}


def engine_whitelist() -> set:
    """白名单引擎名集合（小写）；env 优先，其次配置文件；空 = 全部放行。"""
    raw = os.environ.get('INFOSEEK_ENGINE_WHITELIST', '')
    if raw:
        return {n.strip().lower() for n in raw.split(',') if n.strip()}
    cfg = _load_config()
    return {str(n).strip().lower() for n in cfg.get('whitelist', []) if str(n).strip()}


def probe_enabled() -> bool:
    """探测开关：INFOSEEK_ENGINE_PROBE=1 优先；其次配置文件 probe.enabled；默认关。"""
    v = os.environ.get('INFOSEEK_ENGINE_PROBE', '')
    if v:
        return v not in ('0', 'false', 'False', 'no', 'off')
    return bool(_load_config().get('probe', {}).get('enabled', False))


def _probe_timeout() -> float:
    """探测超时秒：env > 配置 > 默认 5。"""
    v = os.environ.get('INFOSEEK_PROBE_TIMEOUT', '')
    if v:
        try:
            return float(v)
        except ValueError:
            pass
    return float(_load_config().get('probe', {}).get('timeout', 5.0))


def _probe_ttl() -> int:
    """探测缓存 TTL 秒：env > 配置 > 默认 600。"""
    v = os.environ.get('INFOSEEK_PROBE_TTL', '')
    if v:
        try:
            return int(v)
        except ValueError:
            pass
    return int(_load_config().get('probe', {}).get('ttl', 600))


def _probe_urls() -> dict:
    """探测 URL 表：配置文件 probe.urls 覆盖默认。"""
    urls = dict(_DEFAULT_PROBE_URLS)
    urls.update(_load_config().get('probe', {}).get('urls', {}) or {})
    return urls


def probe_http(url: str, timeout: float) -> tuple:
    """返回 (ok, elapsed, err)——GA12 起委托 net_probe 唯一真源（同构签名，严格 200）。"""
    try:
        from net_probe import probe_http as _probe
    except Exception:
        from scripts.net_probe import probe_http as _probe  # type: ignore
    return _probe(url, timeout)


def _refresh_probe_cache(force: bool = False) -> dict:
    """加载探测结果缓存（磁盘 → 内存）；过期/缺失 → 返回空。"""
    if force or not _mem_cache['data']:
        try:
            if _CACHE_PATH.exists():
                _mem_cache['data'] = json.loads(_CACHE_PATH.read_text(encoding='utf-8'))
        except Exception:
            _mem_cache['data'] = None
    data = _mem_cache['data'] or {}
    if force:
        return {}
    ts = data.get('ts', 0)
    if time.time() - ts > _probe_ttl():
        return {}
    return data.get('result', {})


def _save_probe_cache(result: dict) -> None:
    _mem_cache['data'] = {'ts': time.time(), 'result': result}
    try:
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_PATH.write_text(json.dumps({'ts': time.time(), 'result': result},
                                          ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass  # 缓存写失败不影响路由


def _probe_free(name: str) -> bool:
    """免费引擎可用性（缓存 + 探测）；不存在探测配置 → 放行。"""
    urls = _probe_urls()
    url = urls.get(name)
    if not url:
        return True
    cached = _refresh_probe_cache()
    if name in cached:
        return bool(cached[name].get('ok'))
    ok, _, _ = probe_http(url, _probe_timeout())
    cached[name] = {'ok': ok, 'ts': time.time()}
    _save_probe_cache(cached)
    return ok


def route_engines(engines: list) -> list:
    """路由过滤引擎列表：白名单 + 键控 key 检查 + 可选免费探测。返回 [(name, fn), ...]。"""
    if not engines:
        return engines
    wl = engine_whitelist()
    do_probe = probe_enabled()
    out = []
    for name, fn in engines:
        key = name.lower()
        if wl and key not in wl:
            continue  # 白名单精确控制：名单外一律剔除
        if key in ('exa', 'tavily', 'zhipu', 'metaso', 'tinyfish', 'qveris'):
            env_map = {'exa': 'EXA_API_KEY', 'tavily': 'TAVILY_API_KEY',
                       'zhipu': 'ZHIPU_API_KEY', 'metaso': 'METASO_API_KEY',
                       'tinyfish': 'TINYFISH_API_KEY', 'qveris': 'QVERIS_API_KEY'}
            if not os.environ.get(env_map[key]):
                continue  # 无 key 的键控引擎直接剔除（零网络开销）
        elif do_probe and not _probe_free(name):
            continue  # 探测确认不可达的免费引擎剔除（TTL 内复用缓存）
        out.append((name, fn))
    return out


def cli() -> int:
    """CLI：查看当前路由决策（白名单 + 探测结果）。"""
    import sys
    print('=== infoseek 引擎路由（engine_router v1.0.0 · 策略②）===')
    print(f'白名单: {sorted(engine_whitelist()) or "(空=全部放行)"}')
    print(f'探测: {"开启" if probe_enabled() else "关闭"} '
          f'(timeout={_probe_timeout()}s ttl={_probe_ttl()}s cache={_CACHE_PATH})')
    if engine_whitelist():
        print(f'键控过滤结果: {sorted(engine_whitelist())} 中保留已配置 key 者')
    for name, url in _probe_urls().items():
        if probe_enabled():
            ok, dt, err = probe_http(url, _probe_timeout())
            print(f'  {name:16s} {"✅" if ok else "❌ " + err} ({dt}s)')
        else:
            print(f'  {name:16s} (探测关闭)')
    return 0


if __name__ == '__main__':
    sys.exit(cli())