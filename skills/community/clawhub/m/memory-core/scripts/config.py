import json
import os


def _skill_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_json(path: str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def _deep_merge(a: dict, b: dict) -> dict:
    out = dict(a or {})
    for k, v in (b or {}).items():
        if isinstance(out.get(k), dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _load_siliconflow_key_from_openclaw() -> dict:
    openclaw_path = os.path.expanduser("~/.openclaw/openclaw.json")
    cfg = _read_json(openclaw_path) or {}
    providers = (cfg.get("models") or {}).get("providers") or {}
    for k, p in providers.items():
        base = (p or {}).get("baseUrl") or ""
        if "siliconflow" in k or "siliconflow" in base:
            api_key = (p or {}).get("apiKey") or ""
            base_url = base or "https://api.siliconflow.cn/v1"
            return {"api_key": api_key, "base_url": base_url}
    return {}


def get_config() -> dict:
    root = _skill_root()
    defaults = {
        "embedding": {
            "provider": os.getenv("MEMORY_CORE_EMBEDDING_PROVIDER", "siliconflow"),
            "model": os.getenv("MEMORY_CORE_EMBEDDING_MODEL", "BAAI/bge-m3"),
            "api_key": os.getenv("MEMORY_CORE_EMBEDDING_API_KEY", ""),
            "base_url": os.getenv("MEMORY_CORE_EMBEDDING_BASE_URL", "https://api.siliconflow.cn/v1"),
            "timeout_sec": float(os.getenv("MEMORY_CORE_EMBEDDING_TIMEOUT_SEC", "15")),
            "max_input_chars": int(os.getenv("MEMORY_CORE_EMBEDDING_MAX_INPUT_CHARS", "2000")),
        },
        "lancedb": {
            "path": os.getenv("MEMORY_CORE_LANCEDB_PATH", os.path.join(root, "data", "memory.lance")),
            "max_results": int(os.getenv("MEMORY_CORE_MAX_RESULTS", "5")),
        },
        "memory": {
            "auto_budget": os.getenv("MEMORY_CORE_AUTO_BUDGET", "1") not in ("0", "false", "False"),
            "default_tier": os.getenv("MEMORY_CORE_DEFAULT_TIER", "medium"),
            "min_score": float(os.getenv("MEMORY_CORE_MIN_SCORE", "0")),
            "max_chars_per_memory": int(os.getenv("MEMORY_CORE_MAX_CHARS_PER_MEMORY", "600")),
            "max_total_chars": int(os.getenv("MEMORY_CORE_MAX_TOTAL_CHARS", "1800")),
            "tiers": {
                "small": {"max_chars_per_memory": 400, "max_total_chars": 1200},
                "medium": {"max_chars_per_memory": 600, "max_total_chars": 1800},
                "large": {"max_chars_per_memory": 900, "max_total_chars": 2700},
            },
        },
    }

    file_cfg = _read_json(os.path.join(root, "config.json")) or {}
    if any(
        k in file_cfg
        for k in [
            "embedding_provider",
            "embedding_model",
            "embedding_api_key",
            "embedding_base_url",
            "embedding_timeout_sec",
            "embedding_max_input_chars",
            "max_results",
            "auto_budget",
            "default_tier",
            "max_chars_per_memory",
            "max_total_chars",
            "min_score",
        ]
    ):
        file_cfg = _deep_merge(
            {
                "embedding": {
                    "provider": file_cfg.get("embedding_provider", defaults["embedding"]["provider"]),
                    "model": file_cfg.get("embedding_model", defaults["embedding"]["model"]),
                    "api_key": file_cfg.get("embedding_api_key", defaults["embedding"]["api_key"]),
                    "base_url": file_cfg.get("embedding_base_url", defaults["embedding"]["base_url"]),
                    "timeout_sec": file_cfg.get("embedding_timeout_sec", defaults["embedding"]["timeout_sec"]),
                    "max_input_chars": file_cfg.get("embedding_max_input_chars", defaults["embedding"]["max_input_chars"]),
                },
                "lancedb": {
                    "max_results": file_cfg.get("max_results", defaults["lancedb"]["max_results"]),
                },
                "memory": {
                    "auto_budget": file_cfg.get("auto_budget", defaults["memory"]["auto_budget"]),
                    "default_tier": file_cfg.get("default_tier", defaults["memory"]["default_tier"]),
                    "max_chars_per_memory": file_cfg.get("max_chars_per_memory", defaults["memory"]["max_chars_per_memory"]),
                    "max_total_chars": file_cfg.get("max_total_chars", defaults["memory"]["max_total_chars"]),
                    "min_score": file_cfg.get("min_score", defaults["memory"]["min_score"]),
                },
            },
            file_cfg,
        )
    cfg = _deep_merge(defaults, file_cfg)

    if cfg.get("embedding", {}).get("provider") == "siliconflow" and not cfg.get("embedding", {}).get("api_key"):
        sf = _load_siliconflow_key_from_openclaw()
        cfg["embedding"] = _deep_merge(cfg.get("embedding") or {}, sf)

    return cfg
