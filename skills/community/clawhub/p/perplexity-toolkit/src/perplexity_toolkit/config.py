"""Configuration management for Perplexity Toolkit."""

import logging
import os
import uuid
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


def _default_session_prefix() -> str:
    """Give each CLI process an isolated default WebBridge session namespace."""
    return f"perplexity-{os.getpid()}-{uuid.uuid4().hex[:8]}"


@dataclass
class Config:
    """Global configuration."""

    # Browser driver
    # Only 'webbridge' is implemented. See drivers/DRIVER_REGISTRY — that is the
    # authoritative list; do not name aspirational backends here.
    driver_backend: str = "webbridge"
    locale: str = "zh"  # 'zh' or 'en'
    webbridge_url: str = "http://127.0.0.1:10086/command"
    # A caller can override this with PERPLEXITY_SESSION_PREFIX when a
    # multi-process workflow must continue the same task thread.
    session_prefix: str = field(default_factory=_default_session_prefix)

    # Perplexity
    base_url: str = "https://www.perplexity.ai"

    # Timing
    page_load_wait: float = 4.0
    search_wait: float = 15.0
    deep_research_wait: float = 90.0
    model_council_wait: float = 25.0
    step_by_step_wait: float = 20.0
    mode_switch_wait: float = 1.0
    action_wait: float = 0.5

    # Retry
    max_retries: int = 3

    # Batch
    batch_delay: float = 3.0
    batch_progress_file: str = ".batch_progress"

    def make_session(self, suffix: str = "search") -> str:
        """Generate a task-scoped session name for the requested mode."""
        return self.session_prefix if not suffix else f"{self.session_prefix}-{suffix}"


# Env var name -> Config field (all prefixed PERPLEXITY_)
_ENV_FIELDS = {
    "PERPLEXITY_DRIVER": "driver_backend",
    "PERPLEXITY_LOCALE": "locale",
    "PERPLEXITY_WEBBRIDGE_URL": "webbridge_url",
    "PERPLEXITY_BASE_URL": "base_url",
    "PERPLEXITY_SESSION_PREFIX": "session_prefix",
    "PERPLEXITY_PAGE_LOAD_WAIT": "page_load_wait",
    "PERPLEXITY_SEARCH_WAIT": "search_wait",
    "PERPLEXITY_DEEP_RESEARCH_WAIT": "deep_research_wait",
    "PERPLEXITY_MODEL_COUNCIL_WAIT": "model_council_wait",
    "PERPLEXITY_STEP_BY_STEP_WAIT": "step_by_step_wait",
    "PERPLEXITY_MODE_SWITCH_WAIT": "mode_switch_wait",
    "PERPLEXITY_ACTION_WAIT": "action_wait",
    "PERPLEXITY_MAX_RETRIES": "max_retries",
    "PERPLEXITY_BATCH_DELAY": "batch_delay",
    "PERPLEXITY_BATCH_PROGRESS_FILE": "batch_progress_file",
}


def _env_overrides(cfg: Config) -> Config:
    """Apply PERPLEXITY_* environment variable overrides to a config."""
    for env_name, field_name in _ENV_FIELDS.items():
        value = os.environ.get(env_name)
        if value is None or value == "":
            continue
        current = getattr(cfg, field_name)
        if isinstance(current, float):
            try:
                value = float(value)
            except ValueError:
                continue
        elif isinstance(current, int):
            try:
                value = int(value)
            except ValueError:
                continue
        setattr(cfg, field_name, value)
        logger.debug("Config override: %s=%r (from env %s)", field_name, value, env_name)
    return cfg


# Singleton default config
_default: Config = Config()


def get_config() -> Config:
    return _env_overrides(_default)


def set_config(**kwargs) -> Config:
    """Update default config and return it."""
    global _default
    for k, v in kwargs.items():
        if hasattr(_default, k):
            setattr(_default, k, v)
    return _default
