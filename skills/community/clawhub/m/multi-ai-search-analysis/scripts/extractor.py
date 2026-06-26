#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据自动提取工具 - 从 AI 回复中自动提取关键数据和洞察
版本：v1.0
功能：
- NLP + 正则表达式提取关键数据
- 质量评分系统
- 数据对比表自动生成
"""

import re
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


class DataExtractor:
    """数据自动提取器"""
    
    def __init__(self):
        # 常见数据模式
        self.patterns = {
            # 数值数据
            'percentage': r'(\d+\.?\d*)\s*%',  # 百分比
            'number': r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)',  # 普通数字
            'currency': r'[\$￥€£]\s*(\d+\.?\d*)',  # 货币
            'date': r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',  # 日期
            'year': r'\b(19\d{2}|20\d{2})\b',  # 年份
            
            # 特定场景数据
            'oil_price': r'油价.*?(\d+\.?\d*)\s*美元',  # 油价
            'gdp_growth': r'GDP.*?(\d+\.?\d*)\s*%',  # GDP 增长
            'inflation': r'(CPI|通胀).*?(\d+\.?\d*)\s*%',  # 通胀率
            'unemployment': r'失业率.*?(\d+\.?\d*)\s*%',  # 失业率
            'market_cap': r'市值.*?[\$￥€£]\s*(\d+\.?\d*)',  # 市值
            
            # 比较性语言
            'increase': r'(增长 | 上升 | 提高 | 增加).*?(\d+\.?\d*)\s*%',
            'decrease': r'(下降 | 减少 | 降低).*?(\d+\.?\d*)\s*%',
            
            # 预测性语言
            'prediction': r'(预计 | 预测 | 或将 | 可能).*?(\d+\.?\d*)\s*(%|美元 | 亿 | 万)?',
            'target': r'(目标 | 达到).*?(\d+\.?\d*)\s*(%|美元 | 亿 | 万)?',
        }
        
        # 质量评分权重
        self.scoring_weights = {
            'word_count': 0.2,  # 字数
            'data_points': 0.3,  # 数据点数量
            'structure': 0.2,  # 结构清晰度
            'sources': 0.15,  # 引用来源
            'specificity': 0.15,  # 具体性
        }
    
    def extract_all(self, text: str) -> Dict:
        """提取所有类型的数据"""
        results = {
            'numbers': [],
            'percentages': [],
            'dates': [],
            'predictions': [],
            'key_insights': [],
            'data_points': []
        }
        
        # 提取百分比
        for match in re.finditer(self.patterns['percentage'], text):
            results['percentages'].append({
                'value': float(match.group(1)),
                'context': self._get_context(text, match.start(), match.end()),
                'position': match.start()
            })
        
        # 提取日期
        for match in re.finditer(self.patterns['date'], text):
            results['dates'].append({
                'value': match.group(1),
                'context': self._get_context(text, match.start(), match.end()),
                'position': match.start()
            })
        
        # 提取预测
        for match in re.finditer(self.patterns['prediction'], text):
            results['predictions'].append({
                'text': match.group(0),
                'value': match.group(2),
                'unit': match.group(3) or '',
                'context': self._get_context(text, match.start(), match.end()),
                'position': match.start()
            })
        
        # 提取关键数据点（数字 + 上下文）
        results['data_points'] = self._extract_data_points(text)
        
        # 提取关键洞察
        results['key_insights'] = self._extract_key_insights(text)
        
        return results
    
    def _extract_data_points(self, text: str) -> List[Dict]:
        """提取带上下文的数据点"""
        data_points = []
        
        # 查找所有数字及其上下文
        for match in re.finditer(r'(\d+\.?\d*)\s*(%|美元 | 亿 | 万 | 千 | 百万 | 十亿)?', text):
            value = match.group(1)
            unit = match.group(2) or ''
            context = self._get_context(text, match.start(), match.end(), radius=30)
            
            # 过滤掉太短或无意义的数字
            if len(value) > 1 or unit:
                data_points.append({
                    'value': value,
                    'unit': unit,
                    'context': context.strip(),
                    'position': match.start()
                })
        
        return data_points
    
    def _extract_key_insights(self, text: str) -> List[str]:
        """提取关键洞察（带有关键词的句子）"""
        insights = []
        keywords = [
            '关键', '核心', '重要', '显著', '大幅', '首次', '突破',
            '创纪录', '历史新高', '转折点', '里程碑', '决定性',
            '因此', '所以', '由此可见', '综上所述', '总的来说'
        ]
        
        # 按句号分割句子
        sentences = re.split(r'[。！？.!?\n]', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20 or len(sentence) > 200:
                continue
            
            # 检查是否包含关键词
            for keyword in keywords:
                if keyword in sentence:
                    insights.append(sentence)
                    break
        
        return insights[:10]  # 最多返回 10 条
    
    def _get_context(self, text: str, start: int, end: int, radius: int = 50) -> str:
        """获取匹配位置前后的上下文"""
        context_start = max(0, start - radius)
        context_end = min(len(text), end + radius)
        
        prefix = '...' if context_start > 0 else ''
        suffix = '...' if context_end < len(text) else ''
        
        return f"{prefix}{text[context_start:context_end]}{suffix}"
    
    def calculate_quality_score(self, text: str, platform: str = '') -> Dict:
        """
        计算回复质量评分
        
        Returns:
            dict: {
                'total_score': float,  # 总分 0-100
                'breakdown': dict,  # 各维度得分
                'level': str  # 等级（优秀/良好/一般/较差）
            }
        """
        breakdown = {}
        
        # 1. 字数评分（20%）
        word_count = len(text)
        if word_count >= 1000:
            score_word = 100
        elif word_count >= 500:
            score_word = 80
        elif word_count >= 300:
            score_word = 60
        elif word_count >= 100:
            score_word = 40
        else:
            score_word = 20
        breakdown['word_count'] = {
            'score': score_word,
            'value': word_count,
            'weight': self.scoring_weights['word_count']
        }
        
        # 2. 数据点评分（30%）
        data = self.extract_all(text)
        data_point_count = len(data['data_points']) + len(data['percentages'])
        if data_point_count >= 10:
            score_data = 100
        elif data_point_count >= 5:
            score_data = 80
        elif data_point_count >= 3:
            score_data = 60
        elif data_point_count >= 1:
            score_data = 40
        else:
            score_data = 20
        breakdown['data_points'] = {
            'score': score_data,
            'value': data_point_count,
            'weight': self.scoring_weights['data_points']
        }
        
        # 3. 结构评分（20%）
        structure_indicators = [
            r'##|###',  # Markdown 标题
            r'^\d+\.|^一、|^1\.',  # 编号列表
            r'^[-*•]\s',  # 项目符号
            r'\|.*\|',  # 表格
        ]
        structure_count = sum(1 for pattern in structure_indicators 
                            if re.search(pattern, text, re.MULTILINE))
        score_structure = min(100, structure_count * 25)
        breakdown['structure'] = {
            'score': score_structure,
            'value': structure_count,
            'weight': self.scoring_weights['structure']
        }
        
        # 4. 引用来源评分（15%）
        source_patterns = [
            r'据.*?报道', r'根据.*?数据', r'引用.*?',
            r'\[\d+\]', r'\(\d{4}\)', r'http[s]?://',
            r'来源：', r'参考：'
        ]
        source_count = sum(len(re.findall(pattern, text)) 
                         for pattern in source_patterns)
        if source_count >= 5:
            score_sources = 100
        elif source_count >= 3:
            score_sources = 80
        elif source_count >= 1:
            score_sources = 60
        else:
            score_sources = 30
        breakdown['sources'] = {
            'score': score_sources,
            'value': source_count,
            'weight': self.scoring_weights['sources']
        }
        
        # 5. 具体性评分（15%）
        # 检查是否有具体的数字、日期、名称等
        specificity_score = 0
        if data['percentages']:
            specificity_score += 30
        if data['dates']:
            specificity_score += 30
        if data['predictions']:
            specificity_score += 20
        if len(data['key_insights']) >= 3:
            specificity_score += 20
        breakdown['specificity'] = {
            'score': min(100, specificity_score),
            'value': f"{len(data['percentages'])}%, {len(data['dates'])} dates, {len(data['predictions'])} predictions",
            'weight': self.scoring_weights['specificity']
        }
        
        # 计算总分
        total_score = (
            score_word * self.scoring_weights['word_count'] +
            score_data * self.scoring_weights['data_points'] +
            score_structure * self.scoring_weights['structure'] +
            score_sources * self.scoring_weights['sources'] +
            specificity_score * self.scoring_weights['specificity']
        )
        
        # 确定等级
        if total_score >= 85:
            level = '优秀'
        elif total_score >= 70:
            level = '良好'
        elif total_score >= 55:
            level = '一般'
        else:
            level = '较差'
        
        return {
            'total_score': round(total_score, 1),
            'breakdown': breakdown,
            'level': level,
            'platform': platform
        }
    
    def generate_comparison_table(self, results: List[Dict]) -> str:
        """
        生成数据对比表
        
        Args:
            results: 包含 platform, content, extracted_data 的列表
        
        Returns:
            str: Markdown 格式的对比表
        """
        if not results:
            return "无数据可对比"
        
        # 收集所有数据点类型
        all_data_types = set()
        for result in results:
            if 'extracted_data' in result:
                data = result['extracted_data']
                if data.get('percentages'):
                    all_data_types.add('percentages')
                if data.get('predictions'):
                    all_data_types.add('predictions')
                if data.get('key_insights'):
                    all_data_types.add('insights')
        
        # 生成表格
        lines = []
        lines.append("## 数据对比表\n")
        
        # 百分比对比
        if 'percentages' in all_data_types:
            lines.append("### 百分比数据对比\n")
            lines.append("| 平台 | 数据 1 | 数据 2 | 数据 3 | 共识值 |")
            lines.append("|------|--------|--------|--------|--------|")
            
            for result in results:
                platform = result.get('platform', 'Unknown')
                data = result.get('extracted_data', {})
                percentages = data.get('percentages', [])[:3]  # 最多 3 个
                
                values = [f"{p['value']}%" for p in percentages]
                while len(values) < 3:
                    values.append('-')
                
                lines.append(f"| {platform} | {values[0]} | {values[1]} | {values[2]} | - |")
            
            lines.append("")
        
        # 质量评分对比
        lines.append("### 质量评分对比\n")
        lines.append("| 平台 | 总分 | 字数 | 数据点 | 结构 | 引用 | 具体性 | 等级 |")
        lines.append("|------|------|------|--------|------|------|--------|------|")
        
        for result in results:
            platform = result.get('platform', 'Unknown')
            quality = result.get('quality_score', {})
            breakdown = quality.get('breakdown', {})
            
            total = quality.get('total_score', 0)
            word_score = breakdown.get('word_count', {}).get('score', 0)
            data_score = breakdown.get('data_points', {}).get('score', 0)
            struct_score = breakdown.get('structure', {}).get('score', 0)
            source_score = breakdown.get('sources', {}).get('score', 0)
            spec_score = breakdown.get('specificity', {}).get('score', 0)
            level = quality.get('level', '-')
            
            lines.append(
                f"| {platform} | {total} | {word_score} | {data_score} | "
                f"{struct_score} | {source_score} | {spec_score} | {level} |"
            )
        
        return '\n'.join(lines)


def main():
    """测试函数"""
    extractor = DataExtractor()
    
    # 测试文本
    test_text = """
    根据最新数据，2026 年全球油价预计将上涨 15%，达到每桶 95 美元。
    国际能源署（IEA）预测，到 2026 年底，布伦特原油价格可能突破 100 美元大关。
    
    关键洞察：
    1. 中东局势紧张是主要推动因素
    2. 全球需求增长 3.2%
    3. OPEC+ 减产协议延长至 2026 年 12 月
    
    据高盛报告，油价上涨可能导致全球通胀率上升 0.5 个百分点。
    预计美联储将推迟降息至 2026 年 Q4。
    """
    
    print(f"{Fore.CYAN}=== 数据提取测试 ==={Style.RESET_ALL}\n")
    
    # 提取数据
    data = extractor.extract_all(test_text)
    print(f"{Fore.GREEN}提取到的百分比：{len(data['percentages'])} 个{Style.RESET_ALL}")
    for p in data['percentages']:
        print(f"  - {p['value']}%: {p['context']}")
    
    print(f"\n{Fore.GREEN}提取到的日期：{len(data['dates'])} 个{Style.RESET_ALL}")
    for d in data['dates']:
        print(f"  - {d['value']}: {d['context']}")
    
    print(f"\n{Fore.GREEN}提取到的预测：{len(data['predictions'])} 个{Style.RESET_ALL}")
    for p in data['predictions']:
        print(f"  - {p['text']}")
    
    print(f"\n{Fore.GREEN}关键洞察：{len(data['key_insights'])} 条{Style.RESET_ALL}")
    for i in data['key_insights'][:3]:
        print(f"  - {i}")
    
    # 质量评分
    print(f"\n{Fore.CYAN}=== 质量评分测试 ==={Style.RESET_ALL}\n")
    quality = extractor.calculate_quality_score(test_text, 'Test Platform')
    
    print(f"总分：{Fore.YELLOW}{quality['total_score']}{Style.RESET_ALL} ({quality['level']})")
    print(f"\n详细评分:")
    for dim, info in quality['breakdown'].items():
        print(f"  {dim}: {info['score']} (权重：{info['weight']*100:.0f}%)")
    
    print(f"\n{Fore.CYAN}=== 完成 ==={Style.RESET_ALL}")


if __name__ == '__main__':
    main()
