#!/usr/bin/env python3
"""Check authz + feegrant readiness for OpenMath authz submissions."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from submission_config import (
    KEYRING_BACKEND,
    SubmissionConfig,
    SubmissionConfigError,
    authz_onboarding_text,
    detect_working_shentud,
    load_submission_config,
)

AUTHZ_OUTER_WRAPPER_MESSAGES = {"/cosmos.authz.v1beta1.MsgExec"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check authz + feegrant readiness for OpenMath authz submissions."
    )
    parser.add_argument(
        "--config",
        default=None,
        help=(
            "Shared config path (resolution: --config, then OPENMATH_ENV_CONFIG, "
            "then ./.openmath-skills/openmath-env.json, then ~/.openmath-skills/openmath-env.json)."
        ),
    )
    return parser


def run_command(args: list[str], *, shentud_bin: str | None = None) -> str:
    command = list(args)
    if shentud_bin and command and command[0] == "shentud":
        command[0] = shentud_bin

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "command failed"
        raise RuntimeError(f"{' '.join(command)}: {message}")
    return result.stdout.strip()


def run_json(args: list[str], *, shentud_bin: str | None = None) -> dict:
    output = run_command(args, shentud_bin=shentud_bin)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        command = list(args)
        if shentud_bin and command and command[0] == "shentud":
            command[0] = shentud_bin
        raise RuntimeError(f"{' '.join(command)}: expected JSON output") from exc


def print_status(kind: str, label: str, detail: str | None = None) -> None:
    suffix = f" - {detail}" if detail else ""
    print(f"[{kind}] {label}{suffix}")


def collect_values(payload: object, key: str) -> list[object]:
    values: list[object] = []
    if isinstance(payload, dict):
        for current_key, value in payload.items():
            if current_key == key:
                values.append(value)
            values.extend(collect_values(value, key))
    elif isinstance(payload, list):
        for value in payload:
            values.extend(collect_values(value, key))
    return values


def flatten_strings(values: list[object]) -> list[str]:
    flattened: list[str] = []
    for value in values:
        if isinstance(value, list):
            flattened.extend(str(item) for item in value)
        else:
            flattened.append(str(value))
    return flattened


def extract_authz_messages(payload: object) -> set[str]:
    return {
        msg.strip()
        for msg in flatten_strings(collect_values(payload, "msg"))
        if msg.strip()
    }


def check_local_key(config: SubmissionConfig, *, shentud_bin: str) -> tuple[bool, bool]:
    try:
        address = run_command(
            [
                "shentud",
                "keys",
                "show",
                config.agent_key_name,
                "-a",
                "--keyring-backend",
                KEYRING_BACKEND,
            ],
            shentud_bin=shentud_bin,
        )
    except RuntimeError as exc:
        print_status("missing", "local agent key", str(exc))
        return False, False

    print_status("ok", "local agent key", f"{config.agent_key_name} -> {address}")
    if address != config.agent_address:
        print_status(
            "missing",
            "agent address matches config",
            f"config={config.agent_address}, local={address}",
        )
        return True, False

    print_status("ok", "agent address matches config", config.agent_address)
    return True, True


def check_authz_grants(config: SubmissionConfig, *, shentud_bin: str) -> bool:
    try:
        payload = run_json(
            [
                "shentud",
                "query",
                "authz",
                "grants",
                config.prover_address,
                config.agent_address,
                "--node",
                config.shentu_node_url,
                "-o",
                "json",
            ],
            shentud_bin=shentud_bin,
        )
    except RuntimeError as exc:
        print_status("missing", "authz grants", str(exc))
        return False

    granted_messages = extract_authz_messages(payload)
    if granted_messages:
        print_status("ok", "authz grants found", ", ".join(sorted(granted_messages)))
    else:
        print_status("missing", "authz grants found", "no granted message types returned")

    ready = True
    for msg_type in config.authz_messages:
        if msg_type in AUTHZ_OUTER_WRAPPER_MESSAGES:
            print_status(
                "warn",
                f"authz grant for {msg_type}",
                "outer wrapper message; check this under feegrant_messages instead",
            )
            continue
        if msg_type in granted_messages:
            print_status("ok", f"authz grant for {msg_type}")
        else:
            print_status("missing", f"authz grant for {msg_type}")
            ready = False

    return ready


def check_feegrant(config: SubmissionConfig, *, shentud_bin: str) -> tuple[bool, bool]:
    try:
        payload = run_json(
            [
                "shentud",
                "query",
                "feegrant",
                "grant",
                config.fee_granter_address,
                config.agent_address,
                "--node",
                config.shentu_node_url,
                "-o",
                "json",
            ],
            shentud_bin=shentud_bin,
        )
    except RuntimeError as exc:
        print_status("missing", "feegrant grant", str(exc))
        return False, False

    print_status("ok", "feegrant grant", f"{config.fee_granter_address} -> {config.agent_address}")

    allowed_messages = set(flatten_strings(collect_values(payload, "allowed_messages")))
    if not allowed_messages:
        print_status(
            "warn",
            "feegrant allowed_messages",
            "no AllowedMsgAllowance filter found; feegrant appears unrestricted",
        )
        messages_ready = True
    else:
        print_status(
            "ok",
            "feegrant allowed_messages found",
            ", ".join(sorted(allowed_messages)),
        )
        messages_ready = True
        for msg_type in config.feegrant_messages:
            if msg_type in allowed_messages:
                print_status("ok", f"feegrant message {msg_type}")
            else:
                print_status("missing", f"feegrant message {msg_type}")
                messages_ready = False

    spend_limits = collect_values(payload, "spend_limit")
    expirations = collect_values(payload, "expiration")
    if not spend_limits or spend_limits == [[]]:
        print_status("warn", "feegrant spend_limit", "no spend_limit detected")
    else:
        print_status("ok", "feegrant spend_limit")

    if not expirations or expirations == [None]:
        print_status("warn", "feegrant expiration", "no expiration detected")
    else:
        print_status("ok", "feegrant expiration")

    return True, messages_ready


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        config = load_submission_config(args.config)
    except SubmissionConfigError as exc:
        print(exc, file=sys.stderr)
        return 1

    print("Config:", config.config_path)
    print("Prover Addr:", config.prover_address)
    print("Agent Key:", config.agent_key_name)
    print("Agent Addr:", config.agent_address)
    print("Fee Granter (derived):", config.fee_granter_address)
    print()
    print("Local checks")

    ready = True

    try:
        shentud_bin, version = detect_working_shentud()
        detail = version if shentud_bin == "shentud" else f"{version} ({shentud_bin})"
        print_status("ok", "shentud available", detail)
    except RuntimeError as exc:
        print_status("missing", "shentud available", str(exc))
        return 1

    key_exists, key_matches = check_local_key(config, shentud_bin=shentud_bin)
    ready = ready and key_exists and key_matches

    print()
    print("Chain checks")
    authz_ready = check_authz_grants(config, shentud_bin=shentud_bin)
    feegrant_exists, feegrant_ready = check_feegrant(config, shentud_bin=shentud_bin)

    ready = ready and authz_ready and feegrant_exists and feegrant_ready

    print()
    if ready:
        print("Status: ready")
        return 0

    print("Status: not ready")
    print()
    print(authz_onboarding_text(config.config_path, config_exists=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
