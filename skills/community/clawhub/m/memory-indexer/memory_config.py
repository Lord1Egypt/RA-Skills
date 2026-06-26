#!/usr/bin/env python3
"""
Memory Indexer - 配置管理模块
支持从配置文件加载设置
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# 默认配置
DEFAULT_CONFIG = {
    # 路径配置
    "paths": {
        "workspace": str(Path.home() / ".openclaw" / "workspace"),
        "memory_dir": None,  # None 表示使用默认值 (workspace/memory)
        "external_memory_dir": None,
        "agents_dir": None,
        "backup_dir": None,
        "indexer_dir": None,
        "snapshot_dir": None,
    },
    # 阈值配置
    "thresholds": {
        "warning_mb": 70,
        "critical_mb": 85,
        "max_memory_size_kb": 10,
        "max_session_size_kb": 10,
    },
    # 索引器配置
    "indexer": {
        "keywords_topk": 10,
    },
    # 快照配置
    "snapshot": {
        "auto_snapshot": False,
        "max_snapshots": 10,
    },
}

# 配置文件路径（支持环境变量覆盖）
_CONFIG_FILE = os.getenv("MEMORY_INDEXER_CONFIG", ".memory-indexer/config.json")
CONFIG_FILE = Path.home() / _CONFIG_FILE


def get_config_path() -> Path:
    """获取配置文件路径"""
    return CONFIG_FILE


def _expand_path(path: Any) -> Optional[Path]:
    """展开路径（支持 ~ 和环境变量）"""
    if path is None:
        return None
    if isinstance(path, Path):
        return path
    return Path(os.path.expanduser(os.path.expandvars(str(path))))


def _resolve_path(path: Optional[str], default: Path) -> Path:
    """解析路径，空值使用默认值"""
    if path:
        expanded = _expand_path(path)
        if expanded:
            return expanded
    return default


def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config = DEFAULT_CONFIG.copy()
    
    # 尝试读取配置文件
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                config = _deep_merge(config, user_config)
        except Exception as e:
            print(f"⚠️ 配置文件加载失败: {e}")
            print(f"   使用默认配置")
    
    # 环境变量覆盖
    env_mappings = {
        "MEMORY_INDEXER_WARNING": ("thresholds", "warning_mb"),
        "MEMORY_INDEXER_CRITICAL": ("thresholds", "critical_mb"),
        "MEMORY_INDEXER_MAX_MEMORY_KB": ("thresholds", "max_memory_size_kb"),
        "MEMORY_INDEXER_KEYWORDS": ("indexer", "keywords_topk"),
    }
    
    for env_var, (section, key) in env_mappings.items():
        if os.getenv(env_var):
            try:
                config[section][key] = int(os.getenv(env_var))
            except ValueError:
                pass
    
    return config


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """深度合并字典"""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def save_config(config: Dict[str, Any] = None):
    """保存配置文件"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    if config is None:
        config = DEFAULT_CONFIG.copy()
    
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def init_config():
    """初始化配置文件"""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        print(f"✅ 配置文件已创建: {CONFIG_FILE}")
    else:
        print(f"ℹ️ 配置文件已存在: {CONFIG_FILE}")


# ==================== 路径获取函数 ====================

def get_workspace() -> Path:
    """获取工作空间路径"""
    config = load_config()
    return _resolve_path(config.get("paths", {}).get("workspace"), Path.home() / ".openclaw" / "workspace")


def get_memory_dir() -> Path:
    """获取 memory 目录路径"""
    config = load_config()
    paths = config.get("paths", {})
    if paths.get("memory_dir"):
        return _resolve_path(paths["memory_dir"], get_workspace() / "memory")
    return get_workspace() / "memory"


def get_external_memory_dir() -> Path:
    """获取外部记忆目录路径"""
    config = load_config()
    paths = config.get("paths", {})
    if paths.get("external_memory_dir"):
        return _resolve_path(paths["external_memory_dir"], get_workspace() / "memory")
    return get_workspace() / "memory"


