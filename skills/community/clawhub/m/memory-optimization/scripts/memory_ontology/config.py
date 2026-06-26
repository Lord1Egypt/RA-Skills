"""
Configuration module for memory_ontology package.
Contains path configuration, constants, and environment loading.
"""

import os
from pathlib import Path
from typing import Dict

# Path configuration - supports KG_DIR environment variable
# Development: ontology/ (relative path)
# Production: /root/.openclaw/workspace/memory/ontology/
# NOTE: When imported from the package (memory_ontology/__init__.py), __file__ points to the package,
# so we need parent.parent to get to scripts/. When imported from the shim (memory_ontology.py),
# parent gives us scripts/ directly.
_PACKAGE_DIR = Path(__file__).parent
if _PACKAGE_DIR.name == 'memory_ontology':
    # Imported from package
    SCRIPT_DIR = _PACKAGE_DIR.parent
else:
    # Imported from shim or directly
    SCRIPT_DIR = _PACKAGE_DIR
WORKSPACE_ROOT = SCRIPT_DIR.parent


def load_env_file():
    """从 .env 文件加载环境变量

    查找 WORKSPACE_ROOT/.env 文件并设置环境变量。
    跳过注释和空行，支持带引号的值。
    """
    env_file = WORKSPACE_ROOT / ".env"
    if not env_file.exists():
        return

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            # 解析 KEY=value
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                os.environ[key] = value


# 加载 .env 文件（必须在读取 KG_DIR 之前）
load_env_file()

# 现在根据环境变量设置路径
_kg_dir = os.environ.get('KG_DIR', '')  # 可配置的知识图谱目录
ONTOLOGY_DIR = Path(_kg_dir) if _kg_dir else WORKSPACE_ROOT / "ontology"

# 验证 KG_DIR 不超过工作区根目录（防止路径遍历攻击）
# 安全检查：当 KG_DIR 被显式设置时必须验证
_ALLOW_ANY_KG_DIR = os.environ.get('ALLOW_ANY_KG_DIR', '').lower() in ('1', 'true', 'yes')
if _kg_dir and not _ALLOW_ANY_KG_DIR:
    try:
        if not ONTOLOGY_DIR.resolve().is_relative_to(WORKSPACE_ROOT.resolve()):
            raise ValueError(f"KG_DIR must be within workspace root: {WORKSPACE_ROOT}")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"KG_DIR path validation failed: {e}")
GRAPH_FILE = ONTOLOGY_DIR / "graph.jsonl"
SCHEMA_FILE = ONTOLOGY_DIR / "memory-schema.yaml"
BASE_SCHEMA_FILE = ONTOLOGY_DIR / "schema.yaml"

# ========== Phase 1b: 记忆进化字段配置 ==========

# 各实体类型的默认衰减率 (每月)
DECAY_RATES: Dict[str, float] = {
    'Decision': 0.95,
    'LessonLearned': 0.90,
    'Finding': 0.80,
    'SkillCard': 0.99,
    'Commitment': 0.85,
    'ContextSnapshot': 0.75,
    'Note': 0.85,
    'Task': 0.80,
    'Project': 0.90,
    'Preference': 0.90,  # Phase 2
    'Concept': 0.95,  # Phase 4: Concepts decay slowly
    # 默认值
    'default': 0.90
}

# 衰减阈值，低于此值标记为归档候选
DECAY_THRESHOLD = 0.10

# 访问时衰减阈值（小时），超过此时间才触发衰减
ACCESS_DECAY_THRESHOLD_HOURS = 1

# 文件锁超时（秒）
LOCK_TIMEOUT_SECONDS = 10