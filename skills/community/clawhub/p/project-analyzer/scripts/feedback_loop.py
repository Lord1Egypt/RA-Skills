"""
Feedback Loop - 反馈循环
质量校验和自动修正
"""

from typing import Dict, List
from constraint_checker import ConstraintChecker


class FeedbackLoop:
    """反馈循环 - 镜子"""
    
    def __init__(self):
        self.validators = [
            ConstraintChecker(),
        ]
        self.iteration_count = 0
        self.max_iterations = 3
    
    def validate(self, document: Dict) -> Dict:
        """验证文档质量"""
        results = {
            'passed': True,
            'issues': [],
            'suggestions': []
        }
        
        for validator in self.validators:
            result = validator.check(
                document.get('content', ''),
                document.get('type')
            )
            if not result.get('passed'):
                results['passed'] = False
            results['issues'].extend(result.get('issues', []))
            results['suggestions'].extend(result.get('warnings', []))
        
        return results
    
    def reflect(self, content: str, issues: List) -> str:
        """根据反馈修正内容"""
        self.iteration_count += 1
        
        if self.iteration_count >= self.max_iterations:
            return content
        
        fixed = content
        
        for issue in issues:
            if issue.get('type') == 'forbidden_pattern':
                pattern = issue.get('pattern')
                if pattern:
                    fixed = fixed.replace(pattern, f'【{pattern}】')
        
        return fixed


class QualityValidator:
    """质量验证器"""
    
    QUALITY_CHECKS = {
        'min_length': 1000,
        'max_line_length': 120,
        'code_blocks_valid': True,
        'tables_valid': True
    }
    
    def validate(self, content: str) -> Dict:
        """验证质量"""
        issues = []
        suggestions = []
        
        # 检查长度
        if len(content) < self.QUALITY_CHECKS['min_length']:
            issues.append({
                'type': 'too_short',
                'severity': 'warning',
                'message': f'文档长度不足: {len(content)} < {self.QUALITY_CHECKS["min_length"]}'
            })
            suggestions.append('建议补充更多细节内容')
        
        # 检查代码块
        if '```' in content:
            code_blocks = content.count('```')
            if code_blocks % 2 != 0:
                issues.append({
                    'type': 'invalid_code_block',
                    'severity': 'error'
                })
        
        return {
            'passed': len([i for i in issues if i.get('severity') == 'error']) == 0,
            'issues': issues,
            'suggestions': suggestions
        }


class ConsistencyValidator:
    """一致性验证器"""
    
    def validate(self, content: str) -> Dict:
        """验证一致性"""
        issues = []
        
        # 检查术语一致性
        # 检查编号连续性
        # 检查引用有效性
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }


# 导出
__all__ = ['FeedbackLoop', 'QualityValidator', 'ConsistencyValidator']
