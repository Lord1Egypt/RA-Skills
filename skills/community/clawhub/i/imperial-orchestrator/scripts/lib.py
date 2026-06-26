#!/usr/bin/env python3
"""Imperial Orchestrator core library.

Auto-discovers models from openclaw.json, classifies capabilities,
manages health state, and provides routing utilities.
"""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install with: python3 -m pip install --user --break-system-packages pyyaml"
    ) from exc


# ── File I/O ──────────────────────────────────────────────────────────

def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def now_ts() -> int:
    return int(time.time())


# ── Data Classes ──────────────────────────────────────────────────────

@dataclass
class ModelInfo:
    model_ref: str
    provider: str
    auth_group: str
    local: bool = False
    capabilities: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    context_window: int = 32768
    latency_tier: str = "medium"
    cost_tier: str = "medium"
    input_types: List[str] = field(default_factory=lambda: ["text"])
    is_embedding: bool = False
    is_image_gen: bool = False


@dataclass
class HealthInfo:
    status: str = "unknown"  # healthy/degraded/auth_dead/cooldown/down
    last_error: Optional[str] = None
    last_checked: Optional[int] = None
    cooldown_until: Optional[int] = None
    auth_error_count: int = 0
    recent_failures: int = 0
    recent_successes: int = 0

    def healthy(self, now: Optional[int] = None) -> bool:
        n = now or now_ts()
        if self.cooldown_until and self.cooldown_until > n:
            return False
        return self.status in {"healthy", "unknown", "degraded"}


# ── Capability Inference ──────────────────────────────────────────────

# Known model families and their capabilities
MODEL_CAPABILITY_MAP = {
    # Anthropic
    "claude-opus": ["reasoning_high", "coding_strong", "writing_strong", "tool_use_stable"],
    "claude-sonnet": ["reasoning_mid", "coding_strong", "writing_good", "tool_use_stable"],
    "claude-haiku": ["cheap_fast", "coding_good", "writing_good", "stable_generalist"],
    # OpenAI
    "gpt-4o": ["reasoning_mid", "coding_good", "writing_good", "stable_generalist", "tool_use_stable"],
    "gpt-4.1": ["reasoning_mid", "coding_good", "writing_good", "stable_generalist"],
    "gpt-5": ["reasoning_high", "coding_strong", "tool_use_stable"],
    "o1": ["reasoning_high", "coding_strong"],
    "o3": ["reasoning_high", "coding_strong"],
    "o4": ["reasoning_high", "coding_strong"],
    # Qwen
    "qwen": ["reasoning_mid", "coding_good", "ops_good"],
    # DeepSeek
    "deepseek": ["reasoning_mid", "coding_strong", "cheap_fast"],
    # Kimi / Moonshot
    "kimi": ["reasoning_high", "writing_strong", "tool_use_stable"],
    "moonshot": ["reasoning_mid", "writing_good"],
    # MiniMax
    "minimax": ["reasoning_mid", "writing_good", "stable_generalist"],
    # Local models
    "gpt-oss": ["coding_good", "local_private", "cheap_fast", "survival_ready"],
    "abliterated": ["coding_good", "local_private", "survival_ready"],
    "llama": ["coding_good", "local_private", "survival_ready"],
    "mistral": ["coding_good", "local_private", "survival_ready"],
    "codestral": ["coding_strong", "local_private", "survival_ready"],
    "gemma": ["cheap_fast", "local_private", "survival_ready"],
}

# Role assignment based on capabilities
CAPABILITY_TO_ROLES = {
    "reasoning_high": ["cabinet-planner", "censor-review"],
    "reasoning_mid": ["router-chief", "cabinet-planner"],
    "coding_strong": ["ministry-coding"],
    "coding_good": ["ministry-coding", "ministry-ops"],
    "writing_strong": ["ministry-writing"],
    "writing_good": ["ministry-writing"],
    "ops_good": ["ministry-ops"],
    "stable_generalist": ["router-chief", "ministry-writing"],
    "cheap_fast": ["router-chief", "emergency-scribe"],
    "local_private": ["emergency-scribe"],
    "survival_ready": ["emergency-scribe"],
    "tool_use_stable": ["ministry-ops", "ministry-coding"],
}

# Embedding / non-chat model patterns (to exclude from routing)
EMBEDDING_PATTERNS = [
    "embed", "embedding", "nomic", "text-embedding", "bge-", "e5-",
    "clip", "jina-embeddings",
]

