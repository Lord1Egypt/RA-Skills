"""
Constraint Checker - 约束检查器
验证文档是否符合约束条件
"""

import re
from typing import Dict, List, Tuple


class ConstraintChecker:
    """约束检查器 - 缰绳"""
    
    def __init__(self):
        self.constraints = {
            'forbidden_patterns': ['TODO', '待补充', '...', '[待填写]', 'xxx'],
            'required_markers': ['## 文档信息'],
            'min_length': 1000
        }
    
    def check(self, content: str, doc_type: str = None) -> Dict:
        """检查约束"""
        results = {
            'passed': True,
            'issues': [],
            'warnings': []
        }
        
        # 检查禁止模式
        for pattern in self.constraints.get('forbidden_patterns', []):
            if pattern in content:
                results['passed'] = False
                results['issues'].append({
                    'type': 'forbidden_pattern',
                    'pattern': pattern,
                    'severity': 'error'
                })
        
        # 检查最小长度
        if len(content) < self.constraints.get('min_length', 1000):
            results['warnings'].append({
                'type': 'min_length',
                'expected': self.constraints['min_length'],
                'actual': len(content),
                'severity': 'warning'
            })
        
        # 检查必需标记
        for marker in self.constraints.get('required_markers', []):
            if marker not in content:
                results['warnings'].append({
                    'type': 'missing_marker',
                    'marker': marker,
                    'severity': 'warning'
                })
        
        # 检查章节完整性（针对特定文档类型）
        if doc_type:
            section_check = self._check_sections(content, doc_type)
            if not section_check['passed']:
                results['warnings'].extend(section_check.get('issues', []))
        
        return results
    
    def enforce(self, content: str, doc_type: str = None) -> Tuple[bool, str]:
        """强制执行约束，返回 (是否通过, 修复后内容)"""
        fixed = content
        
        # 自动修复常见问题
        for pattern in self.constraints.get('forbidden_patterns', []):
            if pattern in fixed:
                # 替换为明确的标记
                replacement = f'【{pattern}】'
                fixed = fixed.replace(pattern, replacement)
        
        # 检查是否全部通过
        check_result = self.check(fixed, doc_type)
        
        return check_result['passed'], fixed
    
    def _check_sections(self, content: str, doc_type: str) -> Dict:
        """检查文档章节完整性"""
        required_sections = {
            'srs': ['## 1. 引言', '## 2. 总体描述', '## 3. 功能需求', '## 4. 非功能需求'],
            'sad': ['## 1. 架构概述', '## 2. 技术选型', '## 3. 模块设计'],
            'sdd': ['## 1. 模块详细设计', '## 2. 接口设计', '## 3. 数据结构'],
            'dbd': ['## 1. 数据库概述', '## 2. 表结构', '## 3. 索引设计'],
            'apid': ['## 1. 接口概述', '## 2. 接口列表', '## 3. 错误码'],
            'tsd': ['## 1. 测试策略', '## 2. 测试用例', '## 3. 覆盖率']
        }
        
        sections = required_sections.get(doc_type, [])
        result = {
            'passed': True,
            'issues': []
        }
        
        for section in sections:
            if section not in content:
                result['passed'] = False
                result['issues'].append({
                    'type': 'missing_section',
                    'section': section,
                    'severity': 'warning'
                })
        
        return result


class StructureValidator:
    """结构验证器"""
    
    def validate(self, content: str, doc_type: str) -> Dict:
        """验证文档结构"""
        result = {
            'passed': True,
            'issues': []
        }
        
        # 检查标题层级
        h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
        
        if h1_count == 0:
            result['passed'] = False
            result['issues'].append({
                'type': 'missing_h1',
                'severity': 'error'
            })
        
        if h2_count == 0:
            result['issues'].append({
                'type': 'no_subsections',
                'severity': 'warning'
            })
        
        # 检查代码块格式
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        for block in code_blocks:
            if not block.startswith('```') or not block.endswith('```'):
                result['issues'].append({
                    'type': 'invalid_code_block',
                    'severity': 'error'
                })
        
        return result


class ContentValidator:
    """内容验证器"""
    
    def validate(self, content: str) -> Dict:
        """验证文档内容"""
        result = {
            'passed': True,
            'issues': []
        }
        
        # 检查表格格式
        tables = re.findall(r'\|[^\n]+\|', content)
        if tables:
            # 检查表格格式一致性
            col_counts = [len([c for c in t.split('|') if c.strip()]) for t in tables]
            if len(set(col_counts)) > 1 and col_counts[0] != col_counts[-1]:  # 跳过表头分隔符
                result['issues'].append({
                    'type': 'inconsistent_tables',
                    'severity': 'warning'
                })
        
        # 检查链接格式
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        for text, url in links:
            if not url.startswith('http') and not url.startswith('#'):
                result['issues'].append({
                    'type': 'invalid_link',
                    'text': text,
                    'url': url,
                    'severity': 'warning'
                })
        
        return result


# 导出
__all__ = ['ConstraintChecker', 'StructureValidator', 'ContentValidator']
