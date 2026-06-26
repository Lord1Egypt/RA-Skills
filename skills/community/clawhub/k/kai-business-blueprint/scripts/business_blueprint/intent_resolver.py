"""
意图解析器 - Intent Resolver

根据用户goals、scope、sourceRefs自动推断蓝图意图
返回 blueprintIntent 和 strategySelection
"""

import re
from typing import Dict, List, Any


class IntentResolver:
    """意图解析器"""

    # 视角关键词定义
    PERSPECTIVE_KEYWORDS = {
        "product": {
            "keywords": ["产品", "能力", "功能", "价值", "产品规划", "产品蓝图", "产品架构"],
            "weight": 1.0
        },
        "technical": {
            "keywords": ["架构", "技术", "调用", "链路", "技术架构", "系统架构", "技术蓝图"],
            "weight": 1.0
        },
        "business": {
            "keywords": ["业务域", "CRM", "ERP", "OA", "业务蓝图", "业务架构", "业务域划分"],
            "weight": 1.0
        },
        "data": {
            "keywords": ["数据", "数据治理", "数据流转", "数据生命周期", "数据蓝图"],
            "weight": 1.0
        },
        "organizational": {
            "keywords": ["组织", "部门", "团队", "组织架构", "组织蓝图"],
            "weight": 1.0
        }
    }

    # 行业关键词定义（overlay_id完整名称）
    INDUSTRY_KEYWORDS = {
        "finance-regulatory": {
            "keywords": ["金融", "银行", "风控", "合规", "监管", "信贷", "支付"],
            "weight": 1.2
        },
        "manufacturing-supply-chain": {
            "keywords": ["制造", "工厂", "供应链", "MES", "生产", "车间", "仓储"],
            "weight": 1.2
        },
        "retail-operations": {
            "keywords": ["零售", "门店", "POS", "会员", "电商", "渠道"],
            "weight": 1.2
        },
        "healthcare-compliance": {
            "keywords": ["医疗", "医院", "健康", "患者", "诊疗"],
            "weight": 1.2
        }
    }

    def analyze_goals(self, goals: List[str]) -> Dict[str, Any]:
        """分析用户目标，推断蓝图意图"""
        if not goals:
            return {
                "primary": "product",
                "secondary": None,
                "mode": "auto",
                "confidence": 0.70,
                "reason": "no goals provided, default to product"
            }

        # 合并所有goals文本
        goal_text = " ".join(goals)

        # 计算各视角得分
        perspective_scores = {}
        for perspective, config in self.PERSPECTIVE_KEYWORDS.items():
            score = 0
            for keyword in config["keywords"]:
                # 精确匹配
                if keyword in goal_text:
                    score += config["weight"]
            perspective_scores[perspective] = score

        # 选择最高得分视角
        if sum(perspective_scores.values()) == 0:
            primary = "product"
            confidence = 0.70
        else:
            primary = max(perspective_scores, key=perspective_scores.get)
            max_score = perspective_scores[primary]
            # 归一化置信度
            confidence = min(max_score / max(len(goals), 1) * 0.3 + 0.70, 0.95)

        # 检测行业overlay
        secondary = self.detect_industry_overlay(goals)

        # 如果检测到行业，提高置信度
        if secondary:
            confidence = min(confidence + 0.10, 0.95)

        return {
            "primary": primary,
            "secondary": secondary,
            "mode": "auto",
            "confidence": round(confidence, 2),
            "reason": f"matched {perspective_scores[primary]} keywords in {primary} perspective"
        }

    def detect_industry_overlay(self, goals: List[str]) -> str | None:
        """检测行业叠加"""
        goal_text = " ".join(goals)

        # 计算各行业得分
        industry_scores = {}
        for industry, config in self.INDUSTRY_KEYWORDS.items():
            score = 0
            for keyword in config["keywords"]:
                if keyword in goal_text:
                    score += config["weight"]
            industry_scores[industry] = score

        # 选择最高得分行业（阈值：至少匹配1个关键词）
        if not industry_scores or max(industry_scores.values()) < 1.0:
            return None

        return max(industry_scores, key=industry_scores.get)

    def infer_strategy_selection(self, intent: Dict) -> Dict[str, Any]:
        """根据意图推断策略选择"""
        perspective_map = {
            "product": "product-capability",
            "technical": "technical-architecture",
            "business": "business-domain",
            "data": "data-governance",
            "organizational": "organizational"
        }

        strategy = perspective_map.get(intent["primary"], "product-capability")

        return {
            "selected": strategy,
            "source": "auto",
            "reason": intent["reason"],
            "confidence": intent["confidence"],
            "reviewNeeded": intent["confidence"] < 0.75
        }

    # 行业字段到overlay_id的映射
    INDUSTRY_TO_OVERLAY_MAP = {
        "finance": "finance-regulatory",
        "manufacturing": "manufacturing-supply-chain",
        "retail": "retail-operations",
        "healthcare": "healthcare-compliance"
    }

    def resolve_intent(self, blueprint: Dict) -> Dict[str, Any]:
        """解析蓝图意图（完整流程）"""
        goals = blueprint.get("context", {}).get("goals", [])
        industry = blueprint.get("meta", {}).get("industry", None)

        # 分析goals
        intent = self.analyze_goals(goals)

        # 如果goals没有检测到行业，使用meta.industry
        if not intent["secondary"] and industry and industry != "common":
            # 映射industry到overlay_id
            overlay_id = self.INDUSTRY_TO_OVERLAY_MAP.get(industry, industry)
            intent["secondary"] = overlay_id
            intent["confidence"] = min(intent["confidence"] + 0.05, 0.95)

        # 推断策略选择
        strategy_selection = self.infer_strategy_selection(intent)

        return {
            "blueprintIntent": intent,
            "strategySelection": strategy_selection
        }


if __name__ == "__main__":
    # 测试意图解析器
    resolver = IntentResolver()

    test_goals = [
        ["产品规划：展示云之家产品能力架构"],
        ["技术架构图：展示系统调用链路"],
        ["金融产品蓝图：展示支付风控能力"],
        ["制造业供应链蓝图：展示供应商到交付全链路"]
    ]

    for goals in test_goals:
        intent = resolver.analyze_goals(goals)
        strategy = resolver.infer_strategy_selection(intent)
        print(f"Goals: {goals[0]}")
        print(f"Intent: {intent['primary']} ({intent['confidence']})")
        print(f"Overlay: {intent['secondary']}")
        print(f"Strategy: {strategy['selected']}")
        print()