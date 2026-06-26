"""
cli.py — `infinity-router` command-line interface.

Commands
--------
scan    discover and rank all free models
pick    auto-configure the best model + fallback chain
use     set a specific model by name (exact or partial)
bench   latency-test the top N models
status  show current config, cache state, and target info
reset   remove model config from the target
"""

import argparse
import json
import os
import sys
import time
from typing import Optional

from infinity_router.models import (
    get_ranked_free_models,
    cache_summary,
    clear_rate_limits,
    CACHE_TTL_H,
    COOLDOWN_MIN,
)
from infinity_router.probe import bench_model, validate_models
from infinity_router.targets import (
    BaseTarget,
    OpenClawTarget,
    get_target,
    list_targets,
    fmt_primary,
    fmt_list,
    FREE_ROUTER,
)


# ──────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ──────────────────────────────────────────────────────────────────────────────

def _api_keys() -> list[str]:
    """
    Return all configured OpenRouter API keys, deduplicated, order preserved.

    Sources checked (in priority order):
      1. Env var   OPENROUTER_API_KEY=key1,key2,...
      2. openclaw.json  env.OPENROUTER_API_KEY
      3. auth-profile.json  profiles.openrouter:default.key
         (~/.openclaw/agents/main/agent/auth-profile.json)

    Each source may contain one key or multiple comma-separated keys.
    NOTE: auth-profile.json should use only ONE key per profile for OpenClaw
    inference to work correctly. Store extra keys in openclaw.json env or env var.
    """
    from pathlib import Path
    from infinity_router.targets import _OPENCLAW_PATH

    raw_sources: list[str] = []

    # 1. Environment variable
    env_raw = os.environ.get("OPENROUTER_API_KEY", "")
    if env_raw:
        raw_sources.append(env_raw)

    # 2. openclaw.json env block
    if _OPENCLAW_PATH.exists():
        try:
            cfg = json.loads(_OPENCLAW_PATH.read_text())
            oc_raw = cfg.get("env", {}).get("OPENROUTER_API_KEY", "")
            if oc_raw:
                raw_sources.append(oc_raw)
        except Exception:
            pass

    # 3. auth-profile.json (OpenClaw's per-agent key store)
    auth_profile = Path.home() / ".openclaw/agents/main/agent/auth-profiles.json"
    if auth_profile.exists():
        try:
            ap = json.loads(auth_profile.read_text())
            ap_raw = (
                ap.get("profiles", {})
                  .get("openrouter:default", {})
                  .get("key", "")
            )
            if ap_raw:
                raw_sources.append(ap_raw)
        except Exception:
            pass

    # Parse and deduplicate
    seen: set[str] = set()
    keys: list[str] = []
    for src in raw_sources:
        for k in src.split(","):
            k = k.strip()
            if k and k not in seen:
                seen.add(k)
                keys.append(k)
    return keys


def _api_key() -> Optional[str]:
    keys = _api_keys()
    return keys[0] if keys else None


def _require_key() -> str:
    keys = _api_keys()
    if not keys:
        sys.exit(
            "Error: OPENROUTER_API_KEY is not set.\n"
            "  export OPENROUTER_API_KEY='sk-or-...'\n"
            "  Free key → https://openrouter.ai/keys"
        )
    return keys[0]


def _require_keys() -> list[str]:
    keys = _api_keys()
    if not keys:
        sys.exit(
            "Error: OPENROUTER_API_KEY is not set.\n"
            "  export OPENROUTER_API_KEY='sk-or-...'\n"
            "  Free key → https://openrouter.ai/keys"
        )
    return keys


def _fmt_ctx(tokens: int) -> str:
    if tokens >= 1_000_000:
        return f"{tokens // 1_000_000}M"
    if tokens >= 1_000:
        return f"{tokens // 1_000}K"
    return str(tokens)


_PROBE_DELAY = 1.5   # seconds between probes on the same key
_PROBE_LIMIT = 12    # max candidates to probe per run


