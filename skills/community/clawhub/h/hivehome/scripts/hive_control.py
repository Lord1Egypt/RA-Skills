#!/usr/bin/env python3
# SECURITY MANIFEST:
#   Environment variables accessed: HIVE_USERNAME, HIVE_PASSWORD,
#   HIVE_DEVICE_GROUP_KEY, HIVE_DEVICE_KEY, HIVE_DEVICE_PASSWORD (optional, for device login)
#   External endpoints called: beekeeper.hivehome.com / api.prod.bgchprod.info (via Pyhiveapi only)
#   Local files read: none
#   Local files written: none

"""
Hive Home CLI – status and control for heating, hot water. Uses Pyhiveapi.
Run from skill dir: python scripts/hive_control.py <command> [options]
Requires: pyhiveapi>=1.0.0 (pip install "pyhiveapi>=1.0.0"); env HIVE_USERNAME, HIVE_PASSWORD (and device keys for non-interactive use).
If you see attribute/method errors, upgrade: pip install -U pyhiveapi
"""

import argparse
import os
import sys


def get_session():
    """Build Hive session: device login if device keys set, else username/password (may prompt for 2FA)."""
    from pyhiveapi import Hive, SMS_REQUIRED

    username = os.environ.get("HIVE_USERNAME")
    password = os.environ.get("HIVE_PASSWORD")
    if not username or not password:
        print("Error: set HIVE_USERNAME and HIVE_PASSWORD", file=sys.stderr)
        sys.exit(1)

    dgk = os.environ.get("HIVE_DEVICE_GROUP_KEY")
    dk = os.environ.get("HIVE_DEVICE_KEY")
    dp = os.environ.get("HIVE_DEVICE_PASSWORD")

    if dgk and dk and dp:
        session = Hive(
            username=username,
            password=password,
            deviceGroupKey=dgk,
            deviceKey=dk,
            devicePassword=dp,
        )
        session.deviceLogin()
    else:
        session = Hive(username=username, password=password)
        login = session.login()
        if login.get("ChallengeName") == SMS_REQUIRED:
            print("Error: 2FA required. Set HIVE_DEVICE_* after one interactive login, or run with TTY.", file=sys.stderr)
            sys.exit(1)
    session.startSession()
    return session


def cmd_status(session, _args):
    heating = session.deviceList.get("climate", [])
    water = session.deviceList.get("water_heater", [])
    lines = []
    for i, h in enumerate(heating):
        name = h.get("hiveName", "Heating") + (f" ({i})" if len(heating) > 1 else "")
        mode = session.heating.getMode(h)
        cur = session.heating.getCurrentTemperature(h)
        tgt = session.heating.getTargetTemperature(h)
        boost = session.heating.getBoostStatus(h)
        lines.append(f"Heating {name}: mode={mode} current={cur}°C target={tgt}°C boost={boost}")
    for i, w in enumerate(water):
        name = w.get("hiveName", "Hot water") + (f" ({i})" if len(water) > 1 else "")
        mode = session.hotwater.getMode(w)
        state = session.hotwater.getState(w)
        boost = session.hotwater.getBoost(w)
        lines.append(f"Hot water {name}: mode={mode} state={state} boost={boost}")
    if not lines:
        lines.append("No heating or hot water devices found.")
    print("\n".join(lines))


def cmd_set_temp(session, args):
    heating = session.deviceList.get("climate", [])
    if not heating:
        print("No heating device found.", file=sys.stderr)
        sys.exit(1)
    zone = heating[args.zone_index]
    session.heating.setTargetTemperature(zone, args.temp)
    print(f"Target temperature set to {args.temp}°C.")


def cmd_mode(session, args):
    heating = session.deviceList.get("climate", [])
    if not heating:
        print("No heating device found.", file=sys.stderr)
        sys.exit(1)
    zone = heating[args.zone_index]
    # API expects SCHEDULE, MANUAL, OFF (not HEAT)
    mode_map = {"HEAT": "MANUAL", "MANUAL": "MANUAL", "SCHEDULE": "SCHEDULE", "OFF": "OFF"}
    api_mode = mode_map.get(args.mode.upper(), args.mode.upper())

    if api_mode == "MANUAL":
        # Hive often only applies MANUAL when target is sent in the same request
        target = getattr(args, "temp", None)
        if target is None:
            target = session.heating.getTargetTemperature(zone)
            if target is None or target < 5:
                target = 20
        target = int(round(float(target)))
        product = session.data.products.get(zone["hiveID"], {})
        ptype = product.get("type", "heating")
        session.hiveRefreshTokens()
        resp = session.api.setState(ptype, zone["hiveID"], mode="MANUAL", target=str(target))
        if resp.get("original") == 200:
            session.getDevices(zone["hiveID"])
            print(f"Heating mode set to MANUAL at {target}°C.")
        else:
            print(f"Heating mode set to MANUAL (target {target}°C). API response: {resp.get('original')}", file=sys.stderr)
    else:
        session.heating.setMode(zone, api_mode)
        print(f"Heating mode set to {api_mode}.")


