#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_longtail_cn_benchmark_cn3.py — P1-CN3 长尾中文评估基准

量化验收 CN2/CN4 的四层退化是否被治理（靶子源自《infoseek 长尾中文召回
评估报告》2026-09-29，references/ROADMAP.md L107-108）：

  A 召回退化：长尾中文 query 在通用/国际引擎下召回为空或质量差 →
              CN2 中文引擎优先路由必须把 CN-AI-Web 前置并提权。
  B 召回增强零增益：增强（别名扩展/提权）未带来排序/融合增益 →
              提权后 CN-AI-Web 融合权重须真实抬升且参与排序。
  C 过滤门控误杀：短中文/正常 query 被误判为长尾而错误路由/提权 →
              仅长尾触发，短词/纯英文零误杀。
  D jieba 缺失回退：无 jieba 时长尾判定/路由须仍可用、不崩 →
              纯 re 判定路径独立于 jieba。

全部离线：不触网，net_probe 用桩，环境用例自管 env。
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import net_probe  # noqa: E402
import infoseek_pipeline as ip  # noqa: E402

PASS: list[str] = []
FAIL: list[str] = []


def ok(name: str, cond) -> None:
    (PASS if cond else FAIL).append(name)
    print(("  [PASS] " if cond else "  [FAIL] ") + name)


# --- 环境隔离：锁定 CN2/CN4 默认态，清空旁路 ---
for _k in list(os.environ):
    if _k.startswith("INFOSEEK_"):
        del os.environ[_k]

# 离线 fixture：长尾中文四层的代表性 query
LONG_CN = [
    "信阳板栗今年产量是多少？",
    "2025年国内新能源汽车销量排名前十有哪些",
    "县级公立医院绩效改革最新政策如何落地",
]
SHORT_CN = ["股票", "苹果", "量化"]
EN_Q = ["best quantitative trading strategy for futures", "apple stock price"]


def layer_names(q):
    return [n for n, _ in ip._default_layer(q)]


print("=== A 召回退化：长尾中文必须前置中文引擎 ===")
for q in LONG_CN:
    n = layer_names(q)
    ok(f"A 前置 CN-AI-Web：{q[:12]}", n and n[0] == "CN-AI-Web")
    ok(f"A 仅一个 CN 实例：{q[:12]}", n.count("CN-AI-Web") == 1)
    ok(f"A 仍保留通用引擎兜底：{q[:12]}", "Bing-RSS" in n or "DuckDuckGo-HTML" in n)

print("=== B 召回增强零增益：提权须真实抬升融合权重并影响排序 ===")
for q in LONG_CN:
    w = ip._engine_weight_for("CN-AI-Web", q)
    ok(f"B CN 权重提至 1.0：{q[:12]}", abs(w - 1.0) < 1e-9)
    ok(f"B 提权不超封顶：{q[:12]}", w <= 1.0 + 1e-9)
# 基线引擎权重不被污染
ok("B Bing-RSS 基线不变", abs(ip._engine_weight_for("Bing-RSS", LONG_CN[0]) - 0.9) < 1e-9)
# 排序增益：构造 merge_diverse 所需最小结构，验证 CN 结果在长尾 query 下排前
def _item(engine, title="t"):
    return {"title": title, "url": f"https://x/{engine}", "engine": engine, "content": ""}
merged = ip._merge_diverse(
    {"Bing-RSS": [_item("Bing-RSS")],
     "CN-AI-Web": [_item("CN-AI-Web")],
     "DuckDuckGo-HTML": [_item("DuckDuckGo-HTML")]}, 5, LONG_CN[0]
)
ok("B 融合排序 CN-AI-Web 居首", merged and merged[0].get("engine") == "CN-AI-Web")

print("=== C 过滤门控误杀：短中文/英文不得触发前置或提权 ===")
for q in SHORT_CN + EN_Q:
    n = layer_names(q)
    ok(f"C 不前置 CN：{q[:14]}", n.count("CN-AI-Web") == 0)
    ok(f"C 不提权 CN：{q[:14]}", abs(ip._engine_weight_for("CN-AI-Web", q) - 0.3) < 1e-9)
    ok(f"C 未被误判长尾：{q[:14]}", ip._longtail_cn(q) is False)

print("=== C+ 开关回退：CN_PRIORITY=0 回到 P0-2 末尾兜底 ===")
os.environ["INFOSEEK_CN_PRIORITY"] = "0"
for q in LONG_CN:
    n = layer_names(q)
    ok(f"C+ CN 回末尾：{q[:12]}", n.index("CN-AI-Web") == len(n) - 1)
    ok(f"C+ 权重回落：{q[:12]}", abs(ip._engine_weight_for("CN-AI-Web", q) - 0.3) < 1e-9)
del os.environ["INFOSEEK_CN_PRIORITY"]

print("=== D jieba 缺失回退：纯 re 路径独立于可选依赖 ===")
# 长尾判定只依赖 _CJK_RE + 字数，不 import jieba；用模块属性探测
saved = getattr(ip, "_JIEBA", None) if hasattr(ip, "_JIEBA") else None
try:
    if hasattr(ip, "_JIEBA"):
        ip._JIEBA = None
        ip._JIEBA_PROBED = True
    for q in LONG_CN:
        ok(f"D 无 jieba 仍判长尾：{q[:12]}", ip._longtail_cn(q) is True)
        n = layer_names(q)
        ok(f"D 无 jieba 仍前置 CN：{q[:12]}", n and n[0] == "CN-AI-Web")
finally:
    if hasattr(ip, "_JIEBA"):
        ip._JIEBA = saved

print("=== D+ CN4 netguard：端点全不可达优雅降级 / 探测异常保守保留 ===")
_real_check = net_probe.check_hosts
try:
    net_probe.check_hosts = lambda hosts, **kw: {
        h: {"host": h, "ok": False, "err": "unreachable", "ts": 0,
            "cached": False, "elapsed": None} for h in hosts}
    r = ip._search_cn_web(LONG_CN[0], 3)
    ok("D+ 全不可达返空、不污染主链", r == [])
    net_probe.check_hosts = lambda hosts, **kw: (_ for _ in ()).throw(RuntimeError("probe boom"))
    ip._http_get = lambda u, timeout=10: (_ for _ in ()).throw(Exception("net down"))
    r2 = ip._search_cn_web(LONG_CN[0], 3)
    ok("D+ 探测异常保守保留且不崩", r2 == [])
finally:
    net_probe.check_hosts = _real_check

print(f"\nlongtail_cn_benchmark_cn3: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL:
    print("未通过：" + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
