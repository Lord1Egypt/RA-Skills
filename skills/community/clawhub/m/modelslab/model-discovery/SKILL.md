---
name: modelslab-model-discovery
description: Search and discover 50,000+ AI models on ModelsLab, check usage analytics, and monitor generation history via the Agent Control Plane API.
---

# ModelsLab Model Discovery & Usage

Search 50,000+ AI models, check usage analytics, and monitor generation history via the Agent Control Plane API.

## When to Use This Skill

- Search for models by name, feature, provider, or tags
- Find the best model for a specific task (image, video, audio, LLM)
- Get model details (capabilities, parameters, pricing)
- Check API usage summary and credit consumption
- View generation history with date filters
- Browse available model filters, tags, and providers

## Authentication

All endpoints require a bearer token.

```
Base URL: https://modelslab.com/api/agents/v1
Authorization: Bearer <agent_access_token>
```

Get a token via the `modelslab-account-management` skill or `POST /auth/login`.

## Helper

```python
import requests

BASE = "https://modelslab.com/api/agents/v1"

def headers(token):
    return {"Authorization": f"Bearer {token}"}
```

## Model Search

### Search Models

```python
def search_models(token, search=None, feature=None, provider=None,
                  model_type=None, base_model=None, tags=None,
                  sort="recommended", per_page=20):
    """Search the ModelsLab model library.

    Args:
        search: Free text search query
        feature: Filter by feature — "imagen", "video_fusion", "audio_gen",
                 "llmaster", "threed", "interior", "deepfake"
        provider: Filter by provider name
        model_type: Filter by model type
        base_model: Filter by base model (e.g., "SDXL", "Flux")
        tags: Comma-separated tags
        sort: "recommended" (default), "newest", "popular"
        per_page: Results per page (default 20)
    """
    params = {"sort": sort, "per_page": per_page}
    if search: params["search"] = search
    if feature: params["feature"] = feature
    if provider: params["provider"] = provider
    if model_type: params["model_type"] = model_type
    if base_model: params["base_model"] = base_model
    if tags: params["tags"] = tags

    resp = requests.get(
        f"{BASE}/models",
        headers=headers(token),
        params=params
    )
    return resp.json()["data"]

# Search for Flux image models
models = search_models(token, search="flux", feature="imagen", sort="popular")
for m in models:
    print(f"{m['model_id']}: {m['name']}")
```

### Search by Feature

```python
# Image generation models
image_models = search_models(token, feature="imagen", per_page=10)

# Video generation models
video_models = search_models(token, feature="video_fusion", per_page=10)

# Audio generation models
audio_models = search_models(token, feature="audio_gen", per_page=10)

# LLM / Chat models
llm_models = search_models(token, feature="llmaster", per_page=10)

# 3D generation models
threed_models = search_models(token, feature="threed", per_page=10)

# Interior design models
interior_models = search_models(token, feature="interior", per_page=10)
```

### Get Model Details

```python
def get_model_detail(token, model_id):
    """Get full details for a specific model.

    Returns: capabilities, endpoint configurations with agent-friendly
    `parameters` JSON Schema (types, constraints, defaults), pricing, etc.
    """
    resp = requests.get(
        f"{BASE}/models/{model_id}",
        headers=headers(token)
    )
    return resp.json()["data"]

# Usage
model = get_model_detail(token, "flux-dev")
print(f"Name: {model['name']}")
print(f"Type: {model.get('model_type')}")
print(f"Provider: {model.get('provider')}")

# Access agent-friendly parameters for each endpoint
for ep in model.get("endpoint_configurations", []):
    params = ep.get("parameters")
    if params:
        print(f"\nEndpoint: {ep['name']}")
        for name, schema in params["properties"].items():
            print(f"  {name}: {schema['type']}", end="")
            if "enum" in schema:
                print(f" (options: {schema['enum']})", end="")
            if "default" in schema:
                print(f" [default: {schema['default']}]", end="")
            print()
```

### Browse Filters, Tags, Providers

```python
def get_model_filters(token):
    """Get all available filter options (features, types, categories)."""
    resp = requests.get(f"{BASE}/models/filters", headers=headers(token))
    return resp.json()["data"]

def get_model_tags(token):
    """Get all available model tags."""
    resp = requests.get(f"{BASE}/models/tags", headers=headers(token))
    return resp.json()["data"]

def get_model_providers(token):
    """Get all model providers."""
    resp = requests.get(f"{BASE}/models/providers", headers=headers(token))
    return resp.json()["data"]

# Usage
filters = get_model_filters(token)
tags = get_model_tags(token)
providers = get_model_providers(token)
print(f"Available features: {[f['name'] for f in filters.get('features', [])]}")
print(f"Top tags: {tags[:10]}")
print(f"Providers: {[p['name'] for p in providers]}")
```

## Usage Analytics

### Usage Summary

```python
def get_usage_summary(token):
    """Get overall API usage summary — total calls, credits used, etc."""
    resp = requests.get(f"{BASE}/usage/summary", headers=headers(token))
    return resp.json()["data"]

# Usage
summary = get_usage_summary(token)
print(f"Total API calls: {summary.get('total_calls', 0)}")
print(f"Credits used: {summary.get('credits_used', 0)}")
```

### Usage by Product

```python
def get_usage_by_product(token):
    """Get usage breakdown by product (image, video, audio, etc.)."""
    resp = requests.get(f"{BASE}/usage/products", headers=headers(token))
    return resp.json()["data"]

# Usage
products = get_usage_by_product(token)
for product in products:
    print(f"{product['name']}: {product.get('calls', 0)} calls")
```

