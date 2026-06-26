#!/usr/bin/env python3
"""Switch the active OpenClaw character.

Usage:
  shift_role.py list              List all registered roles
  shift_role.py <name>            Switch active role to <name>

The active role lives at ~/.openclaw/workspace.
When shifting, the current workspace is moved back to its original path
and the target role's workspace is moved to ~/.openclaw/workspace.
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
ROLES_FILE = os.path.join(OPENCLAW_DIR, "ROLES.json")
ACTIVE_WORKSPACE = os.path.join(OPENCLAW_DIR, "workspace")


def load_roles():
    if not os.path.exists(ROLES_FILE):
        return None
    with open(ROLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_roles(data):
    data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    with open(ROLES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_workspace_state(workspace_path):
    state_file = os.path.join(workspace_path, ".openclaw", "workspace-state.json")
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def write_workspace_state(workspace_path, updates):
    state_file = os.path.join(workspace_path, ".openclaw", "workspace-state.json")
    state = read_workspace_state(workspace_path) or {}
    state.update(updates)
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def list_roles():
    data = load_roles()
    if not data:
        print("No ROLES.json found. No roles registered.")
        return []

    roles = data.get("roles", [])
    if not roles:
        print("No roles registered.")
        return []

    print("Available roles:")
    for i, role in enumerate(roles, 1):
        marker = " <- active" if role["workspacePath"] == ACTIVE_WORKSPACE else ""
        print(f"  {i}. {role['name']}{marker}")
        print(f"     {role['workspacePath']}")

    return roles


def shift(target_name):
    data = load_roles()
    if not data:
        print("Error: ROLES.json not found. Register roles first.")
        sys.exit(1)

    roles = data.get("roles", [])

    target = None
    for role in roles:
        if role["name"] == target_name:
            target = role
            break

    if not target:
        print(f"Error: Role '{target_name}' not found.")
        list_roles()
        sys.exit(1)

    target_path = target["workspacePath"]

    if target_path == ACTIVE_WORKSPACE:
        print(f"'{target_name}' is already the active role.")
        return

    # Step 1: Save current active workspace back to its original path
    if os.path.exists(ACTIVE_WORKSPACE) and os.path.isdir(ACTIVE_WORKSPACE):
        state = read_workspace_state(ACTIVE_WORKSPACE)
        original_path = None

        if state and "originalWorkspacePath" in state:
            original_path = state["originalWorkspacePath"]

        if not original_path:
            # Find which role currently points to ACTIVE_WORKSPACE
            for role in roles:
                if role["workspacePath"] == ACTIVE_WORKSPACE and role["name"] != target_name:
                    # Reconstruct a reasonable path
                    safe_name = role["name"].lower().replace(" ", "-")
                    original_path = os.path.join(OPENCLAW_DIR, f"workspace-{safe_name}-saved")
                    break

        if not original_path:
            print("Error: Cannot determine original path for current active workspace.")
            print("Check .openclaw/workspace-state.json inside the workspace.")
            sys.exit(1)

        if os.path.exists(original_path):
            print(f"Error: Cannot save current workspace — path already exists: {original_path}")
            sys.exit(1)

        print(f"Saving current workspace -> {original_path}")
        shutil.move(ACTIVE_WORKSPACE, original_path)

        write_workspace_state(original_path, {"workspacePath": original_path})

        for role in roles:
            if role["workspacePath"] == ACTIVE_WORKSPACE:
                role["workspacePath"] = original_path
                break

    # Step 2: Move target workspace to active position
    if not os.path.exists(target_path):
        print(f"Error: Target workspace does not exist: {target_path}")
        sys.exit(1)

    print(f"Activating '{target_name}' -> {ACTIVE_WORKSPACE}")
    shutil.move(target_path, ACTIVE_WORKSPACE)

    write_workspace_state(ACTIVE_WORKSPACE, {
        "originalWorkspacePath": target_path,
        "workspacePath": ACTIVE_WORKSPACE,
    })

    target["workspacePath"] = ACTIVE_WORKSPACE

    # Step 3: Persist changes
    save_roles(data)

    print(f"\nActive role: {target_name}")
    print(f"Workspace: {ACTIVE_WORKSPACE}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        list_roles()
    else:
        shift(cmd)
