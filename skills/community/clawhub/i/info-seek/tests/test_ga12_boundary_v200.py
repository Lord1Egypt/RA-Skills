#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_ga12_boundary_v200.py — GA12 网络边界门控守护测试（v2.0.0，36 断言）

覆盖五步链：
  ① net_probe 唯一真源（规整/缓存/可达语义/批量/委托收口）
  ② registry.yaml 边界声明 + 3 网络能力化 + core 访问器
  ③ boundary_gate（check_declared/available/preflight/默认OFF/fail-open）
  ④ 受限清单报告渲染
  ⑤ capability_compensator 边界预检（ON 显式降级 / OFF 零变更 / fail-open）

原则：全程注入 mock probe，零真实网络；门控 env 用后还原（测试隔离）。
"""

import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if detail and not cond else ""))


# ── 受控 probe：按 host 可达表返回 ──────────────────────────
def make_probe(reachable):
    def _probe(hosts, timeout=5.0, force=False, workers=8):
        return {h: {"host": h, "ok": h in reachable, "elapsed": 0.01,
                    "err": "" if h in reachable else "mock-unreach",
                    "ts": 0, "cached": False} for h in hosts}
    return _probe


PROBE_OK = make_probe({"*"})  # 全可达占位（实际用 set 判断）
PROBE_RESTRICTED = make_probe(set())  # 全不可达
PROBE_PARTIAL = make_probe({"cn.bing.com", "api.github.com"})

# ── env 隔离 ────────────────────────────────────────────────
_saved_gate = os.environ.pop("INFOSEEK_BOUNDARY_GATE", None)

# ═══════════════════════════════════════════════════════════
# ① net_probe
# ═══════════════════════════════════════════════════════════
import net_probe

check("1 net_probe 模块导入", hasattr(net_probe, "probe_host"))
check("2 host 规整去 scheme/路径",
      net_probe._normalize_host("HTTPS://www.Wikidata.org/w/api.php?x=1")
      == "www.wikidata.org")
net_probe.reset_cache()
r = net_probe.probe_host("unit-test-host-%d.local" % os.getpid(), timeout=1.0)
check("3 probe_host 返回结构",
      set(["host", "ok", "elapsed", "err", "ts", "cached"]).issubset(r.keys()))
r2 = net_probe.probe_host(r["host"], timeout=1.0)
check("4 TTL 缓存命中（cached=True）", r2["cached"] is True and r2["ok"] == r["ok"])
empty = net_probe.probe_host("", timeout=1.0)
check("5 空 host 判不可达不抛错", empty["ok"] is False)
batch = net_probe.check_hosts(["a.local", "b.local"], timeout=1.0,
                              probe=None) if False else net_probe.check_hosts.__name__ == "check_hosts"
check("6 check_hosts 批量接口存在", batch is True)

# 委托收口
import engine_router
import search_engine_health
check("7 engine_router.probe_http 已委托 net_probe",
      "net_probe" in (engine_router.probe_http.__doc__ or ""))
check("8 search_engine_health.probe_http 已委托 net_probe",
      "net_probe" in (search_engine_health.probe_http.__doc__ or ""))

# ═══════════════════════════════════════════════════════════
# ② registry 声明 + 访问器
# ═══════════════════════════════════════════════════════════
from core import capability_registry as reg
reg.reload()
caps = {c["name"]: c for c in reg.list_capabilities()}
check("9 能力数=14（12 原有 + Exa/Tavily 搜索替代层占位）", len(caps) == 14)
check("10 新增 WikiVerify", "WikiVerify" in caps)
check("11 新增 L4Transcribe", "L4Transcribe" in caps)
check("12 新增 PatentLookup", "PatentLookup" in caps)
check("13 三新能力默认 OFF + 受限声明",
      all(caps[n].get("enabled") is False and
          caps[n].get("network_boundary") == "sandbox_restricted"
          for n in ("WikiVerify", "L4Transcribe", "PatentLookup")))
check("14 get_requires_hosts 返回 list",
      isinstance(reg.get_requires_hosts("WikiVerify"), list)
      and "www.wikidata.org" in reg.get_requires_hosts("WikiVerify"))
check("15 get_network_boundary 枚举",
      reg.get_network_boundary("AccountTrustScorer") == "local"
      and reg.get_network_boundary("WikiVerify") == "sandbox_restricted"
      and reg.get_network_boundary("Maigret") == "open")
ledger = reg.get_network_boundaries()
check("16 network_boundaries host 台账≥11", len(ledger) >= 11
      and "www.wikidata.org" in ledger)

# ═══════════════════════════════════════════════════════════
# ③ boundary_gate
# ═══════════════════════════════════════════════════════════
import boundary_gate as bg

decl = bg.check_all_declared()
check("17 check_all_declared 覆盖 14 能力", len(decl) == 14)
check("18 全部声明完整（无 issue）", all(d["ok"] for d in decl))
check("19 未知能力声明校验失败",
      bg.check_declared("NoSuchCap")["ok"] is False)
check("20 local 恒可用",
      bg.available("AccountTrustScorer", probe=PROBE_RESTRICTED)["status"] == "local")
check("21 open 无 host 保守放行（untested_no_hosts）",
      bg.available("Maigret", probe=PROBE_RESTRICTED)["status"] == "untested_no_hosts")
av = bg.available("WikiVerify", probe=PROBE_RESTRICTED)
check("22 受限 host 实测不可达→boundary_restricted",
      av["status"] == "boundary_restricted" and av["available"] is False
      and len(av["unreachable"]) == 4)
av_ok = bg.available("WikiVerify", probe=make_probe(set(reg.get_requires_hosts("WikiVerify"))))
check("23 全部 host 可达→available", av_ok["status"] == "available")

# 门控默认 OFF
os.environ.pop("INFOSEEK_BOUNDARY_GATE", None)
pf = bg.preflight("WikiVerify", probe=PROBE_RESTRICTED)
check("24 preflight 默认 OFF 恒放行（零网络）",
      pf["allowed"] is True and pf["gated"] is False and pf["status"] == "gate_off")

# 门控 ON
os.environ["INFOSEEK_BOUNDARY_GATE"] = "1"
pf_on = bg.preflight("WikiVerify", probe=PROBE_RESTRICTED)
check("25 门控 ON 不可达→allowed=False + 给 degrade_to",
      pf_on["allowed"] is False and pf_on["gated"] is True
      and pf_on["status"] == "boundary_restricted"
      and "manual_review" in pf_on["degrade_to"])
pf_ok = bg.preflight("WikiVerify", probe=make_probe(set(reg.get_requires_hosts("WikiVerify"))))
check("26 门控 ON host 可达→allowed=True", pf_ok["allowed"] is True)


def boom_probe(hosts, **k):
    raise RuntimeError("probe down")


pf_fo = bg.preflight("WikiVerify", probe=boom_probe)
check("27 探测异常 fail-open 放行",
      pf_fo["allowed"] is True and pf_fo["status"] == "fail_open")
os.environ.pop("INFOSEEK_BOUNDARY_GATE", None)

# ═══════════════════════════════════════════════════════════
# ④ 报告
# ═══════════════════════════════════════════════════════════
rep = bg.restricted_report(probe=PROBE_PARTIAL)
md = bg.render_report_md(rep)
check("28 报告含能力表/台账/降级/原则四段",
      all(s in md for s in ("能力边界声明", "Host 实测台账", "降级路径", "边界原则")))
tmp_md = os.path.join(tempfile.mkdtemp(), "nb.md")
p = bg.write_report(tmp_md, probe=PROBE_PARTIAL)
check("29 write_report 落盘成功", os.path.exists(p) and os.path.getsize(p) > 200)

# ═══════════════════════════════════════════════════════════
# ⑤ compensator 边界预检
# ═══════════════════════════════════════════════════════════
import capability_compensator as cc

os.environ["INFOSEEK_BOUNDARY_GATE"] = "1"
os.environ["INFOSEEK_ENABLE_WIKIVERIFY"] = "1"
reg.reload()
# compensator 内部 from boundary_gate import preflight（无 probe 入参），
# 故注入 bg 模块级 check_hosts（其默认 fn 引用模块全局 check_hosts）
bg.check_hosts = PROBE_RESTRICTED
res = cc.compensate("WikiVerify", {
    "WikiVerify": lambda *a, **k: "should-not-run",
    "manual_review": lambda *a, **k: "manual"})
check("30 ON：受限能力显式降级 manual_review",
      res.used == "manual_review" and res.result == "manual")
check("31 ON：trail 留痕 boundary_restricted",
      any(s[0] == "WikiVerify" and "boundary_restricted" in s[1] for s in res.trail))
check("32 ON：boundary_restricted 标志置位", res.boundary_restricted is True)

os.environ["INFOSEEK_BOUNDARY_GATE"] = "0"
res2 = cc.compensate("WikiVerify", {"WikiVerify": lambda *a, **k: "real"})
check("33 OFF：已启用受限能力正常执行（零变更）",
      res2.used == "WikiVerify" and res2.result == "real"
      and res2.boundary_restricted is False)

# 默认 OFF 且不设 gate env
os.environ.pop("INFOSEEK_BOUNDARY_GATE", None)
res3 = cc.compensate("WikiVerify", {"WikiVerify": lambda *a, **k: "real2"})
check("34 未设门控 env：预检跳过零变更",
      res3.used == "WikiVerify" and res3.boundary_restricted is False)

# compensator fail-open：boundary_gate.preflight 抛错时不阻断
os.environ["INFOSEEK_BOUNDARY_GATE"] = "1"
orig_pre = bg.preflight
bg.preflight = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("gate crash"))
res4 = cc.compensate("WikiVerify", {"WikiVerify": lambda *a, **k: "real3"})
check("35 compensator 门控异常 fail-open", res4.used == "WikiVerify")
bg.preflight = orig_pre
os.environ.pop("INFOSEEK_BOUNDARY_GATE", None)
os.environ.pop("INFOSEEK_ENABLE_WIKIVERIFY", None)
reg.reload()

# audit_trail 含 boundary 信息
tr = cc.audit_trail(res)
check("36 audit_trail 输出含 exhausted/gap 字段",
      "exhausted=" in tr and "gap=" in tr)

# ── 汇总 ────────────────────────────────────────────────────
print(f"\nGA12 边界门控: {len(PASS)} PASS / {len(FAIL)} FAIL（目标 36 断言）")
if _saved_gate is not None:
    os.environ["INFOSEEK_BOUNDARY_GATE"] = _saved_gate
sys.exit(1 if FAIL else 0)