IMAGE_GEN_PATTERNS = [
    "dall-e", "stable-diffusion", "midjourney", "imagen", "flux",
]

# Local provider names
LOCAL_PROVIDERS = {"ollama", "ollma", "localhost", "local", "lmstudio"}


def is_embedding_model(model_id: str) -> bool:
    """Check if a model is an embedding model (not for chat routing)."""
    lower = model_id.lower()
    return any(p in lower for p in EMBEDDING_PATTERNS)


def is_image_gen_model(model_id: str) -> bool:
    """Check if a model is an image generation model."""
    lower = model_id.lower()
    return any(p in lower for p in IMAGE_GEN_PATTERNS)


def infer_capabilities(model_id: str, provider: str, local: bool) -> List[str]:
    """Infer model capabilities from its name and provider."""
    lower = model_id.lower()
    caps = set()

    for pattern, pattern_caps in MODEL_CAPABILITY_MAP.items():
        if pattern in lower:
            caps.update(pattern_caps)

    # If nothing matched, give generic caps
    if not caps:
        if local:
            caps = {"local_private", "survival_ready", "cheap_fast"}
        else:
            caps = {"stable_generalist"}

    # Local models always get these
    if local:
        caps.add("local_private")
        caps.add("survival_ready")

    return sorted(caps)


def infer_roles(capabilities: List[str]) -> List[str]:
    """Infer suitable roles from capabilities."""
    roles = set()
    for cap in capabilities:
        if cap in CAPABILITY_TO_ROLES:
            roles.update(CAPABILITY_TO_ROLES[cap])
    return sorted(roles) if roles else ["emergency-scribe"]


def infer_cost_tier(cost_input: float, local: bool) -> str:
    """Infer cost tier from per-MTok input price."""
    if local or cost_input == 0:
        return "free"
    if cost_input <= 1:
        return "low"
    if cost_input <= 5:
        return "medium"
    return "high"


def infer_latency_tier(local: bool, context_window: int) -> str:
    """Rough latency inference."""
    if local:
        return "slow"
    if context_window >= 200000:
        return "medium"  # Large context models tend to be slower
    return "fast"


# ── OpenClaw Config Parsing ───────────────────────────────────────────

def read_openclaw_config(path: Optional[Path] = None) -> Dict[str, Any]:
    """Read openclaw.json, searching default paths if none given."""
    search_paths = []
    if path:
        search_paths.append(path)
    search_paths.extend([
        Path.home() / ".openclaw" / "openclaw.json",
        Path("/etc/openclaw/openclaw.json"),
    ])
    for p in search_paths:
        if p.exists():
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
    return {}


def extract_models_from_config(openclaw_config: Dict[str, Any]) -> List[ModelInfo]:
    """Extract all chat-capable models from openclaw.json providers section."""
    models = []
    providers_cfg = openclaw_config.get("models", {}).get("providers", {})

    for provider_key, provider_data in providers_cfg.items():
        is_local = provider_key.lower() in LOCAL_PROVIDERS
        provider_api = provider_data.get("api", "")
        auth_group = f"{provider_key}-default"

        for model_cfg in provider_data.get("models", []):
            model_id = model_cfg.get("id", "")
            if not model_id:
                continue

            # Skip embedding and image-gen models
            if is_embedding_model(model_id):
                continue
            if is_image_gen_model(model_id):
                continue

            full_ref = f"{provider_key}/{model_id}"
            context_window = int(model_cfg.get("contextWindow", 32768))
            cost_input = float(model_cfg.get("cost", {}).get("input", 0))
            input_types = model_cfg.get("input", ["text"])

            capabilities = infer_capabilities(model_id, provider_key, is_local)
            roles = infer_roles(capabilities)
            cost_tier = infer_cost_tier(cost_input, is_local)
            latency_tier = infer_latency_tier(is_local, context_window)

            models.append(ModelInfo(
                model_ref=full_ref,
                provider=provider_key,
                auth_group=auth_group,
                local=is_local,
                capabilities=capabilities,
                roles=roles,
                context_window=context_window,
                latency_tier=latency_tier,
                cost_tier=cost_tier,
                input_types=input_types,
            ))

    # Also check for default/fallback models referenced at top level
    defaults = openclaw_config.get("agents", {}).get("defaults", {})
    for key in ["model", "fallbackModel", "imageModel"]:
        val = defaults.get(key)
        if val and isinstance(val, str):
            # Check if already discovered
            if not any(m.model_ref == val for m in models):
                provider = val.split("/", 1)[0] if "/" in val else "unknown"
                model_id = val.split("/", 1)[1] if "/" in val else val
                if not is_embedding_model(model_id) and not is_image_gen_model(model_id):
                    is_local = provider.lower() in LOCAL_PROVIDERS
                    capabilities = infer_capabilities(model_id, provider, is_local)
                    models.append(ModelInfo(
                        model_ref=val,
                        provider=provider,
                        auth_group=f"{provider}-default",
                        local=is_local,
                        capabilities=capabilities,
                        roles=infer_roles(capabilities),
                    ))

    return models


