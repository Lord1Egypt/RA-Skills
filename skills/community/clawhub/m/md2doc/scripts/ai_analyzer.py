#!/usr/bin/env python3
"""
AI 文档分析器
自动识别文档类型、生成插图、创建图表
"""

import re
import json
from typing import Dict, List, Tuple, Optional


class DocumentAnalyzer:
    """文档类型分析器"""
    
    # 文档类型特征关键词
    DOC_PATTERNS = {
        'product': {
            'keywords': ['PRD', '产品需求', '功能需求', '用户故事', '原型', '交互', '产品经理', 
                        'feature', 'requirement', 'user story', 'mockup', 'prototype'],
            'weight': 1.0
        },
        'tech': {
            'keywords': ['API', '接口', '架构', '数据库', '算法', '代码', '技术方案', 
                        'implementation', 'database', 'algorithm', 'architecture', 'technical'],
            'weight': 1.0
        },
        'business': {
            'keywords': ['商业计划', '市场分析', '竞品分析', '商业模式', '盈利', 'ROI',
                        'business plan', 'market analysis', 'competitor', 'revenue', 'strategy'],
            'weight': 1.0
        },
        'academic': {
            'keywords': ['摘要', '关键词', '引言', '结论', '参考文献', '实验', '研究',
                        'abstract', 'introduction', 'conclusion', 'reference', 'research'],
            'weight': 1.0
        },
        'report': {
            'keywords': ['周报', '月报', '总结', '汇报', '进展', '里程碑', 'KPI',
                        'weekly', 'monthly', 'summary', 'report', 'progress', 'milestone'],
            'weight': 0.8
        }
    }
    
    def __init__(self):
        self.confidence_threshold = 0.3
    
    def analyze(self, content: str) -> Tuple[str, float, Dict]:
        """
        分析文档类型
        
        返回: (文档类型, 置信度, 详细信息)
        """
        content_lower = content.lower()
        scores = {}
        
        for doc_type, pattern in self.DOC_PATTERNS.items():
            score = 0
            matches = []
            for keyword in pattern['keywords']:
                count = content_lower.count(keyword.lower())
                if count > 0:
                    score += count * pattern['weight']
                    matches.append((keyword, count))
            scores[doc_type] = {
                'score': score,
                'matches': matches
            }
        
        # 找出最高分的类型
        if not scores:
            return 'default', 0.0, {}
        
        best_type = max(scores.keys(), key=lambda x: scores[x]['score'])
        best_score = scores[best_type]['score']
        
        # 计算置信度 (0-1)
        total_score = sum(s['score'] for s in scores.values())
        confidence = best_score / total_score if total_score > 0 else 0
        
        # 根据置信度决定是否使用检测到的类型
        if confidence < self.confidence_threshold:
            return 'default', confidence, scores
        
        return best_type, confidence, scores
    
    def suggest_style(self, doc_type: str) -> str:
        """根据文档类型推荐样式"""
        style_map = {
            'product': 'product',
            'tech': 'tech',
            'business': 'business',
            'academic': 'academic',
            'report': 'business',
            'default': 'default'
        }
        return style_map.get(doc_type, 'default')
    
    def extract_topics(self, content: str) -> List[str]:
        """提取文档主题关键词"""
        # 提取所有标题作为主题
        topics = []
        for line in content.split('\n'):
            if line.startswith('#'):
                topic = line.lstrip('#').strip()
                if topic:
                    topics.append(topic)
        return topics[:5]  # 取前5个主题
    
    def suggest_images(self, content: str, doc_type: str) -> List[Dict]:
        """
        建议需要生成的插图
        
        返回: [{'section': '章节标题', 'description': '图片描述', 'prompt': 'AI绘图提示词'}]
        """
        suggestions = []
        topics = self.extract_topics(content)
        
        # 根据文档类型生成不同的插图建议
        if doc_type == 'product':
            # 产品文档 - 建议产品示意图、流程图
            if topics:
                suggestions.append({
                    'section': '产品概述',
                    'description': f'{topics[0]} 产品概念图',
                    'prompt': f'Product concept illustration for "{topics[0]}", modern flat design, blue and white color scheme, professional, clean background'
                })
            
        elif doc_type == 'tech':
            # 技术文档 - 建议架构图、流程图
            if len(topics) >= 2:
                suggestions.append({
                    'section': '技术架构',
                    'description': '系统架构示意图',
                    'prompt': 'Technical architecture diagram, clean lines, server icons, database symbols, cloud computing, blue and gray colors, professional style'
                })
                
        elif doc_type == 'business':
            # 商业文档 - 建议商业图表、增长曲线
            suggestions.append({
                'section': '商业分析',
                'description': '商业增长趋势图',
                'prompt': 'Business growth chart, upward trending graph, professional blue color scheme, modern corporate style, clean background'
            })
            
        elif doc_type == 'academic':
            # 学术文档 - 建议研究示意图
            if topics:
                suggestions.append({
                    'section': '研究方法',
                    'description': '研究流程示意图',
                    'prompt': f'Research methodology diagram for "{topics[0]}", academic style, clean and minimal, educational illustration'
                })
        
        return suggestions


