# ============ 安全检测规则配置 ============
# 从 rules.json 加载检测规则
# 避免在源代码中直接写敏感模式字符串

import json
import os
from pathlib import Path

RULES_DIR = Path(__file__).parent
RULES_JSON = RULES_DIR / "rules.json"

def load_rules_from_json():
    """从 JSON 文件加载规则"""
    try:
        with open(RULES_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: {RULES_JSON} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing {RULES_JSON}: {e}")
        return None

RULES_DATA = load_rules_from_json()

if RULES_DATA:
    VERSION = RULES_DATA.get('version', '4.0.8')
    
    # 从 JSON 构建 SECURITY_CHECKS 列表
    SECURITY_CHECKS = []
    for rule in RULES_DATA.get('rules', []):
        rule_id = rule['id']
        rule_name = rule['name']
        patterns = rule.get('patterns', {})
        severity = rule.get('severity', 'medium')
        SECURITY_CHECKS.append((rule_id, rule_name, patterns, severity))
    
    # 从 JSON 加载其他配置
    NET_PATTERNS = RULES_DATA.get('net_patterns', {})
    FALSE_POSITIVE_PATTERNS = set(RULES_DATA.get('false_positive_patterns', []))
    REQUIRED_SKILL_SECTIONS = RULES_DATA.get('required_skill_sections', [])
    AUDITOR_FILES = RULES_DATA.get('auditor_files', [])
    SUPPORTED_LANGUAGES = RULES_DATA.get('supported_languages', {})
    
    print(f"✓ Loaded {len(SECURITY_CHECKS)} rules from rules.json")
else:
    raise RuntimeError("Failed to load rules.json")
