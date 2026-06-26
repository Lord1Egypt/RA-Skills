# -*- coding: utf-8 -*-
"""
多策略统一运行器 v2.0

功能：
  - 执行所有已集成的量化策略
  - 策略间相关性分析
  - 组合收益对比
  - 多策略资产配置建议

用法:
  python strategy_runner.py                    # 运行所有策略
  python strategy_runner.py --strategy csi300  # 只运行沪深300指增
  python strategy_runner.py --list             # 列出所有可用策略
  python strategy_runner.py --date 2026-05-16  # 指定日期
  python strategy_runner.py --correlation      # 策略相关性分析
  python strategy_runner.py --compare          # 策略绩效对比
  python strategy_runner.py --portfolio        # 多策略资产配置
"""

import sys
import os
import json
import argparse
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# 策略注册表
# ============================================================

STRATEGIES = {
    'csi300': {
        'name': '沪深300指增策略',
        'module': 'strategies.csi300_enhanced',
        'class': 'CSI300EnhancedStrategy',
        'bench': '000300.SH',
        'rebalance': 'monthly',
        'desc': 'ICIR加权多因子，月度调仓，2025超额10.7%',
        'category': '宽基指增',
    },
    'csi500': {
        'name': '中证500指增策略',
        'module': 'strategies.csi500_enhanced',
        'class': 'CSI500EnhancedStrategy',
        'bench': '000905.SH',
        'rebalance': 'monthly',
        'desc': 'ICIR加权/风险预算复合，2025超额9.5%/29.97%',
        'category': '宽基指增',
    },
    'csi1000': {
        'name': '中证1000指增策略',
        'module': 'strategies.csi1000_enhanced',
        'class': 'CSI1000EnhancedStrategy',
        'bench': '000852.SH',
        'rebalance': 'monthly',
        'desc': '多模型融合+AI，2025超额17.49%',
        'category': '宽基指增',
    },
    'multi_composite': {
        'name': '多策略复合因子',
        'module': 'strategies.multi_strategy_composite',
        'class': 'CompositeStrategy',
        'bench': '000300.SH',
        'rebalance': 'monthly',
        'desc': '60%基础+30%域内+10%域外，年化超额12.6%',
        'category': '主动量化',
    },
    'quant_selection': {
        'name': '量化选股(空气指增)',
        'module': 'strategies.quant_stock_selection',
        'class': 'QuantStockSelectionStrategy',
        'bench': '无基准',
        'rebalance': 'weekly',
        'desc': '全市场无约束，AI驱动，2025收益45.02%',
        'category': '主动量化',
    },
    'growth_stage': {
        'name': '成长期优选组合',
        'module': 'strategies.growth_stage_portfolio',
        'class': 'GrowthStagePortfolioStrategy',
        'bench': '000906.SH',
        'rebalance': 'monthly',
        'desc': '三层递进筛选，2025收益84.1%',
        'category': '主动量化',
    },
    'kcb': {
        'name': '科创板策略',
        'module': 'strategies.kcb_strategy',
        'class': 'KCBStrategy',
        'bench': '000688.SH',
        'rebalance': 'monthly',
        'desc': '四因子等权，2025收益~18.61%',
        'category': '特色策略',
    },
    'factor16_m': {
        'name': '16因子量价(月频)',
        'module': 'strategies.factor16_monthly',
        'class': 'Factor16MonthlyStrategy',
        'bench': '全市场中性',
        'rebalance': 'monthly',
        'desc': '高频因子低频化，年化收益47.51%',
        'category': '高频量价',
    },
    'factor16_w': {
        'name': '16因子量价(周频)',
        'module': 'strategies.factor16_weekly',
        'class': 'Factor16WeeklyStrategy',
        'bench': '全市场中性',
        'rebalance': 'weekly',
        'desc': '周度调仓，年化收益82.67%',
        'category': '高频量价',
    },
}

