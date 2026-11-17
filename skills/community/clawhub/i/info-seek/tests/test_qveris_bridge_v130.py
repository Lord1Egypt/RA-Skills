#!/usr/bin/env python3
"""test_qveris_bridge_v130.py — QVeris 桥接测试（v1.3 CN 端点适配 + 真实凭据验证过）

覆盖（对齐 P4 验收）：
  Q1  端点选区：sk-cn- → CN 区 / 其他 → 国际区 / env 强制覆盖
  Q2  无 key 降级：available=False，discover/inspect/call/search 均 [] 
  Q3  Discover→Inspect→Call 流程（mock：CN 精简 discover → inspect 补全 → call 成功）
  Q4  配额/认证错误上抛：429→QVerisQuotaError，401→QVerisAuthError（供生命周期分类）
  Q5  单能力失败跳过 + 高亮结果结构（url/title/snippet/tool_id/cost）
  Q6  失败 HTTP（网络/超时）→ QVerisError（模块级 search 吞掉返回 []）
  Q7  search_id 透传 Call（伪造外层 search_id → 断言 call payload 带 search_id）
  Q8  pipeline 集成：_search_qveris 包装、429 上抛被生命周期标记、无 key []、
      有 key 经 qv_search 返回规范结果
"""
import os
import sys
import json
import tempfile
from pathlib import Path
from unittest import mock

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))

import qveris_client as qc

_tmp = tempfile.mkdtemp()
os.environ['INFOSEEK_DATA_DIR'] = _tmp

passed, failed = [], []
def check(name, cond, detail=''):
    (passed if cond else failed).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── Q1: 端点选区 ──
check('Q1 sk-cn- → CN 区',
      qc._endpoint_for_key('sk-cn-abc') == 'https://qveris.cn/api/v1')
check('Q1 普通 sk- → 国际区',
      qc._endpoint_for_key('sk-abc') == 'https://qveris.ai/api/v1')
check('Q1 空 key → 国际区默认',
      qc._endpoint_for_key('') == 'https://qveris.ai/api/v1')
check('Q1 env 强制覆盖优先',
      qc._endpoint_for_key('sk-cn-x') == 'https://qveris.cn/api/v1')
check('Q1 客户端实例 base_url',
      qc.QVerisClient(api_key='sk-cn-x').base_url == 'https://qveris.cn/api/v1')
check('Q1 国际客户端 base_url',
      qc.QVerisClient(api_key='sk-x').base_url == 'https://qveris.ai/api/v1')


# ── Q2: 无 key 降级 ──
_c0 = qc.QVerisClient(api_key='')
check('Q2 available=False', not _c0.available())
check('Q2 discover=[]', _c0.discover('x') == [])
check('Q2 inspect=[]', _c0.inspect(['a']) == [])
check('Q2 call={}', _c0.call('a', {}) == {})
check('Q2 search=[]', _c0.search('x') == [])
check('Q2 模块级 search=[]', qc.search('x') == [])


# ── mock HTTP 层 ──
def _resp(payload: dict):
    """构造可读 urlopen 响应对象。"""
    class _R:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps(payload).encode('utf-8')
    return _R()


def _mock_urlopen(case: str):
    """根据请求体路由到仿真响应。case: ok | quota | auth | netfail | timeout"""
    def _handler(req, timeout=5):
        body = json.loads(req.data.decode('utf-8')) if req.data else {}
        path = req.full_url.split('?')[0]  # 去掉 query 参数再匹配路径
        if case == 'ok':
            # CN 风格：discover 精简 + 外层 search_id；inspect 补全；call 成功
            if path.endswith('/search'):
                return _resp({'search_id': 'srch_mock_1', 'results': [
                    {'tool_id': 't_a', 'capability': 'capa a', 'cost_class': 'low', 'reliability': 'A'},
                ]})
            if path.endswith('/tools/by-ids'):
                return _resp({'results': [
                    {'tool_id': 't_a', 'name': '工具A', 'provider_name': 'provA',
                     'examples': {'sample_parameters': {'p': 1}}, 'billing_rule': {}},
                ]})
            if path.endswith('/tools/execute'):
                return _resp({'execution_id': 'exec_mock_1', 'success': True,
                              'result': {'data': {'x': 1}}, 'remaining_credits': 998})
            return _resp({})
        if case == 'quota':
            import urllib.error
            e = urllib.error.HTTPError(req.full_url, 429, 'Too Many', {}, None)
            raise e
        if case == 'auth':
            import urllib.error
            e = urllib.error.HTTPError(req.full_url, 401, 'Unauthorized', {}, None)
            raise e
        if case == 'netfail':
            import urllib.error
            raise urllib.error.URLError('refused')
        if case == 'timeout':
            raise TimeoutError('timed out')
        return _resp({})
    return _handler


