#!/usr/bin/env python3
"""qveris_client.py — QVeris 能力路由网络客户端（v1.3 CN 端点适配）

QVeris = AI Agent 能力路由网络：discover → inspect → probe → call。
本模块以**零第三方依赖**（urllib）直连 REST API，供 infoseek 搜索链消费
结构化金融/数据能力（量化 / 宏观固收 / 风控合规 / 投资研究 / 加密 / 另类信号）。

双端点（key 前缀自动区分，env 可强制覆盖）：
  国际  https://qveris.ai/api/v1     ← 默认（sk- 前缀 key）
  CN    https://qveris.cn/api/v1     ← key 以 sk-cn- 开头时自动切换（国内合规区）

协议映射（两区一致，Bearer 认证）：
  discover  POST /search                   自然语言发现能力（免费）
  inspect   POST /tools/by-ids             按 tool_id 查看能力详情（免费）
  probe     POST /tools/probe?tool_id=     预验证参数 + 报价（免费，不执行）
  call      POST /tools/execute?tool_id=   执行能力（消耗 credits，沙箱结构化输出）
  audit     GET  /auth/usage/history/v2 · /auth/credits/ledger（用量/余额审计）

v1.3 变更（对齐 qveris.cn/docs/rest-api 与 MCP 文档）：
  - 双端点自动切换（sk-cn- → CN 区；INFOSEEK_QVERIS_BASE_URL 强制覆盖）
  - call 参数改名 parameters → params_to_tool；search 流程透传 search_id
  - inspect/call 请求体以新版字段为准，同时保留旧字段别名兼容

错误分类：自定义异常带 `code` 属性（429→quota / 401/403→forbidden），
与 engine_lifecycle.classify 直接兼容，自动进入引擎健康/配额生命周期。
"""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# 配置（env 可覆盖）
# ═══════════════════════════════════════════════════════════════

BASE_URLS = {
    'intl': 'https://qveris.ai/api/v1',
    'cn': 'https://qveris.cn/api/v1',
}
_DEFAULT_BASE_URL = os.environ.get(
    'INFOSEEK_QVERIS_BASE_URL', BASE_URLS['intl'])
DEFAULT_TIMEOUT = float(os.environ.get('INFOSEEK_QVERIS_TIMEOUT', '5'))
# 每次 search 最多执行的 call 次数（credits 保护；discover/inspect 免费不计数）
DEFAULT_CALL_BUDGET = int(os.environ.get('INFOSEEK_QVERIS_CALL_BUDGET', '3'))
_UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
       '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


def _endpoint_for_key(api_key: str) -> str:
    """按 key 前缀选区：sk-cn- → CN 区；其余 → 国际区。env 显式设置时优先。"""
    if os.environ.get('INFOSEEK_QVERIS_BASE_URL'):
        return os.environ['INFOSEEK_QVERIS_BASE_URL']
    return BASE_URLS['cn'] if api_key.startswith('sk-cn-') else _DEFAULT_BASE_URL


# ═══════════════════════════════════════════════════════════════
# 错误类型（code 属性与 engine_lifecycle.classify 兼容）
# ═══════════════════════════════════════════════════════════════

class QVerisError(Exception):
    """QVeris 调用错误基类。code 供 classify 分类（429→quota / 401,403→forbidden）。"""
    def __init__(self, message: str = '', code: Optional[int] = None):
        super().__init__(message or self.__class__.__name__)
        self.code = code


class QVerisQuotaError(QVerisError):
    """配额/限流/余额不足（HTTP 429 或 Insufficient credits）。"""
    def __init__(self, message: str = 'quota exhausted or rate limited', code: int = 429):
        super().__init__(message, code)


class QVerisAuthError(QVerisError):
    """认证失败（401/403）。"""
    def __init__(self, message: str = 'unauthorized', code: int = 401):
        super().__init__(message, code)


# ═══════════════════════════════════════════════════════════════
# Key 解析（env 优先，KeyManager 兜底；均缺失返回 ''）
# ═══════════════════════════════════════════════════════════════

def _resolve_key() -> str:
    v = os.environ.get('QVERIS_API_KEY', '')
    if v:
        return v
    try:
        import sys
        from pathlib import Path
        root = Path(__file__).parent.parent
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        from core.key_manager import get_key
        return get_key('qveris') or ''
    except Exception:
        return ''


# ═══════════════════════════════════════════════════════════════
# HTTP 层（零依赖 urllib）
# ═══════════════════════════════════════════════════════════════

