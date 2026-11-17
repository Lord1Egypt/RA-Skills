#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
platform_adapter.py — 平台 Web 搜索引擎适配器（三路并发 · P0）

定位：平台 web 搜索是"第 N+1 路引擎"。以统一二元组 (name, fn) 注册进引擎池
默认层（_default_layer），自动获得并行调度 / 失败隔离 / url 去重 / 多样性合并 /
健康生命周期剔除 / 保留池兜底 全部能力（并发内核零改动）。

三路径（探测到哪个用哪个；均失败 → 不注册，零网络开销）：
  1. INFOSEEK_PLATFORM_CHANNEL=<module[:attr]>：宿主注入通道（首选）
     —— WorkBuddy 桌面 / Codex 等宿主拉起 infoseek 时注入 wb_run 通道
  2. 约定模块 workbuddy_channel / mcp_channel（平台预装，可 import）
  3. ima / OpenAPI：OpenAPI v1.1.7 实证仅 Notes+KB 管理端点，无 web search
     ——仅保留探测位，探测到才注册（当前不产生注册）

通道模块契约：
  search(query, max_results) -> list[dict]   # 必选：{url,title,snippet}[]
  health() -> bool|None                        # 可选：启动探测（False/异常 → 不注册）
  meta = {'name','provider','cost'}            # 可选：注册名 / 来源标注 / 成本标注

归一化（宽容解析，抗平台 schema 漂移）：
  {ok,count,provider,hits:[...]} → hits 条目字典/字符串混排均可
  {results:[...]} / {data:[...]} / {web:[...]} / {items:[...]} → 平铺
  直接 list → 原样
  url 缺失条目过滤；title/snippet 缺失补默认值；长度截断

配置（env）：
  INFOSEEK_PLATFORM_WEBSEARCH        auto|wb|mcp|ima|off   默认 auto（探测）
  INFOSEEK_PLATFORM_CHANNEL          通道模块 spec（auto/wb 模式的注入通道）
  INFOSEEK_PLATFORM_MCP_CHANNEL      MCP 网关通道 spec（auto/mcp 模式）
  INFOSEEK_PLATFORM_IMA_CHANNEL      ima OpenAPI 通道 spec（auto/ima 模式）
  INFOSEEK_PLATFORM_WEBSEARCH_TIMEOUT 秒                    默认 10（硬超时）
  INFOSEEK_PLATFORM_WEBSEARCH_WEIGHT  float                 默认 0.9（融合权重）
  INFOSEEK_PLATFORM_THROTTLE_MS       int                   默认 0（adapter 内节流）

工程约束：
  - 超时在 adapter 内抛异常 → 上层 _call_engine 记 failure → 健康剔除
  - 纯 CLI / 无宿主注入 → platform_engines() 返回 []，零网络开销
  - 本文件不 import infoseek_pipeline（无循环依赖）；仅被其 import
