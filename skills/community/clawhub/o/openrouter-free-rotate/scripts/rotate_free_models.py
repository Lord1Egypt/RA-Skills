#!/usr/bin/env python3
"""OpenRouter Free Model Rotate v2.0

Full-featured scanner: capability-aware scoring, concurrent testing,
smart fallback selection, result caching, and JSON/Markdown reports.

Usage examples:
    python3 rotate_free_models.py --api-key SK_OR_XXX --restart
    python3 rotate_free_models.py --api-key SK_OR_XXX --scan --sort score
    python3 rotate_free_models.py --api-key SK_OR_XXX --bench
    python3 rotate_free_models.py --api-key SK_OR_XXX --filter multimodal
    python3 rotate_free_models.py --api-key SK_OR_XXX --json /tmp/report.json
"""

import argparse
import base64
import json
import os
import sys
import time
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

# ──────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────

API_BASE = "https://openrouter.ai/api/v1"

# Scoring weights — higher = more preferred
SCORE_CONTEXT_PER_100K = 2        # context window bonus
SCORE_MAX_TOKENS_PER_1K = 0.5     # output length bonus
SCORE_REASONING = 8               # reasoning bonus
SCORE_MULTIMODAL = 5              # image/audio input bonus
SCORE_VIDEO = 3                   # video input bonus
SCORE_SPEED_PER_100MS = -0.3      # latency penalty

# Quality benchmark prompt (tests following instructions + creativity)
BENCH_PROMPT = "Reply with exactly: PONG"

# ──────────────────────────────────────────────────────
# OpenRouter API
# ──────────────────────────────────────────────────────

def api_request(api_key, endpoint, body, timeout=30):
    """Generic POST to OpenRouter."""
    req_data = json.dumps(body).encode()
    req = __import__("urllib.request").request.Request(
        f"{API_BASE}/{endpoint}",
        data=req_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openclaw.ai",
            "X-Title": "OpenClaw"
        }
    )
    import urllib.request, urllib.error
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, json.loads(resp.read()), ""
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="ignore")[:200]
        return e.status, None, f"HTTP {e.code}: {err_body}"
    except urllib.error.URLError as e:
        return 0, None, str(e.reason)[:100]
    except Exception as e:
        return 0, None, str(e)[:100]


def fetch_all_models(api_key):
    """Fetch all models, filter free ones."""
    import urllib.request, urllib.error
    req = urllib.request.Request(
        f"{API_BASE}/models",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "HTTP-Referer": "https://openclaw.ai",
            "X-Title": "OpenClaw"
        }
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        models = data.get("data", [])
        free = []
        for m in models:
            pricing = m.get("pricing", {})
            p = float(pricing.get("prompt", "0"))
            c = float(pricing.get("completion", "0"))
            if p == 0 and c == 0:
                free.append(m)
        return free
    except Exception as e:
        print(f"Failed to fetch models: {e}")
        return []


# ──────────────────────────────────────────────────────
# Smart Scoring
# ──────────────────────────────────────────────────────

def score_model(m, latency_ms=0):
    """Score a model by capability. Higher = better."""
    s = 0
    ctx = m.get("context_length", 0)
    s += (ctx / 100000) * SCORE_CONTEXT_PER_100K  # context bonus

    arch = m.get("architecture", {})
    in_mods = arch.get("input_modalities", [])
    out_mods = arch.get("output_modalities", [])

    # Multimodal bonuses
    if "image" in in_mods:
        s += SCORE_MULTIMODAL
    if "audio" in in_mods:
        s += SCORE_MULTIMODAL
    if "video" in in_mods:
        s += SCORE_VIDEO

    # Reasoning support
    params = m.get("supported_parameters", [])
    if "reasoning" in params or "include_reasoning" in params:
        s += SCORE_REASONING

    # Output length
    tp = m.get("top_provider", {})
    max_tok = tp.get("max_completion_tokens") or 8192
    s += (max_tok / 1000) * SCORE_MAX_TOKENS_PER_1K

    # Latency penalty
    s += (latency_ms / 100) * SCORE_SPEED_PER_100MS

    # Known quality boosters (brand recognition)
    mid = m["id"].lower()
    if "qwen" in mid and "coder" in mid:
        s += 5
    if "qwen3" in mid or "qwen-3" in mid:
        s += 3
    if "llama" in mid and "70b" in mid:
        s += 4
    if "gpt" in mid:
        s += 2
    if "gemini" in mid or "gemma" in mid:
        s += 2
    if "mistral" in mid or "mixtral" in mid:
        s += 2

    return round(s, 1)


