#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Host Semantic Config — host-level custom signal/event-type definitions.

This module loads a host_semantics.json file that lets each gateway host
define extra signal keywords, map them to event types, set priorities,
and choose auto/suggest/manual creation policy.

The config is ADDITIVE: it extends (never replaces) the hardcoded
signal lists in event_store.py.  Hosts can also override the
auto/suggest policy for built-in event types.

File location (resolved at runtime):
  $OPENCLAW_STATE_DIR/workspace/personal-hooks/host_semantics.json

Schema:
{
  "version": 1,
  "categories": [
    {
      "id":             "identity",          // unique per category
      "label":          "身份類",             // display label
      "signals":        ["我是...","叫我..."],
      "event_type":     "identity_event",    // → appended to EVENT_TYPES if new
      "default_title":  "身份資訊：{signal}",
      "desired_followup": "記住並反映在稱呼中",
      "priority":       "medium",            // low|medium|high|critical
      "policy":         "suggest",           // auto|suggest|manual
      "negation_aware": true,                // apply NEGATION_PREFIXES check
      "rank":           50                   // detection order (lower = higher priority)
    },
    ...
  ],
  "policy_overrides": {
    // Override auto/suggest for built-in types
    "relationship_event": "auto",
    "work_event": "auto"
  }
}
"""

import json
import os
from typing import Optional, List, Dict, Any

__version__ = "1.0.0"

DEFAULT_OPENCLAW_STATE_DIR = os.path.expanduser("~/.openclaw")

# ── Default empty config ──

EMPTY_CONFIG: Dict[str, Any] = {
    "version": 1,
    "categories": [],
    "policy_overrides": {},
}

# ── Example host_semantics.json (written on first load if missing) ──

EXAMPLE_CONFIG: Dict[str, Any] = {
    "version": 1,
    "categories": [
        {
            "id": "identity",
            "label": "身份類",
            "signals": ["我是", "叫我", "我的名字", "my name is", "稱呼我"],
            "event_type": "identity_event",
            "default_title": "身份資訊：{signal}",
            "desired_followup": "記住並反映在稱呼中",
            "priority": "low",
            "policy": "suggest",
            "negation_aware": False,
            "rank": 60,
        },
        {
            "id": "life_context",
            "label": "生活情境類",
            "signals": [
                "搬家", "出國", "旅行", "出差", "回老家", "換工作",
                "畢業", "入學", "結婚", "離婚", "懷孕", "退休",
            ],
            "event_type": "life_context_event",
            "default_title": "生活情境：{signal}",
            "desired_followup": "留意對日常的影響",
            "priority": "medium",
            "policy": "suggest",
            "negation_aware": True,
            "rank": 45,
        },
        {
            "id": "work_context",
            "label": "工作情境類",
            "signals": [
                "deadline", "上線", "demo", "面試", "開會", "報告",
                "加班", "on call", "交接", "績效", "升遷", "被裁",
            ],
            "event_type": "work_event",
            "default_title": "工作情境：{signal}",
            "desired_followup": "適時關心進度與壓力",
            "priority": "medium",
            "policy": "suggest",
            "negation_aware": True,
            "rank": 40,
        },
        {
            "id": "relationship",
            "label": "關係類",
            "signals": [
                "吵架", "冷戰", "分手", "復合", "想念", "紀念日",
                "約會", "告白", "曖昧", "被拒", "劈腿",
            ],
            "event_type": "relationship_event",
            "default_title": "關係事件：{signal}",
            "desired_followup": "溫和關心，不主動追問細節",
            "priority": "medium",
            "policy": "suggest",
            "negation_aware": True,
            "rank": 35,
        },
        {
            "id": "health_wellness",
            "label": "健康/情緒類（擴充）",
            "signals": [
                "失眠", "睡不著", "過敏", "拉肚子", "胃痛",
                "腰痛", "感冒", "咳嗽", "流鼻水", "眼睛痛",
                "復健", "回診", "抽血", "打針", "吃藥",
            ],
            "event_type": "health_event",
            "default_title": "健康狀況：{signal}",
            "desired_followup": "主動關心身體狀況",
            "priority": "high",
            "policy": "auto",
            "negation_aware": True,
            "rank": 5,
        },
    ],
    "policy_overrides": {},
}


def _resolve_config_path() -> str:
    """Resolve host_semantics.json path from env or default."""
    state_dir = os.environ.get("OPENCLAW_STATE_DIR", DEFAULT_OPENCLAW_STATE_DIR)
    return os.path.join(state_dir, "workspace/personal-hooks/host_semantics.json")


def load_semantic_config(path: Optional[str] = None) -> Dict[str, Any]:
    """Load host semantic config. Returns EMPTY_CONFIG if file missing or invalid."""
    path = path or _resolve_config_path()
    if not os.path.isfile(path):
        return dict(EMPTY_CONFIG)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "categories" not in data:
            return dict(EMPTY_CONFIG)
        return data
    except (json.JSONDecodeError, OSError):
        return dict(EMPTY_CONFIG)


def save_semantic_config(config: Dict[str, Any], path: Optional[str] = None) -> str:
    """Write config to disk. Returns path written."""
    path = path or _resolve_config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return path


def init_example_config(path: Optional[str] = None) -> str:
    """Write the example config if file doesn't exist. Returns path."""
    path = path or _resolve_config_path()
    if os.path.isfile(path):
        return path
    return save_semantic_config(EXAMPLE_CONFIG, path)


# ── Config → Detection Structures ──

class SemanticCategory:
    """Parsed category ready for detection."""

    __slots__ = (
        "id", "label", "signals", "event_type", "default_title",
        "desired_followup", "priority", "policy", "negation_aware", "rank",
    )

    def __init__(self, raw: Dict[str, Any]):
        self.id: str = raw.get("id", "unknown")
        self.label: str = raw.get("label", self.id)
        self.signals: List[str] = raw.get("signals", [])
        self.event_type: str = raw.get("event_type", "custom")
        self.default_title: str = raw.get("default_title", "{signal}")
        self.desired_followup: str = raw.get("desired_followup", "")
        self.priority: str = raw.get("priority", "medium")
        self.policy: str = raw.get("policy", "suggest")  # auto|suggest|manual
        self.negation_aware: bool = raw.get("negation_aware", True)
        self.rank: int = raw.get("rank", 50)

    def format_title(self, matched_signal: str) -> str:
        return self.default_title.replace("{signal}", matched_signal)


def parse_categories(config: Dict[str, Any]) -> List[SemanticCategory]:
    """Parse config into sorted list of SemanticCategory (lower rank first)."""
    cats = []
    for raw in config.get("categories", []):
        if not raw.get("signals"):
            continue
        cats.append(SemanticCategory(raw))
    cats.sort(key=lambda c: c.rank)
    return cats


def get_policy_overrides(config: Dict[str, Any]) -> Dict[str, str]:
    """Return {event_type: policy} overrides from config."""
    return dict(config.get("policy_overrides", {}))


# ── CLI ──

def main():
    import sys
    args = sys.argv[1:]
    if not args:
        print(json.dumps({"error": "usage: semantic_config.py <init|show|path>"}, ensure_ascii=False))
        sys.exit(1)

    cmd = args[0]

    if cmd == "init":
        p = init_example_config()
        print(json.dumps({"ok": True, "path": p, "action": "init_example"}, ensure_ascii=False))

    elif cmd == "show":
        cfg = load_semantic_config()
        print(json.dumps(cfg, ensure_ascii=False, indent=2))

    elif cmd == "path":
        print(_resolve_config_path())

    else:
        print(json.dumps({"error": f"unknown command: {cmd}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
