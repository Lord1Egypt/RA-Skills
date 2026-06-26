#!/usr/bin/env python3
"""
discover_models.py — Fetch and rank free OpenRouter models.
Usage:
  python3 discover_models.py           # use cache if fresh
  python3 discover_models.py --refresh # force fresh fetch
"""
import json
import math
import os
import sys
import time
import urllib.request
from pathlib import Path

MODELS_URL  = "https://openrouter.ai/api/v1/models"
CACHE_FILE  = Path("/tmp/.openrouter_free_models_cache.json")
CACHE_TTL   = 3600  # seconds


def load_env_simple(path: Path) -> dict:
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        result[k.strip()] = v.strip().strip("\"'")
    return result


def get_env():
    env = {}
    env.update(load_env_simple(Path.home() / ".env"))
    env.update(load_env_simple(Path(".env")))
    env.update(os.environ)
    return env


def fetch_free_models(force_refresh: bool = False) -> list:
    if not force_refresh and CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        if age < CACHE_TTL:
            return json.loads(CACHE_FILE.read_text())

    print("[openrouter-connect] Fetching model list from OpenRouter...", file=sys.stderr)
    with urllib.request.urlopen(MODELS_URL, timeout=10) as resp:
        all_models = json.loads(resp.read())["data"]

    free = [
        m for m in all_models
        if m.get("pricing", {}).get("prompt") == "0"
        and m.get("pricing", {}).get("completion") == "0"
    ]
    CACHE_FILE.write_text(json.dumps(free))
    print(f"[openrouter-connect] Found {len(free)} free models (cached to {CACHE_FILE})", file=sys.stderr)
    return free


def auto_rank(free_models: list, env: dict) -> list:
    tier_a = set((env.get("OPENROUTER_TIER_A") or "google,meta-llama,mistralai,anthropic").split(","))
    tier_b = set((env.get("OPENROUTER_TIER_B") or "qwen,nvidia,microsoft,cohere,deepseek").split(","))
    now = time.time()
    scored = []
    for m in free_models:
        ctx   = m.get("context_length", 4096)
        ctx_s = min(math.log(max(ctx, 1)) / math.log(200_000), 1.0)

        created  = m.get("created", 0)
        age_days = (now - created) / 86400 if created else 730
        rec_s    = max(0.0, 1.0 - age_days / 730)

        provider = m["id"].split("/")[0]
        rep_s    = 1.0 if provider in tier_a else (0.7 if provider in tier_b else 0.4)

        score = 0.4 * ctx_s + 0.3 * rec_s + 0.3 * rep_s
        scored.append((score, m))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [m for _, m in scored]


def main():
    force_refresh = "--refresh" in sys.argv
    env = get_env()

    free_models = fetch_free_models(force_refresh)
    ranked      = auto_rank(free_models, env)

    # Apply user's preferred list if set
    preferred_env = env.get("OPENROUTER_PREFERRED_MODELS", "")
    preferred     = [p.strip() for p in preferred_env.split(",") if p.strip()]

    free_ids = {m["id"] for m in ranked}
    ordered  = [m for m in preferred if m in free_ids] + \
               [m for m in ranked if m["id"] not in preferred]

    print("\nFree models found (ranked):")
    print(f"  {'#':<4} {'Model ID':<55} {'Context':>10}  {'Provider':<14} Score")
    print("  " + "-" * 95)
    for i, m in enumerate(ordered[:20], 1):
        ctx      = m.get("context_length", 0)
        ctx_str  = f"{ctx // 1000}k" if ctx else "?"
        provider = m["id"].split("/")[0]
        stars    = "★★★" if provider in {"google","meta-llama","mistralai","anthropic"} else \
                   "★★☆" if provider in {"qwen","nvidia","microsoft","cohere","deepseek"} else "★☆☆"
        print(f"  {i:<4} {m['id']:<55} {ctx_str:>10}  {provider:<14} {stars}")

    print(f"\n  ... and {max(0, len(ordered)-20)} more (use --refresh to update)\n")

    # Output JSON for piping to other scripts
    if "--json" in sys.argv:
        print(json.dumps([m["id"] for m in ordered]))


if __name__ == "__main__":
    main()
