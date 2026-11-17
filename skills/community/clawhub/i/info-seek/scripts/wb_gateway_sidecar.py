#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wb_gateway_sidecar.py — WorkBuddy MCP Gateway 仿真 sidecar（P0 网关实测基建）
-----------------------------------------------------------------------------
形态对齐 WorkBuddy MCP Gateway 官方实证（docs.work-buddy.ai/handbook/operations_mcp-gateway）：
  - FastMCP sidecar，JSON-RPC 2.0 over stdio（逐行 JSON）
  - 工具面 7 个：wb_init / wb_search / wb_run / wb_advance / wb_step_result /
                 wb_status / wb_capability_result
  - 内置 WebSearch 子系统：web_search（真实 Bing CN 抓取）/ web_search_health / web_fetch
  - MCP 客户端侧工具名命名空间前缀：mcp__work-buddy__wb_*（本 sidecar 以裸名提供）

⚠️ 本文件是**仿真实现**（沙箱无 WorkBuddy 桌面端，用于离线实测 P0 平台适配器全链路），
   非 WorkBuddy 官方网关。真实宿主场景由 WorkBuddy 桌面端在 localhost:5126 提供，
   channel 通过 env WBG_GATEWAY_URL / WBG_SIDECAR_CMD 切换接入形态。

用法：python wb_gateway_sidecar.py              # stdio 模式（MCP 标准接入）
      python wb_gateway_sidecar.py --http 5126  # HTTP JSON-RPC 模式（旁路）
"""

import argparse
import json
import re
import sys
import threading
import time
import urllib.parse
import urllib.request

VERSION = '0.1.0-sim'
PROVIDER = 'workbuddy-gateway(sim)'
CAPABILITIES = ['web_search', 'web_fetch', 'web_search_health']

_UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
       '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')


# ---------------------------------------------------------------------------
# WebSearch 子系统（真实抓取：cn.bing.com，沙箱实测可达 200）
# ---------------------------------------------------------------------------

def _bing_search(query: str, max_results: int = 8) -> list:
    """cn.bing.com 真实搜索 → [{url,title,snippet}, ...]（尽力容错）。"""
    url = 'https://cn.bing.com/search?' + urllib.parse.urlencode(
        {'q': query, 'count': min(max(max_results, 1), 20), 'setlang': 'zh-hans'})
    req = urllib.request.Request(url, headers={
        'User-Agent': _UA,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml',
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='replace')

    out, seen = [], set()
    for block in re.findall(r'<li class="b_algo".*?</li>', html, re.S):
        m = re.search(r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not m:
            continue
        url, title = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not url.startswith('http') or '/search?' in url:
            continue
        if url in seen:
            continue
        snippet = ''
        p = re.search(r'<p[^>]*>(.*?)</p>', block, re.S)
        if p:
            snippet = re.sub(r'<[^>]+>', '', p.group(1)).strip()
        seen.add(url)
        out.append({'url': url, 'title': title or '', 'snippet': snippet[:400]})
        if len(out) >= max_results:
            break
    return out


def _web_fetch(url: str, max_chars: int = 2000) -> dict:
    """web_fetch 子系统：抓取页面纯文本前缀（尽力容错）。"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': _UA})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read(64 * 1024).decode('utf-8', errors='replace')
        text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', raw, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return {'ok': True, 'url': url, 'text': text[:max_chars],
                'chars': len(text)}
    except Exception as e:
        return {'ok': False, 'url': url, 'error': str(e)}


# ---------------------------------------------------------------------------
# 会话状态机 + capability 分发
# ---------------------------------------------------------------------------

class GatewaySession:
    def __init__(self):
        self.session_id = 'wb-' + re.sub(r'\D', '', str(time.time()))[-10:]
        self.created = time.time()
        self.steps = {}      # step_id -> 步骤状态（wb_advance 推进）
        self.next_step = 0

    def init(self, params: dict) -> dict:
        return {'ok': True, 'session_id': self.session_id,
                'version': VERSION, 'provider': PROVIDER,
                'capabilities': CAPABILITIES,
                'client_version': params.get('client_version', 'unknown')}

    def status(self) -> dict:
        return {'ok': True, 'status': 'ready', 'session_id': self.session_id,
                'uptime_s': round(time.time() - self.created, 1),
                'capabilities': CAPABILITIES, 'provider': PROVIDER}


