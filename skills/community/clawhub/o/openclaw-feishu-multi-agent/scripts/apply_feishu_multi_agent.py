#!/usr/bin/env python3
"""Semi-automatically apply OpenClaw + Feishu multi-agent artifacts to ~/.openclaw."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import (
    backup_file,
    ensure_parent,
    find_coordinator,
    is_placeholder,
    load_json,
    load_roles,
    role_agent_dir,
    role_workspace,
    write_json,
)
from render_feishu_multi_agent import render_identity, render_protocol


def ensure_list_path(data: dict[str, Any], path: list[str]) -> list[Any]:
    cur: dict[str, Any] = data
    for part in path[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    leaf = cur.get(path[-1])
    if not isinstance(leaf, list):
        leaf = []
        cur[path[-1]] = leaf
    return leaf


def ensure_dict_path(data: dict[str, Any], path: list[str]) -> dict[str, Any]:
    cur = data
    for part in path:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    return cur


def merge_agent_list(config: dict[str, Any], roles: list[dict[str, Any]], state_dir: Path) -> list[str]:
    changes: list[str] = []
    agent_list = ensure_list_path(config, ["agents", "list"])
    by_id = {item.get("id"): item for item in agent_list if isinstance(item, dict) and item.get("id")}
    for role in roles:
        target = by_id.get(role["agentId"])
        desired_workspace = str(role_workspace(role, state_dir))
        desired_agent_dir = str(role_agent_dir(role, state_dir))
        if target is None:
            agent_list.append(
                {"id": role["agentId"], "workspace": desired_workspace, "agentDir": desired_agent_dir}
            )
            changes.append(f"add agents.list entry: {role['agentId']}")
            continue
        if not target.get("workspace") or is_placeholder(target.get("workspace")):
            target["workspace"] = desired_workspace
            changes.append(f"set workspace for {role['agentId']}")
        if not target.get("agentDir") or is_placeholder(target.get("agentDir")):
            target["agentDir"] = desired_agent_dir
            changes.append(f"set agentDir for {role['agentId']}")
    return changes


def merge_tooling(config: dict[str, Any], roles: list[dict[str, Any]]) -> list[str]:
    changes: list[str] = []
    tools = ensure_dict_path(config, ["tools"])
    sessions = ensure_dict_path(tools, ["sessions"])
    if sessions.get("visibility") != "all":
        sessions["visibility"] = "all"
        changes.append("set tools.sessions.visibility=all")

    agent_to_agent = ensure_dict_path(tools, ["agentToAgent"])
    if agent_to_agent.get("enabled") is not True:
        agent_to_agent["enabled"] = True
        changes.append("set tools.agentToAgent.enabled=true")

    existing_allow = agent_to_agent.get("allow")
    if not isinstance(existing_allow, list):
        existing_allow = []
        agent_to_agent["allow"] = existing_allow
    for role in roles:
        if role["agentId"] not in existing_allow:
            existing_allow.append(role["agentId"])
            changes.append(f"allow agentToAgent: {role['agentId']}")
    return changes


def merge_accounts_and_bindings(config: dict[str, Any], roles: list[dict[str, Any]]) -> list[str]:
    changes: list[str] = []
    accounts = ensure_dict_path(config, ["channels", "feishu", "accounts"])
    bindings = ensure_list_path(config, ["bindings"])
    binding_pairs = {
        (item.get("agentId"), item.get("match", {}).get("accountId"))
        for item in bindings
        if isinstance(item, dict) and isinstance(item.get("match"), dict)
    }

    for role in roles:
        account = accounts.get(role["accountId"])
        if not isinstance(account, dict):
            account = {}
            accounts[role["accountId"]] = account
            changes.append(f"add Feishu account: {role['accountId']}")
        if account.get("name") != role["roleName"]:
            account["name"] = role["roleName"]
            changes.append(f"set account name for {role['accountId']}")

        for key in ("appId", "appSecret"):
            incoming = role.get(key)
            if not is_placeholder(incoming):
                if account.get(key) != incoming:
                    account[key] = incoming
                    changes.append(f"set {key} for {role['accountId']}")
            elif key not in account:
                account[key] = "replace_me"
                changes.append(f"set placeholder {key} for {role['accountId']}")

        pair = (role["agentId"], role["accountId"])
        if pair not in binding_pairs:
            bindings.append(
                {
                    "agentId": role["agentId"],
                    "match": {"channel": "feishu", "accountId": role["accountId"]},
                }
            )
            binding_pairs.add(pair)
            changes.append(f"add binding {role['agentId']} -> {role['accountId']}")
    return changes


def apply_protocol(path: Path, content: str, write: bool, backup: bool) -> list[str]:
    changes: list[str] = []
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return changes
    changes.append(f"write {path}")
    if write:
        ensure_parent(path)
        if backup and path.exists():
            backup_file(path)
        path.write_text(content, encoding="utf-8")
    return changes


def apply_identity_files(
    roles: list[dict[str, Any]],
    coordinator_name: str,
    state_dir: Path,
    write: bool,
    backup: bool,
) -> list[str]:
    changes: list[str] = []
    for role in roles:
        target_dir = role_agent_dir(role, state_dir)
        target = target_dir / "IDENTITY.md"
        content = render_identity(role, coordinator_name)
        if target.exists() and target.read_text(encoding="utf-8") == content:
            continue
        changes.append(f"write {target}")
        if write:
            target_dir.mkdir(parents=True, exist_ok=True)
            if backup and target.exists():
                backup_file(target)
            target.write_text(content, encoding="utf-8")
    return changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roles", required=True, help="Path to roles.json")
    parser.add_argument("--state-dir", default="~/.openclaw", help="OpenClaw state dir")
    parser.add_argument("--write", action="store_true", help="Write changes back to disk")
    parser.add_argument("--backup", action="store_true", help="Create backups before overwriting files")
    parser.add_argument(
        "--apply-identities",
        action="store_true",
        help="Also write IDENTITY.md for each role to its agentDir",
    )
    args = parser.parse_args(argv)

    roles_path = Path(args.roles).expanduser().resolve()
    state_dir = Path(args.state_dir).expanduser().resolve()
    protocol_path = state_dir / "PROTOCOL.md"
    config_path = state_dir / "openclaw.json"

    system_name, roles = load_roles(roles_path)
    coordinator = find_coordinator(roles)

    if config_path.exists():
        config = load_json(config_path)
    else:
        config = {}

    changes: list[str] = []
    changes.extend(merge_agent_list(config, roles, state_dir))
    changes.extend(merge_tooling(config, roles))
    changes.extend(merge_accounts_and_bindings(config, roles))
    changes.extend(apply_protocol(protocol_path, render_protocol(system_name, roles), args.write, args.backup))

    if args.write:
        ensure_parent(config_path)
        if args.backup and config_path.exists():
            backup_file(config_path)
        write_json(config_path, config)
    changes.append(f"{'write' if args.write else 'preview'} {config_path}")

    if args.apply_identities:
        changes.extend(apply_identity_files(roles, coordinator["roleName"], state_dir, args.write, args.backup))

    print("OpenClaw + Feishu multi-agent apply")
    print()
    print(f"Mode: {'write' if args.write else 'dry-run'}")
    print(f"State dir: {state_dir}")
    print(f"Roles: {len(roles)}")
    print()
    if changes:
        print("Planned changes")
        for item in changes:
            print(f"- {item}")
    else:
        print("Planned changes")
        print("- none")
    if not args.write:
        print()
        print("Nothing was written. Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
