"""
快导(KD) Skill - Python工具脚本包
提供脚本生成、格式检查、Excel操作等功能
"""

import sys
import io

# Windows 编码修复 - 必须在所有导入之前
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

__version__ = "1.0.0"
__author__ = "快导(KD)"

from .script_generator import ScriptGenerator
from .format_checker import FormatChecker
from .excel_manager import ExcelManager
from .config_manager import ConfigManager
from .feishu_permission_helper import FeishuPermissionHelper
from .workflow_manager import WorkflowManager

__all__ = [
    "ScriptGenerator",
    "FormatChecker",
    "ExcelManager",
    "ConfigManager",
    "FeishuPermissionHelper",
    "WorkflowManager"
]
