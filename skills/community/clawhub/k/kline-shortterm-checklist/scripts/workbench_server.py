#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""workbench_server.py — 实时选股工作台后端（零依赖，仅标准库）。

提供:
  GET  /                ->  serving workbench_realtime.html
  GET/POST /api/run     -> 实时重跑 东财初筛(select_stocks.py) + 新浪K线(kline_history.py --top 40 --json)
                           + 东财分时强度自取(intraday_strength_em 内嵌) + 合并(intraday_strength_wind.py --merge)
                           -> 写 candidates.json / screen_meta.json / kline_data.json / intraday_raw.json
                              / intraday_strength.json -> 计算并返回 payload JSON
  GET  /api/data        -> 读取盘上 candidates/kline/announcement/intraday/screen_meta
                           计算 payload JSON（不重跑，展示当前快照 / 最近一次实时结果）

判定逻辑严格复用 kline-shortterm-checklist 的 report_html.py（verdict / is_st / deep），
保证工作台与筛查报告结论零偏差。

数据来源分工（自服务闭环）：
  · 初筛 / 日K / 分时强度  —— 工作台「实时重新筛查」一键自取（东财 push2delay / 新浪日K），无需 Agent。
  · Wind 公告核查(announcement_check.json) —— 仍由 Agent 跑完写盘（Wind MCP 仅 Agent 可调，属技能硬性边界）；
    未跑时工作台自动回落 👁，不影响其他逻辑。
