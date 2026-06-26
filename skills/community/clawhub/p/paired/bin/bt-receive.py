#!/usr/bin/env python3
"""bt-receive — Listen for OBEX pushes from paired devices.

Foreground: registers an OBEX agent and saves any incoming files to
~/Downloads/bluetooth/ (or --save-to). Ctrl-C to stop.

Examples:
  bt-receive
  bt-receive --save-to /tmp/incoming
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_obex


def main() -> int:
    ap = argparse.ArgumentParser(description="Listen for incoming OBEX pushes")
    ap.add_argument("--save-to", default=None,
                    help="Where to save received files (default ~/Downloads/bluetooth)")
    args = ap.parse_args()

    return bt_obex.run_receive_agent(save_dir=args.save_to)


if __name__ == "__main__":
    sys.exit(main())
