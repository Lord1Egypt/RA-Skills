#!/usr/bin/env python3
"""
ModelSense — Auto-update model pricing data from OpenRouter API.
Preserves manual fields (benchmark_strengths, best_for, etc.)
Only updates: cost_input_per_m, cost_output_per_m, context_window.
"""

import os
import sys
import json
import yaml
import requests
from datetime import date

OPENROUTER_API = "https://openrouter.ai/api/v1/models"
MODELS_FILE = "data/models.yaml"

# Map OpenRouter model IDs to our model IDs
OPENROUTER_ID_MAP = {
    "anthropic/claude-opus-4":        "anthropic/claude-opus-4-6",
    "anthropic/claude-sonnet-4":      "anthropic/claude-sonnet-4-6",
    "anthropic/claude-haiku-4-5":     "anthropic/claude-haiku-4-5",
    "openai/o3":                      "openai/o3",
    "openai/gpt-5.2":                 "openai/gpt-5.2",
    "openai/gpt-4o":                  "openai/gpt-4o",
    "google/gemini-pro-1.5":          "google/gemini-3.1-pro",
    "google/gemini-flash-1.5":        "google/gemini-2.5-flash",
    "deepseek/deepseek-chat":         "deepseek/deepseek-chat",
    "x-ai/grok-beta":                 "xai/grok-4",
}

def fetch_openrouter_models():
    headers = {}
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    resp = requests.get(OPENROUTER_API, headers=headers, timeout=30)
    resp.raise_for_status()
    return {m["id"]: m for m in resp.json().get("data", [])}

def update_models(or_models, local_models):
    updated = 0
    for model in local_models:
        model_id = model.get("id", "")
        # Try direct match first, then via map
        or_id = next(
            (k for k, v in OPENROUTER_ID_MAP.items() if v == model_id),
            None
        )
        if not or_id:
            continue
        
        or_data = or_models.get(or_id)
        if not or_data:
            continue
        
        pricing = or_data.get("pricing", {})
        # OpenRouter pricing is per-token; convert to per-million
        if "prompt" in pricing:
            model["cost_input_per_m"] = round(float(pricing["prompt"]) * 1_000_000, 4)
        if "completion" in pricing:
            model["cost_output_per_m"] = round(float(pricing["completion"]) * 1_000_000, 4)
        if "context_length" in or_data:
            model["context_window"] = or_data["context_length"]
        
        updated += 1
        print(f"  Updated: {model_id}")
    
    return updated

def main():
    print("🔍 Fetching OpenRouter model data...")
    try:
        or_models = fetch_openrouter_models()
        print(f"  Found {len(or_models)} models on OpenRouter")
    except Exception as e:
        print(f"⚠️  Failed to fetch OpenRouter data: {e}")
        sys.exit(0)  # Don't fail the CI run

    print("📂 Loading local models.yaml...")
    with open(MODELS_FILE, "r") as f:
        data = yaml.safe_load(f)
    
    models = data.get("models", [])
    print(f"  Found {len(models)} local models")

    print("🔄 Updating pricing data...")
    updated = update_models(or_models, models)

    # Update the last-updated timestamp
    data["_meta"] = {
        "last_auto_update": str(date.today()),
        "source": "openrouter.ai/api/v1/models",
        "models_updated": updated,
    }

    with open(MODELS_FILE, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✅ Done. Updated {updated} models → {MODELS_FILE}")

if __name__ == "__main__":
    main()
