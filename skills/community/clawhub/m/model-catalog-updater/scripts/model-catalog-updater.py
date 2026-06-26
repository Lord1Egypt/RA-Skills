#!/usr/bin/env python3
"""
Model Catalog Updater - Fetch and add models from OpenAI-compatible APIs to OpenClaw config
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Config
CONFIG_PATH = Path(r"C:\Users\zebuM\.openclaw\openclaw.json")
BACKUP_NAME = "openclawworking.json"
DEFAULT_CONTEXT = 128000
DEFAULT_MAX_TOKENS = 8192
REASONING_PATTERNS = ["deepseek-r1", "qwq", "o1-", "o3-", "reasoning", "think"]
VISION_PATTERNS = ["vision", "multimodal", "image", "gpt-4-vision", "claude-3"]


def load_config():
    """Load OpenClaw config."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """Save OpenClaw config."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def backup_config():
    """Create backup of config before edits."""
    backup_path = CONFIG_PATH.parent / BACKUP_NAME
    shutil.copy(CONFIG_PATH, backup_path)
    return backup_path


def get_providers(config):
    """Extract provider info from config."""
    providers = config.get("models", {}).get("providers", {})
    result = []
    for name, data in providers.items():
        base_url = data.get("baseUrl", "unknown")
        api_key = data.get("apiKey", "")
        result.append({
            "name": name,
            "baseUrl": base_url,
            "apiKey": api_key,
            "api": data.get("api", "openai-completions")
        })
    return result


def fetch_models(provider):
    """Fetch models from provider's /v1/models endpoint."""
    base_url = provider["baseUrl"].rstrip("/")
    api_key = provider["apiKey"]
    
    # Build auth header based on key type
    if api_key.startswith("env:"):
        import os
        env_var = api_key[4:]
        api_key = os.environ.get(env_var, "")
    
    headers = {"Accept": "application/json"}
    if api_key and api_key not in ["lmstudio", "qwen-oauth", "minimax-oauth"]:
        headers["Authorization"] = f"Bearer {api_key}"
    
    url = f"{base_url}/models"
    
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("data", [])
    except HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def is_reasoning_model(model_id):
    """Detect if model is a reasoning model based on ID patterns."""
    model_lower = model_id.lower()
    return any(pattern in model_lower for pattern in REASONING_PATTERNS)


def is_vision_model(model_id):
    """Detect if model supports vision based on ID patterns."""
    model_lower = model_id.lower()
    return any(pattern in model_lower for pattern in VISION_PATTERNS)


def create_model_entry(model_id, model_data=None):
    """Create a model entry for config."""
    name = model_data.get("name", model_id) if model_data else model_id
    
    entry = {
        "id": model_id,
        "name": name,
        "reasoning": is_reasoning_model(model_id),
        "input": ["text", "image"] if is_vision_model(model_id) else ["text"],
        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        "contextWindow": DEFAULT_CONTEXT,
        "maxTokens": DEFAULT_MAX_TOKENS
    }
    return entry


def get_existing_model_ids(config, provider_name):
    """Get model IDs already in config for a provider."""
    providers = config.get("models", {}).get("providers", {})
    if provider_name not in providers:
        return set()
    return {
        m["id"] for m in providers[provider_name].get("models", [])
    }


def add_models_to_config(config, provider_name, models_to_add):
    """Add selected models to config."""
    # Ensure provider exists in models.providers
    if "models" not in config:
        config["models"] = {"mode": "merge", "providers": {}}
    if "providers" not in config["models"]:
        config["models"]["providers"] = {}
    if provider_name not in config["models"]["providers"]:
        config["models"]["providers"][provider_name] = {
            "models": [],
            "api": "openai-completions"
        }
    
    # Get existing model IDs for this provider
    existing_ids = get_existing_model_ids(config, provider_name)
    
    # Add to models.providers.{provider}.models
    added_to_provider = []
    for model_id in models_to_add:
        if model_id not in existing_ids:
            entry = create_model_entry(model_id)
            config["models"]["providers"][provider_name]["models"].append(entry)
            added_to_provider.append(model_id)
    
    # Ensure agents.defaults.models exists
    if "agents" not in config:
        config["agents"] = {"defaults": {}}
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "models" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["models"] = {}
    
    # Add to agents.defaults.models
    added_to_agents = []
    for model_id in models_to_add:
        full_id = f"{provider_name}/{model_id}"
        if full_id not in config["agents"]["defaults"]["models"]:
            config["agents"]["defaults"]["models"][full_id] = {}
            added_to_agents.append(full_id)
    
    return added_to_provider, added_to_agents


