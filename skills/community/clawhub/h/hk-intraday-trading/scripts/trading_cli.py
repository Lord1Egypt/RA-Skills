#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股日内交易 - 命令行工具
用法:
  python trading_cli.py record 2026-03-12 09988 阿里巴巴-SW 75 stop_loss -1.5 "数据源错误"
  python trading_cli.py status
  python trading_cli.py adjust
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feedback_loop import FeedbackLoop
from hk_simple_picker import HKSimplePicker


def cmd_status(args):
    """查看当前状态"""
    loop = FeedbackLoop()
    status = loop.get_strategy_status()
    
    print("\n" + "=" * 60)
    print("📊 港股日内交易 - 当前状态")
    print("=" * 60)
    
    print("\n🎯 策略参数:")
    print(f"  选股最低评分: {status['strategy_config']['min_score']}")
    print(f"  止损幅度: {status['strategy_config']['stop_loss_pct']}%")
    print(f"  目标涨幅: {status['strategy_config']['target_gain_pct']}%")
    print(f"  最大持仓: {status['strategy_config']['max_positions']}只")
    print(f"  最后更新: {status['strategy_config']['last_updated']}")
    
    print("\n📈 表现汇总:")
    summary = status['performance_summary']
    print(f"  交易天数: {summary.get('total_trading_days', 0)}")
    print(f"  总选股次数: {summary.get('total_selections', 0)}")
    print(f"  买入次数: {summary.get('total_buys', 0)}")
    print(f"  卖出成功: {summary.get('total_sells_achieved', 0)}")
    print(f"  止损触发: {summary.get('total_stop_loss', 0)}")
    print(f"  买入成功率: {summary.get('buy_success_rate_pct', 0)}%")
    print(f"  总盈亏: {summary.get('overall_profit_pct', 0)}%")
    print(f"  平均盈亏: {summary.get('avg_profit_per_trade_pct', 0)}%")
    print(f"  最佳交易: {summary.get('best_trade_pct', 0)}%")
    print(f"  最差交易: {summary.get('worst_trade_pct', 0)}%")
    
    print("\n📝 最近优化:")
    for opt in status['optimization_history']:
        print(f"  [{opt['date']}] {opt['change']}")
        print(f"           原因: {opt['reason']}")
        print(f"           结果: {opt.get('result', '待验证')}")
    
    print("\n💡 最近经验:")
    for lesson in status['recent_lessons']:
        print(f"  [{lesson['date']}] {lesson['lesson']}")
        print(f"           影响: {lesson['impact']} → {lesson['action']}")
    
    print("\n" + "=" * 60)
    return 0


def cmd_record(args):
    """记录交易结果
    
    结果选项（只有3种）：
    - no_buy: 没有成交（未触发买入价）
    - stop_loss: 买入后触发止损
    - sell_achieved: 买入后触发卖出价
    """
    if len(args) < 6:
        print("用法: python trading_cli.py record <日期> <代码> <名称> <评分> <结果> <盈亏> [原因]")
        print("结果选项（只有3种）: no_buy, stop_loss, sell_achieved")
        return 1
    
    date = args[0]
    code = args[1]
    name = args[2]
    score = int(args[3])
    result = args[4]
    pnl_pct = float(args[5])
    reason = args[6] if len(args) > 6 else ""
    
    loop = FeedbackLoop()
    result = loop.manual_record(date, code, name, score, result, pnl_pct, reason)
    
    print(f"\n✅ 已记录交易结果")
    print(f"   股票: {name} ({code})")
    print(f"   结果: {result['recorded']} 笔")
    
    if result['adjustments']:
        print(f"\n🔄 自动触发策略调整:")
        for adj in result['adjustments']:
            print(f"   {adj['type']}: {adj['from']} → {adj['to']}")
            print(f"   原因: {adj['reason']}")
    
    return 0


def cmd_pick(args):
    """运行选股"""
    print("\n🖥️ 运行盘前选股...")
    picker = HKSimplePicker()
    suggestions = picker.run_daily_selection()
    
    if suggestions:
        print(f"\n✅ 选出 {len(suggestions)} 只股票:")
        for s in suggestions:
            print(f"   {s['stock_name']} ({s['stock_code']}) - 评分: {s['score']} - {s['action']}")
    else:
        print("\n⚠️ 今日无符合条件的股票")
    
    return 0


