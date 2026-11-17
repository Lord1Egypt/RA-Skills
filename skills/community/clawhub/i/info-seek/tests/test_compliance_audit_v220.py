#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_compliance_audit_v220.py — D-8 / P3-9 守护：合规审计自动化（30 断言）

D-8（= P3-9 立项形式）：抓取合规 / 版权 / 凭证审计的自动化报告。
本套件守护 `scripts/compliance_audit.py`：①四链真源复用口径一致；②只读 + 零网络；
③降级容错（consent 缺失 / stats 空 dict）；④误报白名单分级；⑤产物与退出码语义。

分组：
  A1-A6 模块与真源     —— 文件存在 / 四链函数 / AUDIT_VERSION / 头部 mod-v / ROOT / 零网络 import
  B1-B7 四链结构       —— 链名与顺序 / verdict 域 / 与 leak_scan·capability_registry·boundary_gate·真源 json 计数一致
  C1-C6 分级与容错     —— test_fixture·placeholder·actionable 三分 / 脱敏 / consent 缺失降级 / stats 空 dict
  D1-D5 零网络与基线   —— static_only / 不调 available 探测 / bad=[] / 声明冲突空 / actionable=0
  E1-E4 报告产物       —— 结构 / 落地 / 严格 UTF-8 / Markdown 骨架
  F1-F2 退出码         —— 默认 0 / --strict 有可处置项时 1

