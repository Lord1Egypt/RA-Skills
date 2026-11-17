# -*- coding: utf-8 -*-
"""
test_identity_clients_v100.py — Maigret/Sherlock 身份归因客户端 + 代偿集成测试

验证：
  C1 默认 OFF：未启用时 search() 返回 []（不发任何请求）
  C2 合规闸口：启用但未授权 → 上抛 ConsentRequired
  C3 CLI 缺失信号：启用+授权但 CLI 不存在 → 上抛 CapabilityUnavailable
     （供 capability_compensator 捕获并降级到 Sherlock → manual_review）
  C4 Sherlock 同等行为（默认 OFF / ConsentRequired / Unavailable）
  C5 代偿集成：真实 Maigret 客户端作为 handler，CLI 缺失触发整条 degrade 链
     Maigret(不可用) → Sherlock(模拟成功) → 不触达 manual_review

v2.1.0（2026-09-18）加固：
  - 不再依赖「本机恰好没装 CLI」的环境偶然性（沙箱/CI 可能装了 maigret/sherlock，
    旧测试会发起真实网络扫描挂死）。统一用 monkeypatch 显式锁定路径：
      * C3/C4 把 _resolve_cli 指到不存在的可执行 → 稳定触发 CapabilityUnavailable；
      * C6/C7 注入假 subprocess.CompletedProcess + 临时报告文件，**零网络**验证
        真实 CLI 契约（argv 含 --csv/-J simple、解析真实 schema、username 回填）。
全程不触碰任何真实凭据、不发起真实网络请求。
"""
import os
import sys
import pathlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import subprocess
from core import capability_registry as cr
from core.capability_errors import ConsentRequired, CapabilityUnavailable
import maigret_client
import sherlock_client
from capability_compensator import compensate

# 隔离 env，避免测试间串扰
os.environ.pop('INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION', None)
os.environ.pop('INFOSEEK_IDENTITY_CONSENT', None)
# v2.2.0 加固：capability_registry._env_override() 会让 INFOSEEK_ENABLE_<CAP>
# 覆盖注册表声明（enabled:false → True）。若外部环境（如真实环境探测）遗留
# 这些 env，C1「默认 OFF」前提被静默破坏 → 显式锁定为「无 env 覆盖」的纯注册表默认态。
for _cap_env in ('INFOSEEK_ENABLE_MAIGRET',
                 'INFOSEEK_ENABLE_SHERLOCK',
                 'INFOSEEK_ENABLE_ACCOUNTTRUSTSCORER'):
    os.environ.pop(_cap_env, None)

_PASS = 0
_FAIL = 0


def check(name, cond, detail=''):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
    print(('[PASS] ' if cond else '[FAIL] ') + name + (f'  ({detail})' if detail else ''))
    return cond


# 启用状态的注册表缓存（绕过 default_off 以测合规/降级逻辑）
_ENABLED_CACHE = {
    'version': 1,
    'capabilities': [
        {'name': 'Maigret', 'kind': 'identity_attribution', 'enabled': True,
         'requires_consent': True, 'degrade_to': ['Sherlock', 'manual_review'],
         'health_probe': 'engine_lifecycle'},
        {'name': 'Sherlock', 'kind': 'identity_attribution', 'enabled': True,
         'requires_consent': True, 'degrade_to': ['manual_review'],
         'health_probe': 'engine_lifecycle'},
        {'name': 'manual_review', 'kind': 'graceful_fallback', 'enabled': True,
         'requires_consent': False, 'degrade_to': [], 'health_probe': 'none'},
    ],
}


def _with_enabled():
    cr._cache = dict(_ENABLED_CACHE)


def _reset():
    cr._cache = None
    cr.revoke_consent('Maigret')
    cr.revoke_consent('Sherlock')


# ── C1: 默认 OFF ──
r1 = maigret_client.search('someuser')
check('C1 Maigret 默认 OFF → 返回 []', r1 == [], f'got {r1!r}')
r1b = sherlock_client.search('someuser')
check('C1 Sherlock 默认 OFF → 返回 []', r1b == [], f'got {r1b!r}')

# ── C2: 合规闸口 ──
_with_enabled()
try:
    maigret_client.search('someuser', consent=False)
    check('C2 Maigret 未授权 → ConsentRequired', False)
except ConsentRequired:
    check('C2 Maigret 未授权 → ConsentRequired', True)
