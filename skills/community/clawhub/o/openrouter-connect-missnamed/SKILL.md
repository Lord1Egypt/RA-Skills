---
name: openrouter-connect
description: >
  Use this skill whenever the user wants to work with OpenRouter's free LLM models.
  Triggers include: any mention of "OpenRouter", "free models", "openrouter-connect", routing
  queries through a free LLM, writing code to call OpenRouter, or picking/testing
  an OpenRouter model. Also use when the user wants to proxy a question to a free
  model, compare free model outputs, or scaffold code (Python or JS/TS) that calls
  OpenRouter. Always use this skill when OpenRouter or free-tier LLM routing is involved.
---

# OpenClaw — OpenRouter Free Model Skill

OpenClaw helps you:
1. **Discover** all currently-free OpenRouter models at runtime
2. **Select** one using a ranked preference list (fallback chain)
3. **Proxy** a query live through the chosen model right in this conversation
4. **Scaffold** production-ready Python or TypeScript code that does the same

---

## Step 0 — Read the API key

Look for `OPENROUTER_API_KEY` in this priority order:

1. **Project `.env`** — `./` relative to the user's current working directory  
2. **Global `~/.env`** — the user's home directory  
3. **Shell environment** — already exported in the current shell session

Use the helper script to resolve this:

```bash
python3 /home/claude/openrouter-connect/scripts/resolve_key.py
```

If no key is found, tell the user and show them the quick-start box:

> **No key found.** Get a free key at https://openrouter.ai/keys then add it to `.env`:
> ```
> OPENROUTER_API_KEY=sk-or-...
> ```

---

## Step 1 — Discover free models

Run the discovery script to fetch and cache the free model list:

```bash
python3 /home/claude/openrouter-connect/scripts/discover_models.py [--refresh]
```

This calls `GET https://openrouter.ai/api/v1/models` (no auth required) and filters
for models where **both** `pricing.prompt == "0"` and `pricing.completion == "0"`.

The script outputs a JSON array ranked by the default preference list (see
`references/model_preferences.md` for how ranking works and how to customise it).

Pass `--refresh` to bypass the 1-hour local cache.

---

## Step 2 — Select a model (ranked fallback chain)

Read `references/model_preferences.md` for the full preference system.

**Quick summary:**
- The user's explicit ranked list is tried first (index 0 = highest priority)
- If a listed model isn't free right now, it's skipped
- If no listed model is available, fall back to the auto-ranked free pool
- Auto-ranking scores by: context window (weight 0.4), recency (0.3), provider reputation (0.3)

To ask the user for their preference list, show them the discovered models and say:
> "Here are the free models I found. Would you like to rank your favourites, or should I pick the best one automatically?"

---

## Step 3a — Proxy a query live

Once a model is selected, call it directly using the script:

```bash
python3 /home/claude/openrouter-connect/scripts/proxy_query.py \
  --model "mistralai/mistral-7b-instruct:free" \
  --prompt "Your question here"
```

Stream the response back to the user and note which model was used.

If the model returns a 429 (rate limit) or 5xx, automatically retry with the next
model in the ranked list. Log which model was tried and why it was skipped.

---

## Step 3b — Scaffold code for the user

Read the appropriate template from `references/`:
- **Python**: `references/python_template.md`
- **TypeScript / JS**: `references/typescript_template.md`

Fill in:
- The selected model ID
- `.env` loading boilerplate (checks `./` then `~/`)
- The fallback/retry loop
- A working `main()` example with the user's actual prompt if they provided one

Always include inline comments explaining the fallback logic.

---

## Edge cases & notes

| Situation | Behaviour |
|-----------|-----------|
| Model mid-list becomes paid | Skip it, log a warning, continue down the list |
| All ranked models unavailable | Fall back to auto-ranked free pool |
| No free models found at all | Tell the user — OpenRouter's free tier may be down |
| Key found but invalid (401) | Prompt user to check the key; show the OpenRouter keys URL |
| User provides a model not in the free list | Warn them it may incur cost; ask to confirm |
| Streaming not supported by model | Fall back to non-streaming request silently |

---

## Reference files

| File | When to read |
|------|-------------|
| `references/model_preferences.md` | Ranking algorithm, customisation, default weights |
| `references/python_template.md` | Generating Python code |
| `references/typescript_template.md` | Generating TS/JS code |
