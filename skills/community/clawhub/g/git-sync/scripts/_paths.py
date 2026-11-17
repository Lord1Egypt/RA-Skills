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
# 多仓库模型（v2.37.0）：按项目类型解析目标仓库
# 仓库注册表在 config.json 的 "repos" 字段（git-sync 数据目录）
DIST_DIR     = SKILLS_ROOT / ".dist"

# ── 清单与配置文件 ──────────────────────────────────
MANIFEST_FILE = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "manifest.json"
CONFIG_FILE   = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "config.json"

# 默认仓库名（类型 → 仓库名）
DEFAULT_REPO_BY_TYPE = {
    "skill": "maby_skills",
    "agent": "maby_agent",
}

def load_config():
    """读取 git-sync config.json（含多仓库注册表）"""
    import json
    cfg = {}
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}
    return cfg

def get_repo_name(project_type: str) -> str:
    """按项目类型返回目标仓库名（skill→maby_skills, agent→maby_agent）"""
    cfg = load_config()
    repos = cfg.get("repos", {})
    for name, rc in repos.items():
        if rc.get("type") == project_type:
            return name
    return DEFAULT_REPO_BY_TYPE.get(project_type, "maby_skills")

def get_repo_config(project_type: str) -> dict:
    """按项目类型返回仓库配置 {name, path, gitee, github, readme}"""
    cfg = load_config()
    repos = cfg.get("repos", {})
    repo_name = get_repo_name(project_type)
    rc = repos.get(repo_name, {})
    return {
        "name": repo_name,
        "path": rc.get("path", str(Path.home() / ".workbuddy" / "workbuddy-skills")),
        "gitee": rc.get("gitee", {}),
        "github": rc.get("github", {}),
        "readme": rc.get("readme", {}),
    }

def get_work_repo(project_type: str):
    """按项目类型返回工作仓库路径（skill→maby_skills, agent→maby_agent）"""
    rc = get_repo_config(project_type)
    return Path(rc["path"])

# 兼容旧引用：WORK_REPO 指向 skill 类型仓库（maby_skills）
WORK_REPO    = get_work_repo("skill")
README_FILE  = WORK_REPO / "README.md"

# ── 清单与配置文件 ──────────────────────────────────
MANIFEST_FILE = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "manifest.json"
CONFIG_FILE   = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "config.json"

# ── 凭证文件 ──────────────────────────────────────────
GIT_CREDENTIALS = Path.home() / ".git-credentials"

# ── 脚本临时文件前缀 ────────────────────────────────
SCAN_OUT_PREFIX = ".sensitive_scan_"
TEMP_FILE_PREFIX = "git_sync_tmp_"

# ── 临时文件路径生成函数 ────────────────────────────
def temp_scan_path(name: str) -> Path:
    """敏感扫描结果：TEMP_DIR / sensitive_scan_{name}.json"""
    return TEMP_DIR / f"sensitive_scan_{name}.json"

def temp_scan_decisions_path(name: str) -> Path:
    """敏感扫描 LLM 判定：TEMP_DIR / sensitive_scan_{name}.decisions.json"""
    return TEMP_DIR / f"sensitive_scan_{name}.decisions.json"

def temp_filter_scan_path(name: str) -> Path:
    """文件过滤器扫描结果：TEMP_DIR / file_filter_{name}.json"""
    return TEMP_DIR / f"file_filter_{name}.json"

def temp_filter_decisions_path(name: str) -> Path:
    """文件过滤器 LLM 判定：TEMP_DIR / file_filter_{name}.decisions.json"""
    return TEMP_DIR / f"file_filter_{name}.decisions.json"

def resume_state_path(name: str) -> Path:
    """断点续跑状态：TEMP_DIR / resume_{name}.json

    记录 LLM 决策让位后卡在哪个环节（file_filter / sensitive_scan），
    重跑时据此跳过已完成的步骤，从当前环节继续。
    """
    return TEMP_DIR / f"resume_{name}.json"