def cmd_adjust(args):
    """手动调整策略"""
    if len(args) < 2:
        print("用法: python trading_cli.py adjust <参数> <值>")
        print("参数: min_score, stop_loss_pct, target_gain_pct, max_positions")
        return 1
    
    param = args[0]
    value = args[1]
    
    loop = FeedbackLoop()
    config = loop.strategy_config
    
    # 根据参数类型调整
    if param == "min_score":
        config["selection_criteria"]["min_score"] = int(value)
    elif param == "stop_loss_pct":
        config["trade_settings"]["stop_loss_pct"] = float(value)
    elif param == "target_gain_pct":
        config["trade_settings"]["target_gain_pct"] = float(value)
    elif param == "max_positions":
        config["trade_settings"]["max_positions"] = int(value)
    else:
        print(f"未知参数: {param}")
        return 1
    
    # 添加优化历史
    from datetime import datetime
    if "optimization_history" not in config:
        config["optimization_history"] = []
    
    config["optimization_history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "change": f"手动调整: {param} = {value}",
        "reason": "人工优化",
        "result": "待验证"
    })
    
    config["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    loop._save_json("strategy_config.json", config)
    print(f"\n✅ 已调整 {param} = {value}")
    
    return 0


def cmd_lesson(args):
    """添加经验教训"""
    if len(args) < 3:
        print("用法: python trading_cli.py lesson <经验> <影响> <行动>")
        return 1
    
    lesson = args[0]
    impact = args[1]
    action = " ".join(args[2:])
    
    from datetime import datetime
    loop = FeedbackLoop()
    loop.add_lesson_learned(datetime.now().strftime("%Y-%m-%d"), lesson, impact, action)
    
    print(f"\n✅ 已添加经验: {lesson}")
    return 0


def cmd_review(args):
    """深度复盘分析"""
    try:
        from review_analyzer import ReviewAnalyzer
        analyzer = ReviewAnalyzer()
        
        if args and args[0] == "--report":
            # 生成完整报告
            report = analyzer.generate_report()
            print(report)
        else:
            # 快速查看关键指标
            analysis = analyzer.analyze()
            wr = analysis.get("win_rate", {})
            s = analysis.get("summary", {})
            
            print("\n📊 快速复盘摘要")
            print("=" * 40)
            print(f"  累计胜率: {wr.get('win_rate', 0)}% ({wr.get('wins', 0)}/{wr.get('total_trades', 0)})")
            print(f"  累计收益: {wr.get('total_pnl', 0)}%")
            print(f"  平均每笔: {wr.get('avg_pnl', 0)}%")
            print()
            print(f"  未成交: {s.get('no_buy_count', 0)}次 ({s.get('no_buy_pct', 0)}%)")
            print(f"  止损: {s.get('stop_loss_count', 0)}次 ({s.get('stop_loss_pct', 0)}%)")
            print(f"  止盈: {s.get('sell_achieved_count', 0)}次 ({s.get('sell_achieved_pct', 0)}%)")
            print()
            print(f"  结论: {wr.get('conclusion', '暂无')}")
            print("=" * 40)
            print("  完整报告: python trading_cli.py review --report")
        
        return 0
    except Exception as e:
        print(f"复盘分析失败: {e}")
        return 1


def main():
    if len(sys.argv) < 2:
        print("港股日内交易命令行工具")
        print("=" * 50)
        print("核心交易逻辑：盘前选股 → 默认按选股信息交易 → 盘后复盘")
        print()
        print("复盘结果（只有3种）:")
        print("  - no_buy       : 没有成交（未触发买入价）")
        print("  - stop_loss    : 买入后触发止损价卖出")
        print("  - sell_achieved: 买入后触发卖出价止盈")
        print()
        print("用法:")
        print("  python trading_cli.py status           查看当前状态")
        print("  python trading_cli.py pick              运行盘前选股")
        print("  python trading_cli.py record <args>     记录交易结果")
        print("  python trading_cli.py review            快速复盘摘要")
        print("  python trading_cli.py review --report   完整复盘报告")
        print("  python trading_cli.py adjust <args>     手动调整策略")
        print("  python trading_cli.py lesson <args>     添加经验教训")
        print()
        print("示例:")
        print("  python trading_cli.py record 2026-03-12 09988 阿里巴巴-SW 75 no_buy 0 \"未触发买入价\"")
        print("  python trading_cli.py record 2026-03-12 03690 美团-W 80 stop_loss -1.5 \"触发止损\"")
        print("  python trading_cli.py record 2026-03-12 01810 小米-W 75 sell_achieved 1.0 \"达到目标\"")
        print("  python trading_cli.py adjust min_score 70")
        print("  python trading_cli.py review")
        return 0
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "status":
        return cmd_status(args)
    elif cmd == "record":
        return cmd_record(args)
    elif cmd == "pick":
        return cmd_pick(args)
    elif cmd == "adjust":
        return cmd_adjust(args)
    elif cmd == "lesson":
        return cmd_lesson(args)
    elif cmd == "review":
        return cmd_review(args)
    else:
        print(f"未知命令: {cmd}")
        return 1


if __name__ == "__main__":
    sys.exit(main())