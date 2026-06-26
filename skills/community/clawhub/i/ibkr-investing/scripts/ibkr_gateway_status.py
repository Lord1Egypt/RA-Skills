#!/usr/bin/env python3
"""Quick diagnostic — is the IB Gateway reachable on the configured port?

Useful first thing when a scheduled task fails: confirms whether the issue is
the Gateway itself (down, restarting, awaiting 2FA) or something downstream.
"""
from __future__ import annotations

import os
import socket
import sys

from _ibkr_client import _host, _port, env_summary, is_live


def main() -> int:
    print(env_summary())
    host = _host()
    port = _port()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    reachable = False
    try:
        s.connect((host, port))
        reachable = True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"  TCP connect to {host}:{port} FAILED ({type(e).__name__}: {e})")
    finally:
        s.close()

    if reachable:
        print(f"  TCP connect to {host}:{port} OK")
        # Now try a real handshake via ib_async.
        try:
            from ib_async import IB
        except ImportError:
            print("  ib_async not installed; cannot complete handshake test.")
            return 1
        ib = IB()
        try:
            ib.connect(host, port, clientId=int(os.environ.get("IBKR_CLIENT_ID", "97")), readonly=True, timeout=8.0)
            accounts = ib.managedAccounts()
            print(f"  IBKR API handshake OK; managed accounts: {accounts}")
            return 0
        except Exception as e:
            print(f"  IBKR API handshake FAILED: {e}")
            print(f"  Common causes:")
            print(f"   - 2FA prompt waiting on IBKR Mobile app")
            print(f"   - Gateway in daily auto-restart window")
            print(f"   - Wrong port (live=4001 / paper=4002)")
            return 1
        finally:
            try:
                ib.disconnect()
            except Exception:
                pass

    # Reachability already failed; help the user troubleshoot.
    print()
    print("Troubleshooting:")
    print(f"  1. Is the Docker Gateway running?  docker ps | grep ib-gateway")
    print(f"  2. Did you flip IBKR_LIVE_MODE correctly? Currently {'LIVE' if is_live() else 'PAPER'}.")
    print(f"  3. Check Gateway logs:  docker logs <container> --tail 30")
    return 1


if __name__ == "__main__":
    sys.exit(main())
