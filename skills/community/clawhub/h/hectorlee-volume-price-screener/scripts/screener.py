#!/usr/bin/env python3
"""
纯量价选股 - 主入口
====================
识别「放量拉升 → 缩量调整 → 横盘整理」形态（纯量价，无基本面）。

用法:
  python screener.py --all --top 20            # 全市场扫描，输出Top20
  python screener.py 000001 600519             # 指定股票诊断
  python screener.py --all --top 20 --detail   # ��评分明细
  python screener.py --search 茅台             # 搜索后诊断
  python screener.py --params '{"window":20}'  # 覆盖参数

输出颜色: 涨=红, 跌=绿（A股惯例）; 不命中/剔除用灰色标注原因。
"""

import argparse
import json
import os
import sys
import time
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pattern_detect import detect_pattern, detect_from_klines, detect_reversal, PatternResult, DEFAULT_PARAMS, Bar
from scoring import score_pattern, ScoreResult
from risk_filter import comprehensive_filter
from data_provider import get_all_stocks, fetch_klines_batch, fetch_quotes_batch, search_stock, get_kline
from adaptive import market_volatility, adaptive_params, describe

# 终端颜色（macOS/Linux 支持）
from colors import RED, GREEN, YELLOW, CYAN, GRAY, BOLD, RESET, MAGENTA


def color_pct(pct: float) -> str:
    if pct > 0:
        return f"{RED}+{pct:.2f}%{RESET}"
    if pct < 0:
        return f"{GREEN}{pct:.2f}%{RESET}"
    return f"{pct:.2f}%"


def print_header(params: dict = None):
    p = params or DEFAULT_PARAMS
    print(f"\n{BOLD}═══ 纯量价形态选股 V3.7（放量→缩量→6变体+多因子+多周期+行业共振）═══{RESET}")
    print(f"{GRAY}窗口: {p['window']}日 | 6变体(D/E/C/B/A/R) | 振幅≤{p['amp_max']}%{GRAY}(趋势斜率陡峭时自适应放宽至15%){RESET}")
    print(f"{GRAY}主板3-5%分档 | 创业6%+2.0 | 科创4%+2.0 | 北交5%+3.0 | 曝光度:近50日上榜次数{RESET}\n")


def variant_color(label: str) -> str:
    """变体标签颜色"""
    color_map = {
        "突破延续": f"{RED}{BOLD}突破延续{RESET}",
        "蓄力突破": f"{MAGENTA}{BOLD}蓄力突破{RESET}",
        "回踩确认": f"{GREEN}{BOLD}回踩确认{RESET}",
        "高位平台": f"{YELLOW}{BOLD}高位平台{RESET}",
        "标准横盘": f"{CYAN}标准横盘{RESET}",
        "底部反转": f"{RED}{BOLD}底部反转{RESET}",
    }
    return color_map.get(label, f"{GRAY}{label}{RESET}")


def level_color(level: str) -> str:
    if level == "强势形态":
        return f"{RED}{BOLD}{level}{RESET}"
    if level == "标准形态":
        return f"{YELLOW}{level}{RESET}"
    return f"{GRAY}{level}{RESET}"


