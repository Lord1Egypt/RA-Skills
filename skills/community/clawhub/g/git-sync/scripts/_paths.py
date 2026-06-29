"""
_paths.py — git-sync 路径集中管理
只包含路径常量和路径推导函数，不包含任何业务逻辑。

R-12 审计锚点：所有数据目录声明集中在此文件，
各脚本通过 `from _paths import ...` 引用。
"""
import os
from pathlib import Path

# ── 基础目录 ──────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR   = _SCRIPT_DIR.parent
SKILLS_ROOT = SKILL_DIR.parent
SKILL_NAME  = SKILL_DIR.name

# ── 数据目录（R-12 规范） ────────────────────────────
DEFAULT_DATA_DIR_RAW = "skills/.standardization/git-sync/data/"
_data_dir_abs = SKILLS_ROOT / ".standardization" / "git-sync" / "data"

STD_ROOT     = SKILLS_ROOT / ".standardization"
STD_DIR      = STD_ROOT / SKILL_NAME
DATA_DIR     = SKILLS_ROOT / ".standardization" / "git-sync" / "data"
OUTPUTS_DIR  = STD_DIR / "outputs"
BACKUP_DIR   = STD_DIR / "backup"
CACHE_DIR    = SKILLS_ROOT / ".standardization" / "git-sync" / "cache"
TEMP_DIR     = STD_DIR / "temp"

# ── 仓库与分发目录 ──────────────────────────────────
WORK_REPO    = Path.home() / ".workbuddy" / "workbuddy-skills"
DIST_DIR     = SKILLS_ROOT / ".dist"
README_FILE  = WORK_REPO / "README.md"

# ── 清单与配置文件 ──────────────────────────────────
MANIFEST_FILE = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "manifest.json"
CONFIG_FILE   = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "config.json"

# ── 凭证文件 ──────────────────────────────────────────
GIT_CREDENTIALS = Path.home() / ".git-credentials"

# ── 脚本临时文件前缀 ────────────────────────────────
SCAN_OUT_PREFIX = ".sensitive_scan_"
