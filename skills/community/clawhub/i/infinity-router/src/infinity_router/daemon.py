"""
daemon.py — `infinity-router-daemon` entry point.

Monitors the active model and rotates to the next best available
model when it becomes rate-limited or unresponsive.

Commands
--------
(no flag)      one-shot check, rotate if needed
--loop / -l    continuous monitoring loop (Ctrl-C to stop)
--rotate / -r  force-rotate to the next model right now
--status / -s  show rotation history and cooldown state
--clear-rl     clear all rate-limit records
--target / -t  openclaw | claude-code  (default: openclaw)
"""

import argparse
import json
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from infinity_router.models import (
    get_ranked_free_models,
    is_rate_limited,
    mark_rate_limited,
    expire_stale_rate_limits,
    clear_rate_limits,
    COOLDOWN_MIN,
)
from infinity_router.probe import health_check
from infinity_router.targets import (
    BaseTarget,
    OpenClawTarget,
    get_target,
    fmt_primary,
    fmt_list,
    FREE_ROUTER,
)


# ── State ──────────────────────────────────────────────────────────────────────
_STATE_PATH    = Path.home() / ".infinity-router" / "daemon-state.json"
CHECK_INTERVAL = 60  # seconds between health-check cycles


# ──────────────────────────────────────────────────────────────────────────────
# State helpers
# ──────────────────────────────────────────────────────────────────────────────

def _load_state() -> dict:
    if _STATE_PATH.exists():
        try:
            return json.loads(_STATE_PATH.read_text())
        except json.JSONDecodeError:
            pass
    return {"rotations": 0, "last_rotation": None, "last_reason": None}


def _save_state(state: dict) -> None:
    _STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _STATE_PATH.write_text(json.dumps(state, indent=2))


def _bump(state: dict, reason: str) -> None:
    state["rotations"]     = state.get("rotations", 0) + 1
    state["last_rotation"] = datetime.now().isoformat()
    state["last_reason"]   = reason
    _save_state(state)


def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _base(primary: str) -> str:
    """Strip 'openrouter/' routing prefix from an OpenClaw primary value."""
    return primary.removeprefix("openrouter/")


# ──────────────────────────────────────────────────────────────────────────────
# Core rotation
# ──────────────────────────────────────────────────────────────────────────────

def _api_key() -> Optional[str]:
    import os
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    from infinity_router.targets import _OPENCLAW_PATH
    if _OPENCLAW_PATH.exists():
        try:
            cfg = json.loads(_OPENCLAW_PATH.read_text())
            return cfg.get("env", {}).get("OPENROUTER_API_KEY")
        except Exception:
            pass
    return None


def _next_model(api_key: str, skip: Optional[str]) -> Optional[str]:
    """Highest-ranked model that is not rate-limited and not `skip`."""
    for m in get_ranked_free_models(api_key):
        mid = m["id"]
        if "openrouter/free" in mid:
            continue
        if skip and mid == skip:
            continue
        if is_rate_limited(mid):
            continue
        return mid
    return None


def rotate(api_key: str, state: dict, target: BaseTarget, reason: str) -> bool:
    """
    Switch the primary model to the next available one.
    Rebuilds the fallback chain afterward.
    Returns True on success.
    """
    current = target.read_primary()
    current_base = _base(current) if current else None

    print(f"[{_ts()}] rotate  reason={reason}  from={current_base or 'none'}")

    nxt = _next_model(api_key, current_base)
    if not nxt:
        print("  no available model — all may be rate-limited")
        return False

    print(f"  → {nxt}")
    target.write_primary(nxt)

    # Rebuild fallback chain
    models    = get_ranked_free_models(api_key)
    fallbacks = [FREE_ROUTER]
    for m in models:
        if len(fallbacks) >= 5:
            break
        mid = m["id"]
        if "openrouter/free" in mid or mid == nxt or is_rate_limited(mid):
            continue
        fallbacks.append(mid)

    target.write_fallbacks(fallbacks)
    print(f"  fallbacks  {fallbacks}")

    _bump(state, reason)
    print(f"  total rotations: {state['rotations']}")
    return True


