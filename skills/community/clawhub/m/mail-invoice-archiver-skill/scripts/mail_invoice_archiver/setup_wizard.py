from __future__ import annotations

import getpass
import sys
from pathlib import Path

from .auth import available_auth_methods, store_in_system_credentials
from .config import RuntimeConfig, apply_provider_defaults, default_config_path, write_config
from .providers import (
    default_system_service_name,
    get_mail_provider,
    list_mail_providers,
    normalize_mail_provider,
)
from .system_credentials import system_store_spec


def run_setup(
    *,
    config_path: Path | None = None,
    mail_provider: str | None = None,
    provider: str | None = None,
    email: str | None = None,
    secret: str | None = None,
    service: str | None = None,
    env_email_var: str | None = None,
    env_secret_var: str | None = None,
    interactive: bool = True,
) -> dict[str, object]:
    path = config_path or default_config_path()
    existing = RuntimeConfig.load(path) if path.exists() else RuntimeConfig()
    previous_mail_provider = existing.mail_provider

    chosen_provider = (provider or "").strip().lower() or None
    if chosen_provider is None:
        if not interactive or not sys.stdin.isatty():
            raise RuntimeError("Provider must be given in non-interactive setup")
        chosen_provider = _prompt_provider()

    cfg = existing
    cfg.auth_provider = chosen_provider
    cfg.email_address = email or cfg.email_address
    provider_was_explicit = mail_provider is not None
    cfg.mail_provider = normalize_mail_provider(mail_provider or cfg.mail_provider, cfg.email_address)
    if cfg.mail_provider == "custom" and interactive and not provider_was_explicit and sys.stdin.isatty():
        cfg.mail_provider = _prompt_mail_provider()
    prompt_provider = get_mail_provider(cfg.mail_provider, cfg.email_address)

    if chosen_provider == "system":
        if not cfg.email_address and interactive:
            cfg.email_address = input(f"{prompt_provider.display_name} email address: ").strip()
        if not provider_was_explicit:
            cfg.mail_provider = normalize_mail_provider(cfg.mail_provider, cfg.email_address)
        cfg = apply_provider_defaults(cfg)
        cfg.keychain_service = _resolve_system_service(
            existing_service=cfg.keychain_service,
            previous_mail_provider=previous_mail_provider,
            chosen_mail_provider=cfg.mail_provider,
            explicit_service=service,
        )
        prompt_provider = get_mail_provider(cfg.mail_provider, cfg.email_address)
        secret_value = secret
        if not secret_value and interactive:
            secret_value = getpass.getpass(f"{prompt_provider.display_name} {prompt_provider.secret_label}: ").strip()
        if not cfg.email_address or not secret_value:
            raise RuntimeError(f"System credential setup requires email and {prompt_provider.secret_label}")
        store_in_system_credentials(cfg.keychain_service, cfg.email_address, secret_value)
        cfg.auth_secret = ""
    elif chosen_provider == "env":
        cfg.env_email_var = env_email_var or cfg.env_email_var
        cfg.env_secret_var = env_secret_var or cfg.env_secret_var
        if not cfg.email_address and interactive:
            cfg.email_address = input(f"{prompt_provider.display_name} email address: ").strip()
        if not provider_was_explicit:
            cfg.mail_provider = normalize_mail_provider(cfg.mail_provider, cfg.email_address)
        cfg.auth_secret = ""
    elif chosen_provider == "config":
        if not cfg.email_address and interactive:
            cfg.email_address = input(f"{prompt_provider.display_name} email address: ").strip()
        if not provider_was_explicit:
            cfg.mail_provider = normalize_mail_provider(cfg.mail_provider, cfg.email_address)
        cfg = apply_provider_defaults(cfg)
        prompt_provider = get_mail_provider(cfg.mail_provider, cfg.email_address)
        secret_value = secret
        if not secret_value and interactive:
            secret_value = getpass.getpass(f"{prompt_provider.display_name} {prompt_provider.secret_label}: ").strip()
        if not cfg.email_address or not secret_value:
            raise RuntimeError(f"Config setup requires email and {prompt_provider.secret_label}")
        cfg.auth_secret = secret_value
    elif chosen_provider == "prompt":
        if not cfg.email_address and interactive:
            cfg.email_address = input(f"{prompt_provider.display_name} email address: ").strip()
        if not provider_was_explicit:
            cfg.mail_provider = normalize_mail_provider(cfg.mail_provider, cfg.email_address)
        if not cfg.email_address:
            raise RuntimeError("Prompt setup requires an email address")
        cfg.auth_secret = ""
    else:
        raise RuntimeError(f"Unknown setup provider: {chosen_provider}")

    cfg = apply_provider_defaults(cfg)
    provider_info = get_mail_provider(cfg.mail_provider, cfg.email_address)
    written = write_config(cfg, path)
    return {
        "setup_complete": True,
        "config_path": str(written),
        "mail_provider": cfg.mail_provider,
        "mail_provider_label": provider_info.display_name,
        "auth_provider": cfg.auth_provider,
        "email_address": cfg.email_address,
        "keychain_service": cfg.keychain_service,
        "env_email_var": cfg.env_email_var,
        "env_secret_var": cfg.env_secret_var,
        "post_setup_notes": _post_setup_notes(cfg),
    }


