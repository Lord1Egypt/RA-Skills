"""
规则引擎 - Rule Engine

根据Perspective和Overlay配置，计算系统的层级归属
使用typed signals + score机制，可解释决策
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class RuleEngine:
    """规则引擎"""

    def __init__(self, perspective: Dict, overlay: Dict | None = None):
        """
        初始化规则引擎

        Args:
            perspective: Perspective配置（从JSON加载）
            overlay: Overlay配置（可选）
        """
        self.perspective = perspective
        self.overlay = overlay
        self.layer_order = [rule["layer"] for rule in perspective.get("rules", [])]

    def calculate_signal_score(self, system: Dict, signal: Dict) -> float:
        """计算单个signal的得分"""
        signal_type = signal.get("type")
        weight = signal.get("weight", 1.0)

        if signal_type == "category":
            # 检查system.category是否匹配
            system_category = system.get("category")
            if system_category in signal.get("values", []):
                return weight

        elif signal_type == "nameKeyword":
            # 检查system.name是否包含关键词
            system_name = system.get("name", "")
            keywords = signal.get("values", [])
            matched_count = sum(1 for kw in keywords if kw in system_name)
            return weight * matched_count

        elif signal_type == "propertyMatch":
            # 检查system.properties字段匹配
            prop_name = signal.get("property")
            prop_values = signal.get("values", [])
            system_value = system.get("properties", {}).get(prop_name)
            if system_value in prop_values:
                return weight

        return 0.0

    def calculate_layer_score(self, system: Dict, rule: Dict) -> float:
        """计算系统在该层的得分"""
        total_score = 0.0

        for signal in rule.get("signals", []):
            total_score += self.calculate_signal_score(system, signal)

        return total_score

    def apply_overlay_adjustment(self, system: Dict, layer_scores: Dict) -> Dict:
        """应用Overlay调整"""
        if not self.overlay:
            return layer_scores

        adjusted_scores = layer_scores.copy()

        for adjustment in self.overlay.get("adjustments", []):
            target_layer = adjustment.get("layer")

            # 检查是否满足adjustment条件
            condition_met = False
            for signal in adjustment.get("signals", []):
                if self.calculate_signal_score(system, signal) > 0:
                    condition_met = True
                    break

            if condition_met:
                score_delta = adjustment.get("scoreDelta", 0)
                current_score = adjusted_scores.get(target_layer, 0)

                # 如果overlay定义了一个新层（不在perspective规则中），直接创建
                if target_layer not in adjusted_scores:
                    # 新层需要满足minScore（默认60）
                    # scoreDelta如果足够大（>=60），则创建该层
                    if score_delta >= 60:
                        adjusted_scores[target_layer] = score_delta
                    else:
                        # 否则作为现有层的叠加
                        adjusted_scores[target_layer] = score_delta
                else:
                    # 现有层叠加得分
                    adjusted_scores[target_layer] = current_score + score_delta

        return adjusted_scores

    def assign_layer(self, system: Dict) -> Dict[str, Any]:
        """为系统分配层级"""
        # 计算各层基础得分
        layer_scores = {}
        for rule in self.perspective.get("rules", []):
            layer = rule.get("layer")
            score = self.calculate_layer_score(system, rule)

            # 只记录超过minScore的层
            min_score = rule.get("minScore", 60)
            if score >= min_score:
                layer_scores[layer] = score

        # 应用Overlay调整
        if self.overlay:
            layer_scores = self.apply_overlay_adjustment(system, layer_scores)

        # 选择最高得分层
        if layer_scores:
            best_layer = max(layer_scores, key=layer_scores.get)
            best_score = layer_scores[best_layer]

            # 计算置信度（归一化到0-1）
            # 基准：得分>=150为高置信度(1.0)，得分>=100为中等(0.8)，得分>=60为低(0.7)
            if best_score >= 150:
                confidence = 1.0
            elif best_score >= 100:
                confidence = 0.85
            else:
                confidence = 0.70

            review_needed = confidence < self.perspective.get("reviewThreshold", 0.75)
        else:
            # 使用fallback层
            best_layer = self.perspective.get("fallbackLayer", "未分层")
            best_score = 0
            confidence = 0.5
            review_needed = True

        return {
            "layer": best_layer,
            "score": best_score,
            "confidence": round(confidence, 2),
            "reviewNeeded": review_needed,
            "all_scores": layer_scores  # 可解释：所有候选层的得分
        }

    def assign_layers_batch(self, systems: List[Dict]) -> Dict[str, Dict]:
        """批量分配层级"""
        assignments = {}
        for system in systems:
            system_id = system.get("id")
            assignment = self.assign_layer(system)
            assignments[system_id] = assignment

        return assignments


def load_perspective(perspective_id: str, registry_path: str = "scripts/business_blueprint/strategy_registry/perspectives") -> Dict:
    """加载Perspective配置"""
    perspective_file = Path(registry_path) / f"{perspective_id}.json"

    if not perspective_file.exists():
        # Fallback：使用默认配置
        return create_default_perspective(perspective_id)

    return json.load(open(perspective_file))


def load_overlay(overlay_id: str, registry_path: str = "scripts/business_blueprint/strategy_registry/overlays") -> Dict | None:
    """加载Overlay配置"""
    if not overlay_id:
        return None

    overlay_file = Path(registry_path) / f"{overlay_id}.json"

    if not overlay_file.exists():
        # Fallback：使用默认配置
        return create_default_overlay(overlay_id)

    return json.load(open(overlay_file))


def create_default_perspective(perspective_id: str) -> Dict:
    """创建默认Perspective配置"""
    # 简化版默认配置（Phase 1可用）
    if perspective_id == "product-capability":
        return {
            "strategyId": "product-capability",
            "version": "1.0-default",
            "rules": [
                {
                    "layer": "user-entry",
                    "layerName": "用户接入层",
                    "signals": [
                        {"type": "nameKeyword", "values": ["客户端", "APP", "Portal", "前端"], "weight": 80},
                        {"type": "category", "values": ["frontend", "client"], "weight": 100}
                    ],
                    "minScore": 60
                },
                {
                    "layer": "gateway",
                    "layerName": "服务网关层",
                    "signals": [
                        {"type": "nameKeyword", "values": ["网关", "Gateway", "API网关"], "weight": 80},
                        {"type": "category", "values": ["gateway"], "weight": 100}
                    ],
                    "minScore": 60
                },
                {
                    "layer": "platform-core",
                    "layerName": "平台基础层",
                    "signals": [
                        {"type": "nameKeyword", "values": ["用户中心", "消息中心", "权限中心"], "weight": 80}
                    ],
                    "minScore": 60
                },
                {
                    "layer": "core-business",
                    "layerName": "核心业务层",
                    "signals": [
                        {"type": "nameKeyword", "values": ["服务", "系统"], "weight": 60}
                    ],
                    "minScore": 50
                }
            ],
            "fallbackLayer": "core-business",
            "reviewThreshold": 0.75,
            "conflictPolicy": "highest_score"
        }

    # 其他perspective的默认配置可以类似扩展
    return {
        "strategyId": perspective_id,
        "version": "1.0-default",
        "rules": [],
        "fallbackLayer": "未分层",
        "reviewThreshold": 0.75
    }


def create_default_overlay(overlay_id: str) -> Dict:
    """创建默认Overlay配置"""
    if overlay_id == "finance":
        return {
            "overlayId": "finance",
            "version": "1.0-default",
            "adjustments": [
                {
                    "layer": "risk-control",
                    "layerName": "风险控制层",
                    "signals": [
                        {"type": "nameKeyword", "values": ["风控", "风险评估", "预警", "反欺诈"], "weight": 120}
                    ],
                    "scoreDelta": 30
                },
                {
                    "layer": "regulatory",
                    "layerName": "监管合规层",
                    "signals": [
                        {"type": "nameKeyword", "values": ["合规", "审计", "监管"], "weight": 120}
                    ],
                    "scoreDelta": 40
                }
            ]
        }

    # 其他overlay的默认配置可以类似扩展
    return {
        "overlayId": overlay_id,
        "version": "1.0-default",
        "adjustments": []
    }


if __name__ == "__main__":
    # 测试规则引擎
    perspective = create_default_perspective("product-capability")
    overlay = create_default_overlay("finance")

    engine = RuleEngine(perspective, overlay)

    # 测试系统
    test_systems = [
        {"id": "sys-1", "name": "客户端层", "category": "frontend"},
        {"id": "sys-2", "name": "网关层", "category": "gateway"},
        {"id": "sys-3", "name": "支付风控网关"},
        {"id": "sys-4", "name": "会议服务"}
    ]

    for system in test_systems:
        assignment = engine.assign_layer(system)
        print(f"System: {system['name']}")
        print(f"Layer: {assignment['layer']} (score={assignment['score']}, confidence={assignment['confidence']})")
        print(f"Review needed: {assignment['reviewNeeded']}")
        print()