# -*- coding: utf-8 -*-
"""
test_consent_cli_v210.py — 能力授权 consent CLI 端到端守护（v2.1.0）

闭合 ROADMAP P1#3：验证 list/grant/revoke/doctor/shell-init 与审计落盘，
全程内存注册表 + 临时审计日志，不触碰真实长期授权、不发起网络。
"""
import os
import sys
import tempfile
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, '..', 'scripts'))
sys.path.insert(0, os.path.join(_HERE, '..'))

from core import capability_registry as cr
import infoseek_consent_cli as cli

_PASS = 0
_FAIL = 0


def check(name, cond, detail=''):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
    print(('[PASS] ' if cond else '[FAIL] ') + name + (f'  ({detail})' if detail else ''))


# 临时审计日志隔离
_tmp = tempfile.TemporaryDirectory()
os.environ['INFOSEEK_DATA_DIR'] = _tmp.name
cr.reload()

_ENABLED = {
    'version': 1,
    'capabilities': [
        {'name': 'Maigret', 'kind': 'identity_attribution', 'enabled': False,
         'requires_consent': True, 'degrade_to': ['Sherlock', 'manual_review']},
        {'name': 'Sherlock', 'kind': 'identity_attribution', 'enabled': False,
         'requires_consent': True, 'degrade_to': ['manual_review']},
        {'name': 'manual_review', 'kind': 'graceful_fallback', 'enabled': True,
         'requires_consent': False, 'degrade_to': []},
    ],
}
cr._cache = dict(_ENABLED)

# 1) list 能展示三个能力（不抛、含表头数据）
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cli.main(['list', '--kind', 'identity_attribution'])
out = buf.getvalue()
check('list rc=0', rc == 0)
check('list 含 Maigret/Sherlock', 'Maigret' in out and 'Sherlock' in out, out[:80])
check('list 默认 effective=no', out.count('no') >= 1)

# 2) grant 未知能力 → rc=2
check('grant 未知能力 rc=2', cli.main(['grant', 'Nope']) == 2)
check('revoke 未知能力 rc=2', cli.main(['revoke', 'Nope']) == 2)

# 3) grant 合法能力 → consent 生效 + 审计落盘 + 输出 export 行
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cli.main(['grant', 'Sherlock'])
gout = buf.getvalue()
check('grant Sherlock rc=0', rc == 0)
check('grant 后 consent_granted=True', cr.consent_granted('Sherlock'))
check('grant 输出含 export 引导', 'INFOSEEK_ENABLE_SHERLOCK=1' in gout, gout[:120])
logp = cr.consent_log_path()
check('grant 审计落盘', logp and Path(logp).exists()
      and 'grant Sherlock' in Path(logp).read_text(encoding='utf-8'), logp)

# 4) revoke → consent 清除 + 审计记录
with contextlib.redirect_stdout(io.StringIO()):
    rc = cli.main(['revoke', 'Sherlock'])
check('revoke Sherlock rc=0', rc == 0)
check('revoke 后 consent_granted=False', not cr.consent_granted('Sherlock'))
check('revoke 审计落盘',
      'revoke Sherlock' in Path(logp).read_text(encoding='utf-8'))

# 5) doctor 不抛且含默认 OFF 能力
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cli.main(['doctor'])
dout = buf.getvalue()
check('doctor rc=0 且列 Maigret', rc == 0 and 'Maigret' in dout)
check('doctor 给出授权步骤', 'INFOSEEK_ENABLE_MAIGRET' in dout)

# 6) shell-init 在无 env 时不启用任何能力
for k in list(os.environ):
    if k.startswith('INFOSEEK_ENABLE_'):
        os.environ.pop(k)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cli.main(['shell-init'])
sout = buf.getvalue()
check('shell-init rc=0', rc == 0 and 'eval' in sout)

# 7) env 名推导（无自定义 env_var 时自动大写）
check('env 名推导 Sherlock', cli._env_name('Sherlock') == 'INFOSEEK_ENABLE_SHERLOCK')

cr._cache = None
_tmp.cleanup()
print(f'\n=== consent CLI 测试: {_PASS} PASS / {_FAIL} FAIL ===')
sys.exit(1 if _FAIL else 0)
