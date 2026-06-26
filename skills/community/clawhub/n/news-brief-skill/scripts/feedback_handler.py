#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedback Handler Module
反馈处理模块：处理用户反馈，执行优化操作
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

class FeedbackHandler:
    """反馈处理器"""
    
    def __init__(self, user_id: str, user_config: Dict[str, Any] = None):
        self.user_id = user_id
        self.user_config = user_config or {}
        self.project_root = Path(__file__).parent.parent
        
        # 反馈关键词映射
        self.feedback_keywords = {
            'content': ['内容', '关键词', '摘要', '详细', '简略'],
            'format': ['格式', '排版', '条数', '样式', '布局'],
            'channel': ['渠道', '推送', '时间', '频率', '微信', '邮件', '钉钉']
        }
        
        # 优化选项映射
        self.optimization_options = {
            '1': 'content',
            '2': 'format', 
            '3': 'channel',
            '0': 'none'
        }
    
    def trigger_feedback_prompt(self):
        """触发反馈询问"""
        feedback_prompt = """
📰 新闻简报已送达！

需要查看某条新闻详细信息请回复对应序号；
需要优化内容（关键词、摘要详略）请回复1；
需要优化格式（排版、条数）请回复2； 
需要调整推送渠道/时间请回复3；
无需调整请回复0

💡 也可随时发送"反馈"或"优化"触发此流程。
"""
        print(feedback_prompt)
    
    def process_feedback(self, feedback_text: str) -> Dict[str, Any]:
        """
        处理用户反馈
        
        Args:
            feedback_text: 用户反馈文本
            
        Returns:
            处理结果字典
        """
        try:
            feedback_text = feedback_text.strip().lower()
            
            # 检查是否为数字选项
            if feedback_text in self.optimization_options:
                opt_type = self.optimization_options[feedback_text]
                if opt_type == 'none':
                    return {'action': 'no_action', 'message': '保持当前配置'}
                else:
                    return self._handle_optimization_request(opt_type)
            
            # 检查是否为序号（查看详情）
            if feedback_text.isdigit():
                news_index = int(feedback_text)
                return self._handle_detail_request(news_index)
            
            # 检查关键词触发
            if any(keyword in feedback_text for keyword in ['反馈', '优化', 'adjust', 'optimize']):
                return self.trigger_feedback_prompt_result()
            
            # 分析反馈内容类型
            feedback_type = self._analyze_feedback_type(feedback_text)
            if feedback_type:
                return self._handle_optimization_request(feedback_type)
            
            # 默认处理
            return {
                'action': 'unknown',
                'message': '未识别的反馈内容，请使用数字选项或明确说明优化需求'
            }
            
        except Exception as e:
            return {
                'action': 'error',
                'message': f'处理反馈时出错: {str(e)}'
            }
    
    def _analyze_feedback_type(self, feedback_text: str) -> Optional[str]:
        """分析反馈类型"""
        feedback_text = feedback_text.lower()
        
        # 内容优化关键词
        for keyword in self.feedback_keywords['content']:
            if keyword in feedback_text:
                return 'content'
        
        # 格式优化关键词  
        for keyword in self.feedback_keywords['format']:
            if keyword in feedback_text:
                return 'format'
        
        # 渠道优化关键词
        for keyword in self.feedback_keywords['channel']:
            if keyword in feedback_text:
                return 'channel'
        
        return None
    
    def _handle_optimization_request(self, opt_type: str) -> Dict[str, Any]:
        """处理优化请求"""
        if opt_type == 'content':
            return self._handle_content_optimization()
        elif opt_type == 'format':
            return self._handle_format_optimization()
        elif opt_type == 'channel':
            return self._handle_channel_optimization()
        else:
            return {'action': 'error', 'message': '未知的优化类型'}
    
    def _handle_content_optimization(self) -> Dict[str, Any]:
        """处理内容优化请求"""
        current_keywords = self.user_config.get('interest_keywords', [])
        current_summary_style = self.user_config.get('summary_style', 'standard')
        
        optimization_guide = f"""
🔧 内容优化选项：

当前兴趣关键词: {', '.join(current_keywords) if current_keywords else '未设置'}

【关键词管理】
• 添加关键词: 回复 "添加 [关键词]"
• 删除关键词: 回复 "删除 [关键词]"  
• 清空关键词: 回复 "清空关键词"

【摘要详略】
当前模式: {current_summary_style}
• 简洁模式(50字): 回复 "简洁"
• 标准模式(65字): 回复 "标准" 
• 详细模式(80字): 回复 "详细"

回复 "取消" 返回主菜单
"""
        return {
            'action': 'content_optimization',
            'message': optimization_guide,
            'current_config': {
                'keywords': current_keywords,
                'summary_style': current_summary_style
            }
        }
    
    def _handle_format_optimization(self) -> Dict[str, Any]:
        """处理格式优化请求"""
        current_max_items = self.user_config.get('max_items', 5)
        current_show_credibility = self.user_config.get('show_credibility', True)
        current_summary_style = self.user_config.get('summary_style', 'standard')
        
        optimization_guide = f"""
🎨 格式优化选项：

当前设置:
• 推送条数: {current_max_items}条
• 显示可信度: {'是' if current_show_credibility else '否'}
• 摘要模式: {current_summary_style}

【条数调整】
回复数字 3-10 来设置推送条数

【可信度显示】  
回复 "显示可信度" 或 "隐藏可信度"

【摘要模式】
回复 "简洁" / "标准" / "详细"

回复 "取消" 返回主菜单
"""
        return {
            'action': 'format_optimization',
            'message': optimization_guide,
            'current_config': {
                'max_items': current_max_items,
                'show_credibility': current_show_credibility,
                'summary_style': current_summary_style
            }
        }
    
    def _handle_channel_optimization(self) -> Dict[str, Any]:
        """处理渠道优化请求"""
        current_primary = self.user_config.get('primary_channel', 'wechat')
        current_backup = self.user_config.get('backup_channels', [])
        current_push_time = self.user_config.get('push_time', '08:00')
        current_frequency = self.user_config.get('frequency', 'daily')
        
        optimization_guide = f"""
📡 渠道优化选项：

当前设置:
• 主渠道: {current_primary}
• 备用渠道: {', '.join(current_backup) if current_backup else '无'}
• 推送时间: {current_push_time}
• 频率: {current_frequency}

【渠道设置】
• 设置主渠道: 回复 "主渠道 [wechat/email/dingtalk/telegram]"
• 添加备用渠道: 回复 "备用渠道 [渠道名]"
• 移除备用渠道: 回复 "移除 [渠道名]"

【时间频率】
• 设置推送时间: 回复 "时间 HH:MM"
• 设置频率: 回复 "频率 [daily/weekday/custom]"

回复 "取消" 返回主菜单
"""
        return {
            'action': 'channel_optimization',
            'message': optimization_guide,
            'current_config': {
                'primary_channel': current_primary,
                'backup_channels': current_backup,
                'push_time': current_push_time,
                'frequency': current_frequency
            }
        }
    
    def _handle_detail_request(self, news_index: int) -> Dict[str, Any]:
        """处理详情请求"""
        # 这里需要从最近的新闻缓存中获取详情
        # 实际实现中需要维护新闻缓存
        detail_message = f"""
📋 正在获取第 {news_index} 条新闻的详细内容...

由于技术限制，详细内容需要您点击原文链接查看。
您可以回复其他序号查看不同新闻，或进行优化设置。
"""
        return {
            'action': 'detail_request',
            'message': detail_message,
            'news_index': news_index
        }
    
    def trigger_feedback_prompt_result(self) -> Dict[str, Any]:
        """触发反馈提示的结果"""
        self.trigger_feedback_prompt()
        return {
            'action': 'feedback_prompt',
            'message': '已重新发送反馈选项'
        }
    
    def apply_content_optimization(self, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用内容优化
        
        Args:
            optimization_data: 优化数据
            
        Returns:
            优化结果
        """
        try:
            new_config = self.user_config.copy()
            
            # 处理关键词
            if 'keywords' in optimization_data:
                if optimization_data['keywords'] == 'clear':
                    new_config['interest_keywords'] = []
                elif 'add' in optimization_data:
                    current = new_config.get('interest_keywords', [])
                    new_config['interest_keywords'] = list(set(current + [optimization_data['add']]))
                elif 'remove' in optimization_data:
                    current = new_config.get('interest_keywords', [])
                    if optimization_data['remove'] in current:
                        current.remove(optimization_data['remove'])
                    new_config['interest_keywords'] = current
            
            # 处理摘要风格
            if 'summary_style' in optimization_data:
                valid_styles = ['concise', 'standard', 'detailed']
                if optimization_data['summary_style'] in valid_styles:
                    new_config['summary_style'] = optimization_data['summary_style']
            
            return {
                'success': True,
                'new_config': new_config,
                'message': '内容优化已应用'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'应用内容优化失败: {str(e)}'
            }
    
    def apply_format_optimization(self, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用格式优化
        
        Args:
            optimization_data: 优化数据
            
        Returns:
            优化结果
        """
        try:
            new_config = self.user_config.copy()
            
            # 处理推送条数
            if 'max_items' in optimization_data:
                max_items = int(optimization_data['max_items'])
                if 3 <= max_items <= 10:
                    new_config['max_items'] = max_items
            
            # 处理可信度显示
            if 'show_credibility' in optimization_data:
                new_config['show_credibility'] = bool(optimization_data['show_credibility'])
            
            # 处理摘要风格
            if 'summary_style' in optimization_data:
                valid_styles = ['concise', 'standard', 'detailed']
                if optimization_data['summary_style'] in valid_styles:
                    new_config['summary_style'] = optimization_data['summary_style']
            
            return {
                'success': True,
                'new_config': new_config,
                'message': '格式优化已应用'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'应用格式优化失败: {str(e)}'
            }
    
    def apply_channel_optimization(self, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用渠道优化
        
        Args:
            optimization_data: 优化数据
            
        Returns:
            优化结果
        """
        try:
            new_config = self.user_config.copy()
            
            # 处理主渠道
            if 'primary_channel' in optimization_data:
                valid_channels = ['wechat', 'email', 'dingtalk', 'telegram']
                if optimization_data['primary_channel'] in valid_channels:
                    new_config['primary_channel'] = optimization_data['primary_channel']
            
            # 处理备用渠道
            if 'backup_channels' in optimization_data:
                valid_channels = ['wechat', 'email', 'dingtalk', 'telegram']
                backup = [ch for ch in optimization_data['backup_channels'] if ch in valid_channels]
                new_config['backup_channels'] = backup
            
            # 处理推送时间
            if 'push_time' in optimization_data:
                # 验证时间格式 HH:MM
                if re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', optimization_data['push_time']):
                    new_config['push_time'] = optimization_data['push_time']
            
            # 处理频率
            if 'frequency' in optimization_data:
                valid_frequencies = ['daily', 'weekday', 'custom']
                if optimization_data['frequency'] in valid_frequencies:
                    new_config['frequency'] = optimization_data['frequency']
            
            return {
                'success': True,
                'new_config': new_config,
                'message': '渠道优化已应用'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'应用渠道优化失败: {str(e)}'
            }
    
    def save_feedback_record(self, feedback_data: Dict[str, Any]):
        """保存反馈记录"""
        try:
            from scripts.config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.save_feedback_history(self.user_id, feedback_data)
            
        except Exception as e:
            print(f"保存反馈记录失败: {e}")
    
    def save_optimization_log(self, optimization_data: Dict[str, Any]):
        """保存优化日志"""
        try:
            from scripts.config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.save_optimization_log(self.user_id, optimization_data)
            
        except Exception as e:
            print(f"保存优化日志失败: {e}")