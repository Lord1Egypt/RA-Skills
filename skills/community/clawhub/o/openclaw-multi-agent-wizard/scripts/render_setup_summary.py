#!/usr/bin/env python3
"""Render a concise beginner-friendly setup summary.

Usage:
  python scripts/render_setup_summary.py --mode "多 bot 多 agent" --agents 产品助理,研发助理 --mapping "产品机器人->产品助理" "研发机器人->研发助理" --gateway restarted
"""

from __future__ import annotations

import argparse
import sys


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True)
    parser.add_argument("--agents", required=True, help="comma-separated agent names")
    parser.add_argument(
        "--mapping",
        nargs="*",
        default=[],
        help='mapping entries like "产品群->产品助理"',
    )
    parser.add_argument(
        "--gateway",
        required=True,
        choices=["restarted", "not-needed"],
    )
    parser.add_argument(
        "--next-test",
        default="Send a simple greeting in the target bot or group.",
    )
    args = parser.parse_args()

    agents = [item.strip() for item in args.agents.split(",") if item.strip()]
    gateway_line = (
        "restarted automatically"
        if args.gateway == "restarted"
        else "restart not needed"
    )

    print("Setup complete.\n")
    print("Current mode:")
    print(f"- {args.mode}\n")

    print("Agents created:")
    for agent in agents:
        print(f"- {agent}")
    print()

    print("Current mapping:")
    if args.mapping:
        for item in args.mapping:
            print(f"- {item}")
    else:
        print("- No mapping summary was provided.")
    print()

    print("Gateway:")
    print(f"- {gateway_line}\n")

    print("Next test:")
    print(f"- {args.next_test}\n")

    print("If there is no reply:")
    print("- Tell me and I will check the local gateway status and logs for you.")


if __name__ == "__main__":
    main()
