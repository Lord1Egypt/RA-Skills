#!/usr/bin/env python3
"""
Configuration manager for Smart Model Router.

Handles multi-layer config merging, OpenClaw integration, and model list management.
Priority: CLI args > env vars > config.json > models.json > openclaw.json > defaults

Zero external dependencies — Python 3.8+ stdlib only.
"""

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ModelEntry:
    """A single model with its cost and capability scores."""
    id: str                                        # full id, e.g. "qwen/qwen3.6-plus"
    cost: float = 5.0                              # 1 (cheapest) – 10 (most expensive)
    capabilities: Dict[str, float] = field(default_factory=lambda: {
        "code": 5.0, "reasoning": 5.0, "agentic": 5.0,
    })

    @property
    def provider(self) -> str:
        return self.id.split("/")[0] if "/" in self.id else ""

    @property
    def name(self) -> str:
        return self.id.split("/", 1)[1] if "/" in self.id else self.id


@dataclass
class RouteConfig:
    """Merged configuration exposed to the router."""
    # Dimension weights
    weights: Dict[str, float] = field(default_factory=lambda: {
        "tokenCount":        0.10,
        "codePresence":      0.12,
        "reasoningMarkers":  0.15,
        "technicalTerms":    0.10,
        "creativeMarkers":   0.06,
        "simpleIndicators":  0.08,
        "multiStepPatterns": 0.06,
        "questionComplexity": 0.05,
        "imperativeVerbs":   0.06,
        "constraintCount":   0.07,
        "outputFormat":      0.06,
        "agenticTask":       0.11,
    })

    # Token thresholds
    thresholds: Dict[str, int] = field(default_factory=lambda: {
        "simpleTokens": 80,
        "complexTokens": 300,
    })

    # Tier boundaries
    tiers: Dict[str, float] = field(default_factory=lambda: {
        "simpleMedium":     -0.08,
        "mediumComplex":     0.15,
        "complexReasoning":  0.55,
    })

    # Default profile
    default_profile: str = "auto"

    # Models list
    models: List[ModelEntry] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Keyword libraries (bilingual zh+en) — ported from JS v4 dimensions.js
# ---------------------------------------------------------------------------

DEFAULT_KEYWORDS = {
    "code": [
        "代码", "code", "函数", "function", "class", "方法", "method",
        "API", "接口", "bug", "修复", "脚本", "script", "编程",
        "python", "javascript", "java", "sql", "实现", "算法",
        "模块", "组件", "服务", "后台", "服务器", "部署",
        "调试", "debug", "编译", "运行", "执行", "重构", "refactor",
        "优化", "重写", "迁移", "移植",
    ],
    "reasoning": [
        "分析", "analyze", "推理", "reasoning", "为什么", "why",
        "比较", "compare", "评估", "evaluate", "思考", "论证",
        "证明", "解释", "原因", "逻辑", "推导", "结论",
        "判断", "决策", "方案", "建议", "利弊", "权衡",
        "可能性", "假设", "验证", "思路", "策略",
    ],
    "technical": [
        "架构", "architecture", "部署", "deploy", "优化", "optimize",
        "算法", "algorithm", "系统", "system", "性能", "performance",
        "安全", "security", "加密", "encrypt", "分布式", "distributed",
        "微服务", "microservice", "容器", "container", "数据库", "database",
        "架构师", "技术选型", "方案", "设计模式", "重构",
    ],
    "creative": [
        "写作", "write", "故事", "story", "创意", "creative",
        "设计", "design", "文章", "article", "文案", "copy",
        "小说", "novel", "诗歌", "poem", "剧本", "script",
    ],
    "simple": [
        "是什么", "what is", "定义", "definition", "怎么读", "how to read",
        "翻译", "translate", "意思是", "meaning", "介绍", "introduce",
    ],
    "imperative": [
        "写", "write", "生成", "generate", "创建", "create",
        "实现", "implement", "帮我", "help me", "请", "please",
        "做", "make", "构建", "build", "设计", "design",
    ],
    "constraint": [
        "必须", "must", "不能", "cannot", "只能", "only",
        "需要", "need", "要求", "require", "限制", "limit",
        "不要", "禁止", "forbid",
    ],
    "outputFormat": [
        "JSON", "json", "表格", "table", "列表", "list",
        "Markdown", "markdown", "格式", "format", "结构", "structure",
        "模板", "template",
    ],
    "agentic": [
        "工具", "tool", "调用", "call", "执行", "execute",
        "文件", "file", "读取", "read", "写入", "write",
        "系统", "system", "命令", "command", "shell", "bash",
        "API", "请求", "request", "fetch", "http",
        "自动", "auto", "批量", "batch", "定时", "cron",
        "agent", "智能体", "助手", "assistant", "workflow",
        "操作", "operate", "处理", "process", "解析", "parse",
    ],
}