设计原则：本套件**不自我 SKIP**（无可选依赖）；一切断言基于真源实时取值，
不硬编码可变数量（仅对稳定基线做等值校验）。
"""
import ast
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (ROOT, os.path.join(ROOT, "scripts"), os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

from mcp_tools_common import SKILL_VERSION  # 唯一对外版本真源

import compliance_audit as ca
import leak_scan as ls
import capability_registry as cr
import boundary_gate as bg

PASS, FAIL = [], []
TARGET = 30


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def head_versions(rel, n=14):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return set()
    with open(p, encoding="utf-8", errors="replace") as f:
        head = "".join(f.readlines()[:n])
    return set(re.findall(r"v(\d+\.\d+\.\d+)", head))


print("=== ① 模块与真源 ===")
MODULE_REL = "scripts/compliance_audit.py"
MODULE_ABS = os.path.join(ROOT, MODULE_REL)
ok("A1 审计模块存在且非空", os.path.exists(MODULE_ABS) and os.path.getsize(MODULE_ABS) > 2000,
   f"size={os.path.getsize(MODULE_ABS) if os.path.exists(MODULE_ABS) else 0}")

chain_fns = {n: getattr(ca, n, None) for n in
             ("audit_credentials", "audit_crawl_compliance", "audit_network_boundary",
              "audit_provenance")}
ok("A2 四链审计函数齐备且可调用",
   all(callable(v) for v in chain_fns.values()),
   ",".join(k for k, v in chain_fns.items() if not callable(v)) or "OK")

ok("A3 AUDIT_VERSION == 真源 SKILL_VERSION", ca.AUDIT_VERSION == SKILL_VERSION,
   f"模块={ca.AUDIT_VERSION} / 真源={SKILL_VERSION}")

hv = head_versions(MODULE_REL)
ok("A4 模块头部 mod-v ⊆ 真源（D-6 C1 免登记）", bool(hv) and hv <= {SKILL_VERSION},
   f"头部版本={sorted(hv)}")

ok("A5 ROOT 解析指向技能根", (ca.ROOT / "SKILL.md").exists() and (ca.ROOT / "scripts").is_dir(),
   f"ROOT={ca.ROOT}")

src = Path(MODULE_ABS).read_text(encoding="utf-8", errors="replace")
tree = ast.parse(src)
mods = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        mods.update(a.name.split(".")[0] for a in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module:
        mods.add(node.module.split(".")[0])
net_bad = mods & {"urllib", "requests", "socket", "httpx", "aiohttp", "http", "ftplib"}
ok("A6 零网络：模块未导入任何网络库", not net_bad, f"涉网导入={sorted(net_bad) or '无'}")

print("\n=== ② 四链结构 ===")
report = ca.build_report()
names = [c["chain"] for c in report["chains"]]
ok("B1 报告含四链且顺序正确",
   names == ["credentials", "crawl_compliance", "network_boundary", "provenance"],
   f"实际={names}")

verdicts = [c["verdict"] for c in report["chains"]]
ok("B2 每链 verdict 取值合法",
   all(v in {"pass", "warn", "fail", "unknown"} for v in verdicts), f"实际={verdicts}")

cred = report["chains"][0]
ok("B3 凭证链模式数与 leak_scan 真源一致",
   cred["scanner"]["pattern_count"] == len(ls.KEY_PATTERNS) and cred["scanner"]["pattern_count"] >= 8,
   f"审计={cred['scanner']['pattern_count']} / 真源={len(ls.KEY_PATTERNS)}")

ok("B4 凭证链确实扫描仓库（文件数 > 100）", cred["scan"]["files_scanned"] > 100,
   f"files_scanned={cred['scan']['files_scanned']}")

crawl = report["chains"][1]
live_caps = cr.list_capabilities()
ok("B5 抓取链能力数与注册表真源一致",
   crawl["registry"]["total"] == len(live_caps) and crawl["registry"]["total"] == len(crawl["capabilities"]),
   f"审计={crawl['registry']['total']} / 真源={len(live_caps)}")

net = report["chains"][2]
live_bound = bg.check_all_declared()
ok("B6 边界链校验数与 boundary_gate 真源一致",
   net["checked"] == len(live_bound) and net["checked"] == net["ok"] + net["failed"],
   f"审计={net['checked']} / 真源={len(live_bound)}")

prov = report["chains"][3]
ts = json.loads((Path(ROOT) / "references" / "trusted-sources.json").read_text(encoding="utf-8"))
ok("B7 来源链计数与 trusted-sources.json 真源一致",
   prov["white_list"] == len(ts.get("white_list", []))
   and prov["kb_sources"] == len(ts.get("kb_sources", []))
   and prov["version"] == str(ts.get("version", "")),
   f"白名单={prov['white_list']}/{len(ts.get('white_list', []))} "
   f"kb={prov['kb_sources']}/{len(ts.get('kb_sources', []))} v={prov['version']}")

print("\n=== ③ 分级与容错 ===")
ok("C1 测试路径命中 → test_fixture",
   ca._classify("sk-" + "abcdef1234567890", os.path.join(ROOT, "tests", "test_x.py")) == "test_fixture")

ok("C2 占位符值 → placeholder",
   ca._classify("sk-" + "your-key-here", os.path.join(ROOT, "scripts", "x.py")) == "placeholder",
   f"分级={ca._classify('sk-'+'your-key-here', 'x.py')}")

plain_val = "ak_" + "live" + "_" + "9f3c7b21" * 3
ok("C3 无占位特征 → actionable",
   ca._classify(plain_val, os.path.join(ROOT, "scripts", "x.py")) == "actionable")

red = ca._redact(plain_val, "actionable")
ok("C4 actionable 明文不落报告且含脱敏标记",
   plain_val not in red and "***" in red, f"redact={red}")

cl = ca.read_consent_log()
need_keys = {"path", "exists", "lines", "grant", "revoke", "malformed", "source"}
ok("C5 consent 台账读取降级不抛且字段齐备",
   need_keys <= set(cl) and isinstance(cl["exists"], bool),
   f"path={cl['path']} exists={cl['exists']} source={cl['source']}")

_orig_stats = ca._KEYS.KeyManager.instance().stats
try:
    ca._KEYS.KeyManager.instance().stats = lambda *a, **k: {}
    empty_chain = ca.audit_credentials()
    empty_ok = (empty_chain["key_status"]["providers"] == 0
                and empty_chain["key_status"]["records"] == 0)
finally:
    ca._KEYS.KeyManager.instance().stats = _orig_stats
ok("C6 空 key stats 下不抛且计数为 0", empty_ok,
   f"providers={empty_chain['key_status']['providers']}")

print("\n=== ④ 零网络与基线 ===")
ok("D1 边界链为静态声明校验（probe=False）",
   net["mode"] == "static_only" and net["probe"] is False, f"mode={net['mode']}")

_orig_avail = bg.available


def _boom(*a, **k):
    raise AssertionError("available() 不应被合规审计调用（须零网络）")


try:
    bg.available = _boom
    net2 = ca.audit_network_boundary()
    probe_free = net2["checked"] == net["checked"] and net2["checked"] > 0
finally:
    bg.available = _orig_avail
ok("D2 审计不调用 available() 探测（零网络实证）", probe_free,
   f"checked={net2['checked']}")

ok("D3 边界链基线 bad=[]（全部声明合规）", net["failed"] == 0 and net["issues"] == {},
   f"failed={net['failed']} issues={net['issues']}")

ok("D4 抓取链无「启用∧需授权」声明冲突",
   crawl["consent"]["declared_conflicts"] == [],
   f"冲突={crawl['consent']['declared_conflicts']}")

ok("D5 凭证链自检 actionable == 0（误报白名单生效）",
   cred["scan"]["actionable"] == 0
   and cred["scan"]["whitelisted"] == cred["scan"]["raw_findings"],
   f"raw={cred['scan']['raw_findings']} whitelisted={cred['scan']['whitelisted']} "
   f"分级={cred['scan']['by_class']}")

print("\n=== ⑤ 报告产物 ===")
ok("E1 报告 meta 齐备且日期合法",
   bool(re.match(r"\d{4}-\d{2}-\d{2}$", report.get("date", "")))
   and report.get("version") == SKILL_VERSION
   and os.path.abspath(report.get("root", "")) == os.path.abspath(ROOT),
   f"date={report.get('date')} version={report.get('version')}")

with tempfile.TemporaryDirectory() as td:
    md_tmp = os.path.join(td, "r.md")
    js_tmp = os.path.join(td, "r.json")
    paths = ca.write_report(md_tmp, js_tmp, report)
    ok("E2 write_report 产出 Markdown + JSON",
       os.path.exists(md_tmp) and os.path.exists(js_tmp) and len(paths) == 2,
       f"paths={[p.name for p in paths.values()]}")

repo_paths = ca.write_report("references/compliance-audit-report.md",
                             "references/compliance-audit-report.json", report)
md_repo = Path(ROOT) / "references" / "compliance-audit-report.md"
bad_utf8 = ""
try:
    md_repo.read_bytes().decode("utf-8")
except UnicodeDecodeError as e:
    bad_utf8 = f"@{e.start} 0x{e.object[e.start]:02x}"
ok("E3 仓库报告产物严格 UTF-8 可解码", not bad_utf8, bad_utf8 or f"{md_repo.stat().st_size} bytes")

md_text = md_repo.read_text(encoding="utf-8")
ok("E4 Markdown 骨架含四链章节与总判定",
   all(k in md_text for k in ("① 凭证审计", "② 抓取合规", "③ 网络边界", "④ 版权来源"))
   and f"总判定：**{report['verdict']}**" in md_text,
   f"verdict={report['verdict']}")

print("\n=== ⑥ 退出码语义 ===")
ok("F1 默认（非 --strict）退出码 0", ca.main([]) == 0)

_orig_cred = ca.audit_credentials


def _fake_cred(*a, **k):
    d = dict(cred)
    d["scan"] = dict(cred["scan"], actionable=1)
    d["verdict"] = "fail"
    return d


try:
    ca.audit_credentials = _fake_cred
    strict_rc = ca.main(["--strict"])
finally:
    ca.audit_credentials = _orig_cred
ok("F2 --strict 存在可处置项时退出码 1", strict_rc == 1, f"rc={strict_rc}")

print(f"\n{'=' * 56}")
print(f"test_compliance_audit_v220: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"(target {TARGET})")
if FAIL:
    print("失败项: " + ", ".join(FAIL))
print(f"{'=' * 56}")
sys.exit(1 if FAIL else 0)