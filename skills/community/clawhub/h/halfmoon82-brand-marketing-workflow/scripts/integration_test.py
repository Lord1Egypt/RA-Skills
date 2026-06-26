#!/usr/bin/env python3
"""Integration test suite for brand-marketing-workflow skill.

Tests 4 categories:
- orchestrator end-to-end
- authorization state transitions
- browser compliance decisions
- degradation paths
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

BASE = Path('/Users/macmini/.openclaw/workspace/skills/brand-marketing-workflow/scripts')

PASS = "✅ PASS"
FAIL = "❌ FAIL"


def run(script: str, payload: dict) -> dict:
    proc = subprocess.run(
        ['python3', str(BASE / script)],
        input=json.dumps(payload).encode(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
    )
    return json.loads(proc.stdout.decode())


def check(label: str, condition: bool) -> bool:
    print(f"  {PASS if condition else FAIL}  {label}")
    return condition


def section(title: str) -> None:
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


results = []

# ─── 1. Orchestrator end-to-end ──────────────────
section("1) Orchestrator — fashion brand full run")
o = run('workflow_orchestrator.py', {
    "brand_name": "Aurora Lane",
    "brand_tone": "calm sharp poetic",
    "channels": ["xiaohongshu", "weibo"],
    "competitor_scope": ["UNIQLOZH public signals"],
    "execution_action": "draft_prepare",
    "browser_action": "collect_public_signals",
    "data_access": "public",
    "need_login": False
})
results += [
    check("brand_brief present", bool(o.get("brand_brief"))),
    check("content_strategy present", bool(o.get("content_strategy"))),
    check("content_assets present", bool(o.get("content_assets"))),
    check("competitor_report present", bool(o.get("competitor_report"))),
    check("performance_report present", bool(o.get("performance_report"))),
    check("iteration_plan present", bool(o.get("iteration_plan"))),
    check("status == ready_for_iteration", o.get("status") == "ready_for_iteration"),
    check("low_confidence == False", o.get("low_confidence") == False),
    check("browser.compliant == True", o.get("browser", {}).get("compliant") == True),
    check("authorization.has_boundary == False (draft_prepare allowed)", o.get("authorization", {}).get("has_boundary") == False),
]

# ─── 2. Authorization state transitions ──────────
section("2) Authorization — publish requires pause")
a1 = run('authorization_manager.py', {
    "action": "publish", "data_access": "authorized",
    "requires_payment": False, "human_response": "", "state": "running"
})
results += [
    check("has_boundary == True", a1["has_boundary"]),
    check("decision == pause", a1["decision"] == "pause"),
    check("pause flag True", a1["pause"] == True),
    check("state == awaiting_confirmation", a1["state"] == "awaiting_confirmation"),
]

section("2b) Authorization — publish resumes on confirm")
a2 = run('authorization_manager.py', {
    "action": "publish", "data_access": "authorized",
    "requires_payment": False, "human_response": "授权执行", "state": "awaiting_confirmation"
})
results += [
    check("decision == allow", a2["decision"] == "allow"),
    check("state == resumed", a2["state"] == "resumed"),
]

section("2c) Authorization — payment requires authorize_payment")
a3 = run('authorization_manager.py', {
    "action": "payment", "data_access": "authorized",
    "requires_payment": True, "human_response": "授权支付", "state": "awaiting_confirmation"
})
results += [
    check("decision == allow_payment", a3["decision"] == "allow_payment"),
    check("state == resumed", a3["state"] == "resumed"),
]

section("2d) Authorization — deny triggers degrade")
a4 = run('authorization_manager.py', {
    "action": "publish", "data_access": "authorized",
    "requires_payment": False, "human_response": "拒绝", "state": "awaiting_confirmation"
})
results += [
    check("decision == degrade", a4["decision"] == "degrade"),
    check("state == degraded", a4["state"] == "degraded"),
]

# ─── 3. Browser compliance ────────────────────────
section("3) Browser — public collect allowed")
b1 = run('browser_execution.py', {
    "action": "collect public signals",
    "data_access": "public", "need_login": False, "platform": "xiaohongshu"
})
results += [
    check("compliant == True", b1["compliance"]["compliant"]),
    check("decision == allow", b1["compliance"]["decision"] == "allow"),
    check("capability_plan not empty", bool(b1.get("capability_plan"))),
]

section("3b) Browser — bypass captcha blocked + degrade path")
b2 = run('browser_execution.py', {
    "action": "bypass captcha",
    "data_access": "unknown", "need_login": True, "platform": "xiaohongshu"
})
results += [
    check("compliant == False", b2["compliance"]["compliant"] == False),
    check("decision == degrade", b2["compliance"]["decision"] == "degrade"),
    check("degrade_to not empty", bool(b2["compliance"].get("degrade_to"))),
]

# ─── Summary ──────────────────────────────────────
total = len(results)
passed = sum(results)
print(f"\n{'='*50}")
print(f"  TOTAL: {passed}/{total} passed {'✅' if passed == total else '⚠️'}")
print('='*50)
exit(0 if passed == total else 1)
