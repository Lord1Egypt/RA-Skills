#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_forensics_v160.py — FakeDetect 账号取证融入集成测试（v1.6.0 · A1/A2/C1/C2/C3/B1 全链路）

覆盖（融入方案 A+B+C 与 ROADMAP §6.7）：
  F1 [A1] 注册表：FakeDetect 注册（kind=account_forensics / enabled=False / requires_consent=True
      / weight=0.85 / degrade_to=[AccountTrustScorer, manual_review] / env_var=INFOSEEK_ENABLE_FAKE_DETECT）
  F2 [A1] 双源一致性：capabilities/registry.yaml 与 _DEFAULT_REGISTRY 字段一致
  F3 [A1] 闸门：默认 OFF；env 闸；consent 闸；env+consent 双闸生效（is_effective_enabled）
  F4 [A1] 降级链：degrade_chain(FakeDetect) = [FakeDetect, AccountTrustScorer, manual_review]
  F5 [A2] 信号门控：pipeline 自动路径（无深度信号）→ AccountTrustScorer（行为不变）
  F6 [A2] 信号门控：深度信号（时序/图谱）→ FakeDetect 路径 + forensics 明细
  F7 [A2] 信号门控：FakeDetect 关闭时深度账号原样走 ATS（零替代风险）
  F8 [C1] 引擎函数化：detect(dataset) -> Report 输出契约（status/sufficiency/verdicts/
      coord_clusters/sync_groups/summary/degradation/blindspots/meta）
  F9 [C1] 充分性门控：信号不足 → degraded insufficient_signals（缺数据≠水军）
  F10 [C1] 盲区断言：BLINDSPOTS 声明 G3(漏检~75%)/G4(漏检~67%)
  F11 [C2] 合规审计：深度取证路径审计落盘 [account_forensics] 前缀
  F12 [B1] MCP 注册：TOOLS 含 account_forensics + canonical 保留
  F13 [B1] MCP 合规：未启用 → blocked disabled / consent=False → blocked no_consent
  F14 [B1] MCP 全链：显式投喂数据 → ok + 四层命中 + target_accounts 过滤

全程不触碰真实凭据、不发起真实网络请求。
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'core'))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'extensions' / 'fake_detect'))

import numpy as np

from core import capability_registry as cr
import infoseek_mcp_server as m
from infoseek_pipeline import _verify_accounts, _account_deep_sufficient

# 环境隔离：清掉可能残留的闸门设置
os.environ.pop('INFOSEEK_ENABLE_FAKE_DETECT', None)
os.environ.pop('INFOSEEK_ENABLE_ACCOUNTTRUSTSCORER', None)
os.environ.pop('INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION', None)
cr.reload()
cr._consent_state.clear()

passed, failed = [], []


def check(name, cond, detail=''):
    if cond:
        passed.append(name)
        print(f"  [PASS] {name}" + (f"  ({detail})" if detail else ""))
    else:
        failed.append(name)
        print(f"  [FAIL] {name}" + (f"  ({detail})" if detail else ""))


def gen_deep_accounts(n_norm=30, n_bot=8, seed=5):
    """合成带深度信号账号（时序+ER+图），水军带尖峰涨粉+互关团。"""
    rng = np.random.RandomState(seed)
    accts = []
    for i in range(n_norm + n_bot):
        bot = i >= n_norm
        g = np.abs(rng.normal(2, 2, 120))
        if bot:
            for d in (15, 45, 75):
                g[d:d + 3] += 30
        accts.append({
            'username': f'u{i}', 'platform': 'x', 'followers': int(rng.randint(1000, 50000)),
            'following': int(rng.randint(50, 2000)), 'posts': 300,
            'er': round(float(rng.uniform(0.0005, 0.001) if bot else rng.uniform(0.01, 0.05)), 5),
            'likes_series': np.abs(rng.normal(50, 30, 120)).tolist(),
            'growth_series': np.round(g, 1).tolist(),
        })
    for a in range(n_norm, n_norm + n_bot):
        for b in range(a + 1, n_norm + n_bot):
            if rng.rand() < 0.5:
                accts[a].setdefault('edges', []).append((f'u{a}', f'u{b}'))
    return accts


