#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_identity_attribution_v150.py — 身份归因能力链 P0 消费侧集成测试（v1.5.0）

覆盖（T1 发现→验证闭环 / T2 MCP 工具 / T3 主链集成）：
  C1 [T1] _verify_accounts：AccountTrustScorer 启用+授权 → 附加 verdict/trust_score（真实评分）
  C2 [T1] _verify_accounts：AccountTrustScorer 未启用 → 原样返回（验证是增强不阻断）
  C3 [T2] MCP 注册：TOOLS 含 identity_attribution 且 schema 完整、canonical 保留
  C4 [T2] MCP 分发·未启用 → blocked（显式报错，非静默空）
  C5 [T2] MCP 分发·未授权（consent=False）→ blocked no_consent（显式报错）
  C6 [T2] MCP 分发·空 username → failed invalid_input
  C7 [T3] route_query·identity 未启用 → skipped-disabled → manual_review（无 skipped-identity-path）
  C8 [T3] route_query·identity 启用未授权 → skipped-no-consent → manual_review
  C9 [T3] route_query·identity 启用+授权+全链耗尽 → manual_review 缺口（不伪造数据）

全程不触碰真实凭据、不发起真实网络请求（CLI 缺失即短路降级）。
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'core'))
sys.path.insert(0, str(ROOT))

from core import capability_registry as cr
import infoseek_mcp_server as m
import tiered_router
from infoseek_pipeline import _verify_accounts

os.environ.pop('INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION', None)
os.environ.pop('INFOSEEK_IDENTITY_CONSENT', None)

passed, failed = [], []


def check(name, cond, detail=''):
    if cond:
        passed.append(name)
        print(f"  [PASS] {name}" + (f"  ({detail})" if detail else ""))
    else:
        failed.append(name)
        print(f"  [FAIL] {name}" + (f"  ({detail})" if detail else ""))


# ── 注册表注入：Maigret/Sherlock/AccountTrustScorer 全启用（测试用，绕过 default_off）──
_ENABLED_CACHE = {
    'version': 1,
    'capabilities': [
        {'name': 'Maigret', 'kind': 'identity_attribution', 'enabled': True,
         'requires_consent': True, 'degrade_to': ['Sherlock', 'manual_review'],
         'health_probe': 'engine_lifecycle'},
        {'name': 'Sherlock', 'kind': 'identity_attribution', 'enabled': True,
         'requires_consent': True, 'degrade_to': ['manual_review'],
         'health_probe': 'engine_lifecycle'},
        {'name': 'AccountTrustScorer', 'kind': 'identity_attribution', 'enabled': True,
         'requires_consent': True, 'degrade_to': ['manual_review'],
         'health_probe': 'none'},
        {'name': 'manual_review', 'kind': 'graceful_fallback', 'enabled': True,
         'requires_consent': False, 'degrade_to': [], 'health_probe': 'none'},
    ],
}


def _with_enabled(consent: bool = True):
    cr._cache = dict(_ENABLED_CACHE)
    if consent:
        for n in ('Maigret', 'Sherlock', 'AccountTrustScorer'):
            cr.grant_consent(n)


def _reset():
    cr._cache = None
    for n in ('Maigret', 'Sherlock', 'AccountTrustScorer'):
        cr.revoke_consent(n)
    os.environ.pop('INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION', None)


# ═══════════════════════════════════════════════════════════════
# C1/C2 — T1 发现→验证闭环
# ═══════════════════════════════════════════════════════════════
print("\n== C1/C2: T1 _verify_accounts 验证闭环 ==")
_reset()
_with_enabled(consent=True)
discovered = [
    {"username": "alice", "platform": "GitHub", "url": "https://github.com/alice",
     "confidence": 0.9, "source": "Maigret", "cross_platform_matches": 3},
    {"username": "bot1", "platform": "微博", "url": "https://weibo.com/bot1",
     "confidence": 0.8, "source": "Maigret", "cross_platform_matches": 0},
    {"platform": "(需人工核实)", "url": "", "username": "x", "_gap": True},
]
out = _verify_accounts(discovered)
_VALID_VERDICTS = {"real", "likely_real", "suspicious", "bot", "unknown"}
check("C1 验证闭环附加 verdict（合法枚举 + trust_score 数值）",
      out[0].get("verdict") in _VALID_VERDICTS and isinstance(out[0].get("trust_score"), (int, float)),
      f"verdict={out[0].get('verdict')} trust={out[0].get('trust_score')}")
