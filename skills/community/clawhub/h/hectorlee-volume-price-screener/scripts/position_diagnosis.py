#!/usr/bin/env python3
"""
持仓诊断模块
============
对持仓中的每只股票进行量价形态识别、评分和风险评估，
输出格式化的诊断表格和建议。

用法:
    python position_diagnosis.py positions.json
    python position_diagnosis.py positions.json --detail
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pattern_detect import detect_from_klines, PatternResult, Bar
from scoring import score_pattern
from data_provider import get_kline, get_realtime_quote
from risk_filter import comprehensive_filter, is_st_name
from colors import RED, GREEN, YELLOW, CYAN, BOLD, RESET, GRAY

KLINE_COUNT = 90


# ============================================================
# 持仓加载
# ============================================================

def load_positions(filepath: str) -> list:
    """加载持仓 JSON 文件"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"{RED}错误: 持仓文件必须是 JSON 数组格式{RESET}")
            sys.exit(1)
        for i, pos in enumerate(data):
            if not isinstance(pos, dict):
                print(f"{RED}错误: 第 {i+1} 条记录格式无效{RESET}")
                sys.exit(1)
            for field in ("code", "name", "cost", "shares"):
                if field not in pos:
                    print(f"{RED}错误: 第 {i+1} 条记录缺少字段 '{field}'{RESET}")
                    sys.exit(1)
        return data
    except FileNotFoundError:
        print(f"{RED}错误: 文件不存在 '{filepath}'{RESET}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{RED}错误: JSON 解析失败 - {e}{RESET}")
        sys.exit(1)


# ============================================================
# 单股诊断
# ============================================================

def diagnose_position(pos: dict, detail: bool = False) -> dict:
    """对单只持仓进行诊断

    返回:
        {
            "code": str,
            "name": str,
            "cost": float,
            "shares": int,
            "latest_price": float or None,
            "pnl_pct": float or None,
            "pattern": str,
            "pattern_variant": str,
            "score": float or None,
            "score_level": str,
            "recommendation": str,
            "risk": str,
            "error": str or None,
            "detail": dict or None,  # --detail 时附加
        }
    """
    code = pos["code"]
    name = pos["name"]
    cost = float(pos["cost"])
    shares = int(pos["shares"])

    result = {
        "code": code,
        "name": name,
        "cost": cost,
        "shares": shares,
        "latest_price": None,
        "pnl_pct": None,
        "pattern": "-",
        "pattern_variant": "",
        "score": None,
        "score_level": "",
        "recommendation": "",
        "risk": "",
        "error": None,
        "detail": None,
    }

    # ---- 1. 获取K线 ----
    klines = get_kline(code, KLINE_COUNT)
    if klines is None or len(klines) == 0:
        result["error"] = "K线获取失败"
        return result

    # 最新价格（K线最后一日收盘价）
    latest = klines[-1]["close"]
    result["latest_price"] = latest

    # ---- 2. 计算盈亏 ----
    if cost > 0:
        result["pnl_pct"] = round((latest - cost) / cost * 100.0, 2)

    # ---- 3. 名称级风险检查（无需形态结果） ----
    if is_st_name(name):
        result["risk"] = "ST/*ST"

    # ---- 4. 量价形态检测 ----
    pattern = detect_from_klines(klines, code=code)
    divergence_warning = False
    detail_data = None

    if pattern is not None:
        result["pattern"] = f"{pattern.pattern_variant}-{pattern.pattern_label}"
        result["pattern_variant"] = pattern.pattern_variant
        divergence_warning = pattern.divergence_warning

        # ---- 5. 形态评分 ----
        score = score_pattern(pattern)
        result["score"] = score.total
        result["score_level"] = score.level

        # K线级风险过滤
        bars = [
            Bar(date=k["date"], open=k["open"], high=k["high"],
                low=k["low"], close=k["close"], volume=k["volume"])
            for k in klines
        ]
        excluded, reason, skipped = comprehensive_filter(
            code, name, bars, pattern.anchor_idx,
            anchor_turnover=None, quote=None, params=None,
            min_days=60, min_turnover=3.0
        )
        if excluded:
            result["risk"] = reason
        elif skipped:
            result["risk"] = "换手率数据缺失"

        # --detail 详情
        if detail:
            detail_data = {
                "anchor_date": pattern.anchor_date,
                "surge_pct": round(pattern.surge_pct, 2),
                "volume_ratio": round(pattern.volume_ratio, 2),
                "shrink_days": pattern.shrink_days,
                "shrink_depth": round(pattern.shrink_depth, 2),
                "amplitude": round(pattern.amplitude, 2),
                "divergence_warning": divergence_warning,
                "breakout_60d": pattern.breakout_60d,
                "ma_support": pattern.ma_support,
                "vol_ma_bull": pattern.vol_ma_bull,
                "score_breakdown": score.details if score else None,
            }
    else:
        result["pattern"] = "未识别"
        # 无形态时，用 bars 做基础 K 线级风险检查（仅次新股检测）
        bars = [
            Bar(date=k["date"], open=k["open"], high=k["high"],
                low=k["low"], close=k["close"], volume=k["volume"])
            for k in klines
        ]
        from risk_filter import check_new_stock
        excluded, reason = check_new_stock(bars, min_days=60, code=code)
        if excluded:
            result["risk"] = reason

    result["detail"] = detail_data

    # ---- 6. 建议判定 ----
    pnl = result["pnl_pct"]
    if divergence_warning and pnl is not None and pnl < -10.0:
        result["recommendation"] = "卖出"
    elif divergence_warning or (pnl is not None and pnl < -5.0):
        result["recommendation"] = "减仓"
    else:
        result["recommendation"] = "持有"

    return result