def _run_capability(cap: str, params: dict) -> dict:
    """wb_run 核心分发：capability 执行 → {ok,count,provider,hits|result}。"""
    cap = (cap or '').strip().lower()
    if cap == 'web_search':
        query = str(params.get('query', '')).strip()
        if not query:
            return {'ok': False, 'error': 'query 为空'}
        try:
            hits = _bing_search(query, int(params.get('max_results', 8)))
        except Exception as e:
            return {'ok': False, 'error': f'web_search 抓取失败: {e}'}
        return {'ok': True, 'count': len(hits), 'provider': PROVIDER,
                'capability': 'web_search', 'hits': hits}
    if cap == 'web_fetch':
        return _web_fetch(str(params.get('url', '')),
                          int(params.get('max_chars', 2000)))
    if cap in ('web_search_health', 'health'):
        return {'ok': True, 'status': 'healthy',
                'capability': 'web_search', 'provider': PROVIDER}
    return {'ok': False, 'error': f'未知 capability: {cap!r}，'
                                  f'可用: {CAPABILITIES}'}


# ---------------------------------------------------------------------------
# 工具分发（7 个 wb_*，对齐官方工具面）
# ---------------------------------------------------------------------------

def _dispatch_tool(name: str, arguments: dict, sess: GatewaySession) -> dict:
    args = arguments or {}
    if name == 'wb_init':
        return sess.init(args)
    if name == 'wb_search':
        # 能力发现（官方：经 wb_search 发现 capability schema）
        q = args.get('query', '') or ''
        return {'ok': True, 'capabilities': CAPABILITIES,
                'schema': {'web_search': {
                    'query': 'string(required)', 'max_results': 'int(1-20)',
                    'description': 'WorkBuddy 内置 WebSearch 子系统'
                                   '（Web Search / Web Fetch / Health）'}},
                'matched': [c for c in CAPABILITIES
                            if q and c.startswith(q.lower())]}
    if name == 'wb_run':
        return _run_capability(args.get('capability', ''), args.get('params', {}))
    if name == 'wb_advance':
        # 复合任务推进：以 step 为单位（web_search 可直接单步执行）
        step = args.get('step') or 'web_search'
        sess.next_step += 1
        sid = f'{sess.session_id}-s{sess.next_step}'
        sess.steps[sid] = {'step': step, 'params': args.get('params', {}),
                           'status': 'done', 'ts': time.time()}
        res = _run_capability(step, args.get('params', {}))
        sess.steps[sid]['result'] = res
        return {'ok': True, 'step_id': sid,
                'step_result': res,
                'remaining_steps': 0, 'done': True}
    if name == 'wb_step_result':
        sid = args.get('step_id', '')
        return sess.steps.get(sid, {'ok': False, 'error': f'step {sid!r} 不存在'})
    if name == 'wb_status':
        return sess.status()
    if name == 'wb_capability_result':
        cap = args.get('capability', '')
        if cap not in CAPABILITIES:
            return {'ok': False, 'error': f'capability {cap!r} 不可用'}
        return {'ok': True, 'capability': cap,
                'capabilities': CAPABILITIES,
                'schema': {'web_search': {
                    'query': 'string(required)', 'max_results': 'int(1-20)'},
                    'web_fetch': {'url': 'string(required)',
                                  'max_chars': 'int'},
                    'web_search_health': {}}}
    return {'ok': False, 'error': f'未知工具 {name!r}'}


_TOOLS = [
    {'name': 'wb_init',
     'description': '初始化 WorkBuddy 会话，返回 session_id/capabilities',
     'inputSchema': {'type': 'object',
                     'properties': {'client_version': {'type': 'string'}}}},
    {'name': 'wb_search',
     'description': '发现 capability 与 schema（WebSearch 子系统入口）',
     'inputSchema': {'type': 'object',
                     'properties': {'query': {'type': 'string'}}}},
    {'name': 'wb_run',
     'description': '执行 capability（web_search / web_fetch / web_search_health）',
     'inputSchema': {'type': 'object',
                     'properties': {
                         'capability': {'type': 'string',
                                        'enum': CAPABILITIES},
                         'params': {'type': 'object'}},
                     'required': ['capability', 'params']}},
    {'name': 'wb_advance',
     'description': '推进复合任务（step 级执行）',
     'inputSchema': {'type': 'object',
                     'properties': {'step': {'type': 'string'},
                                    'params': {'type': 'object'}}}},
    {'name': 'wb_step_result',
     'description': '查询步骤执行结果',
     'inputSchema': {'type': 'object',
                     'properties': {'step_id': {'type': 'string'}}}},
    {'name': 'wb_status',
     'description': '网关/会话健康状态',
     'inputSchema': {'type': 'object', 'properties': {}}},
    {'name': 'wb_capability_result',
     'description': '查询 capability 详情与 schema',
     'inputSchema': {'type': 'object',
                     'properties': {'capability': {'type': 'string'}}}},
]