def analyze_one(code: str, name: str, klines: List[dict], quote: Optional[dict],
                params: dict, detail: bool = False, ml_model: Optional[dict] = None) -> Optional[dict]:
    """分析单只股票，返回结构化结果或 None（不命中/剔除）"""
    # 形态识别（dict格式K线 → Bar 列表）
    result = detect_from_klines(klines, code=code, params=params)
    # V3.1: 标准形态未命中时，尝试底部反转
    is_reversal = False
    if result is None:
        bars_raw = [Bar(date=k["date"], open=float(k["open"]), high=float(k["high"]),
                        low=float(k["low"]), close=float(k["close"]), volume=float(k["volume"]))
                    for k in klines]
        result = detect_reversal(bars_raw, code=code, params=params)
        is_reversal = result is not None
    if result is None:
        return None
    # 风险过滤（用与形态识别一致的 Bar 列表）
    bars = [Bar(date=k["date"], open=float(k["open"]), high=float(k["high"]),
                low=float(k["low"]), close=float(k["close"]), volume=float(k["volume"]))
            for k in klines]
    # 换手率过滤：仅当放量日就是最新交易日时，实时换手率才有效；否则视为数据缺失（跳过）
    anchor_turnover = None
    if quote and klines and result.anchor_date == klines[-1]["date"]:
        anchor_turnover = quote.get("turnover")
    excluded, reason, skipped = comprehensive_filter(
        code, name, bars, result.anchor_idx,
        anchor_turnover=anchor_turnover, quote=quote, params=params)
    if excluded:
        return {"excluded": True, "reason": reason, "name": name, "code": code}

    # 评分
    score = score_pattern(result, params)

    # ML 概率（可选）
    prob = None
    if ml_model is not None:
        try:
            from ml_model import predict, extract_feature_vector
            sample = {
                "surge_pct": result.surge_pct, "volume_ratio": result.volume_ratio,
                "shrink_days": result.shrink_days, "shrink_depth": result.shrink_depth,
                "amplitude": result.amplitude, "range_position": result.range_position,
                "pullback_ratio": result.pullback_ratio, "low_point_rise": result.low_point_rise,
                "breakout_60d": result.breakout_60d, "ma_support": result.ma_support,
                "vol_ma_bull": result.vol_ma_bull, "conc_rise_3d": result.conc_rise_3d,
                "conc_fall_3d": result.conc_fall_3d, "score": score.total,
            }
            model = ml_model.get("model")
            prob = float(model.predict_proba([extract_feature_vector(sample)])[0][1])
        except Exception:
            prob = None

    return {
        "excluded": False,
        "code": code, "name": name,
        "result": result, "score": score,
        "quote": quote, "skipped": skipped,
        "prob": prob,
    }


