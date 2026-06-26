"""
安全模块 - 提供认证、授权、沙箱、日志等安全功能
支持三种安全模式：宽松模式、标准模式、严格模式
"""
import os
import re
import json
import hashlib
from typing import Optional, List, Dict, Any
from functools import wraps
from datetime import datetime


class SecurityMode:
    """安全模式枚举"""
    DISABLED = "disabled"    # 禁用所有安全功能
    RELAXED = "relaxed"     # 宽松模式 - 仅认证
    STANDARD = "standard"     # 标准模式 - 认证 + 基本沙箱
    STRICT = "strict"        # 严格模式 - 完整限制


class SecurityConfig:
    """安全配置类"""

    PRESETS = {
        SecurityMode.RELAXED: {
            "description": "宽松模式 - 仅启用 API 认证，基本不限制功能",
            "shell_whitelist_mode": False,
            "shell_blocked_commands": ["format", "shutdown", "restart"],
            "shell_blocked_patterns": [],
            "file_sandbox_enabled": False,
            "file_blocked_dirs": [],
            "file_blocked_patterns": [],
            "process_protection_enabled": False,
        },
        SecurityMode.STANDARD: {
            "description": "标准模式 - 认证 + 基本沙箱保护",
            "shell_whitelist_mode": True,
            "shell_blocked_commands": ["del", "rm", "rmdir", "format", "shutdown", "restart",
                                        "net user", "net localgroup", "reg add", "reg delete",
                                        "taskkill", "kill -9", "curl -o", "wget"],
            "shell_blocked_patterns": [r"rm\s+-rf", r"del\s+/[fq]", r"format\s+"],
            "file_sandbox_enabled": True,
            "file_blocked_dirs": ["/Windows", "/Program Files", "/Program Files (x86)",
                                   "/$Recycle.Bin", "/System Volume Information"],
            "file_blocked_patterns": [r"\.\./", r"\.exe$", r"\.dll$"],
            "process_protection_enabled": True,
        },
        SecurityMode.STRICT: {
            "description": "严格模式 - 完整安全限制",
            "shell_whitelist_mode": True,
            "shell_blocked_commands": ["del", "rm", "rmdir", "format", "shutdown", "restart",
                                        "net user", "net localgroup", "reg add", "reg delete",
                                        "taskkill", "kill -9", "curl -o", "wget", "invoke-webrequest",
                                        "invoke-restmethod", "iex", "iwr", "downloadstring"],
            "shell_blocked_patterns": [r"rm\s+-rf", r"del\s+/[fq]", r"format\s+",
                                       r"\|.*iex", r"powershell.*-enc"],
            "file_sandbox_enabled": True,
            "file_allowed_dirs": [],
            "file_blocked_dirs": ["/Windows", "/Program Files", "/Program Files (x86)",
                                   "/$Recycle.Bin", "/System Volume Information",
                                   "/Users/Public", "/PerfLogs"],
            "file_blocked_patterns": [r"\.\./", r"\.exe$", r"\.dll$", r"\.bat$", r"\.cmd$",
                                        r"\.ps1$", r"\.sh$", r"\.vbs$", r"\.js$", r"\.msi$"],
            "process_protection_enabled": True,
        }
    }

    def __init__(self):
        self.mode: str = SecurityMode.DISABLED
        self.api_key: Optional[str] = None
        self.api_key_hash: Optional[str] = None

        self.shell_whitelist_mode: bool = False
        self.shell_allowed_commands: List[str] = []
        self.shell_blocked_commands: List[str] = []
        self.shell_blocked_patterns: List[str] = []

        self.file_sandbox_enabled: bool = False
        self.file_allowed_dirs: List[str] = []
        self.file_blocked_dirs: List[str] = []
        self.file_blocked_patterns: List[str] = []

        self.process_protection_enabled: bool = False

        self.log_enabled: bool = True
        self.log_file: str = "security.log"
        self.log_sensitive: bool = False

    def apply_preset(self, mode: str):
        """应用安全模式预设"""
        if mode == SecurityMode.DISABLED:
            self.mode = SecurityMode.DISABLED
            return

        if mode not in self.PRESETS:
            raise ValueError(f"未知的安全模式: {mode}")

        self.mode = mode
        preset = self.PRESETS[mode]

        self.shell_whitelist_mode = preset["shell_whitelist_mode"]
        self.shell_blocked_commands = preset["shell_blocked_commands"].copy()
        self.shell_blocked_patterns = preset["shell_blocked_patterns"].copy()

        self.file_sandbox_enabled = preset["file_sandbox_enabled"]
        self.file_blocked_dirs = preset["file_blocked_dirs"].copy()
        self.file_blocked_patterns = preset["file_blocked_patterns"].copy()
        self.file_allowed_dirs = preset.get("file_allowed_dirs", []).copy()

        self.process_protection_enabled = preset.get("process_protection_enabled", False)

    @property
    def is_enabled(self) -> bool:
        """检查是否启用安全功能"""
        return self.mode != SecurityMode.DISABLED

    @property
    def enabled(self) -> bool:
        """兼容旧接口"""
        return self.is_enabled

    def load_from_file(self, config_path: str = "security_config.json"):
        """从文件加载配置"""
        if not os.path.exists(config_path):
            self.apply_preset(SecurityMode.DISABLED)
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if 'api_key' in config and config['api_key']:
                self.set_api_key(config['api_key'])

            mode = config.get('mode', SecurityMode.DISABLED)
            self.apply_preset(mode)

            if 'custom' in config:
                custom = config['custom']
                if 'shell' in custom:
                    shell_config = custom['shell']
                    self.shell_whitelist_mode = shell_config.get('whitelist_mode', self.shell_whitelist_mode)
                    self.shell_allowed_commands = shell_config.get('allowed_commands', [])
                    self.shell_blocked_commands = shell_config.get('blocked_commands', self.shell_blocked_commands)
                    self.shell_blocked_patterns = shell_config.get('blocked_patterns', self.shell_blocked_patterns)

                if 'file' in custom:
                    file_config = custom['file']
                    self.file_sandbox_enabled = file_config.get('enabled', self.file_sandbox_enabled)
                    self.file_allowed_dirs = file_config.get('allowed_dirs', [])
                    self.file_blocked_dirs = file_config.get('blocked_dirs', self.file_blocked_dirs)
                    self.file_blocked_patterns = file_config.get('blocked_patterns', self.file_blocked_patterns)

                if 'process' in custom:
                    self.process_protection_enabled = custom['process'].get('enabled', self.process_protection_enabled)

            if 'log' in config:
                log_config = config['log']
                self.log_enabled = log_config.get('enabled', True)
                self.log_file = log_config.get('file', 'security.log')
                self.log_sensitive = log_config.get('sensitive', False)

        except Exception as e:
            print(f"加载安全配置失败: {e}")
            self.apply_preset(SecurityMode.DISABLED)

    def save_to_file(self, config_path: str = "security_config.json"):
        """保存配置到文件"""
        config = {
            'mode': self.mode,
            'api_key': self.api_key or '',
            'custom': {
                'shell': {
                    'whitelist_mode': self.shell_whitelist_mode,
                    'allowed_commands': self.shell_allowed_commands,
                    'blocked_commands': self.shell_blocked_commands,
                    'blocked_patterns': self.shell_blocked_patterns
                },
                'file': {
                    'enabled': self.file_sandbox_enabled,
                    'allowed_dirs': self.file_allowed_dirs,
                    'blocked_dirs': self.file_blocked_dirs,
                    'blocked_patterns': self.file_blocked_patterns
                },
                'process': {
                    'enabled': self.process_protection_enabled
                }
            },
            'log': {
                'enabled': self.log_enabled,
                'file': self.log_file,
                'sensitive': self.log_sensitive
            }
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def set_api_key(self, api_key: str):
        """设置 API Key"""
        self.api_key = api_key
        self.api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    def verify_api_key(self, api_key: str) -> bool:
        """验证 API Key"""
        if not self.api_key:
            return True
        return hashlib.sha256(api_key.encode()).hexdigest() == self.api_key_hash

    def get_mode_info(self) -> Dict[str, Any]:
        """获取当前模式信息"""
        return {
            "mode": self.mode,
            "description": self.PRESETS.get(self.mode, {}).get("description", "自定义配置"),
            "shell_whitelist_mode": self.shell_whitelist_mode,
            "file_sandbox_enabled": self.file_sandbox_enabled,
            "process_protection_enabled": self.process_protection_enabled,
            "api_key_set": bool(self.api_key)
        }


config = SecurityConfig()
config.load_from_file()


def log_operation(operation: str, details: Dict[str, Any], allowed: bool = True, reason: str = ""):
    """记录操作日志"""
    if not config.log_enabled:
        return

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "mode": config.mode,
        "operation": operation,
        "details": details.copy() if details else {},
        "allowed": allowed,
        "reason": reason
    }

    if not config.log_sensitive:
        if 'password' in str(log_entry.get('details', {})):
            log_entry['details']['password'] = 'REDACTED'
        if 'content' in log_entry.get('details', {}) and len(str(log_entry['details']['content'])) > 100:
            log_entry['details']['content'] = str(log_entry['details']['content'])[:100] + '...'

    try:
        with open(config.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception:
        pass


def check_shell_command(command: str, shell: str = "powershell") -> tuple[bool, str]:
    """
    检查 Shell 命令是否安全

    Returns:
        (是否允许, 拒绝原因)
    """
    if not config.is_enabled:
        return True, ""

    cmd_lower = command.lower().strip()

    for pattern in config.shell_blocked_patterns:
        if re.search(pattern, cmd_lower, re.IGNORECASE):
            log_operation("shell_blocked", {"command": command, "shell": shell, "pattern": pattern}, False, f"匹配到禁止模式: {pattern}")
            return False, f"命令包含禁止模式: {pattern}"

    for blocked in config.shell_blocked_commands:
        if blocked.lower() in cmd_lower:
            log_operation("shell_blocked", {"command": command, "shell": shell, "blocked": blocked}, False, f"命令包含禁止关键字: {blocked}")
            return False, f"命令包含禁止关键字: {blocked}"

    if not config.shell_whitelist_mode:
        log_operation("shell_allowed", {"command": command, "shell": shell}, True)
        return True, ""

    allowed_cmds = ['get-process', 'get-service', 'get-childitem', 'dir', 'ls', 'pwd',
                    'get-content', 'select-object', 'where-object', 'convertto-json',
                    'echo', 'write-output', 'get-date', 'get-host', 'hostname',
                    'get-item', 'get-itemproperty', 'test-path', 'split-path',
                    'join-path', 'resolve-path', 'get-acl', 'get-filehash']

    allowed_cmds.extend(config.shell_allowed_commands)

    for allowed in allowed_cmds:
        if cmd_lower.startswith(allowed.lower()) or f" {allowed.lower()}" in cmd_lower:
            log_operation("shell_allowed", {"command": command, "shell": shell, "matched": allowed}, True)
            return True, ""

    log_operation("shell_blocked", {"command": command, "shell": shell}, False, "命令不在白名单中")
    return False, "命令不在白名单中"


def check_file_path(file_path: str, operation: str = "read") -> tuple[bool, str]:
    """
    检查文件路径是否安全

    Returns:
        (是否允许, 拒绝原因)
    """
    if not config.is_enabled or not config.file_sandbox_enabled:
        return True, ""

    try:
        abs_path = os.path.abspath(file_path)
    except Exception as e:
        log_operation("file_blocked", {"path": file_path, "operation": operation}, False, f"路径解析失败: {e}")
        return False, f"路径解析失败: {e}"

    path_lower = abs_path.lower()

    for blocked in config.file_blocked_dirs:
        if blocked.lower() in path_lower:
            log_operation("file_blocked", {"path": file_path, "operation": operation}, False, f"路径包含禁止目录: {blocked}")
            return False, f"路径包含禁止目录: {blocked}"

    for pattern in config.file_blocked_patterns:
        if re.search(pattern, abs_path, re.IGNORECASE):
            log_operation("file_blocked", {"path": file_path, "operation": operation}, False, f"路径匹配禁止模式: {pattern}")
            return False, f"路径匹配禁止模式: {pattern}"

    if config.file_allowed_dirs:
        allowed = False
        for allowed_dir in config.file_allowed_dirs:
            if path_lower.startswith(allowed_dir.lower()):
                allowed = True
                break
        if not allowed:
            log_operation("file_blocked", {"path": file_path, "operation": operation}, False, "路径不在允许目录列表中")
            return False, "路径不在允许目录列表中"

    log_operation("file_allowed", {"path": file_path, "operation": operation}, True)
    return True, ""


def check_process_operation(process_name: str, operation: str = "kill") -> tuple[bool, str]:
    """
    检查进程操作是否安全

    Returns:
        (是否允许, 拒绝原因)
    """
    if not config.is_enabled or not config.process_protection_enabled:
        return True, ""

    protected_processes = [
        'system', 'csrss', 'wininit', 'services', 'lsass', 'smss',
        'winlogon', 'dwm', 'explorer', 'taskhostw', 'runtimebroker',
        'searchindexer', 'securityhealthservice', 'windowsdefender',
        'svchost', 'fontdrvhost', 'sihost'
    ]

    process_lower = process_name.lower().replace('.exe', '')

    if process_lower in protected_processes:
        log_operation("process_blocked", {"name": process_name, "operation": operation}, False, "系统保护进程")
        return False, f"无法对系统保护进程执行操作: {process_name}"

    log_operation("process_allowed", {"name": process_name, "operation": operation}, True)
    return True, ""