def _probe_model(
    keys: list[str], mid: str, key_idx: int = 0
) -> tuple[bool, str | None, int]:
    """
    Probe one model, rotating through all keys on rate-limit.
    Returns (ok, error, next_key_idx).
    """
    from infinity_router.probe import health_check
    n = len(keys)
    for i in range(n):
        key = keys[(key_idx + i) % n]
        ok, err = health_check(key, mid, timeout=12)
        if err != "rate_limit":
            return ok, err, (key_idx + i + 1) % n
        # all keys exhausted on rate_limit — return failure
    return False, "rate_limit(all keys)", (key_idx + 1) % n


def _build_fallback_chain(
    keys: list[str], exclude: str, count: int, target: BaseTarget,
    validate: bool = False,
) -> list[str]:
    """
    Build a fallback list of `count` entries.
    openrouter/free (smart router) is always inserted first.
    `exclude` is the new primary model — skip it.
    When validate=True, candidates are probed with key rotation and delay.
    Probing is capped at _PROBE_LIMIT to avoid flooding.
    """
    api_key = keys[0]
    models  = get_ranked_free_models(api_key)
    current = target.read_primary()
    chain   = []

    primary_of_free = fmt_primary(FREE_ROUTER)
    if fmt_primary(exclude) != primary_of_free:
        chain.append(FREE_ROUTER)

    candidates = []
    for m in models:
        mid = m["id"]
        if "openrouter/free" in mid:
            continue
        if mid == exclude:
            continue
        if current and fmt_primary(mid) == current:
            continue
        candidates.append(mid)

    if validate and candidates:
        needed  = count - len(chain)
        pool    = candidates[:_PROBE_LIMIT]
        nk      = len(keys)
        print(f"  validating top {len(pool)} candidates ({nk} key(s), {_PROBE_DELAY}s delay) …")
        valid   = []
        key_idx = 0
        for i, mid in enumerate(pool):
            if len(valid) >= needed:
                break
            if i > 0:
                # shorter delay when rotating keys
                sleep_t = _PROBE_DELAY / nk if nk > 1 else _PROBE_DELAY
                time.sleep(sleep_t)
            label = mid[:55]
            print(f"    {label:<55}", end="", flush=True)
            ok, err, key_idx = _probe_model(keys, mid, key_idx)
            if ok:
                valid.append(mid)
                print("  ✓")
            else:
                print(f"  ✗  {err}")
        candidates = valid

    for mid in candidates:
        if len(chain) >= count:
            break
        chain.append(mid)

    return chain


# ──────────────────────────────────────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────────────────────────────────────

def cmd_scan(args: argparse.Namespace) -> None:
    api_key = _require_key()
    target  = get_target(args.target)

    print("Scanning OpenRouter for free models …\n")
    try:
        models = get_ranked_free_models(api_key, refresh=args.refresh)
    except ConnectionError as e:
        sys.exit(str(e))

    if not models:
        sys.exit("No free models found.")

    limit   = args.limit
    current = target.read_primary()
    fbs     = target.read_fallbacks()

    W = 52
    print(f"  {'#':<3}  {'Model ID':<{W}}  {'Context':<8}  {'Score':<7}  Status")
    print("  " + "─" * (W + 30))

    for i, m in enumerate(models[:limit], 1):
        mid = m.get("id", "?")
        ctx = _fmt_ctx(m.get("context_length", 0))
        sc  = m.get("_score", 0.0)

        tag = ""
        if current and fmt_primary(mid) == current:
            tag = "● primary"
        elif fmt_list(mid) in fbs or fmt_primary(mid) in fbs:
            tag = "· fallback"

        print(f"  {i:<3}  {mid:<{W}}  {ctx:<8}  {sc:.3f}    {tag}")

    extra = len(models) - limit
    if extra > 0:
        print(f"\n  … {extra} more. Pass --limit {limit + 10} to see more.")

    print(f"\n  Total: {len(models)} free models   Cache: {cache_summary()}")
    print("  Try:   infinity-router pick   or   infinity-router use <name>")


