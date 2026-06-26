#!/usr/bin/env python3
"""
proxy_query.py — Send a prompt to the best available free OpenRouter model.

Usage:
  python3 proxy_query.py --prompt "Your question"
  python3 proxy_query.py --model "mistralai/mistral-7b-instruct:free" --prompt "Hi"
  echo "Your question" | python3 proxy_query.py

Options:
  --model MODEL    Force a specific model (skips preference resolution)
  --prompt TEXT    The user message to send
  --system TEXT    System prompt (default: "You are a helpful assistant.")
  --no-stream      Disable streaming (get full response at once)
  --json           Output as JSON  {model, response, tokens_used}
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
MODELS_ENDPOINT     = f"{OPENROUTER_API_BASE}/models"
CHAT_ENDPOINT       = f"{OPENROUTER_API_BASE}/chat/completions"
CACHE_FILE          = Path("/tmp/.openrouter_free_models_cache.json")
CACHE_TTL           = 3600
MAX_RETRIES         = 3

# Ranked preference list — Qwen → GLM → Nemotron → auto-ranked pool
PREFERRED_MODELS = [
    # Tier 1: Qwen
    "qwen/qwen-2.5-72b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
    "qwen/qwen-2-72b-instruct:free",
    # Tier 2: GLM (Zhipu AI)
    "thudm/glm-4-9b:free",
    "thudm/glm-z1-32b:free",
    # Tier 3: Nemotron (NVIDIA)
    "nvidia/llama-3.1-nemotron-70b-instruct:free",
    "nvidia/nemotron-4-340b-instruct:free",
]


# ── env / key helpers (same as resolve_key.py) ───────────────────────────────

def load_env_file(p: Path) -> dict:
    if not p.exists():
        return {}
    out = {}
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip("\"'")
    return out


def get_env() -> dict:
    env = {}
    env.update(load_env_file(Path.home() / ".env"))
    env.update(load_env_file(Path(".env")))
    env.update(os.environ)
    return env


def get_key(env: dict) -> str:
    key = env.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        sys.exit(
            "ERROR: OPENROUTER_API_KEY not found.\n"
            "Add it to ./.env or ~/.env:\n\n"
            "  OPENROUTER_API_KEY=sk-or-...\n\n"
            "Get a free key at https://openrouter.ai/keys"
        )
    return key


# ── model resolution ─────────────────────────────────────────────────────────

def fetch_free_models(force: bool = False) -> list:
    if not force and CACHE_FILE.exists():
        if time.time() - CACHE_FILE.stat().st_mtime < CACHE_TTL:
            return json.loads(CACHE_FILE.read_text())
    with urllib.request.urlopen(MODELS_ENDPOINT, timeout=10) as r:
        data = json.loads(r.read())["data"]
    free = [m for m in data
            if m.get("pricing", {}).get("prompt") == "0"
            and m.get("pricing", {}).get("completion") == "0"]
    CACHE_FILE.write_text(json.dumps(free))
    return free


def auto_rank(models: list, env: dict) -> list[str]:
    tier_a = set((env.get("OPENROUTER_TIER_A") or "google,meta-llama,mistralai,anthropic").split(","))
    tier_b = set((env.get("OPENROUTER_TIER_B") or "qwen,nvidia,microsoft,cohere,deepseek").split(","))
    now = time.time()
    scored = []
    for m in models:
        ctx   = m.get("context_length", 4096)
        ctx_s = min(math.log(max(ctx, 1)) / math.log(200_000), 1.0)
        age   = (now - m.get("created", 0)) / 86400 if m.get("created") else 730
        rec_s = max(0.0, 1.0 - age / 730)
        prov  = m["id"].split("/")[0]
        rep_s = 1.0 if prov in tier_a else (0.7 if prov in tier_b else 0.4)
        scored.append((0.4*ctx_s + 0.3*rec_s + 0.3*rep_s, m["id"]))
    scored.sort(reverse=True)
    return [mid for _, mid in scored]


def build_order(forced_model: str | None, env: dict) -> list[str]:
    if forced_model:
        return [forced_model]

    free_models = fetch_free_models()
    free_ids    = {m["id"] for m in free_models}

    env_prefs = env.get("OPENROUTER_PREFERRED_MODELS", "")
    preferred = [p.strip() for p in env_prefs.split(",") if p.strip()] \
                or PREFERRED_MODELS

    ranked = auto_rank(free_models, env)
    return ([m for m in preferred if m in free_ids] +
            [m for m in ranked if m not in preferred])


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def post_json(url: str, payload: dict, api_key: str) -> urllib.request.Request:
    body    = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    request.add_header("Authorization", f"Bearer {api_key}")
    request.add_header("HTTP-Referer", "https://github.com/openrouter-connect")
    return request


# ── streaming ─────────────────────────────────────────────────────────────────

def stream_response(resp) -> tuple[str, int]:
    """Read SSE stream, print to stdout, return (full_text, total_tokens)."""
    chunks       = []
    total_tokens = 0
    for raw_line in resp:
        line = raw_line.decode().rstrip()
        if not line.startswith("data: "):
            continue
        data = line[6:]
        if data == "[DONE]":
            break
        try:
            obj   = json.loads(data)
            delta = obj["choices"][0]["delta"].get("content", "")
            if delta:
                print(delta, end="", flush=True)
                chunks.append(delta)
            if obj.get("usage"):
                total_tokens = obj["usage"].get("total_tokens", 0)
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
    print()  # newline
    return "".join(chunks), total_tokens


# ── main send loop ────────────────────────────────────────────────────────────

def send(prompt: str, system: str, model_order: list[str],
         api_key: str, stream: bool, as_json: bool) -> None:

    tried = []
    for model_id in model_order[:MAX_RETRIES]:
        tried.append(model_id)
        print(f"[openrouter-connect] Trying: {model_id}", file=sys.stderr)

        payload = {
            "model":    model_id,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            "stream": stream,
        }
        req = post_json(CHAT_ENDPOINT, payload, api_key)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                if stream:
                    text, tokens = stream_response(resp)
                else:
                    body  = json.loads(resp.read())
                    text  = body["choices"][0]["message"]["content"]
                    tokens = body.get("usage", {}).get("total_tokens", 0)
                    if not as_json:
                        print(text)

            if as_json:
                print(json.dumps({"model": model_id, "response": text, "tokens_used": tokens}))
            return

        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                print(f"[openrouter-connect] {model_id} → HTTP {e.code}, trying next…", file=sys.stderr)
                continue
            raise
        except Exception as e:
            print(f"[openrouter-connect] {model_id} → error: {e}, trying next…", file=sys.stderr)
            continue

    sys.exit(f"All {MAX_RETRIES} models failed or rate-limited.\nTried: {tried}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Query a free OpenRouter model")
    parser.add_argument("--model",     help="Force a specific model ID")
    parser.add_argument("--prompt",    help="User message (reads stdin if omitted)")
    parser.add_argument("--system",    default="You are a helpful assistant.")
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("--json",      action="store_true", help="Output as JSON")
    args = parser.parse_args()

    prompt = args.prompt or sys.stdin.read().strip()
    if not prompt:
        sys.exit("ERROR: No prompt provided. Use --prompt or pipe via stdin.")

    env         = get_env()
    api_key     = get_key(env)
    model_order = build_order(args.model, env)

    if not model_order:
        sys.exit("ERROR: No free models available right now.")

    send(
        prompt      = prompt,
        system      = args.system,
        model_order = model_order,
        api_key     = api_key,
        stream      = not args.no_stream,
        as_json     = args.json,
    )


if __name__ == "__main__":
    main()
