#!/usr/bin/env python3
"""Audit OpenClaw + Feishu multi-agent configuration against a roles file."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import dotted_get, load_json, load_roles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roles", required=True, help="Path to roles.json")
    parser.add_argument(
        "--config",
        default="~/.openclaw/openclaw.json",
        help="Path to openclaw.json (default: ~/.openclaw/openclaw.json)",
    )
    args = parser.parse_args(argv)

    roles_path = Path(args.roles).expanduser().resolve()
    config = load_json(Path(args.config).expanduser().resolve())
    _, roles = load_roles(roles_path)

    failures: list[str] = []
    warnings: list[str] = []

    agent_ids = {item.get("id") for item in dotted_get(config, ["agents", "list"], []) if isinstance(item, dict)}
    accounts = dotted_get(config, ["channels", "feishu", "accounts"], {})
    bindings = dotted_get(config, ["bindings"], [])
    binding_pairs = {
        (item.get("agentId"), dotted_get(item, ["match", "accountId"]))
        for item in bindings
        if isinstance(item, dict)
    }

    allow = set(dotted_get(config, ["tools", "agentToAgent", "allow"], []) or [])
    sessions_visibility = dotted_get(config, ["tools", "sessions", "visibility"])
    agent_to_agent_enabled = dotted_get(config, ["tools", "agentToAgent", "enabled"])

    if sessions_visibility != "all":
        failures.append("tools.sessions.visibility should be 'all'")
    if agent_to_agent_enabled is not True:
        failures.append("tools.agentToAgent.enabled should be true")

    for role in roles:
        agent_id = role["agentId"]
        account_id = role["accountId"]
        if agent_id not in agent_ids:
            failures.append(f"missing agent in agents.list: {agent_id}")
        if account_id not in accounts:
            failures.append(f"missing Feishu account in channels.feishu.accounts: {account_id}")
        if (agent_id, account_id) not in binding_pairs:
            failures.append(f"missing binding for agent/account pair: {agent_id} -> {account_id}")
        if agent_id not in allow:
            failures.append(f"missing agent in tools.agentToAgent.allow: {agent_id}")

    coordinators = [role for role in roles if role.get("isCoordinator")]
    if len(coordinators) != 1:
        failures.append("roles file must contain exactly one coordinator")

    default_group_policy = dotted_get(config, ["channels", "feishu", "accounts", "default", "groupPolicy"])
    if default_group_policy == "open":
        warnings.append("channels.feishu.accounts.default.groupPolicy is 'open'; review security posture")

    print("OpenClaw + Feishu multi-agent audit")
    print()
    print(f"Roles checked: {len(roles)}")
    print(f"Coordinator: {coordinators[0]['agentId'] if coordinators else 'N/A'}")
    print()

    if failures:
        print("FAILURES")
        for item in failures:
            print(f"- {item}")
    else:
        print("FAILURES")
        print("- none")

    print()
    if warnings:
        print("WARNINGS")
        for item in warnings:
            print(f"- {item}")
    else:
        print("WARNINGS")
        print("- none")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
