#!/usr/bin/env python3
"""
ModelPool — Free AI Model Manager for OpenClaw
Auto-discover, configure, and maintain free AI models with multi-key rotation.
"""

import json
import os
import sys
import subprocess
import urllib.request
import ssl
import time
import argparse

VERSION = "1.0.1"
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
CACHE_PATH = os.path.expanduser("~/.openclaw/modelpool_cache.json")
KEYS_PATH = os.path.expanduser("~/.openclaw/modelpool_keys.json")
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

# Model quality scoring weights
QUALITY_WEIGHTS = {
    "reasoning": 30,       # Reasoning capability bonus
    "context_large": 20,   # >128k context
    "context_medium": 10,  # >64k context
    "known_good": 25,      # Known high-quality models
}

# Known high-quality free models (manually curated)
KNOWN_GOOD_MODELS = [
    "stepfun/step-3.5-flash",
    "qwen/qwen3-coder",
    "nvidia/nemotron",
    "nousresearch/hermes-3-llama-3.1-405b",
    "openai/gpt-oss",
    "google/gemma",
    "deepseek/deepseek",
    "meta-llama/llama-3",
]

SSL_CTX = ssl.create_default_context()


def ensure_config_exists():
    """Ensure OpenClaw config directory and file exist."""
    config_dir = os.path.dirname(CONFIG_PATH)
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    if not os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({"models": {"providers": {}}, "agents": {"defaults": {}}}, f, indent=2)


def load_config():
    ensure_config_exists()
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ⚠️  Config load warning: {e}", file=sys.stderr)
        return {"models": {"providers": {}}, "agents": {"defaults": {}}}


def save_config(config):
    ensure_config_exists()
    # Backup before writing
    backup_path = CONFIG_PATH + ".bak"
    if os.path.isfile(CONFIG_PATH):
        import shutil
        shutil.copy2(CONFIG_PATH, backup_path)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def load_keys():
    try:
        with open(KEYS_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, FileNotFoundError):
        return {"keys": []}


def save_keys(keys_data):
    with open(KEYS_PATH, "w") as f:
        json.dump(keys_data, f, indent=2)


def validate_key(api_key):
    """Validate an OpenRouter API key by making a test request."""
    if not api_key or not api_key.startswith("sk-or-") or len(api_key) < 20:
        return False, "Key should start with 'sk-or-'"
    req = urllib.request.Request(
        OPENROUTER_MODELS_URL,
        headers={"Authorization": f"Bearer {api_key}"}
    )
    try:
        resp = urllib.request.urlopen(req, context=SSL_CTX, timeout=15)
        data = json.loads(resp.read())
        if "data" in data:
            return True, f"{len(data['data'])} models accessible"
        return False, "Unexpected response"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Invalid key (401 Unauthorized)"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)[:60]


def fetch_free_models(api_key):
    """Fetch all free models from OpenRouter API."""
    req = urllib.request.Request(
        OPENROUTER_MODELS_URL,
        headers={"Authorization": f"Bearer {api_key}"}
    )
    try:
        resp = urllib.request.urlopen(req, context=SSL_CTX, timeout=30)
        data = json.loads(resp.read())
    except Exception as e:
        print(f"  ❌ Failed to fetch models: {e}")
        return []

    free_models = []
    for m in data.get("data", []):
        pricing = m.get("pricing", {})
        prompt_price = float(pricing.get("prompt") or 0)
        completion_price = float(pricing.get("completion") or 0)
        if prompt_price == 0 and completion_price == 0:
            free_models.append({
                "id": m.get("id", ""),
                "name": m.get("name", ""),
                "context_length": m.get("context_length", 0),
                "description": m.get("description", "")[:100],
                "architecture": m.get("architecture", {}),
            })
    return free_models


def score_model(model):
    """Score a model by quality. Returns 0-100."""
    score = 0
    mid = model.get("id", "").lower()
    ctx = model.get("context_length", 0) or 0

    # Context window bonus
    if ctx >= 128000:
        score += QUALITY_WEIGHTS["context_large"]
    elif ctx >= 64000:
        score += QUALITY_WEIGHTS["context_medium"]

    # Reasoning bonus (check if model name suggests reasoning)
    reasoning_keywords = ["think", "reason", "flash", "coder", "step"]
    if any(kw in mid for kw in reasoning_keywords):
        score += QUALITY_WEIGHTS["reasoning"]

    # Known good model bonus
    for known in KNOWN_GOOD_MODELS:
        if known in mid:
            score += QUALITY_WEIGHTS["known_good"]
            break

    # Penalize very small models
    if "mini" in mid or "tiny" in mid or "small" in mid:
        score -= 15

    return score


