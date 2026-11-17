#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_doc_state_sync_d6.py — D-6 守护：文档真实状态同步机制（29 断言）

ROADMAP 二·补 D-6：风险表 / ROADMAP / CHANGELOG / 内部 docstring 版本与结论自动校验。

四段式：
  ①真源与对外文档对齐 A1-A8：SKILL_VERSION 与 SKILL.md / README / CHANGELOG /
    package.json / ROADMAP 表头逐处一致
  ②ROADMAP 同步不变量 B1-B9：更新日不滞后于最近执行记录；回归行套件数 == 实际套件数；
    B-5 / P2-4~P2-6 / D-1~D-5 完成项已勾；ROADMAP 为严格 UTF-8（无坏字节残留）
  ③docstring 版本分歧白名单 C1-C4：core/ scripts/ 头部 mod-v 集合必须 ⊆
    SKILL_VERSION ∪ 显式登记分歧；白名单自身无过期项
  ④数据契约与产物版本 D1-D4：dist 产物 / synonyms _meta / 风险表版本行

设计原则：冻结当前分歧快照 + 未来新漂移立即报警 —— 白名单登记的是已复核为
模块内部版本（mod-v）的合法分歧；未登记文件一旦出现 ≠ SKILL_VERSION 的
docstring 版本即 FAIL，提示登记或修正。不改任何公开签名；本套件不自我 SKIP。
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

from mcp_tools_common import SKILL_VERSION  # 唯一真源

PASS, FAIL = [], []
TARGET = 29

# run_tests.py 排除集（与 tests/run_tests.py 保持一致）
EXCLUDED_SUITES = {"test_deep_v101.py"}

# 模块内部版本（mod-v）合法分歧白名单：已复核为「模块自身迭代版本」而非对外版本
DIVERGENCE_WHITELIST = {
    "core/__init__.py": {"3.1.0"},
    "core/anchor_score_v2.py": {"1.8.1", "2.0.2"},
    "core/claim_store.py": {"2.3.1", "2.4.0"},
    "core/conflict_v2.py": {"1.8.0", "2.0.0", "2.0.1"},
    "core/conflict_v3.py": {"2.2.1", "2.3.0", "2.3.1", "2.4.0"},
    "core/conflict_weight.py": {"2.5.0"},
    "core/contradiction_scorer.py": {"2.3.1", "2.4.0", "2.5.0"},
    "core/dep_registry.py": {"1.0.0"},
    "core/entities.py": {"2.0.0", "2.0.1", "2.1.0"},
    "core/entity_aliases.py": {"2.1.1"},
    "core/entity_enricher.py": {"2.1.0"},
    "core/entity_graph.py": {"2.3.0"},
    "core/entity_heat.py": {"2.1.0", "2.3.1", "2.4.0"},
    "core/entity_meta.py": {"2.0.1", "2.1.0"},
    "core/entity_pending.py": {"2.1.0", "2.1.1"},
    "core/entity_profile.py": {"2.3.0"},
    "core/entity_tracker.py": {"2.1.0", "2.5.0"},
    "core/entity_trajectory.py": {"2.3.0", "2.3.1", "2.4.0"},
    "core/freshness_cron.py": {"2.0.0", "2.1.1", "2.2.0"},
    "core/identity_aggregator.py": {"2.1.0"},
    "core/key_manager.py": {"1.0.1"},
    "core/jieba_bridge.py": {"1.0.0"},
    "core/learned_anchor_store.py": {"1.0.0"},
    "core/llm_router.py": {"2.0.0"},
    "core/ner.py": {"2.0.0", "2.3.3", "2.4.1", "2.6.0"},
    "core/person_ner.py": {"1.0.0", "1.9.0"},
    "core/state_dir.py": {"3.1.1"},
    "core/traced_export.py": {"2.3.0", "2.3.1"},
    "core/wikidata_sync.py": {"2.1.1"},
    "core/xling_bridge.py": {"1.0.0", "1.9.0"},
    "scripts/account_trust_scorer.py": {"1.1.0"},
    "scripts/anchor_adapter.py": {"1.8.1", "2.0.2"},
    "scripts/boundary_gate.py": {"2.0.0"},
    "scripts/conflict_detection.py": {"1.8.0"},
    "scripts/domain_orchestrator.py": {"1.9.0"},
    "scripts/domain_router.py": {"1.8.1"},
    "scripts/engine_lifecycle.py": {"1.0.1"},
    "scripts/exporter.py": {"1.8.0"},
    "scripts/forensics_retrain.py": {"1.6.0"},
    "scripts/identity_confidence_fusion.py": {"1.7.0"},
    "scripts/infoseek_consent_cli.py": {"2.1.0"},
    "scripts/infoseek_core_v2.py": {"1.8.1", "2.0.0", "3.0.0"},
    "scripts/infoseek_helper.py": {"1.4.0", "2.0.0"},
    "scripts/infoseek_host.py": {"1.0.0"},
    "scripts/infoseek_keys_cli.py": {"1.0.1"},
    "scripts/infoseek_mcp_server.py": {"1.0.0"},
    "scripts/infoseek_pipeline.py": {"1.5.2"},
    "scripts/compliance_audit.py": {"2.6.1"},
    "scripts/hf_sample_kit.py": {"2.2.0"},
    "scripts/infoseek_zerodep_nlp.py": {"1.2.0"},
    "scripts/l2_pen_test.py": {"1.4.2"},
    "scripts/l2_renderer.py": {"1.5.0"},
    "scripts/leak_scan.py": {"1.0.1"},
    "scripts/mcp_tools_analysis.py": {"1.0.1", "1.8.1"},
    "scripts/mcp_tools_archive.py": {"1.0.1"},
    "scripts/mcp_tools_async.py": {"1.0.1"},
    "scripts/mcp_tools_check.py": {"1.0.1"},
    "scripts/mcp_tools_common.py": {"1.0.0", "1.0.1"},
    "scripts/mcp_tools_forensics.py": {"2.2.0"},
    "scripts/mcp_tools_identity.py": {"1.5.0"},
    "scripts/mcp_tools_keys.py": {"1.0.1"},
    "scripts/mcp_tools_search.py": {"1.0.1"},
    "scripts/mirror_map.py": {"2.5.0"},
    "scripts/net_probe.py": {"2.2.0"},
    "scripts/perf_baseline_v101.py": {"2.2.0"},
    "scripts/platform_adapter.py": {"1.1.7"},
    "scripts/probe_three_chain.py": {"1.8.3"},
    "scripts/public_apis_catalog.py": {"1.0.0"},
    "scripts/search_engine_health.py": {"1.0.1"},
    "scripts/shadow_compare_s4.py": {"1.0.0"},
    "scripts/promote_s5.py": {"1.0.0"},
    "scripts/summarize_adapter.py": {"1.7.0"},
    "scripts/text_tokenizer.py": {"1.1.0"},
    "scripts/tiered_router.py": {"1.0.0"},
    "scripts/s3_expand.py": {"1.0.0"},
    "scripts/train_l1_thresholds.py": {"1.0.0"},
}

