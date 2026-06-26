---
name: pangolinfo-ai-serp
description: >
  Search Google and get AI Overviews using Pangolin APIs. Use this skill when
  the user wants to: search Google with AI answers, get search engine results,
  perform multi-turn AI search conversations, or capture search screenshots.
  Requires PANGOLIN_EMAIL + PANGOLIN_PASSWORD env vars (or PANGOLIN_API_KEY).
---

# Pangolinfo AI SERP Skill

Search Google and retrieve AI Overviews, organic search results, and screenshots via Pangolin APIs.

## When to Use This Skill

Activate this skill when the user's intent matches any of these patterns:

- "Search Google for ...", "Google ...", "Look up ..."
- "What does Google say about ...", "Search the web for ..."
- "Get AI overview for ...", "AI search for ..."
- "Get search results for ...", "SERP for ..."
- "Take a screenshot of Google results for ..."
- "Follow up on the search with ..."
- Chinese equivalents: "搜索一下...", "谷歌搜索...", "帮我查一下...", "用Google搜...", "搜一下...", "AI搜索..."

Do **not** use this skill for Amazon product searches, price lookups, or review scraping -- those require a different skill.

## Prerequisites

### Runtime

- Python 3.8+ (uses only the standard library -- no `pip install` needed)

### Pangolin Account