print("=" * 70)
print("FakeDetect 账号取证融入测试（v1.6.0）")
print("=" * 70)

# ── F1 [A1] 注册表 ──
print("\n-- F1/F2/F3/F4: 能力注册与降级链 --")
cap = cr.get_capability('FakeDetect')
check("F1 注册存在", cap is not None)
if cap:
    check("F1 kind=account_forensics", cap.get('kind') == 'account_forensics')
    check("F1 enabled=False 默认 OFF", cap.get('enabled') is False)
    check("F1 requires_consent=True", cap.get('requires_consent') is True)
    check("F1 weight=0.85", abs(float(cap.get('weight', 0)) - 0.85) < 1e-9)
    check("F1 env_var=INFOSEEK_ENABLE_FAKE_DETECT",
          cap.get('env_var') == 'INFOSEEK_ENABLE_FAKE_DETECT')
    check("F1 degrade_to=[AccountTrustScorer, manual_review]",
          cap.get('degrade_to') == ['AccountTrustScorer', 'manual_review'])

# ── F2 [A1] 双源一致性 ──
try:
    import yaml
    y = yaml.safe_load((ROOT / 'capabilities' / 'registry.yaml').read_text(encoding='utf-8'))
    ycap = next(c for c in y['capabilities'] if c['name'] == 'FakeDetect')
    dr = next(c for c in cr._DEFAULT_REGISTRY['capabilities'] if c['name'] == 'FakeDetect')
    diff = {k for k in ('name', 'kind', 'enabled', 'requires_consent', 'weight',
                        'env_var', 'degrade_to') if ycap.get(k) != dr.get(k)}
    check("F2 registry.yaml 与 _DEFAULT_REGISTRY 一致", not diff, f"diff={diff}")
except Exception as e:
    check("F2 双源一致性", False, str(e))

# ── F3 [A1] 闸门 ──
check("F3 默认 OFF（is_effective_enabled=False）", not cr.is_effective_enabled('FakeDetect'))
os.environ['INFOSEEK_ENABLE_FAKE_DETECT'] = '1'
check("F3 env 闸开、consent 未授 → 仍 OFF", not cr.is_effective_enabled('FakeDetect'))
cr.grant_consent('FakeDetect')
check("F3 env+consent 双闸 → ON", cr.is_effective_enabled('FakeDetect'))
os.environ['INFOSEEK_ENABLE_FAKE_DETECT'] = '0'
cr.reload()
check("F3 env=0 覆盖 → OFF", not cr.is_effective_enabled('FakeDetect'))
os.environ['INFOSEEK_ENABLE_FAKE_DETECT'] = '1'
cr.reload()

# ── F4 [A1] 降级链 ──
chain = cr.degrade_chain('FakeDetect')
check("F4 降级链", chain == ['FakeDetect', 'AccountTrustScorer', 'manual_review'], str(chain))

# ── F5/F6/F7 [A2] 信号门控 ──
print("\n-- F5/F6/F7: _verify_accounts 信号门控 --")
os.environ['INFOSEEK_ENABLE_ACCOUNTTRUSTSCORER'] = '1'
cr.grant_consent('AccountTrustScorer')
cr.reload()

# F5: 无深度信号 → ATS（行为不变）
plain = [{'username': 'p1', 'platform': 'x'}, {'username': 'p2', 'platform': 'y'}]
out5 = _verify_accounts(plain)
check("F5 无深度信号 → AccountTrustScorer",
      all(a.get('verify_engine') == 'AccountTrustScorer' for a in out5),
      f"engines={[a.get('verify_engine') for a in out5]}")