try:
    sherlock_client.search('someuser', consent=False)
    check('C2 Sherlock 未授权 → ConsentRequired', False)
except ConsentRequired:
    check('C2 Sherlock 未授权 → ConsentRequired', True)

# ── C3: CLI 缺失 → CapabilityUnavailable（注入不存在的 CLI，零网络）──
cr.grant_consent('Maigret')
_orig_m_cli = maigret_client._resolve_cli
maigret_client._resolve_cli = lambda: ['/nonexistent/infoseek_test_maigret_bin']
try:
    maigret_client.search('someuser', consent=True)
    check('C3 Maigret CLI 缺失 → CapabilityUnavailable', False, '未抛异常')
except CapabilityUnavailable:
    check('C3 Maigret CLI 缺失 → CapabilityUnavailable', True)
except Exception as e:  # noqa
    check('C3 Maigret CLI 缺失 → CapabilityUnavailable', False, f'误抛 {type(e).__name__}')
finally:
    maigret_client._resolve_cli = _orig_m_cli
_reset()

# ── C4: Sherlock CLI 缺失信号（注入不存在的 CLI，零网络）──
_with_enabled()
cr.grant_consent('Sherlock')
_orig_s_cli = sherlock_client._resolve_cli
sherlock_client._resolve_cli = lambda: ['/nonexistent/infoseek_test_sherlock_bin']
try:
    sherlock_client.search('someuser', consent=True)
    check('C4 Sherlock CLI 缺失 → CapabilityUnavailable', False, '未抛异常')
except CapabilityUnavailable:
    check('C4 Sherlock CLI 缺失 → CapabilityUnavailable', True)
except Exception as e:  # noqa
    check('C4 Sherlock CLI 缺失 → CapabilityUnavailable', False, f'误抛 {type(e).__name__}')
finally:
    sherlock_client._resolve_cli = _orig_s_cli
_reset()

# ── C5: 代偿集成（真实 Maigret handler 缺 CLI + 模拟 Sherlock 成功）──
_with_enabled()
cr.grant_consent('Maigret')
cr.grant_consent('Sherlock')


def _fake_sherlock(username, consent=None, timeout=120):
    # 模拟 Sherlock 可用并返回结构化结果
    return [{
        'platform': 'GitHub', 'username': username,
        'url': f'https://github.com/{username}',
        'confidence': 0.9, 'source': 'Sherlock',
    }]


handlers = {
    'Maigret': lambda u, **k: maigret_client.search(u, consent=True),
    'Sherlock': _fake_sherlock,
}
# 让 Maigret 稳定「CLI 缺失」，避免本机装了真 CLI 触发网络扫描
maigret_client._resolve_cli = lambda: ['/nonexistent/infoseek_test_maigret_bin']
res = compensate('Maigret', handlers, 'demo_user')
maigret_client._resolve_cli = _orig_m_cli
names = [t[0] for t in res.trail]
check('C5 代偿链 Maigret→Sherlock 接管', res.used == 'Sherlock', f'used={res.used}')
check('C5 代偿轨迹含 Maigret+Sherlock',
      'Maigret' in names and 'Sherlock' in names, f'trail={res.trail}')
check('C5 未触达 manual_review', 'manual_review' not in names,
      f'trail={res.trail}')
check('C5 结果为 Sherlock 产出',
      bool(res.result) and res.result[0].get('source') == 'Sherlock',
      f'result={res.result!r}')
_reset()


# ═══════════════════════════════════════════════════════════════
# C6/C7：v2.1.0 真实 CLI 契约守护（零网络，注入 subprocess + 报告文件）
# ═══════════════════════════════════════════════════════════════

