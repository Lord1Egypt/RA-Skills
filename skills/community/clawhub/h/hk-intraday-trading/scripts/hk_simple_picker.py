#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股简单选股器 - 核心目标：盘前选出大概率赚钱的日内交易股票
"""
import os
import json
import random
import requests
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HKSimplePicker:
    """港股简单选股器 - 专注选股成功率"""
    
    def __init__(self):
        # 技能根目录
        self.skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 数据目录
        self.data_dir = os.path.join(self.skill_root, "data")
        self.output_dir = os.path.join(self.skill_root, "output/picks")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 加载策略配置
        self.strategy_config = self._load_strategy_config()
        
        # 加载历史表现数据（真实数据）
        self.performance_data = self._load_performance_data()
        
        # 核心港股池（从配置加载）
        self.stock_pool = [s for s in self.strategy_config["selection_criteria"]["stock_pool"] if s["enabled"]]
        
        # 选股策略参数（从配置加载）
        self.strategy_params = {
            "max_picks": self.strategy_config["trade_settings"]["max_positions"],
            "min_success_rate": 0.5,  # 历史成功率阈值
            "min_profit_rate": 0.5,   # 历史盈利概率阈值
            "max_drawdown": 0.05,     # 最大回撤限制
            "confidence_threshold": 0.6,  # 置信度阈值
            "min_score": self.strategy_config["selection_criteria"]["min_score"]
        }
    
    def get_realtime_price(self, stock_code):
        """获取港股实时价格（使用东方财富API）"""
        try:
            # 东方财富港股API
            url = f"https://push2.eastmoney.com/api/qt/stock/get"
            params = {
                "secid": f"116.{stock_code}",
                "fields": "f43,f44,f45,f170,f177"  # 当前价、最高价、最低价、涨跌幅、振幅
            }
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()
            
            if data.get("data"):
                stock_data = data["data"]
                return {
                    "price": stock_data.get("f43", 0) / 1000,  # 单位：港元
                    "high": stock_data.get("f44", 0) / 1000,
                    "low": stock_data.get("f45", 0) / 1000,
                    "change_pct": stock_data.get("f170", 0) / 100,
                    "amplitude": stock_data.get("f177", 0) / 100,
                }
        except Exception as e:
            logger.warning(f"获取股票 {stock_code} 实时价格失败: {e}")
        
        return None
    
    def calculate_trade_prices(self, current_price, score, amplitude_pct=None):
        """计算交易价格（买入价、卖出价、止损价）
        
        规则：
        - 买入价：比当前价低0.5%（给市场调整空间）
        - 卖出价：根据评分和振幅计算目标收益
        - 止损价：根据评分计算止损比例
        """
        if current_price is None or current_price <= 0:
            return None
        
        # 使用振幅计算，如果没有则默认2%
        if amplitude_pct is None or amplitude_pct <= 0:
            amplitude_pct = 2.0
        
        # 根据评分确定目标收益比例和止损比例
        if score >= 80:
            target_gain_pct = amplitude_pct * 0.8  # 目标获取80%振幅
            stop_loss_pct = amplitude_pct * 0.4    # 止损40%振幅
        elif score >= 70:
            target_gain_pct = amplitude_pct * 0.6
            stop_loss_pct = amplitude_pct * 0.5
        elif score >= 60:
            target_gain_pct = amplitude_pct * 0.5
            stop_loss_pct = amplitude_pct * 0.6
        else:
            target_gain_pct = amplitude_pct * 0.4
            stop_loss_pct = amplitude_pct * 0.7
        
        # 计算实际价格
        buy_price = round(current_price * 0.995, 3)   # 比当前价低0.5%买入
        sell_target = round(current_price * (1 + target_gain_pct / 100), 3)
        stop_loss_price = round(current_price * (1 - stop_loss_pct / 100), 3)
        
        # 风险收益比
        risk_reward_ratio = target_gain_pct / stop_loss_pct if stop_loss_pct > 0 else 0
        
        return {
            "current_price": current_price,
            "buy_price": buy_price,
            "sell_target": sell_target,
            "stop_loss": stop_loss_price,
            "target_gain_pct": round(target_gain_pct, 2),
            "stop_loss_pct": round(stop_loss_pct, 2),
            "risk_reward_ratio": round(risk_reward_ratio, 2)
        }
    
    def _load_strategy_config(self):
        """加载策略配置文件"""
        config_file = os.path.join(self.data_dir, "strategy_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning("策略配置文件不存在，使用默认配置")
            return self._get_default_config()
    
    def _load_performance_data(self):
        """加载性能追踪数据"""
        perf_file = os.path.join(self.data_dir, "performance_tracking.json")
        if os.path.exists(perf_file):
            with open(perf_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning("性能追踪文件不存在，使用默认数据")
            return self._get_default_performance()
    
    def _get_default_config(self):
        """获取默认配置"""
        return {
            "version": "1.0",
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "selection_criteria": {
                "min_score": 65,
                "max_rsi": 70,
                "min_rsi": 30,
                "min_volume": 3000000,
                "stock_pool": []
            },
            "trade_settings": {
                "max_positions": 3,
                "buy_discount": 0.005,
                "target_gain_pct": 1.0,
                "stop_loss_pct": 1.5
            }
        }
    
    def _get_default_performance(self):
        """获取默认性能数据"""
        return {
            "version": "1.0",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {},
            "daily_stats": [],
            "stock_performance": {}
        }
    
    def get_stock_history(self, stock_code):
        """获取股票历史表现数据"""
        return self.performance_data.get("stock_performance", {}).get(stock_code, {
            "total_picks": 0,
            "total_buys": 0,
            "successful_sells": 0,
            "stop_losses": 0,
            "win_rate": 0,
            "avg_pnl_pct": 0,
            "max_loss_pct": 0,
            "profit_rate": 0,
            "total_trades": 0,
            "consecutive_wins": 0,
            "consecutive_losses": 0
        })
    
    def _get_history_data(self):
        """获取用于选股的历史数据字典"""
        # 从 performance_tracking 构建历史数据字典
        history = {}
        stock_perf = self.performance_data.get("stock_performance", {})
        for code, data in stock_perf.items():
            history[code] = {
                "win_rate": data.get("win_rate", 0),
                "profit_rate": data.get("profit_rate", 0),
                "avg_profit_pct": data.get("avg_pnl_pct", 0) / 100,  # 转换为小数
                "max_loss_pct": data.get("avg_pnl_pct", 0) / 100 * -1,  # 估算
                "total_trades": data.get("total_picks", 0),
                "consecutive_wins": 0,
                "consecutive_losses": 0
            }
        return history
    
    def calculate_stock_score(self, stock_code):
        """计算股票选股评分（核心函数）"""
        history_data = self._get_history_data()
        
        # 没有历史记录的股票，给基础分60分（让新股有机会尝试）
        if stock_code not in history_data:
            return 60
        
        # 历史记录太少（<3次），给基础分加分
        data = history_data[stock_code]
        total_trades = data.get("total_trades", 0)
        if total_trades < 3:
            return 60 + (total_trades * 5)  # 1次=65, 2次=70, 3次+=正常计算
        
        # 基础评分（0-100分）
        score = 0
        
        # 1. 历史成功率权重最高（40分）
        win_rate = data.get("win_rate", 0)
        score += win_rate * 40
        
        # 2. 历史盈利概率（30分）
        profit_rate = data.get("profit_rate", 0)
        score += profit_rate * 30
        
        # 3. 平均盈利幅度（15分）
        avg_profit = data.get("avg_profit_pct", 0)
        if avg_profit > 0.02:
            score += 15
        elif avg_profit > 0.01:
            score += 10
        elif avg_profit > 0:
            score += 5
        
        # 4. 最大回撤控制（10分）
        max_loss = abs(data.get("max_loss_pct", 0))
        if max_loss < 0.02:
            score += 10
        elif max_loss < 0.03:
            score += 7
        elif max_loss < 0.04:
            score += 4
        
        # 5. 交易次数（5分）
        total_trades = data.get("total_trades", 0)
        if total_trades > 30:
            score += 5
        elif total_trades > 20:
            score += 3
        elif total_trades > 10:
            score += 1
        
        return min(100, max(0, score))
    
    def filter_stocks_by_strategy(self):
        """根据策略筛选股票"""
        qualified_stocks = []
        history_data = self._get_history_data()
        
        for stock in self.stock_pool:
            code = stock["code"]
            data = history_data.get(code, {})
            total_trades = data.get("total_trades", 0)
            
            # 新股（历史记录<3次）或历史表现还可以的，通过筛选
            is_new_stock = total_trades < 3
            
            if is_new_stock:
                # 新股：直接通过，用评分决定
                stock_score = self.calculate_stock_score(code)
                confidence = 0.6  # 新股默认置信度
            else:
                # 老股：检查策略条件
                conditions = [
                    data.get("win_rate", 0) >= self.strategy_params["min_success_rate"],
                    data.get("profit_rate", 0) >= self.strategy_params["min_profit_rate"],
                    abs(data.get("max_loss_pct", 0)) <= self.strategy_params["max_drawdown"],
                ]
                
                if not all(conditions):
                    continue
                
                stock_score = self.calculate_stock_score(code)
                confidence = self.calculate_confidence(stock_score, data)
            
            # 评分低于最低要求的跳过
            if stock_score < self.strategy_params["min_score"]:
                continue
            
            if is_new_stock or confidence >= self.strategy_params["confidence_threshold"]:
                qualified_stocks.append({
                    **stock,
                    "score": stock_score,
                    "confidence": confidence,
                    "is_new": is_new_stock,
                    "win_rate": data.get("win_rate", 0),
                    "profit_rate": data.get("profit_rate", 0),
                    "avg_profit_pct": data.get("avg_profit_pct", 0),
                        "total_trades": data.get("total_trades", 0),
                    })
        
        # 按评分排序
        qualified_stocks.sort(key=lambda x: x["score"], reverse=True)
        
        # 限制数量
        max_picks = self.strategy_params["max_picks"]
        return qualified_stocks[:max_picks]
    
    def calculate_confidence(self, score, data):
        """计算选股置信度"""
        confidence = score / 100.0  # 基础置信度
        
        # 交易次数越多，置信度越高
        total_trades = data.get("total_trades", 0)
        if total_trades > 40:
            confidence *= 1.2
        elif total_trades > 20:
            confidence *= 1.1
        elif total_trades < 5:
            confidence *= 0.7
        
        # 连续盈利/亏损调整
        consecutive_wins = data.get("consecutive_wins", 0)
        consecutive_losses = data.get("consecutive_losses", 0)
        
        if consecutive_wins >= 3:
            confidence *= 0.9  # 连续盈利后可能回调
        elif consecutive_losses >= 3:
            confidence *= 1.1  # 连续亏损后可能反弹
        
        return min(1.0, max(0.0, confidence))
    
    def generate_trading_suggestions(self, selected_stocks):
        """生成交易建议（包含交易价格）"""
        suggestions = []
        
        for stock in selected_stocks:
            code = stock["code"]
            name = stock["name"]
            score = stock["score"]
            confidence = stock["confidence"]
            win_rate = stock["win_rate"]
            
            # 获取实时价格
            market_data = self.get_realtime_price(code)
            
            # 计算交易价格
            trade_prices = None
            if market_data and market_data.get("price"):
                trade_prices = self.calculate_trade_prices(
                    market_data["price"],
                    score,
                    market_data.get("amplitude")
                )
            
            # 基于历史表现生成交易建议
            suggestion = {
                "stock_code": code,
                "stock_name": name,
                "recommendation": "BUY" if score >= 70 else "CONSIDER" if score >= 60 else "WATCH",
                "action": self._get_action(score, confidence),
                "score": round(score, 1),
                "confidence": round(confidence, 2),
                "win_rate": round(win_rate, 3),
                "expected_profit_pct": self._estimate_profit_pct(stock),
                "risk_level": self._assess_risk_level(stock),
                "position_size": self._calculate_position_size(score, confidence),
                "holding_period": "日内",  # 核心是日内交易
                "key_reason": self._get_key_reason(stock),
                # 添加交易价格（供复盘使用）
                "market_data": market_data,
                "trade_prices": trade_prices,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _get_action(self, score, confidence):
        """根据评分和置信度确定行动"""
        if score >= 80 and confidence >= 0.8:
            return "积极买入"
        elif score >= 70 and confidence >= 0.7:
            return "推荐买入"
        elif score >= 60 and confidence >= 0.6:
            return "考虑买入"
        else:
            return "观察"
    
    def _estimate_profit_pct(self, stock):
        """估计盈利幅度"""
        avg_profit = stock.get("avg_profit_pct", 0.02)
        win_rate = stock.get("win_rate", 0.6)
        
        # 简单估算：平均盈利 × 成功率
        return round(avg_profit * win_rate * 100, 2)
    
    def _assess_risk_level(self, stock):
        """评估风险等级"""
        history_data = self._get_history_data()
        stock_data = history_data.get(stock["code"], {})
        max_loss = abs(stock_data.get("max_loss_pct", 0))
        win_rate = stock.get("win_rate", 0)
        
        if win_rate >= 0.7 and max_loss <= 0.02:
            return "低风险"
        elif win_rate >= 0.6 and max_loss <= 0.03:
            return "中风险"
        elif win_rate >= 0.5 and max_loss <= 0.04:
            return "较高风险"
        else:
            return "高风险"
    
    def _calculate_position_size(self, score, confidence):
        """计算仓位大小"""
        # 基于评分和置信度决定仓位
        if score >= 80 and confidence >= 0.8:
            return "30-40%"  # 重仓
        elif score >= 70 and confidence >= 0.7:
            return "20-30%"  # 中等仓位
        elif score >= 60 and confidence >= 0.6:
            return "10-20%"  # 轻仓
        else:
            return "5-10%"   # 试探仓位
    
    def _get_key_reason(self, stock):
        """获取关键理由"""
        reasons = []
        
        if stock.get("win_rate", 0) >= 0.7:
            reasons.append(f"历史成功率{stock['win_rate']*100:.0f}%")
        if stock.get("profit_rate", 0) >= 0.7:
            reasons.append(f"盈利概率{stock['profit_rate']*100:.0f}%")
        if stock.get("avg_profit_pct", 0) >= 0.03:
            reasons.append(f"平均盈利{stock['avg_profit_pct']*100:.1f}%")
        if stock.get("total_trades", 0) > 20:
            reasons.append(f"历史交易{stock['total_trades']}次")
        
        if not reasons:
            reasons.append("符合策略基本条件")
        
        return "，".join(reasons)
    
    def run_daily_selection(self):
        """运行每日选股"""
        logger.info("=" * 50)
        logger.info("港股盘前选股开始")
        logger.info(f"选股时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 50)
        
        # 筛选股票
        selected_stocks = self.filter_stocks_by_strategy()
        
        if not selected_stocks:
            logger.warning("今日无符合条件的股票")
            self._generate_no_pick_report()
            return None
        
        # 生成交易建议
        suggestions = self.generate_trading_suggestions(selected_stocks)
        
        # 保存结果
        self.save_results(suggestions)
        
        logger.info(f"选股完成，选出 {len(suggestions)} 只股票")
        for sugg in suggestions:
            logger.info(f"  {sugg['stock_name']} ({sugg['stock_code']}) - 评分: {sugg['score']} - 建议: {sugg['action']}")
        
        logger.info("=" * 50)
        return suggestions
    
    def save_results(self, suggestions):
        """保存选股结果"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # JSON格式保存
        json_file = os.path.join(self.output_dir, f"picks_{date_str}.json")
        result_data = {
            "date": date_str,
            "generated_at": datetime.now().isoformat(),
            "strategy_version": "simple_v1",
            "total_picks": len(suggestions),
            "avg_score": sum(s["score"] for s in suggestions) / len(suggestions) if suggestions else 0,
            "avg_confidence": sum(s["confidence"] for s in suggestions) / len(suggestions) if suggestions else 0,
            "suggestions": suggestions,
            "strategy_params": self.strategy_params
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        # Markdown格式报告
        md_file = os.path.join(self.output_dir, f"picks_report_{date_str}.md")
        self._generate_markdown_report(md_file, result_data)
        
        logger.info(f"选股结果已保存到: {json_file}")
        logger.info(f"选股报告已保存到: {md_file}")
    
    def _generate_markdown_report(self, filepath, data):
        """生成Markdown格式报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 🍇 港股盘前选股报告\n\n")
            f.write(f"📅 选股日期: {data['date']}\n")
            f.write(f"⏰ 生成时间: {datetime.now().strftime('%H:%M:%S')}\n\n")
            
            f.write("## 🎯 今日选股结果\n\n")
            
            if not data['suggestions']:
                f.write("**今日无符合条件的股票**\n\n")
                f.write("### 可能原因\n")
                f.write("1. 市场条件不满足策略要求\n")
                f.write("2. 历史表现数据不足\n")
                f.write("3. 策略参数设置较严格\n")
                f.write("4. 建议等待更好的机会\n")
            else:
                f.write(f"**共选出 {data['total_picks']} 只股票**\n")
                f.write(f"- 平均评分: {data['avg_score']:.1f}/100\n")
                f.write(f"- 平均置信度: {data['avg_confidence']:.2f}\n\n")
                
                f.write("## 📈 详细选股建议\n\n")
                
                for i, sugg in enumerate(data['suggestions'], 1):
                    f.write(f"### {i}. {sugg['stock_name']} ({sugg['stock_code']})\n\n")
                    
                    # 核心信息表
                    f.write("| 指标 | 数值 | 说明 |\n")
                    f.write("|------|------|------|\n")
                    f.write(f"| **推荐操作** | **{sugg['action']}** | {sugg['recommendation']} |\n")
                    f.write(f"| 综合评分 | {sugg['score']}/100 | 选股策略评分 |\n")
                    f.write(f"| 置信度 | {sugg['confidence']:.2f} | 选股可靠程度 |\n")
                    f.write(f"| 历史成功率 | {sugg['win_rate']:.1%} | 过去交易成功率 |\n")
                    f.write(f"| 预期盈利 | {sugg['expected_profit_pct']}% | 日内预期收益率 |\n")
                    f.write(f"| 风险等级 | {sugg['risk_level']} | 交易风险评估 |\n")
                    f.write(f"| 建议仓位 | {sugg['position_size']} | 资金分配比例 |\n")
                    f.write(f"| 持有周期 | {sugg['holding_period']} | 建议持仓时间 |\n")
                    f.write(f"| 关键理由 | {sugg['key_reason']} | 选股主要依据 |\n\n")
                    
                    # 交易建议
                    f.write("**具体操作建议:**\n")
                    if sugg['action'] == "积极买入":
                        f.write("- 🟢 开盘后择机买入\n")
                        f.write("- 🎯 设置止损止盈\n")
                        f.write("- 📊 重点关注成交量\n")
                    elif sugg['action'] == "推荐买入":
                        f.write("- 🟡 可考虑分批买入\n")
                        f.write("- ⚠️ 注意风险控制\n")
                        f.write("- 🔍 观察开盘走势\n")
                    elif sugg['action'] == "考虑买入":
                        f.write("- 🟠 谨慎观察后再决定\n")
                        f.write("- 📈 等待更明确信号\n")
                        f.write("- 💰 轻仓试探\n")
                    else:
                        f.write("- ⚪ 加入观察列表\n")
                        f.write("- 👀 等待更好机会\n")
                        f.write("- 📝 记录市场表现\n")
                    
                    f.write("\n---\n\n")
            
            f.write("## ⚙️ 选股策略参数\n\n")
            for key, value in data['strategy_params'].items():
                if isinstance(value, float):
                    f.write(f"- **{key}**: {value:.2f}\n")
                else:
                    f.write(f"- **{key}**: {value}\n")
            
            f.write("\n## 📊 策略说明\n\n")
            f.write("**核心目标**: 盘前选出大概率赚钱的日内交易股票\n")
            f.write("**选股逻辑**: 基于历史成功率、盈利概率、风险控制\n")
            f.write("**优化方向**: 通过每日复盘持续改进选股策略\n")
            f.write("**风险提示**: 股市有风险，投资需谨慎\n")
            
            f.write("\n---\n")
            f.write(f"📁 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("🎯 核心目标: 提高选股成功率，实现稳定盈利\n")
            f.write("⚠️ 免责声明: 本报告仅供参考，不构成投资建议\n")
    
    def _generate_no_pick_report(self):
        """生成无选股报告"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        report_file = os.path.join(self.output_dir, f"no_pick_report_{date_str}.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 🍇 港股盘前选股报告\n\n")
            f.write(f"📅 报告日期: {date_str}\n")
            f.write(f"⏰ 生成时间: {datetime.now().strftime('%H:%M:%S')}\n\n")
            
            f.write("## 🎯 今日选股结果\n\n")
            f.write("**今日无符合条件的股票**\n\n")
            
            f.write("## 💡 策略说明\n\n")
            f.write("这是策略严谨性的体现，不是失败。\n\n")
            
            f.write("### 为什么无选股是好事？\n")
            f.write("1. **规避风险**: 避免了勉强交易带来的亏损\n")
            f.write("2. **保存实力**: 在市场不明朗时保留资金\n")
            f.write("3. **等待机会**: 为更好的交易机会做准备\n")
            f.write("4. **策略纪律**: 严格执行选股标准\n\n")
            
            f.write("### 今日建议\n")
            f.write("1. **观察市场**: 关注大盘和个股走势\n")
            f.write("2. **学习复盘**: 分析今日市场特点\n")
            f.write("3. **准备明天**: 为下一个交易日做准备\n")
            f.write("4. **保持耐心**: 交易中耐心比机会更重要\n\n")
            
            f.write("---\n")
            f.write(f"📁 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("🎯 记住: 不交易有时是最好的交易\n")

def main():
    """主函数"""
    picker = HKSimplePicker()
    
    try:
        suggestions = picker.run_daily_selection()
        
        if suggestions:
            print(f"\n✅ 选股完成！共选出 {len(suggestions)} 只股票")
            print("请查看 output/picks 目录下的报告文件")
        else:
            print("\n⚠️  今日无符合条件的股票")
            print("这是策略严谨性的体现，请查看无选股报告")
        
    except Exception as e:
        logger.error(f"选股过程中出错: {str(e)}", exc_info=True)
        print(f"❌ 选股失败: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())