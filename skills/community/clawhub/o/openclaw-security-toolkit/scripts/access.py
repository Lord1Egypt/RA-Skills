#!/usr/bin/env python3
"""
OpenClaw Security Guard - Access Control
Manage devices, users, and permissions.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from utils import (
    OPENCLAW_DIR, Colors, load_config
)


def get_paired_devices() -> List[Dict]:
    """Get list of paired devices."""
    paired_file = OPENCLAW_DIR / "devices" / "paired.json"

    if not paired_file.exists():
        return []

    try:
        with open(paired_file, 'r') as f:
            data = json.load(f)

        devices = []
        for device_id, device_info in data.items():
            devices.append({
                "device_id": device_id[:20] + "...",
                "full_id": device_id,
                "client_id": device_info.get("clientId", "unknown"),
                "platform": device_info.get("platform", "unknown"),
                "role": device_info.get("role", "unknown"),
                "created_at": datetime.fromtimestamp(
                    device_info.get("createdAtMs", 0) / 1000
                ).isoformat() if device_info.get("createdAtMs") else "unknown",
                "last_used": datetime.fromtimestamp(
                    device_info.get("tokens", {}).get("operator", {}).get("lastUsedAtMs", 0) / 1000
                ).isoformat() if device_info.get("tokens", {}).get("operator", {}).get("lastUsedAtMs") else "unknown"
            })

        return devices
    except:
        return []


def get_channel_users() -> Dict[str, List[str]]:
    """Get users allowed for each channel."""
    credentials_dir = OPENCLAW_DIR / "credentials"
    result = {}

    if not credentials_dir.exists():
        return result

    for cred_file in credentials_dir.glob("*allowFrom.json"):
        try:
            with open(cred_file, 'r') as f:
                data = json.load(f)
            channel = cred_file.name.replace("-default-allowFrom.json", "").replace("-allowFrom.json", "")
            result[channel] = data.get("allowFrom", [])
        except:
            pass

    return result


def get_pending_devices() -> List[Dict]:
    """Get list of pending device pairings."""
    pending_file = OPENCLAW_DIR / "devices" / "pending.json"

    if not pending_file.exists():
        return []

    try:
        with open(pending_file, 'r') as f:
            data = json.load(f)

        # Pending file is usually empty or a list
        if isinstance(data, list):
            return data
        return []
    except:
        return []


def list_access_info(verbose: bool = False) -> Dict:
    """Get comprehensive access control information."""
    return {
        "devices": {
            "paired": get_paired_devices(),
            "pending": get_pending_devices()
        },
        "channels": get_channel_users(),
        "summary": {
            "total_devices": len(get_paired_devices()),
            "total_pending": len(get_pending_devices()),
            "total_channels": len(get_channel_users())
        }
    }


def print_access_info(results: Dict, i18n: Dict, verbose: bool = False):
    """Print access control information."""
    print()

    # Devices
    devices = results["devices"]["paired"]
    print(f"{Colors.BOLD}📱 Paired Devices ({len(devices)}){Colors.RESET}\n")

    if devices:
        for d in devices:
            print(f"  {Colors.CYAN}•{Colors.RESET} {d['client_id']} ({d['platform']})")
            if verbose:
                print(f"    ID: {d['device_id']}")
                print(f"    Role: {d['role']}")
                print(f"    Created: {d['created_at']}")
                print(f"    Last used: {d['last_used']}")
            print()
    else:
        print(f"  {Colors.YELLOW}No paired devices{Colors.RESET}\n")

    # Pending
    pending = results["devices"]["pending"]
    if pending:
        print(f"{Colors.BOLD}⏳ Pending Devices ({len(pending)}){Colors.RESET}\n")
        for p in pending:
            print(f"  {Colors.YELLOW}•{Colors.RESET} {p}")

    # Channels
    channels = results["channels"]
    print(f"\n{Colors.BOLD}👥 Channel Permissions{Colors.RESET}\n")

    if channels:
        for channel, users in channels.items():
            print(f"  {Colors.CYAN}•{Colors.RESET} {channel}: {len(users)} user(s)")
            if verbose:
                for u in users:
                    print(f"      - {u}")
            print()
    else:
        print(f"  {Colors.YELLOW}No channel permissions configured{Colors.RESET}\n")


if __name__ == "__main__":
    results = list_access_info(verbose=True)
    print(json.dumps(results, indent=2, ensure_ascii=False))