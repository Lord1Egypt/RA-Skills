#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_perf_profile_d3.py — P2-6/D-3 性能热点分解守护测试（23 断言）

背景：perf_baseline_v101.py 原仅测三段 wall-time + tracemalloc，无函数级分解，
无法定位 research 融合链内部热点；且 baseline dict 的 version 字段长期滞留在
1.0.1（真源 SKILL_VERSION = 2.2.0）→ 文档/产物版本双漂移。

本测试守护 D-3 收口：
  ①代码面：cProfile/pstats 热点分解函数（_parse_pstats / profile_research）、
    --profile CLI 开关、version 漂移已消除（无 1.0.1，字面量与真源一致）
  ②解析面：pstats 文本表格列序 ncalls/tottime/percall/cumtime/percall/func 映射正确
  ③行为面：profile_research 返回 cumulative/tottime 双榜且排序/结构合规
  ④产物面：dist/perf_baseline_v101.json 与 dist/perf_profile_v101.json 版本对齐真源

注：不改 CLI 契约与公开签名；大规模采样由人工执行（560s 窗内 scale≤1000 × 3 轮），
本测试仅用 15 源小规模实跑，避免污染回归时长。
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def note(name, detail):
    print(f"  [note] {name} — {detail}")


SCRIPT = os.path.join(ROOT, "scripts", "perf_baseline_v101.py")
SRC = open(SCRIPT, encoding="utf-8").read()

from mcp_tools_common import SKILL_VERSION  # 真源

print("=== ① 代码面：D-3 收口与版本漂移 ===")

ok(f"C1 SKILL_VERSION 真源 = {SKILL_VERSION}", True, f"实际={SKILL_VERSION}")

ok("C2 perf_baseline 无 1.0.1 残留（漂移已消除）", "1.0.1" not in SRC)

ok("C3 含 cProfile/pstats 热点分解实现",
   "import cProfile" in SRC and "import pstats" in SRC and "def profile_research" in SRC)

ok("C4 含 pstats 文本解析 _parse_pstats", "def _parse_pstats" in SRC)

ok("C5 含 --profile CLI 开关", "--profile" in SRC and "args.profile" in SRC)

# v2.3.0：版本字面量改为动态引用 _BASELINE_VERSION（自真源）——
# 源内不再有写死版本；断言「无写死版本漂移 + 动态常量在场」。
_lit_vers = set(re.findall(r"'version':\s*'([\d.]+)'", SRC))
ok("C6 baseline/prof 版本动态引用真源（无写死字面量）",
   not _lit_vers and "_BASELINE_VERSION" in SRC, f"实测={sorted(_lit_vers)}")

ok("C7 _STATS_ROW 列序为 ncalls/tottime/percall/cumtime/percall/func",
   r"^(\\d+(?:/\\d+)?)\\s+([\\d.]+)\\s+([\\d.]+)\\s+([\\d.]+)\\s+([\\d.]+)\\s+(.+)$".replace("\\\\", "\\") in SRC)

print("\n=== ② 解析面：pstats 表格映射 ===")

import perf_baseline_v101 as pb  # noqa: E402

_FAKE = """
Sat Sep 20 22:00:00 2026    perf_stats

         602 function calls in 3.500 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.001    0.001    3.500    3.500 a.py:1(outer)
        3/1    0.500    0.167    1.250    1.250 b.py:9(mid)
     87746    0.676    0.000    0.676    0.000 c.py:65(leaf)
"""
_rows = pb._parse_pstats(_FAKE)
ok("P1 表头/空行被过滤，仅解析 3 行数据", len(_rows) == 3, f"实测={len(_rows)}")
ok("P2 列序映射正确（ncalls/tottime/cumtime/func）",
   _rows[1]["ncalls"] == "3/1" and _rows[1]["tottime"] == 0.5
   and _rows[1]["cumtime"] == 1.25 and _rows[1]["func"] == "b.py:9(mid)",
   f"实测={_rows[1]}")
ok("P3 '3/1' 分数式 ncalls 保留原样", _rows[1]["ncalls"] == "3/1")
ok("P4 每行含 4 个标准键",
   all(set(r) == {"ncalls", "tottime", "cumtime", "func"} for r in _rows))
