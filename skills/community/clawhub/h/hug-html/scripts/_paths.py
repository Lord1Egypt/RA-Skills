"""
_paths.py — 路径集中管理
只包含路径常量和路径推导函数，不包含任何业务逻辑。
"""
import os
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR    = _SCRIPT_DIR.parent
SKILLS_ROOT  = SKILL_DIR.parent
SKILL_NAME   = SKILL_DIR.name

STD_ROOT     = SKILLS_ROOT / ".standardization"
STD_DIR      = STD_ROOT / SKILL_NAME
DATA_DIR     = STD_DIR / "data"
OUTPUTS_DIR  = STD_DIR / "outputs"
BACKUP_DIR   = STD_DIR / "backup"
CACHE_DIR    = STD_DIR / "cache"
TEMP_DIR     = STD_DIR / "temp"

