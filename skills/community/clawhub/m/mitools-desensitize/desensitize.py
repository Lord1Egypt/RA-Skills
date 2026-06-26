#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据脱敏工具
支持手机号、身份证、银行卡、邮箱、IP地址、中文姓名等多种敏感信息脱敏
"""

import os
import re
import json
import argparse
from typing import Dict, Any, Optional, Tuple

# 配置文件路径
CONFIG_FILE = os.path.expanduser("~/.workbuddy/skills/mitools-desensitize/desensitize_config.json")

# 默认配置
DEFAULT_CONFIG = {
    "levels": {
        "基础脱敏": ["phone", "idcard", "bankcard", "email", "chinese_name"],
        "高级脱敏": ["ip", "path_user", "digit_sequence", "chinese_field", "wildcard"]
    },
    "wildcard_rules": {
        "dev*23": "dev31",
        "prod*server": "demo-server"
    },
    "custom_rules": []
}

# 全局变量
next_ip_index = 100
BASE_FAKE_IP = "139.1.2."

# 规则注册表
RULES = {}


def register_rule(name: str):
    """规则装饰器"""
    def decorator(func):
        RULES[name] = func
        return func
    return decorator


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        return DEFAULT_CONFIG
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 确保必要字段存在
    if "levels" not in config:
        config["levels"] = DEFAULT_CONFIG["levels"]
    if "wildcard_rules" not in config:
        config["wildcard_rules"] = DEFAULT_CONFIG["wildcard_rules"]
    if "custom_rules" not in config:
        config["custom_rules"] = []
    
    return config


def save_config(config: Dict[str, Any]):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def is_valid_ip(ip: str) -> bool:
    """验证IP地址是否有效"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def get_next_fake_ip() -> str:
    """获取下一个伪IP地址"""
    global next_ip_index
    ip = f"{BASE_FAKE_IP}{next_ip_index}"
    next_ip_index += 1
    return ip


def desensitize_username(name: str, username_mapping: Dict[str, str]) -> str:
    """脱敏用户名"""
    if name in username_mapping:
        return username_mapping[name]
    idx = len(username_mapping) + 1
    fake_name = f"demo{idx:02d}"
    username_mapping[name] = fake_name
    return fake_name


def desensitize_ip(ip: str, ip_mapping: Dict[str, str]) -> str:
    """脱敏IP地址"""
    if ip in ip_mapping:
        return ip_mapping[ip]
    fake_ip = get_next_fake_ip()
    ip_mapping[ip] = fake_ip
    return fake_ip


def apply_wildcard_rules(text: str, rules: Dict[str, str]) -> Tuple[str, Dict[str, str]]:
    """应用通配符规则"""
    local_mapping = {}
    for pattern, replacement in rules.items():
        if '*' in pattern:
            regex_pattern = re.escape(pattern).replace(r'\*', r'.*?')
            compiled = re.compile(regex_pattern)

            def replace_match(m):
                matched_str = m.group(0)
                if matched_str in local_mapping:
                    return local_mapping[matched_str]
                local_mapping[matched_str] = replacement
                return replacement

            text = compiled.sub(replace_match, text)
        else:
            if pattern in text:
                if pattern not in local_mapping:
                    local_mapping[pattern] = replacement
                text = text.replace(pattern, replacement)
    return text, local_mapping


# ======================
# 脱敏规则定义
# ======================