_SERVER_INFO = {'name': 'work-buddy-gateway', 'version': VERSION,
                'provider': PROVIDER}


# ---------------------------------------------------------------------------
# stdio 传输（MCP 标准形态：逐行 JSON-RPC 2.0）
# ---------------------------------------------------------------------------

class StdioTransport:
    def __init__(self, reader, writer):
        self.r, self.w = reader, writer
        self.lock = threading.Lock()

    def send(self, obj: dict) -> None:
        with self.lock:
            self.w.write(json.dumps(obj, ensure_ascii=False) + '\n')
            self.w.flush()


def handle_message(msg: dict, sess: GatewaySession, out) -> dict | None:
    method = msg.get('method', '')
    if method == 'initialize':
        return {'jsonrpc': '2.0', 'id': msg.get('id', 0),
                'result': {'protocolVersion': msg.get('params', {}).get(
                    'protocolVersion', '2024-11-05'),
                    'capabilities': {'tools': {}},
                    'serverInfo': _SERVER_INFO}}
    if method == 'notifications/initialized':
        return None  # 通知无响应
    if method == 'ping':
        return {'jsonrpc': '2.0', 'id': msg.get('id', 0), 'result': {}}
    if method == 'tools/list':
        return {'jsonrpc': '2.0', 'id': msg.get('id', 0),
                'result': {'tools': _TOOLS}}
    if method == 'tools/call':
        p = msg.get('params', {})
        try:
            result = _dispatch_tool(p.get('name', ''),
                                    p.get('arguments', {}), sess)
            return {'jsonrpc': '2.0', 'id': msg.get('id', 0),
                    'result': {'content': [{'type': 'text',
                                            'text': json.dumps(
                                                result, ensure_ascii=False)}],
                               'isError': False}}
        except Exception as e:
            return {'jsonrpc': '2.0', 'id': msg.get('id', 0),
                    'error': {'code': -32000, 'message': str(e)}}
    return {'jsonrpc': '2.0', 'id': msg.get('id', 0),
            'error': {'code': -32601, 'message': f'未知方法 {method!r}'}}


def run_stdio() -> int:
    """stdio 主循环：逐行 JSON（MCP 标准适配，纯文本日志走 stderr）。"""
    sess = GatewaySession()
    print(f'[gateway] {_SERVER_INFO["name"]} v{VERSION} stdio 就绪，'
          f'session={sess.session_id}', file=sys.stderr, flush=True)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as e:
            print(f'[gateway] 坏消息: {e}', file=sys.stderr, flush=True)
            continue
        try:
            resp = handle_message(msg, sess, sys.stdout)
        except Exception as e:
            resp = {'jsonrpc': '2.0', 'id': msg.get('id'),
                    'error': {'code': -32603, 'message': str(e)}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + '\n')
            sys.stdout.flush()
    return 0


def run_http(port: int) -> int:
    """HTTP JSON-RPC 旁路（非 MCP 标准，仅调试用）。"""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    sess = GatewaySession()
    print(f'[gateway] HTTP 旁路 http://localhost:{port} session={sess.session_id}',
          file=sys.stderr, flush=True)

    class H(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa: N802
            n = int(self.headers.get('Content-Length', 0))
            try:
                msg = json.loads(self.rfile.read(n) or b'{}')
                resp = handle_message(msg, sess, sys.stderr) or {}
            except Exception as e:
                resp = {'jsonrpc': '2.0', 'id': None,
                        'error': {'code': -32603, 'message': str(e)}}
            body = json.dumps(resp, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):
            pass

    HTTPServer(('127.0.0.1', port), H).serve_forever()


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='WorkBuddy MCP Gateway 仿真 sidecar')
    ap.add_argument('--http', type=int, default=0,
                    help='HTTP 旁路端口（默认 0=仅 stdio）')
    a = ap.parse_args()
    if a.http:
        run_http(a.http)
    else:
        raise SystemExit(run_stdio())