"""

import importlib
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _FutTimeout

log = logging.getLogger(__name__)

DEFAULT_NAME = 'WorkBuddy-WebSearch'
DEFAULT_TIMEOUT = 10.0
DEFAULT_WEIGHT = 0.9

MODE_ENV = 'INFOSEEK_PLATFORM_WEBSEARCH'
CHANNEL_ENV = 'INFOSEEK_PLATFORM_CHANNEL'
MCP_CHANNEL_ENV = 'INFOSEEK_PLATFORM_MCP_CHANNEL'
IMA_CHANNEL_ENV = 'INFOSEEK_PLATFORM_IMA_CHANNEL'
TIMEOUT_ENV = 'INFOSEEK_PLATFORM_WEBSEARCH_TIMEOUT'
WEIGHT_ENV = 'INFOSEEK_PLATFORM_WEBSEARCH_WEIGHT'
THROTTLE_ENV = 'INFOSEEK_PLATFORM_THROTTLE_MS'

# 平台通道名 → 免 import 的约定模块名（平台预装于 PYTHONPATH）
_DEFAULT_MODULES = {
    CHANNEL_ENV: 'workbuddy_channel',
    MCP_CHANNEL_ENV: 'mcp_channel',
    IMA_CHANNEL_ENV: 'ima_channel',
}
_MODE_ORDER = {
    'wb': (CHANNEL_ENV,),
    'mcp': (MCP_CHANNEL_ENV,),
    'ima': (IMA_CHANNEL_ENV,),
    'auto': (CHANNEL_ENV, MCP_CHANNEL_ENV, IMA_CHANNEL_ENV),
}


class EngineAdapter:
    """平台引擎适配器协议（P0 最小面）：统一 search 签名 + 元信息。

    子类只需实现 search(query, max_results)；health() 可选。
    注册后以 (name, fn) 二元组进入引擎池，fn = adapter.search 的闭包包装。
    """

    name = DEFAULT_NAME
    type = 'platform'
    cost = '$0'
    provider = 'unknown'

    def search(self, query: str, max_results: int) -> list:
        """返回 [{url, title, snippet}, ...]，长度 ≤ max_results。"""
        raise NotImplementedError

    def health(self) -> bool:
        """启动可用性探测；None/True → 视为可用，False/异常 → 不注册。"""
        return True


class WorkBuddyAdapter(EngineAdapter):
    """WorkBuddy 桌面端 web_search 通道（wb_run 形态的标准实现）。

    宿主（WorkBuddy 桌面 / Codex）拉起 infoseek 时注入 wb_run 可调用对象
    （形如 wb_run('web_search', {...}) 或 wb_run.tool('web_search', {...})，
    兼容两形态），wrapper 负责 {ok,count,provider,hits} → 归一化列表。
    """

    name = DEFAULT_NAME
    provider = 'workbuddy'

    def __init__(self, wb_run=None):
        self._wb_run = wb_run

    def health(self) -> bool:
        return callable(self._wb_run)

    def search(self, query: str, max_results: int) -> list:
        if not callable(self._wb_run):
            raise RuntimeError('wb_run 不可用（平台宿主未注入通道）')
        raw = self._wb_run('web_search', {'query': query, 'max_results': max_results})
        return _normalize(raw, max_results)


# ---------------------------------------------------------------------------
# schema 归一化（宽容解析，抗平台结果漂移）
# ---------------------------------------------------------------------------

def _norm_hit(hit):
    """单条结果宽容归一化 → {url,title,snippet}；url 缺失 → None。"""
    if isinstance(hit, str):
        if hit.startswith(('http://', 'https://')):
            return {'url': hit, 'title': '', 'snippet': ''}
        return None  # 纯文本条目无法溯源，丢弃
    if not isinstance(hit, dict):
        return None
    url = hit.get('url') or hit.get('link') or hit.get('href')
    if not url:
        return None
    title = hit.get('title') or hit.get('name') or ''
    snippet = (hit.get('snippet') or hit.get('summary')
               or hit.get('description') or hit.get('excerpt') or '')
    return {'url': str(url), 'title': str(title)[:200],
            'snippet': str(snippet)[:400]}


_CONTAINER_KEYS = ('results', 'data', 'web', 'items', 'hits', 'entries', 'list')


def _normalize(raw, max_results: int) -> list:
    """平台返回 schema 宽容归一化（抗漂移）。支持 dict 容器 / 裸 list。"""
    out, seen = [], set()

    def push(items):
        for h in items or []:
            r = _norm_hit(h)
            if r and r['url'] not in seen:
                seen.add(r['url'])
                out.append(r)

    if isinstance(raw, dict):
        for key in _CONTAINER_KEYS:
            if isinstance(raw.get(key), list):
                push(raw[key])
                break  # 只认第一个非空列表键，避免多键重复消费同一数据
        if not out:
            for v in raw.values():  # 兜底：任意列表值（平台 schema 未知漂移）
                if isinstance(v, list) and v and isinstance(v[0], (dict, str)):
                    push(v)
                    break
    elif isinstance(raw, list):
        push(raw)
    return out[:max_results]


# ---------------------------------------------------------------------------
# 通道探测与包装
# ---------------------------------------------------------------------------

def _import_channel(spec: str):
    """按 '<module[:attr]>' 或 'module.attr'（末段为属性）导入通道对象。"""
    mod_path, _, attr = spec.partition(':')
    if not attr and '.' in spec:
        mod_path, _, attr = spec.rpartition('.')
    mod = importlib.import_module(mod_path)
    return getattr(mod, attr) if attr else mod


def _probe_channel():
    """按 env 模式路由探测可用通道；无可用 → None。

    - off       → 显式关闭
    - wb/mcp/ima → 只探对应通道（env spec → 约定模块）
    - auto(默认) → 依次探 wb → mcp → ima
    """
    mode = os.environ.get(MODE_ENV, 'auto').strip().lower()
    if mode == 'off':
        return None
    if mode not in _MODE_ORDER:
        log.warning(f"[platform] 未知模式 {mode!r}，按 auto 处理")
        mode = 'auto'
    for env_key in _MODE_ORDER[mode]:
        spec = os.environ.get(env_key)
        if spec:
            try:
                return _import_channel(spec)
            except Exception as e:
                log.warning(f"[platform] 通道导入失败 {spec}: {e}")
                continue
        try:
            return importlib.import_module(_DEFAULT_MODULES[env_key])
        except Exception:
            continue  # 约定模块未预装 → 下一候选
    return None


def _channel_ready(ch) -> bool:
    """通道有效性：search 可调 + health() 探测（False/异常 → 不注册）。"""
    if not callable(getattr(ch, 'search', None)):
        return False
    health = getattr(ch, 'health', None)
    if callable(health):
        try:
            if health() is False:
                log.info('[platform] 通道 health()=False，跳过注册')
                return False
        except Exception as e:
            log.warning(f'[platform] health() 异常: {e}，跳过注册')
            return False
    return True


def _make_search_fn(ch):
    """包装通道 search → 统一 fn(query, max_results)。

    - 硬超时：单 worker 线程池 + future.result(timeout) → 超时抛异常
      （上层 _call_engine 记 failure → 健康剔除；不影响其他引擎）
    - 节流：INFOSEEK_PLATFORM_THROTTLE_MS 毫秒（并发放大保护）
    - 归一化：_normalize 宽容解析
    """
    timeout = float(os.environ.get(TIMEOUT_ENV, DEFAULT_TIMEOUT))
    throttle = 0.0
    try:
        throttle = int(os.environ.get(THROTTLE_ENV, '0') or 0) / 1000.0
    except ValueError:
        pass
    pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix='platform-adapter')

    def _call(query, max_results):
        if throttle > 0:
            time.sleep(throttle)
        return _normalize(ch.search(query, max_results), max_results)

    def fn(query, max_results):
        fut = pool.submit(_call, query, max_results)
        try:
            return fut.result(timeout=timeout)
        except _FutTimeout:
            fut.cancel()
            raise TimeoutError(
                f'[platform:{ch.name if hasattr(ch, "name") else "channel"}] '
                f'超时 >{timeout}s')
    return fn


# ---------------------------------------------------------------------------
# 注册入口（供 infoseek_pipeline._default_layer() 调用）
# ---------------------------------------------------------------------------

_ENGINE_CACHE = None   # None=未探测；False=探测失败；tuple=(name, fn)
_ENGINE_PROBED = False


def platform_engine():
    """探测 + 构建 → (name, fn) 或 None（失败）。进程内仅探测一次。"""
    global _ENGINE_CACHE, _ENGINE_PROBED
    if not _ENGINE_PROBED:
        _ENGINE_PROBED = True
        try:
            ch = _probe_channel()
            if ch is None or not _channel_ready(ch):
                _ENGINE_CACHE = False
            else:
                meta = getattr(ch, 'meta', None) or {}
                name = meta.get('name') or getattr(ch, 'name', DEFAULT_NAME)
                _ENGINE_CACHE = (name, _make_search_fn(ch))
                log.info(
                    f'[platform] 注册 {name} '
                    f"(provider={meta.get('provider', 'platform')}, "
                    f"cost={meta.get('cost', '$0')})")
        except Exception as e:  # 探测异常 → 不注册，保底可用性
            log.warning(f'[platform] 探测失败: {e}')
            _ENGINE_CACHE = False
    return _ENGINE_CACHE if _ENGINE_CACHE else None


def platform_engines() -> list:
    """供 pipeline 注册入口：成功 → [(name, fn)]；失败 → []（零网络开销）。"""
    e = platform_engine()
    return [e] if e else []


def platform_engine_simulated() -> bool | None:
    """§6A.7 当前注册的平台通道是否为仿真（sim）降级实现。

    返回：
      True  = 已注册但 capability=simulated（stdio sidecar 抓 cn.bing，与池内 Bing 同源）
      False = 已注册且为真实高质量平台通道（HTTP WorkBuddy / mcp / ima）
      None  = 未注册任何平台通道（纯 CLI 沙箱）
    供调度台 auto 模式做通道质量判定（真通道→阶梯少补偿；仅 sim/无通道→保守补偿）。
    进程内复用 platform_engine 的单次探测缓存，不产生额外网络开销。
    """
    e = platform_engine()
    if not e:
        return None
    # 探测期已把通道 meta 记入缓存名；sim 通道名带 (sim) 后缀 / provider 带 (sim)。
    eng_name = e[0] or ''
    return '(sim)' in eng_name or 'simulated' in eng_name



def platform_weight() -> float:
    """融合权重（env INFOSEEK_PLATFORM_WEBSEARCH_WEIGHT 覆盖，默认 0.9）。"""
    try:
        return float(os.environ.get(WEIGHT_ENV, DEFAULT_WEIGHT))
    except (TypeError, ValueError):
        return DEFAULT_WEIGHT


def cli() -> int:
    """CLI：查看平台通道探测结果（默认可复现注册前检查）。"""
    import sys
    print('=== infoseek 平台 adapter（P0）===')
    print(f'模式: {os.environ.get(MODE_ENV, "auto")} '
          f'(权重 {platform_weight()} · 超时 '
          f'{os.environ.get(TIMEOUT_ENV, DEFAULT_TIMEOUT)}s)')
    ch = _probe_channel()
    if ch is None:
        print('通道: ❌ 未探测到（纯 CLI / 宿主未注入 → 不注册，零开销）')
        return 0
    ready = _channel_ready(ch)
    meta = getattr(ch, 'meta', None) or {}
    name = meta.get('name') or getattr(ch, 'name', DEFAULT_NAME)
    print(f'通道: {"✅" if ready else "❌"} {name} '
          f"(provider={meta.get('provider', 'unknown')}, "
          f"cost={meta.get('cost', '$0')})")
    return 0 if ready else 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    raise SystemExit(cli())