def _prompt_provider() -> str:
    methods = available_auth_methods()
    print("Choose credential storage:")
    valid: dict[str, str] = {}
    for index, method in enumerate(methods, start=1):
        status = []
        if method["recommended"]:
            status.append("recommended")
        if not method["available"]:
            status.append("unavailable")
        suffix = f" ({', '.join(status)})" if status else ""
        print(f"{index}. {method['label']}{suffix}")
        print(f"   {method['notes']}")
        valid[str(index)] = str(method["provider"])
    while True:
        choice = input("Select 1-4: ").strip()
        provider = valid.get(choice)
        if not provider:
            print("Please choose a valid option.")
            continue
        selected = next(item for item in methods if item["provider"] == provider)
        if not selected["available"]:
            print("That option is not available on this machine. Choose another one.")
            continue
        return provider


def _prompt_mail_provider() -> str:
    choices = list_mail_providers()
    print("Choose mailbox provider:")
    valid: dict[str, str] = {}
    for index, item in enumerate(choices, start=1):
        print(f"{index}. {item['display_name']} [{item['id']}]")
        print(f"   {item['notes']}")
        valid[str(index)] = str(item["id"])
    while True:
        choice = input(f"Select 1-{len(choices)}: ").strip()
        provider = valid.get(choice)
        if provider:
            return provider
        print("Please choose a valid option.")


def _post_setup_notes(config: RuntimeConfig) -> list[str]:
    provider = get_mail_provider(config.mail_provider, config.email_address)
    if config.auth_provider == "env":
        notes = [
            f"Set {config.env_email_var} to the {provider.display_name} email address.",
            f"Set {config.env_secret_var} to the {provider.secret_label}.",
            "Run doctor again after exporting those variables.",
        ]
        if provider.notes:
            notes.append(provider.notes)
        return notes
    if config.auth_provider == "prompt":
        return [f"The runtime will ask for the {provider.secret_label} every session."]
    if config.auth_provider == "config":
        notes = [f"The config file now contains the {provider.secret_label} in plain text; protect that file carefully."]
        if provider.notes:
            notes.append(provider.notes)
        return notes
    spec = system_store_spec()
    notes = [f"The {provider.secret_label} was stored in {spec['label']}."]
    if provider.notes:
        notes.append(provider.notes)
    return notes


def _resolve_system_service(
    *,
    existing_service: str,
    previous_mail_provider: str | None,
    chosen_mail_provider: str,
    explicit_service: str | None,
) -> str:
    if explicit_service:
        return explicit_service
    previous_default = default_system_service_name(previous_mail_provider)
    if not existing_service or existing_service == previous_default:
        return default_system_service_name(chosen_mail_provider)
    return existing_service