# 策略绩效参考数据
PERF = {
    'csi300':       {'2025_excess': 10.7,  '2025_total': 31.22, 'method': 'ICIR加权多因子',   'te': 4.0,  'n': 100},
    'csi500':       {'2025_excess': 9.5,   '2025_total': 40.0,  'method': '风险预算复合',       'te': 4.0,  'n': 120},
    'csi1000':      {'2025_excess': 17.49, '2025_total': 50.0,  'method': '多模型融合+AI',     'te': 6.0,  'n': 100},
    'multi_composite':{'annual_excess':12.6,'method': '60/30/10卫星',   'te': 5.2,  'n': 130, 'ir': 2.38},
    'quant_selection':{'2025_total':45.02, 'method': '全市场AI',        'te': None, 'n': 100},
    'growth_stage': {'2025_total': 84.1,   '2025_excess_csi800': 63.2,  'method': '三层筛选',  'n': 50},
    'kcb':          {'2025_total': 18.61,  'method': '四因子等权',       'n': 30},
    'factor16_m':   {'annual_long_short': 47.51, 'method': '分钟因子月频', 'monthly_dd': 1.24},
    'factor16_w':   {'annual_long_short': 82.67, 'method': '分钟因子周频', 'weekly_dd': 5.75},
}


def list_strategies():
    """列出所有可用策略"""
    print(f"\n📊 可用策略列表 ({len(STRATEGIES)} 个):\n")
    print(f"{'代码':<15} {'策略名称':<16} {'类别':<10} {'调仓':<8} {'基准':<12} 说明")
    print("-" * 110)
    for code, info in STRATEGIES.items():
        print(f"{code:<15} {info['name']:<16} {info['category']:<10} {info['rebalance']:<8} {info['bench']:<12} {info['desc']}")
    print()


def run_strategy(strategy_code: str, date_str: str, config: dict = None):
    """运行单个策略"""
    if strategy_code not in STRATEGIES:
        print(f"❌ 未知策略: {strategy_code}")
        list_strategies()
        return None

    info = STRATEGIES[strategy_code]
    print(f"\n🚀 启动策略: {info['name']}")
    print(f"   日期: {date_str}")
    print(f"   基准: {info['bench']}")

    # TODO: 动态导入并实例化
    # from importlib import import_module
    # mod = import_module(info['module'])
    # cls = getattr(mod, info['class'])
    # strategy = cls(config)
    # result = strategy.run(date_str)

    print(f"\n⚠️  数据源尚未接入，当前为框架演示模式")

    return {'strategy': strategy_code, 'name': info['name'], 'date': date_str, 'status': 'framework_ready'}


def run_all(date_str: str):
    """运行所有策略"""
    results = {}
    for code in STRATEGIES:
        results[code] = run_strategy(code, date_str)

    print(f"\n{'='*60}")
    print(f"📊 多策略运行汇总 — {date_str}")
    print(f"{'='*60}")
    for code, result in results.items():
        status = result.get('status', 'unknown') if result else 'error'
        name = STRATEGIES[code]['name']
        print(f"  {code} ({name}): {status}")

    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'multi_strategy_{date_str}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n✅ 结果已保存: {output_file}")
    return results


