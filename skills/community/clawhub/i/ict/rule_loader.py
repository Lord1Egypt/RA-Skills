"""
自定义规则加载器
支持从 JSON 文件加载用户自定义检测规则
可与内置规则配合使用
"""
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# 默认自定义规则目录
DEFAULT_RULES_DIR = Path(__file__).parent / "custom_rules"


class RuleLoader:
    """自定义规则加载器"""
    
    def __init__(self, rules_dir: Optional[str] = None):
        self.rules_dir = Path(rules_dir) if rules_dir else DEFAULT_RULES_DIR
        self.rules_dir.mkdir(exist_ok=True)
        self.loaded_rules: List[Dict[str, Any]] = []
    
    def load_from_file(self, filepath: str) -> List[Dict[str, Any]]:
        """从 JSON 文件加载规则"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rules = []
        for rule in data.get('rules', []):
            if self._validate_rule(rule):
                # 转换为与内置规则相同的格式
                rules.append(self._convert_rule_format(rule))
        
        return rules
    
    def _convert_rule_format(self, rule: Dict) -> Tuple:
        """将 JSON 规则转换为内置规则格式 (id, name, patterns, severity)"""
        return (
            rule.get('id', 'custom-rule'),
            rule.get('name', 'Custom Rule'),
            rule.get('patterns', {'all': []}),
            rule.get('severity', 'medium')
        )
    
    def load_from_directory(self, directory: Optional[str] = None) -> List[Tuple]:
        """从目录加载所有规则文件"""
        rules_dir = Path(directory) if directory else self.rules_dir
        all_rules = []
        
        if not rules_dir.exists():
            return all_rules
        
        for json_file in rules_dir.glob("*.json"):
            try:
                rules = self.load_from_file(str(json_file))
                all_rules.extend(rules)
                print(f"✓ 加载 {json_file.name}: {len(rules)} 条规则")
            except Exception as e:
                print(f"✗ 加载 {json_file.name} 失败: {e}")
        
        self.loaded_rules = all_rules
        return all_rules
    
    def _validate_rule(self, rule: Dict[str, Any]) -> bool:
        """验证单条规则"""
        required = ['id', 'name', 'patterns']
        for field in required:
            if field not in rule:
                print(f"✗ 规则缺少必需字段: {field}")
                return False
        
        # 验证正则表达式
        patterns = rule.get('patterns', {})
        for lang, pattern_list in patterns.items():
            for pattern in pattern_list:
                try:
                    re.compile(pattern)
                except re.error as e:
                    print(f"✗ 正则表达式错误 in {rule.get('id')}: {e}")
                    return False
        
        return True
    
    @staticmethod
    def get_builtin_rules_path() -> Path:
        """获取内置规则文件路径"""
        return Path(__file__).parent / "rules.json"
    
    def load_builtin_rules_as_custom(self) -> List[Tuple]:
        """将内置规则加载为自定义规则（用于测试）"""
        json_path = self.get_builtin_rules_path()
        if json_path.exists():
            return self.load_from_file(str(json_path))
        return []


def load_custom_rules(rules_dir: Optional[str] = None) -> List[Tuple]:
    """便捷函数：加载自定义规则
    
    Returns:
        List of (id, name, patterns, severity) tuples
    """
    loader = RuleLoader(rules_dir)
    return loader.load_from_directory()


# 示例用法
if __name__ == "__main__":
    # 测试加载
    loader = RuleLoader()
    
    # 检查是否有内置规则 JSON
    if loader.get_builtin_rules_path().exists():
        rules = loader.load_from_file(str(loader.get_builtin_rules_path()))
        print(f"从内置 JSON 加载: {len(rules)} 条规则")
    else:
        print("无内置规则 JSON 文件")
    
    # 尝试加载自定义规则
    custom_rules = loader.load_from_directory()
    print(f"自定义规则: {len(custom_rules)} 条")