class _FakeProc:
    def __init__(self, returncode=0, stdout='', stderr=''):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _run_cli_contract_case():
    """验证 sherlock/maigret search() 拼出的 argv 与报告解析（真实 schema）。"""
    import tempfile

    # ---- C6 Sherlock: argv 须含 --csv/--print-found；产出 <user>.csv ----
    captured = {}

    def fake_run_s(cmd, cwd=None, capture_output=True, text=True, timeout=None):
        captured['cmd'] = list(cmd)
        captured['cwd'] = cwd
        # 模拟 sherlock 在临时 cwd 写 CSV（真实列头）
        (pathlib.Path(cwd) / 'alice.csv').write_text(
            'username,name,url_main,url_user,exists,http_status,response_time_s\n'
            'alice,GitHub,https://www.github.com/,https://github.com/alice,Claimed,200,0.4\n'
            'alice,Gone,https://g.com/,https://g.com/alice,Available,404,0.9\n',
            encoding='utf-8')
        return _FakeProc(0, '[+] GitHub', '')

    _with_enabled(); cr.grant_consent('Sherlock')
    orig_run = subprocess.run
    subprocess.run = fake_run_s
    orig_cli = sherlock_client._resolve_cli
    sherlock_client._resolve_cli = lambda: ['sherlock']
    try:
        out = sherlock_client.search('alice', consent=True, timeout=30)
    finally:
        subprocess.run = orig_run
        sherlock_client._resolve_cli = orig_cli
        _reset()

    cmd = captured.get('cmd', [])
    check('C6 sherlock argv 用 --csv（非误用 --json）',
          '--csv' in cmd and '--json' not in cmd, f'cmd={cmd}')
    check('C6 sherlock argv 含 --print-found', '--print-found' in cmd)
    check('C6 sherlock 仅解析 Claimed 命中', len(out) == 1, f'out={out}')
    check('C6 sherlock username 回填（非空串）',
          bool(out) and out[0]['username'] == 'alice', f'out={out}')
    check('C6 sherlock 字段 platform/url/http_status',
          bool(out) and out[0]['platform'] == 'GitHub'
          and out[0]['url'] == 'https://github.com/alice'
          and out[0]['http_status'] == 200, f'out={out}')

    # ---- C7 Maigret: argv 须含 -J simple/--top-sites/--no-recursion；产出报告文件 ----
    captured2 = {}

    def fake_run_m(cmd, cwd=None, capture_output=True, text=True, timeout=None):
        captured2['cmd'] = list(cmd)
        reports = pathlib.Path(cwd) / 'reports'
        reports.mkdir(parents=True, exist_ok=True)
        import json as _json
        _json.dump({
            'GitHub': {'url_user': 'https://github.com/bob', 'username': 'bob',
                       'http_status': 200, 'rank': 10,
                       'status': {'username': 'bob', 'site_name': 'GitHub',
                                  'url': 'https://github.com/bob', 'status': 'Claimed',
                                  'ids': {}, 'tags': ['coding']}},
            'Empty': {'url_user': 'https://e.com/bob', 'username': 'bob',
                      'http_status': 404, 'rank': 999,
                      'status': {'username': 'bob', 'site_name': 'Empty',
                                 'url': 'https://e.com/bob', 'status': 'Available',
                                 'ids': {}, 'tags': []}},
        }, open(reports / 'report_bob_simple.json', 'w', encoding='utf-8'))
        return _FakeProc(0, '', '')

    _with_enabled(); cr.grant_consent('Maigret')
    subprocess.run = fake_run_m
    orig_mcli = maigret_client._resolve_cli
    maigret_client._resolve_cli = lambda: ['maigret']
    try:
        outm = maigret_client.search('bob', consent=True, timeout=30, max_sites=100)
    finally:
        subprocess.run = orig_run
        maigret_client._resolve_cli = orig_mcli
        _reset()

    cmdc = captured2.get('cmd', [])
    check('C7 maigret argv 用 -J simple（非旧式 --json flag）',
          ('-J' in cmdc and 'simple' in cmdc) and '--print-found-only' not in cmdc
          and '--skip-existing' not in cmdc, f'cmd={cmdc}')
    check('C7 maigret argv 限站点用 --top-sites（非 -a 全量）',
          '--top-sites' in cmdc and '-a' not in cmdc, f'cmd={cmdc}')
    check('C7 maigret argv 含 --no-recursion/--no-extracting',
          '--no-recursion' in cmdc and '--no-extracting' in cmdc, f'cmd={cmdc}')
    check('C7 maigret 仅解析嵌套 status.Claimed', len(outm) == 1, f'out={outm}')
    check('C7 maigret username/rank/tags 正确',
          bool(outm) and outm[0]['username'] == 'bob'
          and outm[0]['site_rank'] == 10 and outm[0]['tags'] == ['coding'],
          f'out={outm}')


_run_cli_contract_case()

# ── 汇总 ──
print(f'\n=== 身份归因客户端测试: {_PASS} PASS / {_FAIL} FAIL ===')
sys.exit(1 if _FAIL else 0)