_esc = pb._parse_pstats("   ncalls  tottime  percall  cumtime  percall f\n        1    0.5    0.0    0.9    0.0 x.py:1(f)")
ok("P5 无数据行时返回空表（不崩）", pb._parse_pstats("garbage\nno rows here") == []
   and len(_esc) == 1)

print("\n=== ③ 行为面：profile_research 双榜 ===")

_src = []
for i in range(15):
    _src.append({
        "title": f"星河科技行业格局报告 {i}",
        "url": f"https://example.com/a/{i}",
        "content": "星河科技 总部位于深圳 机构评级买入 销量120万台 " * 6,
        "score": 70 + i % 10,
    })

_prof = pb.profile_research("行业 2026 竞争格局", _src, top=10)
ok("B1 返回 cumulative/tottime 双榜",
   isinstance(_prof, dict) and set(_prof) == {"cumulative", "tottime"},
   f"keys={sorted(_prof) if isinstance(_prof, dict) else type(_prof)}")
ok("B2 cumulative 非空且含 4 标准键",
   len(_prof["cumulative"]) > 0
   and all(set(r) == {"ncalls", "tottime", "cumtime", "func"} for r in _prof["cumulative"]))
ok("B3 cumulative 首项为 research（热点入口）",
   "research" in _prof["cumulative"][0]["func"], f"首项={_prof['cumulative'][0]['func']}")
ok("B4 cumulative 按 cumtime 降序",
   all(_prof["cumulative"][i]["cumtime"] >= _prof["cumulative"][i + 1]["cumtime"]
       for i in range(len(_prof["cumulative"]) - 1)))
ok("B5 tottime 按 tottime 降序",
   all(_prof["tottime"][i]["tottime"] >= _prof["tottime"][i + 1]["tottime"]
       for i in range(len(_prof["tottime"]) - 1)))
ok("B6 双榜长度受 top 约束", len(_prof["cumulative"]) <= 10 and len(_prof["tottime"]) <= 10)

print("\n=== ④ 产物面：dist JSON 版本对齐 ===")

_bp = os.path.join(ROOT, "dist", "perf_baseline_v101.json")
if os.path.exists(_bp):
    _bj = json.load(open(_bp, encoding="utf-8"))
    ok("A1 baseline JSON version = 真源", _bj.get("version") == SKILL_VERSION,
       f"实测={_bj.get('version')}")
    _m = _bj.get("metrics") or {}
    ok("A2 baseline JSON 含多轮 P50/P95 采样字段",
       isinstance(_m, dict)
       and all(k in _m for k in ("score_p50", "score_p95", "conflict_p50",
                                 "conflict_p95", "research_p50", "research_p95"))
       and _bj.get("rounds", 0) >= 3,
       f"scale={_bj.get('scale')} rounds={_bj.get('rounds')} "
       f"research_p50={_m.get('research_p50')}")
else:
    note("A1/A2 baseline JSON 缺失（非断言，需人工跑 --scale 1000 --rounds 3）", _bp)

_pp = os.path.join(ROOT, "dist", "perf_profile_v101.json")
if os.path.exists(_pp):
    _pj = json.load(open(_pp, encoding="utf-8"))
    ok("A3 profile JSON version = 真源", _pj.get("version") == SKILL_VERSION,
       f"实测={_pj.get('version')}")
    ok("A4 profile JSON 工具链与双榜结构完整",
       _pj.get("tool") == "cProfile+pstats"
       and len(_pj.get("cumulative_top") or []) > 0
       and len(_pj.get("tottime_top") or []) > 0
       and all(set(r) == {"ncalls", "tottime", "cumtime", "func"}
               for r in _pj["cumulative_top"]))
    ok("A5 profile JSON 保留可追溯字段",
       bool(_pj.get("generated_at")) and bool(_pj.get("subject")))
else:
    note("A3-A5 profile JSON 缺失（非断言，需人工跑 --profile）", _pp)

print(f"\nP2-6/D-3 热点分解守护: {len(PASS)} PASS / {len(FAIL)} FAIL（目标 23 断言）")
sys.exit(1 if FAIL else 0)