# F6: 深度信号 + FakeDetect 双闸 → FakeDetect
deep = gen_deep_accounts()
out6 = _verify_accounts(deep)
eng6 = [a.get('verify_engine') for a in out6]
fd6 = sum(1 for e in eng6 if e == 'FakeDetect')
check("F6 深度账号全部走 FakeDetect", fd6 == len(deep), f"FD={fd6}/{len(deep)}")
if fd6 == len(deep):
    check("F6 输出契约（forensics 明细 + blindspots）",
          'forensics' in out6[0] and out6[0]['forensics'].get('blindspots')
          and out6[0].get('trust_score') is not None)
    bots = sum(1 for a in out6 if a.get('verdict') in ('bot', 'suspicious'))
    check("F6 水军检出≥6/8", bots >= 6, f"bot/suspicious={bots}/8")

# F7: FakeDetect 关闭 → 深度账号降级 ATS（零替代风险）
os.environ['INFOSEEK_ENABLE_FAKE_DETECT'] = '0'
cr.reload()
out7 = _verify_accounts(gen_deep_accounts())
check("F7 FakeDetect 关闭 → 深度账号仍 ATS（零替代风险）",
      all(a.get('verify_engine') == 'AccountTrustScorer' for a in out7))
os.environ['INFOSEEK_ENABLE_FAKE_DETECT'] = '1'
cr.reload()

# ── F8/F9/F10 [C1] 引擎函数化与充分性门控 ──
print("\n-- F8/F9/F10: 引擎 detect() 输出契约 / 充分性 / 盲区 --")
from fake_detect_engine import detect, assess_sufficiency, BLINDSPOTS, gen_demo_dataset
ds_full = gen_demo_dataset()
rep = detect(ds_full)
check("F8 Report 契约字段", all(k in rep for k in
      ('status', 'sufficiency', 'verdicts', 'coord_clusters', 'sync_groups',
       'summary', 'degradation', 'blindspots', 'meta')))
v0 = next(iter(rep['verdicts'].values()))
check("F8 verdict 契约", all(k in v0 for k in
      ('trust_score', 'verdict', 'verdict_cn', 'flags', 'layers')))
check("F8 summary 四层", all(k in rep['summary'] for k in ('l1', 'l2', 'sync', 'l3', 'gate')))
check("F8 demo 水军检出≥9/10",
      sum(1 for i in range(40, 50) if rep['verdicts'].get(str(i), {}).get('verdict')
          in ('bot', 'suspicious')) >= 9)
suf_ok = assess_sufficiency(ds_full)
check("F9 demo 充分性达标", suf_ok['sufficient'] is True)
# 不足场景：仅 username 级（Maigret 式产出）→ 降级
from data_adapter import from_raw
import pandas as pd
weak = from_raw(meta_df=pd.DataFrame({'id': list(range(20)), 'followers': [100] * 20,
                                      'following': [100] * 20, 'posts': [50] * 20, 'er': [0.0] * 20}))
rep_weak = detect(weak)
check("F9 信号不足 → insufficient_signals 降级（缺数据≠水军）",
      rep_weak['status'] == 'degraded' and rep_weak['degradation'] == 'insufficient_signals')
check("F10 盲区声明 G3/G4",
      len(BLINDSPOTS) >= 2 and any('G3' in b for b in BLINDSPOTS)
      and any('G4' in b for b in BLINDSPOTS))

# ── F11 [C2] 合规审计 ──
print("\n-- F11: 审计落盘 [account_forensics] 前缀 --")
from core.state_dir import audit_log_path
ap = audit_log_path()
before = open(ap, encoding='utf-8').read() if os.path.exists(ap) else ''
_verify_accounts(gen_deep_accounts(n_norm=10, n_bot=3, seed=9))
after = open(ap, encoding='utf-8').read() if os.path.exists(ap) else ''
check("F11 审计含 [account_forensics] 前缀", '[account_forensics]' in after[len(before):],
      "新审计行含前缀" if '[account_forensics]' in after[len(before):] else "未落盘")

