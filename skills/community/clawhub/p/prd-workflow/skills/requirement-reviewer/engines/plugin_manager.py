#!/usr/bin/env python3
"""
插件管理器 v1.0

支持按场景加载评审器插件
"""

import os
import sys
from typing import Dict, List, Optional
from importlib import import_module


# 预定义场景配置
SCENARIOS = {
    "default": {
        "name": "默认场景",
        "description": "通用场景，仅加载核心评审器",
        "plugins": ["core"],
        "checkers": [
            "completeness",
            "consistency",
            "terminology",
            "acceptance_criteria"
        ]
    },
    "financial": {
        "name": "金融场景",
        "description": "金融行业场景，加载核心 + 金融插件",
        "plugins": ["core", "financial"],
        "checkers": [
            # 核心评审器
            "completeness",
            "consistency",
            "terminology",
            "acceptance_criteria",
            # 金融插件评审器
            "compliance",
            "business_rules",
            "edge_cases",
            "risk"
        ]
    },
    "internet": {
        "name": "互联网场景",
        "description": "互联网产品场景，加载核心 + 互联网插件",
        "plugins": ["core"],
        "checkers": [
            "completeness",
            "consistency",
            "terminology",
            "acceptance_criteria"
            # 互联网插件评审器（待扩展）
        ]
    }
}


class PluginManager:
    """插件管理器"""

    def __init__(self, base_path: str = None):
        """
        初始化插件管理器

        参数:
            base_path: 插件基础路径，默认为 engines 目录
        """
        self.base_path = base_path or os.path.dirname(__file__)
        self.loaded_plugins = {}
        self.checkers = {}

    def load_scenario(self, scenario: str) -> Dict[str, object]:
        """
        加载场景所需的评审器

        参数:
            scenario: 场景名称 (default/financial/internet)

        返回:
            评审器实例字典
        """
        if scenario not in SCENARIOS:
            print(f"⚠️  未知场景：{scenario}，使用 default 场景")
            scenario = "default"

        scenario_config = SCENARIOS[scenario]
        print(f"📦 加载场景：{scenario_config['name']}")
        print(f"   描述：{scenario_config['description']}")
        print(f"   插件：{scenario_config['plugins']}")

        # 加载插件
        for plugin_name in scenario_config["plugins"]:
            self._load_plugin(plugin_name)

        # 实例化评审器
        self._instantiate_checkers(scenario_config["checkers"])

        return self.checkers

    def load_custom(self, checkers: List[str]) -> Dict[str, object]:
        """
        自定义加载评审器

        参数:
            checkers: 评审器名称列表

        返回:
            评审器实例字典
        """
        # 分析每个评审器属于哪个插件
        plugin_map = self._analyze_checkers(checkers)

        # 加载所需插件
        for plugin_name in plugin_map.keys():
            self._load_plugin(plugin_name)

        # 实例化评审器
        self._instantiate_checkers(checkers)

        return self.checkers

    def _load_plugin(self, plugin_name: str) -> None:
        """加载插件"""
        if plugin_name in self.loaded_plugins:
            return

        # 构建插件路径
        if plugin_name == "core":
            plugin_path = f"{self.base_path}.core"
        else:
            plugin_path = f"{self.base_path}.plugins.{plugin_name}"

        try:
            # 尝试使用绝对导入
            plugin = import_module(plugin_path)
            self.loaded_plugins[plugin_name] = plugin
            print(f"   ✅ 插件已加载：{plugin_name}")
        except ImportError:
            try:
                # 回退到相对导入
                if plugin_name == "core":
                    plugin_path = "core"
                else:
                    plugin_path = f"plugins.{plugin_name}"
                plugin = import_module(plugin_path)
                self.loaded_plugins[plugin_name] = plugin
                print(f"   ✅ 插件已加载：{plugin_name}")
            except ImportError as e:
                print(f"   ❌ 插件加载失败：{plugin_name} - {e}")

    def _analyze_checkers(self, checkers: List[str]) -> Dict[str, List[str]]:
        """
        分析评审器属于哪个插件

        返回:
            {plugin_name: [checker_names]}
        """
        # 核心评审器
        core_checkers = ["completeness", "consistency", "terminology", "acceptance_criteria"]

        # 金融插件评审器
        financial_checkers = ["compliance", "business_rules", "edge_cases", "risk"]

        plugin_map = {"core": [], "financial": []}

        for checker in checkers:
            if checker in core_checkers:
                plugin_map["core"].append(checker)
            elif checker in financial_checkers:
                plugin_map["financial"].append(checker)
            else:
                # 未知评审器，尝试在 core 中查找
                plugin_map["core"].append(checker)

        # 过滤空列表
        return {k: v for k, v in plugin_map.items() if v}

    def _instantiate_checkers(self, checker_names: List[str]) -> None:
        """实例化评审器"""
        checker_mapping = {
            # 核心评审器
            "completeness": ("core", "CompletenessChecker"),
            "consistency": ("core", "ConsistencyChecker"),
            "terminology": ("core", "TerminologyChecker"),
            "acceptance_criteria": ("core", "AcceptanceCriteriaChecker"),
            # 金融插件评审器
            "compliance": ("financial", "ComplianceChecker"),
            "business_rules": ("financial", "BusinessRuleChecker"),
            "edge_cases": ("financial", "EdgeCaseChecker"),
            "risk": ("financial", "RiskChecker")
        }

        for checker_name in checker_names:
            if checker_name not in checker_mapping:
                print(f"   ⚠️  未知评审器：{checker_name}，跳过")
                continue

            plugin_name, class_name = checker_mapping[checker_name]

            if plugin_name not in self.loaded_plugins:
                print(f"   ⚠️  插件未加载：{plugin_name}，跳过 {checker_name}")
                continue

            try:
                plugin = self.loaded_plugins[plugin_name]
                checker_class = getattr(plugin, class_name)
                self.checkers[checker_name] = checker_class()
                print(f"   ✅ 评审器已加载：{checker_name}")
            except AttributeError as e:
                print(f"   ❌ 评审器实例化失败：{checker_name} - {e}")

    def get_checker(self, name: str) -> Optional[object]:
        """获取单个评审器"""
        return self.checkers.get(name)

    def list_available_scenarios(self) -> List[Dict]:
        """列出可用场景"""
        return [
            {
                "name": name,
                "info": info
            }
            for name, info in SCENARIOS.items()
        ]

    def list_loaded_checkers(self) -> List[str]:
        """列出已加载的评审器"""
        return list(self.checkers.keys())


# 测试
if __name__ == "__main__":
    print("=" * 60)
    print("插件管理器测试")
    print("=" * 60)

    # 测试 default 场景
    print("\n【测试 1】Default 场景")
    manager = PluginManager("requirement-reviewer.engines")
    checkers = manager.load_scenario("default")
    print(f"已加载评审器：{manager.list_loaded_checkers()}")

    # 测试 financial 场景
    print("\n【测试 2】Financial 场景")
    manager2 = PluginManager("requirement-reviewer.engines")
    checkers2 = manager2.load_scenario("financial")
    print(f"已加载评审器：{manager2.list_loaded_checkers()}")

    # 测试自定义加载
    print("\n【测试 3】自定义加载")
    manager3 = PluginManager("requirement-reviewer.engines")
    checkers3 = manager3.load_custom(["completeness", "consistency", "compliance"])
    print(f"已加载评审器：{manager3.list_loaded_checkers()}")

    # 列出可用场景
    print("\n【测试 4】可用场景列表")
    for scenario in manager.list_available_scenarios():
        print(f"  - {scenario['name']}: {scenario['info']['description']}")