# ============================================================
# 表格输出
# ============================================================

def format_table(results: list, detail: bool = False):
    """格式化彩色输出诊断表格"""
    if not results:
        print(f"{GRAY}无持仓数据{RESET}")
        return

    # 表头
    header = f"{'代码':<8} {'名称':<10} {'成本':>8} {'现价':>8} {'盈亏%':>8} {'形态':<14} {'评分':>6} {'建议':<6} {'风险'}"
    sep = "-" * len(header.replace(RED, "").replace(GREEN, "").replace(YELLOW, "").replace(CYAN, "").replace(BOLD, "").replace(RESET, "").replace(GRAY, ""))

    print()
    print(f"{BOLD}{header}{RESET}")
    print(f"{GRAY}{'-' * 90}{RESET}")

    for r in results:
        code = r["code"]
        name = r["name"]
        cost = r["cost"]
        shares = r["shares"]

        # 现价
        if r["latest_price"] is not None:
            price_str = f"{r['latest_price']:.2f}"
        else:
            price_str = "-"

        # 盈亏
        pnl = r["pnl_pct"]
        if pnl is not None:
            if pnl >= 0:
                pnl_str = f"{GREEN}+{pnl:.2f}%{RESET}"
            else:
                pnl_str = f"{RED}{pnl:.2f}%{RESET}"
        else:
            pnl_str = f"{GRAY}-{RESET}"

        # 形态
        pattern = r["pattern"]
        variant = r["pattern_variant"]
        if variant == "D":
            pattern_str = f"{CYAN}{pattern}{RESET}"
        elif variant in ("C", "B", "A", "R"):
            pattern_str = pattern
        else:
            pattern_str = f"{GRAY}{pattern}{RESET}"

        # 评分
        score = r["score"]
        if score is not None:
            if score >= 80:
                score_str = f"{RED}{score:.1f}{RESET}"
            elif score >= 60:
                score_str = f"{YELLOW}{score:.1f}{RESET}"
            else:
                score_str = f"{GRAY}{score:.1f}{RESET}"
        else:
            score_str = f"{GRAY}-{RESET}"

        # 建议
        rec = r["recommendation"]
        if rec == "卖出":
            rec_str = f"{RED}{BOLD}{rec}{RESET}"
        elif rec == "减仓":
            rec_str = f"{YELLOW}{BOLD}{rec}{RESET}"
        else:
            rec_str = f"{GREEN}{rec}{RESET}"

        # 风险
        risk = r["risk"] if r["risk"] else "-"
        if risk and risk != "-":
            risk_str = f"{RED}{risk}{RESET}"
        else:
            risk_str = f"{GRAY}-{RESET}"

        # 错误
        error = r.get("error")
        if error:
            print(f"{GRAY}{code:<8} {name:<10} {cost:>8.2f} {'-':>8} {'-':>8} {'-':<14} {'-':>6} {'-':<6} {error}{RESET}")
            continue

        # 对齐处理（去除 ANSI 码后的列宽）
        print(f"{code:<8} {name:<10} {cost:>8.2f} {price_str:>8} {pnl_str:>8} {pattern_str:<14} {score_str:>6} {rec_str:<6} {risk_str}")

    print(f"{GRAY}{'-' * 90}{RESET}")

    # 汇总
    total_count = len(results)
    hold_count = sum(1 for r in results if r["recommendation"] == "持有")
    reduce_count = sum(1 for r in results if r["recommendation"] == "减仓")
    sell_count = sum(1 for r in results if r["recommendation"] == "卖出")
    error_count = sum(1 for r in results if r.get("error"))

    print()
    print(f"{BOLD}汇总:{RESET} 共 {total_count} 只 | "
          f"{GREEN}持有 {hold_count}{RESET} | "
          f"{YELLOW}减仓 {reduce_count}{RESET} | "
          f"{RED}卖出 {sell_count}{RESET}", end="")
    if error_count > 0:
        print(f" | {GRAY}数据异常 {error_count}{RESET}")
    else:
        print()

    # --detail 展开详情
    if detail:
        print()
        print(f"{BOLD}{'=' * 90}{RESET}")
        print(f"{BOLD}详细诊断{RESET}")
        print(f"{BOLD}{'=' * 90}{RESET}")

        for r in results:
            if r.get("error"):
                continue

            print()
            print(f"{BOLD}{r['code']} {r['name']}{RESET}")
            print(f"  成本: {r['cost']:.2f}  现价: {r.get('latest_price', '-')}  "
                  f"盈亏: {r.get('pnl_pct', '-')}%  建议: {r['recommendation']}")

            d = r.get("detail")
            if d is None:
                print(f"  {GRAY}形态未识别，无详细数据{RESET}")
                continue

            print(f"  放量日: {d.get('anchor_date', '-')}  "
                  f"涨幅: {d.get('surge_pct', '-')}%  "
                  f"量比: {d.get('volume_ratio', '-')}")
            print(f"  缩量天数: {d.get('shrink_days', '-')}  "
                  f"缩量深度: {d.get('shrink_depth', '-')}  "
                  f"振幅: {d.get('amplitude', '-')}%")
            print(f"  60日新高: {'是' if d.get('breakout_60d') else '否'}  "
                  f"均线支撑: {'是' if d.get('ma_support') else '否'}  "
                  f"量能多头: {'是' if d.get('vol_ma_bull') else '否'}")
            if d.get("divergence_warning"):
                print(f"  {RED}背离预警: 横盘期放量滞涨（出货嫌疑）{RESET}")

            sb = d.get("score_breakdown")
            if sb:
                print(f"  评分明细: 放量{sb.get('vol_multi', '-')} + "
                      f"缩量{sb.get('shrink_days_score', '-')} + "
                      f"变体{'-'} + "
                      f"趋势{'-'} + "
                      f"加分{'-'} = {r.get('score', '-')} ({r.get('score_level', '-')})")


