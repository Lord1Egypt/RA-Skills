#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workbuddy_channel.py — WorkBuddy MCP Gateway 宿主注入通道（P0）
----------------------------------------------------------------
平台预装约定模块（platform_adapter._DEFAULT_MODULES 的 CHANNEL_ENV 默认名），
向 infoseek 平台 adapter 暴露统一契约：
  search(query, max_results) -> dict   # {ok,count,provider,hits:[{url,title,snippet}]}
  health() -> bool                     # 网关可用性探测（False → 不注册）
  meta = {'name','provider','cost'}    # 注册元信息

接入形态（按序探测）：
  1. WBG_SIDECAR_CMD       显式 sidecar 启动命令（默认：spawn 同目录 wb_gateway_sidecar.py）
                            —— 离线实测 / 无桌面端环境
  2. WBG_GATEWAY_URL       已运行网关的 HTTP JSON-RPC 地址（如 http://localhost:5126）
                            —— 真实 WorkBuddy 桌面端 / 宿主 sidecar 场景
     （真实 FastMCP streamable-http 未覆盖时保持 WBG_SIDECAR_CMD 形态兜底）

内部走标准 MCP 协议（JSON-RPC 2.0）：initialize → notifications/initialized →
wb_init → wb_search(能力发现) → wb_run('web_search', {query, max_results}）。
每个请求硬超时（默认 10s，env WBG_CALL_TIMEOUT 可调），超时抛异常
（上层 platform_adapter 记 failure → 健康剔除，不影响其他引擎）。
"""

import json
import os
import queue
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

name = 'WorkBuddy-WebSearch'

_CALL_TIMEOUT = float(os.environ.get('WBG_CALL_TIMEOUT', '10') or 10)
_SIDECAR = os.environ.get('WBG_SIDECAR_CMD') or (
    f'{sys.executable} {Path(__file__).parent / "wb_gateway_sidecar.py"}')
_GATEWAY_URL = os.environ.get('WBG_GATEWAY_URL', '').strip()

# §6A.7 调度台互斥：stdio sidecar（无 WBG_GATEWAY_URL）内部抓 cn.bing，是 wb 槽位的
# **仿真降级实现**（simulated）；HTTP 网关（WBG_GATEWAY_URL 指向真实 WorkBuddy 桌面端/
# 宿主 sidecar）才是真实高质量平台通道。platform_adapter 据此做 sim/真通道互斥注册。
_SIMULATED = not bool(_GATEWAY_URL)
_SIM_NAME = 'WorkBuddy-WebSearch(sim)'
meta = ({'name': _SIM_NAME, 'provider': 'workbuddy-gateway(sim)',
         'cost': '$0', 'capability': 'simulated', 'source': 'sim'}
        if _SIMULATED else
        {'name': name, 'provider': 'workbuddy-gateway', 'cost': '$0'})


def is_simulated() -> bool:
    """当前通道是否为仿真降级（stdio sidecar 抓 cn.bing），非真实 WorkBuddy 通道。

    判定依据：未注入 WBG_GATEWAY_URL（→ spawn 本地 wb_gateway_sidecar.py）。
    供 platform_adapter 守护⑥互斥注册与 auto 模式通道质量判定（§6A.6/§6A.7）。
    """
    return _SIMULATED

_client = None          # MCP stdio 客户端单例
_lock = threading.Lock()


# ---------------------------------------------------------------------------
# MCP stdio 客户端（最小实现：逐行 JSON-RPC 2.0）
# ---------------------------------------------------------------------------

class _MCPClient:
    def __init__(self, cmd: str):
        self.proc = subprocess.Popen(
            cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1)
        self._pending = {}
        self._next_id = 0
        self._lock = threading.Lock()
        threading.Thread(target=self._read_loop, daemon=True).start()
        self._boot()

    def _read_loop(self):
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            iid = msg.get('id')
            if iid is not None:
                q = self._pending.pop(iid, None)
                if q is not None:
                    q.put(msg)

    def _boot(self):
        """initialize + initialized 通知（MCP 握手）。"""
        self._call('initialize', {
            'protocolVersion': '2024-11-05',
            'capabilities': {},
            'clientInfo': {'name': 'infoseek-platform-adapter',
                           'version': '1.0.0'}})
        self._send({'jsonrpc': '2.0',
                    'method': 'notifications/initialized'})
        self._call('tools/list', {})

    def _next(self) -> int:
        with self._lock:
            self._next_id += 1
            return self._next_id

    def _send(self, msg: dict) -> None:
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + '\n')
        self.proc.stdin.flush()

    def _call(self, method: str, params: dict) -> dict:
        iid = self._next()
        q: queue.Queue = queue.Queue()
        with self._lock:
            self._pending[iid] = q
            try:
                self._send({'jsonrpc': '2.0', 'id': iid,
                            'method': method, 'params': params})
            except BrokenPipeError as e:
                self._pending.pop(iid, None)
                raise RuntimeError(f'网关进程已退出: {e}') from e
        try:
            msg = q.get(timeout=_CALL_TIMEOUT)
        except queue.Empty:
            self._pending.pop(iid, None)
            raise TimeoutError(f'MCP 调用 {method} 超时 >{_CALL_TIMEOUT}s')
        if 'error' in msg:
            raise RuntimeError(f'MCP {method} 错误: {msg["error"]}')
        return msg.get('result', {})

    def close(self):
        """关闭 sidecar 子进程（故障注入 / 资源释放）。"""
        try:
            self.proc.terminate()
            self.proc.wait(timeout=3)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# 网关会话（stdio / http 双形态统一调用面）
# ---------------------------------------------------------------------------

class _Gateway:
    def __init__(self):
        if _GATEWAY_URL:
            self._url = _GATEWAY_URL.rstrip('/')
            self._client = None
        else:
            self._url = ''
            self._client = _MCPClient(_SIDECAR)
        self._session = None

    def close(self):
        """关闭网关连接（stdio sidecar terminate / http 无状态）。"""
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None
        self._session = None

    def proc_pid(self) -> int | None:
        """当前 stdio sidecar 进程 pid（故障注入/健康实测用）。"""
        if self._client is not None and getattr(self._client, 'proc', None):
            return self._client.proc.pid
        return None

    # -- 底层调用 --
    def _http_call(self, method: str, params: dict) -> dict:
        body = json.dumps({'jsonrpc': '2.0', 'id': 1,
                           'method': method, 'params': params}).encode()
        req = urllib.request.Request(
            f'{self._url}/jsonrpc', data=body,
            headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=_CALL_TIMEOUT) as resp:
            msg = json.loads(resp.read().decode())
        if 'error' in msg:
            raise RuntimeError(f'HTTP {method} 错误: {msg["error"]}')
        return msg.get('result', {})

    def _call(self, method: str, params: dict) -> dict:
        return (self._http_call(method, params) if self._client is None
                else self._client._call(method, params))

    def _tool_result(self, name: str, args: dict) -> dict:
        """tools/call → 解析 content[0].text → 工具执行结果 dict。

        （tools/call 返回 {content:[{type:'text',text:'<json>'}]} 包裹，
         ensure/search_hits 统一经此解析，避免直接取顶层字段踩空。）
        """
        r = self._call('tools/call',
                       {'name': name, 'arguments': args})
        text = ''
        for c in (r.get('content') or []):
            if c.get('type') == 'text':
                text = c.get('text', '')
        if not text:
            return {'ok': False, 'count': 0, 'provider': meta['provider'],
                    'hits': []}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {'ok': False, 'count': 0, 'provider': meta['provider'],
                    'hits': []}

    # -- 能力动作 --
    def ensure(self) -> bool:
        """初始化 + 能力确认（幂等）。False → 网关不可用。"""
        try:
            if self._session is None:
                r = self._tool_result('wb_init',
                                      {'client_version': 'infoseek-p0'})
                sess = r.get('session_id') or ''
                caps = r.get('capabilities') or []
                if not sess or 'web_search' not in caps:
                    return False
                self._session = sess
            status = self._tool_result('wb_status', {})
            return bool(status.get('ok')) and 'web_search' in (
                status.get('capabilities') or [])
        except Exception:
            return False

    def search_hits(self, query: str, max_results: int) -> dict:
        """wb_run('web_search') → 原始 {ok,count,provider,hits}。"""
        self.ensure()
        return self._tool_result(
            'wb_run', {'capability': 'web_search',
                       'params': {'query': query,
                                  'max_results': max_results}})


_gateway = None


def _get_gateway():
    global _gateway
    if _gateway is None:
        with _lock:
            if _gateway is None:
                _gateway = _Gateway()
    return _gateway


# ---------------------------------------------------------------------------
# platform_adapter 契约实现
# ---------------------------------------------------------------------------

def health() -> bool:
    """网关注册探测：False / 异常 → platform_adapter 跳过注册。"""
    try:
        return _get_gateway().ensure()
    except Exception:
        return False


def search(query: str, max_results: int) -> dict:
    return _get_gateway().search_hits(query, max_results)


def gateway_pid() -> int | None:
    """当前 sidecar 进程 pid（编排脚本故障注入用）。"""
    try:
        return _get_gateway().proc_pid()
    except Exception:
        return None


def reset_gateway():
    """重建网关连接（编排脚本故障注入恢复用）。"""
    global _gateway
    with _lock:
        if _gateway is not None:
            try:
                _gateway.close()
            except Exception:
                pass
            _gateway = None


if __name__ == '__main__':
    # CLI 自检：python workbuddy_channel.py ['query']
    q = sys.argv[1] if len(sys.argv) > 1 else 'python quant'
    ok = health()
    print(f'health() = {ok} (gateway='
          f'{_GATEWAY_URL or _SIDECAR.split()[-1]})')
    if not ok:
        raise SystemExit(1)
    raw = search(q, 5)
    print(f'search({q!r}) -> ok={raw.get("ok")} count={raw.get("count")}')
    for h in raw.get('hits', [])[:5]:
        print(f'  - {h.get("title", "")[:60]} | {h.get("url", "")[:70]}')
    raise SystemExit(0 if raw.get('ok') else 2)