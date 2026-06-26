#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言解析模块 - 修复版
将中文自然语言转换为日程数据
"""

import re
from datetime import datetime, timedelta

class NaturalLanguageParser:
    def __init__(self):
        self.today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    def parse(self, text):
        text = text.strip()
        
        # 删除操作
        if any(word in text for word in ['删除', '取消', '删掉']):
            return self._parse_delete(text)
        
        # 修改操作判断
        create_keywords = ['点', '号', '上午', '下午', '晚上', '早上', '明天', '后天', '今天']
        has_create_keyword = any(kw in text for kw in create_keywords)
        
        if not has_create_keyword and any(word in text for word in ['推迟', '延后', '提前']):
            return self._parse_update(text)
        
        # 创建操作（默认）
        return self._parse_create(text)
    
    def _parse_create(self, text):
        result = {
            'action': 'create',
            'title': None,
            'start_time': None,
            'end_time': None,
            'location': None,
            'reminder_minutes': 15,
            'is_all_day': False,
            'repeat_rule': None
        }
        
        # 解析日期和时间
        date = self._parse_date(text)
        start_time, end_time, is_all_day = self._parse_time(text, date)
        
        result['start_time'] = start_time
        result['end_time'] = end_time
        result['is_all_day'] = is_all_day
        
        # 提取标题
        title = self._extract_title(text)
        result['title'] = title if title else '新日程'
        
        # 提取地点
        location_match = re.search(r'(?:在|地点|位置|@)\s*([^，,]+?)(?:，|,|提醒|$)', text)
        if location_match:
            result['location'] = location_match.group(1).strip()
        
        # 解析提醒时间
        reminder_match = re.search(r'(?:提前|提早)\s*(\d+)\s*分钟', text)
        if reminder_match:
            result['reminder_minutes'] = int(reminder_match.group(1))
        
        # 解析重复规则
        if '每周' in text:
            weekday_match = re.search(r'每周[一二三四五六日]', text)
            if weekday_match:
                weekday_map = {'一': 'MO', '二': 'TU', '三': 'WE', '四': 'TH', '五': 'FR', '六': 'SA', '日': 'SU'}
                weekday = weekday_match.group(0)[-1]
                result['repeat_rule'] = f'FREQ=WEEKLY;BYDAY={weekday_map.get(weekday, "MO")}'
        elif '每天' in text:
            result['repeat_rule'] = 'FREQ=DAILY'
        
        return result
    
    def _extract_title(self, text):
        """提取日程标题"""
        title = None
        
        # 策略1: 在时间词之后提取
        patterns = [
            r'(?:点|号)\s*([^\d在地点提醒,，].+?)(?:，|,|在|地点|位置|提醒|提前|$)',
            r'(?:上午|下午|晚上|早上)\s*([^\d在地点提醒,，].+?)(?:，|,|在|地点|位置|提醒|提前|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                title = match.group(1).strip()
                break
        
        # 策略2: 如果有"到"，提取后面的内容
        if not title and '到' in text:
            match = re.search(r'到[^，,]*?\s*([^\d在地点提醒,，].+?)(?:，|,|在|地点|位置|提醒|提前|$)', text)
            if match:
                title = match.group(1).strip()
        
        # 策略3: 全天事件
        if not title and ('全天' in text or '整天' in text):
            match = re.search(r'(?:全天|整天)\s*([^在地点提醒,，].+?)(?:，|,|在|地点|位置|提醒|提前|$)', text)
            if match:
                title = match.group(1).strip()
        
        # 清理标题
        if title:
            title = re.sub(r'[，,]\s*(?:地点|在|提醒|提前).*$', '', title)
            title = title.strip()
        
        return title
    
    def _parse_date(self, text):
        date = self.today
        
        if '今天' in text:
            date = self.today
        elif '明天' in text:
            date = self.today + timedelta(days=1)
        elif '后天' in text:
            date = self.today + timedelta(days=2)
        elif '大后天' in text:
            date = self.today + timedelta(days=3)
        elif '下周' in text:
            date = self.today + timedelta(days=7)
        else:
            date_match = re.search(r'(\d{1,2})\s*月\s*(\d{1,2})\s*[号日]', text)
            if date_match:
                month = int(date_match.group(1))
                day = int(date_match.group(2))
                year = self.today.year
                if month < self.today.month:
                    year += 1
                date = datetime(year, month, day)
        
        return date
    
    def _parse_time(self, text, date):
        is_all_day = '全天' in text or '整天' in text
        
        if is_all_day:
            start_time = date.replace(hour=0, minute=0)
            end_time = date.replace(hour=23, minute=59)
            return start_time, end_time, True
        
        # 匹配时间范围
        patterns = [
            r'(?:下午|晚上)\s*(\d{1,2})\s*[点:]\s*(\d{1,2})?\s*到\s*(?:下午|晚上)?\s*(\d{1,2})\s*[点:]\s*(\d{1,2})?',
            r'(?:上午|早上)\s*(\d{1,2})\s*[点:]\s*(\d{1,2})?\s*到\s*(?:上午|早上)?\s*(\d{1,2})\s*[点:]\s*(\d{1,2})?',
            r'(\d{1,2})\s*[点:]\s*(\d{1,2})?\s*到\s*(\d{1,2})\s*[点:]\s*(\d{1,2})?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                start_hour = int(match.group(1))
                start_min = int(match.group(2)) if match.group(2) else 0
                end_hour = int(match.group(3))
                end_min = int(match.group(4)) if match.group(4) else 0
                
                if '下午' in text or '晚上' in text:
                    if start_hour < 12:
                        start_hour += 12
                    if end_hour < 12:
                        end_hour += 12
                
                start_time = date.replace(hour=start_hour, minute=start_min)
                end_time = date.replace(hour=end_hour, minute=end_min)
                return start_time, end_time, False
        
        # 单个时间（支持 "点半"）
        patterns = [
            (r'(?:下午|晚上)\s*(\d{1,2})\s*[点:]\s*(\d{1,2}|半)?', 'afternoon'),
            (r'(?:上午|早上)\s*(\d{1,2})\s*[点:]\s*(\d{1,2}|半)?', 'morning'),
            (r'(\d{1,2})\s*[点:]\s*(\d{1,2}|半)?', 'normal'),
        ]
        
        for pattern, time_type in patterns:
            match = re.search(pattern, text)
            if match:
                hour = int(match.group(1))
                minute_str = match.group(2) if match.group(2) else '0'
                
                # 处理 "半"
                if minute_str == '半':
                    minute = 30
                else:
                    minute = int(minute_str)
                
                # 处理下午/晚上时间
                if time_type == 'afternoon' or ('下午' in text or '晚上' in text):
                    if hour < 12:
                        hour += 12
                
                start_time = date.replace(hour=hour, minute=minute)
                end_time = start_time + timedelta(hours=1)
                return start_time, end_time, False
        
        # 默认时间
        start_time = date.replace(hour=9, minute=0)
        end_time = start_time + timedelta(hours=1)
        return start_time, end_time, False
    
    def _parse_delete(self, text):
        result = {'action': 'delete', 'query': None}
        match = re.search(r'(?:删除|取消|删掉)\s*(.+?)(?:的日程|的事件|$)', text)
        if match:
            result['query'] = match.group(1).strip()
        else:
            result['query'] = text.replace('删除', '').replace('取消', '').replace('删掉', '').strip()
        return result
    
    def _parse_update(self, text):
        """解析修改操作"""
        result = {
            'action': 'update',
            'query': None,
            'changes': {}
        }
        
        # 提取要修改的事件描述
        # 匹配 "把...改到..."、"将...推迟到..." 等模式
        patterns = [
            r'(?:把|将)\s*(.+?)\s*(?:改到|改为|调整到|推迟到|提前到)\s*(.+)',
            r'(?:修改|更改)\s*(.+?)\s*(?:到|为|至)\s*(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                result['query'] = match.group(1).strip()
                new_time_desc = match.group(2).strip()
                
                # 解析新的时间
                # 临时创建解析器来解析新时间
                temp_parser = NaturalLanguageParser()
                temp_result = temp_parser._parse_create(new_time_desc)
                
                if temp_result.get('start_time'):
                    result['changes']['start_time'] = temp_result['start_time']
                    result['changes']['end_time'] = temp_result['end_time']
                break
        
        # 如果没有匹配到完整模式，尝试简单匹配
        if not result['query']:
            # 匹配 "推迟30分钟"、"提前1小时"
            postpone_match = re.search(r'(?:推迟|延后)\s*(\d+)\s*(分钟|小时)', text)
            if postpone_match:
                amount = int(postpone_match.group(1))
                unit = postpone_match.group(2)
                minutes = amount * 60 if unit == '小时' else amount
                result['changes']['postpone_minutes'] = minutes
                # 尝试提取事件描述
                result['query'] = re.sub(r'(?:推迟|延后)\s*\d+\s*(?:分钟|小时)', '', text).strip()
            
            advance_match = re.search(r'(?:提前)\s*(\d+)\s*(分钟|小时)', text)
            if advance_match:
                amount = int(advance_match.group(1))
                unit = advance_match.group(2)
                minutes = amount * 60 if unit == '小时' else amount
                result['changes']['advance_minutes'] = minutes
                result['query'] = re.sub(r'(?:提前)\s*\d+\s*(?:分钟|小时)', '', text).strip()
        
        return result


if __name__ == "__main__":
    parser = NaturalLanguageParser()
    
    test_cases = [
        "明天下午3点开会",
        "后天晚上7点到9点，和客户吃饭，地点在海底捞",
        "3月15号全天出差",
        "每周一上午10点团队例会，提前15分钟提醒",
        "删除明天下午3点的会议",
    ]
    
    for text in test_cases:
        result = parser.parse(text)
        print(f"\n输入: {text}")
        print(f"标题: {result.get('title')}")
        print(f"时间: {result.get('start_time')} - {result.get('end_time')}")
        print(f"地点: {result.get('location')}")
        print(f"重复: {result.get('repeat_rule')}")