"""
import json, os, sys, subprocess, datetime, re, threading, urllib.request, ssl, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CWD = os.path.dirname(os.path.abspath(__file__))
# CWD = 数据目录：启动器复制到用户工作区后运行 → 此处即用户工作区（候选/K线/分时等写这里）。
# 若直接在技能目录运行，CWD 与 SKILL 同目录，数据也写技能目录，无碍。
#
# SKILL = 技能脚本目录（select_stocks.py / kline_history.py / intraday_strength_wind.py 所在）。
# 注意：启动器只复制 workbench_server.py / workbench_realtime.html 到工作区，并不会复制其它
# 技能脚本；因此 SKILL 不能简单取 __file__ 的目录（复制到工作区后那里没有这些脚本），
# 必须回退到固定的用户级技能路径。
def _find_skill():
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(here, "select_stocks.py")):
        return here
    for cand in (
        r"C:\Users\22786\.workbuddy\skills\kline-shortterm-checklist\scripts",
        os.path.join(os.path.expanduser("~"), ".workbuddy", "skills",
                     "kline-shortterm-checklist", "scripts"),
    ):
        if os.path.exists(os.path.join(cand, "select_stocks.py")):
            return cand
    return here  # 最后的兜底
SKILL = _find_skill()
VENV_PY = r"C:\Users\22786\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

PAT_MEAN = {
    "狮子张口": "下跌末端抛压枯竭，多头启动", "挖坑埋牛": "刻意洗盘挖坑，挖完往往起涨",
    "阴阳鉴攻": "横盘蓄势结束，选择向上", "回眸一笑": "回踩确认，二次启动",
    "鱼跃龙门": "趋势反转确认", "葵花向阳": "上涨中继洗盘后继续",
    "美人长腿": "下方有强承接，见底信号", "旭日东升": "空头力竭，多头反包",
    "倒锤头线": "探顶试盘/潜在反转，需次日确认", "希望之星": "经典见底组合",
    "岛形反转": "情绪急转，底部反转强信号", "上涨分手": "上涨中继，短暂洗盘后延续",
}

def norm_key(code):
    return code[2:] if code[:2] in ("sh", "sz", "bj") else code

def to_wind(code):
    c = norm_key(code)
    if c[0] == "6":
        return c + ".SH"
    if c[0] in ("0", "3"):
        return c + ".SZ"
    if c[0] in ("8", "4"):
        return c + ".BJ"
    return c + ".SH"

def to_secid(code):
    """6 位代码 → 东财 secid（沪 1. / 深 0.）。"""
    c = norm_key(code)
    if c[0] == "6":
        return "1." + c
    return "0." + c

def is_st(c):
    return "ST" in (c.get("name") or "").upper()

def ann_get(ach, code):
    return (ach or {}).get(norm_key(code))

def intraday_get(istr, code):
    return (istr or {}).get(norm_key(code))

def verdict(c, ach=None):
    a = ann_get(ach, c["code"]) if ach else None
    if is_st(c):
        return ("不买", "ST风险警示·九不买#6")
    if a and a.get("checked"):
        if a.get("reduction"):
            return ("不买", "减持·九不买#5")
        if a.get("penalty"):
            return ("不买", "违规/监管·九不买#6")
    if c.get("pe") is not None and c["pe"] < 0:
        return ("不买", "亏损·九不买#6")
    if c.get("pe") is not None and c["pe"] > 200:
        return ("观察", "估值偏高·谨慎")
    if a and a.get("checked") and a.get("earnings_warn"):
        return ("观察", "业绩预减·九不买#6 需核")
    return ("符合", "通过·待人工核查")

def load_json(name, default=None):
    p = os.path.join(CWD, name)
    if not os.path.exists(p):
        return default
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def compute_payload(run_mode="data"):
    cands = load_json("candidates.json", [])
    kline_list = load_json("kline_data.json", [])
    kl = {norm_key(d["code"]): d for d in kline_list}
    meta = load_json("screen_meta.json", {}) or {}
    ach = load_json("announcement_check.json", {}) or {}
    istr = load_json("intraday_strength.json", {}) or {}

    data_date = (meta.get("data_date")
                 or (next(iter(kl.values())).get("date") if kl else None)
                 or "最近交易日")
    intraday = bool(meta.get("intraday"))

    # ---- 全候选行 ----
    rows = []
    for c in cands:
        v, note = verdict(c, ach)
        k = kl.get(c["code"])
        trend = ("多头排列✓" if k and k.get("multi") else
                 ("站上均线·未完全多头" if k else "—"))
        isd = intraday_get(istr, c["code"])
        if isd and isd.get("covered"):
            sv = isd["verdict"]
            sdet = "%.0f%%·%+.1f%%" % (isd["above_ratio"] * 100, isd["excess"])
            strength = {"verdict": sv, "detail": sdet, "partial": bool(isd.get("partial")),
                        "last_time": isd.get("last_time"), "source": isd.get("source", "东财")}
        else:
            strength = None
        trigs = []
        if is_st(c): trigs.append("ST风险警示#6")
        a = ann_get(ach, c["code"])
        if a and a.get("checked"):
            if a.get("reduction"): trigs.append("减持#5")
            if a.get("penalty"): trigs.append("违规/监管#6")
            if a.get("earnings_warn"): trigs.append("业绩预减#6")
        if c.get("pe") is not None and c["pe"] < 0: trigs.append("亏损#6")
        if c.get("pe") is not None and c["pe"] > 200: trigs.append("估值偏高")
        tp = trade_plan(c, k)
        if v == "不买":
            tp = dict(tp); tp["action"] = "回避"; tp["ac"] = "bad"
            tp["reason"] = "九不买触发，纪律上不参与买卖，买卖信号仅供参考"
        rows.append({
            "code": c["code"], "name": c["name"], "price": c.get("price"), "chg": c.get("chg"),
            "vr": c.get("vr"), "to": c.get("to"), "fm": c.get("fm"), "pe": c.get("pe"),
            "st": bool(c.get("st")), "trend": trend, "strength": strength,
            "verdict": v, "trigs": trigs,
            "trade_action": tp["action"], "trade_ac": tp["ac"],
        })

    # ---- 九不买剔除分组 ----
    excl_groups = {}
    for r in rows:
        if r["verdict"] == "不买":
            for t in r["trigs"]:
                excl_groups.setdefault(t, []).append({"code": r["code"], "name": r["name"]})

    # ---- 深度研判候选（与 report_html 一致）----
    deep_all = bool(meta.get("deep_all"))
    if deep_all:
        prio = [c for c in cands if c["code"] in kl]
    else:
        prio = [c for c in cands if c["code"] in kl and (
            kl[c["code"]].get("multi") or
            (c.get("pe") and c["pe"] > 0 and c["pe"] < 20) or
            kl[c["code"]].get("near_high", 99) < 1)]
    prio.sort(key=lambda x: -x["vr"])
    if not deep_all:
        prio = prio[:10]

    deep = [build_deep(c, kl.get(c["code"]), ann_get(ach, c["code"]),
                       intraday_get(istr, c["code"]), intraday) for c in prio]

    # ---- KPI ----
    total = len(cands)
    excl = sum(1 for r in rows if r["verdict"] == "不买")
    conf = total - excl
    multi = sum(1 for c in cands if kl.get(c["code"], {}).get("multi") and verdict(c, ach)[0] != "不买")
    kpi = {"total": total, "excl": excl, "conf": conf, "multi": multi}

    # ---- 分时强度分布 ----
    idist = {"强": 0, "中": 0, "弱": 0, "未覆盖": 0}
    for r in rows:
        if r["strength"]:
            idist[r["strength"]["verdict"]] = idist.get(r["strength"]["verdict"], 0) + 1
        else:
            idist["未覆盖"] += 1

    # ---- 覆盖状态 ----
    ann_cov = sum(1 for c in cands if ann_get(ach, c["code"]) and ann_get(ach, c["code"]).get("checked"))
    id_cov = sum(1 for c in cands if (intraday_get(istr, c["code"]) or {}).get("covered"))
    wind = {
        "announcement_covered": ann_cov, "intraday_covered": id_cov, "total": total,
        "present": bool(ach) or bool(istr),
        "intraday_partial": intraday,
        "intraday_source": "东财push2delay(自取)" if id_cov else "",
    }

    source_note = meta.get("source_note") or (
        "东方财富 push2delay（初筛+分时）/ 新浪日K"
        + (" / Wind 公告核查" if ach else "（公告核查未跑·👁）"))

    return {
        "meta": {
            "data_date": data_date, "source_note": source_note, "run_mode": run_mode,
            "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "intraday_partial": intraday,
        },
        "kpi": kpi, "rows": rows, "excl_groups": excl_groups, "deep": deep,
        "intraday_dist": idist, "wind": wind,
        "announcement_check": ach, "intraday_strength": istr,
    }

def build_deep(c, k, a, isd, intraday):
    if not k:
        return {"code": c["code"], "name": c["name"], "nokline": True}
    multi_txt = "是（MA5>MA10>MA20 且价>MA5）" if k.get("multi") else "否（价站上均线，但 MA10 仍在 MA20 下方，属企稳/反弹初期）"
    pat_html = "<br>".join(f"· {p}：{PAT_MEAN.get(p,'')}" for p in k.get("pats", [])) or "无程序化命中（需看图确认 狮子张口/挖坑埋牛/回眸一笑/鱼跃龙门/岛形反转）"
    nh = k.get("near_high", 99)
    if a and a.get("checked"):
        def _why(key):
            lst = a.get(key) or a.get("hits") or []
            return "；".join(lst[:1])
        t3 = ("Wind 公告核查：近窗有回购/增持/中标/合同/重组类利好披露（%s），注意利好兑现/出尽风险 → 需谨慎" % _why("hits_good")
              if a.get("good_news") else "Wind 公告核查（近窗）：无重大利好密集披露 → 未触发")
        t5 = ("⚠️ Wind 公告核查命中：近窗有减持/权益变动披露（%s），触发九不买 #5 → 回避" % _why("hits_reduction")) if a.get("reduction") else \
             "Wind 公告核查（近窗）：无减持/权益变动披露 → 未触发"
        if a.get("penalty"):
            base6 = "⚠️ Wind 公告核查命中：近窗有监管问询/处罚披露（%s），触发 #6 基本面问题 → 回避" % _why("hits_penalty")
        elif a.get("earnings_warn"):
            base6 = "⚠️ 近窗业绩预减/预亏披露（%s），触发 #6 → 需回避" % _why("hits_earn")
        else:
            base6 = (f"⚠️ {c['name']} 属 ST/风险警示股，触发 #6 → 回避" if is_st(c)
                     else f"PE(TTM) {c['pe']:.2f}，非负、非 ST；Wind 核查无违规/预减 → 未触发")
    else:
        t3 = "👁 需核查公告/新闻（运行「公告核查」步骤可由 Wind 客观化），无可见证据"
        t5 = "👁 需查减持公告（运行「公告核查」步骤可由 Wind 客观化），本环境无可达源"
        base6 = (f"⚠️ {c['name']} 属 ST/风险警示股，触发 #6 → 回避" if is_st(c)
                 else f"PE(TTM) {c['pe']:.2f}，非负、非 ST → 未触发")
    nine = [
        ("下跌趋势不买", f"价 {k['close']} > MA20 {k['ma20']}，不在长期均线下方 → 未触发"),
        ("高位放量滞涨不买", ("处 20 日新高突破位，价随量升、非滞涨 → 未触发，但追高需等回踩" if nh < 1 else "处反弹/上行段，非三浪末端诱多 → 未触发")),
        ("利好兑现不买", t3),
        ("短期暴涨不买", ("处 20 日新高突破位，非连续涨停/一字板 → 未触发，但追高需等回踩" if nh < 1 else "近20日距高点尚远（非连续涨停）→ 未触发")),
        ("大股东减持不买", t5),
        ("基本面问题不买", base6),
        ("跌破平台支撑不买", "价在 MA 上方运行，未破位 → 未触发（深跌反弹股需确认不再创新低）"),
        ("技术走坏不买", f"均线非空头排列；量比 {c['vr']:.2f} ≤10 → 未触发"),
        ("换手异常不买", f"换手 {c['to']:.2f}% 在 5~10%；量比≤10 → 未触发"),
    ]
    buypt = ("距 20 日高仅 %.1f%%，处于突破位——按层8须等 14:30 后回踩均线不破再入场，忌追高" % nh) if nh < 1 else ("距 20 日高 %.1f%%，仍有空间；按层8等回踩均线（MA5≈%.2f）低吸" % (nh, k["ma5"]))
    if isd and isd.get("covered"):
        ar = isd["above_ratio"] * 100
        ex = isd["excess"]
        snap = ("（盘中快照截至%s，未收盘）" % isd["last_time"]) if isd.get("partial") else ""
        strength_txt = ("分时强度：<b>%s</b>（均价线上方占比 %.0f%%、跑赢大盘 %+.1f%%%s）" % (isd["verdict"], ar, ex, snap))
    else:
        strength_txt = "分时强度 👁（点「实时重新筛查」由东财自取）"
    concl = ('趋势最强（干净多头排列）' if k.get('multi') else '价格站上均线、反弹初期')
    if nh < 1: concl += '；创新高突破，动能强但需回踩确认'
    else: concl += '；未达前高，安全边际较好'
    if c['pe'] and c['pe'] < 20: concl += '；估值偏低（PE<20）'
    else: concl += '；估值中性'
    v, vnote = verdict(c, a and {norm_key(c['code']): a} or None)
    _trig = []
    if is_st(c): _trig.append("ST风险警示#6")
    if a and a.get("checked"):
        if a.get("reduction"): _trig.append("减持#5")
        if a.get("penalty"): _trig.append("违规/监管#6")
        if a.get("earnings_warn"): _trig.append("业绩预减#6")
    if c.get("pe") is not None and c["pe"] < 0: _trig.append("亏损#6")
    if c.get("pe") is not None and c["pe"] > 200: _trig.append("估值偏高")
    if v == "不买":
        concl_suffix = f"。量化九不买<b>未通过</b>（{'、'.join(_trig)}）→ 回避。"
    elif v == "观察":
        concl_suffix = f"。量化九不买需谨慎（{'、'.join(_trig)}）。"
    else:
        concl_suffix = "。量化九不买全过。"
    ts = (k['close'] > k['ma5'] and k['close'] > k['ma10'])
    vh = k['vratio'] >= 0.8
    io = bool(k.get('multi')) or bool(k.get('pats'))
    tg = k['near_high'] > 5
    sell_items = [
        ("趋势强劲", "命中（价在 MA5/MA10 上方）" if ts else "偏弱（价未稳站短均线）"),
        ("热点题材", "👁 需人工结合当日板块/政策判定"),
        ("指标向好", ("命中（多头排列/底部形态）" if io else "一般（无明确共振）")),
        ("量能健康", ("命中（量价配合）" if vh else "偏弱（缩量，需观察）")),
        ("逻辑未变", "👁 取决于你的买入初衷，无法从量价判定"),
        ("未达目标", (f"命中（距前高尚有 {k['near_high']:.1f}% 空间）" if tg else "已近前高，须先设止盈目标")),
    ]
    obj_hit = sum([ts, vh, io, tg])
    hold = ("持有信号较强，可继续持有，严格按下方离场信号风控" if obj_hit >= 3 else
            "持有信号中等，可持有但收紧止损（如 MA5 下方）" if obj_hit == 2 else
            "持有信号偏弱，仅宜快进快出/小仓，破短均线即走")
    exit_sig = (f"⏹ <b>下车信号（离场条件）</b>：跌破 MA5({k['ma5']:.2f}) 或前低失效、"
                f"量价背离（价升量缩）、逻辑破坏、或达预设止盈 —— 任一触发即离场，其余继续持有。")
    return {
        "code": c["code"], "name": c["name"], "c": c, "k": k, "v": v, "trigs": _trig,
        "nine": nine, "multi_txt": multi_txt, "pat_html": pat_html, "buypt": buypt,
        "strength_txt": strength_txt, "concl": concl, "concl_suffix": concl_suffix,
        "sell_items": sell_items, "obj_hit": obj_hit, "hold": hold, "exit_sig": exit_sig,
        "trade_plan": (dict(trade_plan(c, k), action="回避", ac="bad",
                           reason="九不买触发，纪律上不参与买卖，买卖信号仅供参考")
                       if v == "不买" else trade_plan(c, k)),
    }

def trade_plan(c, k):
    """仓位买卖纪律（用户定制）：
       - 下跌趋势 + 相对底部 + 主力吸筹 + 金叉 → 建仓1成
       - 趋势反转为上升（多头排列）→ 加2成
       - 高位 + 浮盈≥10% → 减1/3
       - 跌破5日线 → 清仓
       可自动判定：趋势方向/相对底部/金叉/跌破5日线/高位区；
       主力吸筹(需筹码分布 cyq)、浮盈≥10%(需持仓成本) 标👁人工。"""
    if not k:
        return {"available": False, "action": "观望", "ac": "", "reason": "无K线数据，无法研判"}
    close=k.get("close"); ma5=k.get("ma5"); ma10=k.get("ma10"); ma20=k.get("ma20")
    hh=k.get("hh"); ll=k.get("ll"); near_high=k.get("near_high"); chg20=k.get("chg20")
    multi=bool(k.get("multi"))
    if multi:
        trend_dir="上升"
    elif (ma5 is not None and ma10 is not None and ma5 < ma10) or (chg20 is not None and chg20 < 0):
        trend_dir="下跌"
    else:
        trend_dir="震荡"
    pos=None
    if None not in (close, hh, ll) and hh > ll:
        pos=(close-ll)/(hh-ll)
    rel_bottom = (pos is not None and pos < 0.35)
    gold_cross = (None not in (ma5, ma10, close) and ma5 > ma10 and close >= ma5)
    break_ma5 = (None not in (close, ma5) and close < ma5)
    high_zone = (near_high is not None and near_high < 6)
    sigs=[
        ("下跌趋势", trend_dir=="下跌", f"MA5({ma5})<MA10({ma10}) 且未多头" if (ma5 and ma10) else "—"),
        ("相对底部", rel_bottom, f"处近期区间下35%内（位置≈{pos*100:.0f}%）" if pos is not None else "—"),
        ("主力吸筹", None, "👁 需筹码分布(cyq)数据人工确认"),
        ("金叉", gold_cross, "MA5>MA10 且价≥MA5"),
        ("趋势反转上升", multi, "均线多头排列(MA5>MA10>MA20,价>MA5)"),
        ("高位浮盈≥10%", None, "👁 需持仓成本，人工确认浮盈≥10%"),
        ("跌破五日线", break_ma5, "收盘价<MA5"),
    ]
    if break_ma5:
        action="清仓"; ac="bad"; reason=f"价格 {close} 已跌破5日线(MA5={ma5:.2f})，触发清仓纪律。"
    elif high_zone:
        action="减仓 (减1/3)"; ac="warn"; reason=f"处高位区（距20日高仅 {near_high:.1f}%），若持仓浮盈≥10%即减1/3仓（浮盈项👁需人工确认）。"
    elif multi:
        action="加仓 (加2成)"; ac="ok"; reason="趋势反转为上升（多头排列），若已建底仓则加2成；未见顶部/破位信号。"
    elif trend_dir=="下跌" and rel_bottom and gold_cross:
        action="建仓 (买入1成)"; ac="ok"; reason="下跌末端·相对底部 + 金叉，符合建仓条件（主力吸筹👁需同步确认），先建1成试错。"
    else:
        action="观望"; ac=""; reason="当前未触发明确买卖信号，按纪律观望，等趋势/信号确认后再动。"
    return {
        "available": True, "trend_dir": trend_dir,
        "pos": (round(pos,2) if pos is not None else None),
        "rel_bottom": rel_bottom, "gold_cross": gold_cross, "break_ma5": break_ma5,
        "high_zone": high_zone, "multi": multi, "sigs": sigs,
        "action": action, "ac": ac, "reason": reason,
    }

# ---------------- 东财分时自取（内嵌，无需 Agent / Wind） ----------------
EM_TREND_URL = ("https://push2delay.eastmoney.com/api/qt/stock/trends2/get"
                "?secid={secid}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13"
                "&fields2=f51,f52,f53,f54,f55,f56,f57,f58&iscr=0&ndays=1")

def _em_fetch(secid, retries=4):
    """拉一只标的的当日分钟序列（push2delay）。返回 trends 列表或 None。"""
    ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    url = EM_TREND_URL.format(secid=secid)
    last_err = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0", "Referer": "https://quote.eastmoney.com/"})
            raw = urllib.request.urlopen(req, timeout=20, context=ctx).read().decode("utf-8", "ignore")
            d = json.loads(raw).get("data") or {}
            tr = d.get("trends") or []
            if tr:
                return tr
            last_err = "empty"
        except Exception as e:
            last_err = e
        time.sleep(0.4 * (i + 1))
    if last_err not in (None, "empty"):
        print(f"  [EM] {secid} 拉取失败: {last_err}")
    return None

def _build_columns():
    return [{"name": "TIME"}, {"name": "MATCH"}, {"name": "OPEN"},
            {"name": "HIGH"}, {"name": "LOW"}, {"name": "TURNOVER"}, {"name": "VOLUME"}]

def _rows_from_trends(tr):
    """trends: 'YYYY-MM-DD HH:MM,open,close,high,low,vol(手),amount(元),avg'。
    重组为 Wind 兼容 data（TURNOVER=额元, VOLUME=量股=手×100）。"""
    rows = []
    for line in tr:
        f = line.split(",")
        if len(f) < 8:
            continue
        t, o, cl, h, lo, v, amt = f[0], f[1], f[2], f[3], f[4], f[5], f[6]
        try:
            rows.append([t, float(cl), float(o), float(h), float(lo),
                         float(amt), float(v) * 100.0])
        except ValueError:
            continue
    return rows

def fetch_intraday_em(cwd, delay=0.35):
    """读 candidates.json，对全部候选 + 沪深300 基准用东财 push2delay 自取分时，
    写出 intraday_raw.json（与 Wind 版结构兼容），返回覆盖只数（失败返回 -1 表示无候选）。"""
    cands = load_json_in(cwd, "candidates.json", [])
    if not cands:
        return -1
    # 数据基准日（用于 raw.date 标注，merge 不强制匹配）
    meta = load_json_in(cwd, "screen_meta.json", {}) or {}
    date = meta.get("data_date", datetime.date.today().strftime("%Y-%m-%d"))

    stocks = {}
    for c in cands:
        secid = to_secid(c["code"])
        tr = _em_fetch(secid)
        if not tr:
            continue
        rows = _rows_from_trends(tr)
        if not rows:
            continue
        stocks[c["code"]] = {
            "name": c.get("name", ""), "windcode": to_wind(c["code"]),
            "data": {"columns": _build_columns(), "rows": rows},
        }
        time.sleep(delay)
    # 基准：沪深300
    bench = None
    btr = _em_fetch("1.000300")
    if btr:
        brows = _rows_from_trends(btr)
        if brows:
            bench = {"windcode": "000300.SH", "data": {"columns": _build_columns(), "rows": brows}}

    raw = {"date": date, "benchmark": bench, "stocks": stocks}
    with open(os.path.join(cwd, "intraday_raw.json"), "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)
    print(f"  [EM] 分时自取完成：{len(stocks)}/{len(cands)} 只候选覆盖（含基准={'有' if bench else '无'}）")
    return len(stocks)

def load_json_in(cwd, name, default=None):
    p = os.path.join(cwd, name)
    if not os.path.exists(p):
        return default
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

# ---------------- HTTP ----------------
class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/run"):
            self._run()
        elif self.path.startswith("/api/data"):
            try:
                self._send(200, compute_payload("data"))
            except Exception as e:
                self._send(500, {"error": str(e)})
        elif self.path in ("/", "/index.html"):
            self._serve_html()
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path.startswith("/api/run"):
            self._run()
        else:
            self._send(404, {"error": "not found"})

    def _serve_html(self):
        p = os.path.join(CWD, "workbench_realtime.html")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                self._send(200, f.read(), "text/html; charset=utf-8")
        else:
            self._send(404, "workbench_realtime.html not found")

    def _run(self):
        # 实时重跑：东财初筛 + 新浪K线 + 东财分时自取（公告核查仍由 Agent/Wind 另跑）
        log = []
        try:
            # 1) select_stocks
            r1 = subprocess.run([VENV_PY, os.path.join(SKILL, "select_stocks.py")],
                                cwd=CWD, capture_output=True, text=True, timeout=180)
            log.append(r1.stdout.strip().splitlines()[-3:] if r1.stdout else [])
            if r1.returncode != 0:
                log.append("select_stocks stderr: " + r1.stderr[:500])
            # 2) kline_history --top 40 --json
            r2 = subprocess.run([VENV_PY, os.path.join(SKILL, "kline_history.py"),
                                 "--top", "40", "--json"],
                                cwd=CWD, capture_output=True, text=True, timeout=300)
            log.append(r2.stdout.strip().splitlines()[-3:] if r2.stdout else [])
            if r2.returncode != 0:
                log.append("kline_history stderr: " + r2.stderr[:500])
            # 3) 东财分时自取（无需 Agent/Wind）
            try:
                n = fetch_intraday_em(CWD)
                if n and n > 0:
                    r3 = subprocess.run([VENV_PY, os.path.join(SKILL, "intraday_strength_wind.py"), "--merge"],
                                        cwd=CWD, capture_output=True, text=True, timeout=120)
                    log.append(r3.stdout.strip().splitlines()[-3:] if r3.stdout else [])
                    if r3.returncode != 0:
                        log.append("intraday merge stderr: " + r3.stderr[:300])
                else:
                    log.append("东财分时自取：无候选或拉取失败，跳过（分时强度回落 👁）")
            except Exception as e:
                log.append("东财分时自取异常: " + str(e)[:300])
            payload = compute_payload("live")
            payload["run_log"] = [item for sub in log for item in (sub if isinstance(sub, list) else [sub])]
            self._send(200, payload)
        except subprocess.TimeoutExpired as e:
            self._send(504, {"error": "实时重跑超时", "detail": str(e)})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def log_message(self, *a):
        pass  # 静默

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"选股工作台实时服务已启动: http://127.0.0.1:{port}/")
    print(f"  工作目录: {CWD}")
    print(f"  按 Ctrl+C 停止")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()

if __name__ == "__main__":
    main()
