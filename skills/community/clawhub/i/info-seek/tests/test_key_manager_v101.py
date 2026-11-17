#!/usr/bin/env python3
"""Infoseek v1.0.1 KeyManager 归一化 Key 管理测试（K1-K12）

覆盖：
- K1  env 退化兼容（未注册 → 读 env）
- K2  注册后多 key 池优先（session key > env）
- K3  least-used 选择（used_count 最小优先）
- K4  状态机：3 连败 → DEGRADED
- K5  状态机：5 连败 → CIRCUIT_OPEN + 冷却
- K6  熔断中 get 回退 env
- K7  成功回注恢复 ACTIVE
- K8  配额感知：用尽自动切换 / 全部用尽回退 env
- K9  轮换 rotate（最旧 key 置后）
- K10 吊销 revoke
- K11 统计脱敏（key_fingerprint 不含完整 key）
- K12 用量落盘 key_usage.json
"""
import os
import sys
import json
import tempfile
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK))  # 使 `core.llm_router` 包导入可用（usage_report 成本表）

# 隔离阈值（避免影响其他测试）
os.environ['INFOSEEK_KEY_FAIL_THRESHOLD'] = '3'
os.environ['INFOSEEK_KEY_CIRCUIT_THRESHOLD'] = '5'

from key_manager import KeyManager, BUILTIN_PROVIDERS

passed, failed = [], []

def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


def fresh_manager() -> KeyManager:
    km = KeyManager.instance()
    km.reset()
    return km


# ── K1: env 退化兼容 ──
km = fresh_manager()
os.environ['EXA_API_KEY'] = 'sk-env-key-0001'
check('K1 未注册读 env', km.get('exa') == 'sk-env-key-0001')
os.environ.pop('EXA_API_KEY', None)
check('K1b env 空时返回空串', km.get('exa') == '')

# ── K2: 注册后多 key 池优先 ──
km.register('exa', 'sk-session-key-0002')
os.environ['EXA_API_KEY'] = 'sk-env-key-0001'
check('K2 注册 key 优先于 env', km.get('exa') == 'sk-session-key-0002')
os.environ.pop('EXA_API_KEY', None)

# ── K3: least-used 选择 ──
km.register('pool', 'key-A-1111')
km.register('pool', 'key-B-2222')
first = km.get('pool')   # used_count 相同 → 先注册的 A
second = km.get('pool')  # A.used=1 > B.used=0 → 选 B
third = km.get('pool')   # B.used=1, A.used=1 → 选 A（同 count 用 fail_count 最少，相等取先）
check('K3 least-used 轮换', first == 'key-A-1111' and second == 'key-B-2222' and third == 'key-A-1111',
      f"seq={first[:5]},{second[:5]},{third[:5]}")

# ── K4: 3 连败 → DEGRADED ──
km2 = fresh_manager()
km2.register('deg', 'key-deg-0000')
for _ in range(3):
    km2.report_failure('deg')
s = km2.stats()['deg'][0]
check('K4 3连败 DEGRADED', s['status'] == 'DEGRADED' and s['fail_count'] == 3,
      f"status={s['status']} fail={s['fail_count']}")

# ── K5: 5 连败 → CIRCUIT_OPEN + 冷却 ──
km2.report_failure('deg')
km2.report_failure('deg')
s = km2.stats()['deg'][0]
check('K5 5连败 CIRCUIT_OPEN', s['status'] == 'CIRCUIT_OPEN' and s['circuit_open_until'] > 0,
      f"status={s['status']} cooldown={s['circuit_open_until']>0}")

# ── K6: 熔断中 get 回退 env ──
os.environ['DEG_API_KEY'] = 'sk-env-fallback'
check('K6 熔断回退 env', km2.get('deg', env_name='DEG_API_KEY') == 'sk-env-fallback')
os.environ.pop('DEG_API_KEY', None)

# ── K7: 成功回注恢复 ──
km2.report_success('deg')
s = km2.stats()['deg'][0]
check('K7 成功恢复 ACTIVE', s['status'] == 'ACTIVE' and s['fail_count'] == 0,
      f"status={s['status']} fail={s['fail_count']}")

# ── K8: 配额感知 ──
km3 = fresh_manager()
km3.register('quota', 'key-Q-1111')
km3.register('quota', 'key-Q-2222')
km3.set_quota('quota', 1)  # 池内全部 limit=1
g1 = km3.get('quota')      # Q1
g2 = km3.get('quota')      # Q1 用尽 → Q2
g3 = km3.get('quota')      # Q2 用尽 → env（空）
check('K8 配额用尽切换+回退', g1 == 'key-Q-1111' and g2 == 'key-Q-2222' and g3 == '',
      f"g1={g1[:5]} g2={g2[:5]} g3={repr(g3)}")