# ── Task Classification ───────────────────────────────────────────────

KEYWORDS_COMPLEX = {
    "architecture", "设计", "重构", "cluster", "distributed", "high availability",
    "multi", "复杂", "审计", "secure", "security", "incident", "合规",
    "redesign", "migration", "refactor",
}

DOMAIN_KEYWORDS = {
    "ministry-coding": {
        "code", "coding", "golang", "rust", "swift", "flutter", "api",
        "gorm", "wireguard", "bug", "debug", "fix", "refactor",
        "function", "class", "module", "compile", "build", "test",
        "typescript", "python", "java", "react", "vue", "nextjs",
        "代码", "函数", "接口", "重构", "编译", "调试", "算法",
    },
    "ministry-ops": {
        "docker", "k8s", "deploy", "systemd", "linux", "ceph", "nginx",
        "openresty", "iptables", "nftables", "infra", "server", "ssh",
        "backup", "cron", "ci", "cd", "pipeline", "terraform", "ansible",
        "cloudflare", "dns", "ssl", "certificate",
        "部署", "运维", "服务器", "容器", "集群", "网络", "防火墙",
    },
    "ministry-security": {
        "security", "harden", "threat", "oauth", "abuse", "cve", "vuln",
        "firewall", "encryption", "permission", "credential", "2fa", "mfa",
        "injection", "xss", "csrf",
        "注入", "漏洞", "安全审计", "安全漏洞", "安全审查", "加固", "威胁", "渗透", "越权", "提权",
    },
    "ministry-writing": {
        "文案", "title", "banner", "readme", "copy", "docs", "documentation",
        "marketing", "blog", "article", "translate", "翻译", "translation",
        "content", "seo", "summary",
        "写作", "文章", "摘要", "标语", "简介", "标题",
    },
    "ministry-legal": {
        "合同", "条款", "policy", "terms", "privacy", "agreement", "compliance",
        "contract", "legal", "license", "gdpr",
        "隐私", "协议", "法律", "法务", "合规",
    },
    "ministry-finance": {
        "price", "pricing", "margin", "收益", "apy", "settlement",
        "commission", "budget", "revenue", "profit",
        "毛利", "定价", "财务", "利润", "回本", "年化",
    },
}


def tokenize_task(task: str) -> List[str]:
    parts = re.split(r"[^\w\u4e00-\u9fff\-\.]+", task.lower())
    return [p for p in parts if p]


def infer_complexity(task: str) -> str:
    text = task.lower()
    tokens = set(tokenize_task(task))
    score = 0
    if len(task) > 180:
        score += 1
    if any(k in text for k in KEYWORDS_COMPLEX):
        score += 2
    if any(word in tokens for word in ["plan", "phase", "roadmap", "review", "audit"]):
        score += 1
    if score >= 3:
        return "high"
    if score >= 1:
        return "medium"
    return "low"


def match_role_by_keywords(task: str) -> Optional[str]:
    tokens = set(tokenize_task(task))
    text = task.lower()
    best: Optional[Tuple[str, int]] = None
    for role, words in DOMAIN_KEYWORDS.items():
        hits = sum(1 for w in words if w in tokens or w in text)
        if hits and (best is None or hits > best[1]):
            best = (role, hits)
    return best[0] if best else None


# ── Registry ──────────────────────────────────────────────────────────