def discover_and_rank(api_key):
    """Discover free models and rank by quality."""
    print("  🔍 Fetching free models from OpenRouter...")
    models = fetch_free_models(api_key)
    if not models:
        return []

    # Score and sort
    for m in models:
        m["score"] = score_model(m)
    models.sort(key=lambda x: -x["score"])

    # Cache results
    cache = {"timestamp": time.time(), "models": models}
    try:
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f, indent=2)
    except:
        pass

    return models


def build_provider_config(key, models, provider_name):
    """Build OpenClaw provider config for a set of models."""
    model_configs = []
    for m in models:
        mc = {
            "id": m["id"],
            "name": m.get("name", m["id"]),
            "reasoning": any(kw in m["id"].lower() for kw in ["think", "reason", "flash", "coder", "step"]),
            "input": ["text"],
            "contextWindow": m.get("context_length", 128000),
            "maxTokens": 32768,
        }
        model_configs.append(mc)

    return {
        "baseUrl": "https://openrouter.ai/api/v1",
        "apiKey": key,
        "api": "openai-completions",
        "authHeader": True,
        "models": model_configs,
    }


def distribute_models(models, num_keys, top_n=6):
    """Distribute top models across keys in interleaved fashion."""
    top = models[:min(top_n * num_keys, len(models))]
    groups = [[] for _ in range(num_keys)]
    for i, m in enumerate(top):
        groups[i % num_keys].append(m)
    return groups


def build_fallback_chain(keys, model_groups):
    """Build interleaved fallback chain across keys."""
    chain = []
    max_len = max(len(g) for g in model_groups)
    for i in range(max_len):
        for k_idx, group in enumerate(model_groups):
            if i < len(group):
                provider = f"openrouter" if k_idx == 0 else f"openrouter{k_idx + 1}"
                model_id = group[i]["id"]
                chain.append(f"{provider}/{model_id}")
    return chain


# ============================================================
# Commands
# ============================================================

def cmd_setup(args):
    """Interactive setup."""
    print("")
    print("🦞 ModelPool Setup")
    print("=" * 40)
    print("")

    keys_data = load_keys()
    existing_keys = keys_data.get("keys", [])

    if existing_keys:
        print(f"  Found {len(existing_keys)} existing key(s)")
        add_more = input("  Add more keys? (y/N): ").strip().lower()
        if add_more != "y":
            keys = existing_keys
        else:
            new_key = input("  New OpenRouter Key: ").strip()
            if new_key:
                existing_keys.append(new_key)
            keys = existing_keys
    else:
        print("  Enter your OpenRouter API Key(s)")
        print("  (Get one free at https://openrouter.ai)")
        print("")
        keys = []
        for i in range(1, 11):
            prompt = f"  Key {i}" + (" (required)" if i == 1 else " (optional, Enter to skip)") + ": "
            key = input(prompt).strip()
            if not key:
                break
            keys.append(key)

    if not keys:
        print("  ❌ At least one key is required")
        sys.exit(1)

    # Validate keys
    print("\n  🔑 Validating keys...")
    valid_keys = []
    for i, key in enumerate(keys, 1):
        ok, msg = validate_key(key)
        if ok:
            print(f"    Key {i}: ✅ {msg}")
            valid_keys.append(key)
        else:
            print(f"    Key {i}: ❌ {msg} (skipped)")

    if not valid_keys:
        print("\n  ❌ No valid keys. Check your keys and try again.")
        sys.exit(1)

    keys = valid_keys

    # Save keys
    keys_data["keys"] = keys
    save_keys(keys_data)
    print(f"\n  ✅ {len(keys)} valid key(s) saved")

    # Discover models
    print("")
    models = discover_and_rank(keys[0])
    if not models:
        print("  ❌ No free models found")
        sys.exit(1)
    print(f"  ✅ Found {len(models)} free models")

    # Distribute across keys
    top_per_key = 3
    model_groups = distribute_models(models, len(keys), top_per_key)

    # Configure providers
    print("\n  ⚙️  Configuring providers...")
    config = load_config()
    config.setdefault("models", {}).setdefault("providers", {})

    for i, (key, group) in enumerate(zip(keys, model_groups)):
        provider_name = "openrouter" if i == 0 else f"openrouter{i + 1}"
        config["models"]["providers"][provider_name] = build_provider_config(key, group, provider_name)
        model_names = [m["id"].split("/")[-1] for m in group]
        print(f"    ✅ {provider_name}: {', '.join(model_names)}")

    # Build fallback chain
    print("\n  🔗 Building fallback chain...")
    chain = build_fallback_chain(keys, model_groups)
    primary = chain[0] if chain else "openrouter/stepfun/step-3.5-flash:free"
    fallbacks = chain[1:] if len(chain) > 1 else []

    config.setdefault("agents", {}).setdefault("defaults", {})["model"] = {
        "primary": primary,
        "fallbacks": fallbacks,
    }

    save_config(config)
    print(f"    Primary: {primary}")
    print(f"    Fallbacks: {len(fallbacks)}")

    # Validate and restart
    print("\n  🔍 Validating...")
    subprocess.run(["openclaw", "config", "validate"], capture_output=True)

    print("  🔄 Restarting OpenClaw...")
    subprocess.run(["openclaw", "daemon", "restart"], capture_output=True)
    time.sleep(15)

    print("")
    print("=" * 40)
    print(f"🎉 Done! {len(models)} free models, {len(keys)} keys, {len(keys)}x quota")
    print("=" * 40)
    print("")