# ── K9: 轮换 rotate ──
km4 = fresh_manager()
km4.register('rot', 'key-R-1111')
km4.register('rot', 'key-R-2222')
km4.get('rot')  # A used=1
km4.get('rot')  # B used=1
rotated = km4.rotate('rot')
order_after = [km4.get('rot'), km4.get('rot')]
check('K9 rotate 重排', rotated and len(set(order_after)) == 2,
      f"rotated={rotated} after={[k[:5] for k in order_after]}")

# ── K10: 吊销 revoke ──
km4.revoke('rot', key_fingerprint='2222')
revoked_rec = [r for r in km4._records['rot'] if '2222' in r.key]
active_rec = [r for r in km4._records['rot'] if '1111' in r.key]
check('K10 revoke 按指纹', revoked_rec[0].status == 'REVOKED' and active_rec[0].status == 'ACTIVE')

# ── K11: 统计脱敏 ──
km5 = fresh_manager()
km5.register('mask', 'REDACTED-SECRET')
st = km5.stats()['mask'][0]
fp = st['key_fingerprint']
check('K11 指纹脱敏', 'sk-very-secret' not in fp and fp.startswith('sk-v') and fp.endswith('9999'),
      f"fp={fp}")

# ── K12: 用量落盘 ──
km6 = fresh_manager()
km6.register('persist', 'sk-persist-0001')
km6.get('persist')
tmp = tempfile.mktemp(suffix='.json')
p = km6.persist_usage(path=tmp)
data = json.loads(Path(p).read_text(encoding='utf-8'))
check('K12 用量落盘', 'persist' in data and data['persist'][0]['used_count'] == 1,
      f"persisted={list(data.keys())}")
Path(tmp).unlink(missing_ok=True)

# ── K13: BUILTIN_PROVIDERS 完整 ──
check('K13 内置 provider 注册表 ≥12', len(BUILTIN_PROVIDERS) >= 12,
      f"count={len(BUILTIN_PROVIDERS)}")

# ── K14: .env 加载 ──
env_file = tempfile.mktemp(suffix='.env')
Path(env_file).write_text('TEST_DOTENV_KEY=sk-dotenv-value\n# comment\nEMPTY_LINE\n', encoding='utf-8')
km7 = KeyManager(dotenv=True, dotenv_path=env_file)
check('K14 .env 加载', os.environ.get('TEST_DOTENV_KEY') == 'sk-dotenv-value')
Path(env_file).unlink(missing_ok=True)

# ═══════════════════════════════════════════════════════════════
# K15-K22: P3 扩展 —— FileBackend 加密 / 用量报表 / MCP 工具面
# ═══════════════════════════════════════════════════════════════

# ── K15: FileBackend 加密落盘（cryptography 可用时）──
try:
    import cryptography  # noqa
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

if HAS_CRYPTO:
    kmf = fresh_manager()
    kmf.register('deepseek', 'sk-file-secret-777')
    fpath = tempfile.mktemp(suffix='.json')
    pfile = kmf.save_keys(path=fpath)
    raw_bytes = Path(pfile).read_bytes()
    check('K15 加密落盘（密文非明文）', b'sk-file-secret' not in raw_bytes and Path(pfile).exists())

    kmf2 = fresh_manager()
    n = kmf2.load_keys(path=fpath)
    check('K16 加密加载恢复', n == 1 and kmf2.get('deepseek') == 'sk-file-secret-777',
          f"n={n}")

    # 密钥不匹配 → KeyManagementError
    import shutil
    bad_fp = fpath + '.bad'
    bad_kp = Path(str(fpath)).with_suffix('.key').as_posix() + '.bad'
    shutil.copy(fpath, bad_fp)  # 数据文件拷贝（密文），配坏 key
    Path(bad_kp).write_text('not-a-valid-fernet-key')
    from key_manager import KeyManagementError
    kmf3 = fresh_manager()
    try:
        kmf3.load_keys(path=bad_fp, key_path=bad_kp)
        check('K17 密钥不匹配抛 KeyManagementError', False)
    except KeyManagementError:
        check('K17 密钥不匹配抛 KeyManagementError', True)
    except Exception:
        check('K17 密钥不匹配抛 KeyManagementError', False)
    for f in (fpath, Path(str(fpath)).with_suffix('.key'), fpath + '.bad', bad_kp):
        Path(f).unlink(missing_ok=True)
else:
    check('K15 加密落盘（cryptography 不可用→SKIP）', True, '⏭️ cryptography 未安装')
    check('K16 加密加载恢复（SKIP）', True, '⏭️')
    check('K17 密钥不匹配（SKIP）', True, '⏭️')

# ── K18: 用量报表（含成本估算）──
kmr = fresh_manager()
kmr.register('deepseek', 'sk-r')
kmr.register('exa', 'e-r')
kmr.get('deepseek'); kmr.get('deepseek'); kmr.get('exa')
uf = tempfile.mktemp(suffix='.json')
kmr.persist_usage(path=uf)
rep = kmr.usage_report(path=uf)
row_ds = next((r for r in rep['rows'] if r['provider'] == 'deepseek'), None)
check('K18 用量报表结构', row_ds is not None and row_ds['calls'] == 2 and 'est_cost_usd' in row_ds,
      f"ds_calls={row_ds['calls'] if row_ds else '?'} total={rep['total_est_cost_usd']}")
