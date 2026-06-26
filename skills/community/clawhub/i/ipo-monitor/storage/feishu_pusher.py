#!/usr/bin/env python3
"""
飞书推送模块
"""
import requests
import logging
from datetime import datetime
from typing import Dict, List


class FeishuPusher:
    """飞书推送"""
    
    def __init__(self, config):
        self.config = config
        self.webhook = config.feishu_webhook
        self.mention_ids = config.feishu_mention_ids
        self.logger = logging.getLogger(__name__)
    
    def send_daily_report(self, changes: Dict):
        """发送日报"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        # 构建消息
        message = self._build_message(changes, date)
        
        self._send(message)
    
    def _build_message(self, changes: Dict, date: str) -> str:
        """构建消息内容"""
        lines = []
        lines.append(f"📈 IPO监控日报 ({date})")
        lines.append("")
        
        # 按板块分组
        added_by_exchange = {}
        updated_by_exchange = {}
        
        for item in changes.get('added', []):
            ex = item['exchange']
            added_by_exchange.setdefault(ex, []).append(item['data'])
        
        for item in changes.get('updated', []):
            ex = item['exchange']
            updated_by_exchange.setdefault(ex, []).append(item['data'])
        
        # 输出新增
        if added_by_exchange:
            for exchange, items in added_by_exchange.items():
                lines.append(f"【{exchange}】新增 {len(items)} 家")
                for i, item in enumerate(items, 1):
                    lines.append(self._format_ipo_item(i, item, is_new=True))
                lines.append("")
        
        # 输出更新
        if updated_by_exchange:
            for exchange, items in updated_by_exchange.items():
                lines.append(f"【{exchange}】更新 {len(items)} 家")
                for item in items:
                    lines.append(self._format_ipo_updated(item))
                lines.append("")
        
        # 汇总
        summary = changes.get('summary', {})
        total_added = sum(s.get('added', 0) for s in summary.values())
        total_updated = sum(s.get('updated', 0) for s in summary.values())
        
        lines.append(f"📊 共计：新增 {total_added} 家 | 更新 {total_updated} 家")
        
        # @相关人员
        if self.mention_ids:
            lines.append("")
            lines.append("<at id=all>")
        
        return "\n".join(lines)
    
    def _format_ipo_item(self, index: int, item: Dict, is_new: bool = True) -> str:
        """格式化IPO条目"""
        name = item.get('company_name', '')
        code = item.get('stock_code', '')
        status = item.get('application_status', '')
        url = item.get('source_url', '')
        
        # 截断过长的名称
        if len(name) > 20:
            name = name[:18] + '...'
        
        # 格式化募集金额和发行价
        details = []
        if item.get('fundraising_amount'):
            details.append(f"募集{item.get('fundraising_amount')}")
        if item.get('issue_price_range'):
            details.append(f"发行价{item.get('issue_price_range')}")
        
        detail_str = f" - {', '.join(details)}" if details else ""
        
        # 构建输出
        if url:
            return f"  {index}. {name} ({code}) - {status}{detail_str}\n     [查看原文]({url})"
        else:
            return f"  {index}. {name} ({code}) - {status}{detail_str}"
    
    def _format_ipo_updated(self, item: Dict) -> str:
        """格式化更新条目"""
        name = item.get('company_name', '')
        code = item.get('stock_code', '')
        old_status = item.get('old_status', '')
        new_status = item.get('application_status', '')
        url = item.get('source_url', '')
        
        if len(name) > 20:
            name = name[:18] + '...'
        
        if url:
            return f"  • {name} ({code})\n    {old_status} → {new_status}\n    [查看原文]({url})"
        else:
            return f"  • {name} ({code})\n    {old_status} → {new_status}"
    
    def _send(self, message: str):
        """发送飞书消息"""
        if not self.webhook or self.webhook == "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_HERE":
            self.logger.warning("飞书Webhook未配置，跳过推送")
            print("=" * 50)
            print("飞书消息内容:")
            print(message)
            print("=" * 50)
            return
        
        url = self.webhook
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            result = response.json()
            
            if result.get('code') == 0:
                self.logger.info("飞书消息发送成功")
            else:
                self.logger.error(f"飞书消息发送失败: {result}")
        except Exception as e:
            self.logger.error(f"飞书消息发送异常: {e}")


# 导出
__all__ = ['FeishuPusher']
