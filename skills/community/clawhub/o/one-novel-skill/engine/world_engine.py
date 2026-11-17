#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
world_engine.py — 世界观规则引擎 + 三层架构管理

参考：网文创作的系统化工程报告 §2
三层架构：物理层/社会层/叙事层
规则引擎：IF-THEN 约束检查
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

_log = logging.getLogger("world_engine")


class WorldEngine:
    """世界观规则引擎 — 用代码思维管理设定"""

    def __init__(self):
        # 三层架构
        self._layers = {
            "物理层": {},   # 世界基本规则
            "社会层": {},   # 权力/经济/文化结构
            "叙事层": {},   # 当前大事/主线位置
        }
        # 规则引擎: {能力名: {消耗, 限制, 条件}}
        self._rules: Dict[str, Dict] = {}
        # 设定记忆
        self._settings_log: List[str] = []

    # ========== 设定管理 ==========

    def set_setting(self, layer: str, key: str, value: Any):
        """设置世界观设定"""
        if layer in self._layers:
            self._layers[layer][key] = value
            self._settings_log.append(f"[{layer}] {key} = {value}")
            _log.info(f"世界观设定: [{layer}] {key}")

    def get_setting(self, layer: str, key: str) -> Any:
        return self._layers.get(layer, {}).get(key)

    def get_layer_text(self, layer: str) -> str:
        """获取指定层文本（用于注入 Prompt）"""
        data = self._layers.get(layer, {})
        if not data:
            return ""
        lines = [f"=== {layer} ==="]
        for k, v in data.items():
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    def get_all_settings(self) -> str:
        """获取全部设定文本"""
        parts = []
        for layer in ["物理层", "社会层", "叙事层"]:
            text = self.get_layer_text(layer)
            if text:
                parts.append(text)
        return "\n\n".join(parts)

    # ========== 规则引擎 ==========

    def add_rule(self, ability: str, cost: str = "", restrictions: List[str] = None,
                 conditions: str = "", risk: str = ""):
        """添加一条规则：IF 使用能力 THEN 检查约束"""
        self._rules[ability] = {
            "消耗": cost,
            "限制": restrictions or [],
            "条件": conditions,
            "风险": risk,
        }
        _log.info(f"规则注册: {ability} (消耗={cost})")

    def validate_action(self, ability: str, context: Dict = None) -> List[str]:
        """校验某个行为是否符合世界观规则"""
        issues = []
        rule = self._rules.get(ability)
        if not rule:
            return [f"[世界观] 未注册的能力: {ability}，请添加到规则引擎"]

        # 检查限制条件
        restrictions = rule.get("限制", [])
        if context:
            for r in restrictions:
                if r in context.get("environment", ""):
                    issues.append(f"[世界观] {ability} 不能用于 {r} 环境")

        # 检查前提条件
        condition = rule.get("条件", "")
        if condition and context:
            if not context.get("conditions_met", False):
                issues.append(f"[世界观] {ability} 需要条件: {condition}")

        return issues

    def validate_text(self, text: str) -> List[str]:
        """校验文本中是否有违反世界观规则的行为"""
        issues = []
        for ability, rule in self._rules.items():
            if ability in text:
                # 检测限制词
                restrictions = rule.get("限制", [])
                for r in restrictions:
                    if r in text:
                        # 检查能力名和限制词是否在相近位置
                        pos_ability = text.find(ability)
                        pos_restriction = text.find(r)
                        if abs(pos_ability - pos_restriction) < 500:
                            issues.append(
                                f"[世界观] 可能违规：{ability} 附近出现限制词 '{r}'"
                            )
        return issues

    # ========== 金手指代价检查 ==========

    POWER_COST_TYPES = ["资源代价", "时间代价", "道德代价", "命运代价"]

    def add_power(self, name: str, cost_type: str, cost_detail: str):
        """登记金手指及其代价类型"""
        if cost_type not in self.POWER_COST_TYPES:
            cost_type = "资源代价"
        self._rules[f"金手指:{name}"] = {
            "消耗": cost_detail,
            "代价类型": cost_type,
            "限制": [],
            "条件": "",
            "风险": "",
        }

    def analyze_power_balance(self) -> List[str]:
        """分析金手指平衡性"""
        issues = []
        powers = {k: v for k, v in self._rules.items() if k.startswith("金手指:")}
        if not powers:
            return []

        cost_types = set(v.get("代价类型", "") for v in powers.values())
        if len(cost_types) < 2:
            issues.append(f"[世界观] 金手指代价类型单一 ({cost_types})，建议多样化")

        return issues

    # ========== 持久化 ==========

    def to_dict(self) -> dict:
        return {
            "layers": self._layers,
            "rules": self._rules,
            "settings_log": self._settings_log[-100:],
        }

    def load_from_dict(self, data: dict):
        self._layers.update(data.get("layers", {}))
        self._rules.update(data.get("rules", {}))
        self._settings_log = data.get("settings_log", [])

    def reset(self):
        self._layers = {k: {} for k in self._layers}
        self._rules.clear()
        self._settings_log.clear()