def cmd_pick(args: argparse.Namespace) -> None:
    keys    = _require_keys()
    api_key = keys[0]
    target  = get_target(args.target)

    if args.auth and isinstance(target, OpenClawTarget):
        target.ensure_auth_profile()

    nk = len(keys)
    print(f"Selecting best free model … ({nk} API key(s))")
    try:
        models = get_ranked_free_models(api_key, refresh=True)
    except ConnectionError as e:
        sys.exit(str(e))

    if not models:
        sys.exit("No free models returned from OpenRouter.")

    candidates = [m for m in models if "openrouter/free" not in m["id"]]

    if args.validate:
        print("  probing candidates for a working primary …")
        best    = None
        key_idx = 0
        for i, m in enumerate(candidates[:_PROBE_LIMIT]):
            mid_try = m["id"]
            label   = mid_try[:55]
            print(f"    {label:<55}", end="", flush=True)
            if i > 0:
                time.sleep(_PROBE_DELAY / nk if nk > 1 else _PROBE_DELAY)
            ok, err, key_idx = _probe_model(keys, mid_try, key_idx)
            if ok:
                print("  ✓  → primary")
                best = m
                break
            else:
                print(f"  ✗  {err}")
        if best is None:
            sys.exit("No reachable primary model found after probing.")
    else:
        best = candidates[0] if candidates else models[0]

    mid  = best["id"]
    ctx  = best.get("context_length", 0)
    sc   = best.get("_score", 0.0)

    if not args.fallbacks_only:
        old = target.read_primary()
        if old:
            print(f"  replacing  {old}")
        print(f"  primary    {mid}")
        print(f"  context    {_fmt_ctx(ctx)} tokens    score {sc:.3f}")
        target.write_primary(mid)
    else:
        print(f"  primary unchanged  ({target.read_primary() or 'none'})")
        print(f"  best available     {mid}  ({_fmt_ctx(ctx)} tokens, score {sc:.3f})")

    if not args.no_fallbacks:
        chain = _build_fallback_chain(
            keys, mid, args.count, target, validate=args.validate
        )
        target.write_fallbacks(chain)
        print(f"\n  fallbacks ({len(chain)}):")
        for fb in chain:
            print(f"    ↳  {fb}")

    print(f"\n  [{target.label}] config updated.")
    if isinstance(target, OpenClawTarget):
        print("  run: openclaw gateway restart")


def cmd_use(args: argparse.Namespace) -> None:
    keys    = _require_keys()
    api_key = keys[0]
    target  = get_target(args.target)
    query   = args.model

    try:
        models = get_ranked_free_models(api_key)
    except ConnectionError as e:
        sys.exit(str(e))

    ids     = [m["id"] for m in models]
    matched = query if query in ids else next(
        (mid for mid in ids if query.lower() in mid.lower()), None
    )

    if not matched:
        sys.exit(
            f"No free model matching '{query}'.\n"
            "  Run: infinity-router scan"
        )

    if args.fallbacks_only:
        existing = target.read_fallbacks()
        if fmt_list(matched) not in existing:
            target.write_fallbacks([matched, *existing])
        print(f"  added to fallbacks  {matched}")
        print(f"  primary unchanged   ({target.read_primary() or 'none'})")
    else:
        print(f"  setting primary  {matched}")
        target.write_primary(matched)
        if not args.no_fallbacks:
            validate = getattr(args, "validate", False)
            chain = _build_fallback_chain(keys, matched, 5, target, validate=validate)
            target.write_fallbacks(chain)
            preview = ", ".join(chain[:3])
            if len(chain) > 3:
                preview += " …"
            print(f"  fallbacks        {preview}")

    print(f"\n  [{target.label}] done.")
    if isinstance(target, OpenClawTarget):
        print("  run: openclaw gateway restart")