# ── F12/F13/F14 [B1] MCP 工具 ──
print("\n-- F12/F13/F14: account_forensics MCP 工具 --")
names = {t['name'] for t in m.TOOLS if t['name'] in m._CANONICAL_TOOL_NAMES}
check("F12 canonical 含 account_forensics", 'account_forensics' in names)
from mcp_tools_forensics import tool_account_forensics
os.environ.pop('INFOSEEK_ENABLE_FAKE_DETECT', None)
cr.reload()
r13a = tool_account_forensics({'dataset': {'meta': [{'id': 1}]}, 'consent': True})
check("F13 未启用 → blocked/disabled", r13a.get('degradation') == 'disabled')
os.environ['INFOSEEK_ENABLE_FAKE_DETECT'] = '1'
cr.reload()
r13b = tool_account_forensics({'dataset': {'meta': [{'id': 1}]}, 'consent': False})
check("F13 consent=False → blocked/no_consent", r13b.get('degradation') == 'no_consent')
cr.grant_consent('FakeDetect')
ds_mcp = gen_demo_dataset()
meta = ds_mcp.meta_df.reset_index().to_dict('records') if False else \
    [{'id': int(i)} | {c: (float(ds_mcp.meta_df.loc[i, c]) if c == 'er'
                           else int(ds_mcp.meta_df.loc[i, c])) for c in ('followers', 'following', 'posts')}
     for i in ds_mcp.meta_df.index]
rm = tool_account_forensics({'dataset': {
    'meta': meta, 'likes': {str(k): v.tolist() for k, v in ds_mcp.likes.items()},
    'growth': {str(k): v.tolist() for k, v in ds_mcp.growth.items()},
    'edges': [[int(a), int(b)] for a, b in ds_mcp.G.edges()]}, 'consent': True})
check("F14 MCP 全链 status=ok", rm.get('status') == 'ok',
      f"deg={rm.get('degradation')} verdicts={rm.get('verdict_count')}")
check("F14 输出契约字段", all(k in rm for k in
      ('verdicts', 'coord_clusters', 'sync_groups', 'summary', 'sufficiency',
       'degradation', 'blindspots', 'meta')))
rt = tool_account_forensics({'dataset': {
    'meta': meta, 'likes': {str(k): v.tolist() for k, v in ds_mcp.likes.items()},
    'growth': {str(k): v.tolist() for k, v in ds_mcp.growth.items()},
    'edges': [[int(a), int(b)] for a, b in ds_mcp.G.edges()]},
    'target_accounts': ['40', '41'], 'consent': True})
check("F14 target_accounts 过滤", rt.get('verdict_count') == 2, f"count={rt.get('verdict_count')}")

# ── F15 [B3] 重训管道冒烟 ──
print("\n-- F15: 重训管道（B3）冒烟 --")
sys.path.insert(0, str(ROOT / 'scripts'))
from forensics_retrain import retrain_l1, build_feature_matrix, gen_adv_batch, cap_recall, ADV_LEVELS
l1r = retrain_l1(ds_full, verbose=False)
check("F15 L1 重训产出阈值与指标",
      'trained_thresholds' in l1r and 'holdout_trained' in l1r['metrics']
      and l1r['metrics']['holdout_trained']['fpr'] <= 0.02,
      f"holdout FPR={l1r['metrics']['holdout_trained']['fpr']}")
X, y, norm_ids = build_feature_matrix(ds_full)
Xa = gen_adv_batch(ADV_LEVELS[0], 20, seed=7, X_norm=X[norm_ids])
rec, fpr, t = cap_recall(np.clip(Xa[:, 1] / 0.05, 0, 1), np.ones(len(Xa)))
check("F15 对抗生成器 + CAP 指标", Xa.shape == (20, X.shape[1]) and 0 <= rec <= 1.0)
print("     对抗级别:", ADV_LEVELS)

# ── 汇总 ──
print("\n" + "=" * 70)
print(f"FakeDetect 融入测试: {len(passed)} passed / {len(failed)} failed")
print("=" * 70)
sys.exit(1 if failed else 0)