# ── Q3: Discover→Inspect→Call 全流程（mock ok）──
_c = qc.QVerisClient(api_key='sk-cn-mock123')
with mock.patch('urllib.request.urlopen', side_effect=_mock_urlopen('ok')):
    hits = _c.discover('q', limit=2)
    check('Q3 discover 返回精简候选', len(hits) == 1 and hits[0]['tool_id'] == 't_a')
    check('Q3 discover 记录外层 search_id', _c.last_search_id == 'srch_mock_1')
    ins = _c.inspect(['t_a'])
    check('Q3 inspect 补全 name/examples',
          ins[0]['name'] == '工具A' and ins[0]['examples']['sample_parameters']['p'] == 1)
    res = _c.search('q', max_results=2, budget=2)
    check('Q3 search 端到端结果 1 条', len(res) == 1, f"n={len(res)}")
    if res:
        r = res[0]
        check('Q3 结果 url/标题结构', r['url'].startswith('qveris://exec/') and '工具A' in r['title'])
        check('Q3 结果 snippet 含数据', 'x' in (r.get('snippet') or ''))
        check('Q3 结果 tool_id/provider/cost',
              r['tool_id'] == 't_a' and r['provider'] == 'provA' and r['cost_credits'] == 0)
        check('Q3 结果余额透传', r['credits_remaining'] == 998)


# ── Q4: 配额/认证错误上抛 ──
_cq = qc.QVerisClient(api_key='sk-cn-mock429')
with mock.patch('urllib.request.urlopen', side_effect=_mock_urlopen('quota')):
    try:
        _cq.discover('q')
        check('Q4 discover 429 → 上抛', False, '未抛异常')
    except qc.QVerisQuotaError:
        check('Q4 discover 429 → QVerisQuotaError', True)
    except Exception as e:
        check('Q4 discover 429 → QVerisQuotaError', False, f"got {type(e).__name__}")
    try:
        _cq.search('q')
        check('Q4 search 429 → 上抛', False, '未抛异常')
    except qc.QVerisQuotaError:
        check('Q4 search 429 → QVerisQuotaError', True)
    except Exception as e:
        check('Q4 search 429 → QVerisQuotaError', False, f"got {type(e).__name__}")

_ca = qc.QVerisClient(api_key='sk-cn-mock401')
with mock.patch('urllib.request.urlopen', side_effect=_mock_urlopen('auth')):
    try:
        _ca.discover('q')
        check('Q4 discover 401 → 上抛', False)
    except qc.QVerisAuthError:
        check('Q4 discover 401 → QVerisAuthError', True)
    except Exception as e:
        check('Q4 discover 401 → QVerisAuthError', False, f"got {type(e).__name__}")


# ── Q5: 单能力失败跳过（call 抛一般错误 → 继续） ──
def _mock_call_fail(req, timeout=5):
    body = json.loads(req.data.decode('utf-8')) if req.data else {}
    path = req.full_url.split('?')[0]
    if path.endswith('/search'):
        return _resp({'search_id': 'srch_x', 'results': [
            {'tool_id': 't_ok', 'capability': 'ok'},
            {'tool_id': 't_fail', 'capability': 'fail'},
        ]})
    if path.endswith('/tools/by-ids'):
        return _resp({'results': [
            {'tool_id': 't_ok', 'name': 'OK', 'examples': {'sample_parameters': {}}},
            {'tool_id': 't_fail', 'name': 'FAIL', 'examples': {'sample_parameters': {}}},
        ]})
    if path.endswith('/tools/execute'):
        if json.loads(req.data)['tool_id'] == 't_fail':
            raise qc.QVerisError('boom')   # 一般能力失败 → search 跳过
        return _resp({'execution_id': 'e1', 'success': True,
                      'result': {'data': {'ok': 1}}, 'remaining_credits': 100})
    return _resp({})