def cmd_boost(session, args):
    heating = session.deviceList.get("climate", [])
    if not heating:
        print("No heating device found.", file=sys.stderr)
        sys.exit(1)
    zone = heating[args.zone_index]
    session.heating.setBoostOn(zone, str(args.minutes), float(args.temp))
    print(f"Heating boost on for {args.minutes} min at {args.temp}°C.")


def cmd_boost_off(session, args):
    heating = session.deviceList.get("climate", [])
    if not heating:
        print("No heating device found.", file=sys.stderr)
        sys.exit(1)
    zone = heating[args.zone_index]
    session.heating.setBoostOff(zone)
    print("Heating boost off.")


def cmd_hotwater_boost(session, args):
    water = session.deviceList.get("water_heater", [])
    if not water:
        print("No hot water device found.", file=sys.stderr)
        sys.exit(1)
    hw = water[args.zone_index]
    session.hotwater.setBoostOn(hw, args.minutes)
    print(f"Hot water boost on for {args.minutes} min.")


def cmd_hotwater_boost_off(session, args):
    water = session.deviceList.get("water_heater", [])
    if not water:
        print("No hot water device found.", file=sys.stderr)
        sys.exit(1)
    hw = water[args.zone_index]
    session.hotwater.setBoostOff(hw)
    print("Hot water boost off.")


def cmd_hotwater_mode(session, args):
    water = session.deviceList.get("water_heater", [])
    if not water:
        print("No hot water device found.", file=sys.stderr)
        sys.exit(1)
    hw = water[args.zone_index]
    session.hotwater.setMode(hw, args.mode.upper())
    print(f"Hot water mode set to {args.mode.upper()}.")


def main():
    parser = argparse.ArgumentParser(
        description="Hive Home control (heating, hot water). Set HIVE_USERNAME, HIVE_PASSWORD; for automation set HIVE_DEVICE_* after first login."
    )
    parser.add_argument("--zone", type=int, default=0, dest="zone_index", help="Device index if multiple (default 0)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show heating and hot water status")

    p_set = sub.add_parser("set-temp", help="Set target temperature (°C)")
    p_set.add_argument("temp", type=int, help="Target temperature in °C")
    p_set.set_defaults(zone_index=0)

    p_mode = sub.add_parser("mode", help="Set heating mode (SCHEDULE, MANUAL/heat, OFF)")
    p_mode.add_argument("mode", choices=["schedule", "heat", "manual", "off"], help="Mode (heat = manual)")
    p_mode.add_argument("temp", type=int, nargs="?", default=None, help="For heat/manual: target °C (default: current or 20)")
    p_mode.set_defaults(zone_index=0)

    p_boost = sub.add_parser("boost", help="Turn heating boost on")
    p_boost.add_argument("minutes", type=int, help="Boost duration (minutes)")
    p_boost.add_argument("temp", type=int, nargs="?", default=21, help="Target temp °C (default 21)")
    p_boost.set_defaults(zone_index=0)

    sub.add_parser("boost-off", help="Turn heating boost off").set_defaults(zone_index=0)

    p_hw = sub.add_parser("hotwater-boost", help="Turn hot water boost on")
    p_hw.add_argument("minutes", type=int, help="Boost duration (minutes)")
    p_hw.set_defaults(zone_index=0)

    sub.add_parser("hotwater-boost-off", help="Turn hot water boost off").set_defaults(zone_index=0)

    p_hwm = sub.add_parser("hotwater-mode", help="Set hot water mode (SCHEDULE, OFF)")
    p_hwm.add_argument("mode", choices=["schedule", "off"], help="Mode")
    p_hwm.set_defaults(zone_index=0)

    args = parser.parse_args()
    session = get_session()

    handlers = {
        "status": cmd_status,
        "set-temp": cmd_set_temp,
        "mode": cmd_mode,
        "boost": cmd_boost,
        "boost-off": cmd_boost_off,
        "hotwater-boost": cmd_hotwater_boost,
        "hotwater-boost-off": cmd_hotwater_boost_off,
        "hotwater-mode": cmd_hotwater_mode,
    }
    handlers[args.command](session, args)


if __name__ == "__main__":
    main()