# ──────────────────────────────────────────────────────────────────────────────
# Check cycle
# ──────────────────────────────────────────────────────────────────────────────

def check_cycle(api_key: str, state: dict, target: BaseTarget) -> bool:
    """
    Probe the current primary model.
    Rotate if it is rate-limited, unavailable, or unresponsive.
    Returns True if a rotation happened.
    """
    primary = target.read_primary()
    if not primary:
        print(f"[{_ts()}] no primary set — running initial pick")
        return rotate(api_key, state, target, "initial")

    base = _base(primary)

    if is_rate_limited(base):
        return rotate(api_key, state, target, "cooldown_active")

    print(f"[{_ts()}] checking {base} …", end=" ", flush=True)
    ok, err = health_check(api_key, base)

    if ok:
        print("OK")
        return False

    print(err)
    if err == "rate_limit":
        mark_rate_limited(base)
    return rotate(api_key, state, target, err or "unknown")


# ──────────────────────────────────────────────────────────────────────────────
# Run modes
# ──────────────────────────────────────────────────────────────────────────────

def run_once(api_key: str, target: BaseTarget) -> None:
    state = _load_state()
    expire_stale_rate_limits()
    check_cycle(api_key, state, target)


def run_loop(api_key: str, target: BaseTarget) -> None:
    print(f"infinity-router-daemon  interval={CHECK_INTERVAL}s  cooldown={COOLDOWN_MIN}m")
    print("─" * 55)

    running = True

    def _stop(sig, frame):
        nonlocal running
        print("\nDaemon stopping …")
        running = False

    signal.signal(signal.SIGINT,  _stop)
    signal.signal(signal.SIGTERM, _stop)

    state = _load_state()

    while running:
        try:
            expire_stale_rate_limits()
            check_cycle(api_key, state, target)
        except Exception as exc:
            print(f"[{_ts()}] unhandled error: {exc}")

        for _ in range(CHECK_INTERVAL):
            if not running:
                break
            time.sleep(1)

    print("Daemon stopped.")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="infinity-router-daemon",
        description="Monitor and auto-rotate free AI models.",
    )
    parser.add_argument("--loop",     "-l", action="store_true", help="Continuous monitoring loop")
    parser.add_argument("--rotate",   "-r", action="store_true", help="Force-rotate now")
    parser.add_argument("--status",   "-s", action="store_true", help="Show daemon state")
    parser.add_argument("--clear-rl",       action="store_true", help="Clear rate-limit records")
    parser.add_argument("--target",   "-t",
                        default="openclaw", metavar="TARGET",
                        help="openclaw | claude-code  (default: openclaw)")

    args   = parser.parse_args()
    target = get_target(args.target)

    if args.status:
        state = _load_state()
        from infinity_router.models import _load_rl
        rl = _load_rl()
        print("infinity-router-daemon state")
        print("═" * 40)
        print(f"  rotations      {state.get('rotations', 0)}")
        print(f"  last rotation  {state.get('last_rotation', 'never')}")
        print(f"  last reason    {state.get('last_reason', 'n/a')}")
        print(f"\n  rate-limited ({len(rl)}):")
        for mid, since in rl.items():
            print(f"    {mid}  (since {since})")
        if not rl:
            print("    none")
        return

    if args.clear_rl:
        clear_rate_limits()
        print("Rate-limit records cleared.")
        return

    api_key = _api_key()
    if not api_key:
        sys.exit(
            "Error: OPENROUTER_API_KEY is not set.\n"
            "  export OPENROUTER_API_KEY='sk-or-…'"
        )

    if args.rotate:
        state = _load_state()
        rotate(api_key, state, target, "forced")
        return

    if args.loop:
        run_loop(api_key, target)
    else:
        run_once(api_key, target)


if __name__ == "__main__":
    main()