def main():
    """Interactive model catalog."""
    parser = argparse.ArgumentParser(description="Model Catalog Updater")
    parser.add_argument("--provider", "-p", help="Provider name (from slash command)")
    parser.add_argument("--list-providers", action="store_true", help="List available providers")
    args = parser.parse_args()
    
    print("📊 Model Catalog Updater\n")
    
    # Load config
    config = load_config()
    
    # Get providers
    providers = get_providers(config)
    
    if not providers:
        print("❌ No providers configured in openclaw.json")
        sys.exit(1)
    
    # Build provider lookup
    provider_map = {p["name"]: p for p in providers}
    
    # Handle --list-providers
    if args.list_providers:
        print("Available providers:")
        for name in provider_map:
            print(f"  - {name}")
        sys.exit(0)
    
    # Handle --provider from slash command
    if args.provider:
        if args.provider not in provider_map:
            print(f"❌ Unknown provider: {args.provider}")
            print(f"   Available: {', '.join(provider_map.keys())}")
            sys.exit(1)
        provider = provider_map[args.provider]
        provider_name = args.provider
    else:
        # Interactive mode - show providers
        print("Your configured providers:")
        for i, p in enumerate(providers, 1):
            print(f"  {i}. {p['name']} ({p['baseUrl']})")
        
        # Select provider
        try:
            choice = input("\nSelect provider [1-{}]: ".format(len(providers)))
            idx = int(choice) - 1
            if idx < 0 or idx >= len(providers):
                print("❌ Invalid selection")
                sys.exit(1)
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Cancelled")
            sys.exit(1)
        
        provider = providers[idx]
        provider_name = provider["name"]
    
    print(f"\nFetching models from {provider_name}...")
    
    # Fetch models
    models = fetch_models(provider)
    
    if isinstance(models, dict) and "error" in models:
        print(f"❌ {models['error']}")
        sys.exit(1)
    
    if not models:
        print("❌ No models returned from API")
        sys.exit(1)
    
    # Get existing models for this provider
    existing_ids = get_existing_model_ids(config, provider_name)
    
    # Filter to only new models
    all_model_ids = [m.get("id", "unknown") for m in models]
    new_model_ids = [mid for mid in all_model_ids if mid not in existing_ids]
    skipped_count = len(all_model_ids) - len(new_model_ids)
    
    if not new_model_ids:
        print(f"\n✅ All {len(all_model_ids)} models already in config")
        sys.exit(0)
    
    # Show only new models
    print(f"\nNew models available ({len(new_model_ids)} new, {skipped_count} already in config):")
    for i, model_id in enumerate(new_model_ids, 1):
        print(f"  {i}. {model_id}")
    
    # Select models
    try:
        selection = input("\nSelect models to add (comma-separated, or 'all'): ").strip()
        if selection.lower() == "all":
            selected_indices = list(range(len(new_model_ids)))
        else:
            selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
            selected_indices = [i for i in selected_indices if 0 <= i < len(new_model_ids)]
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Cancelled")
        sys.exit(1)
    
    if not selected_indices:
        print("❌ No valid selection")
        sys.exit(1)
    
    models_to_add = [new_model_ids[i] for i in selected_indices]
    
    # Backup
    backup_path = backup_config()
    print(f"\n✅ Backup created: {backup_path}")
    
    # Add to config
    added_provider, added_agents = add_models_to_config(config, provider_name, models_to_add)
    
    # Save
    save_config(config)
    
    print(f"✅ Added to models.providers.{provider_name}.models:")
    for m in added_provider:
        print(f"   - {m}")
    
    print(f"✅ Added to agents.defaults.models:")
    for m in added_agents:
        print(f"   - {m}")
    
    print("\n🔄 Restart OpenClaw to apply changes")


if __name__ == "__main__":
    main()
