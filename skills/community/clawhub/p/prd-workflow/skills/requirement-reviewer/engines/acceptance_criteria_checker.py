#!/usr/bin/env python3
"""
验收标准检查引擎 v1.0

检查验收标准的完整性和合理性
"""

import re
from typing import List, Dict


class AcceptanceCriteriaChecker:
    """验收标准检查引擎"""
    
    # 验收标准模板要素
    REQUIRED_ELEMENTS = [
        "前置条件",
        "操作步骤",
        "预期结果",
        "验收标准"
    ]
    
    # Given-When-Then 格式检查
    GWT_PATTERN = re.compile(r'(Given|当|在.*情况下).*?(When|当.*时).*?(Then|那么 | 则).*?', re.IGNORECASE)
    
    def check(self, prd_content: str) -> Dict:
        """
        检查验收标准
        
        参数:
            prd_content: PRD 文档内容
            
        返回:
            {
                "check_type": "acceptance_criteria",
                "score": 85,
                "issues": [...],
                "statistics": {...}
            }
        """
        issues = []
        
        # 提取验收标准章节
        acceptance_section = self.extract_acceptance_section(prd_content)
        
        if not acceptance_section:
            issues.append({
                "type": "missing_acceptance_section",
                "severity": "high",
                "title": "缺少验收标准章节",
                "description": "PRD 中没有验收标准章节",
                "location": "文档结构",
                "suggestion": "补充验收标准章节，包含功能验收、性能验收、安全验收等"
            })
            return {
                "check_type": "acceptance_criteria",
                "score": 0,
                "status": "fail",
                "issues": issues,
                "statistics": {}
            }
        
        # 检查验收标准要素
        element_issues = self.check_required_elements(acceptance_section)
        issues.extend(element_issues)
        
        # 检查 Given-When-Then 格式
        gwt_issues = self.check_gwt_format(acceptance_section)
        issues.extend(gwt_issues)
        
        # 检查验收标准覆盖率
        coverage_issues = self.check_coverage(prd_content, acceptance_section)
        issues.extend(coverage_issues)
        
        # 检查验收标准合理性
        quality_issues = self.check_quality(acceptance_section)
        issues.extend(quality_issues)
        
        # 计算得分
        score = self.calculate_score(issues)
        
        # 统计信息
        statistics = {
            "total_test_cases": self.count_test_cases(acceptance_section),
            "gwt_format_count": self.count_gwt_format(acceptance_section),
            "coverage_rate": self.calculate_coverage_rate(prd_content, acceptance_section)
        }
        
        return {
            "check_type": "acceptance_criteria",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "statistics": statistics
        }
    
    def extract_acceptance_section(self, prd_content: str) -> str:
        """提取验收标准章节"""
        patterns = [
            r'(验收标准.*?)(?=#|$)',
            r'(测试用例.*?)(?=#|$)',
            r'(Acceptance Criteria.*?)(?=#|$)',
            r'(验收.*?)(?=#|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, prd_content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1)
        
        return ""
    
    def check_required_elements(self, section: str) -> List[Dict]:
        """检查验收标准必备要素"""
        issues = []
        
        for element in self.REQUIRED_ELEMENTS:
            if element not in section:
                issues.append({
                    "type": "missing_element",
                    "severity": "medium",
                    "title": f"缺少{element}",
                    "description": f"验收标准中缺少{element}要素",
                    "location": "验收标准章节",
                    "suggestion": f"补充{element}，确保验收标准完整"
                })
        
        return issues
    
    def check_gwt_format(self, section: str) -> List[Dict]:
        """检查 Given-When-Then 格式"""
        issues = []
        
        # 统计使用 GWT 格式的用例数
        gwt_matches = self.GWT_PATTERN.findall(section)
        gwt_count = len(gwt_matches)
        
        # 统计总用例数
        total_cases = section.count("用例") + section.count("AC-") + section.count("测试")
        
        if total_cases > 0:
            gwt_rate = gwt_count / total_cases
            
            if gwt_rate < 0.5:
                issues.append({
                    "type": "low_gwt_usage",
                    "severity": "low",
                    "title": "Given-When-Then 格式使用率低",
                    "description": f"只有{gwt_rate*100:.1f}%的用例使用 GWT 格式",
                    "location": "验收标准章节",
                    "suggestion": "建议使用 Given-When-Then 格式编写验收标准，提高可读性和可执行性"
                })
        
        return issues
    
    def check_coverage(self, prd_content: str, acceptance_section: str) -> List[Dict]:
        """检查验收标准覆盖率"""
        issues = []
        
        # 提取功能清单
        function_patterns = [
            r'功能\s*\d+\.?\d*[:：]?\s*(.+?)(?:\n|$)',
            r'功能点[:：]?\s*(.+?)(?:\n|$)',
            r'支持(.+?)功能'
        ]
        
        functions = []
        for pattern in function_patterns:
            matches = re.findall(pattern, prd_content)
            functions.extend(matches)
        
        if functions:
            # 检查每个功能是否有对应用收标准
            uncovered_functions = []
            for func in functions:
                if func not in acceptance_section and func[:5] not in acceptance_section:
                    uncovered_functions.append(func)
            
            if len(uncovered_functions) > len(functions) * 0.3:
                issues.append({
                    "type": "low_coverage",
                    "severity": "high",
                    "title": "验收标准覆盖率低",
                    "description": f"{len(uncovered_functions)}个功能缺少验收标准",
                    "uncovered_functions": uncovered_functions[:5],
                    "location": "验收标准章节",
                    "suggestion": "为每个功能补充验收标准，确保覆盖率>70%"
                })
        
        return issues
    
    def check_quality(self, section: str) -> List[Dict]:
        """检查验收标准质量"""
        issues = []
        
        # 检查是否有量化指标
        quantitative_patterns = [
            r'\d+%',
            r'\d+ms',
            r'\d+ 秒',
            r'\d+ 分钟',
            r'QPS',
            r'TPS',
            r'并发'
        ]
        
        has_quantitative = any(re.search(pattern, section) for pattern in quantitative_patterns)
        
        if not has_quantitative:
            issues.append({
                "type": "no_quantitative_metrics",
                "severity": "medium",
                "title": "缺少量化指标",
                "description": "验收标准中没有量化指标",
                "location": "验收标准章节",
                "suggestion": "补充性能指标（响应时间、并发数）、业务指标（转化率、成功率）等"
            })
        
        # 检查是否有优先级标注
        priority_patterns = [r'P[0-2]', r'高优先级', r'中优先级', r'低优先级', r'Must', r'Should', r'Could']
        has_priority = any(re.search(pattern, section) for pattern in priority_patterns)
        
        if not has_priority:
            issues.append({
                "type": "no_priority",
                "severity": "low",
                "title": "缺少优先级标注",
                "description": "验收标准没有标注优先级",
                "location": "验收标准章节",
                "suggestion": "为验收标准标注优先级（P0/P1/P2 或 Must/Should/Could）"
            })
        
        return issues
    
    def calculate_score(self, issues: List[Dict]) -> int:
        """计算得分"""
        base_score = 100
        
        deduction = 0
        for issue in issues:
            if issue["severity"] == "high":
                deduction += 20
            elif issue["severity"] == "medium":
                deduction += 10
            elif issue["severity"] == "low":
                deduction += 5
        
        return max(0, base_score - deduction)
    
    def count_test_cases(self, section: str) -> int:
        """统计测试用例数量"""
        return section.count("用例") + section.count("AC-") + section.count("测试")
    
    def count_gwt_format(self, section: str) -> int:
        """统计 GWT 格式用例数"""
        return len(self.GWT_PATTERN.findall(section))
    
    def calculate_coverage_rate(self, prd_content: str, acceptance_section: str) -> float:
        """计算覆盖率"""
        # 简化实现：检查功能关键词在验收标准中的出现率
        function_keywords = ["功能", "模块", "支持", "提供"]
        
        prd_func_count = sum(prd_content.count(kw) for kw in function_keywords)
        acceptance_func_count = sum(acceptance_section.count(kw) for kw in function_keywords)
        
        if prd_func_count > 0:
            return acceptance_func_count / prd_func_count * 100
        return 0


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD
    
    ## 功能设计
    功能 1: 用户注册
    功能 2: 养老测算
    功能 3: 产品推荐
    
    ## 验收标准
    
    ### 功能验收
    用例 1: 用户注册
    Given 用户打开注册页面
    When 填写手机号和验证码
    Then 注册成功
    
    用例 2: 养老测算
    Given 用户已登录
    When 点击测算按钮
    Then 显示测算结果
    """
    
    checker = AcceptanceCriteriaChecker()
    result = checker.check(test_prd)
    
    print("验收标准检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"问题数：{len(result['issues'])}")
    print(f"统计：{result['statistics']}")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}: {issue['description']}")