class DataExtractor:
    """数据提取器 - 从 Markdown 中提取表格数据"""
    
    def extract_tables(self, content: str) -> List[Dict]:
        """
        提取所有表格数据
        
        返回: [{'title': '表标题', 'headers': [], 'rows': [], 'type': '数据类型'}]
        """
        tables = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 检测表格开始
            if line.startswith('|') and '|' in line[1:]:
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    table_lines.append(lines[i].strip())
                    i += 1
                
                # 解析表格
                parsed = self._parse_table(table_lines)
                if parsed:
                    # 尝试找到表格标题（前面的文本）
                    title = self._find_table_title(lines, i - len(table_lines))
                    parsed['title'] = title
                    tables.append(parsed)
            else:
                i += 1
        
        return tables
    
    def _parse_table(self, lines: List[str]) -> Optional[Dict]:
        """解析表格内容"""
        rows = []
        headers = []
        
        for idx, line in enumerate(lines):
            # 跳过分隔行
            if '---' in line or line.replace('|', '').replace('-', '').replace(':', '').strip() == '':
                continue
            
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if not cells:
                continue
            
            if idx == 0 or (idx == 1 and '---' not in line):
                headers = cells
            else:
                rows.append(cells)
        
        if headers and rows:
            return {
                'headers': headers,
                'rows': rows,
                'type': self._detect_data_type(headers, rows)
            }
        return None
    
    def _detect_data_type(self, headers: List[str], rows: List[List[str]]) -> str:
        """检测数据类型"""
        # 检查是否包含数字列
        numeric_cols = 0
        for col_idx in range(len(headers)):
            try:
                for row in rows[:3]:  # 检查前3行
                    if col_idx < len(row):
                        val = row[col_idx].replace('%', '').replace(',', '').strip()
                        float(val)
                numeric_cols += 1
            except:
                pass
        
        # 根据列名判断
        header_str = ' '.join(headers).lower()
        if any(kw in header_str for kw in ['时间', '日期', 'time', 'date', '月份', '季度']):
            return 'time_series'
        elif any(kw in header_str for kw in ['占比', '百分比', 'percent', '比例']):
            return 'percentage'
        elif numeric_cols >= 2:
            return 'numeric_comparison'
        else:
            return 'categorical'
    
    def _find_table_title(self, lines: List[str], table_start: int) -> str:
        """查找表格标题（表格前面的文本）"""
        # 向前查找5行
        for i in range(table_start - 1, max(0, table_start - 6), -1):
            line = lines[i].strip()
            if line and not line.startswith('|'):
                # 去掉 Markdown 标记
                title = line.lstrip('#').strip()
                if title:
                    return title
        return '数据表'


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self):
        self.supported_types = ['bar', 'line', 'pie', 'horizontal_bar']
    
    def generate_chart(self, table_data: Dict, chart_type: str = 'auto') -> str:
        """
        根据表格数据生成图表
        
        返回: 图表图片路径
        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
            matplotlib.rcParams['axes.unicode_minus'] = False
        except ImportError:
            print("警告: 未安装 matplotlib，无法生成图表")
            return None
        
        headers = table_data['headers']
        rows = table_data['rows']
        data_type = table_data.get('type', 'categorical')
        
        # 自动选择图表类型
        if chart_type == 'auto':
            chart_type = self._suggest_chart_type(data_type, headers, rows)
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == 'bar':
            self._create_bar_chart(ax, headers, rows)
        elif chart_type == 'horizontal_bar':
            self._create_horizontal_bar_chart(ax, headers, rows)
        elif chart_type == 'line':
            self._create_line_chart(ax, headers, rows)
        elif chart_type == 'pie':
            self._create_pie_chart(ax, headers, rows)
        
        plt.tight_layout()
        
        # 保存图表
        import tempfile
        chart_path = tempfile.mktemp(suffix='.png')
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def _suggest_chart_type(self, data_type: str, headers: List[str], rows: List[List[str]]) -> str:
        """建议图表类型"""
        if data_type == 'time_series':
            return 'line'
        elif data_type == 'percentage':
            return 'pie'
        elif len(rows) > 5:
            return 'horizontal_bar'
        else:
            return 'bar'
    
    def _create_bar_chart(self, ax, headers, rows):
        """创建柱状图"""
        labels = [row[0] for row in rows if row]
        values = []
        for row in rows:
            if len(row) > 1:
                try:
                    values.append(float(row[1].replace('%', '').replace(',', '')))
                except:
                    values.append(0)
        
        x = range(len(labels))
        ax.bar(x, values, color='#4472C4')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel(headers[1] if len(headers) > 1 else '数值')
        ax.set_title(headers[0] if headers else '数据对比')
    
    def _create_horizontal_bar_chart(self, ax, headers, rows):
        """创建水平柱状图"""
        labels = [row[0] for row in rows if row]
        values = []
        for row in rows:
            if len(row) > 1:
                try:
                    values.append(float(row[1].replace('%', '').replace(',', '')))
                except:
                    values.append(0)
        
        ax.barh(range(len(labels)), values, color='#4472C4')
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlabel(headers[1] if len(headers) > 1 else '数值')
        ax.set_title(headers[0] if headers else '数据对比')
    
    def _create_line_chart(self, ax, headers, rows):
        """创建折线图"""
        labels = [row[0] for row in rows if row]
        values = []
        for row in rows:
            if len(row) > 1:
                try:
                    values.append(float(row[1].replace('%', '').replace(',', '')))
                except:
                    values.append(0)
        
        ax.plot(labels, values, marker='o', color='#4472C4', linewidth=2)
        ax.set_ylabel(headers[1] if len(headers) > 1 else '数值')
        ax.set_title(headers[0] if headers else '趋势图')
        plt.xticks(rotation=45, ha='right')
    
    def _create_pie_chart(self, ax, headers, rows):
        """创建饼图"""
        labels = [row[0] for row in rows if row]
        values = []
        for row in rows:
            if len(row) > 1:
                try:
                    values.append(float(row[1].replace('%', '').replace(',', '')))
                except:
                    values.append(0)
        
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(headers[0] if headers else '占比分布')


def analyze_document(content: str) -> Dict:
    """
    完整分析文档
    
    返回分析结果字典
    """
    analyzer = DocumentAnalyzer()
    extractor = DataExtractor()
    
    # 分析文档类型
    doc_type, confidence, details = analyzer.analyze(content)
    
    # 推荐样式
    suggested_style = analyzer.suggest_style(doc_type)
    
    # 提取主题
    topics = analyzer.extract_topics(content)
    
    # 建议插图
    image_suggestions = analyzer.suggest_images(content, doc_type)
    
    # 提取表格数据
    tables = extractor.extract_tables(content)
    
    return {
        'document_type': doc_type,
        'confidence': confidence,
        'suggested_style': suggested_style,
        'topics': topics,
        'image_suggestions': image_suggestions,
        'tables': tables,
        'details': details
    }


if __name__ == '__main__':
    # 测试
    test_content = """
# 产品需求文档

## 项目概述
这是一个电商APP的产品需求文档。

## 功能模块

| 模块 | 用户数 | 占比 |
|------|--------|------|
| 首页 | 10000 | 50% |
| 商品 | 5000 | 25% |
| 购物车 | 3000 | 15% |
| 我的 | 2000 | 10% |

## 技术架构
使用微服务架构。
"""
    
    result = analyze_document(test_content)
    print(json.dumps(result, ensure_ascii=False, indent=2))