# Multi-step regex patterns (pre-compiled)
import re
MULTI_STEP_PATTERNS = [
    re.compile(r"首先.*然后", re.IGNORECASE),
    re.compile(r"第一步", re.IGNORECASE),
    re.compile(r"第二步", re.IGNORECASE),
    re.compile(r"step\s*\d", re.IGNORECASE),
    re.compile(r"\d+\.\s"),
    re.compile(r"先.*再", re.IGNORECASE),
    re.compile(r"首先.*最后", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Model loaders
# ---------------------------------------------------------------------------

def load_models_from_openclaw() -> List[ModelEntry]:
    """
    Auto-discover models from ~/.openclaw/openclaw.json.
    All models get cost=5, capabilities={code:5, reasoning:5, agentic:5}.
    """
    openclaw_path = Path.home() / ".openclaw" / "openclaw.json"
    if not openclaw_path.exists():
        return []

    try:
        config = json.loads(openclaw_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    models: List[ModelEntry] = []
    seen_ids: set = set()

    # 1. Extract from agents.defaults.models
    defaults = config.get("agents", {}).get("defaults", {})
    model_map = defaults.get("models", {})
    if isinstance(model_map, dict):
        for provider_model, entry in model_map.items():
            if isinstance(entry, dict) and entry.get("enabled", True) is False:
                continue
            if provider_model not in seen_ids:
                models.append(ModelEntry(id=provider_model))
                seen_ids.add(provider_model)

    # 2. Extract from agents.list[].model.primary + fallbacks (dedup)
    for agent in config.get("agents", {}).get("list", []):
        primary = agent.get("model", {}).get("primary", "")
        if primary and "/" in primary and primary not in seen_ids:
            models.append(ModelEntry(id=primary))
            seen_ids.add(primary)
        for fb in agent.get("model", {}).get("fallbacks", []):
            if fb and "/" in fb and fb not in seen_ids:
                models.append(ModelEntry(id=fb))
                seen_ids.add(fb)

    return models


def load_models_from_file(path: str) -> List[ModelEntry]:
    """
    Load user-provided models.json.
    Format: {"models": [{"id": "...", "cost": 3, "capabilities": {"code": 9, ...}}, ...]}
    - id: required
    - cost: optional (default 5)
    - capabilities: optional (default all 5.0)
    """
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[smart-model-router] Warning: cannot read models file {path}: {exc}", file=__import__("sys").stderr)
        return []

    default_cap = {"code": 5.0, "reasoning": 5.0, "agentic": 5.0}
    models: List[ModelEntry] = []
    for m in data.get("models", []):
        if "id" not in m:
            continue
        models.append(ModelEntry(
            id=m["id"],
            cost=m.get("cost", 5),
            capabilities=m.get("capabilities", {**default_cap}),
        ))
    return models


# ---------------------------------------------------------------------------
# Config file loader
# ---------------------------------------------------------------------------

def load_config_file(path: Optional[str] = None) -> dict:
    """Load user config.json (weights, thresholds, tiers, profile). Returns empty dict on failure."""
    if path:
        try:
            return json.loads(Path(path).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def merge_config(
    models_path: Optional[str] = None,
    config_path: Optional[str] = None,
    profile: Optional[str] = None,
) -> RouteConfig:
    """
    Build a fully merged RouteConfig.

    Priority: CLI > env > config.json > defaults
    Model loading: models.json (user) > openclaw.json (auto) > empty
    """
    # --- models ---
    if models_path:
        models = load_models_from_file(models_path)
        # Intersect with actually available models from openclaw.json
        available = load_models_from_openclaw()
        available_ids = {m.id for m in available}
        before = len(models)
        models = [m for m in models if m.id in available_ids]
        removed = before - len(models)
        if removed > 0:
            removed_ids = [m.id for m in load_models_from_file(models_path) if m.id not in available_ids]
            print(f"[smart-model-router] Filtered {removed} unavailable model(s): {', '.join(removed_ids)}", file=sys.stderr)
            if not models:
                # Fallback to openclaw.json if all models were filtered out
                print("[smart-model-router] All models filtered; falling back to openclaw.json", file=sys.stderr)
                models = available
    else:
        models = load_models_from_openclaw()

    # --- user config overlay ---
    user_cfg = load_config_file(config_path)

    # --- build RouteConfig ---
    rc = RouteConfig()

    # Overlay weights
    if "dimensions" in user_cfg:
        w = user_cfg["dimensions"].get("weights")
        if isinstance(w, dict):
            rc.weights.update(w)
        t = user_cfg["dimensions"].get("thresholds")
        if isinstance(t, dict):
            rc.thresholds.update(t)

    # Overlay tiers
    if "tiers" in user_cfg:
        rc.tiers.update(user_cfg["tiers"])

    # Profile: CLI > env > config > default
    env_profile = os.environ.get("MODEL_ROUTER_PROFILE")
    if profile:
        rc.default_profile = profile
    elif env_profile:
        rc.default_profile = env_profile
    elif "profiles" in user_cfg and "default" in user_cfg["profiles"]:
        rc.default_profile = user_cfg["profiles"]["default"]

    rc.models = models
    return rc
