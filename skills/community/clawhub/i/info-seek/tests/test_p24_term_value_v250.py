#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_p24_term_value_v250.py — P2-4/D-4 叙述句事实槽召回守护测试（mod v2.5.0，22 断言）

背景：contradiction_scorer v2.4.0 的 `_enum_conflict` 仅走 opposites 预定义词对，
`_value_conflicts` 非数值型枚举值冲突完全不处理 → 叙述句「同槽值不同」三类漏检
（机构评级 买入↔卖出 / 总部 深圳↔北京 / 销量口径），仅靠否定词旁路命中。

本测试守护 v2.5.0 的 term-value 扩展：
  ①数据真源（aspects 24 簇 / opposites 9 组 / _meta 1.1.0 / NUMERIC_ASPECTS 12 类 /
    _TERM_VALUE_ASPECTS 4 项 / 词表精度）
  ②term-value 冲突行为（location / person_change / analyst_rating 双路径 / listing_status）
  ③去重计数（单槽 35 分，不因双路径重复计分）
  ④反向零误报（同值 / 一致口径 / 量纲隔离）
  ⑤长文本不稀释 + schema 兼容 + 无方面文本不崩

已知边界（仅登记，不作断言）：sales_volume「台↔吨」、trend_dir 英文 upgrade/downgrade
子串命中、analyst_rating 跨语言同义（buy↔增持）。均记于 ROADMAP P2-4 延伸项。
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if detail and not cond else ""))


def note(name, detail=""):
    print(f"[KNOWN] {name}" + (f"  -> {detail}" if detail else ""))


import contradiction_scorer as cs  # noqa: E402

syn = cs._load_synonyms()


def r(a, b):
    return cs.keyed_score("星河生物", "星河生物", a, b)


# ═══════════════════════════════════════════════════════════
# A0 数据真源
# ═══════════════════════════════════════════════════════════
check("1 synonyms 加载", isinstance(syn, dict) and bool(syn.get("aspects")))
check("2 aspects 36 簇（v1.2.0 长叙述句事实槽召回扩充 12 簇）",
      len(syn.get("aspects", {})) == 36, str(len(syn.get("aspects", {}))))
check("3 opposites ≥9 组且含 analyst_rating 互斥对",
      len(syn.get("opposites", {})) >= 9 and bool(syn.get("opposites", {}).get("analyst_rating")),
      str(len(syn.get("opposites", {}))))
meta = syn.get("_meta", {})
check("4 _meta.version=1.2.0 且 aspects_count=36",
      str(meta.get("version")) == "1.2.0" and meta.get("aspects_count") == 36,
      f"version={meta.get('version')} count={meta.get('aspects_count')}")
check("5 NUMERIC_ASPECTS 12 类且含 sales_volume/analyst_rating",
      len(cs.NUMERIC_ASPECTS) >= 12 and {"sales_volume", "analyst_rating"} <= set(cs.NUMERIC_ASPECTS),
      str(sorted(cs.NUMERIC_ASPECTS)))
check("6 _TERM_VALUE_ASPECTS = location/person_change/analyst_rating/listing_status",
      set(cs._TERM_VALUE_ASPECTS) == {"location", "person_change", "analyst_rating", "listing_status"},
      str(sorted(cs._TERM_VALUE_ASPECTS)))
check("7 词表精度：location 含『总部』、person_change 含『首席执行官』",
      "总部" in syn["aspects"].get("location", {}).get("zh", [])
      and "首席执行官" in syn["aspects"].get("person_change", {}).get("zh", []))

# ═══════════════════════════════════════════════════════════
# A1 term-value 冲突行为
# ═══════════════════════════════════════════════════════════
r1 = r("星河生物 公司总部位于深圳", "星河生物 公司总部位于北京")
check("8 location 深圳↔北京 判 term 词位值冲突",
      r1["score"] >= 35 and "location" in r1["conflict_slots"]
      and any("词位值冲突" in x for x in r1["reasons"]),
      f"score={r1['score']} slots={r1['conflict_slots']} reasons={r1['reasons']}")

r2 = r("星河生物 董事长赵远航辞去职务", "星河生物 董事长孙启铭")
check("9 person_change 赵远航↔孙启铭 判冲突",
      r2["score"] >= 35 and "person_change" in r2["conflict_slots"],
      f"score={r2['score']} slots={r2['conflict_slots']} reasons={r2['reasons']}")

tv = cs._build_keyed_slots("星河生物", "星河生物 董事长赵远航辞去职务", syn).get("person_change", {}).get("term_values")
check("10 person_change 值已剥离尾部动作词（不含『辞去职务』）",
      tv == ["赵远航"], str(tv))

r3 = r("星河生物 机构评级为买入 维持推荐", "星河生物 机构评级为卖出 下调评级")
check("11 analyst_rating 买入↔卖出 走 opposites 反义冲突路径",
      r3["score"] >= 35 and any("反义冲突" in x for x in r3["reasons"]),
      f"score={r3['score']} reasons={r3['reasons']}")

