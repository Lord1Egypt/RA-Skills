"""
Parser utilities - 日期和输入解析工具。
"""
import re
from datetime import datetime
from typing import List, Dict, Optional


def parse_date(text: str, current_month: str = None) -> str:
    """
    智能解析日期文本为 YYYY-MM-DD 格式。
    
    Args:
        text: 日期文本
        current_month: 当前月份（YYYY-MM），用于补全简写日期
    
    Returns:
        格式化后的日期字符串 (YYYY-MM-DD)
    """
    text = text.strip()
    
    # 如果已经是完整格式
    if re.match(r'^\d{4}-\d{2}-\d{2}$', text):
        return text
    
    # 尝试解析 YYYY-M-D 格式（自动补零）
    match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})$', text)
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"
    
    # 获取当前年月
    if current_month:
        year = current_month.split('-')[0]
        month = current_month.split('-')[1]
    else:
        now = datetime.now()
        year = str(now.year)
        month = str(now.month).zfill(2)
    
    # 解析纯数字日期
    # 2位: 05 -> 当月 05 日
    if re.match(r'^\d{1,2}$', text):
        day = int(text)
        return f"{year}-{month}-{day:02d}"
    
    # 4位: 0315 或 0314 -> 当月 MM-DD
    if re.match(r'^\d{4}$', text):
        month_part = int(text[:2])
        day_part = int(text[2:])
        if month_part > 12:  # 可能是 DDMM 格式
            day_part = month_part
            month_part = int(month)
        return f"{year}-{month_part:02d}-{day_part:02d}"
    
    # 解析中文格式: 3月15日, 3月15, 3月5日
    match = re.match(r'^(\d{1,2})月(\d{1,2})日?$', text)
    if match:
        m, d = match.groups()
        return f"{year}-{int(m):02d}-{int(d):02d}"
    
    # 解析中文格式: 3月
    match = re.match(r'^(\d{1,2})月$', text)
    if match:
        m = match.group(1)
        return f"{year}-{int(m):02d}-01"
    
    # 无法解析，返回原文本（让调用者处理）
    return text


def parse_input(text: str) -> List[Dict]:
    """
    解析用户输入为交易列表。
    
    支持格式：
    - "2026-03-15 -50 餐饮 现金 午餐"
    - "3月15日 花了50元 餐饮"
    - 批量多行输入
    
    Args:
        text: 用户输入文本
    
    Returns:
        交易字典列表
    """
    transactions = []
    
    # 按行分割
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 解析日期（寻找日期模式）
        date = None
        remaining = line
        
        # 尝试匹配日期格式
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # 2026-03-15
            r'\d{1,2}月\d{1,2}日?',  # 3月15日
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, line)
            if match:
                date_text = match.group()
                if '月' in date_text:
                    date = parse_date(date_text)
                else:
                    date = date_text
                remaining = line[:match.start()] + line[match.end():]
                break
        
        # 如果没有找到日期，使用今天
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 处理"花了XX元"这类关键词
        remaining = remaining.strip()
        
        # 提取金额
        amount = None
        amount_patterns = [
            (r'花了\s*(\d+(?:\.\d+)?)\s*元?', lambda m: -float(m.group(1))),
            (r'收入\s*(\d+(?:\.\d+)?)', lambda m: float(m.group(1))),
            (r'\+\s*(\d+(?:\.\d+)?)', lambda m: float(m.group(1))),
            (r'-\s*(\d+(?:\.\d+)?)', lambda m: -float(m.group(1))),
            (r'^(-?\d+(?:\.\d+)?)', lambda m: float(m.group(1))),
        ]
        
        for pattern, converter in amount_patterns:
            match = re.search(pattern, remaining)
            if match:
                amount = converter(match)
                remaining = remaining[:match.start()] + remaining[match.end():]
                break
        
        # 如果没有找到金额，跳过这一行
        if amount is None:
            continue
        
        # 解析剩余部分：分类、账户、描述
        parts = remaining.split()
        
        category = '其他'
        account = '现金'
        description = ''
        
        if len(parts) >= 1:
            category = parts[0]
        if len(parts) >= 2:
            account = parts[1]
        if len(parts) >= 3:
            description = ' '.join(parts[2:])
        
        transactions.append({
            'date': date,
            'amount': amount,
            'category': category,
            'account': account,
            'description': description
        })
    
    return transactions
