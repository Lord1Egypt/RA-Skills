#!/usr/bin/env python3
"""
Fetch all OpenRouter models and output structured JSON for the picker UI.
Usage: python3 fetch_models.py [--config ~/.openclaw/openclaw.json]

KEY DESIGN: All model IDs are normalized — the "openrouter/" prefix is stripped
so that virtual models (auto, free) and API models (owl-alpha, etc.) share the
same ID namespace. The prefix is re-added only when writing back to config.
"""
import json
import sys
import urllib.request
import argparse
import subprocess

# Virtual models that exist in OpenClaw config but NOT in the OpenRouter API.
# Their IDs are already bare (no openrouter/ prefix).
VIRTUAL_MODELS = [
    {"id": "auto",  "name": "OpenRouter: Auto (智能路由)", "caps": [], "context": 0, "pricing": {"prompt":"0","completion":"0"}, "_virtual": True},
    {"id": "free",  "name": "OpenRouter: Free (免费轮询)", "caps": ["free"], "context": 0, "pricing": {"prompt":"0","completion":"0"}, "_virtual": True},
]

def fetch_openrouter_models():
    url = "https://openrouter.ai/api/v1/models"
    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-model-picker/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["data"]

def parse_capabilities(model):
    caps = []
    arch = model.get("architecture", {})
    modality = arch.get("modality", "")
    if "image" in modality or "vision" in modality.lower():
        caps.append("vision")
    id_lower = model.get("id", "").lower()
    name_lower = model.get("name", "").lower()
    if any(k in id_lower or k in name_lower for k in ["thinking","reasoning","r1","o1","o3","o4","r2","qwq","r7"]):
        caps.append("reasoning")
    if id_lower.endswith(":free"):
        caps.append("free")
    if "online" in id_lower or ":online" in id_lower:
        caps.append("online")
    if "embed" in id_lower or "embedding" in id_lower:
        caps.append("embedding")
    return caps

def normalize_id(mid):
    """Strip 'openrouter/' prefix for consistent ID matching."""
    if not mid:
        return mid
    if mid.startswith('openrouter/'):
        return mid[11:]  # len('openrouter/') == 11
    return mid

def load_current_config():
    """Use openclaw config get to read current model settings."""
    try:
        r = subprocess.run(
            ["openclaw", "config", "get", "agents.defaults"],
            capture_output=True, text=True, timeout=10
        )
        data = json.loads(r.stdout)
        primary = data.get("model", {}).get("primary", "openrouter/auto")
        fallbacks = data.get("model", {}).get("fallbacks", [])
        models_dict = data.get("models", {})
        enabled = list(models_dict.keys())
        aliases = {k: v.get("alias","") for k,v in models_dict.items() if v.get("alias")}
        return {"primary": primary, "fallbacks": fallbacks, "enabled": enabled, "aliases": aliases}
    except Exception as e:
        return {"primary": "openrouter/auto", "fallbacks": [], "enabled": [], "aliases": {}, "error": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="~/.openclaw/openclaw.json")
    args = parser.parse_args()

    try:
        raw_models = fetch_openrouter_models()
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch models: {e}"}))
        sys.exit(1)

    current = load_current_config()

    # Group by provider.
    # Extract provider from RAW id (before normalization) so openrouter/* stays in openrouter group.
    groups = {}
    seen_bare_ids = set()

    for m in raw_models:
        raw_id = m.get("id", "")
        bare_id = normalize_id(raw_id)
        seen_bare_ids.add(bare_id)

        # Provider comes from raw_id, not bare_id
        if raw_id.startswith("openrouter/"):
            provider = "openrouter"
        else:
            parts = raw_id.split("/")
            provider = parts[0] if len(parts) > 1 else "other"

        if provider not in groups:
            groups[provider] = []

        groups[provider].append({
            "id": bare_id,
            "name": m.get("name", raw_id),
            "caps": parse_capabilities(m),
            "context": m.get("context_length", 0),
            "pricing": {
                "prompt": m.get("pricing", {}).get("prompt", "0"),
                "completion": m.get("pricing", {}).get("completion", "0"),
            }
        })

    # Inject virtual models (auto/free) if not already in API results
    virt_added = []
    for vm in VIRTUAL_MODELS:
        if vm["id"] not in seen_bare_ids:
            virt_added.append({
                "id": vm["id"],
                "name": vm["name"],
                "caps": vm["caps"],
                "context": 0,
                "pricing": {"prompt": "0", "completion": "0"},
            })
            seen_bare_ids.add(vm["id"])

    if virt_added:
        if "openrouter" not in groups:
            groups["openrouter"] = []
        groups["openrouter"] = virt_added + groups.get("openrouter", [])

    # Sort: openrouter first, then by model count desc
    def sort_key(item):
        if item[0] == "openrouter":
            return -9999
        return -len(item[1])

    sorted_groups = sorted(groups.items(), key=sort_key)

    # Normalize current config IDs
    normalized_enabled = [normalize_id(e) for e in current["enabled"]]
    normalized_primary = normalize_id(current["primary"])
    normalized_fallbacks = [normalize_id(f) for f in current["fallbacks"]]
    normalized_aliases = {normalize_id(k): v for k, v in current.get("aliases", {}).items() if v}

    output = {
        "groups": [{"provider": k, "models": v} for k, v in sorted_groups],
        "total": len(raw_models),
        "current": {
            "primary": normalized_primary,
            "fallbacks": normalized_fallbacks,
            "enabled": normalized_enabled,
            "aliases": normalized_aliases,
        }
    }
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()