#!/usr/bin/env python3
"""
动量持仓顾问 V1.0 — 主入口

用法:
  python advisor.py --portfolio              # 持仓批量诊断
  python advisor.py --portfolio --detail     # 带明细
  python advisor.py 300663 --cost 6.88       # 单股诊断
  python advisor.py 300663 600519 --detail   # 多股
  python advisor.py --search 科蓝 --cost 6.88
  python advisor.py --scan --top 20          # 全市场动量扫描
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Optional

# 添加 volume-price-screener 到 path 以复用 data_provider
_SCREENER_DIR = os.path.expanduser('~/.workbuddy/skills/volume-price-screener/scripts')
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() and '__file__' in locals() else os.path.dirname(os.path.abspath(sys.argv[0]))

# 确保当前目录优先级最高
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if os.path.exists(_SCREENER_DIR) and _SCREENER_DIR not in sys.path:
    sys.path.append(_SCREENER_DIR)

from momentum_detect import detect_all
from momentum_scoring import calculate_score, format_score_output, format_score_compact
from cross_ref import get_vp_result, compute_fusion_bonus, format_vp_summary
from risk_filter import run_risk_checks
from portfolio import get_positions, calc_pnl
from sector_resonance import detect_sector_resonance, format_resonance_report
from logic_overlay import load_fundamentals, load_events, format_overlay_summary

# V1.4.0: 全局加载逻辑覆盖层配置（启动时一次）
FUNDAMENTALS = load_fundamentals()
EVENTS = load_events()

# ─── 颜色支持 ───

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def _c(text, color):
    return f"{color}{text}{Color.RESET}"

# ─── 单股诊断 ───

def diagnose_single(code: str, cost: float = None, detail: bool = False, prev_decision: str = None):
    """对单只股票执行完整诊断"""
    try:
        from data_provider import get_kline, get_realtime_quote
    except ImportError:
        print("错误: 无法导入 data_provider，请确保 volume-price-screener 已安装")
        sys.exit(1)
    
    # 获取数据
    kline = get_kline(code, count=90)
    if not kline or len(kline) < 20:
        print(f"  {code}: K线数据不足")
        return None
    
    quote = get_realtime_quote(code)
    name = quote.get('name', code) if quote else code
    price = quote.get('price', 0) if quote else kline[-1]['close']
    turnover = quote.get('turnover', None) if quote else None
    
    # 风险检查
    risk = run_risk_checks(name, kline, turnover)
    
    # 形态检测
    detect_result = detect_all(kline, turnover, code=code)
    
    # === 量价收敛形态交叉引用 ===
    vp_result = get_vp_result(kline, code)
    
    # 先算基础动量分，获取初步决策
    base_score = calculate_score(kline, detect_result, cost=cost, latest_price=price, prev_decision=prev_decision)
    momentum_decision = base_score['decision']
    
    # 计算融合加成
    vp_bonus, vp_reason = compute_fusion_bonus(vp_result, momentum_decision)
    
    # 最终评分（含量价共振 + 加仓信号 + 成本因子 + 资金流向 + 决策滞回 + V1.4.0逻辑覆盖层）
    fund_cfg = FUNDAMENTALS.get(code)
    score_result = calculate_score(kline, detect_result, vp_bonus, vp_reason, vp_result, cost, price, prev_decision=prev_decision,
                                   code=code, fundamental=fund_cfg, events=EVENTS)
    
    # 交叉引用 volume-price-screener
    vp_summary = format_vp_summary(vp_result)
    
    if detail:
        output = format_score_output(score_result, detect_result, name, code, cost, price, kline)
        if vp_summary:
            output += f"\n{_c(vp_summary, Color.CYAN)}"
        if vp_result and vp_result.get('warning'):
            output += f"\n{_c('  *** ' + vp_result['warning'] + ' ***', Color.RED)}"
        print(output)
    else:
        line = format_score_compact(score_result, detect_result, name, code)
        if cost and price:
            pnl = calc_pnl(cost, price)
            line += f"  成本{cost:.2f} PnL{pnl:+.1f}%"
        # 量价收敛标记
        if vp_result:
            tier_mark = {'strong': '!', 'standard': '+', 'watch': '~'}
            mark = tier_mark.get(vp_result.get('tier', 'watch'), '~')
            line += f"  VP:{mark}{vp_result['variant']}/{vp_result['score']}"
        # 加仓信号
        buy = score_result.get('buy_advice')
        if buy:
            stars = '⭐' * score_result.get('buy_grade', 0)
            line += f"  {stars}{buy}"
        # V1.4.0: 逻辑覆盖层标注
        ov = score_result.get('overlay_notes') or []
        if ov:
            line += _c(format_overlay_summary(ov), Color.CYAN)
        print(line)
    
    # 风险警告
    if risk['has_critical']:
        for c in risk['triggered']:
            if c['level'] == 'critical':
                detail_text = c["detail"]
                print(f"    {_c('WARN ' + detail_text, Color.RED)}")
    
    return {
        'code': code, 'name': name, 'score': score_result,
        'detect': detect_result, 'risk': risk,
        'price': price, 'cost': cost,
    }


# ─── 全市场扫描 ───

def diagnose_scan(top_n: int = 20, detail: bool = False):
    """全市场动量扫描，输出 Top N"""
    try:
        from data_provider import get_all_stocks, fetch_klines_batch
    except ImportError:
        print("全市场扫描需要 volume-price-screener")
        return
    
    print(f"{_c('=== Momentum Scan ===', Color.BOLD)}")
    print(f"Fetching stock list...")
    
    stocks = get_all_stocks()
    print(f"Total: {len(stocks)} stocks, scanning...")
    
    # 分批获取K线并诊断
    batch_size = 500
    results = []
    total = len(stocks)
    
    for batch_start in range(0, total, batch_size):
        batch = stocks[batch_start:batch_start + batch_size]
        codes = [s['code'] for s in batch]
        
        # 获取K线
        klines = fetch_klines_batch(codes, count=90, workers=12)
        
        for stock, code in zip(batch, codes):
            kline = klines.get(code)
            if not kline or len(kline) < 20:
                continue
            
            detect_result = detect_all(kline, code=code)
            score_result = calculate_score(kline, detect_result)
            
            # 只收集持有和加仓信号
            if score_result['decision'] in ('hold', 'hold_buy'):
                results.append({
                    'code': code,
                    'name': stock.get('name', code),
                    'score': score_result,
                    'detect': detect_result,
                })
        
        pct = min(100, (batch_start + batch_size) * 100 // total)
        print(f"  {pct}% ({batch_start + batch_size}/{total})...")
    
    # 按评分排序
    results.sort(key=lambda r: r['score']['total'], reverse=True)
    top = results[:top_n]
    
    print(f"\n{_c(f'Top {len(top)} Momentum Stocks', Color.BOLD)}")
    print()
    
    for i, r in enumerate(top):
        line = format_score_compact(r['score'], r['detect'], r['name'], r['code'])
        print(f"{i+1:>3}. {line}")
    
    if detail:
        for r in top:
            print()
            output = format_score_output(r['score'], r['detect'], r['name'], r['code'])
            print(output)


# ─── 持仓批量 ───

def diagnose_portfolio(detail: bool = False, filepath: str = None):
    """批量诊断持仓文件中的所有股票"""
    positions = get_positions(filepath)
    if not positions:
        print("持仓文件为空，请先在 data/positions.json 中添加持仓")
        return
    
    # === V1.3.5: 加载前次决策用于滞回 ===
    prev_decisions = {}
    prev_file = filepath.replace('.json', '_prev_decisions.json') if filepath else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'prev_decisions.json'
    )
    try:
        if os.path.exists(prev_file):
            with open(prev_file, 'r') as f:
                prev_decisions = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    
    print(f"{_c('=== Momentum Position Advisor V1.3.5 ===', Color.BOLD)}")
    print()
    
    results = []
    current_decisions = {}
    for pos in positions:
        code = pos['code']
        cost = pos.get('cost', 0)
        prev_d = prev_decisions.get(code)
        result = diagnose_single(code, cost, detail, prev_decision=prev_d)
        if result:
            results.append(result)
            current_decisions[code] = result['score']['decision']
        print()
    
    # === V1.3.5: 保存当前决策供下次使用 ===
    try:
        os.makedirs(os.path.dirname(prev_file), exist_ok=True)
        with open(prev_file, 'w') as f:
            json.dump(current_decisions, f, indent=2)
    except (OSError, IOError):
        pass  # 写入失败不影响主流程
    
    # 汇总
    hold = [r for r in results if r['score']['decision'] in ('hold', 'hold_buy')]
    reduce_list = [r for r in results if r['score']['decision'] in ('reduce', 'reduce_watch')]
    watch_list = [r for r in results if r['score']['decision'] == 'watch']
    sell_list = [r for r in results if r['score']['decision'] == 'sell']
    
    print(f"{_c('--- Summary ---', Color.BOLD)}")
    parts = []
    if hold: parts.append(f"HOLD: {len(hold)}")
    if reduce_list: parts.append(f"REDUCE: {len(reduce_list)}")
    if watch_list: parts.append(f"WATCH: {len(watch_list)}")
    if sell_list: parts.append(f"SELL: {len(sell_list)}")
    print(f"  {'  '.join(parts)}")
    
    # 板块共振检测
    if len(results) >= 2:
        resonance_report, _ = detect_sector_resonance(results)
        if resonance_report:
            print(format_resonance_report(resonance_report))


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description='动量持仓顾问 V1.0')
    parser.add_argument('codes', nargs='*', help='股票代码列表')
    parser.add_argument('--cost', type=float, help='成本价（仅单股时有效）')
    parser.add_argument('--detail', action='store_true', help='输出五维评分明细')
    parser.add_argument('--portfolio', action='store_true', help='持仓批量诊断')
    parser.add_argument('--search', type=str, help='搜索股票名称')
    parser.add_argument('--scan', action='store_true', help='全市场动量扫描')
    parser.add_argument('--top', type=int, default=20, help='扫描Top N')
    parser.add_argument('--params', type=str, help='参数覆盖 JSON')
    parser.add_argument('--file', type=str, help='持仓文件路径')
    
    args = parser.parse_args()
    
    params = {}
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError:
            print(f"警告: 无效的 JSON 参数: {args.params}")
    
    # 持仓批量模式
    if args.portfolio:
        diagnose_portfolio(detail=args.detail, filepath=args.file)
        return
    
    # 全市场扫描模式
    if args.scan:
        diagnose_scan(top_n=args.top, detail=args.detail)
        return
    
    # 搜索模式
    codes = list(args.codes)
    if args.search:
        try:
            from data_provider import search_stock
            results = search_stock(args.search)
            if results:
                codes.append(results[0]['code'])
                print(f"搜索 '{args.search}' → {results[0]['name']}({results[0]['code']})")
            else:
                print(f"未找到 '{args.search}'")
                return
        except ImportError:
            print("搜索功能需要 volume-price-screener")
            return
    
    # 单股/多股模式
    if not codes:
        print("用法: python advisor.py <代码> [--cost 成本] [--detail]")
        print("      python advisor.py --portfolio [--detail]")
        print("      python advisor.py --search <名称>")
        sys.exit(1)
    
    cost = args.cost
    results = []
    
    for code in codes:
        result = diagnose_single(code, cost, args.detail)
        if result:
            results.append(result)
        if len(codes) > 1:
            print()
    
    # === 板块共振检测（仅多股模式） ===
    if len(results) >= 2:
        resonance_report, _ = detect_sector_resonance(results)
        if resonance_report:
            report = format_resonance_report(resonance_report)
            print(report)
            
            # 有共振降级时，重新输出调整后的评分
            has_downgrade = any(v >= 2 for v in resonance_report.values())
            if has_downgrade:
                print("\n─── 共振降级后评分 ───")
                _, adjusted = detect_sector_resonance(results)
                for a in adjusted:
                    score_data = a.get('score', {})
                    downgrade_info = score_data.get('sector_downgrade')
                    if downgrade_info:
                        name = a.get('name', a.get('code', ''))
                        code = a.get('code', '')
                        orig_d = downgrade_info['original_decision']
                        new_d = score_data['decision']
                        arrow = '⬇' if new_d != orig_d else '→'
                        print(f"  {arrow} {name}({code}): "
                              f"{downgrade_info['original_total']}分({orig_d}) "
                              f"→ {score_data['total']}分({new_d}) "
                              f"[{downgrade_info['reason'][:40]}...]")


if __name__ == '__main__':
    main()