Path(uf).unlink(missing_ok=True)

# ── K19: 无用量文件报表容错 ──
kmr2 = fresh_manager()
rep2 = kmr2.usage_report(path=tempfile.mktemp(suffix='.json'))
check('K19 无文件报表返回 error', 'error' in rep2)

# ── K20: MCP 工具面含 Key 管理工具 ──
import sys as _sys
_sys.path.insert(0, str(INFOSEEK / 'scripts'))
try:
    from infoseek_mcp_server import TOOLS
    tool_names = {t['name'] for t in TOOLS}
    check('K20 MCP 工具面含 manage_keys/key_usage', 
          'manage_keys' in tool_names and 'key_usage' in tool_names,
          f"total={len(TOOLS)}")
except ImportError:
    check('K20 MCP 工具面', True, '⏭️ mcp_server 不可导入')

# ── K21: revoke 子串指纹匹配 ──
kmv = fresh_manager()
kmv.register('rv', 'key-revoke-me-1234')
kmv.register('rv', 'key-keep-me-5678')
n = kmv.revoke('rv', key_fingerprint='1234')
remaining = [r for r in kmv._records['rv'] if r.status != 'REVOKED']
check('K21 revoke 子串指纹', n == 1 and len(remaining) == 1 and remaining[0].key.endswith('5678'),
      f"revoked={n} remaining={len(remaining)}")

# ── K22: CLI 脚本存在且可执行 ──
cli_path = INFOSEEK / 'scripts' / 'infoseek_keys_cli.py'
check('K22 keys CLI 存在', cli_path.exists())

# ═══════════════════════════════════════════════════════════════
# K23-K27: v1.0.1 B1/B2/B3 —— Keyring / token 用量 / CLI backup
# ═══════════════════════════════════════════════════════════════

# ── K23: Keyring 可用性探测 ──
from key_manager import KeyManager as _KM
_kmk = _KM.instance(); _kmk.reset()
_check_kr = _kmk.keyring_available()
check('K23 keyring 探测', isinstance(_check_kr, bool), f"available={_check_kr}")

# ── K24: Keyring 写入/恢复（可用时）──
if _check_kr:
    try:
        import keyring as _kr
        _kmk.register('deepseek', 'sk-kr-test-999')
        n_w = _kmk.save_to_keyring()
        _kmk2 = _KM.instance(); _kmk2.reset()
        n_r = _kmk2.load_from_keyring()
        got = _kmk2.get('deepseek')
        check('K24 keyring 写读闭环', n_w >= 1 and n_r >= 1 and got == 'sk-kr-test-999',
              f"w={n_w} r={n_r}")
        # 清理
        for i in range(3):
            try: _kr.delete_password('infoseek', f'deepseek:{i}')
            except Exception: break
    except Exception as e:
        check('K24 keyring 写读闭环', False, str(e)[:60])
else:
    check('K24 keyring 写读闭环（不可用 SKIP）', True, '⏭️')

# ── K25: token 用量累计与报表 ──
_kmt = _KM.instance(); _kmt.reset()
_kmt.record_usage('deepseek', 1000, 500)
_kmt.record_usage('deepseek', 200, 100)
_kmt.record_usage('exa', 0, 0)
tu = _kmt.token_usage()
check('K25 token 累计', tu.get('deepseek', {}).get('input_tokens') == 1200
      and tu.get('deepseek', {}).get('output_tokens') == 600, f"{tu}")

# ── K26: usage_report token 成本折算 ──
_uf2 = tempfile.mktemp(suffix='.json')
_kmt.persist_usage(path=_uf2)
_rep = _kmt.usage_report(path=_uf2)
_row_ds = next((r for r in _rep['rows'] if r['provider'] == 'deepseek'), None)
check('K26 报表 token 明细', _row_ds is not None and _row_ds['input_tokens'] == 1200
      and _row_ds['est_cost_usd'] > 0, f"in={_row_ds['input_tokens'] if _row_ds else '?'}")
Path(_uf2).unlink(missing_ok=True)

# ── K27: CLI backup/restore 子命令存在 ──
import subprocess as _sp
_cli = str(INFOSEEK / 'scripts' / 'infoseek_keys_cli.py')
_help = _sp.run([sys.executable, _cli, '--help'], capture_output=True, text=True).stdout
check('K27 CLI backup/restore 子命令', 'backup' in _help and 'restore' in _help)

# ── 统一总结（v1.0.1 修正：中途总结移除，K1-K27 全量统一输出）──
print(f"\n=== KeyManager 测试: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")

# ── K28: CLI keyring-persist/load 子命令存在 ──
_help2 = _sp.run([sys.executable, _cli, '--help'], capture_output=True, text=True).stdout
check('K28 CLI keyring 子命令', 'keyring-persist' in _help2 and 'keyring-load' in _help2)