def cmd_auto(args):
    """Non-interactive auto-configure using existing keys."""
    keys_data = load_keys()
    keys = keys_data.get("keys", [])
    if not keys:
        # Try to extract from existing config
        config = load_config()
        providers = config.get("models", {}).get("providers", {})
        for name, info in providers.items():
            if "openrouter" in name.lower():
                key = info.get("apiKey", "")
                if key and key not in keys:
                    keys.append(key)
    if not keys:
        print("  ❌ No keys found. Run 'freeswitch setup' first.")
        sys.exit(1)

    print(f"\n  🔄 Auto-configuring with {len(keys)} key(s)...")
    models = discover_and_rank(keys[0])
    if not models:
        print("  ❌ No free models found")
        sys.exit(1)

    model_groups = distribute_models(models, len(keys), 3)
    config = load_config()
    config.setdefault("models", {}).setdefault("providers", {})

    for i, (key, group) in enumerate(zip(keys, model_groups)):
        provider_name = "openrouter" if i == 0 else f"openrouter{i + 1}"
        config["models"]["providers"][provider_name] = build_provider_config(key, group, provider_name)

    chain = build_fallback_chain(keys, model_groups)
    config.setdefault("agents", {}).setdefault("defaults", {})["model"] = {
        "primary": chain[0],
        "fallbacks": chain[1:],
    }
    save_config(config)

    subprocess.run(["openclaw", "daemon", "restart"], capture_output=True)
    time.sleep(10)
    print(f"  ✅ Configured {len(models)} models, {len(keys)} keys")
    print(f"  Primary: {chain[0]}")
    print("")


def cmd_list(args):
    """List available free models."""
    keys_data = load_keys()
    keys = keys_data.get("keys", [])
    if not keys:
        config = load_config()
        for name, info in config.get("models", {}).get("providers", {}).items():
            if "openrouter" in name.lower():
                key = info.get("apiKey", "")
                if key:
                    keys.append(key)
                    break
    if not keys:
        print("  ❌ No keys found")
        return

    models = discover_and_rank(keys[0])
    print(f"\n  📋 {len(models)} free models available:\n")
    print(f"  {'Rank':<5} {'Score':<6} {'Model ID':<55} {'Context':<10}")
    print(f"  {'─'*5} {'─'*6} {'─'*55} {'─'*10}")
    for i, m in enumerate(models[:30], 1):
        ctx = f"{m['context_length']//1000}k" if m['context_length'] else "?"
        print(f"  {i:<5} {m['score']:<6} {m['id']:<55} {ctx:<10}")
    if len(models) > 30:
        print(f"\n  ... and {len(models) - 30} more")
    print("")


def cmd_switch(args):
    """Switch primary model."""
    model = args.model
    config = load_config()
    model_config = config.get("agents", {}).get("defaults", {}).get("model", {})
    if isinstance(model_config, str):
        model_config = {"primary": model_config, "fallbacks": []}

    old = model_config.get("primary", "none")
    model_config["primary"] = model
    config["agents"]["defaults"]["model"] = model_config
    save_config(config)

    subprocess.run(["openclaw", "daemon", "restart"], capture_output=True)
    print(f"  ✅ Switched: {old} → {model}")