### Generation History

```python
def get_usage_history(token, from_date=None, to_date=None, limit=100):
    """Get detailed generation history with optional date filters.

    Args:
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        limit: Max items (1-200, default 100)
    """
    params = {"limit": limit}
    if from_date: params["from"] = from_date
    if to_date: params["to"] = to_date

    resp = requests.get(
        f"{BASE}/usage/history",
        headers=headers(token),
        params=params
    )
    return resp.json()["data"]

# Get last 7 days of history
history = get_usage_history(token, from_date="2025-01-01", to_date="2025-01-07")
for item in history:
    print(f"{item['created_at']}: {item.get('endpoint')} - {item.get('status')}")
```

## Common Workflows

### Find Best Model for a Task

```python
def find_best_model(token, task_description, feature):
    """Search for the best model for a given task."""
    models = search_models(
        token,
        search=task_description,
        feature=feature,
        sort="recommended",
        per_page=5
    )

    if not models:
        print("No models found. Try broader search terms.")
        return None

    best = models[0]
    print(f"Recommended: {best['model_id']} — {best['name']}")
    return best["model_id"]

# Find best model for realistic portraits
model_id = find_best_model(token, "realistic portrait photography", "imagen")

# Find best video model
model_id = find_best_model(token, "text to video cinematic", "video_fusion")
```

### Monitor Usage and Alerts

```python
def check_usage_health(token, max_daily_spend=100):
    """Monitor usage and alert if spending too fast."""
    from datetime import date

    today = date.today().isoformat()
    history = get_usage_history(token, from_date=today, to_date=today)

    daily_cost = sum(item.get("cost", 0) for item in history)
    daily_calls = len(history)

    print(f"Today: {daily_calls} API calls, ${daily_cost:.2f} spent")

    if daily_cost > max_daily_spend:
        print(f"WARNING: Daily spend ${daily_cost:.2f} exceeds ${max_daily_spend}")
        return False
    return True
```

### Complete Model Selection Pipeline

```python
def select_model_for_generation(token, prompt, media_type="image"):
    """Full pipeline: search models, check usage, select best model."""

    # Map media type to feature
    feature_map = {
        "image": "imagen",
        "video": "video_fusion",
        "audio": "audio_gen",
        "3d": "threed",
        "chat": "llmaster"
    }
    feature = feature_map.get(media_type, "imagen")

    # Search models
    models = search_models(token, search=prompt, feature=feature, per_page=5)

    if not models:
        # Fallback: search without prompt
        models = search_models(token, feature=feature, sort="popular", per_page=5)

    # Check usage
    summary = get_usage_summary(token)
    print(f"Credits remaining: {summary.get('credits_remaining', 'N/A')}")

    # Return top model
    if models:
        model = models[0]
        print(f"Selected: {model['model_id']} ({model['name']})")
        return model["model_id"]
    return None

# Usage
model_id = select_model_for_generation(token, "anime character", "image")
```

## MCP Server Access

These same capabilities are available via the Agent Control Plane MCP server:
- **URL**: `https://modelslab.com/mcp/agents`
- **Tools**: `agent-models`, `agent-usage`

See: https://docs.modelslab.com/mcp-web-api/agent-control-plane

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/models` | Search models |
| GET | `/models/filters` | Available filter options |
| GET | `/models/tags` | Available tags |
| GET | `/models/providers` | Available providers |
| GET | `/models/{modelId}` | Model details |
| GET | `/usage/summary` | Usage summary |
| GET | `/usage/products` | Usage by product |
| GET | `/usage/history` | Generation history |

## Feature Values

Use these feature values when filtering models:

| Feature | Description |
|---------|-------------|
| `imagen` | Image generation (text-to-image, img-to-img) |
| `video_fusion` | Video generation (text-to-video, img-to-video) |
| `audio_gen` | Audio generation (TTS, music, SFX, voice cloning) |
| `llmaster` | LLM / Chat completions |
| `threed` | 3D model generation |
| `interior` | Interior design |
| `deepfake` | Face swap / Deepfake |

## Best Practices

### 1. Use Feature Filters
```python
# More efficient than broad text search
models = search_models(token, feature="imagen", sort="popular")
```

### 2. Cache Model Lists
```python
# Model lists don't change frequently
import functools

@functools.lru_cache(maxsize=32)
def cached_search(feature, sort="recommended"):
    return search_models(token, feature=feature, sort=sort)
```

### 3. Check Model Details Before Using
```python
detail = get_model_detail(token, model_id)
# Verify model supports your use case, check pricing, etc.
```

### 4. Monitor Usage Regularly
```python
# Set up daily usage checks
summary = get_usage_summary(token)
if summary.get("credits_remaining", 0) < 100:
    print("Low credits — consider topping up wallet")
```

## Resources

- **API Documentation**: https://docs.modelslab.com/agents-api/usage-and-models
- **Model Library**: https://modelslab.com/models
- **MCP Server**: https://docs.modelslab.com/mcp-web-api/agent-control-plane
- **Dashboard**: https://modelslab.com/dashboard

## Related Skills

- `modelslab-account-management` - Account setup, API keys, teams
- `modelslab-billing-subscriptions` - Wallet funding and subscriptions
- `modelslab-image-generation` - Use discovered models for image generation
- `modelslab-video-generation` - Use discovered models for video generation