class I18n:
    """Multi-language support. Loads from config/i18n.yaml."""

    def __init__(self, root: Path, lang: str = ""):
        self._cfg = load_yaml(root / "config" / "i18n.yaml")
        self._lang = lang or self._cfg.get("default_language", "zh")
        self._titles = self._cfg.get("role_titles", {})
        self._modes = self._cfg.get("modes", {})
        self._msgs = self._cfg.get("messages", {})
        self._routing_kw = self._cfg.get("routing_keywords_i18n", {})

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str) -> None:
        self._lang = value

    def role_title(self, role: str, lang: str = "") -> str:
        lk = lang or self._lang
        return self._titles.get(role, {}).get(lk, role)

    def mode_label(self, mode: str, lang: str = "") -> str:
        lk = lang or self._lang
        return self._modes.get(mode, {}).get(lk, mode)

    def msg(self, key: str, lang: str = "", **kwargs: Any) -> str:
        lk = lang or self._lang
        template = self._msgs.get(key, {}).get(lk, "")
        if not template:
            template = self._msgs.get(key, {}).get("en", key)
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template

    def routing_keywords(self, category: str) -> List[str]:
        """Return extra routing keywords for all i18n languages."""
        extra: List[str] = []
        cat_kw = self._routing_kw.get(category, {})
        for lang_kws in cat_kw.values():
            if isinstance(lang_kws, list):
                extra.extend(lang_kws)
        return extra

    @property
    def available_languages(self) -> List[str]:
        return self._cfg.get("languages", ["zh", "en"])


class Registry:
    def __init__(self, root: Path, lang: str = ""):
        self.root = root
        self.model_cfg = load_yaml(root / "config" / "model_registry.yaml")
        self.roles_cfg = load_yaml(root / "config" / "agent_roles.yaml")
        self.rules_cfg = load_yaml(root / "config" / "routing_rules.yaml")
        self.fail_cfg = load_yaml(root / "config" / "failure_policies.yaml")
        self.prompts_cfg = load_yaml(root / "config" / "agent_prompts.yaml")
        self.i18n = I18n(root, lang)

    def get_system_prompt(self, role: str) -> Optional[str]:
        """Return the deep system prompt for a role, or None if not defined."""
        prompts = self.prompts_cfg.get("prompts", {})
        role_prompt = prompts.get(role, {})
        return role_prompt.get("system_prompt")

    def get_role_metadata(self, role: str) -> Dict[str, Any]:
        """Return full role metadata including title, imperial_analog, forbidden_actions."""
        return self.roles_cfg.get("roles", {}).get(role, {})

    def known_models(self) -> Dict[str, ModelInfo]:
        """Return manually registered models (from registry yaml)."""
        defaults = self.model_cfg.get("defaults", {})
        items = {}
        for ref, cfg in (self.model_cfg.get("models") or {}).items():
            items[ref] = ModelInfo(
                model_ref=ref,
                provider=cfg.get("provider") or ref.split("/", 1)[0],
                auth_group=cfg.get("auth_group") or (cfg.get("provider") or ref.split("/", 1)[0]),
                local=bool(cfg.get("local", False)),
                capabilities=list(cfg.get("capabilities", [])),
                roles=list(cfg.get("roles", [])),
                context_window=int(cfg.get("context_window", defaults.get("default_context_window", 32768))),
                latency_tier=cfg.get("latency_tier", defaults.get("default_latency_tier", "medium")),
                cost_tier=cfg.get("cost_tier", defaults.get("default_cost_tier", "medium")),
            )
        return items

    def overrides(self) -> Dict[str, Dict[str, Any]]:
        """Return manual overrides section."""
        return self.model_cfg.get("overrides", {}) or {}


# ── State Management ──────────────────────────────────────────────────

def build_initial_state(reg: Registry, openclaw_config: Dict[str, Any]) -> Dict[str, Any]:
    """Build state from auto-discovered models + manual overrides."""
    # Auto-discover from openclaw.json
    discovered = extract_models_from_config(openclaw_config)

    # Also include manually registered models
    known = reg.known_models()
    overrides = reg.overrides()

    models: Dict[str, Any] = {}

    # Add auto-discovered models
    for info in discovered:
        data = asdict(info)
        data["health"] = asdict(HealthInfo())
        data["source"] = "auto"
        models[info.model_ref] = data

    # Enrich with per-model api_type from openclaw.json
    providers_cfg = openclaw_config.get("models", {}).get("providers", {})
    for provider_key, provider_data in providers_cfg.items():
        for model_cfg in provider_data.get("models", []):
            model_id = model_cfg.get("id", "")
            if not model_id:
                continue
            full_ref = f"{provider_key}/{model_id}"
            if full_ref in models:
                models[full_ref]["api_type"] = (model_cfg.get("api") or provider_data.get("api") or "openai-completions").lower()

    # Add/merge manually registered models
    for ref, info in known.items():
        if ref in models:
            # Manual registry overrides auto-discovered
            models[ref].update({
                "capabilities": info.capabilities or models[ref].get("capabilities", []),
                "roles": info.roles or models[ref].get("roles", []),
                "source": "registry+auto",
            })
        else:
            data = asdict(info)
            data["health"] = asdict(HealthInfo())
            data["source"] = "registry"
            models[ref] = data

    # Apply overrides
    for ref, overr in overrides.items():
        if ref in models:
            for k, v in overr.items():
                if k in ("capabilities", "roles") and isinstance(v, list):
                    existing = set(models[ref].get(k, []))
                    existing.update(v)
                    models[ref][k] = sorted(existing)
                else:
                    models[ref][k] = v

    return {
        "generated_at": now_ts(),
        "models": models,
        "providers": {},
        "auth_groups": {},
    }