def print_result(entry: dict, detail: bool = False):
    """打印单只股票结果"""
    if entry.get("excluded"):
        print(f"  {GRAY}✗ {entry['code']} {entry['name']} — {entry['reason']}{RESET}")
        return

    r: PatternResult = entry["result"]
    s: ScoreResult = entry["score"]
    q = entry.get("quote") or {}
    price = q.get("price", 0)
    pct = q.get("change_pct", 0)
    anchor_vol_ratio = r.volume_ratio

    line = (f"  {CYAN}{entry['code']}{RESET} {entry['name']:<8s} "
            f"{BOLD}{price:.2f}{RESET} {color_pct(pct):<10s} "
            f"{variant_color(r.pattern_label):<16s} "
            f"{BOLD}{s.total:.1f}{RESET}分  "
            f"{GRAY}放量日{r.anchor_date} 量比{anchor_vol_ratio:.1f} "
            f"缩量{r.shrink_days}日 振幅{r.amplitude:.1f}%{RESET}")
    if entry.get("sector_bonus"):
        line += f"  {YELLOW}[{entry.get('sector_name','板块')}共振+{entry['sector_bonus']:.0f}]{RESET}"
    rc = s.details.get("recurrence_count", 0)
    if rc > 0:
        line += f"  {MAGENTA}[近50日上榜{rc}次]{RESET}"
    if entry.get("prob") is not None:
        p = entry["prob"]
        p_color = RED if p >= 0.6 else (YELLOW if p >= 0.5 else GRAY)
        line += f"  {p_color}ML上涨概率{p*100:.0f}%{RESET}"
    print(line)

    if r.divergence_warning:
        penalty = s.details.get('divergence_penalty', -10)
        print(f"    {YELLOW}⚠ 背离预警：横盘期出现放量滞涨（出货嫌疑） {penalty:.0f}分{RESET}")

    if detail:
        d = s.details
        variant = d.get("variant", "A")
        print(f"    {GRAY}├ 放量质量{s.vol_score:.1f}/30"
              f"（倍数{d['vol_multi_tag']}·{d['vol_multi']:.0f} + 拉升{d['surge_score']:.0f} + 新高{d['breakout_60d_score']:.0f}）")
        print(f"    ├ 缩量质量{s.shrink_score:.1f}/20"
              f"（深度{d.get('shrink_depth_tag','?')}·{d.get('shrink_depth',0)*100:.0f}% + 天数{d.get('shrink_days_score',0):.0f}）")

        # 变体相关明细
        if r.is_reversal:
            print(f"    ├ 反转质量{s.variant_score:.1f}/25"
                  f"（跌幅{d.get('reversal_decline',0):.1f}%·{d.get('decline_score',0):.0f}"
                  f" + 地量{d.get('reversal_volume_dry',0)*100:.0f}%·{d.get('dry_score',0):.0f}）")
        elif variant == "D":
            print(f"    ├ 延续质量{s.variant_score:.1f}/25"
                  f"（涨幅{d.get('gain_score',0):.0f} + 阳线{d.get('bull_score',0):.0f}"
                  f" + 拒绝回调{d.get('breakdown_score',0):.0f}）")
        elif variant == "C":
            print(f"    ├ 回踩质量{s.variant_score:.1f}/25"
                  f"（精准度{d.get('precision_score',0):.0f} + 反弹{d.get('recovery_score',0):.0f}"
                  f" + 振幅{d.get('amplitude_score',0):.0f} + 低点抬高{'✓' if d.get('low_point_rise') else '✗'}）")
        elif variant == "B":
            print(f"    ├ 高位平台{s.variant_score:.1f}/25"
                  f"（振幅{d.get('amplitude_score',0):.0f} + 高位占比{d.get('platform_score',0):.0f}"
                  f" + 距离{d.get('dist_score',0):.0f} + 低点抬高{'✓' if d.get('low_point_rise') else '✗'}）")
        else:
            print(f"    ├ 横盘质量{s.variant_score:.1f}/25"
                  f"（振幅{d.get('amplitude_score',0):.0f} + 位置{d.get('position','?')}·{d.get('position_score',0):.0f}"
                  f" + 回调{d.get('pullback_score',0):.0f} + 低点抬高{'✓' if d.get('low_point_rise') else '✗'}）")

        print(f"    ├ 趋势量能{s.trend_score:.1f}/15"
              f"（新高{'✓' if d['trend_breakout'] else '✗'} + 均线{'✓' if d['trend_ma_support'] else '✗'}"
              f" + 量能多头{'✓' if d['trend_vol_ma_bull'] else '✗'}）")
        print(f"    └ 加分信号{s.bonus_score:.1f}/15"
              f"（3日量价齐升{'✓' if d.get('conc_rise_3d') else '✗'} + 3日量缩价跌{'✓' if d.get('conc_fall_3d') else '✗'}"
              f" + 连阳蓄力{d.get('pre_surge_days',0)}日{'✓' if d.get('pre_surge_days',0)>=3 else '✗'}）{RESET}")
        # V3.5 多因子+多周期+曝光度
        mf = d.get('multi_factor_score', 0)
        wk = d.get('weekly_bonus', 0)
        wk_trend = d.get('weekly_trend', '')
        rc = d.get('recurrence_count', 0)
        rs = d.get('recurrence_score', 0)
        if mf > 0 or wk != 0 or rc > 0:
            parts = []
            if mf > 0:
                parts.append(f"多因子+{mf:.0f}(流动性{d.get('mkt_factor_score',0):.0f}+波动{d.get('vol_factor_score',0):.0f}+趋势{d.get('trend_factor_score',0):.0f})")
            if wk != 0:
                color = "\033[92m" if wk > 0 else "\033[91m"
                parts.append(f"周线{color}{wk:+.0f}{RESET}({wk_trend})")
            if rc > 0:
                parts.append(f"曝光度+{rs:.0f}分(近50日上榜{rc}次)")
            print(f"    {GRAY}└ V3.5: {' | '.join(parts)}{RESET}")
        if entry.get("skipped"):
            print(f"    {GRAY}注: 腾讯日K无历史换手率，换手率过滤已跳过{RESET}")


