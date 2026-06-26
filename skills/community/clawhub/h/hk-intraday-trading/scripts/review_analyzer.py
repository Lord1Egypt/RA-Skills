#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股日内交易 - 复盘分析器
深度分析交易结果，提供策略优化建议
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict


class ReviewAnalyzer:
    """复盘分析器"""
    
    def __init__(self, skill_root: str = None):
        if skill_root is None:
            self.skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.skill_root = skill_root
        
        self.data_dir = os.path.join(self.skill_root, "data")
        self.output_dir = os.path.join(self.skill_root, "output")
        
        self.performance_data = self._load_json("performance_tracking.json")
        self.strategy_config = self._load_json("strategy_config.json")
    
    def _load_json(self, filename: str) -> Dict:
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def analyze(self, date: str = None) -> Dict:
        """深度分析复盘结果"""
        daily_stats = self.performance_data.get("daily_stats", [])
        
        if not daily_stats:
            return {"error": "暂无交易记录"}
        
        # 按结果类型统计
        results = {"no_buy": [], "stop_loss": [], "sell_achieved": []}
        for record in daily_stats:
            result = record.get("result", "unknown")
            if result in results:
                results[result].append(record)
        
        # 计算统计数据
        analysis = {
            "summary": self._calc_summary(daily_stats),
            "by_result": {
                "no_buy": self._analyze_no_buy(results["no_buy"]),
                "stop_loss": self._analyze_stop_loss(results["stop_loss"]),
                "sell_achieved": self._analyze_sell_achieved(results["sell_achieved"]),
            },
            "stock_analysis": self._analyze_by_stock(daily_stats),
            "strategy_insights": self._generate_insights(results, daily_stats),
            "win_rate": self._calc_win_rate(daily_stats),
        }
        
        return analysis
    
    def _calc_summary(self, daily_stats: List[Dict]) -> Dict:
        """计算汇总统计"""
        total = len(daily_stats)
        no_buy = sum(1 for d in daily_stats if d.get("result") == "no_buy")
        stop_loss = sum(1 for d in daily_stats if d.get("result") == "stop_loss")
        sell_achieved = sum(1 for d in daily_stats if d.get("result") == "sell_achieved")
        
        # 计算收益率
        total_pnl = sum(d.get("pnl_pct", 0) for d in daily_stats)
        avg_pnl = total_pnl / total if total > 0 else 0
        
        # 买入后的收益率（排除no_buy）
        trades_with_position = [d for d in daily_stats if d.get("result") in ["stop_loss", "sell_achieved"]]
        if trades_with_position:
            trade_pnl = sum(d.get("pnl_pct", 0) for d in trades_with_position)
            avg_trade_pnl = trade_pnl / len(trades_with_position)
        else:
            trade_pnl = 0
            avg_trade_pnl = 0
        
        return {
            "total_trades": total,
            "no_buy_count": no_buy,
            "stop_loss_count": stop_loss,
            "sell_achieved_count": sell_achieved,
            "no_buy_pct": round(no_buy / total * 100, 1) if total > 0 else 0,
            "stop_loss_pct": round(stop_loss / total * 100, 1) if total > 0 else 0,
            "sell_achieved_pct": round(sell_achieved / total * 100, 1) if total > 0 else 0,
            "total_pnl": round(total_pnl, 2),
            "avg_pnl_per_trade": round(avg_pnl, 2),
            "avg_pnl_after_buy": round(avg_trade_pnl, 2),
        }
    
    def _analyze_no_buy(self, records: List[Dict]) -> Dict:
        """分析没有成交的情况"""
        if not records:
            return {"count": 0, "reasons": [], "insights": []}
        
        # 统计原因
        reasons = defaultdict(int)
        for r in records:
            reason = r.get("reason", "未说明原因")
            reasons[reason] += 1
        
        # 分析：no_buy 说明买入价设置不合理（要么太高，要么开盘就涨停/不给你机会）
        insights = []
        if len(records) >= 2:
            insights.append("连续未成交，可能是买入价设置过于保守")
            insights.append("建议：适当提高买入价（减少折扣）或调整选股标准")
        elif len(records) >= 1:
            insights.append("未触发买入价，说明价格未跌到目标位置")
            insights.append("可能原因：1) 开盘高开 2) 买入价设置过高 3) 股票走势不及预期")
        
        return {
            "count": len(records),
            "avg_score": sum(r.get("score", 0) for r in records) / len(records) if records else 0,
            "top_reasons": dict(sorted(reasons.items(), key=lambda x: -x[1])[:3]),
            "insights": insights,
        }
    
    def _analyze_stop_loss(self, records: List[Dict]) -> Dict:
        """分析止损情况"""
        if not records:
            return {"count": 0, "avg_loss": 0, "reasons": [], "insights": []}
        
        losses = [r.get("pnl_pct", 0) for r in records]
        avg_loss = sum(losses) / len(losses) if losses else 0
        
        # 统计原因
        reasons = defaultdict(int)
        for r in records:
            reason = r.get("reason", "未说明原因")
            reasons[reason] += 1
        
        # 分析：止损说明选股或止损价设置有问题
        insights = []
        if len(records) >= 2:
            insights.append("连续止损，说明选股策略可能有问题")
            insights.append("建议：1) 提高选股评分标准 2) 放宽止损幅度 3) 更换股票池")
        elif len(records) >= 1:
            insights.append("触发止损，可能是：1) 选股时趋势判断错误 2) 止损幅度过窄 3) 市场整体下跌")
        
        return {
            "count": len(records),
            "avg_loss": round(avg_loss, 2),
            "max_loss": round(min(losses), 2) if losses else 0,
            "top_reasons": dict(sorted(reasons.items(), key=lambda x: -x[1])[:3]),
            "insights": insights,
        }
    
    def _analyze_sell_achieved(self, records: List[Dict]) -> Dict:
        """分析止盈情况"""
        if not records:
            return {"count": 0, "avg_gain": 0, "reasons": [], "insights": []}
        
        gains = [r.get("pnl_pct", 0) for r in records]
        avg_gain = sum(gains) / len(gains) if gains else 0
        
        # 统计原因
        reasons = defaultdict(int)
        for r in records:
            reason = r.get("reason", "未说明原因")
            reasons[reason] += 1
        
        # 分析：止盈是成功案例，分析为什么成功
        insights = []
        if len(records) >= 2:
            insights.append("多次止盈成功，说明当前选股策略有效")
            insights.append("建议：保持当前策略，可适当放宽选股条件增加机会")
        elif len(records) >= 1:
            insights.append("成功止盈，说明选股时趋势判断正确")
            insights.append("成功要素：1) 选对方向 2) 买入价合理 3) 波动够大")
        
        return {
            "count": len(records),
            "avg_gain": round(avg_gain, 2),
            "max_gain": round(max(gains), 2) if gains else 0,
            "top_reasons": dict(sorted(reasons.items(), key=lambda x: -x[1])[:3]),
            "insights": insights,
        }
    
    def _analyze_by_stock(self, daily_stats: List[Dict]) -> Dict:
        """按股票分析"""
        stock_stats = defaultdict(lambda: {"total": 0, "no_buy": 0, "stop_loss": 0, "sell_achieved": 0, "scores": []})
        
        for record in daily_stats:
            code = record.get("stock", "unknown")
            stock_stats[code]["total"] += 1
            result = record.get("result", "unknown")
            if result in stock_stats[code]:
                stock_stats[code][result] += 1
            score = record.get("score", 0)
            if score:
                stock_stats[code]["scores"].append(score)
        
        # 转换为列表并计算胜率
        result = {}
        for code, stats in stock_stats.items():
            trades = stats["stop_loss"] + stats["sell_achieved"]
            win_rate = stats["sell_achieved"] / trades * 100 if trades > 0 else 0
            avg_score = sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else 0
            
            result[code] = {
                "total": stats["total"],
                "no_buy": stats["no_buy"],
                "stop_loss": stats["stop_loss"],
                "sell_achieved": stats["sell_achieved"],
                "win_rate": round(win_rate, 1),
                "avg_score": round(avg_score, 1),
            }
        
        return result
    
    def _calc_win_rate(self, daily_stats: List[Dict]) -> Dict:
        """计算累计胜率"""
        # 只看有实际持仓的（排除no_buy）
        trades = [d for d in daily_stats if d.get("result") in ["stop_loss", "sell_achieved"]]
        
        if not trades:
            return {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "conclusion": "暂无实际交易数据"
            }
        
        wins = sum(1 for t in trades if t.get("result") == "sell_achieved")
        losses = sum(1 for t in trades if t.get("result") == "stop_loss")
        win_rate = wins / len(trades) * 100
        
        # 累计收益率
        total_pnl = sum(t.get("pnl_pct", 0) for t in trades)
        
        return {
            "total_trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 1),
            "total_pnl": round(total_pnl, 2),
            "avg_pnl": round(total_pnl / len(trades), 2),
            "conclusion": self._get_conclusion(win_rate, total_pnl)
        }
    
    def _get_conclusion(self, win_rate: float, total_pnl: float) -> str:
        """根据胜率和收益率给出结论"""
        if win_rate >= 60 and total_pnl > 0:
            return "🎉 策略表现优秀，保持当前策略"
        elif win_rate >= 50 and total_pnl > 0:
            return "✅ 策略基本可行，可适当优化"
        elif win_rate >= 40:
            return "⚠️ 策略表现一般，建议优化选股标准"
        else:
            return "🔴 策略表现较差，需要重大调整"
    
    def _generate_insights(self, results: Dict, daily_stats: List[Dict]) -> List[str]:
        """生成综合洞察"""
        insights = []
        
        no_buy = len(results["no_buy"])
        stop_loss = len(results["stop_loss"])
        sell_achieved = len(results["sell_achieved"])
        total = no_buy + stop_loss + sell_achieved
        
        if total == 0:
            return ["暂无数据"]
        
        # 分析no_buy率
        no_buy_rate = no_buy / total * 100
        if no_buy_rate > 50:
            insights.append(f"⚠️ 未成交率过高({no_buy_rate:.0f}%)，买入价可能设置过于保守")
            insights.append("→ 建议：减少买入折扣，或选择开盘更强势的股票")
        
        # 分析止损率
        if total - no_buy > 0:
            stop_loss_rate = stop_loss / (total - no_buy) * 100
            if stop_loss_rate > 60:
                insights.append(f"⚠️ 止损率过高({stop_loss_rate:.0f}%)，选股或止损设置有问题")
                insights.append("→ 建议：提高选股评分标准，或放宽止损幅度")
        
        # 分析止盈率
        if total - no_buy > 0:
            sell_rate = sell_achieved / (total - no_buy) * 100
            if sell_rate > 60:
                insights.append(f"✅ 止盈率较高({sell_rate:.0f}%)，当前选股策略有效")
        
        # 综合建议
        if no_buy_rate > 40 and stop_loss_rate > 40:
            insights.append("🔴 选股策略需要重大调整，建议重新评估选股标准")
        
        return insights
    
    def generate_report(self, date: str = None) -> str:
        """生成复盘分析报告"""
        analysis = self.analyze(date)
        
        if "error" in analysis:
            return f"错误: {analysis['error']}"
        
        s = analysis["summary"]
        wr = analysis["win_rate"]
        
        report = f"""
📊 港股日内交易复盘分析
══════════════════════════════════════

📈 总体统计
──────────────────────────────────────
  总选股次数: {s['total_trades']}
  未成交(no_buy): {s['no_buy_count']} ({s['no_buy_pct']}%)
  买入后止损: {s['stop_loss_count']} ({s['stop_loss_pct']}%)
  买入后卖出: {s['sell_achieved_count']} ({s['sell_achieved_pct']}%)

💰 收益率统计
──────────────────────────────────────
  累计收益率: {s['total_pnl']}%
  平均每笔收益: {s['avg_pnl_per_trade']}%
  买入后平均收益: {s['avg_pnl_after_buy']}%

🏆 累计胜率
──────────────────────────────────────
  实际交易次数: {wr['total_trades']}
  成功次数: {wr['wins']}
  失败次数: {wr['losses']}
  胜率: {wr['win_rate']}%
  结论: {wr['conclusion']}

🔍 深度分析
──────────────────────────────────────
"""
        
        # no_buy分析
        nb = analysis["by_result"]["no_buy"]
        if nb["count"] > 0:
            report += f"""
【未成交分析】{nb['count']}次
  平均评分: {nb['avg_score']:.0f}
  原因: {', '.join(nb['top_reasons'].keys())[:50]}
  洞察: {'; '.join(nb['insights'][:2])}
"""
        
        # stop_loss分析
        sl = analysis["by_result"]["stop_loss"]
        if sl["count"] > 0:
            report += f"""
【止损分析】{sl['count']}次
  平均亏损: {sl['avg_loss']}%
  最大亏损: {sl['max_loss']}%
  原因: {', '.join(sl['top_reasons'].keys())[:50]}
  洞察: {'; '.join(sl['insights'][:2])}
"""
        
        # sell_achieved分析
        sa = analysis["by_result"]["sell_achieved"]
        if sa["count"] > 0:
            report += f"""
【止盈分析】{sa['count']}次
  平均盈利: {sa['avg_gain']}%
  最大盈利: {sa['max_gain']}%
  原因: {', '.join(sa['top_reasons'].keys())[:50]}
  洞察: {'; '.join(sa['insights'][:2])}
"""
        
        # 综合洞察
        report += """
💡 策略优化建议
──────────────────────────────────────
"""
        for insight in analysis["strategy_insights"]:
            report += f"  {insight}\n"
        
        # 个股分析
        report += """
📊 个股表现
──────────────────────────────────────
"""
        for code, stats in analysis["stock_analysis"].items():
            name = code
            report += f"  {name}: 选股{stats['total']}次, 胜率{stats['win_rate']}%, 平均评分{stats['avg_score']}\n"
        
        report += f"""
══════════════════════════════════════
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        return report


def main():
    analyzer = ReviewAnalyzer()
    report = analyzer.generate_report()
    print(report)
    
    # 保存报告
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = f"/Users/xiaoputao/.openclaw/workspace/skills/hk-intraday-trading/output/复盘分析_{date_str}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {output_path}")


if __name__ == "__main__":
    main()