def _post(base_url: str, path: str, payload: Optional[dict], api_key: str, timeout: float = DEFAULT_TIMEOUT) -> dict:
    """POST JSON → 解析响应。错误映射为 QVeris 异常族。"""
    body = json.dumps(payload or {}).encode('utf-8')
    req = urllib.request.Request(
        base_url + path,
        data=body,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': _UA,
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode('utf-8', errors='ignore') or '{}'
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise QVerisQuotaError(f'QVeris rate limited (429): {e.reason}')
        if e.code in (401, 403):
            raise QVerisAuthError(f'QVeris auth failed ({e.code}): {e.reason}')
        raise QVerisError(f'QVeris HTTP {e.code}: {e.reason}', code=e.code)
    except urllib.error.URLError as e:
        raise QVerisError(f'QVeris network error: {e.reason}', code=None)
    except TimeoutError:
        raise QVerisError('QVeris timeout', code=None)


def _ensure_success(data: dict):
    """HTTP 200 但业务失败（success:false）→ 抛对应异常。"""
    if isinstance(data, dict) and data.get('success') is False:
        msg = data.get('error_message') or ''
        if 'insufficient' in msg.lower() or 'credits' in msg.lower():
            raise QVerisQuotaError(f'QVeris insufficient credits: {msg}')
        raise QVerisError(f'QVeris execute failed: {msg}')


# ═══════════════════════════════════════════════════════════════
# 客户端
# ═══════════════════════════════════════════════════════════════

class QVerisClient:
    """QVeris 能力路由客户端（discover/inspect/probe/call）。"""

    def __init__(self, api_key: str = '', session_id: str = ''):
        self._key = api_key or _resolve_key()
        self._session_id = session_id or f'infoseek-{int(time.time())}'
        # 端点随 key 选区（env 可强制覆盖）
        self._base_url = _endpoint_for_key(self._key)
        # 最近一次 discover/inspect 的服务端 search_id（CN 端点在外层返回）
        self._last_search_id = ''

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def last_search_id(self) -> str:
        return self._last_search_id

    def available(self) -> bool:
        return bool(self._key)

    # ── 协议四步 ──
    def discover(self, query: str, limit: int = 5, view: str = 'routing') -> List[Dict]:
        """能力发现（免费）。返回 results 列表（tool_id/capability/cost_class/reliability）。

        服务端 search_id 存至 self._last_search_id（Call 阶段透传）。
        """
        if not self.available():
            return []
        data = _post(self._base_url, '/search', {
            'query': query, 'limit': max(1, min(limit, 100)),
            'session_id': self._session_id, 'view': view,
        }, self._key)
        self._last_search_id = data.get('search_id') or self._last_search_id
        return data.get('results') or []

    def inspect(self, tool_ids: List[str], view: str = 'lean') -> List[Dict]:
        """能力详情（免费）。返回完整结构（name/params/examples/provider_name/billing_rule）。

        CN 端点同样在外层返回 search_id，覆盖 self._last_search_id（优先于 discover 的）。
        """
        if not self.available() or not tool_ids:
            return []
        data = _post(self._base_url, '/tools/by-ids', {
            'tool_ids': tool_ids, 'session_id': self._session_id, 'view': view,
        }, self._key)
        self._last_search_id = data.get('search_id') or self._last_search_id
        return data.get('results') or []

    def probe(self, tool_id: str, parameters: Optional[dict] = None) -> Dict:
        """预验证参数 + 报价（免费，不执行）。"""
        if not self.available():
            return {}
        data = _post(self._base_url, f'/tools/probe?tool_id={tool_id}', {
            'parameters': parameters or {}, 'checks': ['schema', 'quote'], 'live_budget': 'none',
        }, self._key)
        return data if isinstance(data, dict) else {}

    def call(self, tool_id: str, parameters: Optional[dict] = None,
             model: str = '', max_response_size: int = 8192, search_id: str = '') -> Dict:
        """执行能力（消耗 credits）。返回完整响应（execution_id/result.data/billing/cost）。

        参数经 `params_to_tool` 字段传递（v1.3 对齐官方 REST/Call 契约）；
        同时保留旧字段 `parameters` 别名兼容早期部署。
        """
        if not self.available():
            return {}
        payload: Dict[str, Any] = {
            'tool_id': tool_id,
            'session_id': self._session_id,
            'params_to_tool': parameters or {},
            'parameters': parameters or {},   # 旧字段别名（兼容）
            'max_response_size': max_response_size,
        }
        if search_id:
            payload['search_id'] = search_id
        if model:
            payload['model'] = model
        data = _post(self._base_url, f'/tools/execute?tool_id={tool_id}', payload, self._key)
        _ensure_success(data)
        return data if isinstance(data, dict) else {}

    # ── 高层：面向调研的 search（discover → inspect 补全 → 预算内 call）──
    def search(self, query: str, max_results: int = 5, budget: int = 0) -> List[Dict]:
        """按意图发现能力、补全详情后执行（discover/inspect 免费；call 受 budget 限制）。

        流程对齐官方契约 Discover → Inspect → Call：
          1. discover 拿候选（tool_id + 服务端 search_id；CN 端点结果为精简结构）
          2. inspect 批量补全 name/examples.sample_parameters/provider_name（免费）
          3. 预算内 call（credits 保护），结果转为 infoseek 搜索链结构
        """
        if not self.available():
            return []
        budget = budget or DEFAULT_CALL_BUDGET
        hits = self.discover(query, limit=max(1, min(max_results + 1, 10)))
        if not hits:
            return []
        # 精简结构补全（CN discover 无 name/examples → 走 inspect，国际版已有则跳过）
        need = [h.get('tool_id') for h in hits
                if h.get('tool_id') and not (h.get('name') and h.get('examples'))]
        full = {}
        if need:
            for it in self.inspect(need):
                if it.get('tool_id'):
                    full[it['tool_id']] = it
        search_id = self._last_search_id  # 最后一次 discover/inspect 的服务端 search_id

        out: List[Dict] = []
        for hit in hits[:budget]:
            tool_id = hit.get('tool_id') or ''
            if not tool_id:
                continue
            details = full.get(tool_id) or hit
            params = ((details.get('examples') or {}).get('sample_parameters')) or {}
            try:
                resp = self.call(tool_id, params, max_response_size=8192, search_id=search_id)
            except QVerisQuotaError:
                raise  # 配额耗尽：上抛，由引擎生命周期标记
            except QVerisError:
                continue  # 单能力失败跳过，尝试下一个
            data = (resp.get('result') or {}).get('data')
            if data is None:
                continue
            out.append(self._to_result(tool_id, details, data, resp))
            if len(out) >= max_results:
                break
        return out

    @staticmethod
    def _to_result(tool_id: str, hit: Dict, data: Any, resp: Dict) -> Dict:
        name = hit.get('name') or tool_id
        provider = hit.get('provider_name') or ''
        snippet = json.dumps(data, ensure_ascii=False)[:500]
        exec_id = resp.get('execution_id') or tool_id
        billing = resp.get('billing') or {}
        cost = billing.get('list_amount_credits') or resp.get('cost') or 0
        return {
            'url': f'qveris://exec/{exec_id}',
            'title': f'[{provider or "QVeris"}] {name}',
            'snippet': snippet,
            'tool_id': tool_id,
            'provider': provider,
            'cost_credits': cost,
            'credits_remaining': resp.get('remaining_credits'),
        }


# ═══════════════════════════════════════════════════════════════
# 模块级便捷入口（pipeline 直接引用）
# ═══════════════════════════════════════════════════════════════

_client: Optional[QVerisClient] = None


def get_client() -> QVerisClient:
    global _client
    if _client is None:
        _client = QVerisClient()
    return _client


def search(query: str, max_results: int = 5, budget: int = 0) -> List[Dict]:
    """便捷：QVeris 能力搜索（pipeline._search_qveris 调用）。

    无 key → []；配额/认证错误**上抛**（QVerisQuotaError/QVerisAuthError），
    由 _call_engine 经 record_failure 分类（429→quota 禁用）；仅吞一般能力失败。
    """
    try:
        return get_client().search(query, max_results=max_results, budget=budget)
    except (QVerisQuotaError, QVerisAuthError):
        raise
    except QVerisError:
        return []


if __name__ == '__main__':
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else 'today SP500 movers'
    c = QVerisClient()
    prefix = (c._key[:6] + '…') if c.available() else '(none)'
    print(f'available={c.available()} endpoint={c.base_url} key={prefix}')
    if c.available():
        print(json.dumps(c.search(q, max_results=3), ensure_ascii=False, indent=2)[:800])
    else:
        print('未配置 QVERIS_API_KEY：先 export QVERIS_API_KEY=<key> 或 keys add qveris')