def refresh_group_summaries(state: Dict[str, Any]) -> None:
    providers: Dict[str, Dict[str, Any]] = {}
    auth_groups: Dict[str, Dict[str, Any]] = {}
    n = now_ts()

    for model_ref, data in state.get("models", {}).items():
        provider = data.get("provider", "unknown")
        auth_group = data.get("auth_group", provider)
        health = data.get("health", {})
        ok = HealthInfo(**health).healthy(n)

        providers.setdefault(provider, {"healthy_models": 0, "models": []})
        providers[provider]["models"].append(model_ref)
        providers[provider]["healthy_models"] += 1 if ok else 0

        auth_groups.setdefault(auth_group, {"healthy_models": 0, "models": []})
        auth_groups[auth_group]["models"].append(model_ref)
        auth_groups[auth_group]["healthy_models"] += 1 if ok else 0

    state["providers"] = providers
    state["auth_groups"] = auth_groups


def record_failure(state: Dict[str, Any], model_ref: str, error_type: str, cooldown_seconds: int = 600) -> None:
    model = state.get("models", {}).get(model_ref)
    if not model:
        return
    h = model.setdefault("health", {})
    now = now_ts()
    h["last_checked"] = now
    h["last_error"] = error_type
    h["recent_failures"] = int(h.get("recent_failures", 0)) + 1

    auth_error_types = {"auth", "401", "invalid_api_key", "invalid_access_token", "expired_token"}
    if error_type in auth_error_types:
        h["status"] = "auth_dead"
        h["auth_error_count"] = int(h.get("auth_error_count", 0)) + 1
        h["cooldown_until"] = now + cooldown_seconds
        auth_group = model.get("auth_group")
        if auth_group:
            for _, sibling in state.get("models", {}).items():
                if sibling.get("auth_group") == auth_group:
                    sh = sibling.setdefault("health", {})
                    sh["status"] = "cooldown" if sibling is not model else "auth_dead"
                    sh["cooldown_until"] = now + cooldown_seconds
                    sh["last_error"] = f"auth_group:{error_type}"
    elif error_type == "timeout":
        h["status"] = "degraded"
    else:
        h["status"] = "down"
        h["cooldown_until"] = now + min(cooldown_seconds, 300)

    refresh_group_summaries(state)


def record_success(state: Dict[str, Any], model_ref: str) -> None:
    model = state.get("models", {}).get(model_ref)
    if not model:
        return
    h = model.setdefault("health", {})
    h["last_checked"] = now_ts()
    h["last_error"] = None
    h["status"] = "healthy"
    h["recent_successes"] = int(h.get("recent_successes", 0)) + 1
    h["cooldown_until"] = None
    refresh_group_summaries(state)


def count_healthy_models(state: Dict[str, Any]) -> int:
    c = 0
    for data in state.get("models", {}).values():
        if HealthInfo(**data.get("health", {})).healthy():
            c += 1
    return c


# ── Token Estimation ─────────────────────────────────────────────────

def estimate_tokens(text: str) -> int:
    """粗略估算 token 数。中文约 1.5 token/字，英文约 1.3 token/word。"""
    if not text:
        return 0
    # 分离中文字符和非中文
    cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    remaining = re.sub(r"[\u4e00-\u9fff]", "", text)
    en_words = len(remaining.split())
    # 中文: ~1.5 token/字, 英文: ~1.3 token/word, 标点等: ~1 token each
    return int(cn_chars * 1.5 + en_words * 1.3 + 10)


