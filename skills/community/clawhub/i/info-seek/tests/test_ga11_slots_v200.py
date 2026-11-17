#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_ga11_slots_v200.py — GA11 键控事实槽守护测试（v2.0.0，38 断言）

覆盖：
  数据真源 / 槽抽取（主体契约·方面命中·数值就近归属·年份·中文百分比）
  同键值冲突（数值/枚举/极性·同值不冲突·量纲隔离·去重计数）
  L1-01..06 零回归 / 12 组段落语料（≥8/12 low+，4 真实差异≥medium）
  长文本不稀释 / schema 向后兼容
  B 层混合分层（表外方面动态键·max 融合·降级链·opt-in·缓存）
"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "scripts"), ROOT, os.path.join(ROOT, "core")):
    if p not in sys.path:
        sys.path.insert(0, p)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -> {detail}" if detail and not cond else ""))


import contradiction_scorer as cs

# ═══════════════════════════════════════════════════════════
# A0 数据真源
# ═══════════════════════════════════════════════════════════
syn = cs._load_synonyms()
check("1 synonym.json 加载", isinstance(syn, dict) and bool(syn.get("aspects")))
check("2 36 个方面簇（v1.2.0 长叙述句事实槽召回扩充 12 簇）",
      len(syn.get("aspects", {})) == 36, str(len(syn.get("aspects", {}))))
check("3 opposites 含互斥对",
      any(p == ["开源", "闭源"] for p in syn.get("opposites", {}).get("open_source", [])))
check("4 否定词表非空", bool(syn.get("negation_zh")) and bool(syn.get("negation_en")))

# ═══════════════════════════════════════════════════════════
# A1 槽抽取
# ═══════════════════════════════════════════════════════════
t = "宁德时代2025年三季度财报显示公司营收同比增长12%，净利润稳步提升。"
sl = cs._build_keyed_slots({"text": t}, t, syn)
check("5 命中 revenue 方面", "revenue" in sl)
check("6 营收数值就近归属(12%)",
      any(v["value"] == 12 and v["percent"] for v in sl.get("revenue", {}).get("values", [])))
check("7 年份不被误抽为指标数值",
      all(v["value"] != 2025 for v in sl.get("revenue", {}).get("values", [])))
check("8 季度序号不误抽", all(v["value"] != 3 for v in sl.get("revenue", {}).get("values", [])))

t2 = "该公司成立于2015年"
sl2 = cs._build_keyed_slots({"text": t2}, t2, syn)
check("9 年份归 founded_year",
      any(v["value"] == 2015 for v in sl2.get("founded_year", {}).get("values", [])))

t3 = "营收提升百分之二十"
sl3 = cs._build_keyed_slots({"text": t3}, t3, syn)
check("10 中文百分比 百分之二十=20",
      any(v["value"] == 20 and v["percent"] for v in sl3.get("revenue", {}).get("values", [])))

# 主体契约
sl4a = cs._build_keyed_slots({"text": "公司A营收增长20%", "entity": "公司A"}, "公司A营收增长20%", syn)
check("11 契约主体键来自 claim.entity",
      all(e.get("subject") == "公司a" for e in sl4a.values()))
sl4b = cs._build_keyed_slots({"text": "营收增长20%"}, "营收增长20%", syn)
check("12 缺省主体键为全局空串",
      all(e.get("subject") == "" for e in sl4b.values()))

# 防串味：35% 后接"利润率"不判给 profit
t4 = "营收大幅增长35%，利润率创下新高。"
sl5 = cs._build_keyed_slots({"text": t4}, t4, syn)
check("13 增长率不跨指标串味（profit 空）",
      sl5.get("profit", {}).get("values", []) == [])

# ═══════════════════════════════════════════════════════════
# A2 同键值冲突
# ═══════════════════════════════════════════════════════════
def r(a, b, ca=None, cb=None):
    return cs.score_contradiction({"text": a, **(ca or {})}, {"text": b, **(cb or {})})


r_num = r("宁德时代三季度营收同比增长12%", "宁德时代同期营收大幅增长35%")
check("14 同方面数值差异判冲突", "revenue" in r_num["conflict_slots"])
check("15 单冲突因=35 medium", r_num["score"] == 35 and r_num["severity"] == "medium")

r_same = r("宁德时代 Q3 营收增长 20%", "宁德时代三季度营收提升 20%")
check("16 同义归一+同值不冲突", r_same["score"] < 30 and r_same["conflict_slots"] == [])
r_cnpct = r("宁德时代 Q3 营收增长 20%", "宁德时代三季度营收提升百分之二十")
check("17 20% 与 百分之二十 归一不冲突", r_cnpct["score"] < 30)

r_enum = r("OpenAI 宣布 GPT-5 完全开源", "OpenAI 官方确认 GPT-5 保持闭源")
check("18 开源↔闭源反义冲突", "open_source" in r_enum["conflict_slots"])

