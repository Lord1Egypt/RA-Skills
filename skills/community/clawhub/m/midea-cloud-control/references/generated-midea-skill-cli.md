# Generated file: midea_skill_cli.py

When this skill is used for the first time, write the following file to the user's local workspace or a temporary working directory as `midea_skill_cli.py`.

Before running it, ensure `config_store.py` from `generated-config-store.md` has also been written next to it.

```python
from __future__ import annotations

import argparse
import asyncio
import json

import aiohttp
from midealocal.cloud import MideaCloud, get_midea_cloud

from config_store import CONFIG_PATH, load_config, save_config


async def connect(account: str, password: str) -> int:
    servers = await MideaCloud.get_cloud_servers()
    cloud_name = servers[next(iter(servers))]

    async with aiohttp.ClientSession() as session:
        cloud = get_midea_cloud(cloud_name, session, account, password)
        ok = await cloud.login()
        if not ok:
            print(json.dumps({
                "ok": False,
                "action": "connect",
                "error": "login_failed",
                "message": "Midea cloud login failed. Check account/password or cloud routing.",
            }, ensure_ascii=False, indent=2))
            return 1

        homes = await cloud.list_home()
        devices: dict[str, dict] = {}
        raw_devices: list[dict] = []
        for home_id, home_name in homes.items():
            appliances = await cloud.list_appliances(int(home_id))
            if isinstance(appliances, dict):
                for device_id, info in appliances.items():
                    name = info.get("name") or str(device_id)
                    devices[name] = {
                        "id": int(device_id),
                        "name": name,
                        "sn": info.get("sn"),
                        "model_number": info.get("model_number"),
                        "type": info.get("type"),
                        "home_id": int(home_id),
                        "home_name": home_name,
                    }
                    raw_devices.append({
                        "id": int(device_id),
                        "name": name,
                        "model_number": info.get("model_number"),
                        "type": info.get("type"),
                        "home_name": home_name,
                    })

    path = save_config({
        "account": account,
        "password": password,
        "cloud_name": cloud_name,
        "devices": devices,
    })
    print(json.dumps({
        "ok": True,
        "action": "connect",
        "message": "Connected successfully.",
        "config_path": str(path),
        "cloud_name": cloud_name,
        "device_count": len(raw_devices),
        "devices": raw_devices,
    }, ensure_ascii=False, indent=2))
    return 0


def list_cached() -> int:
    cfg = load_config()
    if not cfg:
        print(json.dumps({
            "ok": False,
            "action": "list",
            "error": "missing_config",
            "message": f"No config found. Connect account first: {CONFIG_PATH}",
        }, ensure_ascii=False, indent=2))
        return 1

    devices = []
    for name, info in cfg.get("devices", {}).items():
        devices.append({
            "name": name,
            "id": info.get("id"),
            "model_number": info.get("model_number"),
            "type": info.get("type"),
            "home_name": info.get("home_name"),
        })

    print(json.dumps({
        "ok": True,
        "action": "list",
        "cloud_name": cfg.get("cloud_name"),
        "config_path": str(CONFIG_PATH),
        "device_count": len(devices),
        "devices": devices,
    }, ensure_ascii=False, indent=2))
    return 0


async def toggle(device_name: str, power: str) -> int:
    cfg = load_config()
    if not cfg:
        print(json.dumps({
            "ok": False,
            "action": "toggle",
            "error": "missing_config",
            "message": f"No config found. Connect account first: {CONFIG_PATH}",
        }, ensure_ascii=False, indent=2))
        return 1

    devices = cfg.get("devices", {})
    device = devices.get(device_name)
    if not device:
        print(json.dumps({
            "ok": False,
            "action": "toggle",
            "error": "device_not_found",
            "message": f"Device '{device_name}' not found in cached config.",
            "known_devices": sorted(devices.keys()),
        }, ensure_ascii=False, indent=2))
        return 1

    async with aiohttp.ClientSession() as session:
        cloud = get_midea_cloud(cfg["cloud_name"], session, cfg["account"], cfg["password"])
        ok = await cloud.login()
        if not ok:
            print(json.dumps({
                "ok": False,
                "action": "toggle",
                "error": "login_failed",
                "message": "Midea cloud login failed with saved credentials.",
            }, ensure_ascii=False, indent=2))
            return 1
        await cloud._api_request(
            f"/v1/appliance/operation/togglePower/{device['id']}",
            {"power": power == "on"},
        )

    print(json.dumps({
        "ok": True,
        "action": "toggle",
        "message": f"Power command sent: {power}",
        "device_name": device_name,
        "device_id": device["id"],
    }, ensure_ascii=False, indent=2))
    return 0


async def main() -> int:
    parser = argparse.ArgumentParser(description="Unified CLI for the midea-cloud-control skill.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_connect = sub.add_parser("connect")
    p_connect.add_argument("--account", required=True)
    p_connect.add_argument("--password", required=True)

    sub.add_parser("list")

    p_toggle = sub.add_parser("toggle")
    p_toggle.add_argument("--device-name", required=True)
    p_toggle.add_argument("--power", required=True, choices=["on", "off"])

    args = parser.parse_args()
    if args.cmd == "connect":
        return await connect(args.account, args.password)
    if args.cmd == "list":
        return list_cached()
    if args.cmd == "toggle":
        return await toggle(args.device_name, args.power)
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
```
