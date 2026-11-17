"""`kalo config` — show/save credentials and defaults."""

from __future__ import annotations

import json

from .. import config as config_mod
from .. import onboarding, render, validate
from ..core import Command, Flag
from ..errors import UsageError


def config_show(cfg, opts, args):
    path = config_mod.config_path()
    masked = "missing"
    if cfg.api_key:
        masked = f"set (…{cfg.api_key[-4:]})" if len(cfg.api_key) > 4 else "set"
    data = {
        "file": str(path) + ("" if path.exists() else " (missing)"),
        "api_key": masked,
        "base_url": cfg.base_url,
        "defaults": f"region {cfg.region} · language {cfg.language} · currency {cfg.currency}",
    }
    if opts.get("json"):
        render.out(json.dumps(data, ensure_ascii=False))
        return 0
    render.emit_detail("config", data)
    if not cfg.authed:
        render.emit_help(onboarding.SETUP_LINES)
    return 0


def config_set(cfg, opts, args):
    updates = {
        "api_key": opts.get("key"),
        "base_url": opts.get("base_url"),
        "region": opts.get("region"),
        "language": opts.get("language"),
        "currency": opts.get("currency"),
    }
    updates = {k: v for k, v in updates.items() if v is not None}
    if not updates:
        raise UsageError(
            "nothing to set",
            ["usage: kalo config set --key <API_KEY> [--region US]"],
        )
    if "region" in updates:
        region = updates["region"].upper()
        if region not in validate.REGIONS:
            raise UsageError(
                f"unknown region '{region}'", [f"valid regions: {', '.join(validate.REGIONS)}"]
            )
        updates["region"] = region
    path = config_mod.save(updates)
    render.out(f"config: saved {', '.join(sorted(updates))} to {path}")
    return 0


COMMANDS = [
    Command(
        path="config show",
        summary="Show current credentials (masked) and defaults",
        handler=config_show,
        examples=["kalo config"],
    ),
    Command(
        path="config set",
        summary="Save credentials/defaults to ~/.config/kalodata/config.toml",
        handler=config_set,
        flags=[
            Flag("--key", "KaloData API token (secret-key header)", metavar="KEY"),
            Flag("--base-url", "API base URL (default production)", metavar="URL"),
            Flag("--region", "default region", metavar="REGION"),
            Flag("--language", "default language", metavar="LANG"),
            Flag("--currency", "default currency", metavar="CUR"),
        ],
        examples=["kalo config set --key <token> --region US"],
    ),
]
