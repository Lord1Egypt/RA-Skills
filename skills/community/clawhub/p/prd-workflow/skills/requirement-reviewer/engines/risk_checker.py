#!/usr/bin/env python3
"""
风险检查引擎 v2.0

检查风险揭示是否充分
"""

import re
from typing import List, Dict, Set


class RiskChecker:
    """风险检查引擎"""

    # 风险类型定义
    RISK_TYPES = {
        "market_risk": {
            "name": "市场风险",
            "priority": "P0",
            "keywords": ["市场风险", "市场价格波动", "经济周期", "政策变化", "利率风险"],
            "description": "因市场价格波动导致投资损失的风险"
        },
        "credit_risk": {
            "name": "信用风险",
            "priority": "P0",
            "keywords": ["信用风险", "违约风险", "信用评级下降", "交易对手风险"],
            "description": "交易对手违约或信用评级下降导致损失的风险"
        },
        "liquidity_risk": {
            "name": "流动性风险",
            "priority": "P0",
            "keywords": ["流动性风险", "无法变现", "赎回限制", "市场流动性不足"],
            "description": "无法及时变现或赎回受限的风险"
        },
        "management_risk": {
            "name": "管理风险",
            "priority": "P1",
            "keywords": ["管理风险", "管理人风险", "投资决策风险", "操作人员风险"],
            "description": "基金管理人管理不善导致损失的风险"
        },
        "policy_risk": {
            "name": "政策风险",
            "priority": "P1",
            "keywords": ["政策风险", "法律法规变化", "监管政策变化", "税收政策变化"],
            "description": "因政策法规变化导致损失的风险"
        },
        "technology_risk": {
            "name": "技术风险",
            "priority": "P1",
            "keywords": ["技术风险", "系统故障", "技术故障", "IT 风险", "网络攻击"],
            "description": "技术系统故障导致损失的风险"
        },
        "operation_risk": {
            "name": "操作风险",
            "priority": "P1",
            "keywords": ["操作风险", "操作失误", "人为错误", "流程风险"],
            "description": "操作流程失误导致损失的风险"
        }
    }

    # 必需的风险揭示要素
    REQUIRED_ELEMENTS = {
        "risk_level": {
            "name": "风险等级说明",
            "patterns": [r"风险等级 [为是：]\s*(R[1-5])", r"产品风险等级"],
            "priority": "P0"
        },
        "worst_case": {
            "name": "最不利投资情形",
            "patterns": ["最不利", "最坏情况", "极端情况", "最大损失", "本金损失"],
            "priority": "P0"
        },
        "risk_match": {
            "name": "风险匹配说明",
            "patterns": ["风险匹配", "风险承受能力", "适当性匹配"],
            "priority": "P0"
        }
    }

    # 风险等级与产品类型的对应
    RISK_LEVEL_REQUIREMENTS = {
        "R1": ["market_risk", "liquidity_risk"],
        "R2": ["market_risk", "credit_risk", "liquidity_risk"],
        "R3": ["market_risk", "credit_risk", "liquidity_risk", "management_risk"],
        "R4": ["market_risk", "credit_risk", "liquidity_risk", "management_risk", "policy_risk"],
        "R5": ["market_risk", "credit_risk", "liquidity_risk", "management_risk", "policy_risk", "technology_risk"]
    }

    def check(self, prd_content: str, risk_level: str = "R3") -> Dict:
        """
        检查风险揭示完整性

        参数:
            prd_content: PRD 文档内容
            risk_level: 产品风险等级

        返回:
            {
                "check_type": "risk_disclosure",
                "score": 85,
                "status": "pass/warning/fail",
                "issues": [...],
                "covered_risks": [...],
                "missing_risks": [...]
            }
        """
        issues = []
        covered_risks = []
        missing_risks = []

        # 检测文档中实际提到的风险等级
        detected_risk_level = self.detect_risk_level(prd_content)
        if detected_risk_level and detected_risk_level != risk_level:
            issues.append({
                "id": "RISK_LEVEL_MISMATCH",
                "type": "risk_level_inconsistency",
                "severity": "high",
                "title": "风险等级不一致",
                "description": f"文档中风险等级 ({detected_risk_level}) 与传入参数 ({risk_level}) 不一致",
                "location": "产品概述章节",
                "suggestion": "统一风险等级表述"
            })

        # 检查必需的风险揭示要素
        print("   🔍 检查风险揭示要素...")
        element_issues = self.check_required_elements(prd_content)
        issues.extend(element_issues)

        # 检查各类风险揭示
        print("   🔍 检查风险类型覆盖...")
        for risk_type, risk_info in self.RISK_TYPES.items():
            covered = self.check_risk_coverage(prd_content, risk_info["keywords"])

            if covered:
                covered_risks.append(risk_type)
            else:
                # 根据风险等级判断是否必需
                required_risks = self.RISK_LEVEL_REQUIREMENTS.get(risk_level, [])
                if risk_type in required_risks:
                    missing_risks.append(risk_type)
                    issues.append({
                        "id": f"MISSING_{risk_type.upper()}",
                        "type": "missing_risk_disclosure",
                        "severity": "high" if risk_info["priority"] == "P0" else "medium",
                        "title": f"缺失{risk_info['name']}揭示",
                        "description": f"{risk_level}产品需要揭示{risk_info['name']}",
                        "location": "风险揭示章节",
                        "suggestion": f"补充{risk_info['name']}揭示：{risk_info['description']}"
                    })

        # 计算得分
        score = self.calculate_score(issues, len(self.RISK_TYPES))

        return {
            "check_type": "risk_disclosure",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "covered_risks": covered_risks,
            "missing_risks": missing_risks,
            "risk_level": risk_level,
            "coverage_rate": len(covered_risks) / len(self.RISK_TYPES) * 100 if self.RISK_TYPES else 0
        }

    def detect_risk_level(self, content: str) -> str:
        """检测文档中提到的风险等级"""
        patterns = [
            r"产品风险等级 [为是：]\s*(R[1-5])",
            r"风险等级 [为是：]\s*(R[1-5])",
            r"本产品风险等级 [为是：]\s*(R[1-5])"
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)

        return None

    def check_required_elements(self, content: str) -> List[Dict]:
        """检查必需的风险揭示要素"""
        issues = []

        for element_id, element_info in self.REQUIRED_ELEMENTS.items():
            found = False

            for pattern in element_info["patterns"]:
                if re.search(pattern, content, re.IGNORECASE):
                    found = True
                    break

            if not found:
                issues.append({
                    "id": f"MISSING_{element_id.upper()}",
                    "type": "missing_risk_element",
                    "severity": "high" if element_info["priority"] == "P0" else "medium",
                    "title": f"缺失：{element_info['name']}",
                    "description": f"风险揭示缺少{element_info['name']}",
                    "location": "风险揭示章节",
                    "suggestion": f"补充{element_info['name']}相关说明"
                })

        return issues

    def check_risk_coverage(self, content: str, keywords: List[str]) -> bool:
        """检查某类风险是否被覆盖"""
        for keyword in keywords:
            if keyword.lower() in content.lower():
                return True
        return False

    def calculate_score(self, issues: List[Dict], total_risks: int) -> int:
        """计算得分"""
        base_score = 100

        # 统计缺失的风险类型数量
        missing_risk_count = len([i for i in issues if i["type"] == "missing_risk_disclosure"])

        # 每缺失一个风险类型扣分
        risk_deduction = missing_risk_count * 10

        # 其他问题扣分
        other_deduction = 0
        for issue in issues:
            if issue["type"] != "missing_risk_disclosure":
                if issue["severity"] == "high":
                    other_deduction += 10
                elif issue["severity"] == "medium":
                    other_deduction += 5

        return max(0, base_score - risk_deduction - other_deduction)

    def get_risk_disclosure_template(self, risk_type: str) -> str:
        """获取风险揭示模板"""
        templates = {
            "market_risk": """
## 市场风险

证券市场价格会因为国际政治环境、国内宏观经济环境、经济周期波动、利率期限结构变化等因素产生波动，从而对本产品的收益水平产生影响。投资者可能面临市场风险。
""",
            "credit_risk": """
## 信用风险

信用风险是指本产品投资的标的发行人或交易对手无法履行其承诺的风险。当交易对手无法履行支付义务时，本产品可能会遭受损失。
""",
            "liquidity_risk": """
## 流动性风险

流动性风险是指投资者无法在合理价格下及时变现的风险。在市场流动性不足或发生巨额赎回时，本产品可能面临流动性风险。
""",
            "management_risk": """
## 管理风险

管理风险是指基金管理人管理不善导致的风险。包括但不限于：投资决策失误、风险控制不力、人员操作失误等。
""",
            "policy_risk": """
## 政策风险

政策风险是指因国家法律法规、监管政策、税收政策等发生变化，导致本产品投资收益波动的风险。
""",
            "technology_risk": """
## 技术风险

技术风险是指因技术系统故障、网络攻击、数据丢失等原因，导致本产品无法正常运作或遭受损失的风险。
"""
        }

        return templates.get(risk_type, "")


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD

    ## 风险揭示

    ### 市场风险
    本产品面临市场风险，市场价格波动可能影响收益。

    ### 流动性风险
    在市场流动性不足时，可能面临流动性风险。
    """

    checker = RiskChecker()
    result = checker.check(test_prd, risk_level="R3")

    print("\n风险检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"状态：{result['status']}")
    print(f"覆盖风险类型：{len(result['covered_risks'])}")
    print(f"缺失风险类型：{len(result['missing_risks'])}")
    print(f"\n问题列表:")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}")
