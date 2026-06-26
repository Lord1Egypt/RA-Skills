#!/usr/bin/env python3
"""
港股日内交易复盘报告生成器
基于交易数据和模板生成格式化复盘报告
"""

import json
import datetime
from typing import Dict, List, Any

class HKIntradayReportGenerator:
    """港股日内交易复盘报告生成器"""
    
    def __init__(self, template_path: str = None):
        """初始化报告生成器"""
        self.template_path = template_path
        self.report_data = {}
        
    def load_data(self, data: Dict[str, Any]) -> None:
        """加载交易数据"""
        self.report_data = data
        
    def calculate_statistics(self) -> Dict[str, Any]:
        """计算交易统计数据"""
        stocks = self.report_data.get('stocks', [])
        
        total_stocks = len(stocks)
        buy_achieved = sum(1 for stock in stocks if stock.get('execution', {}).get('buy_achieved', False))
        sell_achieved = sum(1 for stock in stocks if stock.get('execution', {}).get('sell_achieved', False))
        stop_loss_triggered = sum(1 for stock in stocks if stock.get('execution', {}).get('stop_loss_triggered', False))
        
        buy_rate = (buy_achieved / total_stocks * 100) if total_stocks > 0 else 0
        sell_rate = (sell_achieved / total_stocks * 100) if total_stocks > 0 else 0
        stop_loss_rate = (stop_loss_triggered / total_stocks * 100) if total_stocks > 0 else 0
        sell_success_rate = (sell_achieved / buy_achieved * 100) if buy_achieved > 0 else 0
        
        return {
            'total_stocks': total_stocks,
            'buy_achieved': buy_achieved,
            'sell_achieved': sell_achieved,
            'stop_loss_triggered': stop_loss_triggered,
            'buy_rate': round(buy_rate, 1),
            'sell_rate': round(sell_rate, 1),
            'stop_loss_rate': round(stop_loss_rate, 1),
            'sell_success_rate': round(sell_success_rate, 1)
        }
    
    def generate_report(self) -> str:
        """生成复盘报告"""
        if not self.report_data:
            raise ValueError("未加载交易数据")
            
        date = self.report_data.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
        time = self.report_data.get('time', datetime.datetime.now().strftime('%H:%M:%S'))
        stocks = self.report_data.get('stocks', [])
        stats = self.calculate_statistics()
        
        # 生成报告头部
        report = f"""🍇 {date} 港股交易复盘报告
📅 复盘日期：{date}
⏰ 复盘时间：{time}
📊 今日交易执行情况
────────────────────
"""
        
        # 生成每只股票的执行情况
        for i, stock in enumerate(stocks, 1):
            name = stock.get('name', '')
            code = stock.get('code', '')
            score = stock.get('score', 0)
            buy_target = stock.get('buy_target', 0)
            sell_target = stock.get('sell_target', 0)
            stop_loss = stock.get('stop_loss', 0)
            risk_reward = stock.get('risk_reward_ratio', 0)
            
            market_data = stock.get('market_data', {})
            high = market_data.get('high', 0)
            low = market_data.get('low', 0)
            close = market_data.get('close', 0)
            
            execution = stock.get('execution', {})
            buy_achieved = execution.get('buy_achieved', False)
            buy_reason = execution.get('buy_reason', '')
            sell_achieved = execution.get('sell_achieved', False)
            sell_reason = execution.get('sell_reason', '')
            stop_loss_triggered = execution.get('stop_loss_triggered', False)
            stop_loss_reason = execution.get('stop_loss_reason', '')
            
            # 计算涨跌幅
            buy_to_sell_pct = ((sell_target - buy_target) / buy_target * 100) if buy_target > 0 else 0
            buy_to_stop_loss_pct = ((stop_loss - buy_target) / buy_target * 100) if buy_target > 0 else 0
            
            # 添加股票信息
            report += f"""{i}️⃣ {name} ({code})
├─ 选股评分：{score}/100
├─ 目标买入：{buy_target:.3f}
├─ 目标卖出：{sell_target:.3f} (+{buy_to_sell_pct:.2f}%)
├─ 止损价格：{stop_loss:.3f} ({buy_to_stop_loss_pct:.2f}%)
├─ 风险收益比：{risk_reward:.2f}:1
├─ 今日行情：最高{high}｜最低{low}｜收盘{close}
└─ 执行结果：
├─ 买入：{'✅' if buy_achieved else '❌'} {'达成' if buy_achieved else '未达成'}（{buy_reason}）
├─ 卖出：{'✅' if sell_achieved else '❌'} {'达成' if sell_achieved else '未达成'}（{sell_reason}）
└─ 止损：{'✅' if not stop_loss_triggered else '❌'} {'未触发' if not stop_loss_triggered else '触发'}（{stop_loss_reason}）

"""
        
        # 生成交易统计
        report += f"""📈 交易统计
────────────────────
• 总选股数：{stats['total_stocks']}只
• 买入达成：{stats['buy_achieved']}只（{stats['buy_rate']}%）
• 卖出达成：{stats['sell_achieved']}只（{stats['sell_rate']}%）
• 止损触发：{stats['stop_loss_triggered']}只（{stats['stop_loss_rate']}%）
• 卖出成功率：{stats['sell_success_rate']}%（基于买入股票）

"""
        
        # 生成策略评价（简化版）
        report += """🎯 选股策略深度评价
────────────────────
🔍 策略有效性分析：
[请根据实际交易数据填写策略分析内容]

💡 关键问题诊断
────────────────────
[请根据实际交易数据填写问题诊断内容]

🚀 策略优化建议
────────────────────
[请根据实际交易数据填写优化建议内容]

📋 明日行动计划
────────────────────
数据层面
• 收集今日交易执行数据
• 分析价格区间与成交关系
• 更新股票池评分参数

策略层面
• 优化买入价计算逻辑
• 调整卖出目标设置方法
• 改进选股评分标准

执行层面
• 保持日内交易原则
• 严格执行止损纪律
• 记录每笔交易细节

✅ 复盘结论
────────────────────
今日策略表现：[请填写评价]
• 优点：[请填写优点]
• 缺点：[请填写缺点]
• 重点：[请填写重点]
明日重点：[请填写明日重点]
长期目标：[请填写长期目标]
📁 报告生成时间：{date} {time}
🔗 数据来源：今日选股结果 + 模拟行情数据
"""
        
        return report
    
    def save_report(self, output_path: str) -> None:
        """保存报告到文件"""
        report = self.generate_report()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {output_path}")