check("C1 缺信号账号不误判真人（unknown 而非 real）",
      out[1].get("verdict") == "unknown", f"verdict={out[1].get('verdict')}")
check("C1 缺口标记原样透传（不评分 _gap 条目）", out[2].get("_gap") is True)
check("C1 不覆盖发现层 confidence", out[0].get("confidence") == 0.9)
check("C1 附加 trust_confidence", out[0].get("trust_confidence") is not None)

_reset()  # 移出授权（consent revoked）
with_enabled_no_ats = dict(_ENABLED_CACHE)
with_enabled_no_ats['capabilities'] = [c for c in _ENABLED_CACHE['capabilities']
                                       if c['name'] != 'AccountTrustScorer']
cr._cache = with_enabled_no_ats
cr.grant_consent('Maigret')
out2 = _verify_accounts(discovered)
check("C2 AccountTrustScorer 未启用 → 原样返回（不阻断）",
      len(out2) == 3 and out2[0].get("verdict") is None)


# ═══════════════════════════════════════════════════════════════
# C3 — T2 MCP 注册
# ═══════════════════════════════════════════════════════════════
print("\n== C3: T2 MCP 工具注册 ==")
_reset()
names = {t['name'] for t in m.TOOLS}
check("C3 TOOLS 含 identity_attribution", 'identity_attribution' in names)
entry = next((t for t in m.TOOLS if t['name'] == 'identity_attribution'), None)
check("C3 schema 完整（username 必填 + consent/max_results）",
      entry is not None
      and entry['inputSchema']['required'] == ['username']
      and 'consent' in entry['inputSchema']['properties']
      and 'max_results' in entry['inputSchema']['properties'])
check("C3 canonical 保留（非废弃）", 'identity_attribution' in m._CANONICAL_TOOL_NAMES)


# ═══════════════════════════════════════════════════════════════
# C4/C5/C6 — T2 MCP 分发（合规显式报错）
# ═══════════════════════════════════════════════════════════════
print("\n== C4/C5/C6: T2 MCP 分发合规闸 ==")
_reset()
r = m.tool_identity_attribution({"username": "alice"})
check("C4 未启用 → blocked disabled（显式报错）",
      r.get("status") == "blocked" and r.get("degradation") == "disabled",
      str(r.get("reason", ""))[:60])

os.environ['INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION'] = '1'
r = m.tool_identity_attribution({"username": "alice", "consent": False})
check("C5 未授权 → blocked no_consent（显式报错）",
      r.get("status") == "blocked" and r.get("degradation") == "no_consent",
      str(r.get("reason", ""))[:60])

r = m.tool_identity_attribution({"username": "  ", "consent": True})
check("C6 空 username → failed invalid_input",
      r.get("status") == "failed" and r.get("degradation") == "invalid_input")


# ═══════════════════════════════════════════════════════════════
# C7/C8/C9 — T3 主链集成（route_query identity 分支）
# ═══════════════════════════════════════════════════════════════
print("\n== C7/C8/C9: T3 route_query identity 接线 ==")
_reset()

# C7：未启用 → skipped-disabled → manual_review
r = tiered_router.route_query("查一下账号 alice", intent="identity")
trail = dict(r.get("trail", []))
check("C7 未启用 → Maigret skipped-disabled",
      trail.get("Maigret") == "skipped-disabled", str(dict(trail)))
check("C7 不再出现 skipped-identity-path",
      all(s != "skipped-identity-path" for _, s in r.get("trail", [])))
check("C7 末端 manual_review 缺口", r.get("used") == "manual_review" and r.get("exhausted") is True)

