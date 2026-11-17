#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
intercept_matrix.py — 配置修改拦截矩阵
======================================

功能:
- 定义哪些配置文件 + 哪些操作 = 需要触发校验
- 动作类型 × 风险等级 → 触发校验级别

使用:
  from intercept_matrix import should_intercept, get_check_level
"""

import os
import os as _os
import fnmatch
from pathlib import Path

_OPENCLAW_JSON = _os.path.expanduser("~/.openclaw/openclaw.json")

# 配置文件路径模式 → 风险等级
CONFIG_RISK_LEVELS = {
    # 主配置层 (一级)
    "openclaw.json": {
        "critical": ["agents", "models", "providers", "security"],
        "medium": ["channels", "plugins", "cron"],
        "low": ["logging", "ui"],
        "path": str(Path.home() / ".openclaw/openclaw.json")
    },
    
    # 子代理配置层 (二级) - 使用 glob 模式
    "agents/*/models.json": {
        "critical": ["model", "provider"],
        "medium": ["timeout"],
        "low": [],
        "pattern": "agents/*/models.json"
    },
    "agents/*/config.json": {
        "critical": ["apiKeys", "credentials"],
        "medium": ["timeout", "retries"],
        "low": [],
        "pattern": "agents/*/config.json"
    },
}

# 敏感路径白名单
SENSITIVE_PATTERNS = [
    _OPENCLAW_JSON.lower(),
    _OPENCLAW_JSON,
    "**/agents/*/models.json",
    "**/agents/*/config.json",
    "**/agents/*/settings.json",
]

# 动作类型 → 触发级别映射
ACTION_TRIGGERS = {
    "edit": {
        "critical": "full",      # snapshot + verify + diff
        "medium": "verify",     # 只验证
        "low": "check"         # 只检查一致性
    },
    "write": {
        "critical": "full",
        "medium": "snapshot",  # 创建快照
        "low": "check"
    },
    "delete": {
        "critical": "full",
        "medium": "full",
        "low": "verify"
    },
    "config.patch": "full-cycle",    # 等同于 full
    "config.apply": "full-cycle",
    "gateway.restart": "verify",
}


def get_risk_level(config_path: str) -> tuple[str, dict]:
    """
    获取配置文件的风险等级
    
    Returns:
        (risk_level, config_info) - ('critical'/'medium'/'low', 配置信息)
    """
    config_path = os.path.abspath(config_path)
    
    for name, info in CONFIG_RISK_LEVELS.items():
        # 精确匹配
        if info.get("path") == config_path:
            return ("critical", info)
        
        # Glob 模式匹配
        if "pattern" in info:
            if fnmatch.fnmatch(config_path, info["pattern"]) or \
               fnmatch.fnmatch(config_path, f"*/{info['pattern']}"):
                return ("critical", info)  # 子代理配置默认 critical
    
    # 默认风险等级
    return ("low", {"critical": [], "medium": [], "low": []})


def should_intercept(action: str, config_path: str) -> bool:
    """
    判断是否需要拦截该操作
    
    Args:
        action: 操作类型 (edit/write/delete/config.patch/config.apply)
        config_path: 配置文件路径
    
    Returns:
        True if should intercept
    """
    risk_level, _ = get_risk_level(config_path)
    
    if risk_level == "critical":
        return True
    if risk_level == "medium" and action in ["edit", "write", "delete"]:
        return True
    if risk_level == "low" and action in ["delete"]:
        return True
    
    return False


def get_check_level(action: str, config_path: str) -> str:
    """
    获取需要执行的校验级别
    
    Returns:
        'full' - snapshot + verify + diff
        'verify' - 只验证 (JSON 语法 + 一致性)
        'check' - 只检查一致性
        'snapshot' - 只创建快照
    """
    risk_level, _ = get_risk_level(config_path)
    
    triggers = ACTION_TRIGGERS.get(action, "check")
    
    if isinstance(triggers, str):
        return triggers  # 直接返回级别名
    
    return triggers.get(risk_level, "check")


def is_sensitive_path(path: str) -> bool:
    """判断是否为敏感路径"""
    abs_path = os.path.abspath(path)
    for pattern in SENSITIVE_PATTERNS:
        if fnmatch.fnmatch(abs_path, pattern) or \
           fnmatch.fnmatch(abs_path, f"*{pattern}*"):
            return True
    return False


def get_intercept_details(action: str, config_path: str) -> dict:
    """
    获取拦截详情，用于日志和决策
    
    Returns:
        {
            'should_intercept': bool,
            'check_level': str,
            'risk_level': str,
            'is_sensitive': bool,
            'reason': str
        }
    """
    risk_level, config_info = get_risk_level(config_path)
    should_int = should_intercept(action, config_path)
    check_lvl = get_check_level(action, config_path) if should_int else "none"
    sensitive = is_sensitive_path(config_path)
    
    return {
        "should_intercept": should_int,
        "check_level": check_lvl,
        "risk_level": risk_level,
        "is_sensitive": sensitive,
        "reason": f"{action} on {risk_level} risk config" if should_int else "no intercept needed",
        "critical_keys": config_info.get("critical", []),
    }


# CLI 接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: intercept_matrix.py <action> <config_path>")
        print("  action: edit/write/delete/config.patch/config.apply")
        print("  config_path: path to config file")
        sys.exit(1)
    
    action = sys.argv[1]
    config_path = sys.argv[2]
    
    details = get_intercept_details(action, config_path)
    import json
    print(json.dumps(details, indent=2))