def get_capabilities(m):
    """Extract model capabilities as list."""
    arch = m.get("architecture", {})
    caps = []
    in_m = arch.get("input_modalities", [])
    if "text" in in_m:
        caps.append("text")
    if "image" in in_m:
        caps.append("image")
    if "audio" in in_m:
        caps.append("audio")
    if "video" in in_m:
        caps.append("video")

    params = m.get("supported_parameters", [])
    if "reasoning" in params or "include_reasoning" in params:
        caps.append("reasoning")

    return caps


# ──────────────────────────────────────────────────────
# Testing
# ──────────────────────────────────────────────────────

def test_model_quick(api_key, model_id, timeout=15):
    """Quick connectivity test."""
    t0 = time.time()
    status, data, err = api_request(
        api_key, "chat/completions",
        {"model": model_id, "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 3},
        timeout=timeout
    )
    latency = (time.time() - t0) * 1000
    if status == 200 and data and data.get("choices"):
        return True, latency, "", data
    return False, latency, f"HTTP {status}" if status else err, data


def test_model_bench(api_key, model_id, timeout=20):
    """Quality benchmark: test instruction following."""
    t0 = time.time()
    status, data, err = api_request(
        api_key, "chat/completions",
        {"model": model_id, "messages": [{"role": "user", "content": BENCH_PROMPT}], "max_tokens": 20},
        timeout=timeout
    )
    latency = (time.time() - t0) * 1000
    if status == 200 and data and data.get("choices"):
        reply = data["choices"][0].get("message", {}).get("content", "").strip()
        bench_ok = "PONG" in reply.upper()
        return True, latency, "", {"bench_ok": bench_ok, "reply": reply[:100]}
    return False, latency, f"HTTP {status}" if status else err, {}


def test_models_concurrent(api_key, models, max_workers=5, bench=False, timeout=15):
    """Test multiple models concurrently."""
    results = []
    total = len(models)
    print(f"\nTesting {total} models concurrently ({max_workers} workers)...\n")

    test_fn = test_model_bench if bench else test_model_quick

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_idx = {
            pool.submit(test_fn, api_key, m["id"], timeout): i
            for i, m in enumerate(models)
        }

        completed = 0
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            m = models[idx]
            try:
                ok, latency, error, extra = future.result()
                completed += 1
                model_info = dict(m)
                model_info["score"] = score_model(m, latency)
                model_info["latency"] = round(latency, 0)
                model_info["ok"] = ok
                model_info["error"] = error
                if bench and extra:
                    model_info["bench_ok"] = extra.get("bench_ok", False)
                    model_info["bench_reply"] = extra.get("reply", "")
                results.append(model_info)
                status_str = "OK" if ok else "FAIL"
                bench_info = f" bench={'OK' if model_info.get('bench_ok', False) else 'NO'}" if bench else ""
                err_info = f"\n        {error}" if error else ""
                print(f"  [{completed:3d}/{total}] {status_str:4s} {latency:7.0f}ms  score={model_info['score']:5.1f}  {m['id']}{bench_info}{err_info}")
            except Exception as e:
                completed += 1
                results.append({**m, "ok": False, "error": str(e)[:80], "latency": 0, "score": -99})
                print(f"  [{completed:3d}/{total}] ERR        0ms  {m['id']}\n        {e}")

    return results


# ──────────────────────────────────────────────────────
# Result Caching
# ──────────────────────────────────────────────────────

def cache_path():
    d = os.path.expanduser("~/.openclaw/state")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "openrouter-free-rotate-cache.json")