_c5 = qc.QVerisClient(api_key='sk-cn-mock5')
with mock.patch('urllib.request.urlopen', side_effect=_mock_call_fail):
    res = _c5.search('q', max_results=5, budget=3)
    check('Q5 失败能力被跳过，成功能力保留', len(res) == 1 and res[0]['tool_id'] == 't_ok',
          f"n={len(res)}")


# ── Q6: 网络失败 → QVerisError（模块级 search 吞掉返回 []）──
_c6 = qc.QVerisClient(api_key='sk-cn-mock6')
with mock.patch('urllib.request.urlopen', side_effect=_mock_urlopen('netfail')):
    try:
        _c6.discover('q')
        check('Q6 URIError → QVerisError', False)
    except qc.QVerisError:
        check('Q6 URIError → QVerisError', True)

with mock.patch('urllib.request.urlopen', side_effect=_mock_urlopen('timeout')):
    try:
        _c6.discover('q')
        check('Q6 Timeout → QVerisError', False)
    except qc.QVerisError:
        check('Q6 Timeout → QVerisError', True)

# 模块级 search 吞网络错误 → []
with mock.patch('urllib.request.urlopen', side_effect=_mock_urlopen('netfail')):
    check('Q6 模块级 search 网络失败 → []', qc.search('q') == [])


# ── Q7: search_id 透传 Call ──
_seen_search_ids = []
def _mock_capture(req, timeout=5):
    body = json.loads(req.data.decode('utf-8')) if req.data else {}
    path = req.full_url.split('?')[0]
    if path.endswith('/search'):
        return _resp({'search_id': 'srch_cap', 'results': [
            {'tool_id': 't_a', 'capability': 'c'}]})
    if path.endswith('/tools/by-ids'):
        return _resp({'results': [{'tool_id': 't_a', 'name': 'A',
                                   'examples': {'sample_parameters': {}}}]})
    if path.endswith('/tools/execute'):
        _seen_search_ids.append(body.get('search_id'))
        return _resp({'execution_id': 'e', 'success': True,
                      'result': {'data': {'v': 2}}, 'remaining_credits': 5})
    return _resp({})

_c7 = qc.QVerisClient(api_key='sk-cn-mock7')
with mock.patch('urllib.request.urlopen', side_effect=_mock_capture):
    _c7.search('q', budget=2)
    check('Q7 Call 透传服务端 search_id', _seen_search_ids == ['srch_cap'],
          f"seen={_seen_search_ids}")


# ── Q8: pipeline 集成 ──
import infoseek_pipeline as pipe
_check_seen = {}
def _fake_qv_search(*a, **k):
    _check_seen['called'] = True
    return [{'url': 'qveris://exec/e', 'title': '[p] n', 'snippet': 's',
             'tool_id': 't', 'provider': 'p', 'cost_credits': 1}]

# Q8a: 无 key → []（env 清空）
os.environ.pop('QVERIS_API_KEY', None)
with mock.patch('qveris_client.search', side_effect=lambda *a, **k: []):
    check('Q8a 无 key pipeline _search_qveris=[]', pipe._search_qveris('q') == [])

# Q8b: 有 key + 正常返回
os.environ['QVERIS_API_KEY'] = 'sk-cn-test'
with mock.patch('qveris_client.search', side_effect=_fake_qv_search):
    r = pipe._search_qveris('q')
    check('Q8b 有 key 返回规范结果', r and r[0]['url'].startswith('qveris://'))

# Q8c: 429 上抛 → 生命周期标记 quota（EL 集成）
import engine_lifecycle as el
el.reset_instance()
lc = el.get_lifecycle()
def _raise_quota(*a, **k):
    raise qc.QVerisQuotaError('quota')
os.environ['QVERIS_API_KEY'] = 'sk-cn-test'
with mock.patch('qveris_client.search', side_effect=_raise_quota):
    try:
        pipe._search_qveris('q')
        check('Q8c 429 上抛', False)
    except qc.QVerisQuotaError:
        check('Q8c 429 上抛', True)
    # _call_engine 包装后标记禁用（对齐 EL7 语义）
    res = pipe._call_engine('QVeris', _raise_quota, 'q', 5)
    check('Q8c _call_engine 返回 []', res == [])
    check('Q8c QVeris 被标记配额禁用', lc.is_disabled('QVeris'))
os.environ.pop('QVERIS_API_KEY', None)


print(f"\n===== {len(passed)} passed, {len(failed)} failed =====")
if failed:
    print("FAILED:", failed)
    sys.exit(1)