"""
watcher.py — Real-time OpenClaw log watcher for Infinity-Router.

Tails the OpenClaw gateway log and auto-rotates the active model when
failure patterns spike above a configurable threshold.

Failure patterns detected
-------------------------
- FailoverError / Unknown model
- model_not_found
- No endpoints found that support tool use
- HTTP 429 / rate_limit
- All fallbacks exhausted

Triggered via
-------------
  infinity-router watch
"""

import json
import os
import re
import signal
import subprocess
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Optional

from infinity_router.models import (
    get_ranked_free_models,
    is_rate_limited,
    mark_rate_limited,
    expire_stale_rate_limits,
)
from infinity_router.targets import (
    BaseTarget,
    get_target,
    FREE_ROUTER,
)


# ── Tunables ──────────────────────────────────────────────────────────────────
LOG_DIR         = Path("/tmp/openclaw")
FAILURE_WINDOW  = 120   # seconds — sliding window for counting failures
FAILURE_THRESH  = 3     # failures in window → trigger rotation
ROTATE_COOLDOWN = 300   # seconds — minimum gap between rotations (5 min)
POLL_INTERVAL   = 2     # seconds — how often to read new log lines

# ── Failure patterns (matched against each log line) ──────────────────────────
_FAILURE_RE = re.compile(
    r"FailoverError"
    r"|Unknown model"
    r"|model_not_found"
    r"|No endpoints found"
    r"|tool.use.*not.supported"
    r"|free-models-per"
    r"|all.*fallback.*failed",
    re.IGNORECASE,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _today_log() -> Path:
    return LOG_DIR / f"openclaw-{datetime.now().strftime('%Y-%m-%d')}.log"


def _api_key() -> Optional[str]:
    raw = os.environ.get("OPENROUTER_API_KEY", "")
    if raw:
        return raw.split(",")[0].strip()
    from infinity_router.targets import _OPENCLAW_PATH
    if _OPENCLAW_PATH.exists():
        try:
            cfg = json.loads(_OPENCLAW_PATH.read_text())
            raw = cfg.get("env", {}).get("OPENROUTER_API_KEY", "")
            if raw:
                return raw.split(",")[0].strip()
        except Exception:
            pass
    # auth-profiles.json fallback
    auth_profiles = Path.home() / ".openclaw/agents/main/agent/auth-profiles.json"
    if auth_profiles.exists():
        try:
            ap  = json.loads(auth_profiles.read_text())
            raw = ap.get("profiles", {}).get("openrouter:default", {}).get("key", "")
            if raw:
                return raw.split(",")[0].strip()
        except Exception:
            pass
    return None


def _restart_gateway() -> bool:
    """Run `openclaw gateway restart`. Returns True on success."""
    try:
        r = subprocess.run(
            ["openclaw", "gateway", "restart"],
            capture_output=True, text=True, timeout=30,
        )
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _notify(url: str, model: str, reason: str) -> None:
    """POST rotation event to a webhook URL (optional)."""
    try:
        import requests
        requests.post(
            url,
            json={"text": f"[infinity-router] rotated → {model}  ({reason})"},
            timeout=10,
        )
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────────────────────
# Entry point  (infinity-router-watch)
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse
    from infinity_router.targets import get_target

    parser = argparse.ArgumentParser(
        prog="infinity-router-watch",
        description="Tail OpenClaw gateway log and auto-rotate models on failures.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  infinity-router-watch\n"
            "  infinity-router-watch --verbose\n"
            "  infinity-router-watch --thresh 5 --window 60\n"
            "  infinity-router-watch --notify https://hooks.example.com/xyz\n"
        ),
    )
    parser.add_argument("--window",   "-w", type=int, default=FAILURE_WINDOW,
                        help=f"Failure sliding window in seconds (default {FAILURE_WINDOW})")
    parser.add_argument("--thresh",   "-n", type=int, default=FAILURE_THRESH,
                        help=f"Failures in window before rotating (default {FAILURE_THRESH})")
    parser.add_argument("--cooldown", "-c", type=int, default=ROTATE_COOLDOWN,
                        help=f"Min seconds between rotations (default {ROTATE_COOLDOWN})")
    parser.add_argument("--notify",         default="",
                        help="Webhook URL to POST rotation events (optional)")
    parser.add_argument("--verbose",  "-v", action="store_true",
                        help="Print every matched failure line")
    parser.add_argument("--target",   "-t", default="openclaw", metavar="TARGET",
                        help="config target: openclaw | claude-code  (default: openclaw)")

    args   = parser.parse_args()
    target = get_target(args.target)

    run_watch(
        target=target,
        notify_url=args.notify or None,
        verbose=args.verbose,
        failure_window=args.window,
        failure_thresh=args.thresh,
        rotate_cooldown=args.cooldown,
    )


if __name__ == "__main__":
    main()


