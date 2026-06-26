#!/usr/bin/env python3
"""
一致性检查引擎 v2.0

检查 PRD 文档前后文是否矛盾
"""

import re
from typing import List, Dict, Set, Tuple
from collections import defaultdict


class ConsistencyChecker:
    """一致性检查引擎"""

    # 风险等级映射
    RISK_LEVELS = {
        "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5,
        "保守型": 1, "稳健型": 2, "平衡型": 3, "成长型": 4, "进取型": 5,
        "低风险": 1, "中低风险": 2, "中风险": 3, "中高风险": 4, "高风险": 5
    }

    # 需要检查一致性的关键数据模式
    KEY_DATA_PATTERNS = {
        "risk_level": {
            "patterns": [
                r'风险等级 [为是：]\s*(R[1-5]|[保守稳平成进][保守型]|低中高风险)',
                r'产品风险等级 [为是：]\s*(R[1-5])',
                r'客户风险等级 [为是：]\s*(R[1-5])',
                r'风险承受能力 [为是：]\s*(R[1-5])'
            ],
            "name": "风险等级",
            "severity": "high"
        },
        "fee_rate": {
            "patterns": [
                r'申购费率 [为是：]\s*([\d.]+)%',
                r'认购费率 [为是：]\s*([\d.]+)%',
                r'赎回费率 [为是：]\s*([\d.]+)%',
                r'管理费率 [为是：]\s*([\d.]+)%',
                r'托管费率 [为是：]\s*([\d.]+)%'
            ],
            "name": "费率",
            "severity": "high"
        },
        "investment_ratio": {
            "patterns": [
                r'投资比例 [为是：]\s*([\d.]+)%',
                r'仓位 [为是：]\s*([\d.]+)%',
                r'配置比例 [为是：]\s*([\d.]+)%'
            ],
            "name": "投资比例",
            "severity": "medium"
        },
        "min_amount": {
            "patterns": [
                r'起购金额 [为是：]\s*([\d,]+) 元',
                r'最低申购金额 [为是：]\s*([\d,]+) 元',
                r'认购起点 [为是：]\s*([\d,]+) 元'
            ],
            "name": "起购金额",
            "severity": "medium"
        }
    }

    # 术语同义词映射（用于检查术语一致性）
    TERM_SYNONYMS = {
        "基金份额": ["份额", "基金份额"],
        "申购": ["申购", "购买", "买入"],
        "赎回": ["赎回", "卖出", "退出"],
        "认购": ["认购", "首次购买"],
        "净值": ["净值", "单位净值", "NAV"],
        "收益率": ["收益率", "回报率", "收益"]
    }

    def check(self, prd_content: str) -> Dict:
        """
        检查 PRD 一致性

        参数:
            prd_content: PRD 文档内容

        返回:
            {
                "check_type": "consistency",
                "score": 85,
                "status": "pass/warning/fail",
                "issues": [...]
            }
        """
        issues = []

        # 检查风险等级一致性
        print("   🔍 检查风险等级一致性...")
        risk_issues = self.check_risk_level_consistency(prd_content)
        issues.extend(risk_issues)

        # 检查费率一致性
        print("   🔍 检查费率一致性...")
        fee_issues = self.check_fee_consistency(prd_content)
        issues.extend(fee_issues)

        # 检查投资比例一致性
        print("   🔍 检查投资比例一致性...")
        ratio_issues = self.check_investment_ratio_consistency(prd_content)
        issues.extend(ratio_issues)

        # 检查起购金额一致性
        print("   🔍 检查起购金额一致性...")
        amount_issues = self.check_min_amount_consistency(prd_content)
        issues.extend(amount_issues)

        # 检查术语一致性
        print("   🔍 检查术语一致性...")
        term_issues = self.check_terminology_consistency(prd_content)
        issues.extend(term_issues)

        # 计算得分
        score = self.calculate_score(issues)

        return {
            "check_type": "consistency",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "total_checks": 5,
            "passed_checks": 5 - len(set(i["type"] for i in issues))
        }

    def check_risk_level_consistency(self, content: str) -> List[Dict]:
        """检查风险等级一致性"""
        issues = []
        risk_mentions = []

        # 提取所有风险等级提及
        for pattern in self.KEY_DATA_PATTERNS["risk_level"]["patterns"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # 提取上下文
                start = max(0, match.start() - 20)
                end = min(len(content), match.end() + 20)
                context = content[start:end].replace('\n', ' ')

                risk_mentions.append({
                    "value": match.group(1),
                    "context": context,
                    "position": match.start()
                })

        # 检查是否一致
        if len(risk_mentions) >= 2:
            unique_values = set(m["value"] for m in risk_mentions)
            if len(unique_values) > 1:
                # 检查是否是产品风险 vs 客户风险的对比
                values_list = [m["value"] for m in risk_mentions]

                # 如果同时存在 R2 和 R3 等，检查是否是不匹配场景
                risk_numbers = [self.RISK_LEVELS.get(v, 0) for v in unique_values]
                if max(risk_numbers) > min(risk_numbers):
                    issues.append({
                        "id": "RISK_INCONSISTENT",
                        "type": "risk_level_mismatch",
                        "severity": "high",
                        "title": "风险等级不一致",
                        "description": f"文档中风险等级存在多个值：{', '.join(unique_values)}",
                        "location": "多处提及",
                        "suggestion": "统一风险等级表述，或明确区分产品风险等级与客户风险等级要求",
                        "details": risk_mentions
                    })

        return issues

    def check_fee_consistency(self, content: str) -> List[Dict]:
        """检查费率一致性"""
        issues = []
        fee_mentions = defaultdict(list)

        for pattern in self.KEY_DATA_PATTERNS["fee_rate"]["patterns"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                fee_name = pattern.split('费率')[0].split('率')[0]
                fee_value = match.group(1)
                fee_mentions[fee_name].append({
                    "value": fee_value,
                    "context": match.group(0),
                    "position": match.start()
                })

        # 检查同一费率是否有不同值
        for fee_name, mentions in fee_mentions.items():
            if len(mentions) >= 2:
                unique_values = set(m["value"] for m in mentions)
                if len(unique_values) > 1:
                    issues.append({
                        "id": f"FEE_{fee_name.upper()}_INCONSISTENT",
                        "type": "fee_mismatch",
                        "severity": "high",
                        "title": f"{fee_name}不一致",
                        "description": f"{fee_name}存在多个值：{', '.join(unique_values)}%",
                        "location": "多处提及",
                        "suggestion": "统一费率数值",
                        "details": mentions
                    })

        return issues

    def check_investment_ratio_consistency(self, content: str) -> List[Dict]:
        """检查投资比例一致性"""
        issues = []
        ratio_mentions = []

        for pattern in self.KEY_DATA_PATTERNS["investment_ratio"]["patterns"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                ratio_mentions.append({
                    "value": float(match.group(1)),
                    "context": match.group(0),
                    "position": match.start()
                })

        # 检查比例是否合理（总和不应超过 100%）
        if ratio_mentions:
            total = sum(m["value"] for m in ratio_mentions)
            if total > 100:
                issues.append({
                    "id": "RATIO_EXCEEDS_100",
                    "type": "ratio_overflow",
                    "severity": "medium",
                    "title": "投资比例总和超过 100%",
                    "description": f"投资比例总和为{total}%",
                    "location": "投资范围章节",
                    "suggestion": "检查投资比例配置，确保总和不超过 100%"
                })

        return issues

    def check_min_amount_consistency(self, content: str) -> List[Dict]:
        """检查起购金额一致性"""
        issues = []
        amount_mentions = defaultdict(list)

        for pattern in self.KEY_DATA_PATTERNS["min_amount"]["patterns"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # 规范化金额
                amount = float(match.group(1).replace(',', ''))
                amount_mentions["min_amount"].append({
                    "value": amount,
                    "context": match.group(0),
                    "position": match.start()
                })

        # 检查同一金额是否有不同值
        for amount_name, mentions in amount_mentions.items():
            if len(mentions) >= 2:
                unique_values = set(m["value"] for m in mentions)
                if len(unique_values) > 1:
                    issues.append({
                        "id": f"AMOUNT_{amount_name.upper()}_INCONSISTENT",
                        "type": "amount_mismatch",
                        "severity": "medium",
                        "title": "起购金额不一致",
                        "description": f"起购金额存在多个值：{[int(v) for v in unique_values]}元",
                        "location": "多处提及",
                        "suggestion": "统一金额数值"
                    })

        return issues

    def check_terminology_consistency(self, content: str) -> List[Dict]:
        """检查术语一致性"""
        issues = []

        # 检查术语使用是否一致
        for standard_term, synonyms in self.TERM_SYNONYMS.items():
            found_synonyms = []
            for synonym in synonyms:
                if synonym in content:
                    found_synonyms.append(synonym)

            # 如果同时使用了多个同义词，提示统一
            if len(found_synonyms) > 1:
                issues.append({
                    "id": f"TERM_{standard_term.upper()}_INCONSISTENT",
                    "type": "terminology_inconsistent",
                    "severity": "low",
                    "title": f"术语使用不统一",
                    "description": f"术语'{standard_term}'在文档中使用了多种表述：{', '.join(found_synonyms)}",
                    "location": "全文档",
                    "suggestion": f"统一使用'{standard_term}'"
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
                deduction += 3

        return max(0, base_score - deduction)


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD

    ## 产品概述
    产品风险等级：R3（平衡型）

    ## 功能需求
    用户风险等级要求：R2

    ## 费率说明
    申购费率：1.5%
    认购费率：1.2%
    """

    checker = ConsistencyChecker()
    result = checker.check(test_prd)

    print("\n一致性检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"状态：{result['status']}")
    print(f"问题数：{len(result['issues'])}")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}")