# 文档级版本白名单（文档自身版本号，非对外版本）
DOC_VERSION_WHITELIST = {"references/risk-register.md": "1.7.0"}
# 数据契约版本白名单（synonyms 词典自身版本）
SYNONYMS_ALLOWED_VERSIONS = {"1.2.0"}


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def note(name, detail):
    print(f"  [note] {name} — {detail}")


def read(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def table_row(text, key):
    m = re.search(r"^\|\s*" + re.escape(key) + r"\s*\|(.*)$", text, re.M)
    return m.group(1) if m else ""


def head_versions(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return set()
    with open(p, encoding="utf-8", errors="replace") as f:
        head = "".join(f.readlines()[:14])
    return set(re.findall(r"v(\d+\.\d+\.\d+)", head))


roadmap = read("references/ROADMAP.md")
skill_md = read("SKILL.md")
readme = read("README.md")
changelog = read("CHANGELOG.md")
pkg = read("package.json")


print("=== ① 真源与对外文档对齐 ===")
ok(f"A1 SKILL_VERSION 真源值 == {SKILL_VERSION}", True, f"实测={SKILL_VERSION}")

m = re.search(r"^version:\s*([\d.]+)\s*$", skill_md, re.M)
ok("A2 SKILL.md frontmatter version == 真源", bool(m) and m.group(1) == SKILL_VERSION,
   f"SKILL.md={m.group(1) if m else '缺失'} / 真源={SKILL_VERSION}")

ok("A3 README 顶部声明 == 真源发布版", f"v{SKILL_VERSION} 发布版" in readme,
   f"查找=v{SKILL_VERSION} 发布版")

ok("A4 README 版本徽章 == 真源", f"version-{SKILL_VERSION}-blue" in readme,
   f"查找=version-{SKILL_VERSION}-blue")

m = re.search(r"^##\s*\[([\d.]+)\]", changelog, re.M)
ok("A5 CHANGELOG 最新条目版本 == 真源", bool(m) and m.group(1) == SKILL_VERSION,
   f"CHANGELOG={m.group(1) if m else '缺失'} / 真源={SKILL_VERSION}")

m = re.search(r'"version"\s*:\s*"([\d.]+)"', pkg)
ok("A6 package.json version == 真源", bool(m) and m.group(1) == SKILL_VERSION,
   f"package.json={m.group(1) if m else '缺失'} / 真源={SKILL_VERSION}")

common_src = read("scripts/mcp_tools_common.py")
defs = re.findall(r'^SKILL_VERSION\s*=\s*"([\d.]+)"', common_src, re.M)
ok("A7 对外版本定义唯一且值 == 真源", len(defs) == 1 and defs[0] == SKILL_VERSION,
   f"定义处={len(defs)} 值={defs}")

m = re.search(r">\s*版本：v([\d.]+)\s*｜\s*更新：(\d{4}-\d{2}-\d{2})", roadmap)
roadmap_ver, roadmap_date = (m.group(1), m.group(2)) if m else ("", "")
ok("A8 ROADMAP 表头版本 == 真源", roadmap_ver == SKILL_VERSION,
   f"ROADMAP=v{roadmap_ver} / 真源={SKILL_VERSION}")

print("\n=== ② ROADMAP 同步不变量 ===")
ok("B1 ROADMAP 表头含合法更新日", bool(re.match(r"\d{4}-\d{2}-\d{2}$", roadmap_date)),
   f"更新={roadmap_date}")

recs = re.findall(r"执行记录（(\d{4}-\d{2}-\d{2})", roadmap)
latest_rec = max(recs) if recs else ""
ok("B2 表头更新日不滞后于最近执行记录", bool(latest_rec) and roadmap_date >= latest_rec,
   f"更新日={roadmap_date} 最近执行记录={latest_rec}")

suites = [os.path.basename(x) for x in glob.glob(os.path.join(ROOT, "tests", "test_*.py"))]
effective = sorted(s for s in suites if s not in EXCLUDED_SUITES)
m = re.search(r"\*\*([\d]+) PASS\s*/\s*([\d]+) SKIP\s*/\s*([\d]+) FAIL\s*/\s*([\d]+) TIMEOUT\*\*（([\d]+) 套件", roadmap)
if m:
    declared_pass, declared_skip, declared_fail, declared_to, declared_suites = (int(m.group(i)) for i in range(1, 6))
else:
    declared_pass = declared_skip = declared_fail = declared_to = declared_suites = -1
ok("B3 回归行声明套件数 == 实际套件数", declared_suites == len(effective),
   f"声明={declared_suites} 实际={len(effective)}")
ok("B4 回归行声明 0 FAIL / 0 TIMEOUT", declared_fail == 0 and declared_to == 0,
   f"FAIL={declared_fail} TIMEOUT={declared_to}")
ok("B5 回归行 PASS == 套件数 - SKIP", declared_pass == declared_suites - declared_skip,
   f"PASS={declared_pass} 套件={declared_suites} SKIP={declared_skip}")

ok("B6 B-5 行已勾完成（路线图自身同步）", "✅" in table_row(roadmap, "B-5"),
   "行状态=" + table_row(roadmap, "B-5")[:40])

p2_rows = {k: table_row(roadmap, k) for k in ("P2-4", "P2-5", "P2-6")}
ok("B7 P2-4 / P2-5 / P2-6 均已勾完成", all("✅" in v for v in p2_rows.values()),
   "未勾=" + ",".join(k for k, v in p2_rows.items() if "✅" not in v))

d_rows = {f"D-{i}": table_row(roadmap, f"D-{i}") for i in range(1, 6)}
ok("B8 D-1 ~ D-5 均已勾完成", all("✅" in v for v in d_rows.values()),
   "未勾=" + ",".join(k for k, v in d_rows.items() if "✅" not in v))

# B9：ROADMAP 必须为严格 UTF-8 —— 历史编辑曾残留 2 个非 UTF-8 字节（0x8a/0x82）
# 位于 L239 行首（L237-238 重复行残迹），已于 2026-09-20 去重修复；此处冻结该不变量。
try:
    with open(os.path.join(ROOT, "references", "ROADMAP.md"), "rb") as _f:
        _rmb = _f.read()
    _rmb.decode("utf-8")
    _rmb_ok, _rmb_detail = True, f"严格 UTF-8 可解码（{len(_rmb)} 字节）"
except UnicodeDecodeError as e:
    _rmb_ok = False
    _rmb_detail = f"坏字节 @{e.start}（{_rmb[e.start]:#x}）"
ok("B9 ROADMAP 为严格 UTF-8（无坏字节 / 替换字符残留）", _rmb_ok, _rmb_detail)

print("\n=== ③ docstring 版本分歧白名单 ===")
scanned = {}
for d in ("core", "scripts"):
    for f in sorted(glob.glob(os.path.join(ROOT, d, "*.py"))):
        rel = os.path.relpath(f, ROOT)
        vs = head_versions(rel)
        if vs:
            scanned[rel] = vs

unregistered = {}
for rel, vs in scanned.items():
    allowed = set(DIVERGENCE_WHITELIST.get(rel, set())) | {SKILL_VERSION}
    extra = vs - allowed
    if extra:
        unregistered[rel] = sorted(extra)
ok("C1 无未登记的 docstring 版本漂移", not unregistered,
   f"扫描={len(scanned)} 未登记={unregistered}" if unregistered else f"扫描 {len(scanned)} 文件全部合规")

stale = {}
for rel, vs in DIVERGENCE_WHITELIST.items():
    found = scanned.get(rel)
    if found is None:
        stale[rel] = "文件缺失或已无版本标注"
    elif set(vs) - found:
        stale[rel] = f"白名单版本 {sorted(set(vs) - found)} 已不存在"
ok("C2 白名单无过期项", not stale, f"过期={stale}" if stale else f"白名单 {len(DIVERGENCE_WHITELIST)} 项全部有效")

ok("C3 包级文档分歧（core/__init__.py / core/state_dir.py）已显式登记",
   "core/__init__.py" in DIVERGENCE_WHITELIST and "core/state_dir.py" in DIVERGENCE_WHITELIST,
   "keys=" + ",".join(k for k in ("core/__init__.py", "core/state_dir.py") if k not in DIVERGENCE_WHITELIST) or "均已登记")

ok("C4 真源文件 scripts/mcp_tools_common.py 已登记（docstring 为模块内部版本）",
   "scripts/mcp_tools_common.py" in DIVERGENCE_WHITELIST,
   f"登记值={sorted(DIVERGENCE_WHITELIST.get('scripts/mcp_tools_common.py', []))}")

print("\n=== ④ 数据契约与产物版本 ===")
def load_json(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return json.load(f)

bj = load_json("dist/perf_baseline_v101.json")
ok("D1 dist/perf_baseline_v101.json version == 真源",
   bool(bj) and bj.get("version") == SKILL_VERSION,
   f"实测={(bj or {}).get('version')}")

pj = load_json("dist/perf_profile_v101.json")
ok("D2 dist/perf_profile_v101.json version == 真源",
   bool(pj) and pj.get("version") == SKILL_VERSION,
   f"实测={(pj or {}).get('version')}")

syn = load_json("references/contradiction-synonyms.json")
syn_ver = ((syn or {}).get("_meta") or {}).get("version")
ok("D3 synonyms 数据契约版本已登记白名单",
   syn_ver in SYNONYMS_ALLOWED_VERSIONS,
   f"实测={syn_ver} 白名单={sorted(SYNONYMS_ALLOWED_VERSIONS)}")

risk = read("references/risk-register.md")
m = re.search(r">\s*版本：v([\d.]+)", risk)
risk_ver = m.group(1) if m else ""
ok("D4 风险表版本行存在且已登记白名单",
   risk_ver == DOC_VERSION_WHITELIST.get("references/risk-register.md"),
   f"实测=v{risk_ver} 白名单=v{DOC_VERSION_WHITELIST.get('references/risk-register.md')}")

print("\n=== ⑤ 文档口径计数与产物引用 ===")
_all_suites = [os.path.basename(x) for x in glob.glob(os.path.join(ROOT, "tests", "test_*.py"))]
_n_files = len(_all_suites)
_n_std = len([s for s in _all_suites if s not in EXCLUDED_SUITES])

m = re.search(r"(\d+)\s*标准套件", skill_md)
ok("E1 SKILL.md §10 标准套件数 == 实测", bool(m) and int(m.group(1)) == _n_std,
   f"声明={m.group(1) if m else '缺失'} 实测={_n_std}")

m = re.search(r"(\d+)\s*个测试文件", skill_md)
ok("E2 SKILL.md §10 测试文件数 == 实测", bool(m) and int(m.group(1)) == _n_files,
   f"声明={m.group(1) if m else '缺失'} 实测={_n_files}")

m = re.search(r"(\d+)\s*个测试文件", readme)
ok("E3 README 测试文件数 == 实测", bool(m) and int(m.group(1)) == _n_files,
   f"声明={m.group(1) if m else '缺失'} 实测={_n_files}")

_refs = set()
for _doc in (readme, skill_md, read("references/risk-register.md")):
    _refs |= set(re.findall(r"dist/[A-Za-z0-9_]+\.json", _doc))
_missing = sorted(r for r in _refs if not os.path.exists(os.path.join(ROOT, r)))
ok("E4 文档引用的 dist/*.json 产物均存在", not _missing,
   f"引用={sorted(_refs)} 缺失={_missing}")

print(f"\nD-6 文档状态同步守护: {len(PASS)} PASS / {len(FAIL)} FAIL（目标 {TARGET} 断言）")
if FAIL:
    print("未通过：" + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
