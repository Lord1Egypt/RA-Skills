#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""
subagent_backoff.py — F33 (v1.9.0).

Orchestration helper for swarm/kanban runs: wraps a subagent call with exponential
backoff so a transient 429 (rate-limit, observed on deleg_ee76efe3 at the 39th call)
doesn't abort the whole swarm. Pure stdlib.

USAGE (as a library):
    from subagent_backoff import with_backoff
    result = with_backoff(lambda: call_subagent(goal), max_retries=5, base_delay=2.0)

USAGE (CLI wrapper):
    python subagent_backoff.py -- python my_spawn_script.py arg1 arg2
"""
import subprocess
import sys
import time


def with_backoff(fn, max_retries=5, base_delay=2.0, backoff=2.0):
    """Call fn(); on exception, retry with exponential sleep. Raise after max_retries."""
    last = None
    for attempt in range(1, max_retries + 1):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 — we re-raise after budget
            last = e
            if attempt == max_retries:
                break
            sleep = base_delay * (backoff ** (attempt - 1))
            print(f"[subagent_backoff] attempt {attempt} failed ({type(e).__name__}); "
                  f"retry in {sleep:.1f}s", file=sys.stderr)
            time.sleep(sleep)
    raise last


def main():
    if "--" not in sys.argv:
        print("usage: python subagent_backoff.py -- <cmd> [args...]", file=sys.stderr)
        return 2
    cmd = sys.argv[sys.argv.index("--") + 1:]

    def _run():
        r = subprocess.run(cmd)
        if r.returncode != 0:
            raise RuntimeError(f"command exited {r.returncode}")
        return r

    try:
        with_backoff(_run)
        return 0
    except Exception as e:
        print(f"[subagent_backoff] FAILED after retries: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
