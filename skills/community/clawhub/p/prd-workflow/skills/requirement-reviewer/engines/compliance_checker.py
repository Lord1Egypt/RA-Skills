#!/usr/bin/env python3
"""
合规检查引擎 v2.0

检查 PRD 文档是否满足金融行业合规要求
"""

import re
from typing import List, Dict, Set


class ComplianceChecker:
    """合规检查引擎"""

    # 合规检查点定义
    COMPLIANCE_CHECKPOINTS = {
        # 通用检查点（适用于所有产品）
        "CC002": {
            "name": "风险匹配原则",
            "description": "必须有风险匹配说明",
            "patterns": ["风险匹配", "风险承受能力匹配", "适当性匹配", "客户风险等级"],
            "regulation": "《证券期货投资者适当性管理办法》",
            "priority": "P0",
            "applicable": ["all"]
        },
        "CC003": {
            "name": "信息披露",
            "description": "必须有信息披露机制",
            "patterns": ["信息披露", "公告", "披露机制", "信息公告"],
            "regulation": "《证券投资基金信息披露管理办法》",
            "priority": "P0",
            "applicable": ["all"]
        },
        "CC006": {
            "name": "风险揭示书",
            "description": "必须有完整风险揭示",
            "patterns": ["风险揭示", "风险揭示书", "风险告知"],
            "regulation": "《金融产品适当性管理指引》",
            "priority": "P0",
            "applicable": ["all"]
        },
        "CC010": {
            "name": "净值化管理",
            "description": "必须说明净值化管理",
            "patterns": ["净值", "净值化管理", "单位净值", "累计净值"],
            "regulation": "《关于规范金融机构资产管理业务的指导意见》",
            "priority": "P0",
            "applicable": ["all"]
        },
        "CC015": {
            "name": "适当性管理",
            "description": "必须有适当性管理说明",
            "patterns": ["适当性", "适当性管理", "投资者适当性"],
            "regulation": "《证券期货投资者适当性管理办法》",
            "priority": "P0",
            "applicable": ["all"]
        },

        # 私募基金检查点
        "CC001": {
            "name": "合格投资者认定",
            "description": "必须有合格投资者认定流程",
            "patterns": ["合格投资者", "投资者认定", "投资者适当性认定"],
            "regulation": "《私募投资基金监督管理暂行办法》",
            "priority": "P0",
            "applicable": ["private", "trust"]
        },
        "CC005": {
            "name": "冷静期制度",
            "description": "必须有冷静期说明",
            "patterns": ["冷静期", "投资冷静期", "犹豫期"],
            "regulation": "《私募投资基金募集行为管理办法》",
            "priority": "P0",
            "applicable": ["private", "trust"]
        },
        "CC007": {
            "name": "回访确认",
            "description": "必须有回访确认机制",
            "patterns": ["回访", "确认回访", "投资回访"],
            "regulation": "《私募投资基金募集行为管理办法》",
            "priority": "P1",
            "applicable": ["private", "trust"]
        },

        # 开放式基金检查点
        "CC012": {
            "name": "巨额赎回管理",
            "description": "必须有巨额赎回条款",
            "patterns": ["巨额赎回", "大额赎回", "赎回限制"],
            "regulation": "《公开募集证券投资基金运作管理办法》",
            "priority": "P0",
            "applicable": ["open_fund"]
        },
        "CC013": {
            "name": "暂停赎回机制",
            "description": "必须有暂停赎回说明",
            "patterns": ["暂停赎回", "赎回暂停", "临时停牌"],
            "regulation": "《公开募集证券投资基金运作管理办法》",
            "priority": "P1",
            "applicable": ["open_fund"]
        },

        # 理财产品检查点
        "CC020": {
            "name": "业绩比较基准",
            "description": "必须有业绩比较基准说明",
            "patterns": ["业绩比较基准", "业绩基准", "比较基准"],
            "regulation": "《商业银行理财业务监督管理办法》",
            "priority": "P0",
            "applicable": ["wealth"]
        },
        "CC021": {
            "name": "理财产品风险评级",
            "description": "必须有理财产品风险评级",
            "patterns": ["风险评级", "产品风险等级", "理财风险"],
            "regulation": "《商业银行理财业务监督管理办法》",
            "priority": "P0",
            "applicable": ["wealth"]
        }
    }

    # 产品类型关键词
    PRODUCT_TYPE_KEYWORDS = {
        "private": ["私募", "非公开", "私募基金"],
        "trust": ["信托", "信托计划"],
        "open_fund": ["开放式", "开放型", "公募开放式"],
        "wealth": ["理财", "银行理财", "理财产品"],
        "fund": ["基金", "公募", "证券投资基金"],
        "amc": ["资管", "资产管理计划", "券商资管"]
    }

    def __init__(self, product_type: str = None, risk_level: str = None):
        """
        初始化合规检查器

        参数:
            product_type: 产品类型 (fund/private/trust/wealth)
            risk_level: 风险等级 (R1-R5)
        """
        self.product_type = product_type
        self.risk_level = risk_level

    def check(self, prd_content: str) -> Dict:
        """
        检查 PRD 合规性

        参数:
            prd_content: PRD 文档内容

        返回:
            {
                "check_type": "compliance",
                "score": 85,
                "status": "pass/warning/fail",
                "issues": [...],
                "passed_checkpoints": 10,
                "total_checkpoints": 12
            }
        """
        issues = []
        passed_checkpoints = 0
        total_checkpoints = 0

        # 自动识别产品类型
        if not self.product_type:
            self.product_type = self.detect_product_type(prd_content)

        print(f"   检测到产品类型：{self.product_type}")

        # 遍历所有检查点
        for checkpoint_id, checkpoint_info in self.COMPLIANCE_CHECKPOINTS.items():
            # 检查是否适用于当前产品类型
            if not self.is_applicable(checkpoint_info, self.product_type):
                continue

            total_checkpoints += 1

            # 检查是否满足
            found = self.check_checkpoint(prd_content, checkpoint_info)

            if found:
                passed_checkpoints += 1
            else:
                # 添加问题
                issues.append({
                    "id": checkpoint_id,
                    "type": "compliance_missing",
                    "severity": "high" if checkpoint_info["priority"] == "P0" else "medium",
                    "title": f"缺失：{checkpoint_info['name']}",
                    "description": checkpoint_info["description"],
                    "location": "全文档",
                    "suggestion": f"补充{checkpoint_info['name']}相关说明",
                    "regulation": checkpoint_info.get("regulation", ""),
                    "checkpoint": checkpoint_id
                })

        # 计算得分
        score = self.calculate_score(passed_checkpoints, total_checkpoints, issues)

        return {
            "check_type": "compliance",
            "score": score,
            "status": "pass" if score >= 80 else "warning" if score >= 60 else "fail",
            "issues": issues,
            "passed_checkpoints": passed_checkpoints,
            "total_checkpoints": total_checkpoints,
            "compliance_rate": (passed_checkpoints / total_checkpoints * 100) if total_checkpoints > 0 else 0
        }

    def detect_product_type(self, content: str) -> str:
        """检测产品类型"""
        for product_type, keywords in self.PRODUCT_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content:
                    return product_type
        return "fund"  # 默认为基金

    def is_applicable(self, checkpoint_info: Dict, product_type: str) -> bool:
        """检查检查点是否适用于当前产品"""
        applicable = checkpoint_info.get("applicable", [])
        if "all" in applicable:
            return True

        # 检查是否匹配
        if product_type in applicable:
            return True

        # 检查大类匹配
        if product_type == "fund" and "open_fund" in applicable:
            return True

        return False

    def check_checkpoint(self, content: str, checkpoint_info: Dict) -> bool:
        """检查单个检查点"""
        patterns = checkpoint_info.get("patterns", [])

        for pattern in patterns:
            if pattern.lower() in content.lower():
                return True

        return False

    def calculate_score(self, passed: int, total: int, issues: List[Dict]) -> int:
        """计算得分"""
        if total == 0:
            return 100

        # 基础分 = 通过率 * 100
        base_score = (passed / total) * 100

        # 扣分（P0 问题额外扣）
        deduction = 0
        p0_issues = len([i for i in issues if i["severity"] == "high"])
        p1_issues = len([i for i in issues if i["severity"] == "medium"])

        deduction = p0_issues * 10 + p1_issues * 5

        return max(0, min(100, int(base_score - deduction)))

    def get_compliance_summary(self) -> Dict:
        """获取合规检查点摘要"""
        summary = {
            "total": len(self.COMPLIANCE_CHECKPOINTS),
            "p0_count": len([c for c in self.COMPLIANCE_CHECKPOINTS.values() if c["priority"] == "P0"]),
            "p1_count": len([c for c in self.COMPLIANCE_CHECKPOINTS.values() if c["priority"] == "P1"]),
            "checkpoints": []
        }

        for checkpoint_id, info in self.COMPLIANCE_CHECKPOINTS.items():
            summary["checkpoints"].append({
                "id": checkpoint_id,
                "name": info["name"],
                "priority": info["priority"],
                "applicable": info["applicable"],
                "regulation": info.get("regulation", "")
            })

        return summary


# 测试
if __name__ == "__main__":
    test_prd = """
    # AI 养老规划助手 PRD

    ## 产品概述
    本产品为养老规划工具，风险等级 R3

    ## 风险揭示
    包含市场风险、信用风险、流动性风险

    ## 信息披露
    定期披露产品信息和净值
    """

    checker = ComplianceChecker()
    result = checker.check(test_prd)

    print("\n合规检查结果:")
    print(f"得分：{result['score']}/100")
    print(f"状态：{result['status']}")
    print(f"通过检查点：{result['passed_checkpoints']}/{result['total_checkpoints']}")
    print(f"合规率：{result['compliance_rate']:.1f}%")
    print(f"\n问题列表:")
    for issue in result['issues'][:5]:
        print(f"  - [{issue['severity']}] {issue['checkpoint']}: {issue['title']}")
