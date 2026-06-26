#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw会话通知器
直接在OpenClaw会话中发送新股通知
"""

import logging
import sys
import os
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OpenClawNotifier:
    """OpenClaw会话通知器"""
    
    def __init__(self):
        """初始化通知器"""
        self.notification_history = []
    
    def send_daily_reminder(self, stocks: List[Dict]) -> str:
        """
        发送每日新股提醒
        
        Args:
            stocks: 今日新股列表
            
        Returns:
            格式化后的消息内容
        """
        if not stocks:
            return "📭 今日无新股可申购，好好休息吧！😴"
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        message = f"""⏰ **新股申购提醒** {current_time}

今日共有 **{len(stocks)}** 只新股可申购：

"""
        
        for i, stock in enumerate(stocks[:5], 1):  # 最多显示5只
            name = stock.get('name', '未知')
            code = stock.get('code', '未知')
            apply_code = stock.get('apply_code', '未知')
            issue_price = stock.get('issue_price', '待定')
            apply_upper = stock.get('online_apply_upper', '未知')
            
            message += f"{i}. **{name}** ({code})\n"
            message += f"   - 申购代码: `{apply_code}`\n"
            message += f"   - 发行价格: **{issue_price}元**\n"
            message += f"   - 申购上限: {apply_upper}股\n"
            
            market = stock.get('market', '')
            if market:
                message += f"   - 上市板块: {market}\n"
            
            message += "\n"
        
        if len(stocks) > 5:
            message += f"还有 {len(stocks) - 5} 只新股未显示...\n\n"
        
        message += "💡 **温馨提示**\n"
        message += "1. 请在交易时间内申购\n"
        message += "2. 确保有对应市场的市值\n"
        message += "3. 中签后及时缴款\n"
        message += "4. 新股有破发风险，申购需谨慎\n\n"
        
        message += "📈 详细分析报告将在稍后推送..."
        
        # 记录通知历史
        self._record_notification('daily_reminder', len(stocks))
        
        return message
    
    def send_stock_report(self, analyses: List[Dict], summary: Dict) -> str:
        """
        发送新股分析报告
        
        Args:
            analyses: 个股分析列表
            summary: 汇总报告
            
        Returns:
            格式化后的报告内容
        """
        if not analyses:
            return "📊 **今日新股报告**\n\n今日无新股可申购，好好休息吧！😴"
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        message = f"""📊 **新股分析报告** {current_time}

### 📈 今日概览
{summary.get('summary', '')}

### 🎯 重点新股推荐
"""
        
        # 显示前3只推荐度最高的新股
        top_stocks = analyses[:3]
        
        for i, analysis in enumerate(top_stocks, 1):
            stock_info = analysis['stock_info']
            key_metrics = analysis['key_metrics']
            valuation = analysis['valuation_analysis']
            advice = analysis['subscription_advice']
            risk = analysis['risk_assessment']
            
            # 股票基本信息
            message += f"\n#### {i}. **{stock_info['name']}** ({stock_info['code']})\n"
            
            # 关键指标
            message += "**关键指标**\n"
            message += f"- 申购代码: `{key_metrics['申购代码']}`\n"
            message += f"- 发行价格: **{key_metrics['发行价格']}**\n"
            message += f"- 申购上限: {key_metrics['申购上限']}\n"
            message += f"- 顶格申购: {key_metrics['顶格申购市值']}\n"
            
            # 估值分析
            if valuation['pe_ratio']:
                pe_status = {
                    '低估': '🟢',
                    '合理': '🟡',
                    '略高': '🟠',
                    '偏高': '🔴',
                    '未知': '⚪',
                }
                status_icon = pe_status.get(valuation['valuation_status'], '⚪')
                message += f"- 估值状态: {status_icon} {valuation['valuation_status']} (PE比率: {valuation['pe_ratio']})\n"
            
            # 申购建议
            advice_icons = {
                '积极申购': '✅✅',
                '建议申购': '✅',
                '谨慎申购': '⚠️',
                '观望': '⏸️',
            }
            advice_icon = advice_icons.get(advice['action'], '❓')
            message += f"- 申购建议: {advice_icon} **{advice['action']}** (信心度: {advice['confidence']})\n"
            
            # 风险提示
            if risk['risk_factors']:
                risk_icons = {'低': '🟢', '中': '🟡', '高': '🔴'}
                risk_icon = risk_icons.get(risk['risk_level'], '⚪')
                message += f"- 风险等级: {risk_icon} {risk['risk_level']}\n"
                if len(risk['risk_factors']) <= 3:
                    for factor in risk['risk_factors']:
                        message += f"  - ⚠️ {factor}\n"
            
            # 简要理由
            if advice['reasons']:
                message += "- **主要理由**: " + "，".join(advice['reasons'][:3]) + "\n"
        
        # 完整列表
        if len(analyses) > 3:
            message += f"\n### 📋 完整列表 ({len(analyses)}只)\n"
            message += "| 股票 | 代码 | 价格 | 建议 | 风险 |\n"
            message += "|------|------|------|------|------|\n"
            
            for analysis in analyses:
                stock_info = analysis['stock_info']
                key_metrics = analysis['key_metrics']
                advice = analysis['subscription_advice']
                risk = analysis['risk_assessment']
                
                # 简化显示
                price_display = key_metrics['发行价格'].replace('元', '')
                advice_display = advice['action'][:2]  # 只显示前2个字
                risk_display = risk['risk_level']
                
                message += f"| {stock_info['name']} | {stock_info['code']} | {price_display} | {advice_display} | {risk_display} |\n"
        
        # 风险提示
        message += """

