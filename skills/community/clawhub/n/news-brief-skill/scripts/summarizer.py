#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Summarizer Module
摘要生成模块：处理新闻内容，生成标准化摘要
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class NewsSummarizer:
    """新闻摘要生成器"""
    
    def __init__(self, user_id: str, user_config: Dict[str, Any]):
        self.user_id = user_id
        self.user_config = user_config
        self.project_root = Path(__file__).parent.parent
        
        # 加载模板
        self.brief_template = self._load_template("config/templates/brief_template.txt")
        self.news_item_template = self._load_template("config/templates/news_item_template.txt")
        
        # 摘要长度配置
        self.summary_lengths = {
            'concise': 50,    # 简洁模式
            'standard': 65,   # 标准模式  
            'detailed': 80    # 详细模式
        }
    
    def _load_template(self, template_path: str) -> str:
        """加载模板文件"""
        template_file = self.project_root / template_path
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def generate_brief(self, news_items: List[Dict[str, Any]]) -> str:
        """
        生成新闻简报
        
        Args:
            news_items: 新闻列表
            
        Returns:
            格式化的简报内容
        """
        try:
            # 获取用户配置
            domain = self.user_config.get('domains', ['tech'])[0]
            summary_style = self.user_config.get('summary_style', 'standard')
            show_credibility = self.user_config.get('show_credibility', True)
            
            # 生成新闻条目
            formatted_items = []
            for i, news in enumerate(news_items, 1):
                formatted_item = self._format_news_item(
                    news, i, summary_style, show_credibility
                )
                formatted_items.append(formatted_item)
            
            # 组装完整简报
            brief_content = self.brief_template.format(
                date=datetime.now().strftime('%Y-%m-%d'),
                domain=self._get_domain_name(domain),
                news_items="\n".join(formatted_items)
            )
            
            return brief_content
            
        except Exception as e:
            print(f"生成简报失败: {e}")
            # 返回简化版本
            return self._generate_fallback_brief(news_items)
    
    def _format_news_item(self, news: Dict[str, Any], index: int, 
                         summary_style: str, show_credibility: bool) -> str:
        """格式化单条新闻"""
        try:
            # 生成摘要
            summary = self._generate_summary(news.get('content', ''), summary_style)
            
            # 评估可信度
            credibility_info = self._evaluate_credibility(news)
            
            # 构建新闻条目
            item_content = self.news_item_template.format(
                index=index,
                title=news.get('title', '无标题'),
                summary=summary,
                source=news.get('source', '未知来源'),
                credibility=credibility_info['level'] if show_credibility else '',
                credibility_reason=credibility_info['reason'] if show_credibility else ''
            )
            
            # 如果不显示可信度，移除相关行
            if not show_credibility:
                lines = item_content.split('\n')
                filtered_lines = [line for line in lines if '⭐ 可信度' not in line]
                item_content = '\n'.join(filtered_lines)
            
            return item_content
            
        except Exception as e:
            print(f"格式化新闻条目失败: {e}")
            return f"{index}. 【{news.get('title', '无标题')}】\n   💡 内容获取失败"
    
    def _generate_summary(self, content: str, style: str) -> str:
        """生成新闻摘要"""
        if not content.strip():
            return "内容暂无"
        
        # 获取摘要长度
        max_length = self.summary_lengths.get(style, 65)
        
        # 简单的摘要生成逻辑（实际可集成AI摘要API）
        # 提取前max_length个字符，确保在句子边界处截断
        if len(content) <= max_length:
            return content.strip()
        
        # 在句子边界处截断
        sentence_endings = ['。', '！', '？', '.', '!', '?']
        truncated = content[:max_length]
        
        # 查找最后一个句子结束符
        last_end = -1
        for ending in sentence_endings:
            pos = truncated.rfind(ending)
            if pos > last_end:
                last_end = pos
        
        if last_end > 0:
            summary = truncated[:last_end + 1]
        else:
            summary = truncated + "..."
        
        return summary.strip()
    
    def _evaluate_credibility(self, news: Dict[str, Any]) -> Dict[str, str]:
        """评估新闻可信度"""
        source = news.get('source', '').lower()
        domain = news.get('domain', '').lower()
        
        # 权威媒体列表
        authoritative_sources = [
            'people', 'xinhua', 'cctv', 'guangming', 'economic',
            'eastmoney', 'cnstock', 'stcn', 'hexun'
        ]
        
        # 可信媒体列表  
        credible_sources = [
            '36kr', 'huxiu', 'ifeng', 'sohu', 'sina', 'netease',
            'qq', 'baidu', 'toutiao'
        ]
        
        if any(auth_source in source or auth_source in domain 
               for auth_source in authoritative_sources):
            return {
                'level': '权威',
                'reason': '官方媒体或权威财经媒体发布'
            }
        elif any(cred_source in source or cred_source in domain 
                for cred_source in credible_sources):
            return {
                'level': '可信', 
                'reason': '知名商业媒体发布'
            }
        else:
            return {
                'level': '普通',
                'reason': '来源未验证或小型媒体'
            }
    
    def _get_domain_name(self, domain_code: str) -> str:
        """获取领域中文名称"""
        domain_names = {
            'tech': '科技',
            'finance': '财经', 
            'politics': '时政',
            'business': '商业',
            'startup': '创业',
            'economy': '经济',
            'society': '社会',
            'general': '综合'
        }
        return domain_names.get(domain_code, domain_code)
    
    def _generate_fallback_brief(self, news_items: List[Dict[str, Any]]) -> str:
        """生成备用简报（当模板失败时）"""
        brief_lines = [f"📅 {datetime.now().strftime('%Y-%m-%d')} 新闻简报"]
        
        for i, news in enumerate(news_items[:5], 1):
            brief_lines.append(f"\n{i}. 【{news.get('title', '无标题')}】")
            brief_lines.append(f"   来源：{news.get('source', '未知')}")
        
        brief_lines.append("\n💡 回复序号查看详情，回复'反馈'进行优化")
        return "\n".join(brief_lines)
    
    def generate_preview_brief(self, news_items: List[Dict[str, Any]], 
                              optimization_type: str, new_config: Dict[str, Any]) -> str:
        """
        生成优化预览版简报
        
        Args:
            news_items: 新闻列表
            optimization_type: 优化类型
            new_config: 新配置
            
        Returns:
            预览版简报内容
        """
        try:
            # 临时使用新配置
            old_config = self.user_config.copy()
            self.user_config = new_config
            
            preview_content = self.generate_brief(news_items)
            
            # 恢复原配置
            self.user_config = old_config
            
            # 添加预览标识
            preview_header = f"🔍 优化预览版 - {optimization_type}\n\n"
            preview_footer = "\n✅ 满意请回复'确认'，不满意请回复'取消'"
            
            return preview_header + preview_content + preview_footer
            
        except Exception as e:
            print(f"生成预览简报失败: {e}")
            return "预览生成失败，请重试"