# ============================================================
# 主入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(f"用法: python {os.path.basename(__file__)} <positions.json> [--detail]")
        print()
        print("  持仓 JSON 格式:")
        print('  [')
        print('    {"code": "600406", "name": "国电南瑞", "cost": 24.50, "shares": 1000},')
        print('    {"code": "000001", "name": "平安银行", "cost": 10.20, "shares": 500}')
        print('  ]')
        sys.exit(1)

    filepath = sys.argv[1]
    detail = "--detail" in sys.argv

    # 加载持仓
    positions = load_positions(filepath)
    if not positions:
        print(f"{YELLOW}持仓列表为空{RESET}")
        return

    print(f"{BOLD}持仓诊断 V3.0{ RESET}")
    print(f"{GRAY}文件: {filepath} | 持仓数: {len(positions)}{RESET}")

    # 逐只诊断
    results = []
    for i, pos in enumerate(positions):
        code = pos.get("code", "")
        name = pos.get("name", "")
        print(f"\r{GRAY}正在诊断: {code} {name} ({i+1}/{len(positions)}){RESET}", end="", flush=True)
        result = diagnose_position(pos, detail=detail)
        results.append(result)

    print(f"\r{GRAY}{' ' * 60}{RESET}", end="\r")  # 清除进度行

    # 输出表格
    format_table(results, detail=detail)


if __name__ == "__main__":
    main()
