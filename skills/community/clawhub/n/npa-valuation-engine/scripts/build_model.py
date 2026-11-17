#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NPA IRR 三层估值测算模型 — 通用生成器

用法：
    python build_model.py --config deal.json --out model.xlsx
    python build_model.py --demo --out demo.xlsx          # 不提供配置则用内置示例
    python build_model.py --config deal.json --print-config  # 查看合并后的完整配置

口径：折价率 = 成交价 / 评估价（千际投行、中指研究院口径）
行号一律动态捕获，避免表结构变动导致公式静默错位。
"""
import argparse
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

# ---------------------------------------------------------------- 市场锚
CITY_ANCHORS = {
    "全国": 0.741, "上海": 0.779, "深圳": 0.944, "重庆": 0.672,
}
ANCHOR_NOTE = "2026年1-7月法拍住宅成交折价率（成交价/评估价）；来源：中指研究院法拍数据库 / 千际投行《法拍行业发展和产品研究报告(2026)》"
ANCHOR_EXTRA = [
    ("2026Q1 变卖阶段", "66.35%（折价最深，靠深度折价推动成交）"),
    ("成交阶段结构", "2026年1-7月 一拍 41.9% / 二拍 45.2%（二拍是主战场）"),
    ("重点城市清仓率", "宁波 80.8% / 上海 78.5% / 深圳 71.3%"),
]

# 不同资产类型的折价要素默认权重（可修复性 1-5）
ASSET_PROFILES = {
    "住宅": [("信息折价", 0.08, 5, "尽调补齐产权/占用/欠费信息，消除信息不对称"),
             ("时间折价", 0.06, 3, "垫资提速、预清场、缩短过户周期（一网通办约15天）"),
             ("流动性折价", 0.07, 1, "靠市场承接，难主动修复 —— 低分即风险"),
             ("风险折价", 0.05, 4, "诉讼/税费/腾退风险定价，用交易结构与条款对冲")],
    "商办": [("信息折价", 0.09, 4, "补齐租约、空置率、欠费与规划限制信息"),
             ("时间折价", 0.09, 3, "改造+招商周期长，须前置产业导入"),
             ("流动性折价", 0.13, 1, "买家范围窄，退出依赖大宗交易/REITs"),
             ("风险折价", 0.08, 3, "用途变更、消防、租约绑定等合规风险")],
    "工业": [("信息折价", 0.08, 4, "地类、环评、能耗指标、产证完整性核查"),
             ("时间折价", 0.08, 3, "改造与产线导入周期长"),
             ("流动性折价", 0.12, 2, "产业集聚区外基本无承接方"),
             ("风险折价", 0.09, 3, "工业用地出让条件、环保整改成本")],
    "股权": [("信息折价", 0.10, 4, "财报穿透、隐性负债、关联交易核查"),
             ("时间折价", 0.08, 2, "控制权交割与治理改组周期长"),
             ("流动性折价", 0.14, 1, "非上市股权退出通道极窄"),
             ("风险折价", 0.10, 3, "质押冻结、优先购买权、信息披露合规")],
}
DEFAULT_CONFIG = {
    "deal": {
        "name": "重庆渝北XX小区2栋1103", "city": "重庆", "asset_type": "住宅-二拍",
        "court_appraisal": 1000000, "start_price": 560000,
        "expected_deal_price": 580000, "market_price": 880000,
    },
    "acquisition_costs": {
        "buyer_taxes": 30000, "auction_commission": 10000,
        "eviction_cost": 20000, "legal_fees": 15000, "due_diligence": 5000,
    },
    "holding": {"quarterly_holding_rate": 0.008, "capital_cost_annual": 0.10, "target_irr": 0.15},
    "scenarios": {
        "conservative": {"exit_price_ratio": 0.88, "disposal_months": 15, "collection_mode": 1, "extra_cost_ratio": 0.03},
        "base":         {"exit_price_ratio": 0.95, "disposal_months": 12, "collection_mode": 2, "extra_cost_ratio": 0.02},
        "optimistic":   {"exit_price_ratio": 1.00, "disposal_months": 8,  "collection_mode": 2, "extra_cost_ratio": 0.01},
    },
    "scorecard": None,   # None = 按 asset_type 自动取 ASSET_PROFILES
    "horizons_months": [6, 9, 12, 15, 18, 24, 30],
}


def deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path=None):
    cfg = DEFAULT_CONFIG
    if path:
        with open(path, encoding="utf-8") as f:
            cfg = deep_merge(DEFAULT_CONFIG, json.load(f))
    if not cfg.get("scorecard"):
        at = str(cfg["deal"].get("asset_type", "住宅")).split("-")[0]
        profile = ASSET_PROFILES.get(at, ASSET_PROFILES["住宅"])
        cfg["scorecard"] = [{"type": t, "ratio": r, "repairability": p, "cost": 30000, "lever": l}
                            for t, r, p, l in profile]
    return cfg


# ---------------------------------------------------------------- 样式
GOLD_D, GOLD_M, GOLD_L = "8B6914", "D4A017", "FDF6E3"
INPUT_F, CALC_F, WARN_F = "FFF9E6", "F2F2F2", "FCE4E4"
F_TITLE = Font(name="微软雅黑", size=14, bold=True, color=GOLD_D)
F_H = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
F_BLK = Font(name="微软雅黑", size=10, bold=True, color=GOLD_D)
F_N = Font(name="微软雅黑", size=10)
F_B = Font(name="微软雅黑", size=10, bold=True)
F_S = Font(name="微软雅黑", size=9, color="808080")
F_R = Font(name="微软雅黑", size=10, color="C00000", bold=True)
F_BIG = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
BD = Border(*[Side(style="thin", color="D9D9D9")] * 4)
C_L = Alignment(horizontal="left", vertical="center", wrap_text=True)
C_C = Alignment(horizontal="center", vertical="center")
C_R = Alignment(horizontal="right", vertical="center")
FILL_H = PatternFill("solid", fgColor=GOLD_D)
FILL_BLK = PatternFill("solid", fgColor=GOLD_L)
FILL_IN = PatternFill("solid", fgColor=INPUT_F)
FILL_CALC = PatternFill("solid", fgColor=CALC_F)
FILL_WARN = PatternFill("solid", fgColor=WARN_F)
FILL_ACC = PatternFill("solid", fgColor=GOLD_M)
NUM, NUM2, PCT, PCT2 = '#,##0', '#,##0.00', '0.0%', '0.00%'


def build(cfg, out_path):
    d, ac = cfg["deal"], cfg["acquisition_costs"]
    ho, sc = cfg["holding"], cfg["scenarios"]
    horizons = cfg["horizons_months"]
    wb = Workbook()
    wb.remove(wb.active)          # 去掉 openpyxl 默认空表，交付件不留空白页
    wb.calculation.fullCalcOnLoad = True
    ROW = {}

    # ============================================ 输入假设
    wi = wb.create_sheet("输入假设")
    wi.sheet_view.showGridLines = False
    for k, v in {'A': 32, 'B': 18, 'C': 18, 'D': 18}.items():
        wi.column_dimensions[k].width = v
    wi.merge_cells("A1:D1")
    wi["A1"] = "② 输入假设　（黄色格=可填；灰色格=公式，勿动）"
    wi["A1"].font = F_TITLE
    wi.row_dimensions[1].height = 24

    def hdr(sh, r, text):
        sh.merge_cells(f"A{r}:D{r}")
        c = sh[f"A{r}"]; c.value = text; c.font = F_BLK; c.fill = FILL_BLK; c.border = BD
        for col in "BCD":
            sh[f"{col}{r}"].border = BD
        return r + 1

    def prow(sh, r, k, vals, is_input=True, fmt=NUM, key=None):
        sh[f"A{r}"] = k; sh[f"A{r}"].font = F_N; sh[f"A{r}"].alignment = C_L; sh[f"A{r}"].border = BD
        for i, col in enumerate("BCD"):
            c = sh[f"{col}{r}"]
            if i < len(vals):
                c.value = vals[i]
            c.font = F_N; c.alignment = C_R; c.border = BD; c.number_format = fmt
            c.fill = FILL_IN if is_input else FILL_CALC
        if key:
            ROW[key] = r
        return r + 1

    r = 3
    r = hdr(wi, r, "【一】标的基本信息")
    r = prow(wi, r, "标的名称", [d.get("name", "")], fmt='General')
    r = prow(wi, r, "所在城市", [d.get("city", "")], fmt='General')
    r = prow(wi, r, "资产类型", [d.get("asset_type", "")], fmt='General')
    r = prow(wi, r, "法院评估价(元)", [d["court_appraisal"]], key='eval')
    r = prow(wi, r, "起拍价(元)", [d["start_price"]], key='start')
    r = prow(wi, r, "预估成交价(元)", [d["expected_deal_price"]], key='deal')
    r = prow(wi, r, "对标市场价(元)", [d["market_price"]], key='mkt')
    r = prow(wi, r, "名义折价率(成交价/评估价)", [f"=B{ROW['deal']}/B{ROW['eval']}"], is_input=False, fmt=PCT)
    r = prow(wi, r, "真实折价率(成交价/市场价)", [f"=B{ROW['deal']}/B{ROW['mkt']}"], is_input=False, fmt=PCT)

    r += 1
    r = hdr(wi, r, "【二】一次性取得与处置成本")
    r = prow(wi, r, "成交价(元)", [f"=B{ROW['deal']}"], is_input=False, key='price')
    r = prow(wi, r, "买方承担税费(元)", [ac.get("buyer_taxes", 0)])
    r = prow(wi, r, "拍卖佣金/辅拍服务费(元)", [ac.get("auction_commission", 0)])
    r = prow(wi, r, "清场腾退费(元)", [ac.get("eviction_cost", 0)])
    r = prow(wi, r, "律师/诉讼/执行费(元)", [ac.get("legal_fees", 0)])
    r = prow(wi, r, "尽调/评估/差旅(元)", [ac.get("due_diligence", 0)])
    r = prow(wi, r, "取得总成本(元)", [f"=SUM(B{ROW['price']}:B{r-1})"], is_input=False, key='C')

    r += 1
    r = hdr(wi, r, "【三】持有成本与资金")
    r = prow(wi, r, "季度持有成本率(按取得成本)", [ho["quarterly_holding_rate"]], fmt=PCT2, key='hc')
    r = prow(wi, r, "资金成本(年化)", [ho["capital_cost_annual"]], fmt=PCT, key='wacc')
    r = prow(wi, r, "目标IRR门槛(年化)", [ho["target_irr"]], fmt=PCT, key='thr')

    r += 1
    r = hdr(wi, r, "【四】三情景假设")
    r = prow(wi, r, "情景", ["保守", "基准", "乐观"], fmt='General', key='hdr_s')
    wi[f"B{ROW['hdr_s']}"].fill = FILL_WARN
    r = prow(wi, r, "退出售价系数(占对标市场价)",
             [sc["conservative"]["exit_price_ratio"], sc["base"]["exit_price_ratio"], sc["optimistic"]["exit_price_ratio"]],
             fmt=PCT, key='f')
    r = prow(wi, r, "处置周期(月)",
             [sc["conservative"]["disposal_months"], sc["base"]["disposal_months"], sc["optimistic"]["disposal_months"]],
             key='mo')
    r = prow(wi, r, "回款方式(1=一次性/2=分3期)",
             [sc["conservative"]["collection_mode"], sc["base"]["collection_mode"], sc["optimistic"]["collection_mode"]],
             key='m')
    r = prow(wi, r, "追加成本系数(占取得总成本)",
             [sc["conservative"]["extra_cost_ratio"], sc["base"]["extra_cost_ratio"], sc["optimistic"]["extra_cost_ratio"]],
             fmt=PCT, key='ac')
    r = prow(wi, r, "处置季度数 n", [f"=ROUNDUP({c}{ROW['mo']}/3,0)" for c in "BCD"],
             is_input=False, key='n')
    anchor = CITY_ANCHORS.get(d.get("city", ""), CITY_ANCHORS["全国"])
    wi.merge_cells(f"A{r}:D{r}")
    wi[f"A{r}"] = (f"提示：{d.get('city','全国')}法拍住宅成交折价率锚 ≈ {anchor:.1%}（成交价/评估价），"
                   f"据此校核上方『退出售价系数』是否合理。")
    wi[f"A{r}"].font = F_R; wi[f"A{r}"].alignment = C_L

    EVAL = f"'输入假设'!$B${ROW['eval']}"
    MKT = f"'输入假设'!$B${ROW['mkt']}"
    CTOT = f"'输入假设'!$B${ROW['C']}"
    HC = f"'输入假设'!$B${ROW['hc']}"
    WACC = f"'输入假设'!$B${ROW['wacc']}"
    THR = f"'输入假设'!$B${ROW['thr']}"

    def COL(col, key):
        return f"'输入假设'!{col}${ROW[key]}"

    # ============================================ 使用说明
    ws = wb.create_sheet("使用说明", 0)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions['A'].width = 4
    ws.column_dimensions['B'].width = 22
    ws.column_dimensions['C'].width = 92
    rr = 1
    ws.merge_cells(f"B{rr}:C{rr}")
    ws[f"B{rr}"] = f"NPA / 法拍 估值测算模型　·　{d.get('name','')}"
    ws[f"B{rr}"].font = F_TITLE
    ws.row_dimensions[rr].height = 26
    rr += 1
    ws.merge_cells(f"B{rr}:C{rr}")
    ws[f"B{rr}"] = f"{d.get('city','')} · {d.get('asset_type','')}　|　填入假设即自动出：三情景 IRR + MOIC 双指标、敏感性矩阵、折价可修复性打分"
    ws[f"B{rr}"].font = F_S

    def sblk(r_, text):
        ws.merge_cells(f"B{r_}:C{r_}")
        c = ws[f"B{r_}"]; c.value = text; c.font = F_BLK; c.fill = FILL_BLK; c.border = BD
        ws[f"C{r_}"].border = BD
        return r_ + 1

    def srow(r_, k, v):
        ws[f"B{r_}"] = k; ws[f"B{r_}"].font = F_B; ws[f"B{r_}"].alignment = C_L; ws[f"B{r_}"].border = BD
        ws[f"C{r_}"] = v; ws[f"C{r_}"].font = F_N; ws[f"C{r_}"].alignment = C_L; ws[f"C{r_}"].border = BD
        return r_ + 1

    rr += 1
    rr = sblk(rr, "一、怎么用（三步）")
    rr = srow(rr, "第1步", "在【输入假设】填黄色格：标的信息 → 取得成本 → 持有与资金 → 三情景假设。灰色格是公式，别动。")
    rr = srow(rr, "第2步", "看【三情景现金流】：每情景年化 IRR、MOIC、NPV 自动算出。【敏感性分析】看『卖价×处置周期』对 IRR 的杀伤力。")
    rr = srow(rr, "第3步", "用【折价打分卡】判断这单值不值得做：可修复折价占比 > 50% 才是好标的；< 30% 建议放弃。")
    rr += 1
    rr = sblk(rr, "二、口径陷阱（必读，最容易错的地方）")
    rr = srow(rr, "折价率两种口径", "① 折扣率 = 成交价 ÷ 评估价（千际投行/中指研究院口径，越高 = 越接近评估价）；② 折价幅度 = 1 − 成交价 ÷ 评估价（克而瑞口径，越高 = 越便宜）。两者互为 1 的补数，混用必错。")
    rr = srow(rr, "本模型口径", "全部采用 ① 成交价 ÷ 评估价。全国 2025 年、2026 年 1-7 月平均均为 74.1%，即约『七四折』，不是打了 74.1% 的折。")
    rr = srow(rr, "更致命的第二层", "评估价 ≠ 市场价（评估价滞后且偏高）。故本模型另算【真实折价率 = 成交价 ÷ 对标市场价】，这才是真安全边际。")
    rr += 1
    rr = sblk(rr, "三、定价锚参考")
    for k in ["全国", "上海", "深圳", "重庆"]:
        rr = srow(rr, k, f"{CITY_ANCHORS[k]:.1%}")
    for k, v in ANCHOR_EXTRA:
        rr = srow(rr, k, v)
    rr = srow(rr, "数据来源", ANCHOR_NOTE)
    rr += 1
    rr = sblk(rr, "四、核心公式（可审计）")
    rr = srow(rr, "资产处置价值", "＝ 可实现市场价值 − 交易与交付成本 − 风险损失 − 资金时间成本（千际投行原文口径）")
    rr = srow(rr, "年化 IRR", "＝ (1 + 季度IRR) ^ 4 − 1（现金流按季度排布）")
    rr = srow(rr, "MOIC", "＝ 总回收 ÷ 总投入（IRR 看效率，MOIC 看绝对倍数；背离 = 钱压得久）")
    rr = srow(rr, "出手纪律", "保守情景 IRR 仍 ≥ 门槛才出手（致远互联口径）")
    rr += 1
    rr = srow(rr, "风险提示", "本模型为决策辅助工具，不构成投资建议。拍卖公告、执行裁定、评估报告、权属登记、实地看样须独立核验。")

    # ============================================ 三情景现金流
    wc = wb.create_sheet("三情景现金流")
    wc.sheet_view.showGridLines = False
    for k, v in {'A': 10, 'B': 18, 'C': 18, 'D': 18, 'E': 44}.items():
        wc.column_dimensions[k].width = v
    wc.merge_cells("A1:E1")
    wc["A1"] = "③ 三情景现金流与回报　（单位：元；现金流按季度排布）"
    wc["A1"].font = F_TITLE
    wc.row_dimensions[1].height = 24
    wc.merge_cells("A2:E2")
    wc["A2"] = "口径：t=0 为取得总成本；持有期每季度计提持有成本；退出季度另扣追加成本。回款方式=2（分3期）时按 40%/30%/30% 在最后三个季度到账。"
    wc["A2"].font = F_S
    for i, col in enumerate("ABCDE"):
        wc[f"{col}4"] = ["季度 t", "保守", "基准", "乐观", "说明"][i]
        wc[f"{col}4"].font = F_H; wc[f"{col}4"].fill = FILL_H
        wc[f"{col}4"].alignment = C_C; wc[f"{col}4"].border = BD
    for i in range(17):
        rw = 5 + i
        wc[f"A{rw}"] = i; wc[f"A{rw}"].font = F_N; wc[f"A{rw}"].alignment = C_C; wc[f"A{rw}"].border = BD
        wc[f"E{rw}"].font = F_S; wc[f"E{rw}"].alignment = C_L
        for col in "BCD":
            N, F_, M_, AC = COL(col, 'n'), COL(col, 'f'), COL(col, 'm'), COL(col, 'ac')
            fml = (f"=IF($A{rw}=0,-{CTOT},IF($A{rw}>{N},0,"
                   f"-{CTOT}*{HC}+{MKT}*{F_}"
                   f"*IF(AND({M_}=2,{N}>=3),"
                   f"IF($A{rw}={N}-2,0.4,IF($A{rw}={N}-1,0.3,IF($A{rw}={N},0.3,0))),"
                   f"IF($A{rw}={N},1,0))"
                   f"-IF($A{rw}={N},{CTOT}*{AC},0)))")
            c = wc[f"{col}{rw}"]; c.value = fml; c.font = F_N; c.number_format = NUM
            c.border = BD; c.alignment = C_R
    wc["E5"] = "取得总成本（成交价+税费+清场+律师+尽调）"
    wc["E6"] = "持有期：每季度计提持有成本"
    for col, scn, lab in (("B", "conservative", "保守"), ("C", "base", "基准"), ("D", "optimistic", "乐观")):
        n_q = -(-sc[scn]["disposal_months"] // 3)
        wc[f"E{5 + n_q}"] = f"{lab}情景处置季度（t={n_q}）"
    LAB = [
        ("净收益合计(元)", lambda c: f"=SUM({c}5:{c}21)", NUM, F_N, FILL_CALC),
        ("总投入(元)", lambda c: f"=ABS(SUMIF({c}5:{c}21,\"<0\"))", NUM, F_N, FILL_CALC),
        ("总回收(元)", lambda c: f"=SUMIF({c}5:{c}21,\">0\")", NUM, F_N, FILL_CALC),
        ("MOIC(倍数)", lambda c: f"=IFERROR(SUMIF({c}5:{c}21,\">0\")/ABS(SUMIF({c}5:{c}21,\"<0\")),\"NA\")", '0.00"x"', F_BIG, FILL_ACC),
        ("IRR(年化)", lambda c: f"=IFERROR((1+IRR({c}5:{c}21))^4-1,\"NA\")", PCT, F_BIG, FILL_ACC),
        ("NPV(元)", lambda c: f"=IFERROR(NPV((1+{WACC})^(1/4)-1,{c}6:{c}21)+{c}5,\"NA\")", NUM, F_N, FILL_CALC),
        ("达标判定(IRR≥门槛)", lambda c: f"=IF(ISNUMBER({c}26),IF({c}26>={THR},\"达标 ✓\",\"不达标 ✗\"),\"NA\")", 'General', F_BIG, FILL_ACC),
    ]
    rw = 22
    for lab, fn, fmt, fnt, fl in LAB:
        wc[f"A{rw}"] = lab; wc[f"A{rw}"].font = F_B; wc[f"A{rw}"].alignment = C_L; wc[f"A{rw}"].border = BD
        for col in "BCD":
            c = wc[f"{col}{rw}"]; c.value = fn(col); c.font = fnt; c.number_format = fmt
            c.border = BD; c.alignment = C_C; c.fill = fl
        rw += 1
    wc[f"A{rw+1}"] = "读法：MOIC 看赚了几倍，IRR 看钱回来的速度。两者背离（MOIC 高但 IRR 低）= 钱压得久，法拍最常见的死法。"
    wc[f"A{rw+1}"].font = F_R

    # ============================================ 敏感性分析
    ws2 = wb.create_sheet("敏感性分析")
    ws2.sheet_view.showGridLines = False
    ws2.column_dimensions['A'].width = 22
    for i in range(2, 12):
        ws2.column_dimensions[get_column_letter(i)].width = 11
    ws2.merge_cells("A1:K1")
    ws2["A1"] = "④ 敏感性分析　年化 IRR 矩阵（退出售价系数 × 处置周期）"
    ws2["A1"].font = F_TITLE
    ws2.merge_cells("A2:K2")
    ws2["A2"] = "口径：按『期末一次性退出』测算，年化IRR =（净回收 ÷ 取得总成本）^(4÷处置季度数) − 1。持有成本与追加成本按【输入假设】基准情景参数计提。"
    ws2["A2"].font = F_S
    ws2["A4"] = "售价系数 \\ 周期(月)"
    ws2["A4"].font = F_H; ws2["A4"].fill = FILL_H; ws2["A4"].alignment = C_C; ws2["A4"].border = BD
    for j, p in enumerate(horizons):
        c = ws2.cell(row=4, column=2 + j, value=p)
        c.font = F_H; c.fill = FILL_H; c.alignment = C_C; c.border = BD
    coeffs = [round(1.05 - 0.05 * i, 2) for i in range(len(horizons) + 5)]
    for i, f in enumerate(coeffs):
        rw = 5 + i
        a = ws2.cell(row=rw, column=1, value=f)
        a.font = F_B; a.number_format = PCT; a.alignment = C_C; a.border = BD; a.fill = FILL_BLK
        for j, p in enumerate(horizons):
            col = get_column_letter(2 + j)
            fml = (f"=IFERROR((({MKT}*$A{rw}-{CTOT}*{COL('C','ac')}"
                   f"-{CTOT}*{HC}*({col}$4/3))/{CTOT})^(4/({col}$4/3))-1,\"NA\")")
            c = ws2.cell(row=rw, column=2 + j, value=fml)
            c.font = F_N; c.number_format = PCT; c.alignment = C_C; c.border = BD
    ws2.cell(row=6 + len(coeffs), column=1,
             value="读法：行=卖得贵不贵，列=耗得久不久。找到『保守售价系数』那一行，看 IRR 在哪个周期区间跌破目标门槛 —— 那就是出手红线。").font = F_R

    # ============================================ 折价打分卡
    w3 = wb.create_sheet("折价打分卡")
    w3.sheet_view.showGridLines = False
    for k, v in {'A': 16, 'B': 14, 'C': 14, 'D': 16, 'E': 20, 'F': 18, 'G': 12, 'H': 38}.items():
        w3.column_dimensions[k].width = v
    w3.merge_cells("A1:H1")
    w3["A1"] = "⑤ 折价四要素打分卡（千际投行框架：信息 / 时间 / 流动性 / 风险折价）"
    w3["A1"].font = F_TITLE
    w3.merge_cells("A2:H2")
    w3["A2"] = "核心判据：可主动修复的折价才是真收益。折价幅度填『占评估价的比例』；可修复性 1-5 分（5=我方完全有能力修复）。"
    w3["A2"].font = F_S
    for j, h in enumerate(["折价类型", "折价幅度", "可修复性(1-5)", "修复成本(元)",
                           "修复后释放价值(元)", "净修复收益(元)", "修复ROI", "我方修复抓手"]):
        c = w3.cell(row=4, column=1 + j, value=h)
        c.font = F_H; c.fill = FILL_H; c.alignment = C_C; c.border = BD
    rw = 5
    for item in cfg["scorecard"]:
        w3.cell(row=rw, column=1, value=item["type"]).font = F_B
        c = w3.cell(row=rw, column=2, value=item["ratio"]); c.number_format = PCT; c.fill = FILL_IN
        c = w3.cell(row=rw, column=3, value=item["repairability"]); c.fill = FILL_IN
        c = w3.cell(row=rw, column=4, value=item["cost"]); c.number_format = NUM; c.fill = FILL_IN
        c = w3.cell(row=rw, column=5, value=f"=B{rw}*{EVAL}*C{rw}/5"); c.number_format = NUM; c.fill = FILL_CALC
        c = w3.cell(row=rw, column=6, value=f"=E{rw}-D{rw}"); c.number_format = NUM; c.fill = FILL_CALC
        c = w3.cell(row=rw, column=7, value=f"=IFERROR(F{rw}/D{rw},\"NA\")"); c.number_format = PCT; c.fill = FILL_CALC
        w3.cell(row=rw, column=8, value=item.get("lever", "")).font = F_S
        for j in range(1, 9):
            w3.cell(row=rw, column=j).border = BD
            w3.cell(row=rw, column=j).alignment = C_L if j in (1, 8) else C_C
        rw += 1
    TOT = rw
    w3.cell(row=TOT, column=1, value="合计").font = F_B
    for j, fml in [(2, f"=SUM(B5:B{TOT-1})"), (4, f"=SUM(D5:D{TOT-1})"), (5, f"=SUM(E5:E{TOT-1})"),
                   (6, f"=SUM(F5:F{TOT-1})"), (7, f"=IFERROR(F{TOT}/D{TOT},\"NA\")"),
                   (3, f"=IFERROR(E{TOT}/(B{TOT}*{EVAL})*5,\"NA\")")]:
        c = w3.cell(row=TOT, column=j, value=fml)
        c.font = F_B; c.fill = FILL_BLK
        c.number_format = PCT if j in (2, 7) else (NUM2 if j == 3 else NUM)
    for j in range(1, 9):
        w3.cell(row=TOT, column=j).border = BD
        w3.cell(row=TOT, column=j).alignment = C_L if j == 1 else C_C
    rr = TOT + 2
    w3.cell(row=rr, column=1, value="结论区").font = F_BLK
    rr += 1
    DEF = f"IFERROR(E{TOT}/(B{TOT}*{EVAL}),0)"
    for k, fml, fmt in [
        ("评估价(元)", f"={EVAL}", NUM),
        ("总折价金额(元)", f"=B{TOT}*{EVAL}", NUM),
        ("可修复折价金额(元)", f"=E{TOT}", NUM),
        ("不可修复折价金额(元)", f"=B{TOT}*{EVAL}-E{TOT}", NUM),
        ("可修复折价占比", f"=IFERROR(E{TOT}/(B{TOT}*{EVAL}),\"NA\")", PCT),
        ("净修复收益合计(元)", f"=F{TOT}", NUM),
        ("判定", f'=IF({DEF}>0.5,"标的可做 ✓ 可修复折价占主导",IF({DEF}>=0.3,"谨慎参与：部分折价可修复","建议放弃 ✗ 折价基本不可修复"))', 'General'),
    ]:
        w3.cell(row=rr, column=1, value=k).font = F_B
        c = w3.cell(row=rr, column=2, value=fml); c.number_format = fmt; c.fill = FILL_CALC; c.font = F_B
        w3.cell(row=rr, column=1).border = BD; c.border = BD
        rr += 1
    rr += 1
    w3.cell(row=rr, column=1, value="注：释放价值 = 折价幅度 × 评估价 × (可修复性/5)。买入时你承担了全部折价，但只有『我方有能力修复』的部分才能变成真实收益，其余是市场公允定价。本卡判『值不值得研究』，IRR 判『这个价格买不买』，两者合看。").font = F_S

    wb.active = 0
    for sh in wb.worksheets:
        sh.page_setup.orientation = 'landscape'
        sh.page_setup.fitToWidth = 1
        sh.page_setup.fitToHeight = 0
        sh.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
        sh.print_options.horizontalCentered = True
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    wb.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="NPA IRR 三层估值测算模型 — 通用生成器")
    ap.add_argument("--config", help="标的数据 JSON（见 templates/deal_template.json）")
    ap.add_argument("--out", default="NPA_IRR模型.xlsx", help="输出 xlsx 路径")
    ap.add_argument("--demo", action="store_true", help="使用内置示例配置")
    ap.add_argument("--print-config", action="store_true", help="打印合并后的完整配置")
    a = ap.parse_args()
    cfg = load_config(None if a.demo else a.config)
    if a.print_config:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        return
    path = build(cfg, a.out)
    print(f"OK 已生成: {os.path.abspath(path)}")


if __name__ == "__main__":
    main()
