"""
Multi-Group-Chat-Manager - 统一配置加载模块
========================================
所有脚本统一从此模块读取配置参数。
零外部依赖，使用 Python 标准库 json 模块。

用法:
    from config import load as load_config
    cfg = load_config()
    val = cfg["session"]["recovery_window_hours"]
"""

import json
import sys
from pathlib import Path

# 修复 Windows 编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIG_FILE = SKILL_DIR / "config.json"

# 默认配置（当 config.json 不存在或部分缺失时的后备值）
DEFAULTS = {
    "session": {
        "recovery_window_hours": 24,
        "recovery_max_messages": 1000,
        "default_max_messages": 100,
    },
    "profiling": {
        "min_update_interval": 300,
        "auto_dedup": True,
        "max_items_per_field": 50,
        "output_language": "zh-CN",
    },
    "memory": {
        "lambda_decay": 0.05,
        "alpha_boost": 0.2,
        "score_threshold": 0.15,
        "new_memory_score": 0.8,
        "auto_decay_interval": 86400,
    },
    "affection": {
        "default_score": 50,
        "small_group_default_score": 85,
        "small_group_ids": [],
        "brief_query_hours": 24,
        "detail_max_entries": 20,
        "min_score": 0,
        "max_score": 100,
        "lock_timeout": 10,
        "lock_stale_seconds": 5,
    },
}

# 缓存，避免每次调用都读磁盘
_cache = None


def _strip_notes(d: dict) -> dict:
    """移除所有以 _note 开头的注释字段"""
    if not isinstance(d, dict):
        return d
    return {
        k: _strip_notes(v) for k, v in d.items()
        if not k.startswith("_note")
    }


def load(force_reload: bool = False) -> dict:
    """
    加载配置。
    
    优先级: config.json 中的值 > 默认值
    
    参数:
        force_reload: True 则重新读取磁盘，不使用缓存
    返回:
        dict: 完整配置字典
    """
    global _cache
    if _cache is not None and not force_reload:
        return _cache

    # 从默认值开始
    config = json.loads(json.dumps(DEFAULTS))  # deep copy

    # 尝试读取 config.json
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                file_config = json.load(f)
            # 移除 _note 注释字段
            file_config = _strip_notes(file_config)
            # 递归合并
            _deep_merge(config, file_config)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[config.py] 警告: 读取 config.json 失败: {e}，使用默认值",
                  file=sys.stderr)

    _cache = config
    return config


def _deep_merge(base: dict, override: dict):
    """
    递归合并字典。override 中的键值覆盖 base 中的同名字段。
    """
    for key, val in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(val, dict):
            _deep_merge(base[key], val)
        else:
            base[key] = val


def get(section: str, key: str, default=None):
    """
    快捷获取单个配置项。
    
    用法:
        from config import get
        val = get("session", "recovery_window_hours", 24)
    """
    cfg = load()
    return cfg.get(section, {}).get(key, default)


# ══════════════════════════════════════════
# CLI 入口（查看当前配置）
# ══════════════════════════════════════════

if __name__ == "__main__":
    cfg = load(force_reload=True)
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