r_year = r("该公司成立于2015年", "资料显示该公司2019年创立")
check("19 成立年份冲突", "founded_year" in r_year["conflict_slots"] and r_year["score"] >= 30)

r_unit = r("该公司营收增长 50%", "该公司营收为 50 亿元")
check("20 量纲隔离（% vs 亿 不冲突）", r_unit["score"] < 30 or "revenue" not in r_unit["conflict_slots"])

r_neg = r("X 不发布新产品", "X 刚刚发布新产品")
check("21 肯否极性冲突", r_neg["score"] >= 20)

r_abs = r("该公司2024年营收为50亿元", "另一财报显示其营收仅30亿元")
check("22 绝对值冲突（50亿 vs 30亿）", "revenue" in r_abs["conflict_slots"])

# 去重计数：同一值对落 revenue+trend_dir 只计 1 冲突因（35 非 60）
check("23 同值对跨槽去重（不抬到 high）",
      r_num["score"] == 35 and len(set(r_num["conflict_slots"])) >= 1)

# 多独立冲突 → high
rm = r("该公司2024年营收增长18%，员工数约500人，总部位于深圳，已开源核心框架。",
       "另一家媒体称该公司2024年营收下滑18%，员工数仅120人，总部位于杭州，且核心框架完全闭源。")
check("24 多独立冲突=high(85)",
      rm["severity"] == "high" and rm["score"] == 85 and len(rm["conflict_slots"]) >= 3)

# 不同主体不比
r_subj = r("公司A营收增长20%", "公司B营收增长35%",
           {"entity": "A"}, {"entity": "B"})
check("25 不同主体不判数值冲突", "revenue" not in r_subj["conflict_slots"])

# ═══════════════════════════════════════════════════════════
# A3 L1-01..06 零回归
# ═══════════════════════════════════════════════════════════
r01 = r("OpenAI 宣布 GPT-5 完全开源", "OpenAI 官方确认 GPT-5 保持闭源")
check("26 L1-01 反义对 medium", r01["score"] >= 30 and r01["severity"] == "medium")
check("27 L1-02 否定不对称≥20", r("X 不发布新产品", "X 刚刚发布新产品")["score"] >= 20)
check("28 L1-03 一致表述<30", r_same["score"] < 30)
check("29 L1-04 无关<10", r("苹果是水果", "OpenAI 发布 GPT")["score"] < 10)
r05 = r("", "")
check("30 L1-05 空文本=0/none", r05["score"] == 0 and r05["severity"] == "none")
t0 = time.time()
_ = r("OpenAI 发布 GPT-5 " * 10000, "GPT-5 闭源")
el = (time.time() - t0) * 1000
check("31 L1-06 200KB 文本<500ms", el < 500, f"{el:.0f}ms")

# ═══════════════════════════════════════════════════════════
# A4 12 组段落语料验收（≥8/12 low+，其中真实差异 4 组≥medium）
# ═══════════════════════════════════════════════════════════
# 12 组段落语料：8 组真实口径差异（期望判出 low+；前 4 组强差异 ≥medium，
# 后 4 组细微差异 low），4 组同义复述（期望 0，控制误报）。
PARAS = [
    # ── 强真实差异（4，≥medium）──────────────────────────
    ("宁德时代2025年三季度财报显示公司营收同比增长12%，净利润稳步提升，市场表现稳健。",
     "另一家媒体援引内部数据称宁德时代同期营收大幅增长35%，利润率创下新高。", "strong"),
    ("该公司在公告中表示2024年全年净利润为18亿元，符合市场预期。",
     "审计文件显示该公司2024年净利润仅6亿元，与此前公告存在明显差距。", "strong"),
    ("据报道该平台月活跃用户数达到2亿，用户规模持续扩张。",
     "第三方监测数据称该平台月活仅8000万左右，与官方口径差异较大。", "strong"),
    ("公司创始人在采访中确认下一轮融资已经完成，金额约5亿美元。",
     "知情人士透露该轮融资实际仅1亿美元，且尚未正式交割。", "strong"),
    # ── 细微真实差异（4，low+，措辞长且口径接近）────────────
    ("财报披露该企业三季度市场份额为21%，继续保持行业第一的位置。",
     "另一家调研机构给出的同期市场份额约为16%，排名第二。", "weak"),
    ("公司介绍其目前员工规模在1000人左右，团队仍在快速扩张。",
     "招聘平台数据显示该公司在岗员工约700人，扩张速度有所放缓。", "weak"),
    ("报道称该药物三期临床试验达到主要终点，疗效显著，公司计划提交上市申请。",
     "另一篇报道提到该药三期研究未达主要终点，疗效不具统计意义，上市存疑。", "weak"),
    ("管理层预计数据中心全年用电成本将下降8%，节能改造效果明显。",
     "但内部核算文件显示用电成本仅下降2%，节能改造收益低于预期。", "weak"),
    # ── 同义复述/一致（4，应判 0）──────────────────────────
    ("宁德时代三季度营业收入同比增长12%，延续增长态势。",
     "宁德时代2025年Q3营收提升了12%，盈利能力保持稳定。", "same"),
    ("报告指出该企业2023年员工总数约3000人，研发占比持续提高。",
     "另一份资料也提到截至2023年该企业雇员约3000名，研发投入加大。", "same"),
    ("官方声明该项目将继续推进，预计年底前上线。",
     "官方在另一场合表示项目按计划推进，年底前可正式上线。", "same"),
    ("公司表示其数据中心全年用电成本下降了8%，节能效果明显。",
     "公司在ESG报告中称数据中心全年用电成本降低8%，能效改善。", "same"),
]
low_plus = 0
strong_medium = 0
same_false = 0
for i, (a, b, kind) in enumerate(PARAS, 1):
    rr = r(a, b)
    flagged = rr["severity"] in ("low", "medium", "high") and rr["score"] >= 10
    if flagged:
        low_plus += 1
    if kind == "strong" and rr["severity"] in ("medium", "high"):
        strong_medium += 1
    if kind == "same" and rr["severity"] in ("medium", "high"):
        same_false += 1
