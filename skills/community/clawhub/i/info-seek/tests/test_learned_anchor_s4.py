#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_learned_anchor_s4.py — S4 守护：learned 锚点层 + 影子模式旁路（27 断言）

方向一·阶段B「影子模式」：验证 core/learned_anchor_store.py 的统一访问协议
（默认 OFF / 损坏回退 / 裁决流转 / 子串冲突 / 原子落盘）与 scripts/shadow_compare_s4.py
的旁路语义（强制 zerodep / 主链零改动 / 差异仅在注入后产生 / 零接线）。

分组：
  A 默认开关      （A1-A3）
  B 损坏回退空表  （B1-B6）
  C 裁决流转      （C1-C5）
  D 子串冲突双向  （D1-D3）
  E 原子落盘      （E1-E2）
  F 影子旁路      （F1-F8）

约束：不自我 SKIP；不依赖可选第三方；全部用临时目录隔离，不碰真实数据文件。
"""

import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "core"), ROOT, os.path.join(ROOT, "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)

# 隔离统一开关：锁定协议默认态，不受进程遗留 env 影响
os.environ.pop("INFOSEEK_LEARNED_ANCHORS", None)

import learned_anchor_store as las  # noqa: E402
import infoseek_zerodep_nlp as zdn  # noqa: E402
import shadow_compare_s4 as scs  # noqa: E402

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── A 默认开关 ──────────────────────────────────────────────────────────
print("=== A 默认开关（统一访问协议默认不启用）===")
os.environ.pop("INFOSEEK_LEARNED_ANCHORS", None)
ok("A1 is_enabled() 默认 False", las.is_enabled() is False)
os.environ["INFOSEEK_LEARNED_ANCHORS"] = "1"
ok("A2 =1 时启用 True", las.is_enabled() is True)
for bad in ("0", "off", "no", "maybe", ""):
    os.environ["INFOSEEK_LEARNED_ANCHORS"] = bad
    if las.is_enabled():
        ok(f"A3 非法值 '{bad}' 不启用", False)
        break
else:
    ok("A3 0/off/no/空值 均不启用", True)
os.environ.pop("INFOSEEK_LEARNED_ANCHORS", None)


# ── B 损坏回退空表（永不抛错）──────────────────────────────────────────
print("\n=== B 损坏回退空表 ===")
d = tempfile.mkdtemp()
p_missing = os.path.join(d, "nope.json")
s = las.load(p_missing)
ok("B1 文件缺失→空表不抛错", s.get("entries") == {} and s.get("version") == las.STORE_VERSION)

p_bad = os.path.join(d, "bad.json")
with open(p_bad, "w", encoding="utf-8") as fh:
    fh.write("{不是合法json,,,")
ok("B2 JSON 损坏→空表不抛错", las.load(p_bad).get("entries") == {})

for raw in ([1, 2, 3], "string", 42, None):
    pp = os.path.join(d, "raw.json")
    with open(pp, "w", encoding="utf-8") as fh:
        json.dump(raw, fh)
    if las.load(pp).get("entries") != {}:
        ok("B3 非 dict 顶层→空表", False, str(type(raw)))
        break
else:
    ok("B3 非 dict 顶层（list/str/int/None）→空表", True)

pp = os.path.join(d, "schema.json")
with open(pp, "w", encoding="utf-8") as fh:
    json.dump({"entries": ["不是dict"]}, fh)
ok("B4 entries 非 dict→空表", las.load(pp).get("entries") == {})

pp = os.path.join(d, "coerce.json")
with open(pp, "w", encoding="utf-8") as fh:
    json.dump({"entries": {
        "甲": {"decision": "奇怪状态"},
        "乙": {"decision": "accept", "substring_of": "固态电池", "has_substring": None},
    }}, fh, ensure_ascii=False)
ce = las.load(pp)["entries"]
ok("B5 非法 decision 归一为 pending", ce.get("甲", {}).get("decision") == "pending")
ok("B6 substring 字段强制为 list 类型（含 None 与字符串坏值）",
   isinstance(ce.get("乙", {}).get("substring_of"), list)
   and ce.get("乙", {}).get("has_substring") == [])


# ── C 裁决流转 ─────────────────────────────────────────────────────────
print("\n=== C 裁决流转（pending→accept/reject）===")
pc = os.path.join(d, "decide.json")
las.reset(pc)
las.upsert_pending("碳酸锂", {"topic": "lithium", "cover": 0.95}, path=pc)
ok("C1 upsert 后为 pending 且 provenance 落库",
   "碳酸锂" in las.pending_terms(pc)
   and las.get("碳酸锂", pc).get("provenance", {}).get("topic") == "lithium")

e = las.set_decision("碳酸锂", "accept", note="抽检通过", path=pc)
ok("C2 accept 后进入 active 且离开 pending",
   "碳酸锂" in las.active_terms("accept", pc)
   and "碳酸锂" not in las.pending_terms(pc)
   and e.get("decided_at") is not None and e.get("note") == "抽检通过")

ok("C3 不存在词 set_decision 返回 None", las.set_decision("幽灵词", "accept", path=pc) is None)
try:
    las.set_decision("碳酸锂", "bad_state", path=pc)
    ok("C4 非法 decision 抛 ValueError", False)
except ValueError:
    ok("C4 非法 decision 抛 ValueError", True)
try:
    las.active_terms("bad_state", pc)
    ok("C5 active_terms 非法 decision 抛 ValueError", False)
except ValueError:
    ok("C5 active_terms 非法 decision 抛 ValueError", True)


# ── D 子串冲突双向登记 ─────────────────────────────────────────────────
print("\n=== D 子串冲突双向登记 ===")
pd_ = os.path.join(d, "conf.json")
las.reset(pd_)
las.bulk_upsert_pending([{"term": "固态电池"}, {"term": "电池"}], path=pd_)
ent = las.list_entries(pd_)
ok("D1 短词 substring_of 指向长词", ent["电池"]["substring_of"] == ["固态电池"])
ok("D2 长词 has_substring 指向短词", ent["固态电池"]["has_substring"] == ["电池"])
pairs = las.conflicts(pd_)
ok("D3 conflicts() 输出 {long,short} 对",
   {"long": "固态电池", "short": "电池"} in pairs, str(pairs))


# ── E 原子落盘 ─────────────────────────────────────────────────────────
print("\n=== E 原子落盘 ===")
pe = os.path.join(d, "atom.json")
las.reset(pe)
las.upsert_pending("数据中心", path=pe)
ok("E1 落盘后正式文件存在且无 .tmp 残留",
   os.path.exists(pe) and not os.path.exists(pe + ".tmp"))
reloaded = las.load(pe)
ok("E2 重新读取与写入一致（entries 含数据中心）",
   "数据中心" in reloaded.get("entries", {}))


# ── F 影子旁路（只记录、绝不改主链门控）────────────────────────────────
print("\n=== F 影子旁路 ===")
text = ("固态电池能量密度显著提升，数据中心算力需求带动铜与电力消耗，"
        "动力电池企业规划产能扩张，供需缺口支撑现货价格中枢上移。" * 2)
orig_jb = zdn._optional_jieba
orig_sm = zdn._optional_summa
orig_freq = frozenset(zdn._ZH_HIGH_FREQ)

# 基线参照：强制 zerodep（与 shadow base 路径同条件）、base_freq 不注入 learned
zdn._optional_jieba = lambda text, top: None
zdn._optional_summa = lambda text, top: None
zdn._ZH_HIGH_FREQ = orig_freq
ref, ref_engine = zdn.extract_keywords_detailed(text, max_kw=15)
ref_terms = [w for w, _ in ref]
# 立即还原，交由 scs.run 自行 force/restore
zdn._optional_jieba = orig_jb
zdn._optional_summa = orig_sm

rec = {"idx": 0, "slug": "demo_topic", "title": "对拍样例", "text": text}
learned = ["固态电池", "数据中心", "动力电池", "供需缺口", "价格中枢"]
report = scs.run([rec], learned)
doc = report["docs"][0]

ok("F1 run 后强制引擎还原（jieba/summa 引用恢复）",
   zdn._optional_jieba is orig_jb and zdn._optional_summa is orig_sm)
ok("F2 run 后 _ZH_HIGH_FREQ 还原为基线集合",
   frozenset(zdn._ZH_HIGH_FREQ) == orig_freq)
ok("F3 base/shadow 引擎均为 zerodep（外部 NLP 已关）",
   doc["engine_base"] == "zerodep" and doc["engine_shadow"] == "zerodep",
   f"{doc['engine_base']}/{doc['engine_shadow']}")
ok("F4 base 抽取与主链基线完全一致（主链零改动）",
   doc["base"] == ref_terms, f"base={doc['base'][:6]} ref={ref_terms[:6]}")
changed = bool(doc["added"] or doc["removed"])
ok("F5 注入 learned 后 shadow 产生差异（旁路可观测）",
   changed and doc["shadow"] != doc["base"],
   f"added={doc['added']} removed={doc['removed']}")
ok("F6 learned_hits 仅做子串命中记录",
   set(doc["learned_hits"]) <= set(learned) and len(doc["learned_hits"]) >= 3,
   str(doc["learned_hits"]))

# 契约审计：S5 后主链经「统一访问协议」受控接线，但默认 OFF 逐字节回退
with open(os.path.join(ROOT, "scripts", "infoseek_zerodep_nlp.py"), "r", encoding="utf-8") as fh:
    main_src = fh.read()
ok("F7a 主链定义统一访问协议 _active_zh_anchors()",
   "def _active_zh_anchors" in main_src)
# 顶层（列0、非函数体内）不得出现 learned_anchor_store 的 import 语句
_top_imports = []
for _line in main_src.splitlines():
    if _line.startswith(("import ", "from ")) and "learned_anchor_store" in _line:
        _top_imports.append(_line)
ok("F7b learned 层为函数内惰性 import（无顶层硬依赖）", not _top_imports, str(_top_imports))
# 默认 OFF（无开关环境变量）时统一访问协议逐字节回退基线
os.environ.pop("INFOSEEK_LEARNED_ANCHORS", None)
ok("F7c 默认 OFF 下 _active_zh_anchors() 逐字节回退基线",
   zdn._active_zh_anchors() == orig_freq)
with open(os.path.join(ROOT, "core", "learned_anchor_store.py"), "r", encoding="utf-8") as fh:
    las_src = fh.read()
# 按真实 import 语句行检测，排除 docstring 中“绝不 import …”的说明文字
import re as _re
_bad_imports = []
for _line in las_src.splitlines():
    s = _line.strip()
    if s.startswith(("import ", "from ")) and (
        "capability_registry" in s or "infoseek_zerodep_nlp" in s):
        _bad_imports.append(s)
ok("F8 learned 层单向依赖（无 cap/主链 import 语句）", not _bad_imports, str(_bad_imports))

# 还原现场
zdn._ZH_HIGH_FREQ = orig_freq

print(f"\nlearned_anchor_s4: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL:
    print("未通过：" + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