def cmd_status(args):
    """Show current status."""
    config = load_config()
    keys_data = load_keys()
    keys = keys_data.get("keys", [])

    model_config = config.get("agents", {}).get("defaults", {}).get("model", {})
    if isinstance(model_config, str):
        primary = model_config
        fallbacks = []
    else:
        primary = model_config.get("primary", "none")
        fallbacks = model_config.get("fallbacks", [])

    providers = config.get("models", {}).get("providers", {})
    or_providers = {k: v for k, v in providers.items() if "openrouter" in k.lower()}

    print(f"\n  🦞 ModelPool Status")
    print(f"  {'─' * 40}")
    print(f"  Keys:      {len(keys)}")
    print(f"  Providers: {len(or_providers)}")
    print(f"  Primary:   {primary}")
    print(f"  Fallbacks: {len(fallbacks)}")
    print(f"  {'─' * 40}")

    if fallbacks:
        print(f"\n  Fallback chain:")
        for i, fb in enumerate(fallbacks, 1):
            print(f"    {i}. {fb}")

    # Test gateway
    result = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
    gw_ok = "18789" in result.stdout
    print(f"\n  Gateway: {'✅ running' if gw_ok else '❌ down'}")
    print("")


def cmd_repair(args):
    """Run repair script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repair_script = os.path.join(script_dir, "repair.py")
    if os.path.exists(repair_script):
        subprocess.run([sys.executable, repair_script])
    else:
        print(f"  ❌ repair.py not found at {script_dir}")
        print("  Try running from the freeswitch/scripts directory")


def cmd_keys_add(args):
    """Add a new key."""
    key = args.key
    keys_data = load_keys()
    if key in keys_data.get("keys", []):
        print("  ⚠️  Key already exists")
        return
    keys_data.setdefault("keys", []).append(key)
    save_keys(keys_data)
    print(f"  ✅ Key added. Total: {len(keys_data['keys'])}")
    print("  Run 'freeswitch auto' to reconfigure with new key")


def cmd_keys_list(args):
    """List all keys."""
    keys_data = load_keys()
    keys = keys_data.get("keys", [])
    print(f"\n  🔑 {len(keys)} key(s):\n")
    for i, k in enumerate(keys, 1):
        masked = k[:12] + "..." + k[-4:]
        print(f"    {i}. {masked}")
    print("")


def cmd_refresh(args):
    """Force refresh model cache."""
    keys_data = load_keys()
    keys = keys_data.get("keys", [])
    if not keys:
        print("  ❌ No keys found")
        return
    models = discover_and_rank(keys[0])
    print(f"  ✅ Cache refreshed: {len(models)} free models")


def main():
    parser = argparse.ArgumentParser(
        prog="modelpool",
        description="ModelPool — Free AI Model Manager for OpenClaw"
    )
    parser.add_argument("--version", action="version", version=f"ModelPool {VERSION}")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("setup", help="Interactive setup")
    sub.add_parser("auto", help="Auto-configure with existing keys")
    sub.add_parser("list", help="List free models")
    sp_switch = sub.add_parser("switch", help="Switch primary model")
    sp_switch.add_argument("model", help="Model ID (e.g. openrouter/stepfun/step-3.5-flash:free)")
    sub.add_parser("status", help="Show current status")
    sub.add_parser("repair", help="Diagnose and fix issues")
    sub.add_parser("refresh", help="Refresh model cache")

    sp_keys = sub.add_parser("keys", help="Manage API keys")
    keys_sub = sp_keys.add_subparsers(dest="keys_command")
    sp_keys_add = keys_sub.add_parser("add", help="Add a key")
    sp_keys_add.add_argument("key", help="OpenRouter API key")
    keys_sub.add_parser("list", help="List keys")

    args = parser.parse_args()

    commands = {
        "setup": cmd_setup,
        "auto": cmd_auto,
        "list": cmd_list,
        "switch": cmd_switch,
        "status": cmd_status,
        "repair": cmd_repair,
        "refresh": cmd_refresh,
    }

    if args.command == "keys":
        if args.keys_command == "add":
            cmd_keys_add(args)
        elif args.keys_command == "list":
            cmd_keys_list(args)
        else:
            sp_keys.print_help()
    elif args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
