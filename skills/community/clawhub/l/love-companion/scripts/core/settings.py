#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局设置的统一读取（v2 排查整改）

解决的问题（排查缺陷 2）：
- 此前 `settings.json` 里的「注入预算」「衰减参数」只在 schema 里定义，
  代码全走 DEFAULT_* 常量——用户改了不生效，是个假旋钮。
- `DEFAULT_DATA_DIR` / `ENV_DATA_DIR` 在 11 个模块各写一份字面量。

约定：
- load() 做**深合并**：用户 settings.json 只覆盖它写明的叶子字段，
  未写明的回退到 schema.settings_template() 的默认值。
- 读取走 core/storage.py，坏文件自动降级为默认设置。
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# 允许 `python scripts/core/settings.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import schema  # noqa: E402
from scripts.core.storage import read_json  # noqa: E402

ENV_DATA_DIR = "LOVE_COMPANION_DATA_DIR"
DEFAULT_DATA_DIR = "~/.love-companion/data"


def resolve_data_dir(data_dir: Optional[str] = None) -> Path:
    """统一的数据目录解析：入参 > 环境变量 > 默认路径"""
    resolved = data_dir or os.environ.get(ENV_DATA_DIR) or DEFAULT_DATA_DIR
    return Path(os.path.expanduser(str(resolved)))


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load(data_dir: Optional[str] = None) -> Dict[str, Any]:
    """读取全局设置（默认模板深合并用户 settings.json）"""
    raw = read_json(resolve_data_dir(data_dir) / "settings.json", {})
    if not isinstance(raw, dict):
        raw = {}
    return _deep_merge(schema.settings_template(), raw)


def decay_params(data_dir: Optional[str] = None) -> Dict[str, float]:
    """记忆衰减参数：settings.json 优先，缺省回退 DEFAULT_DECAY"""
    merged = dict(schema.DEFAULT_DECAY)
    user = load(data_dir).get("衰减参数") or {}
    for key in merged:
        if key in user:
            try:
                merged[key] = float(user[key])
            except (TypeError, ValueError):
                pass
    return merged


def budget_map(data_dir: Optional[str] = None) -> Dict[str, int]:
    """在线注入预算表：settings.json 优先，缺省回退 DEFAULT_INJECTION_BUDGET"""
    merged = dict(schema.DEFAULT_INJECTION_BUDGET)
    user = load(data_dir).get("注入预算") or {}
    for key in merged:
        if key in user:
            try:
                merged[key] = int(user[key])
            except (TypeError, ValueError):
                pass
    return merged


def budget(data_dir: Optional[str], module: str) -> int:
    """单个模块的注入预算（不存在回退 0）"""
    return int(budget_map(data_dir).get(module, 0))


def total_budget(data_dir: Optional[str] = None) -> int:
    return int(budget_map(data_dir).get(
        "合计上限", schema.DEFAULT_INJECTION_BUDGET["合计上限"]))


def collection_enabled(data_dir: Optional[str] = None) -> bool:
    """记忆/信号采集开关（隐私.采集开关），默认开"""
    return bool(load(data_dir).get("隐私", {}).get("采集开关", True))


def age_confirmed(data_dir: Optional[str] = None) -> bool:
    """合规闸门：用户是否已确认年满 18 周岁

    默认未确认。依据《人工智能拟人化互动服务管理暂行办法》，
    虚拟伴侣等虚拟亲密关系服务不得向未成年人提供——未确认前
    orchestrator.Session.prepare() 不注入任何人设与记忆。
    """
    return bool(load(data_dir).get("合规", {}).get("已满18周岁确认", False))


if __name__ == "__main__":
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        print("默认：", json.dumps(decay_params(d), ensure_ascii=False))
        Path(d, "settings.json").write_text(
            json.dumps({"衰减参数": {"half_life_days": 60},
                        "注入预算": {"合计上限": 300}}), encoding="utf-8")
        print("改半衰期后：", decay_params(d)["half_life_days"],
              "（其它键回退默认）", decay_params(d)["recall_boost"])
        print("改总预算后：", total_budget(d))