def main():
    """主函数示例"""
    # 示例数据
    sample_data = {
        "date": "2026-03-04",
        "time": "17:51:00",
        "stocks": [
            {
                "name": "美团-W",
                "code": "03690.HK",
                "score": 80.0,
                "buy_target": 73.729,
                "sell_target": 75.197,
                "stop_loss": 73.552,
                "risk_reward_ratio": 2.0,
                "market_data": {
                    "high": 74.8,
                    "low": 73.8,
                    "close": 74.1
                },
                "execution": {
                    "buy_achieved": False,
                    "buy_reason": "最低价73.8 > 目标价73.729",
                    "sell_achieved": False,
                    "sell_reason": "最高价74.8 < 目标价75.197",
                    "stop_loss_triggered": False,
                    "stop_loss_reason": "安全边际0.248"
                }
            },
            {
                "name": "小米集团-W",
                "code": "01810.HK",
                "score": 60.5,
                "buy_target": 31.303,
                "sell_target": 31.617,
                "stop_loss": 31.271,
                "risk_reward_ratio": 0.83,
                "market_data": {
                    "high": 31.6,
                    "low": 31.3,
                    "close": 31.46
                },
                "execution": {
                    "buy_achieved": True,
                    "buy_reason": "最低价31.3 ≤ 目标价31.303",
                    "sell_achieved": False,
                    "sell_reason": "最高价31.6 < 目标价31.617",
                    "stop_loss_triggered": False,
                    "stop_loss_reason": "安全边际0.029"
                }
            }
        ]
    }
    
    # 生成报告
    generator = HKIntradayReportGenerator()
    generator.load_data(sample_data)
    report = generator.generate_report()
    
    # 输出报告
    print(report)
    
    # 保存报告
    generator.save_report("港股交易复盘报告_2026-03-04.md")

if __name__ == "__main__":
    main()