# C8：启用但未授权 → skipped-no-consent → manual_review
os.environ['INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION'] = '1'
_with_enabled(consent=False)
r = tiered_router.route_query("查一下账号 alice", intent="identity")
trail = dict(r.get("trail", []))
check("C8 启用未授权 → Maigret skipped-no-consent",
      trail.get("Maigret") == "skipped-no-consent", str(dict(trail)))
check("C8 末端 manual_review 缺口", r.get("used") == "manual_review" and r.get("exhausted") is True)

# C9：启用+授权+真实全链耗尽（注入缺失 CLI 稳定触发，零网络；不依赖环境是否装了 CLI）
_with_enabled(consent=True)
import maigret_client as _mc
import sherlock_client as _sc
_mc._resolve_cli = lambda: ['/nonexistent/infoseek_test_maigret_bin']
_sc._resolve_cli = lambda: ['/nonexistent/infoseek_test_sherlock_bin']
try:
    r = tiered_router.route_query("查一下账号 alice", intent="identity", consent=True)
    trail = dict(r.get("trail", []))
    check("C9 全链耗尽 → manual_review 缺口",
          r.get("used") == "manual_review" and r.get("exhausted") is True)
    check("C9 Maigret 尝试过真实调用（非 skipped）",
          trail.get("Maigret") in ("ok", "empty", "fail:CapabilityUnavailable"),
          str(trail.get("Maigret")))
finally:
    # 恢复 CLI 解析（不影响后续真实路径用例）
    import importlib
    importlib.reload(_mc)
    importlib.reload(_sc)

# C9b（v2.1.0）：双源聚合成功路径——注入双源假客户端，验证去重/交叉确认 + 路由成功
print("\n== C9b: v2.1.0 双源聚合成功路径 ==")
_with_enabled(consent=True)
import infoseek_pipeline as _pipe


def _fake_multi(username, consent=False, max_results=10):
    # 模拟两源「各自原始返回」（GitHub 同账号不同写法 + 各自独有平台），
    # 交给 pipeline 内真实 aggregate() 去重/交叉确认。
    from core.identity_aggregator import aggregate
    per_source = {
        "Maigret": [
            {"platform": "GitHub", "url": "https://github.com/alice", "username": username,
             "fullname": "", "site_rank": 10, "confidence": 0.9, "source": "Maigret",
             "http_status": 200, "tags": ["coding"]},
            {"platform": "WordPress", "url": "https://profiles.wordpress.org/alice/",
             "username": username, "site_rank": 12, "confidence": 0.9, "source": "Maigret",
             "http_status": 200},
        ],
        "Sherlock": [
            {"platform": "github", "url": "https://www.github.com/alice/", "username": username,
             "confidence": 0.85, "source": "Sherlock", "http_status": 200},
            {"platform": "Reddit", "url": "https://reddit.com/user/alice", "username": username,
             "confidence": 0.85, "source": "Sherlock", "http_status": 200},
        ],
    }
    agg = aggregate(per_source)
    return agg["accounts"], ["Maigret", "Sherlock"], [("Maigret", "ok:2"), ("Sherlock", "ok:2")]


_orig_collect = _pipe._collect_identity_multisource
_pipe._collect_identity_multisource = _fake_multi
try:
    anchors = _pipe.search_identity_attribution("alice", consent=True, max_results=10)
    urls = {a["url"].rstrip("/").lower().replace("www.", "") for a in anchors}
    check("C9b 双源聚合去重后 3 个锚点", len(anchors) == 3, f"n={len(anchors)}")
    gh = [a for a in anchors if "github.com/alice" in a["url"].lower()]
    check("C9b GitHub 双源交叉确认",
          bool(gh) and gh[0].get("cross_source_confirmed") is True
          and set(gh[0].get("attribution_sources", [])) == {"Maigret", "Sherlock"},
          str(gh[0] if gh else None))
finally:
    _pipe._collect_identity_multisource = _orig_collect

# ═══════════════════════════════════════════════════════════════
print(f"\n结果: {len(passed)} passed / {len(failed)} failed")
_reset()
sys.exit(1 if failed else 0)