def run_scan(codes_names: List[tuple], params: dict, top: int = 20, detail: bool = False,
             exclude_bj: bool = True, market_state: str = "", ml_model: Optional[dict] = None,
             to_json: bool = False):
    """执行扫描：codes_names = [(code, name), ...]"""
    codes = [c for c, _ in codes_names]
    name_map = dict(codes_names)

    t0 = time.time()
    print(f"{GRAY}正在拉取 {len(codes)} 只股票K线...{RESET}")
    klines_map = fetch_klines_batch(codes, count=90, workers=8)
    quotes_map = fetch_quotes_batch(codes, workers=8)
    t1 = time.time()
    print(f"{GRAY}数据拉取完成（{t1-t0:.1f}s），开始形态识别...{RESET}")

    hits, excluded = [], []
    for code, kl in klines_map.items():
        name = name_map.get(code, "")
        q = quotes_map.get(code)
        # V3.7 修复：hithink 本地库列表不含 name，用腾讯行情补齐（ST 过滤依赖 name）
        if not name and q:
            name = q.get("name", "")
        if kl is None or len(kl) < 60:
            excluded.append((code, name, "数据获取失败/K线不足"))
            continue
        entry = analyze_one(code, name, kl, q, params, detail, ml_model=ml_model)
        if entry is None:
            continue
        if entry.get("excluded"):
            excluded.append((code, name, entry["reason"]))
        else:
            hits.append(entry)

    # 排序：分高在前，背离预警降级；有ML概率时概率优先
    # V3.5: 板块共振增强 — 基于行业关键词精确分类（替代代码段）
    INDUSTRY_KW = {
        "电力新能源": ["电","能源","风","光","伏","核","缆","器","网","新能","节能","电池","电热"],
        "科技电子": ["科技","电子","软件","信息","数字","智能","通信","讯","芯","半导","集成","数据"],
        "化工材料": ["化","材","玻","纤","塑","橡","胶","矿","钢","铝","钛","硅","新材","碳"],
        "医药医疗": ["药","医","生物","健康","寿","仙","康","口腔"],
        "机械制造": ["机械","重工","装备","精密","机床","模具","工程","制造","工"],
        "消费家居": ["食品","饮料","酒","家","居","纺","服","鞋","宠","生活","牙"],
        "交通物流": ["交通","物流","港","航空","铁路","高速","车","运","船"],
        "农牧": ["农","牧","种","渔","林","饲料","肥料"],
        "金融地产": ["银行","证券","保险","信托","地产","物业","金融"],
    }
    sector_hits: dict = {}
    for e in hits:
        name = e["name"]
        sect = "其他"
        for sname, kws in INDUSTRY_KW.items():
            if any(kw in name for kw in kws):
                sect = sname
                break
        sector_hits.setdefault(sect, []).append(e)
    for sector, entries in sector_hits.items():
        count = len(entries)
        if count >= 5:          bonus = 15.0  # 强共振
        elif count >= 3:        bonus = 10.0  # 标准共振
        elif count >= 2:        bonus = 5.0   # 弱共振
        else:                   continue
        for e in entries:
            e["score"].total = round(e["score"].total + bonus, 1)
            e["sector_bonus"] = bonus
            e["sector_name"] = sector
    
    if ml_model is not None:
        hits.sort(key=lambda e: (e.get("prob") or 0, e["score"].total,
                                 0 if not e["result"].divergence_warning else 1), reverse=True)
    else:
        hits.sort(key=lambda e: (e["score"].total, 0 if not e["result"].divergence_warning else 1), reverse=True)

    print_header(params)
    if market_state:
        print(f"{GRAY}市场状态: {market_state}（参数自适应已启用）{RESET}")
    if not hits:
        print(f"{GRAY}未命中形态股票。{RESET}")
    else:
        print(f"{BOLD}命中 {len(hits)} 只（显示 Top {min(top, len(hits))}）：{RESET}\n")
        for e in hits[:top]:
            print_result(e, detail)
        if len(hits) > top:
            print(f"\n{GRAY}... 共 {len(hits)} 只命中，仅显示前 {top} 只{RESET}")

    if excluded:
        print(f"\n{GRAY}剔除 {len(excluded)} 只：{RESET}")
        for code, name, reason in excluded[:10]:
            print(f"  {GRAY}✗ {code} {name} — {reason}{RESET}")
        if len(excluded) > 10:
            print(f"  {GRAY}... 等 {len(excluded)} 只{RESET}")

    # JSON 输出
    if to_json:
        json_out = {
            "hits": [{"code": e["code"], "name": e["name"], "variant": e["result"].pattern_variant,
                      "score": e["score"].total, "anchor_date": e["result"].anchor_date,
                      "divergence": e["result"].divergence_warning}
                     for e in hits],
            "total_hits": len(hits),
            "excluded_count": len(excluded),
        }
        print(f"\n--- JSON ---")
        print(json.dumps(json_out, ensure_ascii=False, indent=2))

    t2 = time.time()
    print(f"\n{GRAY}总耗时 {t2-t0:.1f}s{RESET}")


