#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_capability_registry_v100.py — 统一能力注册表 + 代偿层 + 身份归因客户端 测试

覆盖：
  R1 注册表：加载 / 默认 OFF / consent 闸口 / degrade 链 / env 覆盖
  R2 代偿层：Maigret 失败 → Sherlock 接管 → manual_review 缺口标记
  R3 客户端：默认 OFF 静默 / consent 缺失抛 ConsentRequired / CLI 缺失降级 []
  R4 pipeline：双重闸口（env 未设 → []）；模拟启用+授权 → 走代偿返回锚点

风格：顺序脚本 + check() 收集 + 隔离 env（沿用 test_engine_lifecycle / qveris_bridge 范式）
"""

import os
import sys
import types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

PASS = []
FAIL = []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}" + (f"  -> {detail}" if detail and not cond else ""))

# ── 隔离：清空相关 env ──
for k in ("INFOSEEK_ENABLE_MAIGRET", "INFOSEEK_ENABLE_SHERLOCK",
          "INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION"):
    os.environ.pop(k, None)


# ════════════════════════════════════════════
# R1 注册表
# ════════════════════════════════════════════
from core import capability_registry as cr
from core.capability_errors import ConsentRequired, CapabilityUnavailable

check("R1.1 注册表加载", bool(cr.list_capabilities()))
check("R1.2 Maigret 默认 OFF", cr.is_enabled("Maigret") is False)
check("R1.3 Maigret 需 consent", cr.requires_consent("Maigret") is True)
check("R1.4 Maigret 综合启用=False(无授权)", cr.is_effective_enabled("Maigret") is False)
chain = cr.degrade_chain("Maigret")
check("R1.5 degrade 链 Maigret→Sherlock→manual_review",
      chain == ["Maigret", "Sherlock", "manual_review"], str(chain))
check("R1.6 QVeris 默认启用", cr.is_enabled("QVeris") is True)

# env 覆盖
os.environ["INFOSEEK_ENABLE_MAIGRET"] = "1"
check("R1.7 env 覆盖启用(仍缺 consent)", cr.is_effective_enabled("Maigret") is False)
cr.grant_consent("Maigret")
check("R1.8 env+consent 综合启用", cr.is_effective_enabled("Maigret") is True)
os.environ.pop("INFOSEEK_ENABLE_MAIGRET")
cr.revoke_consent("Maigret")
cr.reload()


# ════════════════════════════════════════════
# R2 代偿层
# ════════════════════════════════════════════
from capability_compensator import compensate, audit_trail

# 构造：Maigret 抛不可用 → Sherlock 成功
calls = []
def h_m(u, **kw):
    calls.append("Maigret")
    raise CapabilityUnavailable("Maigret", "no cli")
def h_s(u, **kw):
    calls.append("Sherlock")
    return [{"platform": "GitHub", "url": "https://github.com/x",
             "username": "x", "confidence": 0.85, "source": "Sherlock"}]
def h_mr(u, **kw):
    calls.append("manual_review")
    return [{"platform": "(需人工核实)", "url": "", "username": u,
             "confidence": 0.0, "source": "manual_review", "_gap": True}]

# 用内存注册表绕过 default_off，仅验证代偿逻辑
cr._cache = {"version": 1, "capabilities": [
    {"name": "Maigret", "kind": "identity_attribution", "enabled": True,
     "requires_consent": True, "degrade_to": ["Sherlock", "manual_review"],
     "health_probe": "engine_lifecycle"},
    {"name": "Sherlock", "kind": "identity_attribution", "enabled": True,
     "requires_consent": True, "degrade_to": ["manual_review"],
     "health_probe": "engine_lifecycle"},
    {"name": "manual_review", "kind": "graceful_fallback", "enabled": True,
     "requires_consent": False, "degrade_to": [], "health_probe": "none"},
]}
cr.grant_consent("Maigret"); cr.grant_consent("Sherlock")
handlers = {"Maigret": h_m, "Sherlock": h_s, "manual_review": h_mr}
res = compensate("Maigret", handlers, "testuser")
check("R2.1 代偿命中 Sherlock", res.used == "Sherlock", str(res.used))
check("R2.2 尝试顺序 Maigret→Sherlock", calls == ["Maigret", "Sherlock"], str(calls))
check("R2.3 非缺口(gap=False)", res.gap_flag is False)
_ = audit_trail(res)  # 不抛即可

# 全链失败 → manual_review 缺口
calls2 = []
def h_m2(u, **kw):
    calls2.append("Maigret"); raise CapabilityUnavailable("Maigret", "x")
def h_s2(u, **kw):
    calls2.append("Sherlock"); raise CapabilityUnavailable("Sherlock", "x")
handlers2 = {"Maigret": h_m2, "Sherlock": h_s2, "manual_review": h_mr}
res2 = compensate("Maigret", handlers2, "testuser")
check("R2.4 全链耗尽→manual_review 缺口", res2.gap_flag is True, str(res2.trail))
check("R2.5 缺口 used=manual_review", res2.used == "manual_review", str(res2.used))
cr.revoke_consent("Maigret"); cr.revoke_consent("Sherlock"); cr.reload()


# ════════════════════════════════════════════
# R3 客户端（默认 OFF + consent 闸 + CLI 缺失降级）
# ════════════════════════════════════════════
import maigret_client
import sherlock_client

# 默认 OFF：search_web 静默返回 []
check("R3.1 Maigret 默认 OFF→[]", maigret_client.search_web("anyuser") == [])
check("R3.2 Sherlock 默认 OFF→[]", sherlock_client.search_web("anyuser") == [])

# 即便强制默认 OFF，search(consent=False) 也应安全返回 []（不抛）
check("R3.3 Maigret.search 默认 OFF 安全降级", maigret_client.search("anyuser") == [])

# consent 闸：模拟已启用但无授权 → ConsentRequired
cr._cache = {"version": 1, "capabilities": [
    {"name": "Maigret", "kind": "identity_attribution", "enabled": True,
     "requires_consent": True, "degrade_to": [], "health_probe": "engine_lifecycle"},
]}
try:
    maigret_client.search("anyuser", consent=False)
    check("R3.4 未授权抛 ConsentRequired", False)
except ConsentRequired:
    check("R3.4 未授权抛 ConsentRequired", True)
cr.reload()


# ════════════════════════════════════════════
# R4 pipeline 双重闸口
# ════════════════════════════════════════════
from infoseek_pipeline import search_identity_attribution

check("R4.1 env 未设→[]", search_identity_attribution("testuser") == [])

# 模拟启用+授权，但 Maigret/Sherlock CLI 均缺失 → 走 manual_review 缺口 → 返回 []（不包装）
os.environ["INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION"] = "1"
cr._cache = {"version": 1, "capabilities": [
    {"name": "Maigret", "kind": "identity_attribution", "enabled": True,
     "requires_consent": True, "degrade_to": ["Sherlock", "manual_review"],
     "health_probe": "engine_lifecycle"},
    {"name": "Sherlock", "kind": "identity_attribution", "enabled": True,
     "requires_consent": True, "degrade_to": ["manual_review"],
     "health_probe": "engine_lifecycle"},
    {"name": "manual_review", "kind": "graceful_fallback", "enabled": True,
     "requires_consent": False, "degrade_to": [], "health_probe": "none"},
]}
cr.grant_consent("Maigret"); cr.grant_consent("Sherlock")
# 注入「CLI 缺失」显式锁定路径（v2.1.0：不再依赖本机恰好未装 CLI 的环境偶然性，
# 否则装好真 CLI 的沙箱/CI 会发起真实网络扫描导致超时）
_orig_m = maigret_client._resolve_cli
_orig_s = sherlock_client._resolve_cli
maigret_client._resolve_cli = lambda: ["/nonexistent/infoseek_test_maigret_bin"]
sherlock_client._resolve_cli = lambda: ["/nonexistent/infoseek_test_sherlock_bin"]
try:
    # 两个客户端 CLI 均缺失 → 双源聚合空 → 代偿到 manual_review（缺口）→ []
    out = search_identity_attribution("testuser", consent=True)
finally:
    maigret_client._resolve_cli = _orig_m
    sherlock_client._resolve_cli = _orig_s
check("R4.2 全链缺口→[]（不静默造假）", out == [], str(out)[:80])
os.environ.pop("INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION")
cr.revoke_consent("Maigret"); cr.revoke_consent("Sherlock"); cr.reload()


# ════════════════════════════════════════════
# R5 边界硬化（G1 单例 / G3 代偿闭合 / G6 末端 handler）
# ════════════════════════════════════════════
cr.reload()
if os.path.join(ROOT, "core") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "core"))
import capability_registry as _cr_top
check("R5.1 core 与顶层名同一模块对象（状态不分裂）", cr is _cr_top)
cr.grant_consent("Maigret")
check("R5.2 consent 经 core 授权 → 顶层可见", _cr_top.consent_granted("Maigret") is True)
cr.revoke_consent("Maigret")
_qchain = cr.degrade_chain("QVeris")
check("R5.3 QVeris 代偿链末端闭合 manual_review",
      _qchain == ["QVeris", "Exa", "Tavily", "manual_review"], str(_qchain))
_caps = {c["name"] for c in cr.list_capabilities()}
_dangling = [(c["name"], t) for c in cr.list_capabilities()
             for t in (c.get("degrade_to") or []) if t not in _caps]
check("R5.4 注册表无悬空 degrade_to 引用", not _dangling, str(_dangling))
_r6 = compensate("manual_review", {})
check("R5.5 末端 graceful_fallback 无 handler → gap 显式标记",
      _r6.gap_flag is True and _r6.used == "manual_review",
      f"gap={_r6.gap_flag} used={_r6.used}")


# ════════════════════════════════════════════
# 汇总
# ════════════════════════════════════════════
print(f"\n=== capability_registry 测试: {len(PASS)} passed / {len(FAIL)} failed ===")
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL OK")
