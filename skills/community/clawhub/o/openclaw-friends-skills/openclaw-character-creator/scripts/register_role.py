#!/usr/bin/env python3
"""Register a character role in ~/.openclaw/ROLES.json."""

import json
import os
import sys
from datetime import datetime, timezone

ROLES_FILE = os.path.expanduser("~/.openclaw/ROLES.json")


def load_roles():
    if os.path.exists(ROLES_FILE):
        with open(ROLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "updatedAt": "", "roles": []}


def save_roles(data):
    os.makedirs(os.path.dirname(ROLES_FILE), exist_ok=True)
    data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    with open(ROLES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def register(name, workspace_path):
    data = load_roles()

    for role in data["roles"]:
        if role["workspacePath"] == workspace_path:
            role["name"] = name
            save_roles(data)
            print(f"Updated existing role: {name} -> {workspace_path}")
            return

    for role in data["roles"]:
        if role["name"] == name:
            print(f"Warning: role '{name}' already exists at {role['workspacePath']}")
            print("Overwriting with new workspace path.")
            role["workspacePath"] = workspace_path
            save_roles(data)
            return

    data["roles"].append({"name": name, "workspacePath": workspace_path})
    save_roles(data)
    print(f"Registered: {name} -> {workspace_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: register_role.py <name> <workspace_path>")
        print("  name            Character display name")
        print("  workspace_path  Absolute path to the character workspace")
        sys.exit(1)
    register(sys.argv[1], sys.argv[2])