def show_correlation():
    """策略间相关性分析"""
    print(f"\n🔗 策略间相关性分析")
    print(f"{'='*80}")
    print(f"\n基于策略方法论和选股逻辑的定性相关性矩阵：\n")

    codes = list(STRATEGIES.keys())
    names = [STRATEGIES[c]['name'][:8] for c in codes]

    # 定性相关性矩阵（基于策略特性估算）
    corr_matrix = {
        'csi300':       {'csi300':1.0, 'csi500':0.7, 'csi1000':0.5, 'multi_composite':0.8, 'quant_selection':0.4, 'growth_stage':0.3, 'kcb':0.2, 'factor16_m':0.3, 'factor16_w':0.25},
        'csi500':       {'csi300':0.7, 'csi500':1.0, 'csi1000':0.75,'multi_composite':0.6, 'quant_selection':0.5, 'growth_stage':0.4, 'kcb':0.3, 'factor16_m':0.4, 'factor16_w':0.35},
        'csi1000':      {'csi300':0.5, 'csi500':0.75,'csi1000':1.0, 'multi_composite':0.5, 'quant_selection':0.6, 'growth_stage':0.5, 'kcb':0.4, 'factor16_m':0.5, 'factor16_w':0.45},
        'multi_composite':{'csi300':0.8,'csi500':0.6, 'csi1000':0.5, 'multi_composite':1.0,'quant_selection':0.45,'growth_stage':0.35,'kcb':0.25,'factor16_m':0.35,'factor16_w':0.3},
        'quant_selection':{'csi300':0.4,'csi500':0.5, 'csi1000':0.6, 'multi_composite':0.45,'quant_selection':1.0,'growth_stage':0.6, 'kcb':0.5, 'factor16_m':0.6, 'factor16_w':0.55},
        'growth_stage': {'csi300':0.3, 'csi500':0.4, 'csi1000':0.5, 'multi_composite':0.35,'quant_selection':0.6, 'growth_stage':1.0, 'kcb':0.6, 'factor16_m':0.4, 'factor16_w':0.35},
        'kcb':          {'csi300':0.2, 'csi500':0.3, 'csi1000':0.4, 'multi_composite':0.25,'quant_selection':0.5, 'growth_stage':0.6, 'kcb':1.0, 'factor16_m':0.3, 'factor16_w':0.25},
        'factor16_m':   {'csi300':0.3, 'csi500':0.4, 'csi1000':0.5, 'multi_composite':0.35,'quant_selection':0.6, 'growth_stage':0.4, 'kcb':0.3, 'factor16_m':1.0, 'factor16_w':0.85},
        'factor16_w':   {'csi300':0.25,'csi500':0.35,'csi1000':0.45,'multi_composite':0.3, 'quant_selection':0.55,'growth_stage':0.35,'kcb':0.25,'factor16_m':0.85,'factor16_w':1.0},
    }

    # 打印矩阵头部
    header = f"{'':<15}" + "".join([f"{n:>10}" for n in names])
    print(header)
    print("-" * len(header))

    for c1 in codes:
        row = f"{STRATEGIES[c1]['name'][:10]:<15}"
        for c2 in codes:
            r = corr_matrix.get(c1, {}).get(c2, 0)
            # 颜色标记
            if r >= 0.8:
                row += f"{r:>10.2f}🔴"
            elif r >= 0.5:
                row += f"{r:>10.2f}🟡"
            else:
                row += f"{r:>10.2f}🟢"
        print(row)

    print(f"\n🔴 高相关(≥0.8) | 🟡 中相关(0.5-0.8) | 🟢 低相关(<0.5)")
    print(f"\n💡 低相关策略组合建议:")
    print(f"  • 沪深300指增 + 成长期优选 (相关~0.3) — 大盘稳健 + 成长进攻")
    print(f"  • 多策略复合 + 科创板 (相关~0.25) — 宽基增强 + 科技弹性")
    print(f"  • 16因子量价 + 沪深300指增 (相关~0.3) — 量价Alpha + 基本面Alpha")
    print(f"  • 量化选股 + 中证500指增 (相关~0.5) — 全市场自由 + 中盘约束")


def show_comparison():
    """策略绩效对比"""
    print(f"\n📈 策略绩效对比")
    print(f"{'='*100}\n")

    print(f"{'策略':<16} {'类别':<10} {'2025收益/超额':<16} {'方法':<16} {'调仓':<6} {'TE':<5} {'持仓':<5}")
    print("-" * 100)

    for code, info in STRATEGIES.items():
        p = PERF.get(code, {})
        ret = ''
        if '2025_excess' in p:
            ret = f"超额 {p['2025_excess']}%"
        elif '2025_total' in p:
            ret = f"{p['2025_total']}%"
        elif 'annual_excess' in p:
            ret = f"年化超额 {p['annual_excess']}%"
        elif 'annual_long_short' in p:
            ret = f"多空 {p['annual_long_short']}%"

        te = f"{p.get('te', '-')}" if p.get('te') else '-'
        n = p.get('n', '-')

        print(f"{info['name'][:14]:<16} {info['category']:<10} {ret:<16} {p.get('method',''):<16} {info['rebalance']:<6} {te:<5} {n:<5}")

    print(f"\n💡 收益弹性排序 (从高到低):")
    elastic = [
        ('成长期优选组合', '84.1%', '进攻型'),
        ('16因子量价(周频)', '82.67%', '进攻型'),
        ('16因子量价(月频)', '47.51%', '均衡型'),
        ('量化选股(空气指增)', '45.02%', '进攻型'),
        ('中证1000指增', '~50%', '均衡型'),
        ('中证500指增', '~40%', '稳健型'),
        ('沪深300指增', '31.22%', '稳健型'),
        ('科创板策略', '18.61%', '特色型'),
        ('多策略复合因子', '年化12.6%超额', '均衡型'),
    ]
    for i, (name, ret, style) in enumerate(elastic, 1):
        print(f"  {i}. {name} — {ret} ({style})")


