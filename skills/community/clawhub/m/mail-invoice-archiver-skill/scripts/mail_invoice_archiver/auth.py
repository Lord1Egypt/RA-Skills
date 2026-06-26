from __future__ import annotations

import getpass
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from .config import RuntimeConfig, default_config_path
from .providers import get_mail_provider, list_mail_providers
from .system_credentials import read_system_secret, store_system_secret, system_store_spec


@dataclass(slots=True)
class ResolvedCredentials:
    email: str
    secret: str
    provider: str
    detail: str


class SetupRequiredError(RuntimeError):
    def __init__(self, config_path: Path | None = None) -> None:
        path = config_path or default_config_path()
        super().__init__(f"Setup required. Run setup first and save configuration to {path}.")
        self.config_path = path


def available_auth_methods() -> list[dict[str, object]]:
    methods: list[dict[str, object]] = []
    system_spec = system_store_spec()
    system_available = bool(system_spec["available"])
    methods.append(
        {
            "provider": "system",
            "label": "system credential store",
            "recommended": bool(system_spec["recommended"]),
            "available": system_available,
            "notes": str(system_spec["notes"]),
        }
    )
    methods.append(
        {
            "provider": "env",
            "label": "environment variables",
            "recommended": not bool(system_spec["recommended"]),
            "available": True,
            "notes": "Cross-platform and good for CI or controlled shell sessions.",
        }
    )
    methods.append(
        {
            "provider": "config",
            "label": "config file",
            "recommended": False,
            "available": True,
            "notes": "Cross-platform but stores the authorization code in plain text.",
        }
    )
    methods.append(
        {
            "provider": "prompt",
            "label": "prompt each session",
            "recommended": False,
            "available": True,
            "notes": "Stores no secret, but asks for the authorization code every time.",
        }
    )
    return methods


def setup_required_payload(config_path: Path | None = None) -> dict[str, object]:
    path = config_path or default_config_path()
    return {
        "setup_required": True,
        "config_path": str(path),
        "available_mail_providers": list_mail_providers(),
        "available_auth_methods": available_auth_methods(),
        "next_step": "Run setup and ask the user which mailbox provider and credential storage mode they want.",
    }


def resolve_credentials(
    config: RuntimeConfig,
    *,
    config_path: Path | None = None,
    allow_prompt: bool = True,
) -> ResolvedCredentials:
    provider = (config.auth_provider or "").strip().lower() or "system"
    if provider == "system":
        return _resolve_system_credentials(config)
    if provider == "env":
        return _resolve_env_credentials(config)
    if provider == "config":
        return _resolve_config_credentials(config)
    if provider == "prompt":
        if not allow_prompt:
            raise RuntimeError("Prompt auth provider requires interactive input")
        return _resolve_prompt_credentials(config)
    raise RuntimeError(f"Unknown auth provider: {provider}")


def store_in_system_credentials(service: str, email: str, secret: str) -> None:
    spec = system_store_spec()
    if not spec["available"]:
        raise RuntimeError("System credential store is not available on this machine; use env, config, or prompt")
    store_system_secret(service, email, secret)


def _resolve_system_credentials(config: RuntimeConfig) -> ResolvedCredentials:
    spec = system_store_spec()
    if not spec["available"]:
        raise RuntimeError("System credential store is not available on this machine; use env, config, or prompt")
    email, secret = read_system_secret(config.keychain_service)
    return ResolvedCredentials(
        email=config.email_address or email,
        secret=secret,
        provider="system",
        detail=f"{spec['label']} entry {config.keychain_service}",
    )


def _resolve_env_credentials(config: RuntimeConfig) -> ResolvedCredentials:
    email = os.getenv(config.env_email_var) or config.email_address
    secret = os.getenv(config.env_secret_var)
    if not email or not secret:
        raise RuntimeError(
            f"Environment auth is not ready. Set {config.env_email_var} and {config.env_secret_var}."
        )
    return ResolvedCredentials(
        email=email,
        secret=secret,
        provider="env",
        detail=f"{config.env_email_var} / {config.env_secret_var}",
    )


def _resolve_config_credentials(config: RuntimeConfig) -> ResolvedCredentials:
    if not config.email_address or not config.auth_secret:
        raise RuntimeError("Config auth is incomplete; both email and secret must be present in the config file.")
    return ResolvedCredentials(
        email=config.email_address,
        secret=config.auth_secret,
        provider="config",
        detail="plain-text config secret",
    )


def _resolve_prompt_credentials(config: RuntimeConfig) -> ResolvedCredentials:
    if not sys.stdin.isatty():
        raise RuntimeError("Prompt auth requires an interactive terminal")
    provider = get_mail_provider(config.mail_provider, config.email_address)
    email = config.email_address or input(f"{provider.display_name} email address: ").strip()
    if not email:
        raise RuntimeError("Email address is required")
    secret = getpass.getpass(f"{provider.display_name} {provider.secret_label}: ").strip()
    if not secret:
        raise RuntimeError(f"{provider.secret_label.capitalize()} is required")
    return ResolvedCredentials(
        email=email,
        secret=secret,
        provider="prompt",
        detail="prompted in the current session",
    )