r4 = r("星河生物 投资评级增持", "星河生物 投资评级中性")
check("12 analyst_rating 增持↔中性 走 term 词位值冲突路径",
      r4["score"] >= 35 and any("词位值冲突" in x for x in r4["reasons"]),
      f"score={r4['score']} reasons={r4['reasons']}")

r5 = r("星河生物 评级买入 增持", "星河生物 评级卖出 减持")
check("13 双路径单槽去重：买入+增持↔卖出+减持 = 35（非 60/70）",
      r5["score"] == 35 and r5["conflict_slots"] == ["analyst_rating"],
      f"score={r5['score']} slots={r5['conflict_slots']} reasons={r5['reasons']}")

r6 = r("星河生物 递交招股书 启动上市", "星河生物 已退市 摘牌")
check("14 listing_status 启动上市↔摘牌 判冲突（新增簇已接线）",
      r6["score"] >= 35 and "listing_status" in r6["conflict_slots"],
      f"score={r6['score']} slots={r6['conflict_slots']} reasons={r6['reasons']}")

r7 = r("星河生物 销量为120万台", "星河生物 销量约95万台")
check("15 sales_volume 120万↔95万 走数值冲突路径",
      r7["score"] >= 35 and any("数值冲突" in x for x in r7["reasons"]),
      f"score={r7['score']} reasons={r7['reasons']}")

r8a = r("星河生物 净利润率5%", "星河生物 净利润5亿元")
r8b = r("星河生物 净利润率20%", "星河生物 净利润20亿元")
check("16 量纲隔离：百分比↔绝对量不判冲突（5%↔5亿 / 20%↔20亿元）",
      r8a["score"] == 0 and r8b["score"] == 0,
      f"a={r8a['score']} b={r8b['score']}")

# ═══════════════════════════════════════════════════════════
# A2 反向零误报
# ═══════════════════════════════════════════════════════════
r9 = r("星河生物 公司总部位于深圳", "星河生物 总部设于深圳")
check("17 反例 总部同值异述 → 0", r9["score"] == 0, f"score={r9['score']} reasons={r9['reasons']}")
r10 = r("星河生物 2025年营收12亿元", "星河生物 2025年营业收入12亿元")
check("18 反例 营收一致 → 0", r10["score"] == 0, f"score={r10['score']}")
r11 = r("星河生物 销量为120万台", "星河生物 销量120万台")
check("19 反例 销量相同 → 0", r11["score"] == 0, f"score={r11['score']}")

# ═══════════════════════════════════════════════════════════
# A3 健壮性 / schema
# ═══════════════════════════════════════════════════════════
filler = "该公司经营状况良好业绩稳步提升市场反响积极" * 200  # ≈ 6000 字
la = "星河生物 公司总部位于深圳 " + filler
lb = "星河生物 公司总部位于北京 " + filler
r12 = r(la, lb)
check("20 长文本（6000 字×2）不稀释，仍判 35",
      r12["score"] == 35 and "location" in r12["conflict_slots"],
      f"score={r12['score']} slots={r12['conflict_slots']}")

r13 = r("今天天气不错适合出行", "明天可能下大雨")
check("21 无方面文本不崩且 score=0", r13["score"] == 0, f"score={r13['score']}")

sa = cs._build_keyed_slots("星河生物", "星河生物 2025年营收12亿元", syn)
check("22 schema 兼容：term 方面槽含 term_values 键，非 term 方面为空列表",
      isinstance(sa.get("revenue", {}).get("term_values"), list)
      and sa.get("revenue", {}).get("term_values") == [])

# ═══════════════════════════════════════════════════════════
# 已知边界登记（非断言，修复后应改为正向断言）
# ═══════════════════════════════════════════════════════════
rb1 = r("星河生物 销量为120万台", "星河生物 销量120吨")
note("B1 sales_volume 台↔吨 量纲未识别（_UNIT_SCALE 未覆盖『台/吨』）",
     f"score={rb1['score']} reasons={rb1['reasons']} ——记为 P2-4 延伸项")
rb2 = r("星河生物 机构评级upgrade", "星河生物 机构评级downgrade")
note("B2 trend_dir 英文 upgrade/downgrade 子串命中 up/down（词边界待加固）",
     f"score={rb2['score']} reasons={rb2['reasons']} ——记为 P2-4 延伸项")
rb3 = r("星河生物 评级buy", "星河生物 评级增持")
note("B3 analyst_rating 跨语言同义 buy≡增持 未登记（opposites 缺跨语言对）",
     f"score={rb3['score']} reasons={rb3['reasons']} ——记为 P2-4 延伸项")

# ═══════════════════════════════════════════════════════════
# 汇总
# ═══════════════════════════════════════════════════════════
print(f"\nP2-4/D-4 term-value 守护: {len(PASS)} PASS / {len(FAIL)} FAIL（目标 22 断言）")
sys.exit(1 if FAIL else 0)