"""Environment-backed configuration for local skill runs."""

from __future__ import annotations

from dataclasses import dataclass
import os


class ConfigurationError(ValueError):
    """Raised when environment configuration is invalid."""


def _read_bool(raw_value: str | None, *, default: bool = False) -> bool:
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for Portfolio Risk Desk.

    Redis and Notion writes are host-managed in production. The local runtime
    only needs handoff-oriented configuration such as a default target page.
    """

    civic_client_id: str | None = None
    apify_api_token: str | None = None
    apify_task_id: str | None = None
    apify_x_task_id: str | None = None
    apify_base_url: str = "https://api.apify.com/v2"
    apify_timeout_seconds: int = 120
    apify_max_items: int = 8
    apify_retry_attempts: int = 2
    local_state_dir: str | None = None
    notion_parent_page_id: str | None = None
    enable_live_providers: bool = False
    enable_x_signals: bool = True
    log_level: str = "WARNING"

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> "AppConfig":
        env = environ if environ is not None else os.environ
        config = cls(
            civic_client_id=env.get("CIVIC_CLIENT_ID"),
            apify_api_token=env.get("APIFY_API_TOKEN"),
            apify_task_id=env.get("APIFY_TASK_ID"),
            apify_x_task_id=env.get("APIFY_X_TASK_ID"),
            apify_base_url=env.get("APIFY_BASE_URL", "https://api.apify.com/v2"),
            apify_timeout_seconds=int(env.get("APIFY_TIMEOUT_SECONDS", "120")),
            apify_max_items=int(env.get("APIFY_MAX_ITEMS", "8")),
            apify_retry_attempts=int(env.get("APIFY_RETRY_ATTEMPTS", "2")),
            local_state_dir=env.get("LOCAL_STATE_DIR"),
            notion_parent_page_id=env.get("NOTION_PARENT_PAGE_ID"),
            enable_live_providers=_read_bool(env.get("ENABLE_LIVE_PROVIDERS")),
            enable_x_signals=_read_bool(env.get("ENABLE_X_SIGNALS"), default=True),
            log_level=env.get("LOG_LEVEL", "WARNING"),
        )
        config.validate()
        return config

    def validate(self) -> None:
        if self.enable_live_providers and not self.apify_api_token:
            raise ConfigurationError(
                "APIFY_API_TOKEN is required when ENABLE_LIVE_PROVIDERS is enabled."
            )
        if self.apify_timeout_seconds <= 0:
            raise ConfigurationError("APIFY_TIMEOUT_SECONDS must be a positive integer.")
        if self.apify_max_items <= 0:
            raise ConfigurationError("APIFY_MAX_ITEMS must be a positive integer.")
        if self.apify_retry_attempts <= 0:
            raise ConfigurationError("APIFY_RETRY_ATTEMPTS must be a positive integer.")
