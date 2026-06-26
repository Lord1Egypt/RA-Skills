# Python Template

Use this template when the user asks for Python code. Fill in `PREFERRED_MODELS`
and `USER_PROMPT` from context. Keep all inline comments — they explain the fallback logic.

```python
"""
openrouter_connect_client.py — OpenRouter free-model client with ranked fallback
"""

import os
import json
import math
import time
from pathlib import Path

try:
    from openai import OpenAI  # openai>=1.0 works with OpenRouter
except ImportError:
    raise SystemExit("Run: pip install openai python-dotenv")

from dotenv import load_dotenv


# ── Config ────────────────────────────────────────────────────────────────────

# Ranked preference list — tried in order, skipping unavailable free models.
# Override at runtime via OPENROUTER_PREFERRED_MODELS=a,b,c in your .env
PREFERRED_MODELS: list[str] = [
    # ── Tier 1: Qwen ──────────────────────────────────────
    "qwen/qwen-2.5-72b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "qwen/qwen-2-72b-instruct:free",
    # ── Tier 2: GLM (Zhipu AI) ────────────────────────────
    "thudm/glm-4-9b:free",
    "thudm/glm-z1-32b:free",
    # ── Tier 3: Nemotron (NVIDIA) ─────────────────────────
    "nvidia/llama-3.1-nemotron-70b-instruct:free",
    "nvidia/nemotron-4-340b-instruct:free",
    # ── Tier 4: auto-ranked pool takes over if all above fail
]

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
MODELS_ENDPOINT     = f"{OPENROUTER_API_BASE}/models"
CACHE_FILE          = Path("/tmp/.openrouter_free_models_cache.json")
CACHE_TTL_SECONDS   = 3600  # re-fetch free model list at most once per hour


# ── Key resolution ─────────────────────────────────────────────────────────────

def load_api_key() -> str:
    """
    Look for OPENROUTER_API_KEY in:
      1. ./env  (project root)
      2. ~/.env (global fallback)
      3. Already-exported shell environment
    Raises RuntimeError if not found.
    """
    # 1. Project .env
    project_env = Path(".env")
    if project_env.exists():
        load_dotenv(project_env, override=False)

    # 2. Global ~/.env
    global_env = Path.home() / ".env"
    if global_env.exists():
        load_dotenv(global_env, override=False)

    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "OPENROUTER_API_KEY not found.\n"
            "Add it to ./.env or ~/.env:\n\n"
            "  OPENROUTER_API_KEY=sk-or-...\n\n"
            "Get a free key at https://openrouter.ai/keys"
        )
    return key


# ── Free model discovery ───────────────────────────────────────────────────────

def fetch_free_models(force_refresh: bool = False) -> list[dict]:
    """
    Return a list of free OpenRouter models, using a local cache when fresh.
    No auth required for the /models endpoint.
    """
    import urllib.request

    if not force_refresh and CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        if age < CACHE_TTL_SECONDS:
            with open(CACHE_FILE) as f:
                return json.load(f)

    with urllib.request.urlopen(MODELS_ENDPOINT, timeout=10) as resp:
        all_models: list[dict] = json.loads(resp.read())["data"]

    free = [
        m for m in all_models
        if m.get("pricing", {}).get("prompt") == "0"
        and m.get("pricing", {}).get("completion") == "0"
    ]

    CACHE_FILE.write_text(json.dumps(free))
    return free


def auto_rank(free_models: list[dict]) -> list[str]:
    """
    Score free models and return IDs sorted best-first.
    Scoring: context window 40%, recency 30%, provider reputation 30%.
    """
    tier_a = {"google", "meta-llama", "mistralai", "anthropic"}
    tier_b = {"qwen", "nvidia", "microsoft", "cohere", "deepseek"}

    # Allow overrides from env
    env_a = os.getenv("OPENROUTER_TIER_A", "")
    env_b = os.getenv("OPENROUTER_TIER_B", "")
    if env_a:
        tier_a = set(env_a.split(","))
    if env_b:
        tier_b = set(env_b.split(","))

    now = time.time()
    scored = []
    for m in free_models:
        ctx    = m.get("context_length", 4096)
        ctx_s  = min(math.log(max(ctx, 1)) / math.log(200_000), 1.0)

        created = m.get("created", 0)
        age_days = (now - created) / 86400 if created else 730
        rec_s  = max(0.0, 1.0 - age_days / 730)

        provider = m["id"].split("/")[0]
        rep_s = 1.0 if provider in tier_a else (0.7 if provider in tier_b else 0.4)

        score = 0.4 * ctx_s + 0.3 * rec_s + 0.3 * rep_s
        scored.append((score, m["id"]))

    scored.sort(reverse=True)
    return [mid for _, mid in scored]


def resolve_model(preferred: list[str] | None = None) -> str:
    """
    Return the best available free model ID using the ranked fallback chain:
      1. Try each model in `preferred` — skip if not currently free
      2. Fall back to auto-ranked free pool
    Raises RuntimeError if no free models exist at all.
    """
    free_models  = fetch_free_models()
    free_ids     = {m["id"] for m in free_models}

    # Read preference list from env if not passed in
    if preferred is None:
        env_prefs = os.getenv("OPENROUTER_PREFERRED_MODELS", "")
        preferred = [p.strip() for p in env_prefs.split(",") if p.strip()] \
                    or PREFERRED_MODELS

    for model_id in preferred:
        if model_id in free_ids:
            print(f"[openrouter-connect] Selected (preferred): {model_id}")
            return model_id
        else:
            print(f"[openrouter-connect] Skipping {model_id} (not free right now)")

    # Auto-rank fallback
    ranked = auto_rank(free_models)
    if ranked:
        print(f"[openrouter-connect] Falling back to auto-ranked: {ranked[0]}")
        return ranked[0]

    raise RuntimeError("No free OpenRouter models available right now.")


# ── Query with fallback ────────────────────────────────────────────────────────

def query(
    prompt: str,
    preferred: list[str] | None = None,
    system: str = "You are a helpful assistant.",
    max_retries: int = 3,
    stream: bool = True,
) -> str:
    """
    Send `prompt` to the best available free model.
    On 429 or 5xx, automatically retries with the next model in the chain.
    """
    api_key     = load_api_key()
    free_models = fetch_free_models()
    free_ids    = {m["id"] for m in free_models}

    # Build the full ordered list to try
    env_prefs = os.getenv("OPENROUTER_PREFERRED_MODELS", "")
    if preferred is None:
        preferred = [p.strip() for p in env_prefs.split(",") if p.strip()] \
                    or PREFERRED_MODELS

    ranked_fallback = auto_rank(free_models)
    # Combine: preferred list (filtered to free) + auto-ranked extras
    ordered = [m for m in preferred if m in free_ids] + \
              [m for m in ranked_fallback if m not in preferred]

    client = OpenAI(api_key=api_key, base_url=OPENROUTER_API_BASE)
    tried  = []

    for model_id in ordered[:max_retries]:
        tried.append(model_id)
        try:
            print(f"[openrouter-connect] Trying: {model_id}")
            messages = [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ]
            if stream:
                response = client.chat.completions.create(
                    model=model_id, messages=messages, stream=True
                )
                chunks = []
                for chunk in response:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    chunks.append(delta)
                print()  # newline after stream
                return "".join(chunks)
            else:
                response = client.chat.completions.create(
                    model=model_id, messages=messages
                )
                return response.choices[0].message.content

        except Exception as e:
            err = str(e)
            if "429" in err or "5" in err[:3]:
                print(f"[openrouter-connect] {model_id} failed ({err[:60]}), trying next…")
                continue
            raise  # unexpected error — surface it

    raise RuntimeError(
        f"All {max_retries} models failed or rate-limited.\nTried: {tried}"
    )


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    result = query("Explain what a large language model is in two sentences.")
    # result is also the return value if you call query() from your own code
```

## Dependencies

```
pip install openai python-dotenv
```

## Usage examples

```python
# One-shot query (uses ranked fallback automatically)
from openrouter_connect_client import query
answer = query("What is the capital of France?")

# Custom preference list inline
answer = query(
    "Write a haiku about Python.",
    preferred=[
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ]
)

# Just resolve which model would be chosen without sending a query
from openrouter_connect_client import resolve_model
print(resolve_model())
```