# 每百万 token 的价格（美元），用于成本计算
# 格式: model_pattern -> (input_price_per_mtok, output_price_per_mtok)
MODEL_PRICING = {
    "claude-opus": (15.0, 75.0),
    "claude-sonnet": (3.0, 15.0),
    "claude-haiku": (0.25, 1.25),
    "gpt-4o": (2.5, 10.0),
    "gpt-4.1": (2.0, 8.0),
    "gpt-5": (10.0, 30.0),
    "o1": (15.0, 60.0),
    "o3": (10.0, 40.0),
    "o4": (10.0, 40.0),
    "deepseek": (0.27, 1.1),
    "qwen": (0.8, 2.0),
    "kimi": (1.0, 3.0),
    "moonshot": (1.0, 3.0),
    "minimax": (0.5, 1.5),
}


def lookup_pricing(model_ref: str) -> Tuple[float, float]:
    """查找模型价格（每百万 token）。返回 (input_price, output_price)。"""
    lower = model_ref.lower()
    for pattern, pricing in MODEL_PRICING.items():
        if pattern in lower:
            return pricing
    return (1.0, 3.0)  # 默认估价


def calculate_cost(model_ref: str, input_tokens: int, output_tokens: int) -> float:
    """计算单次调用成本（美元）。"""
    input_price, output_price = lookup_pricing(model_ref)
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000


# ── Rate Limiter ─────────────────────────────────────────────────────

class RateLimiter:
    """基于滑动窗口的简易速率限制器。追踪每个 provider 的请求频率。"""

    def __init__(self, window_seconds: int = 60, max_requests: int = 60):
        self.window = window_seconds
        self.max_requests = max_requests
        self._requests: Dict[str, List[float]] = {}  # provider -> [timestamps]

    def _clean(self, provider: str) -> None:
        cutoff = time.time() - self.window
        self._requests[provider] = [
            t for t in self._requests.get(provider, []) if t > cutoff
        ]

    def can_request(self, provider: str) -> bool:
        self._clean(provider)
        return len(self._requests.get(provider, [])) < self.max_requests

    def record_request(self, provider: str) -> None:
        self._requests.setdefault(provider, []).append(time.time())
        self._clean(provider)

    def wait_time(self, provider: str) -> float:
        """返回需要等待的秒数。0 = 可以立即请求。"""
        self._clean(provider)
        reqs = self._requests.get(provider, [])
        if len(reqs) < self.max_requests:
            return 0.0
        oldest = min(reqs)
        return max(0.0, oldest + self.window - time.time())

    def usage_ratio(self, provider: str) -> float:
        """当前窗口使用率 (0.0 ~ 1.0)。"""
        self._clean(provider)
        return len(self._requests.get(provider, [])) / self.max_requests


# ── Audit Log ────────────────────────────────────────────────────────

class AuditLog:
    """结构化审计日志，记录每次路由和执行决策。"""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self._entries: List[Dict[str, Any]] = []
        if log_file.exists():
            try:
                data = json.loads(log_file.read_text(encoding="utf-8"))
                self._entries = data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError):
                self._entries = []

    def log(self, event: str, **kwargs: Any) -> None:
        entry = {
            "ts": now_ts(),
            "event": event,
            **kwargs,
        }
        self._entries.append(entry)
        # 只保留最近 500 条
        if len(self._entries) > 500:
            self._entries = self._entries[-500:]

    def flush(self) -> None:
        self.log_file.write_text(
            json.dumps(self._entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def recent(self, n: int = 20) -> List[Dict[str, Any]]:
        return self._entries[-n:]

    def stats(self) -> Dict[str, Any]:
        """聚合统计。"""
        total = len(self._entries)
        by_event: Dict[str, int] = {}
        total_cost = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        model_usage: Dict[str, int] = {}

        for e in self._entries:
            ev = e.get("event", "unknown")
            by_event[ev] = by_event.get(ev, 0) + 1
            total_cost += e.get("cost_usd", 0)
            total_input_tokens += e.get("input_tokens", 0)
            total_output_tokens += e.get("output_tokens", 0)
            model = e.get("model")
            if model:
                model_usage[model] = model_usage.get(model, 0) + 1

        return {
            "total_entries": total,
            "by_event": by_event,
            "total_cost_usd": round(total_cost, 4),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "model_usage": model_usage,
        }