def cmd_bench(args: argparse.Namespace) -> None:
    api_key = _require_key()

    try:
        models = get_ranked_free_models(api_key)
    except ConnectionError as e:
        sys.exit(str(e))

    pool = [m for m in models if "openrouter/free" not in m["id"]][:args.count]
    print(f"Benchmarking {len(pool)} models …\n")

    results: list[tuple[str, bool, int, str | None]] = []

    for m in pool:
        mid = m["id"]
        label = mid[:60]
        print(f"  {label:<60}", end="", flush=True)
        ok, ms, err = bench_model(api_key, mid)
        if ok:
            print(f"  ✓  {ms} ms")
        else:
            print(f"  ✗  {err}")
        results.append((mid, ok, ms, err))

    ok_results = sorted(
        [(mid, ms) for mid, ok, ms, _ in results if ok],
        key=lambda x: x[1],
    )
    failed = [mid for mid, ok, _, _ in results if not ok]

    print(f"\n  Ranked by latency:")
    for rank, (mid, ms) in enumerate(ok_results, 1):
        print(f"    {rank}.  {mid}  —  {ms} ms")

    if failed:
        names = ", ".join(m.split("/")[-1] for m in failed)
        print(f"\n  Unreachable ({len(failed)}): {names}")


def cmd_status(args: argparse.Namespace) -> None:
    keys   = _api_keys()
    target = get_target(args.target)

    print("Infinity-Router")
    print("─" * 50)

    if keys:
        for i, k in enumerate(keys, 1):
            masked = f"{k[:8]}…{k[-4:]}" if len(k) > 12 else "***"
            label  = f"API key {i}" if len(keys) > 1 else "API key"
            print(f"  {label:<12}  {masked}")
    else:
        print("  API key     NOT SET  ←  export OPENROUTER_API_KEY='sk-or-…'")

    print(f"\n  Targets:")
    for name, t in list_targets():
        state  = "found" if t.exists() else "not found"
        active = "  ← active" if t.label == target.label else ""
        print(f"    {t.label:<14}  {state}{active}")

    primary = target.read_primary()
    print(f"\n  Primary     {primary or '(none)'}")

    fbs = target.read_fallbacks()
    if fbs:
        print(f"  Fallbacks ({len(fbs)}):")
        for fb in fbs:
            print(f"              ↳  {fb}")
    else:
        print(f"  Fallbacks   (none)")

    print(f"\n  Cache       {cache_summary()}")
    print(f"  Cache TTL   {CACHE_TTL_H}h   |   RL cooldown {COOLDOWN_MIN}m")


def cmd_watch(args: argparse.Namespace) -> None:
    from infinity_router.watcher import run_watch
    target = get_target(args.target)
    run_watch(
        target=target,
        notify_url=args.notify or None,
        verbose=args.verbose,
        failure_window=args.window,
        failure_thresh=args.thresh,
        rotate_cooldown=args.cooldown,
    )