def main():
    ap = argparse.ArgumentParser(description="纯量价形态选股（放量拉升→缩量调整→横盘整理）")
    ap.add_argument("codes", nargs="*", help="股票代码/名称（最多50只）")
    ap.add_argument("--all", action="store_true", help="全市场扫描")
    ap.add_argument("--top", type=int, default=20, help="输出Top N（默认20）")
    ap.add_argument("--detail", action="store_true", help="显示评分明细")
    ap.add_argument("--search", help="搜索关键词后诊断")
    ap.add_argument("--include-bj", action="store_true", help="包含北交所")
    ap.add_argument("--params", help="覆盖参数 JSON，如 '{\"window\":30}'")
    ap.add_argument("--adaptive", action="store_true", help="启用市场波动率参数自适应")
    ap.add_argument("--model", help="ML概率模型路径(.pkl)，启用ML排序")
    ap.add_argument("--json", action="store_true", help="输出JSON格式")
    args = ap.parse_args()

    params = dict(DEFAULT_PARAMS)
    if args.params:
        try:
            params.update(json.loads(args.params))
        except json.JSONDecodeError:
            print(f"{YELLOW}参数解析失败，使用默认参数{RESET}")

    market_state = ""
    if args.adaptive:
        # 用沪深300 近20日平均振幅估计市场波动率
        idx_kl = get_kline("sh000300", 40)
        vol = market_volatility(idx_kl) if idx_kl else None
        params = adaptive_params(params, vol)
        market_state = describe(vol)

    # ML 模型加载
    ml_model = None
    if args.model:
        try:
            from ml_model import load_model
            ml_model = load_model(args.model)
            m = ml_model.get("metrics", {})
            print(f"{CYAN}ML模型已加载: {args.model}（{m.get('backend','?')} AUC={m.get('auc','?')}）{RESET}")
        except Exception as e:
            print(f"{YELLOW}ML模型加载失败（{e}），使用纯评分排序{RESET}")

    # 收集股票
    codes_names: List[tuple] = []
    if args.search:
        for s in search_stock(args.search)[:20]:
            codes_names.append((s["code"], s["name"]))
    elif args.all:
        stocks = get_all_stocks(include_bj=args.include_bj)
        codes_names = [(s["code"], s["name"]) for s in stocks]
    elif args.codes:
        for c in args.codes:
            if c.isdigit() and len(c) == 6:
                from data_provider import _normalize_code
                codes_names.append((_normalize_code(c), c))
            else:
                for s in search_stock(c)[:5]:
                    codes_names.append((s["code"], s["name"]))
    else:
        ap.print_help()
        sys.exit(1)

    if not codes_names:
        print(f"{YELLOW}未找到股票，请检查代码/名称{RESET}")
        sys.exit(1)

    if len(codes_names) > 6000:
        print(f"{YELLOW}股票池过大({len(codes_names)})，请使用 --all 或减少代码数量{RESET}")
        sys.exit(1)

    run_scan(codes_names, params, top=args.top, detail=args.detail,
             exclude_bj=not args.include_bj, market_state=market_state, ml_model=ml_model,
             to_json=args.json)


if __name__ == "__main__":
    main()