def get_agents_dir() -> Path:
    """获取 agents 目录路径"""
    config = load_config()
    paths = config.get("paths", {})
    if paths.get("agents_dir"):
        return _resolve_path(paths["agents_dir"], Path.home() / ".openclaw" / "agents" / "main" / "sessions")
    return Path.home() / ".openclaw" / "agents" / "main" / "sessions"


def get_backup_dir() -> Path:
    """获取备份目录路径"""
    config = load_config()
    paths = config.get("paths", {})
    if paths.get("backup_dir"):
        return _resolve_path(paths["backup_dir"], get_workspace() / "memory-index" / "session-backups")
    return get_workspace() / "memory-index" / "session-backups"


def get_indexer_dir() -> Path:
    """获取 indexer 目录路径"""
    config = load_config()
    paths = config.get("paths", {})
    if paths.get("indexer_dir"):
        return _resolve_path(paths["indexer_dir"], get_workspace() / "skills" / "memory-indexer")
    return get_workspace() / "skills" / "memory-indexer"


def get_snapshot_dir() -> Path:
    """获取快照目录路径"""
    config = load_config()
    paths = config.get("paths", {})
    if paths.get("snapshot_dir"):
        return _resolve_path(paths["snapshot_dir"], get_workspace() / "memory-indexer" / "snapshots")
    return get_workspace() / "memory-indexer" / "snapshots"


# ==================== 阈值获取函数 ====================

def get_warning_threshold() -> int:
    """获取警告阈值 (MB)"""
    config = load_config()
    return config.get("thresholds", {}).get("warning_mb", 70)


def get_critical_threshold() -> int:
    """获取危险阈值 (MB)"""
    config = load_config()
    return config.get("thresholds", {}).get("critical_mb", 85)


def get_max_memory_size_kb() -> int:
    """获取最大 memory 大小 (KB)"""
    config = load_config()
    return config.get("thresholds", {}).get("max_memory_size_kb", 10)


def get_max_session_size_kb() -> int:
    """获取最大 session 大小 (KB)"""
    config = load_config()
    return config.get("thresholds", {}).get("max_session_size_kb", 10)


# ==================== 索引器配置 ====================

def get_keywords_topk() -> int:
    """获取关键词提取数量"""
    config = load_config()
    return config.get("indexer", {}).get("keywords_topk", 10)


# ==================== 快照配置 ====================

def get_auto_snapshot() -> bool:
    """获取自动快照设置"""
    config = load_config()
    return config.get("snapshot", {}).get("auto_snapshot", False)


def get_max_snapshots() -> int:
    """获取最大快照数量"""
    config = load_config()
    return config.get("snapshot", {}).get("max_snapshots", 10)


if __name__ == "__main__":
    # 测试配置功能
    print("📋 Memory Indexer 配置管理")
    print("=" * 50)
    
    init_config()
    
    config = load_config()
    print(f"\n当前配置:")
    print(f"\n路径配置:")
    for key, value in config.get("paths", {}).items():
        print(f"  {key}: {value}")
    print(f"\n阈值配置:")
    for key, value in config.get("thresholds", {}).items():
        print(f"  {key}: {value}")
    print(f"\n索引器配置:")
    for key, value in config.get("indexer", {}).items():
        print(f"  {key}: {value}")
    print(f"\n快照配置:")
    for key, value in config.get("snapshot", {}).items():
        print(f"  {key}: {value}")
    
    print(f"\n解析后的路径:")
    print(f"  workspace: {get_workspace()}")
    print(f"  memory_dir: {get_memory_dir()}")
    print(f"  agents_dir: {get_agents_dir()}")
    print(f"  backup_dir: {get_backup_dir()}")
    print(f"  indexer_dir: {get_indexer_dir()}")
    print(f"  snapshot_dir: {get_snapshot_dir()}")
    
    print(f"\n阈值:")
    print(f"  warning_mb: {get_warning_threshold()}")
    print(f"  critical_mb: {get_critical_threshold()}")
    print(f"  keywords_topk: {get_keywords_topk()}")
