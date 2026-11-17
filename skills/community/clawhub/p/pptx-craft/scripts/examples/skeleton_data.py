# -*- coding: utf-8 -*-
"""
skeleton_data.py — 最小数据模型骨架 (#6 最小骨架优先)
================================================================================
不写 HTML、直接从"数据模型"生成一页可编辑 PPT 的最小示例。
证明：引擎内核只认数据模型，HTML 只是可选兄弟产物。

用法:
  cd scripts && python examples/skeleton_data.py
  → 生成 skeleton_out.pptx（单页，含 1 个 KPI 卡 + 1 个对比卡）

数据模型要点:
  · KpiCard(deck, box, group, kpi)   kpi = {"label","value","sub",可选"color"}
  · CompareCard(deck, box, group, cmp) cmp = {"label","value","sub"}
  · 所有元素放进 Deck()，最后 add_slide_from_deck(prs, deck)
  · 写文件前必须 validate(deck.recs) 几何校验（0 错误才可交付）
"""
import os, sys
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_SCRIPT_DIR))  # 指向上级 scripts/ 目录（引擎所在）
import pptx_flex_engine as eng

eng.configure()  # 默认 1440×680 虚拟画布
prs = eng.new_presentation()
deck = eng.Deck()

# KPI 卡片：左上
eng.KpiCard(deck, eng.Box(80, 200, 360, 200), "kpi1",
            {"label": "DAU", "value": "12.4万", "sub": "环比 +18%", "color": eng.TOK()["color"]["blue"]})

# 对比卡片：右上
eng.CompareCard(deck, eng.Box(500, 200, 360, 200), "cmp1",
                {"label": "次留", "value": "45%", "sub": "行业基准 38%"})

# 几何校验（L1）：0 错误才写文件
errs, warns = eng.validate(deck.recs)
assert not errs, f"几何错误: {errs}"

eng.add_slide_from_deck(prs, deck)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skeleton_out.pptx")
prs.save(out)
print(f"✅ 已生成 {out}（1 页，0 几何错误）")
