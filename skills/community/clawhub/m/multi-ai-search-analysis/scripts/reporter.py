#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成工具 - 生成综合对比分析报告
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from colorama import init, Fore, Style

# 设置 UTF-8 编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

init(autoreset=True)

# 使用 ASCII 兼容符号
CHECK = '[OK]'
CROSS = '[FAIL]'


class ReportGenerator:
    """报告生成器（通用版）"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> dict:
        """加载多种报告模板"""
        return {
            # 通用分析报告模板
            'general': {
                'title': '# {topic} - 综合分析报告',
                'sections': [
                    '## 执行摘要',
                    '## 一、核心观点',
                    '## 二、分维度分析',
                    '## 三、数据对比',
                    '## 四、各家 AI 特色',
                    '## 五、参考来源'
                ]
            },
            # 对比分析模板
            'comparison': {
                'title': '# {topic} - 对比分析报告',
                'sections': [
                    '## 对比总结',
                    '## 一、各选项详情',
                    '## 二、维度对比表',
                    '## 三、优劣势分析',
                    '## 四、推荐建议',
                    '## 五、各家 AI 评价'
                ]
            },
            # 趋势分析模板
            'trend': {
                'title': '# {topic} - 趋势分析报告',
                'sections': [
                    '## 核心趋势',
                    '## 一、现状分析',
                    '## 二、驱动因素',
                    '## 三、未来预测',
                    '## 四、风险与机遇',
                    '## 五、数据支持'
                ]
            },
            # 评测报告模板
            'evaluation': {
                'title': '# {topic} - 评测报告',
                'sections': [
                    '## 评测结论',
                    '## 一、评测维度',
                    '## 二、详细评分',
                    '## 三、优缺点',
                    '## 四、购买建议',
                    '## 五、各家观点'
                ]
            }
        }
    
    def get_template(self, template_name: str = 'general') -> dict:
        """获取指定模板"""
        return self.templates.get(template_name, self.templates['general'])
    
    def generate(self, topic: str, results: List[Dict], 
                 dimensions: List[str] = None, template_name: str = 'general') -> str:
        """
        生成报告（通用版）
        
        Args:
            topic: 分析主题
            results: 各家 AI 回复结果
            dimensions: 分析维度
            template_name: 模板名称（general/comparison/trend/evaluation）
        """
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        platforms = ', '.join(r['platform'] for r in results if r.get('success'))
        template = self.get_template(template_name)
        
        # 构建报告
        report = []
        
        # 标题（支持模板）
        title = template['title'].format(topic=topic)
        report.append(f"{title}\n")
        report.append(f"**生成时间**：{timestamp}  \n")
        report.append(f"**AI 平台**：{platforms}  \n")
        if dimensions:
            report.append(f"**分析维度**：{', '.join(dimensions)}  \n")
        report.append("\n---\n\n")
        
        # 根据模板生成各章节
        for section in template['sections']:
            report.append(f"{section}\n\n")
            
            # 执行摘要/对比总结等
            if '摘要' in section or '总结' in section or '结论' in section:
                report.append("[核心结论，待 AI 提取或用户补充]\n\n")
            
            # 各 AI 回复原文
            elif '回复' in section or '选项' in section or '详情' in section:
                for result in results:
                    if result.get('success'):
                        report.append(f"### {result['platform']}\n\n")
                        content = result.get('content', '无内容')
                        
                        # 如果内容太长，截取前 3000 字
                        if len(content) > 3000:
                            content = content[:3000] + "\n\n...（内容过长，已截断）"
                        
                        report.append(content)
                        report.append("\n\n")
                    else:
                        error = result.get('error', '未知错误')
                        report.append(f"### {result['platform']}\n\n")
                        report.append(f"[X] 获取失败：{error}\n\n")
            
            # 对比表
            elif '对比表' in section or '评分' in section:
                report.append("| 维度 | DeepSeek | Qwen | 豆包 | Kimi | 共识/平均 |\n")
                report.append("|------|----------|------|------|------|-------------|\n")
                report.append("| - | - | - | - | - | - |\n")
                report.append("\n*注：待实现自动数据提取*\n\n")
            
            # 各家特色
            elif '特色' in section or '评价' in section or '观点' in section:
                report.append("*待补充各家 AI 的分析特色*\n\n")
            
            # 其他章节留空待填充
            else:
                report.append("*待补充*\n\n")
        
        # 尾部
        report.append("---\n\n")
        report.append(f"*本报告由 Multi-AI Search Analysis v1.1 自动生成*\n")
        
        return '\n'.join(report)
    
    def save(self, content: str, output_path: str):
        """保存报告"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"{Fore.GREEN}{CHECK} 报告已保存：{output_path}{Style.RESET_ALL}")


def generate_report(topic: str, results: List[Dict], output_path: str = None, 
                    dimensions: List[str] = None, template_name: str = 'general',
                    comparison_table: str = None) -> str:
    """
    便捷函数：生成并保存报告
    
    Args:
        topic: 分析主题
        results: 各家 AI 回复结果
        output_path: 输出路径
        dimensions: 分析维度
        template_name: 报告模板名称
        comparison_table: 数据对比表（可选，由 extractor 生成）
    """
    
    generator = ReportGenerator()
    content = generator.generate(topic, results, dimensions, template_name)
    
    # 如果有对比表，插入到报告中
    if comparison_table:
        # 找到合适的位置插入对比表（通常在"数据对比"章节后）
        lines = content.split('\n')
        insert_index = -1
        for i, line in enumerate(lines):
            if '数据对比' in line or '维度对比表' in line:
                insert_index = i + 2  # 在标题后插入
                break
        
        if insert_index > 0:
            lines.insert(insert_index, comparison_table)
            content = '\n'.join(lines)
    
    if output_path is None:
        reports_dir = Path(__file__).parent.parent / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
        safe_topic = topic.replace('/', '_').replace('\\', '_')
        output_path = str(reports_dir / f"{safe_topic}-{timestamp}.md")
    
    generator.save(content, output_path)
    return output_path


if __name__ == '__main__':
    # 测试
    test_results = [
        {
            'platform': 'DeepSeek',
            'content': '这是 DeepSeek 的回复内容示例...',
            'success': True
        },
        {
            'platform': 'Qwen',
            'content': '这是 Qwen 的回复内容示例...',
            'success': True
        }
    ]
    
    output = generate_report('测试主题', test_results)
    print(f"测试报告已生成：{output}")
