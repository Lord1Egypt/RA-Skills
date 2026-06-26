#!/usr/bin/env python3
"""
业务需求规则检查引擎 v1.0

检查业务需求规则是否符合金融行业规范
"""

import re
from typing import List, Dict


class BusinessRuleChecker:
    """业务需求规则检查引擎"""
    
    # 风险等级映射
    RISK_LEVELS = {
        "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5,
        "保守型": 1, "稳健型": 2, "平衡型": 3, "成长型": 4, "进取型": 5
    }
    
    # 业务规则定义
    BUSINESS_RULES = [
        {
            "id": "BR001",
            "name": "风险等级匹配",
            "rule": "产品风险等级 <= 客户风险等级",
            "severity": "high"
        },
        {
            "id": "BR002",
            "name": "起购金额检查",
            "rule": "客户资产 >= 产品起购金额",
            "severity": "high"
        },
        {
            "id": "BR003",
            "name": "投资期限匹配",
            "rule": "产品期限 <= 客户投资预期期限",
            "severity": "medium"
        },
        {
            "id": "BR004",
            "name": "适当性管理",
            "rule": "必须有风险测评和合格投资者认定流程",
            "severity": "high"
        },
        {
            "id": "BR005",
            "name": "冷静期制度",
            "rule": "私募/信托产品必须有冷静期",
            "severity": "high"
        }
    ]
    
    def check(self, prd_content: str) -> Dict:
        """
        检查业务需求规则
        
        参数:
            prd_content: PRD 文档内容
            
        返回:
            {
                "check_type": "business_rules",
                "score": 85,
                "issues": [...]
            }
        """
        issues = []
        
        # 检查各项业务规则
        issues.extend(self.check_risk_matching(prd_content))
        issues.extend(self.check_minimum_amount(prd_content))
        issues.extend(self.check_investment_term(prd_content))
        issues.extend(self.check_suitability_management(prd_content))
        issues.extend(self.check_cooling_off_period(prd_content))
        
        # 计算得分
        score = self.calculate_score(issues)
        
        return {
            "check_type": "business_rules",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "total_rules": len(self.BUSINESS_RULES),
            "passed_rules": len(self.BUSINESS_RULES) - len(issues)
        }
    
    def check_risk_matching(self, prd_content: str) -> List[Dict]:
        """检查风险等级匹配规则"""
        issues = []
        
        # 提取产品风险等级
        product_risk_pattern = r'产品风险等级 [为是]:?\s*(R[1-5]|保守型 | 稳健型 | 平衡型 | 成长型 | 进取型)'
        product_risk_match = re.search(product_risk_pattern, prd_content)
        
        # 提取客户风险等级要求
        customer_risk_pattern = r'客户风险等级 [为是]:?\s*(R[1-5]|保守型 | 稳健型 | 平衡型 | 成长型 | 进取型)'
        customer_risk_match = re.search(customer_risk_pattern, prd_content)
        
        if product_risk_match and customer_risk_match:
            product_risk = product_risk_match.group(1)
            customer_risk = customer_risk_match.group(1)
            
            product_level = self.RISK_LEVELS.get(product_risk, 0)
            customer_level = self.RISK_LEVELS.get(customer_risk, 0)
            
            if product_level > customer_level:
                issues.append({
                    "id": "BR001",
                    "type": "risk_mismatch",
                    "severity": "high",
                    "title": "风险等级不匹配",
                    "description": f"产品风险等级 ({product_risk}) 高于客户风险等级要求 ({customer_risk})",
                    "location": "产品概述章节",
                    "suggestion": "统一风险等级或补充风险不匹配的处理规则（如警示、确认等）"
                })
        
        return issues
    
    def check_minimum_amount(self, prd_content: str) -> List[Dict]:
        """检查起购金额规则"""
        issues = []
        
        # 检查是否有起购金额说明
        if "起购金额" in prd_content or "最低申购金额" in prd_content:
            # 检查是否有客户资产要求
            if "客户资产" not in prd_content and "资产规模" not in prd_content:
                issues.append({
                    "id": "BR002",
                    "type": "missing_asset_requirement",
                    "severity": "medium",
                    "title": "缺少客户资产要求",
                    "description": "定义了起购金额但未说明客户资产要求",
                    "location": "产品要素章节",
                    "suggestion": "补充客户资产要求或合格投资者资产标准"
                })
        
        return issues
    
    def check_investment_term(self, prd_content: str) -> List[Dict]:
        """检查投资期限匹配规则"""
        issues = []
        
        # 检查是否有投资期限说明
        if "投资期限" in prd_content or "封闭期" in prd_content:
            # 检查是否有客户预期期限说明
            if "客户预期" not in prd_content and "投资预期" not in prd_content:
                issues.append({
                    "id": "BR003",
                    "type": "missing_term_requirement",
                    "severity": "low",
                    "title": "缺少客户投资预期说明",
                    "description": "定义了产品期限但未考虑客户投资预期",
                    "location": "产品要素章节",
                    "suggestion": "补充客户投资预期期限的匹配规则"
                })
        
        return issues
    
    def check_suitability_management(self, prd_content: str) -> List[Dict]:
        """检查适当性管理规则"""
        issues = []
        
        # 检查是否有风险测评
        has_risk_assessment = "风险测评" in prd_content or "风险承受能力" in prd_content
        
        # 检查是否有合格投资者认定
        has_qualified_investor = "合格投资者" in prd_content or "投资者认定" in prd_content
        
        if not has_risk_assessment:
            issues.append({
                "id": "BR004",
                "type": "missing_risk_assessment",
                "severity": "high",
                "title": "缺少风险测评流程",
                "description": "未定义风险测评流程",
                "location": "功能设计章节",
                "suggestion": "补充风险测评问卷、评级流程、有效期管理等功能"
            })
        
        if not has_qualified_investor:
            issues.append({
                "id": "BR004",
                "type": "missing_qualified_investor",
                "severity": "high",
                "title": "缺少合格投资者认定",
                "description": "未定义合格投资者认定流程",
                "location": "功能设计章节",
                "suggestion": "补充合格投资者认定标准、材料上传、审核流程等功能"
            })
        
        return issues
    
    def check_cooling_off_period(self, prd_content: str) -> List[Dict]:
        """检查冷静期制度"""
        issues = []
        
        # 检查是否是私募/信托产品
        is_private = "私募" in prd_content or "非公开" in prd_content
        is_trust = "信托" in prd_content
        
        if is_private or is_trust:
            # 检查是否有冷静期说明
            has_cooling_off = "冷静期" in prd_content or "投资冷静期" in prd_content
            
            if not has_cooling_off:
                issues.append({
                    "id": "BR005",
                    "type": "missing_cooling_off",
                    "severity": "high",
                    "title": "缺少冷静期制度",
                    "description": "私募/信托产品未定义冷静期制度",
                    "location": "交易规则章节",
                    "suggestion": "补充冷静期时长（通常 24 小时）、冷静期解除流程等功能"
                })
        
        return issues
    
    def calculate_score(self, issues: List[Dict]) -> int:
        """计算得分"""
        # 基础分 100 分
        base_score = 100
        
        # 扣分规则
        deduction = 0
        for issue in issues:
            if issue["severity"] == "high":
                deduction += 15
            elif issue["severity"] == "medium":
                deduction += 10
            elif issue["severity"] == "low":
                deduction += 5
        
        return max(0, base_score - deduction)


# 测试
if __name__ == "__main__":
    # 测试用例
    test_prd = """
    # AI 养老规划助手 PRD
    
    ## 产品概述
    产品风险等级：R3（平衡型）
    客户风险等级：R2（稳健型）
    
    ## 功能设计
    包含风险测评功能
    """
    
    checker = BusinessRuleChecker()
    result = checker.check(test_prd)
    
    print("业务规则检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"问题数：{len(result['issues'])}")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}: {issue['description']}")