def load_cache():
    p = cache_path()
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {"models": {}, "last_run": None}


def save_cache(cache):
    cache["last_run"] = datetime.now(timezone.utc).isoformat()
    with open(cache_path(), "w") as f:
        json.dump(cache, f, indent=2)


model_cache = {}
_cache_loaded = False

def get_cached_test(model_id):
    global model_cache, _cache_loaded
    if not _cache_loaded:
        model_cache = load_cache().get("models", {})
        _cache_loaded = True
    entry = model_cache.get(model_id)
    if entry:
        ts = entry.get("tested_at", "")
        try:
            from datetime import datetime
            tested = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            age = datetime.now(timezone.utc) - tested
            if age.total_seconds() < 3600:  # 1 hour cache
                return entry
        except Exception:
            pass
    return None


def update_cache_entry(model_id, ok, latency, score):
    global model_cache
    model_cache[model_id] = {
        "ok": ok,
        "latency": latency,
        "score": score,
        "tested_at": datetime.now(timezone.utc).isoformat()
    }


def persist_cache():
    cache = {"models": model_cache, "last_run": datetime.now(timezone.utc).isoformat()}
    with open(cache_path(), "w") as f:
        json.dump(cache, f, indent=2)


# ──────────────────────────────────────────────────────
# Filtering
# ──────────────────────────────────────────────────────

def filter_models(models, filter_type=None):
    """Filter models by capability."""
    if not filter_type or filter_type == "all":
        return models

    results = []
    for m in models:
        caps = get_capabilities(m)
        if filter_type == "text" and "text" in caps:
            results.append(m)
        elif filter_type == "multimodal" and ("image" in caps or "audio" in caps or "video" in caps):
            results.append(m)
        elif filter_type == "image" and "image" in caps:
            results.append(m)
        elif filter_type == "reasoning":
            params = m.get("supported_parameters", [])
            if "reasoning" in params or "include_reasoning" in params:
                results.append(m)
        elif filter_type == "fast":
            ctx = m.get("context_length", 0)
            if ctx <= 32000:
                results.append(m)
        elif filter_type == "large":
            ctx = m.get("context_length", 0)
            if ctx >= 128000:
                results.append(m)
    return results


# ──────────────────────────────────────────────────────
# Report Generation
# ──────────────────────────────────────────────────────

def generate_report(results, sort_by="score", top_keep=10, bench=False):
    """Sort and pick best models."""
    # Sort: working first by score, then failing
    working = sorted([r for r in results if r["ok"]], key=lambda r: r.get("score", 0), reverse=True)
    failing = sorted([r for r in results if not r["ok"]], key=lambda r: r.get("score", 0), reverse=True)

    if sort_by == "latency":
        working = sorted(working, key=lambda r: r.get("latency", 99999))
    elif sort_by == "name":
        working = sorted(working, key=lambda r: r.get("id", ""))

    return working, failing


