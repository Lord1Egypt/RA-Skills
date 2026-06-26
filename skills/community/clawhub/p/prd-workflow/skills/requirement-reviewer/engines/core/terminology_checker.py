#!/usr/bin/env python3
"""
术语检查引擎 v2.0

检查金融术语使用是否准确
"""

import re
from typing import List, Dict, Set


class TerminologyChecker:
    """术语检查引擎"""

    # 标准术语库
    STANDARD_TERMS = {
        # 基金术语
        "fund_terms": {
            "correct": {
                "认购": "用于基金募集期购买",
                "申购": "用于基金存续期购买",
                "赎回": "基金份额变现",
                "转换": "同一基金管理人旗下基金间转换",
                "定投": "定期定额投资",
                "分红": "基金收益分配",
                "拆分": "基金份额拆分",
                "折算": "基金份额折算"
            },
            "incorrect": {
                "购买基金": "应使用'认购'或'申购'（区分募集期/存续期）",
                "卖出基金": "应使用'赎回'",
                "退出的": "应使用'赎回'或'转换'"
            }
        },
        # 风险术语
        "risk_terms": {
            "correct": {
                "R1": "低风险",
                "R2": "中低风险",
                "R3": "中风险",
                "R4": "中高风险",
                "R5": "高风险",
                "保守型": "对应 R1",
                "稳健型": "对应 R2",
                "平衡型": "对应 R3",
                "成长型": "对应 R4",
                "进取型": "对应 R5"
            },
            "incorrect": {
                "无风险": "金融产品不存在无风险，应使用'低风险'",
                "保本": "除保本基金外，不得宣传保本，应使用'低风险'"
            }
        },
        # 合规术语
        "compliance_terms": {
            "correct": {
                "合格投资者": "符合标准的投资者",
                "适当性管理": "投资者适当性管理",
                "风险承受能力": "投资者风险承受能力",
                "风险测评": "投资者风险承受能力测评",
                "冷静期": "投资冷静期"
            },
            "incorrect": {
                "投资人": "应使用'投资者'",
                "客户": "在正式文档中应使用'投资者'或'客户（投资者）'"
            }
        },
        # 业务术语
        "business_terms": {
            "correct": {
                "T 日": "交易日",
                "T+1 日": "交易日后第一天",
                "工作日": "证券交易所交易日",
                "开放日": "办理申购赎回业务的日期",
                "估值日": "基金资产估值日",
                "净值": "基金份额净值",
                "累计净值": "基金份额累计净值"
            },
            "incorrect": {
                "当天": "应使用'T 日'或'交易日'",
                "第二天": "应使用'T+1 日'",
                "价格": "基金应使用'净值'而非'价格'"
            }
        },
        # 费率术语
        "fee_terms": {
            "correct": {
                "申购费率": "申购时收取的费率",
                "认购费率": "认购时收取的费率",
                "赎回费率": "赎回时收取的费率",
                "管理费率": "基金管理人收取的费率",
                "托管费率": "基金托管人收取的费率",
                "销售服务费": "销售机构收取的服务费"
            },
            "incorrect": {
                "手续费": "应明确为'申购费'、'赎回费'等具体名目",
                "管理费": "正式文档应使用'管理费率'"
            }
        }
    }

    # 术语使用场景规则
    USAGE_RULES = {
        "认购_vs_申购": {
            "rule": "募集期购买用'认购'，存续期购买用'申购'",
            "check_patterns": [
                (r"募集期.*购买", "应使用'认购'"),
                (r"首发.*购买", "应使用'认购'"),
                (r"存续期.*购买", "应使用'申购'"),
                (r"开放期.*购买", "应使用'申购'")
            ]
        },
        "净值 vs 价格": {
            "rule": "基金使用'净值'，股票/债券使用'价格'",
            "check_patterns": [
                (r"基金.*价格", "应使用'基金净值'"),
                (r"基金份额价格", "应使用'基金份额净值'")
            ]
        }
    }

    def check(self, prd_content: str) -> Dict:
        """
        检查术语准确性

        参数:
            prd_content: PRD 文档内容

        返回:
            {
                "check_type": "terminology",
                "score": 90,
                "status": "pass/warning/fail",
                "issues": [...]
            }
        """
        issues = []

        # 检查不正确术语
        print("   🔍 检查不正确术语...")
        incorrect_issues = self.check_incorrect_terms(prd_content)
        issues.extend(incorrect_issues)

        # 检查术语使用场景
        print("   🔍 检查术语使用场景...")
        usage_issues = self.check_usage_rules(prd_content)
        issues.extend(usage_issues)

        # 检查术语一致性
        print("   🔍 检查术语一致性...")
        consistency_issues = self.check_term_consistency(prd_content)
        issues.extend(consistency_issues)

        # 计算得分
        score = self.calculate_score(issues)

        return {
            "check_type": "terminology",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "total_terms_checked": len(self.STANDARD_TERMS),
            "error_count": len(issues)
        }

    def check_incorrect_terms(self, content: str) -> List[Dict]:
        """检查不正确术语使用"""
        issues = []

        for category, term_info in self.STANDARD_TERMS.items():
            incorrect_terms = term_info.get("incorrect", {})

            for incorrect, suggestion in incorrect_terms.items():
                if incorrect in content:
                    # 计算出现次数
                    count = content.count(incorrect)
                    issues.append({
                        "id": f"TERM_{incorrect}",
                        "type": "incorrect_term",
                        "severity": "low",
                        "title": f"术语使用不当：'{incorrect}'",
                        "description": f"发现{count}处使用不当术语'{incorrect}'",
                        "location": "全文档",
                        "suggestion": suggestion,
                        "category": category
                    })

        return issues

    def check_usage_rules(self, content: str) -> List[Dict]:
        """检查术语使用场景"""
        issues = []

        for rule_name, rule_info in self.USAGE_RULES.items():
            for pattern, suggestion in rule_info.get("check_patterns", []):
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    issues.append({
                        "id": f"RULE_{rule_name}",
                        "type": "term_usage_error",
                        "severity": "medium",
                        "title": f"术语使用场景错误：{rule_name}",
                        "description": f"发现不当用法：{match.group(0)}",
                        "location": "匹配位置",
                        "suggestion": suggestion
                    })

        return issues

    def check_term_consistency(self, content: str) -> List[Dict]:
        """检查术语一致性"""
        issues = []

        # 检查同一概念是否使用了多种表述
        term_variants = {
            "合格投资者": ["合格投资者", "合格投资人", "合格客户"],
            "风险承受能力": ["风险承受能力", "风险承受力", "风险容忍度"],
            "适当性": ["适当性", "适合性", "适配性"]
        }

        for standard_term, variants in term_variants.items():
            found_variants = [v for v in variants if v in content]

            # 如果同一概念使用了多种表述，提示统一
            if len(found_variants) > 1:
                issues.append({
                    "id": f"CONSISTENCY_{standard_term}",
                    "type": "term_inconsistency",
                    "severity": "low",
                    "title": f"术语表述不统一：{standard_term}",
                    "description": f"文档中使用了多种表述：{', '.join(found_variants)}",
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
                deduction += 15
            elif issue["severity"] == "medium":
                deduction += 5
            elif issue["severity"] == "low":
                deduction += 2

        return max(0, base_score - deduction)

    def get_standard_terms(self) -> Dict:
        """获取标准术语库"""
        return self.STANDARD_TERMS

    def suggest_term(self, incorrect_term: str) -> str:
        """建议正确术语"""
        for category, term_info in self.STANDARD_TERMS.items():
            if incorrect_term in term_info.get("incorrect", {}):
                return term_info["incorrect"][incorrect_term]
        return None


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD

    ## 产品概述
    客户可以用手购买基金，当天即可确认。
    基金份额价格为 1.0 元。

    ## 交易规则
    投资人通过 APP 下单购买，手续费为 1.5%。
    """

    checker = TerminologyChecker()
    result = checker.check(test_prd)

    print("\n术语检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"状态：{result['status']}")
    print(f"问题数：{len(result['issues'])}")
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['title']}")
        print(f"    建议：{issue['suggestion']}")