# ──────────────────────────────────────────────────────────────────────────────
# Rotation
# ──────────────────────────────────────────────────────────────────────────────

def _rotate(api_key: str, target: BaseTarget, reason: str) -> Optional[str]:
    """
    Mark the current primary as rate-limited, pick the next best model,
    write primary + fallbacks, return the new model ID (or None on failure).
    """
    current = target.read_primary()
    current_base = current.removeprefix("openrouter/") if current else None

    if current_base:
        mark_rate_limited(current_base)

    expire_stale_rate_limits()
    models = get_ranked_free_models(api_key)

    nxt = None
    for m in models:
        mid = m["id"]
        if "openrouter/free" in mid:
            continue
        if current_base and mid == current_base:
            continue
        if is_rate_limited(mid):
            continue
        nxt = mid
        break

    if not nxt:
        print(f"[{_ts()}] no available model — all rate-limited")
        return None

    print(f"[{_ts()}] rotate  {current_base or '?'} → {nxt}  ({reason})")
    target.write_primary(nxt)

    fallbacks = [FREE_ROUTER]
    for m in models:
        if len(fallbacks) >= 5:
            break
        mid = m["id"]
        if "openrouter/free" in mid or mid == nxt or is_rate_limited(mid):
            continue
        fallbacks.append(mid)
    target.write_fallbacks(fallbacks)
    print(f"  fallbacks: {fallbacks}")

    return nxt


# ──────────────────────────────────────────────────────────────────────────────
# Main watch loop
# ──────────────────────────────────────────────────────────────────────────────

def run_watch(
    target: BaseTarget,
    notify_url: Optional[str] = None,
    verbose: bool = False,
    failure_window: int = FAILURE_WINDOW,
    failure_thresh: int = FAILURE_THRESH,
    rotate_cooldown: int = ROTATE_COOLDOWN,
) -> None:
    """
    Tail the OpenClaw log and auto-rotate + restart gateway when
    failures spike above the threshold. Runs until SIGINT / SIGTERM.
    """
    api_key = _api_key()
    if not api_key:
        sys.exit("Error: OPENROUTER_API_KEY not set")

    print("infinity-router watch")
    print(f"  target          {target.label}")
    print(f"  log dir         {LOG_DIR}")
    print(f"  failure window  {failure_window}s")
    print(f"  threshold       {failure_thresh} failures → rotate")
    print(f"  rotate cooldown {rotate_cooldown}s")
    if notify_url:
        print(f"  notify          {notify_url[:40]}…")
    print("─" * 50)

    running       = True
    failures: deque = deque()   # timestamps of recent failures
    last_rotate   = 0.0         # epoch of last rotation
    log_path      = _today_log()
    file_pos      = 0

    # Start from the end of the existing log (don't replay old entries)
    if log_path.exists():
        file_pos = log_path.stat().st_size
        print(f"[{_ts()}] watching {log_path.name} (pos={file_pos})")
    else:
        print(f"[{_ts()}] waiting for {log_path.name} …")

    def _stop(sig, frame):
        nonlocal running
        print("\n[watch] stopping …")
        running = False

    signal.signal(signal.SIGINT,  _stop)
    signal.signal(signal.SIGTERM, _stop)

    while running:
        # ── Date rollover ─────────────────────────────────────────────────────
        new_log = _today_log()
        if new_log != log_path:
            log_path = new_log
            file_pos = 0
            print(f"[{_ts()}] new log: {log_path.name}")

        # ── Read new lines ────────────────────────────────────────────────────
        new_lines: list[str] = []
        if log_path.exists():
            try:
                with open(log_path, "r", errors="replace") as fh:
                    fh.seek(file_pos)
                    new_lines = fh.readlines()
                    file_pos  = fh.tell()
            except OSError:
                pass

        now = time.monotonic()

        for line in new_lines:
            if _FAILURE_RE.search(line):
                failures.append(now)
                if verbose:
                    print(f"  [{_ts()}] ✗ {line.strip()[:120]}")

        # ── Expire old failures ───────────────────────────────────────────────
        cutoff = now - failure_window
        while failures and failures[0] < cutoff:
            failures.popleft()

        # ── Threshold check ───────────────────────────────────────────────────
        if len(failures) >= failure_thresh and now - last_rotate >= rotate_cooldown:
            count  = len(failures)
            reason = f"{count} failures in {failure_window}s"
            print(f"[{_ts()}] threshold hit — {reason}")
            failures.clear()

            new_model = _rotate(api_key, target, reason)
            if new_model:
                last_rotate = now
                print(f"[{_ts()}] restarting gateway …", end=" ", flush=True)
                ok = _restart_gateway()
                print("OK" if ok else "FAILED — run: openclaw gateway restart")

                if notify_url:
                    _notify(notify_url, new_model, reason)

        time.sleep(POLL_INTERVAL)

    print("[watch] stopped.")