@register_rule("chinese_field")
def rule_chinese_field(text: str, mappings: Dict[str, Any]) -> str:
    """字段名脱敏 - 敏感字段名首字保留，后面用**替代"""
    field_map = {
        "用户": "用**",
        "手机号": "手**",
        "邮箱": "邮**",
        "身份证": "身**",
        "银行卡": "银**",
        "姓名": "姓**",
        "地址": "地**",
        "密码": "密**"
    }
    for field, masked in sorted(field_map.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(field, masked)
    return text


@register_rule("digit_sequence")
def rule_digit_sequence(text: str, mappings: Dict[str, Any]) -> str:
    """长串数字脱敏 - 6位以上连续数字替换为等长伪数字"""
    digit_mapping = mappings.setdefault("digit", {})
    counter = mappings.get("digit_counter", 1)

    def replace_digit(match):
        nonlocal counter
        original = match.group(0)
        digits_only = re.sub(r'\D', '', original)
        if len(digits_only) < 6:
            return original
        if digits_only in digit_mapping:
            fake_digits = digit_mapping[digits_only]
        else:
            fake_digits = str(counter).zfill(len(digits_only))
            digit_mapping[digits_only] = fake_digits
            counter += 1
        return fake_digits

    pattern = r'\b(?:\d[ -]?){5,}\d\b'
    text = re.sub(pattern, replace_digit, text)
    mappings["digit_counter"] = counter
    return text


@register_rule("phone")
def rule_phone(text: str, mappings: Dict[str, Any]) -> str:
    """手机号脱敏 - 保留前3位和后3位"""
    return re.sub(r'\b(1[3-9]\d)(\d{5})(\d{3})\b', r'\1*****\3', text)


@register_rule("idcard")
def rule_idcard(text: str, mappings: Dict[str, Any]) -> str:
    """身份证号脱敏 - 保留前3位和后3位"""
    return re.sub(r'\b(\d{3})\d{12}(\d{3})\b', r'\1******\2', text)


@register_rule("bankcard")
def rule_bankcard(text: str, mappings: Dict[str, Any]) -> str:
    """银行卡脱敏 - 保留前2位"""
    def mask_bank_card(match):
        card = match.group(0)
        digits = re.sub(r'\D', '', card)
        if len(digits) in (16, 19):
            masked_digits = digits[:2] + '**' + '*' * (len(digits) - 4)
            groups = [masked_digits[i:i+4] for i in range(0, len(masked_digits), 4)]
            return ' '.join(groups)
        return card
    return re.sub(r'\b(?:\d{4}[ -]?){3,4}\d{4}\b', mask_bank_card, text)


@register_rule("email")
def rule_email(text: str, mappings: Dict[str, Any]) -> str:
    """邮箱脱敏 - 保留前2位，后面用***替代"""
    def mask_email(match):
        local = match.group(1)
        masked_local = (local[:2] if len(local) >= 2 else local.ljust(2, '*')) + '***'
        return f"{masked_local}@***.com"
    return re.sub(r'\b([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', mask_email, text)


@register_rule("chinese_name")
def rule_chinese_name(text: str, mappings: Dict[str, Any]) -> str:
    """中文姓名脱敏 - 保留姓氏，后面用**替代"""
    def mask_chinese_name(match):
        name = match.group(0)
        return name[0] + '**' if name else '**'
    return re.sub(r'[\u4e00-\u9fa5]{2,4}', mask_chinese_name, text)


@register_rule("path_user")
def rule_path_user(text: str, mappings: Dict[str, Any]) -> str:
    """路径用户名脱敏 - 替换路径中的用户名"""
    def replace_user_in_path(match):
        prefix = match.group(1)
        user = match.group(2)
        path_user_mapping = mappings.setdefault("path_user", {})
        username_mapping = mappings.setdefault("username", {})
        if user in path_user_mapping:
            fake_user = path_user_mapping[user]
        else:
            fake_user = desensitize_username(user, username_mapping)
            path_user_mapping[user] = fake_user
        return prefix + fake_user
    return re.sub(r'(/home/|/users?/|~/)([a-zA-Z][a-zA-Z0-9._-]{1,30})', replace_user_in_path, text, flags=re.IGNORECASE)


@register_rule("ip")
def rule_ip(text: str, mappings: Dict[str, Any]) -> str:
    """IP地址脱敏 - 替换为伪IP地址"""
    ip_mapping = mappings.setdefault("ip", {})
    def replace_ip(match):
        ip = match.group(0)
        if is_valid_ip(ip):
            return desensitize_ip(ip, ip_mapping)
        return ip
    return re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', replace_ip, text)


@register_rule("wildcard")
def rule_wildcard(text: str, mappings: Dict[str, Any]) -> str:
    """通配符规则脱敏"""
    config = load_config()
    wildcard_rules = config.get("wildcard_rules", {})
    text, wc_map = apply_wildcard_rules(text, wildcard_rules)
    mappings.setdefault("wildcard", {}).update(wc_map)
    return text


def register_custom_rules():
    """注册自定义规则"""
    config = load_config()
    for idx, custom in enumerate(config.get("custom_rules", [])):
        rule_name = custom.get("name", f"custom_{idx}")
        pattern = custom.get("pattern", "")
        repl = custom.get("replacement", "")
        if pattern:
            @register_rule(rule_name)
            def custom_rule(text, mappings, p=pattern, r=repl):
                return re.sub(p, r, text)


def desensitize(text: str, level: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
    """
    执行脱敏处理
    
    Args:
        text: 原始文本
        level: 脱敏级别，None表示应用所有规则
        
    Returns:
        (脱敏后文本, 映射表)
    """
    global next_ip_index
    next_ip_index = 100

    mappings = {
        "ip": {},
        "username": {},
        "path_user": {},
        "wildcard": {},
        "digit": {},
        "digit_counter": 1
    }

    config = load_config()
    levels = config.get("levels", DEFAULT_CONFIG["levels"])
    
    # 注册自定义规则
    register_custom_rules()
    
    # 确定要应用的规则
    if level and level in levels:
        rule_names = levels[level]
    else:
        # 应用所有规则
        rule_names = []
        for rules in levels.values():
            rule_names.extend(rules)
    
    # 执行脱敏
    for rule_name in rule_names:
        if rule_name in RULES:
            text = RULES[rule_name](text, mappings)
    
    return text, mappings


def restore(text: str, mapping_json: str) -> str:
    """
    根据映射表还原数据
    
    Args:
        text: 脱敏后的文本
        mapping_json: 映射表JSON字符串
        
    Returns:
        还原后的文本
    """
    try:
        mapping = json.loads(mapping_json)
    except json.JSONDecodeError:
        return "[错误] 映射 JSON 格式无效"

    reverse_map = {}
    for category in ['ip', 'username', 'path_user', 'wildcard', 'digit']:
        if category in mapping:
            for orig, fake in mapping[category].items():
                reverse_map[fake] = orig

    # 按长度降序排序，避免短字符串替换干扰长字符串
    sorted_fakes = sorted(reverse_map.keys(), key=len, reverse=True)
    restored = text
    for fake_val in sorted_fakes:
        orig_val = reverse_map[fake_val]
        restored = restored.replace(fake_val, orig_val)

    return restored


def list_rules() -> str:
    """列出所有支持的脱敏规则"""
    config = load_config()
    levels = config.get("levels", DEFAULT_CONFIG["levels"])
    
    output = []
    output.append("\n📋 支持的脱敏规则\n")
    output.append("=" * 60)
    
    rule_descriptions = {
        "phone": "手机号脱敏 (13812345678 → 138*****678)",
        "idcard": "身份证号脱敏 (110101199001011234 → 110******234)",
        "bankcard": "银行卡脱敏 (6222021234567890123 → 62** **** **** **** ***)",
        "email": "邮箱脱敏 (zhangsan@example.com → zh***@***.com)",
        "chinese_name": "中文姓名脱敏 (张三 → 张**)",
        "ip": "IP地址脱敏 (192.168.1.1 → 139.1.2.100)",
        "path_user": "路径用户名脱敏 (/home/zhangsan → /home/demo01)",
        "digit_sequence": "长串数字脱敏 (1234567890 → 0000000001)",
        "chinese_field": "字段名脱敏 (手机号 → 手**)",
        "wildcard": "通配符规则 (dev*23 → dev31)"
    }
    
    for level_name, rules in levels.items():
        output.append(f"\n【{level_name}】")
        for rule in rules:
            desc = rule_descriptions.get(rule, rule)
            output.append(f"  • {desc}")
    
    output.append("\n" + "=" * 60)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description='数据脱敏工具')
    parser.add_argument('action', choices=['desensitize', 'restore', 'list', 'file'],
                       help='操作类型: desensitize(脱敏), restore(还原), list(列出规则), file(文件脱敏)')
    parser.add_argument('--text', '-t', help='要处理的文本')
    parser.add_argument('--file', '-f', help='要处理的文件路径')
    parser.add_argument('--mapping', '-m', help='映射表JSON字符串（还原时使用）')
    parser.add_argument('--level', '-l', help='脱敏级别')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        print(list_rules())
    
    elif args.action == 'desensitize':
        if not args.text:
            print("❌ 错误: 请提供 --text 参数")
            return
        result, mapping = desensitize(args.text, args.level)
        print("\n📝 脱敏结果:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        print("\n📊 映射表:")
        print(json.dumps(mapping, indent=2, ensure_ascii=False))
    
    elif args.action == 'restore':
        if not args.text or not args.mapping:
            print("❌ 错误: 请提供 --text 和 --mapping 参数")
            return
        result = restore(args.text, args.mapping)
        print("\n📝 还原结果:")
        print("-" * 60)
        print(result)
        print("-" * 60)
    
    elif args.action == 'file':
        if not args.file:
            print("❌ 错误: 请提供 --file 参数")
            return
        
        if not os.path.exists(args.file):
            print(f"❌ 错误: 文件不存在: {args.file}")
            return
        
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result, mapping = desensitize(content, args.level)
        
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ 脱敏结果已保存到: {args.output}")
        else:
            print("\n📝 脱敏结果:")
            print("-" * 60)
            print(result[:2000] + "..." if len(result) > 2000 else result)
            print("-" * 60)
        
        # 保存映射表
        mapping_file = args.output + ".mapping.json" if args.output else args.file + ".mapping.json"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        print(f"📊 映射表已保存到: {mapping_file}")


if __name__ == '__main__':
    main()
