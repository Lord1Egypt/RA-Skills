#!/usr/bin/env python3
"""
细粒度权限管理系统
参考 Claude Code 的 ToolPermissionContext 设计

目标：减少日常确认，只在真正危险操作时询问

权限类型：
- read      — 读文件/数据
- write     — 写/创建文件
- execute   — 执行命令
- network   — 网络访问
- elevated  — 提升权限

规则：
- alwaysAllow  — 自动放行
- alwaysAsk    — 每次询问
- alwaysDeny  — 直接拒绝

配置文件：~/.openclaw/bw-openclaw-boost/tools-permissions.json
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum

PERMISSIONS_FILE = Path.home() / ".openclaw" / "bw-openclaw-boost" / "tools-permissions.json"

PermissionType = Literal["read", "write", "execute", "network", "elevated"]
PermissionMode = Literal["alwaysAllow", "alwaysAsk", "alwaysDeny"]
RuleEffect = Literal["allow", "ask", "deny"]


@dataclass
class ToolPermission:
    """工具权限声明"""
    tool: str
    permissions: List[PermissionType]
    description: str
    safe_commands: List[str] = field(default_factory=list)  # 安全命令白名单
    dangerous_patterns: List[str] = field(default_factory=list)  # 危险模式


@dataclass
class PermissionRule:
    """权限规则"""
    effect: RuleEffect
    tool: Optional[str] = None
    permission: Optional[PermissionType] = None
    command_pattern: Optional[str] = None  # e.g. "rm -rf", "drop table"
    file_pattern: Optional[str] = None  # e.g. "*.log", "/system/**"


# 谷宝常用工具的权限声明
DEFAULT_TOOL_PERMISSIONS: List[ToolPermission] = [
    ToolPermission(
        tool="exec",
        permissions=["execute", "network"],
        description="执行 shell 命令",
        safe_commands=[
            "ls", "pwd", "echo", "cat", "head", "tail", "grep", "rg",
            "find", "wc", "cut", "tr", "sort", "uniq", "jq",
            "git status", "git log", "git diff", "git show",
            "python3 -c", "python3 -m",
            "curl -s", "curl -X GET", "wget -q",
            "openclaw status", "openclaw cron list",
            "date", "whoami", "hostname",
        ],
        dangerous_patterns=[
            r"rm\s+-rf\s+/",  # 格式化系统
            r"rm\s+-rf\s+\*",  # 递归删除当前目录
            r"dd\s+if=.*of=/dev/",  # 直接写磁盘
            r":\(\)\{.*:\|:&\};:",  # Fork bomb
            r"curl.*\|.*sh",  # Piped curl execution
            r"wget.*\|.*sh",  # Piped wget execution
            r"shutdown",  # 关机
            r"reboot",  # 重启
            r"mkfs",  # 格式化
            r"dd.*bs=",  # 直接块设备写入
        ]
    ),
    ToolPermission(
        tool="read",
        permissions=["read"],
        description="读取文件",
        safe_commands=["*"],
        dangerous_patterns=[]
    ),
    ToolPermission(
        tool="write",
        permissions=["write"],
        description="写入文件",
        safe_commands=["*.md", "*.txt", "*.json", "*.py", "*.js", "*.sh"],
        dangerous_patterns=[
            r"\/etc\/passwd",  # 系统配置文件
            r"\/system\/",  # 系统目录
            r"\.ssh\/",  # SSH 配置
            r"\.aws\/",  # AWS 配置
        ]
    ),
    ToolPermission(
        tool="web_search",
        permissions=["network"],
        description="网络搜索",
        safe_commands=["*"],
        dangerous_patterns=[]
    ),
    ToolPermission(
        tool="web_fetch",
        permissions=["network", "read"],
        description="抓取网页",
        safe_commands=["https://*", "http://*"],
        dangerous_patterns=[]
    ),
]


def load_permissions() -> Dict:
    """加载权限配置"""
    if PERMISSIONS_FILE.exists():
        try:
            return json.loads(PERMISSIONS_FILE.read_text())
        except:
            pass
    return {"rules": [], "tool_permissions": {}}


def save_permissions(perms: Dict):
    """保存权限配置"""
    PERMISSIONS_FILE.write_text(json.dumps(perms, indent=2, ensure_ascii=False))


def get_tool_permissions() -> Dict[str, ToolPermission]:
    """获取工具权限声明映射"""
    perms = load_permissions()
    result = {}
    
    # 加载默认工具权限
    for tp in DEFAULT_TOOL_PERMISSIONS:
        result[tp.tool] = tp
    
    # 覆盖用户自定义
    for tool, custom in perms.get("tool_permissions", {}).items():
        if tool in result:
            # 合并
            existing = result[tool]
            if "safe_commands" in custom:
                existing.safe_commands = custom["safe_commands"]
            if "dangerous_patterns" in custom:
                existing.dangerous_patterns = custom["dangerous_patterns"]
        else:
            result[tool] = ToolPermission(
                tool=tool,
                permissions=custom.get("permissions", ["execute"]),
                description=custom.get("description", ""),
                safe_commands=custom.get("safe_commands", []),
                dangerous_patterns=custom.get("dangerous_patterns", [])
            )
    
    return result


def check_command_safety(command: str, tool_perm: ToolPermission) -> RuleEffect:
    """
    检查命令安全性
    返回: "allow" | "ask" | "deny"
    """
    # 检查危险模式
    for pattern in tool_perm.dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return "deny"
    
    # 检查安全命令白名单
    for safe in tool_perm.safe_commands:
        if safe == "*":
            return "allow"
        if safe in command:
            return "allow"
    
    # 默认需要询问
    return "ask"


def check_rule_match(rule: Dict, tool: str, command: str, context: Dict) -> bool:
    """检查规则是否匹配当前调用"""
    if rule.get("tool") and rule["tool"] != tool:
        return False
    
    if rule.get("command_pattern"):
        pattern = rule["command_pattern"]
        if not re.search(pattern, command, re.IGNORECASE):
            return False
    
    if rule.get("file_pattern"):
        pattern = rule["file_pattern"]
        file_path = context.get("file", "")
        if not re.search(pattern, file_path):
            return False
    
    return True


def evaluate_permission(
    tool: str,
    command: str = "",
    context: Dict = {}
) -> RuleEffect:
    """
    评估权限请求
    返回: "allow" | "ask" | "deny"
    """
    perms = load_permissions()
    tool_perms = get_tool_permissions()
    
    # 获取该工具的权限声明
    tool_perm = tool_perms.get(tool)
    
    # 1. 先检查危险模式
    if tool_perm and command:
        safety = check_command_safety(command, tool_perm)
        if safety == "deny":
            return "deny"
    
    # 2. 检查用户自定义规则（按优先级）
    rules = perms.get("rules", [])
    for rule in rules:
        if check_rule_match(rule, tool, command, context):
            effect = rule.get("effect", "ask")
            return effect
    
    # 3. 如果工具声明安全命令且命令匹配，直接放行
    if tool_perm and command:
        safety = check_command_safety(command, tool_perm)
        if safety == "allow":
            return "allow"
    
    # 4. 默认询问
    return "ask"


def add_rule(
    effect: RuleEffect,
    tool: Optional[str] = None,
    command_pattern: Optional[str] = None,
    file_pattern: Optional[str] = None,
    description: str = ""
):
    """添加权限规则"""
    perms = load_permissions()
    
    rule = {"effect": effect}
    if tool:
        rule["tool"] = tool
    if command_pattern:
        rule["command_pattern"] = command_pattern
    if file_pattern:
        rule["file_pattern"] = file_pattern
    if description:
        rule["description"] = description
    
    perms["rules"].append(rule)
    save_permissions(perms)
    return rule


def remove_rule(index: int):
    """删除规则"""
    perms = load_permissions()
    if 0 <= index < len(perms["rules"]):
        perms["rules"].pop(index)
        save_permissions(perms)


def list_rules() -> List[Dict]:
    """列出所有规则"""
    perms = load_permissions()
    return perms.get("rules", [])


def get_safe_commands(tool: str) -> List[str]:
    """获取工具的安全命令白名单"""
    tool_perms = get_tool_permissions()
    tp = tool_perms.get(tool)
    return tp.safe_commands if tp else []


def format_rule_description(rule: Dict, index: int) -> str:
    """格式化规则描述"""
    effect = rule.get("effect", "ask")
    effect_emoji = {"allow": "✅", "ask": "❓", "deny": "🚫"}[effect]
    
    parts = []
    if rule.get("tool"):
        parts.append(f"工具={rule['tool']}")
    if rule.get("command_pattern"):
        parts.append(f"命令={rule['command_pattern']}")
    if rule.get("file_pattern"):
        parts.append(f"文件={rule['file_pattern']}")
    if rule.get("description"):
        parts.append(rule['description'])
    
    return f"{index}. [{effect_emoji} {effect.upper()}] {' | '.join(parts)}"


def setup_default_permissions():
    """设置谷宝的默认权限规则"""
    perms = {
        "rules": [
            # 读文件全部放行
            {
                "effect": "allow",
                "tool": "read",
                "description": "读文件自动放行"
            },
            # 安全命令放行
            {
                "effect": "allow",
                "tool": "exec",
                "command_pattern": r"^(ls|pwd|echo|cat|head|tail|grep|rg|find|wc|cut|tr|sort|uniq)\s",
                "description": "常见只读命令"
            },
            {
                "effect": "allow",
                "tool": "exec",
                "command_pattern": r"^git\s+(status|log|diff|show|branch)(?:\s|$)",
                "description": "Git 只读操作"
            },
            {
                "effect": "allow",
                "tool": "exec",
                "command_pattern": r"^(python3|node)\s+(-c|-m)\s+['\"]",
                "description": "Python/Node 安全单行命令"
            },
            {
                "effect": "allow",
                "tool": "exec",
                "command_pattern": r"^curl\s+-s\s+",
                "description": "Curl 只读请求"
            },
            {
                "effect": "allow",
                "tool": "exec",
                "command_pattern": r"^openclaw\s+(status|cron\s+list)",
                "description": "OpenClaw 只读命令"
            },
            {
                "effect": "allow",
                "tool": "exec",
                "command_pattern": r"^(date|whoami|hostname|id|uname)",
                "description": "系统信息命令"
            },
            # 危险命令拒绝
            {
                "effect": "deny",
                "tool": "exec",
                "command_pattern": r"rm\s+-rf",
                "description": "递归删除高危"
            },
            {
                "effect": "deny",
                "tool": "exec",
                "command_pattern": r"dd\s+.*bs=",
                "description": "直接块设备写入"
            },
            {
                "effect": "deny",
                "tool": "exec",
                "command_pattern": r":\(\)\{.*:\|:&\};:",
                "description": "Fork bomb"
            },
            # 写文件询问
            {
                "effect": "ask",
                "tool": "write",
                "description": "写文件默认询问"
            },
            # 网络操作询问
            {
                "effect": "ask",
                "tool": "web_search",
                "description": "网络搜索询问"
            },
            {
                "effect": "ask",
                "tool": "web_fetch",
                "description": "网页抓取询问"
            },
            # 未知 exec 命令询问
            {
                "effect": "ask",
                "tool": "exec",
                "description": "其他 exec 默认询问"
            },
        ],
        "tool_permissions": {}
    }
    
    save_permissions(perms)
    return perms


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("细粒度权限管理系统")
        print("")
        print("用法:")
        print("  permission_manager.py setup          # 设置默认规则")
        print("  permission_manager.py list           # 列出所有规则")
        print("  permission_manager.py check <tool> [command]  # 检查权限")
        print("  permission_manager.py add allow|ask|deny <规则>  # 添加规则")
        print("  permission_manager.py remove <index>  # 删除规则")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "setup":
        setup_default_permissions()
        print("✅ 默认权限规则已设置")
        print("")
        print("规则列表:")
        for i, rule in enumerate(list_rules()):
            print(format_rule_description(rule, i))
    
    elif cmd == "list":
        rules = list_rules()
        print(f"当前 {len(rules)} 条规则:\n")
        for i, rule in enumerate(rules):
            print(format_rule_description(rule, i))
    
    elif cmd == "check" and len(sys.argv) >= 3:
        tool = sys.argv[2]
        command = sys.argv[3] if len(sys.argv) > 3 else ""
        result = evaluate_permission(tool, command)
        effect_emoji = {"allow": "✅", "ask": "❓", "deny": "🚫"}[result]
        print(f"{effect_emoji} {result.upper()}")
    
    elif cmd == "add" and len(sys.argv) >= 4:
        effect = sys.argv[2]
        if effect not in ["allow", "ask", "deny"]:
            print("效果必须是: allow, ask, deny")
            sys.exit(1)
        
        rule_str = " ".join(sys.argv[3:])
        # 简单解析: tool=xxx command=xxx
        rule = {"effect": effect}
        if "tool=" in rule_str:
            import re
            m = re.search(r'tool=(\S+)', rule_str)
            if m:
                rule["tool"] = m.group(1)
        if "command=" in rule_str:
            m = re.search(r'command=(\S+)', rule_str)
            if m:
                rule["command_pattern"] = m.group(1)
        
        add_rule(**rule)
        print(f"✅ 已添加规则: {rule}")
    
    elif cmd == "remove" and len(sys.argv) >= 3:
        try:
            idx = int(sys.argv[2])
            remove_rule(idx)
            print(f"✅ 已删除规则 {idx}")
        except:
            print("无效的规则索引")
    
    else:
        print("未知命令")
        sys.exit(1)
