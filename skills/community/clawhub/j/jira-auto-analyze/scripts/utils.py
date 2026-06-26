#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA自动分析工具函数
"""

import re
import json
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

def check_required_fields(text: str) -> Dict:
    """检查文本中是否包含四项必填信息
    
    Args:
        text: 要检查的文本
        
    Returns:
        dict: 包含检查结果和缺失字段
    """
    text_lower = text.lower()
    
    # 必填字段定义
    required_fields = {
        '环境': {
            'keywords': ['星舰', '飞船', '云'],
            'found': False,
            'value': None
        },
        '通道类型': {
            'keywords': ['web连接器', 'rpa', '乐企'],
            'found': False,
            'value': None
        },
        '项目版本号': {
            'pattern': r'(\d+\.\d+\.\d+|v\d+|版本\d+)',
            'found': False,
            'value': None
        },
        '相关日志': {
            'keywords': ['日志', 'log', 'trace', 'error', 'stack'],
            'found': False,
            'value': None
        }
    }
    
    missing_fields = []
    
    # 检查环境信息
    for env in required_fields['环境']['keywords']:
        if env in text_lower:
            required_fields['环境']['found'] = True
            required_fields['环境']['value'] = env
            break
    
    if not required_fields['环境']['found']:
        missing_fields.append('环境（星舰、飞船、云）')
    
    # 检查通道类型
    for channel in required_fields['通道类型']['keywords']:
        if channel in text_lower:
            required_fields['通道类型']['found'] = True
            required_fields['通道类型']['value'] = channel
            break
    
    if not required_fields['通道类型']['found']:
        missing_fields.append('通道类型（web连接器、rpa、乐企）')
    
    # 检查项目版本号（云工单除外）
    if '云' in text_lower:
        # 云工单不需要版本号
        required_fields['项目版本号']['found'] = True
        required_fields['项目版本号']['value'] = '云环境无需版本号'
    else:
        version_match = re.search(required_fields['项目版本号']['pattern'], text_lower)
        if version_match:
            required_fields['项目版本号']['found'] = True
            required_fields['项目版本号']['value'] = version_match.group(1)
    
    if not required_fields['项目版本号']['found']:
        missing_fields.append('项目相关服务模块版本号')
    
    # 检查相关日志
    for log_keyword in required_fields['相关日志']['keywords']:
        if log_keyword in text_lower:
            required_fields['相关日志']['found'] = True
            required_fields['相关日志']['value'] = log_keyword
            break
    
    if not required_fields['相关日志']['found']:
        missing_fields.append('相关日志信息')
    
    return {
        'is_valid': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'field_details': required_fields
    }

def match_rule(text: str, rules: List[Dict]) -> Optional[Dict]:
    """根据文本内容匹配分配规则，支持优先级处理
    
    Args:
        text: 要匹配的文本
        rules: 规则列表
        
    Returns:
        dict: 匹配的规则，如果没有匹配则返回None
    """
    text_lower = text.lower()
    best_match = None
    best_score = 0
    
    # 首先按优先级排序，高优先级规则先处理
    sorted_rules = sorted(rules, key=lambda x: x.get('priority', 0), reverse=True)
    
    for rule in sorted_rules:
        keywords = rule.get('keywords', [])
        if not keywords:  # 跳过空关键词规则（如"其他工单"）
            continue
            
        match_score = calculate_match_score(text_lower, keywords)
        
        # 如果匹配分数大于0，且大于当前最佳分数，则更新最佳匹配
        if match_score > best_score:
            best_score = match_score
            best_match = rule
            
        # 对于星舰工单，如果有匹配，立即返回（最高优先级）
        if rule.get('rule_name') == '星舰工单' and match_score > 0:
            return rule
    
    # 如果匹配分数大于0，返回匹配的规则
    if best_match and best_score > 0:
        return best_match
    
    # 否则返回"其他工单"规则
    other_rule = next((r for r in rules if r.get('rule_name') == '其他工单'), None)
    return other_rule

def calculate_match_score(text: str, keywords: List[str]) -> float:
    """计算文本与关键词的匹配分数
    
    Args:
        text: 文本内容
        keywords: 关键词列表
        
    Returns:
        float: 匹配分数（0-1）
    """
    if not text or not keywords:
        return 0.0
    
    matches = 0
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in text:
            matches += 1
            # 如果关键词较长，给予更高权重
            weight = min(len(keyword) / 10, 1.0)
            matches += weight
    
    # 计算分数：匹配的关键词数量 / 总关键词数量
    score = matches / len(keywords) if keywords else 0
    return min(score, 1.0)  # 确保不超过1.0

def load_config(config_path: str) -> Dict:
    """加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        dict: 配置信息
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"成功加载配置文件：{config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"配置文件不存在：{config_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"配置文件格式错误：{config_path}")
        raise

def save_config(config: Dict, config_path: str):
    """保存配置文件
    
    Args:
        config: 配置信息
        config_path: 配置文件路径
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        logger.info(f"成功保存配置文件：{config_path}")
    except Exception as e:
        logger.error(f"保存配置文件失败：{str(e)}")
        raise

def format_issue_display(issue: Dict) -> str:
    """格式化工单显示信息
    
    Args:
        issue: 工单信息
        
    Returns:
        str: 格式化后的显示信息
    """
    lines = []
    lines.append(f"工单号: {issue.get('issue_key', '未知')}")
    lines.append(f"状态: {issue.get('status', '未知')}")
    lines.append(f"概要: {issue.get('summary', '无')[:80]}...")
    
    if issue.get('is_valid'):
        lines.append(f"有效性: ✅ 通过")
        lines.append(f"匹配规则: {issue.get('rule_matched', '其他工单')}")
        lines.append(f"建议分配: {issue.get('suggested_assignee', '刘巍')}")
        lines.append(f"回复内容: {issue.get('suggested_reply', '收到，我会及时处理，请稍后')}")
    else:
        lines.append(f"有效性: ❌ 未通过")
        lines.append(f"缺少信息: {', '.join(issue.get('missing_fields', []))}")
    
    return "\n".join(lines)

def create_rejection_comment(missing_fields: List[str], config: Dict) -> str:
    """创建打回评论，包含规范文档链接
    
    Args:
        missing_fields: 缺失字段列表
        config: 配置信息
        
    Returns:
        str: 评论内容
    """
    base_message = config.get('rejection_message', '请提供相关环境、通道类型、版本号及日志信息')
    
    if missing_fields:
        # 格式化缺失信息
        missing_info = '\n'.join([f"- {field}" for field in missing_fields])
        details = f"\n\n**缺少以下必填信息：**\n{missing_info}\n\n请参考工单提交规范补充完整信息：http://confluence.51baiwang.com/pages/viewpage.action?pageId=80049485"
        return base_message + details
    else:
        return base_message