def print_table(working, failing, bench=False, json_out=None):
    """Print formatted results table."""
    print("\n" + "=" * 100)
    print(f"📊 OpenRouter Free Models Report — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 100)

    if working:
        print(f"\n✅ Working models ({len(working)}):")
        print(f"  {'#':<3} {'Score':>6} {'Latency':>8} {'Context':>10} {'Caps':<25} {'Model ID'}")
        print(f"  {'-'*3} {'-'*6} {'-'*8} {'-'*10} {'-'*25} {'-'*50}")
        for i, m in enumerate(working):
            caps = ",".join(get_capabilities(m)[:3])
            ctx = m.get("context_length", "?")
            score = m.get("score", 0)
            lat = m.get("latency", "?")
            mid = m["id"]
            bench_tag = ""
            if bench:
                bench_tag = " [B]" if m.get("bench_ok") else " [BX]"
            print(f"  {i+1:<3} {score:>6.1f} {lat:>7.0f}ms {str(ctx):>10} {caps:<25} {mid}{bench_tag}")

    if failing:
        print(f"\n❌ Failed models ({len(failing)}):")
        for i, m in enumerate(failing):
            err = m.get("error", "unknown")[:70]
            print(f"  {i+1:<3} {m.get('id','')}")
            print(f"       {err}")

    print(f"\n{'='*100}")
    print(f"Total: {len(working)+len(failing)} | Working: {len(working)} | Failed: {len(failing)}")
    if working:
        print(f"🏆 Best model: {working[0]['id']} (score={working[0]['score']:.1f})")
    print("=" * 100)

    # JSON export
    if json_out:
        os.makedirs(os.path.dirname(json_out) or ".", exist_ok=True)
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "working_count": len(working),
            "failed_count": len(failing),
            "working": [{"id": m["id"], "score": m.get("score", 0), "latency": m.get("latency", 0),
                         "context": m.get("context_length", 0), "caps": get_capabilities(m), "bench_ok": m.get("bench_ok")} for m in working],
            "failed": [{"id": m["id"], "error": m.get("error", "")} for m in failing]
        }
        with open(json_out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved to: {json_out}")

    return working


# ──────────────────────────────────────────────────────
# Config I/O
# ──────────────────────────────────────────────────────

def load_json(path):
    with open(os.path.expanduser(path), "r") as f:
        return json.load(f)


def save_json(path, data):
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def build_model_entry(m):
    arch = m.get("architecture", {})
    input_mods = arch.get("input_modalities", [])
    input_types = []
    for t in ["text", "image", "audio"]:
        if t in input_mods:
            input_types.append(t)
    if not input_types:
        input_types = ["text"]

    return {
        "id": m["id"],
        "name": m.get("name", m["id"]),
        "reasoning": False,
        "input": input_types,
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": m.get("context_length", 128000),
        "maxTokens": m.get("top_provider", {}).get("max_completion_tokens", 8192),
        "api": "openai-completions"
    }


def update_configs(working_models, config_path, models_json_path):
    """Update both config files."""
    ids = [m["id"] for m in working_models]

    # Update openclaw.json
    updated_config = False
    try:
        cfg = load_json(config_path)
        prov = cfg.get("models", {}).get("providers", {}).get("openrouter")
        if prov:
            prov["models"] = [{"id": mid, "name": mid} for mid in ids]
            defaults = cfg.get("agents", {}).get("defaults", {})
            if "models" in defaults:
                old = [k for k in defaults["models"] if k.startswith("openrouter/")]
                for k in old:
                    del defaults["models"][k]
                for mid in ids:
                    defaults["models"][f"openrouter/{mid}"] = {}
            save_json(config_path, cfg)
            updated_config = True
    except Exception as e:
        print(f"  ⚠ openclaw.json update failed: {e}")

    # Update models.json
    updated_models = False
    try:
        data = load_json(models_json_path)
        prov = data.get("providers", {}).get("openrouter")
        if prov:
            prov["models"] = [build_model_entry(m) for m in working_models]
            save_json(models_json_path, data)
            updated_models = True
    except Exception as e:
        print(f"  ⚠ models.json update failed: {e}")

    return updated_config, updated_models


def restart_gateway():
    import signal
    import glob
    pid_files = glob.glob(os.path.expanduser("~/.openclaw/state/run/gateway.pid"))
    if pid_files:
        try:
            with open(pid_files[0]) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGUSR1)
            print(f"  ✅ Sent SIGUSR1 to gateway (pid {pid})")
            return True
        except Exception as e:
            print(f"  ⚠ Failed to signal gateway: {e}")
    # Fallback
    try:
        import subprocess
        result = subprocess.run(["pgrep", "-f", "openclaw-gateway"], capture_output=True, text=True)
        if result.returncode == 0:
            for pid in result.stdout.strip().split("\n"):
                os.kill(int(pid), signal.SIGUSR1)
                print(f"  ✅ Sent SIGUSR1 to gateway (pid {pid.strip()})")
            return True
    except Exception:
        pass
    print("  ⚠ Could not find gateway. Restart manually.")
    return False