def cmd_reset(args: argparse.Namespace) -> None:
    target = get_target(args.target)

    if not target.exists():
        print(f"  [{target.label}] config not found — nothing to reset.")
        return

    if hasattr(target, "clear_model_config"):
        target.clear_model_config()
        print(f"  [{target.label}] model config cleared.")
    else:
        print(f"  [{target.label}] does not support reset.")

    if args.clear_rl:
        clear_rate_limits()
        print("  rate-limit records cleared.")


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    root = argparse.ArgumentParser(
        prog="infinity-router",
        description="Unlimited free AI routing via OpenRouter.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "commands:\n"
            "  scan    discover and rank free models\n"
            "  pick    auto-configure best model + fallbacks\n"
            "  use     set a specific model\n"
            "  bench   latency-test top models\n"
            "  watch   tail gateway log, auto-rotate on failures\n"
            "  status  show current state\n"
            "  reset   remove model config\n"
        ),
    )
    root.add_argument("--version", action="version", version="infinity-router 2.1.0")

    _target = dict(
        dest="target", default="openclaw", metavar="TARGET",
        help="config target: openclaw | claude-code  (default: openclaw)",
    )
    sub = root.add_subparsers(dest="cmd")

    # scan ────────────────────────────────────────────────────────────────────
    p = sub.add_parser("scan", help="Discover and rank free models")
    p.add_argument("--limit",   "-n", type=int, default=20, help="Rows to show (default 20)")
    p.add_argument("--refresh", "-r", action="store_true",  help="Bypass cache")
    p.add_argument("--target",  "-t", **_target)

    # pick ────────────────────────────────────────────────────────────────────
    p = sub.add_parser("pick", help="Auto-configure best model + fallbacks")
    p.add_argument("--count",          "-c", type=int, default=5, help="Fallback count (default 5)")
    p.add_argument("--fallbacks-only", "-f", action="store_true",  help="Keep primary, update fallbacks only")
    p.add_argument("--no-fallbacks",         action="store_true",  help="Skip fallback config")
    p.add_argument("--validate",       "-v", action="store_true",  help="Probe each fallback before writing (slower but safe)")
    p.add_argument("--auth",                 action="store_true",  help="Ensure OpenRouter auth profile (OpenClaw)")
    p.add_argument("--target",         "-t", **_target)

    # use ─────────────────────────────────────────────────────────────────────
    p = sub.add_parser("use", help="Set a specific model (exact or partial name)")
    p.add_argument("model", help="Model ID or partial name")
    p.add_argument("--fallbacks-only", "-f", action="store_true", help="Add to fallbacks, keep primary")
    p.add_argument("--no-fallbacks",         action="store_true", help="Skip fallback config")
    p.add_argument("--validate",       "-v", action="store_true", help="Probe each fallback before writing")
    p.add_argument("--target",         "-t", **_target)

    # bench ───────────────────────────────────────────────────────────────────
    p = sub.add_parser("bench", help="Latency-test top models")
    p.add_argument("--count", "-c", type=int, default=5, help="Models to test (default 5)")

    # status ──────────────────────────────────────────────────────────────────
    p = sub.add_parser("status", help="Show config and cache state")
    p.add_argument("--target", "-t", **_target)

    # watch ───────────────────────────────────────────────────────────────────
    p = sub.add_parser("watch", help="Tail gateway log and auto-rotate on failures")
    p.add_argument("--window",   "-w", type=int, default=120,
                   help="Failure sliding window in seconds (default 120)")
    p.add_argument("--thresh",   "-n", type=int, default=3,
                   help="Failures in window before rotating (default 3)")
    p.add_argument("--cooldown", "-c", type=int, default=300,
                   help="Min seconds between rotations (default 300)")
    p.add_argument("--notify",         default="",
                   help="Webhook URL to POST rotation events (optional)")
    p.add_argument("--verbose",  "-v", action="store_true",
                   help="Print every matched failure line")
    p.add_argument("--target",   "-t", **_target)

    # reset ───────────────────────────────────────────────────────────────────
    p = sub.add_parser("reset", help="Remove model config from target")
    p.add_argument("--clear-rl", action="store_true", help="Also clear rate-limit records")
    p.add_argument("--target", "-t", **_target)

    # ─────────────────────────────────────────────────────────────────────────
    args = root.parse_args()
    dispatch = {
        "scan":   cmd_scan,
        "pick":   cmd_pick,
        "use":    cmd_use,
        "bench":  cmd_bench,
        "watch":  cmd_watch,
        "status": cmd_status,
        "reset":  cmd_reset,
    }

    fn = dispatch.get(args.cmd)
    if fn:
        fn(args)
    else:
        root.print_help()


if __name__ == "__main__":
    main()