check("32 段落语料 ≥8/12 判出 low 以上", low_plus >= 8, f"{low_plus}/12")
check("33 4 组强真实差异 ≥medium 且一致组零误报",
      strong_medium >= 4 and same_false == 0,
      f"strong_medium={strong_medium}/4 same_false={same_false}")

# 长文本不稀释：同语义 100 字 vs 300 字同判
short = "公司A营收增长20%"
longp = ("根据公司A发布的2025年第三季度财务报告，在扣除各项成本与税费之后，"
         "其营业收入同比显著增长了20%，延续了此前多个季度的良好上升势头，"
         "管理层在业绩说明会上多次强调了这一增长趋势，并对全年表现保持乐观预期。")
check("34 长文本不稀释（同判 low/none）",
      r(short, longp)["score"] < 30)

# schema 向后兼容
base = r("X 开源", "X 闭源")
check("35 老字段语义不变（score/severity/reasons/neg_hits/shared_slots/slot_score/neg_score）",
      all(k in base for k in ("score", "severity", "reasons", "neg_hits",
                             "shared_slots", "slot_score", "neg_score")))
check("36 新增字段（keyed_score/conflict_slots/scorer_mode）",
      all(k in base for k in ("keyed_score", "conflict_slots", "scorer_mode"))
      and base["scorer_mode"] in ("keyed", "negation"))

# ═══════════════════════════════════════════════════════════
# A5 B 层混合分层
# ═══════════════════════════════════════════════════════════
os.environ.pop("INFOSEEK_CONTRADICTION_LLM", None)
ha = "星河生物2024年股东大会宣布新任董事长为赵远航，接替创始人主持工作。"
hb = "财经记者核实到星河生物现任董事长仍为孙启铭，公司否认发生更替。"


def mock_llm(prompt, **k):
    name = "赵远航" if "赵远航" in prompt else "孙启铭"
    payload = ('{"slots":[{"subject":"星河生物","aspect":"chairman_name",'
               '"value":"' + name + '","unit":"","polarity":"neutral"}]}')
    return {"content": payload}


hyb = cs.score_contradiction_hybrid({"text": ha}, {"text": hb},
                                    enable_llm=True, llm_call_fn=mock_llm)
check("37 B 层表外方面动态键（chairman_name）检出",
      hyb["llm_used"] is True and "chairman_name" in hyb["conflict_slots"]
      and hyb["score"] >= 35)

# 降级 + opt-in 默认关
def boom(prompt, **k):
    raise RuntimeError("no provider")


hb_fail = cs.score_contradiction_hybrid(
    {"text": "Omega公司推出全新电池技术" + str(time.time())},
    {"text": "Omega被曝暂停电池研发" + str(time.time())},
    enable_llm=True, llm_call_fn=boom)
hb_off = cs.score_contradiction_hybrid(
    {"text": "Omega公司推出全新电池技术" + str(time.time())},
    {"text": "Omega被曝暂停电池研发" + str(time.time())})
check("38 LLM 异常/默认 opt-in 均降级本地不报错",
      hb_fail["llm_used"] is False and "llm_error" in hb_fail
      and hb_off["llm_used"] is False)

# ── 汇总 ────────────────────────────────────────────────────
print(f"\nGA11 键控事实槽: {len(PASS)} PASS / {len(FAIL)} FAIL（目标 38 断言）")
sys.exit(1 if FAIL else 0)