# ──────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OpenRouter Free Model Rotate v2.0 — Scan, benchmark, and auto-rotate free models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Rotate all free models, update configs, restart gateway:
    %(prog)s --api-key SK_OR --restart

  Scan and show sorted by score:
    %(prog)s --api-key SK_OR --scan --sort score

  Run quality benchmark:
    %(prog)s --api-key SK_OR --bench

  Filter only multimodal models:
    %(prog)s --api-key SK_OR --filter multimodal

  Test with concurrency + save report:
    %(prog)s --api-key SK_OR --workers 10 --json report.json

  Update without testing (use 1h cached results):
    %(prog)s --api-key SK_OR --use-cache --keep 8
"""
    )
    parser.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY"),
                        help="OpenRouter API key")
    parser.add_argument("--config", default="~/.openclaw/openclaw.json",
                        help="Path to openclaw.json")
    parser.add_argument("--models-json", default="~/.openclaw/agents/main/agent/models.json",
                        help="Path to models.json")
    parser.add_argument("--test", type=int, default=0,
                        help="Max models to test (0=all, default: 0)")
    parser.add_argument("--scan", action="store_true",
                        help="Just scan, no testing")
    parser.add_argument("--bench", action="store_true",
                        help="Run quality benchmark (PONG test)")
    parser.add_argument("--filter", default="all",
                        choices=["all", "text", "multimodal", "image", "reasoning", "fast", "large"],
                        help="Filter by capability")
    parser.add_argument("--sort", default="score",
                        choices=["score", "latency", "name"],
                        help="Sort order for results")
    parser.add_argument("--keep", type=int, default=10,
                        help="Number of working models to keep (default: 10)")
    parser.add_argument("--workers", type=int, default=5,
                        help="Concurrent test workers (default: 5)")
    parser.add_argument("--timeout", type=int, default=15,
                        help="Per-model test timeout seconds (default: 15)")
    parser.add_argument("--restart", action="store_true",
                        help="Restart gateway after update")
    parser.add_argument("--json", dest="json_out", default=None,
                        help="Save report to JSON file")
    parser.add_argument("--use-cache", action="store_true",
                        help="Use cached test results (<1h old) instead of retesting")
    parser.add_argument("--no-update", action="store_true",
                        help="Don't update config files")
    args = parser.parse_args()

    if not args.api_key:
        print("ERROR: --api-key or OPENROUTER_API_KEY env var required")
        sys.exit(1)

    api_key = args.api_key

    # ── Scanning ──
    print("🔍 Scanning OpenRouter for free models...")
    free_models = fetch_all_models(api_key)
    print(f"Found {len(free_models)} free models")

    if not free_models:
        print("No free models found. Exiting.")
        sys.exit(0)

    # ── Filtering ──
    if args.filter != "all":
        free_models = filter_models(free_models, args.filter)
        print(f"After filter '{args.filter}': {len(free_models)} models")

    # ── Score all models ──
    for m in free_models:
        m["base_score"] = score_model(m, 0)

    # ── Scan mode ──
    if args.scan:
        sorted_models = sorted(free_models, key=lambda m: m["base_score"], reverse=True)
        print(f"\n{'#':<3} {'Score':>6} {'Context':>10} {'Capabilities':<35} {'Model ID'}")
        print("=" * 85)
        for i, m in enumerate(sorted_models):
            caps = ",".join(get_capabilities(m))
            print(f"{i+1:<3} {m['base_score']:>6.1f} {str(m.get('context_length','')):>10} {caps:<35} {m['id']}")
        return

    # ── Select models to test ──
    if args.test > 0:
        # Test top N by base_score
        free_models = sorted(free_models, key=lambda m: m["base_score"], reverse=True)
        free_models = free_models[:args.test]
        print(f"\nTesting top {args.test} models by base score...")
    else:
        print(f"\nTesting all {len(free_models)} free models...")

    # ── Cache check ──
    if args.use_cache:
        _ = load_cache()  # Initialize cache
        cached_working = []
        uncached = []
        for m in free_models:
            entry = get_cached_test(m["id"])
            if entry and entry["ok"]:
                m_cached = dict(m)
                m_cached["ok"] = True
                m_cached["latency"] = entry["latency"]
                m_cached["score"] = entry["score"]
                cached_working.append(m_cached)
            elif entry and not entry["ok"]:
                m_cached = dict(m)
                m_cached["ok"] = False
                m_cached["error"] = "cached_fail"
                uncached.append(m_cached)  # Still add to results as failed
            else:
                uncached.append(m)

        if uncached:
            print(f"Cache hit: {len(cached_working)} OK, re-testing {len(uncached)}...")
            test_results = test_models_concurrent(api_key, uncached, args.workers, args.bench, args.timeout)
            # Update cache
            for r in test_results:
                update_cache_entry(r["id"], r["ok"], r.get("latency", 0), r.get("score", 0))
            persist_cache()
            # Merge
            cached_working.extend(test_results)
            for m in uncached:
                found = any(r["id"] == m["id"] for r in test_results)
                if not found:
                    m["score"] = m.get("base_score", 0)
                    cached_working.append(m)
        else:
            cached_working.extend(uncached)
            test_results = cached_working

        working, failing = render_results(cached_working, args.sort)
    else:
        # ── Testing ──
        test_results = test_models_concurrent(api_key, free_models, args.workers, args.bench, args.timeout)
        # Update cache
        for r in test_results:
            update_cache_entry(r["id"], r["ok"], r.get("latency", 0), r.get("score", 0))
        persist_cache()

        working, failing = render_results(test_results, args.sort)

    if not working:
        print("\n❌ No working free models found.")
        sys.exit(1)

    # ── Pick top N ──
    selected = working[:args.keep]
    top_keep = args.keep

    # ── Print summary ──
    print_table(working, failing, args.bench, args.json_out)

    if args.no_update:
        print("\n⏭️  No-update mode. Configs not modified.")
        return

    # ── Update configs ──
    print(f"\n📝 Updating configs with top {top_keep} working models...")
    ok1, ok2 = update_configs(selected, args.config, args.models_json)
    print(f"  openclaw.json : {'✅' if ok1 else '❌'}")
    print(f"  models.json   : {'✅' if ok2 else '❌'}")

    # ── Restart ──
    if args.restart:
        print("\n🔄 Restarting gateway...")
        restart_gateway()

    print(f"\n🎉 Done! Active free models ({len(selected)}):")
    for i, m in enumerate(selected):
        marker = "🏆" if i == 0 else " "
        caps = ",".join(get_capabilities(m)[:3])
        print(f"  {marker} {i+1}. {m['id']} (score={m['score']:.1f}, {caps})")


def render_results(test_results, sort_by):
    """Sort results into working/failing."""
    working = sorted([r for r in test_results if r.get("ok", False)],
                     key=lambda r: r.get("score", 0), reverse=True)
    if sort_by == "latency":
        working = sorted(working, key=lambda r: r.get("latency", 99999))
    elif sort_by == "name":
        working = sorted(working, key=lambda r: r.get("id", ""))

    failing = sorted([r for r in test_results if not r.get("ok", False)],
                     key=lambda r: r.get("score", 0), reverse=True)
    return working, failing


if __name__ == "__main__":
    main()