### ⚠️ 风险提示
1. **数据仅供参考**，不构成投资建议
2. **新股有破发风险**，历史表现不代表未来
3. **申购需对应市值**，请确认账户条件
4. **市场有风险**，投资需谨慎

### 📞 反馈与支持
如有问题或建议，请直接在会话中反馈。

---
*报告生成时间: {current_time}*
*数据来源: 东方财富、同花顺*
*通知方式: OpenClaw会话*
""".format(current_time=current_time)
        
        # 记录通知历史
        self._record_notification('stock_report', len(analyses))
        
        return message
    
    def send_weekly_report(self, stocks_by_date: Dict) -> str:
        """
        发送每周新股日历
        
        Args:
            stocks_by_date: 按日期分组的新股数据
            
        Returns:
            格式化后的周报内容
        """
        if not stocks_by_date:
            return "📅 **本周新股日历**\n\n本周无新股可申购，可以关注其他投资机会。"
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        total_stocks = sum(len(stocks) for stocks in stocks_by_date.values())
        
        message = f"""📅 **本周新股日历** {current_time}

本周共有 **{total_stocks}** 只新股可申购：

"""
        
        for date in sorted(stocks_by_date.keys()):
            date_stocks = stocks_by_date[date]
            weekday = self._get_weekday(date)
            
            message += f"\n### {date} ({weekday})\n"
            message += f"共 {len(date_stocks)} 只新股\n\n"
            
            for stock in date_stocks[:3]:  # 每日期最多显示3只
                name = stock.get('name', '未知')
                code = stock.get('code', '未知')
                apply_code = stock.get('apply_code', '未知')
                issue_price = stock.get('issue_price', '待定')
                
                message += f"- **{name}** ({code})\n"
                message += f"  - 申购代码: `{apply_code}`\n"
                message += f"  - 发行价格: {issue_price}元\n"
            
            if len(date_stocks) > 3:
                message += f"  - 还有 {len(date_stocks) - 3} 只...\n"
            
            message += "\n"
        
        message += "💡 **温馨提示**\n"
        message += "1. 请提前规划申购资金\n"
        message += "2. 注意各新股的申购日期\n"
        message += "3. 确保有对应市场的市值\n\n"
        
        message += "📈 每日详细分析将在当天早上推送..."
        
        # 记录通知历史
        self._record_notification('weekly_report', total_stocks)
        
        return message
    
    def send_error_notification(self, error: str) -> str:
        """
        发送错误通知
        
        Args:
            error: 错误信息
            
        Returns:
            错误通知内容
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        message = f"""❌ **新股分析工具错误通知** {current_time}

### 错误详情
{error[:200]}

### 处理建议
1. 检查网络连接
2. 检查数据源可用性
3. 查看详细日志: `data/logs/app.log`

### 技术支持
请直接在会话中反馈此问题。

---
*错误时间: {current_time}*
"""
        
        # 记录错误
        self._record_notification('error', 0, error=error)
        
        return message
    
    def _get_weekday(self, date_str: str) -> str:
        """获取星期几"""
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            return weekdays[date_obj.weekday()]
        except:
            return ''
    
    def _record_notification(self, notification_type: str, stocks_count: int, error: str = None):
        """记录通知历史"""
        notification = {
            'type': notification_type,
            'time': datetime.now().isoformat(),
            'stocks_count': stocks_count,
            'error': error,
        }
        
        self.notification_history.append(notification)
        
        # 只保留最近100条记录
        if len(self.notification_history) > 100:
            self.notification_history = self.notification_history[-100:]
    
    def get_notification_stats(self) -> Dict:
        """获取通知统计"""
        if not self.notification_history:
            return {'total': 0, 'types': {}}
        
        stats = {'total': len(self.notification_history), 'types': {}}
        
        for notification in self.notification_history:
            ntype = notification['type']
            if ntype not in stats['types']:
                stats['types'][ntype] = 0
            stats['types'][ntype] += 1
        
        return stats


# 全局实例
notifier = OpenClawNotifier()


if __name__ == "__main__":
    # 测试代码
    print("测试OpenClaw通知器...")
    
    # 测试数据
    test_stocks = [
        {
            'code': '301682',
            'name': '测试股票1',
            'apply_code': '301682',
            'issue_price': 69.66,
            'online_apply_upper': 8500,
            'market': '深交所创业板',
        },
        {
            'code': '688781',
            'name': '测试股票2',
            'apply_code': '787781',
            'issue_price': 22.68,
            'online_apply_upper': 14000,
            'market': '上交所科创板',
        }
    ]
    
    # 测试每日提醒
    print("\n1. 每日提醒测试:")
    reminder = notifier.send_daily_reminder(test_stocks)
    print(reminder[:200] + "...")
    
    # 测试错误通知
    print("\n2. 错误通知测试:")
    error_msg = notifier.send_error_notification("测试错误信息：数据获取失败")
    print(error_msg[:200] + "...")
    
    print("\n测试完成！")