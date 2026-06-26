#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股日内交易 - 自动反馈闭环
核心功能：复盘结果 → 自动更新策略参数 → 下次选股自动应用
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FeedbackLoop:
    """自动反馈闭环控制器"""
    
    def __init__(self, skill_root: str = None):
        # 技能根目录
        if skill_root is None:
            self.skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        else:
            self.skill_root = skill_root
        
        self.data_dir = os.path.join(self.skill_root, "data")
        self.output_dir = os.path.join(self.skill_root, "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 加载配置文件
        self.strategy_config = self._load_json("strategy_config.json")
        self.performance_data = self._load_json("performance_tracking.json")
        
        # 闭环阈值配置
        self.config = {
            "auto_adjust_threshold": 3,  # 连续3次失败触发自动调整
            "min_score_adjust": 5,       # 每次调整5分
            "max_score": 85,             # 最高评分上限
            "min_score": 50,             # 最低评分下限
            "consecutive_loss_threshold": 3,  # 连续亏损阈值
            "win_rate_improvement_target": 0.1,  # 目标胜率提升
        }
    
    def _load_json(self, filename: str) -> Dict:
        """加载JSON文件"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_json(self, filename: str, data: Dict) -> None:
        """保存JSON文件"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"已保存: {filepath}")
    
    def get_latest_pick_file(self, date: str = None) -> Optional[str]:
        """获取最近的选股结果文件"""
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        picks_dir = os.path.join(self.output_dir, "picks")
        if not os.path.exists(picks_dir):
            return None
        
        # 查找指定日期的文件
        for filename in os.listdir(picks_dir):
            if date in filename and filename.endswith('.json'):
                return os.path.join(picks_dir, filename)
        return None
    
    def get_market_data(self, date: str) -> Dict[str, Any]:
        """获取当日市场数据（从复盘报告或其他来源）"""
        # 查找复盘报告
        reports_dir = self.output_dir
        report_file = os.path.join(reports_dir, f"港股交易复盘报告_{date}.md")
        
        if not os.path.exists(report_file):
            # 尝试查找修正版
            report_file = os.path.join(reports_dir, f"港股交易复盘报告_{date}_修正版.md")
        
        market_data = {}
        if os.path.exists(report_file):
            logger.info(f"找到复盘报告: {report_file}")
            # TODO: 从报告解析市场数据
            # 目前先返回空，让调用者手动输入
        
        return market_data
    
    def record_daily_result(self, date: str, stock_results: List[Dict]) -> Dict:
        """
        记录当日交易结果（由人工或系统输入）
        
        结果选项（只有3种）：
        - no_buy: 没有成交（未触发买入价）
        - stop_loss: 买入后触发止损价卖出
        - sell_achieved: 买入后触发卖出价止盈
        
        stock_results 格式:
        [
            {
                "code": "09988.HK",
                "name": "阿里巴巴-SW",
                "score": 75,
                "result": "stop_loss",  # no_buy | stop_loss | sell_achieved
                "pnl_pct": -1.5,
                "reason": "说明"
            },
            ...
        ]
        """
        logger.info(f"记录 {date} 的交易结果...")
        
        # 更新每日统计
        if "daily_stats" not in self.performance_data:
            self.performance_data["daily_stats"] = []
        
        # 添加当日记录
        for result in stock_results:
            daily_record = {
                "date": date,
                "stock": result["code"],
                "stock_name": result["name"],
                "result": result["result"],
                "score": result.get("score", 0),
                "pnl_pct": result.get("pnl_pct", 0),
                "reason": result.get("reason", "")
            }
            self.performance_data["daily_stats"].append(daily_record)
        
        # 更新汇总统计（只有3种结果：no_buy, stop_loss, sell_achieved）
        self._update_summary_stats()
        
        # 更新个股表现（只有3种结果）
        for result in stock_results:
            self._update_stock_performance(result)
        
        # 保存更新后的数据
        self.performance_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        self._save_json("performance_tracking.json", self.performance_data)
        
        logger.info(f"已记录 {len(stock_results)} 条交易结果")
        
        # 检查是否需要自动调整策略
        adjustments = self.check_and_adjust_strategy(date)
        
        return {
            "recorded": len(stock_results),
            "adjustments": adjustments,
            "summary": self.performance_data.get("summary", {})
        }
    
    def _update_summary_stats(self) -> None:
        """更新汇总统计"""
        daily_stats = self.performance_data.get("daily_stats", [])
        
        if not daily_stats:
            return
        
        total_trading_days = len(set(d.stat.get("date", "") for d in daily_stats if hasattr(d, 'stat')))
        # 修正：直接用字典列表
        dates = set(d["date"] for d in daily_stats)
        
        total_selections = len(daily_stats)
        total_buys = sum(1 for d in daily_stats if d.get("result") in ["stop_loss", "sell_achieved", "hold_to_close"])
        total_sells_achieved = sum(1 for d in daily_stats if d.get("result") == "sell_achieved")
        total_stop_loss = sum(1 for d in daily_stats if d.get("result") == "stop_loss")
        total_hold = sum(1 for d in daily_stats if d.get("result") == "hold_to_close")
        
        # 计算胜率
        closed_trades = total_sells_achieved + total_stop_loss
        sell_success_rate = (total_sells_achieved / closed_trades * 100) if closed_trades > 0 else 0
        
        # 计算总盈亏
        total_pnl = sum(d.get("pnl_pct", 0) for d in daily_stats)
        avg_pnl = total_pnl / total_selections if total_selections > 0 else 0
        
        # 找出最佳和最差交易
        pnls = [d.get("pnl_pct", 0) for d in daily_stats]
        best_trade = max(pnls) if pnls else 0
        worst_trade = min(pnls) if pnls else 0
        
        self.performance_data["summary"] = {
            "total_trading_days": len(dates),
            "total_selections": total_selections,
            "total_buys": total_buys,
            "total_sells_achieved": total_sells_achieved,
            "total_stop_loss": total_stop_loss,
            "total_hold_to_close": total_hold,
            "buy_success_rate_pct": round(sell_success_rate, 1),
            "overall_profit_pct": round(total_pnl, 2),
            "avg_profit_per_trade_pct": round(avg_pnl, 2),
            "best_trade_pct": round(best_trade, 2),
            "worst_trade_pct": round(worst_trade, 2)
        }
    
    def _update_stock_performance(self, result: Dict) -> None:
        """更新个股表现数据"""
        code = result["code"]
        
        if "stock_performance" not in self.performance_data:
            self.performance_data["stock_performance"] = {}
        
        if code not in self.performance_data["stock_performance"]:
            self.performance_data["stock_performance"][code] = {
                "name": result["name"],
                "total_picks": 0,
                "total_buys": 0,
                "successful_sells": 0,
                "stop_losses": 0,
                "hold_to_close": 0,
                "win_rate": 0,
                "avg_pnl_pct": 0,
                "results": []
            }
        
        stock = self.performance_data["stock_performance"][code]
        stock["total_picks"] += 1
        
        result_type = result.get("result")
        pnl = result.get("pnl_pct", 0)
        
        # 只有3种结果：no_buy, stop_loss, sell_achieved
        # no_buy = 未触发买入价，没有成交
        # stop_loss = 触发止损价卖出
        # sell_achieved = 触发卖出价止盈
        
        if result_type in ["stop_loss", "sell_achieved"]:
            stock["total_buys"] += 1  # 只有这两种才算买入
        
        if result_type == "sell_achieved":
            stock["successful_sells"] += 1
        elif result_type == "stop_loss":
            stock["stop_losses"] += 1
        # no_buy 不计入买卖统计
        
        # 记录结果用于计算连续性
        stock["results"] = stock.get("results", [])[-29:] + [result_type]  # 保留最近30条
        
        # 计算胜率
        closed = stock["successful_sells"] + stock["stop_losses"]
        if closed > 0:
            stock["win_rate"] = stock["successful_sells"] / closed
        
        # 计算平均盈亏
        results = stock.get("results", [])
        if results:
            # 简化：成功的pnl用目标收益率，失败的用实际pnl
            avg_pnl = sum(r.get("pnl_pct", 0) for r in [result]) / len([result])
            # 重新计算所有历史
            all_pnls = []
            for r in self.performance_data["daily_stats"]:
                if r.get("stock") == code:
                    all_pnls.append(r.get("pnl_pct", 0))
            if all_pnls:
                stock["avg_pnl_pct"] = round(sum(all_pnls) / len(all_pnls), 2)
    
    def check_and_adjust_strategy(self, date: str) -> List[Dict]:
        """
        检查策略表现并自动调整
        返回调整记录列表
        """
        adjustments = []
        summary = self.performance_data.get("summary", {})
        
        # 检查连续亏损
        recent_stats = [d for d in self.performance_data.get("daily_stats", []) 
                       if d.get("result") in ["stop_loss", "hold_to_close"]]
        recent_stats = recent_stats[-5:]  # 最近5笔
        
        consecutive_losses = 0
        for stat in reversed(recent_stats):
            if stat.get("result") == "stop_loss":
                consecutive_losses += 1
            else:
                break
        
        # 如果连续亏损 >= 阈值，触发自动调整
        if consecutive_losses >= self.config["consecutive_loss_threshold"]:
            logger.warning(f"检测到连续 {consecutive_losses} 次止损，触发自动调整")
            
            # 调整选股评分阈值
            current_min = self.strategy_config["selection_criteria"]["min_score"]
            new_min = min(current_min + self.config["min_score_adjust"], self.config["max_score"])
            
            if new_min != current_min:
                self.strategy_config["selection_criteria"]["min_score"] = new_min
                adjustments.append({
                    "date": date,
                    "type": "min_score",
                    "from": current_min,
                    "to": new_min,
                    "reason": f"连续{consecutive_losses}次止损，提高选股标准"
                })
            
            # 调整止损幅度（如果太紧）
            current_stop = self.strategy_config["trade_settings"]["stop_loss_pct"]
            if current_stop < 2.0:
                new_stop = min(current_stop + 0.5, 3.0)
                self.strategy_config["trade_settings"]["stop_loss_pct"] = new_stop
                adjustments.append({
                    "date": date,
                    "type": "stop_loss_pct",
                    "from": current_stop,
                    "to": new_stop,
                    "reason": "止损过紧，增加缓冲空间"
                })
            
            # 添加优化历史
            if "optimization_history" not in self.strategy_config:
                self.strategy_config["optimization_history"] = []
            
            for adj in adjustments:
                self.strategy_config["optimization_history"].append({
                    "date": adj["date"],
                    "change": f"{adj['type']}: {adj['from']} → {adj['to']}",
                    "reason": adj["reason"],
                    "result": "待验证"
                })
            
            # 保存更新
            self.strategy_config["last_updated"] = date
            self._save_json("strategy_config.json", self.strategy_config)
            
            logger.info(f"策略自动调整完成: {adjustments}")
        
        # 检查成功率，如果连续高于阈值，可以放宽标准
        win_rate = summary.get("buy_success_rate_pct", 0)
        if win_rate >= 60 and len(recent_stats) >= 5:
            current_min = self.strategy_config["selection_criteria"]["min_score"]
            new_min = max(current_min - 2, self.config["min_score"])
            
            if new_min != current_min:
                self.strategy_config["selection_criteria"]["min_score"] = new_min
                adjustments.append({
                    "date": date,
                    "type": "min_score_relax",
                    "from": current_min,
                    "to": new_min,
                    "reason": f"胜率{win_rate}%较高，放宽选股标准"
                })
                
                self.strategy_config["optimization_history"].append({
                    "date": date,
                    "change": f"min_score: {current_min} → {new_min}",
                    "reason": f"胜率{win_rate}%较高，放宽选股以捕捉更多机会",
                    "result": "待验证"
                })
                
                self.strategy_config["last_updated"] = date
                self._save_json("strategy_config.json", self.strategy_config)
        
        return adjustments
    
    def add_lesson_learned(self, date: str, lesson: str, impact: str, action: str) -> None:
        """添加经验教训"""
        if "lessons_learned" not in self.performance_data:
            self.performance_data["lessons_learned"] = []
        
        self.performance_data["lessons_learned"].append({
            "date": date,
            "lesson": lesson,
            "impact": impact,
            "action": action
        })
        
        # 只保留最近20条
        self.performance_data["lessons_learned"] = self.performance_data["lessons_learned"][-20:]
        
        self._save_json("performance_tracking.json", self.performance_data)
        logger.info(f"已添加经验: {lesson}")
    
    def get_strategy_status(self) -> Dict:
        """获取当前策略状态"""
        return {
            "strategy_config": {
                "min_score": self.strategy_config.get("selection_criteria", {}).get("min_score", 65),
                "stop_loss_pct": self.strategy_config.get("trade_settings", {}).get("stop_loss_pct", 1.5),
                "target_gain_pct": self.strategy_config.get("trade_settings", {}).get("target_gain_pct", 1.0),
                "max_positions": self.strategy_config.get("trade_settings", {}).get("max_positions", 3),
                "last_updated": self.strategy_config.get("last_updated", "N/A")
            },
            "performance_summary": self.performance_data.get("summary", {}),
            "optimization_history": self.strategy_config.get("optimization_history", [])[-5:],
            "recent_lessons": self.performance_data.get("lessons_learned", [])[-3:]
        }
    
    def manual_record(self, date: str, code: str, name: str, score: int, 
                      result: str, pnl_pct: float, reason: str = "") -> Dict:
        """
        手动记录单笔交易结果（用于快速输入）
        
        result 选项: stop_loss, sell_achieved, hold_to_close, no_buy
        """
        return self.record_daily_result(date, [{
            "code": code,
            "name": name,
            "score": score,
            "result": result,
            "pnl_pct": pnl_pct,
            "reason": reason
        }])


def main():
    """测试主函数"""
    loop = FeedbackLoop()
    
    # 显示当前状态
    status = loop.get_strategy_status()
    print("=" * 50)
    print("📊 当前策略状态")
    print("=" * 50)
    print(f"选股最低评分: {status['strategy_config']['min_score']}")
    print(f"止损幅度: {status['strategy_config']['stop_loss_pct']}%")
    print(f"目标涨幅: {status['strategy_config']['target_gain_pct']}%")
    print(f"最大持仓: {status['strategy_config']['max_positions']}只")
    print()
    print("📈 表现汇总:")
    summary = status['performance_summary']
    print(f"  总选股次数: {summary.get('total_selections', 0)}")
    print(f"  买入次数: {summary.get('total_buys', 0)}")
    print(f"  卖出成功: {summary.get('total_sells_achieved', 0)}")
    print(f"  止损触发: {summary.get('total_stop_loss', 0)}")
    print(f"  买入成功率: {summary.get('buy_success_rate_pct', 0)}%")
    print(f"  平均盈亏: {summary.get('avg_profit_per_trade_pct', 0)}%")
    print()
    print("📝 最近优化:")
    for opt in status['optimization_history']:
        print(f"  [{opt['date']}] {opt['change']} - {opt['reason']}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())