Register at [pangolinfo.com](https://www.pangolinfo.com) to obtain credentials.

### Environment Variables

Set **one** of the following:

| Variable | Required | Description |
|----------|----------|-------------|
| `PANGOLIN_API_KEY` | Option A | API Key (skips login) |
| `PANGOLIN_EMAIL` | Option B | Account email |
| `PANGOLIN_PASSWORD` | Option B | Account password |

API key resolution order: `PANGOLIN_API_KEY` env var > cached `~/.pangolin_api_key` > fresh login.

### macOS SSL Certificate Fix

On macOS, Python may fail with `CERTIFICATE_VERIFY_FAILED` because it ships without root certificates by default.

**Symptoms:** The script outputs an error with code `SSL_CERT`.

**Solutions (pick one):**

1. Run the certificate installer that ships with Python:
   ```bash
   /Applications/Python\ 3.x/Install\ Certificates.command
   ```
   (Replace `3.x` with your Python version, e.g. `3.11`)

2. Set the `SSL_CERT_FILE` environment variable:
   ```bash
   pip3 install certifi
   export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
   ```

## First-Time Setup Guide

When a user tries to use this skill and authentication fails (error code `MISSING_ENV`), **do not just repeat the error hint**. Instead, walk the user through the full setup process interactively:

### Step 1: Explain what's needed

Tell the user (in their language):

> To use this skill, you need a Pangolin API account. Pangolin provides Google search and AI Overview data through its APIs.
>
> 使用本技能需要 Pangolin API 账号。Pangolin 提供 Google 搜索和 AI 概览数据的 API 服务。

### Step 2: Guide registration

> 1. Go to [pangolinfo.com](https://www.pangolinfo.com) and create an account
> 2. After login, find your API Key in the dashboard
>
> 1. 访问 [pangolinfo.com](https://www.pangolinfo.com) 注册账号
> 2. 登录后在控制台找到你的 API Key

### Step 3: Collect credentials and authenticate automatically

When the user provides their credentials, **you (the AI agent) should configure them securely**. The script will automatically cache the API key at `~/.pangolin_api_key` for all future calls.

**If user provides an API key (recommended):**
Write it directly to the cache file — avoids shell history entirely:
```bash
echo "<api_key>" > ~/.pangolin_api_key
chmod 600 ~/.pangolin_api_key 2>/dev/null
python3 scripts/pangolin.py --auth-only
```

**If user provides email + password:**
Set env vars in the session and clean up after auth:
```bash
export PANGOLIN_EMAIL="user@example.com"
export PANGOLIN_PASSWORD="their-password"
python3 scripts/pangolin.py --auth-only
unset PANGOLIN_EMAIL PANGOLIN_PASSWORD
```

This avoids passwords appearing in shell history (unlike inline `VAR=x command` syntax) and cleans up credentials after the API key is cached.

Both methods cache the API key automatically. After this one-time setup, **no environment variables are needed** — all future calls will use the cached API key at `~/.pangolin_api_key`.

### Step 4: Confirm and proceed

After auth returns `"success": true`:
1. Tell the user: "认证成功！API Key 已自动缓存，后续使用无需再次输入。" / "Authentication successful! API key cached — no need to enter credentials again."
2. Immediately retry their original request.

### Important

- **The user only needs to provide credentials ONCE** — the script caches the API key permanently at `~/.pangolin_api_key`
- Do not ask the user to manually edit `.bashrc` or `.zshrc` — the script handles persistence automatically
- If the user doesn't have an account yet, explain Pangolin's credit system (2 credits per AI Mode search, 0.5 credits per SERP search) and direct them to [pangolinfo.com](https://www.pangolinfo.com)
- If auth succeeds but credits are exhausted (error code `2001`), tell the user to top up at pangolinfo.com
- API key is permanent and does not expire unless the account is deactivated

## Script Execution

The main script is located at `scripts/pangolin.py` relative to this skill directory.

**Path resolution:** When invoking the script, resolve the absolute path from this skill's directory. Example:

```bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SKILL_DIR/scripts/pangolin.py" --q "your query"
```

Or invoke directly:

```bash
python3 scripts/pangolin.py --q "your query"
```

## Intent-to-Command Mapping

### AI Mode Search (default)

User wants AI-generated answers with references. This is the default mode.

```bash
python3 scripts/pangolin.py --q "what is quantum computing"
```

### Standard SERP

User wants traditional Google search results (organic links + optional AI overview).

```bash
python3 scripts/pangolin.py --q "best databases 2025" --mode serp
```

### SERP with Screenshot

User wants to see the actual Google results page.

```bash
python3 scripts/pangolin.py --q "best databases 2025" --mode serp --screenshot
```

### SERP with Region

User wants SERP results from a specific geographic region.

```bash
python3 scripts/pangolin.py --q "best databases 2025" --mode serp --region us
```

### Multi-Turn Dialogue

User wants to ask follow-up questions in an AI Mode conversation.

```bash
python3 scripts/pangolin.py --q "kubernetes" --follow-up "how to deploy" --follow-up "monitoring tools"
```

### Auth Check

Verify credentials are working without consuming credits.

```bash
python3 scripts/pangolin.py --auth-only
```

## Smart Defaults

| Parameter | Default | Notes |
|-----------|---------|-------|
| `--mode` | `ai-mode` | AI Mode with Google AI Overviews |
| `--num` | `10` | Number of results to request |
| `--screenshot` | off | Pass flag to enable |
| `--follow-up` | none | Repeatable; keep to 5 or fewer for speed |

When the user simply says "search for X" without specifying a mode, use the default `ai-mode`.

## Output Format

The script outputs JSON to **stdout** on success and structured error JSON to **stderr** on failure.

### Success Example (AI Mode)

```json
{
  "success": true,
  "task_id": "1768988520324-766a695d93b57aad",
  "results_num": 1,
  "ai_overview_count": 1,
  "ai_overview": [
    {
      "content": ["Quantum computing uses quantum bits (qubits)..."],
      "references": [
        {
          "title": "Quantum Computing - Wikipedia",
          "url": "https://en.wikipedia.org/wiki/Quantum_computing",
          "domain": "Wikipedia"
        }
      ]
    }
  ],
  "screenshot": "https://image.datasea.network/screenshots/..."
}
```

### Success Example (SERP)

```json
{
  "success": true,
  "task_id": "1768988520324-abcdef123456",
  "results_num": 3,
  "ai_overview_count": 1,
  "ai_overview": [
    {
      "content": ["Java works by compiling source code..."],
      "references": [
        {"title": "How Java Works", "url": "https://docs.oracle.com/...", "domain": "Oracle"}
      ]
    }
  ],
  "organic_results": [
    {
      "title": "Java Tutorial for Beginners",
      "url": "https://example.com/java-tutorial",
      "text": "Learn how Java works from the ground up..."
    }
  ]
}
```

### Error Example

```json
{
  "success": false,
  "error": {
    "code": "MISSING_ENV",
    "message": "No authentication credentials found.",
    "hint": "Set PANGOLIN_API_KEY, or both PANGOLIN_EMAIL and PANGOLIN_PASSWORD environment variables."
  }
}
```

## Response Presentation

When presenting results to the user:

1. **Use natural language** -- never dump raw JSON to the user.
2. **Match the user's language** -- if the user writes in Chinese, respond in Chinese; if English, respond in English.
3. **Summarize the AI overview** first (if present), then list relevant organic results with titles and URLs.
4. **Include source URLs** so the user can verify or explore further.
5. **Mention the screenshot URL** if one was captured, so the user can view the rendered page.
6. **If no AI overview** is present, note that Google did not generate one for this query and present organic results instead.
7. **On error**, explain the issue in plain language and suggest corrective action based on the `hint` field.

## All CLI Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--q` | string | *required* | Search query |
| `--mode` | `ai-mode` \| `serp` | `ai-mode` | API mode |
| `--screenshot` | flag | off | Capture page screenshot |
| `--follow-up` | string (repeatable) | none | Follow-up question (ai-mode only) |
| `--num` | int | `10` | Number of results |
| `--region` | string | none | Geographic region for SERP results (e.g., `us`, `uk`). SERP mode only. |
| `--auth-only` | flag | off | Auth check only (no query needed) |
| `--raw` | flag | off | Output raw API response |

## Output Schema

See [references/output-schema.md](references/output-schema.md) for the complete JSON output schema documentation.

## Cost

- **AI Mode:** 2 credits per request
- **SERP:** 0.5 credits per request

Credits are only consumed on successful requests (API code 0). Auth checks (`--auth-only`) do not consume credits.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | API error (non-zero code from Pangolin) |
| 2 | Usage error (bad arguments) |
| 3 | Network error (connection, SSL, timeout, rate limit) |
| 4 | Authentication error |

## Troubleshooting

### Error Communication Table

| Error Code | Meaning | User-Facing Message | Resolution |
|------------|---------|---------------------|------------|
| `MISSING_ENV` | No credentials | "Authentication credentials are not configured." | Set `PANGOLIN_EMAIL` + `PANGOLIN_PASSWORD` or `PANGOLIN_API_KEY`. |
| `AUTH_FAILED` | Wrong credentials | "Authentication failed. Please check your credentials." | Verify email and password are correct. |
| `RATE_LIMIT` | Too many requests | "The API is rate-limiting requests. Please wait and try again." | Wait a moment, then retry. |
| `NETWORK` | Connection issue | "A network error occurred. Please check your connection." | Check internet, firewall, proxy settings. |
| `SSL_CERT` | Certificate error | "SSL certificate verification failed." | See macOS SSL Certificate Fix section above. |
| `API_ERROR` | Pangolin API error | "The search API returned an error." | Check the `hint` field; see `references/error-codes.md`. |

### Pangolin API Error Codes

| API Code | Meaning | Resolution |
|----------|---------|------------|
| 1004 | Invalid/expired API key | Auto-retried by the script. If persistent, delete `~/.pangolin_api_key` and retry. |
| 2001 | Insufficient credits | Top up credits at pangolinfo.com. |
| 2007 | Account expired | Renew subscription at pangolinfo.com. |
| 10000 | Task execution failed | Retry the request. Check query format. |
| 10001 | Task execution failed | Retry. May be a temporary server issue. |

## Important Notes for AI Agents

1. **Always run `--auth-only` first** if you are unsure whether credentials are configured, before spending credits on a real query.
2. **Default to `ai-mode`** unless the user explicitly asks for standard/traditional search results.
3. **Never expose raw JSON** to the user. Parse the output and present it in natural language.
4. **Respect the user's language.** Respond in the same language the user is writing in.
5. **Keep follow-ups to 5 or fewer** for optimal response time. Warn the user if they request more.
6. **Handle errors gracefully.** If the script exits with a non-zero code, read stderr for the structured error and present the `hint` to the user.
7. **Do not log or echo API keys, passwords, or cookies** in any output, logs, or error messages.
8. **Credit awareness:** AI Mode costs 2 credits per search; SERP costs 0.5 credits. If a user requests many searches in a row, mention the credit cost.
9. **Screenshot is optional.** Only pass `--screenshot` when the user explicitly wants to see the rendered page or when visual context is needed.
10. **Multi-turn is ai-mode only.** Do not attempt `--follow-up` with `--mode serp`.