def show_portfolio_suggestion():
    """多策略资产配置建议"""
    print(f"\n💼 多策略资产配置建议")
    print(f"{'='*80}\n")

    portfolios = {
        '稳健型': {
            'desc': '追求稳健超额收益，控制回撤',
            'alloc': {
                '沪深300指增': '35%',
                '中证500指增': '25%',
                '多策略复合因子': '25%',
                '16因子量价(月频)': '15%',
            },
            'expected_excess': '8-12%年化超额',
            'expected_dd': '回撤 < 10%',
        },
        '均衡型': {
            'desc': '收益风险平衡，风格分散',
            'alloc': {
                '沪深300指增': '20%',
                '中证500指增': '15%',
                '中证1000指增': '15%',
                '成长期优选组合': '15%',
                '量化选股(空气指增)': '15%',
                '16因子量价(月频)': '10%',
                '科创板策略': '10%',
            },
            'expected_excess': '15-25%年化',
            'expected_dd': '回撤 10-20%',
        },
        '进攻型': {
            'desc': '追求高弹性收益，接受较大回撤',
            'alloc': {
                '成长期优选组合': '30%',
                '16因子量价(周频)': '25%',
                '量化选股(空气指增)': '25%',
                '中证1000指增': '10%',
                '科创板策略': '10%',
            },
            'expected_return': '40-80%年化',
            'expected_dd': '回撤 20-35%',
        },
        '全天候': {
            'desc': '跨风格、跨周期、跨策略全覆盖',
            'alloc': {
                '沪深300指增': '15%',
                '中证500指增': '10%',
                '中证1000指增': '10%',
                '多策略复合因子': '15%',
                '成长期优选组合': '15%',
                '量化选股(空气指增)': '10%',
                '16因子量价(月频)': '10%',
                '科创板策略': '10%',
                '现金/对冲': '5%',
            },
            'expected_return': '20-40%年化',
            'expected_dd': '回撤 15-25%',
        },
    }

    for name, pf in portfolios.items():
        print(f"🔹 {name} 组合 — {pf['desc']}")
        print(f"   {'─'*50}")
        for strategy, weight in pf['alloc'].items():
            print(f"     {strategy:<18} {weight}")
        ret_key = 'expected_return' if 'return' in str(pf.get('expected_return','')) else 'expected_excess'
        exp = pf.get('expected_return') or pf.get('expected_excess')
        print(f"   预期: {exp}")
        print(f"   回撤: {pf['expected_dd']}")
        print()


def main():
    parser = argparse.ArgumentParser(description='多策略量化选股运行器 v2.0')
    parser.add_argument('--strategy', '-s', type=str, help='运行指定策略')
    parser.add_argument('--date', '-d', type=str, default=None, help='交易日期 YYYY-MM-DD')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有策略')
    parser.add_argument('--correlation', '-c', action='store_true', help='策略相关性分析')
    parser.add_argument('--compare', action='store_true', help='策略绩效对比')
    parser.add_argument('--portfolio', '-p', action='store_true', help='资产配置建议')
    parser.add_argument('--config', type=str, help='配置文件路径')

    args = parser.parse_args()
    date_str = args.date or date.today().strftime('%Y-%m-%d')

    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)

    if args.list:
        list_strategies()
        return
    if args.correlation:
        show_correlation()
        return
    if args.compare:
        show_comparison()
        return
    if args.portfolio:
        show_portfolio_suggestion()
        return

    if args.strategy:
        run_strategy(args.strategy, date_str, config)
    else:
        run_all(date_str)


if __name__ == '__main__':
    main()
