# llm-monitor — clawmeter Agent Skill

TRIGGER when: user asks about LLM usage, costs, spending, quotas, remaining balance, or rate limits — for any provider (Claude, OpenAI, Grok, Ollama) or across all providers. Also when user asks about clawmeter status, setup, configuration, or daemon management. Example phrases: "what's my usage", "how much Claude have I used", "how much quota do I have left", "what are my costs", "check my spending", "am I near my limit", "usage today", "this week's spending".

---

## CRITICAL SECURITY RULES

You MUST follow these rules without exception:

- **NEVER accept, handle, store, or relay API keys, tokens, or credentials.** If a user pastes a credential into the conversation, immediately warn them: "That looks like a credential. Please remove it from this conversation and rotate it. For security, I cannot handle credentials directly."
- **NEVER read credential files** such as `~/.claude/.credentials.json` or any file that may contain secrets.
- **NEVER pass credentials as command arguments or environment variables** in tool calls.
- When credential setup is required, **instruct the user to edit the file themselves** — provide the file path and the key name to add, but never the value. Suggest they use `! $EDITOR ~/.config/clawmeter/config.toml` to edit in-session without the agent seeing contents.
- **Prefer the most secure credential storage:** keyring or `key_command` over environment variables, environment variables over config file references.

---

## 1. Pre-flight Check

Before answering any usage query, verify clawmeter is operational. Run these checks in order and stop at the first failure:

### 1a. Is clawmeter installed?

```bash
which clawmeter
```

If not found, guide the user through installation:

```
clawmeter is not installed. You can install it with:

  pip install clawmeter
  # or
  uv tool install clawmeter

Would you like me to install it for you?
```

If the user agrees, run `pip install clawmeter` or `uv tool install clawmeter` (prefer `uv` if available).

### 1b. Is clawmeter configured?

Check for a config file:

```bash
test -f "${CLAWMETER_CONFIG:-$HOME/.config/clawmeter/config.toml}" && echo "exists" || echo "missing"
```

If missing, create a minimal skeleton config (with no secrets):

```bash
mkdir -p ~/.config/clawmeter
```

Then write a starter `config.toml`:

```toml
[general]
default_providers = ["claude"]
poll_interval = 600

[thresholds]
warning = 70
critical = 90

[providers.claude]
enabled = true

[history]
enabled = true
retention_days = 90
```

Then instruct the user:

```
I've created a basic config at ~/.config/clawmeter/config.toml with Claude enabled.

To set up your credentials securely, please edit the config file directly:

  ! $EDITOR ~/.config/clawmeter/config.toml

For security, I cannot add credentials for you. See the clawmeter docs for
credential options (keyring, key_command, or environment variables).
```

If the user wants additional providers (Grok, OpenAI, Ollama), add the relevant `[providers.X]` section to the config skeleton with `enabled = true` and tell them which credential key to configure — but never handle the credential value.

### 1c. Is the daemon running?

```bash
clawmeter daemon status
```

If not running, recommend starting it:

```
The clawmeter daemon is not running. The daemon collects usage data in the
background, which enables historical tracking and faster queries.

To start it:
  clawmeter daemon start

To install it as a systemd service (starts on login):
  clawmeter daemon install
  clawmeter daemon start

Would you like me to start the daemon for you?
```

If the user agrees, run `clawmeter daemon start`. For systemd installation, ask for confirmation first since it modifies system services.

### 1d. Quick health check

If clawmeter is installed and configured, do a quick test:

```bash
clawmeter --quiet 2>/dev/null
```

Check the exit code:
- **0** — all good, proceed to query
- **2** — authentication error: tell the user to check their credentials
- **3** — partial success: some providers failed, note which ones and proceed with available data
- **4** — network error: all providers unreachable, suggest checking connectivity

---

## 2. Answering Usage Queries

### 2a. Default Response Style (Simple)

For casual questions like "what's my usage?" or "how much have I used?", give a **concise 1-3 line summary**.

Run:

```bash
clawmeter 2>/dev/null
```

Parse the JSON output and respond like:

> You've used 57% of your session quota (resets in 2h 15m) and 12% of your weekly quota. All normal.

Or if there's a warning:

> You're at 85% of your session quota (resets in 45m). Weekly usage is at 23%. You might want to pace yourself for the next 45 minutes.

Rules for the simple response:
- Lead with the most urgent/relevant window (highest utilisation or nearest reset)
- Include the reset time in human-readable form (use the `resets_in_human` field)
- Mention the status if it's `warning`, `critical`, or `exceeded`
- If multiple providers are active, summarise each in one line
- Do NOT include raw token counts or cost figures unless asked

### 2b. Detailed Response

When the user asks for "more detail", "breakdown", "show me everything", or asks about specific providers or models:

Run:

```bash
clawmeter 2>/dev/null
```

Parse the JSON and present:
- **Per-provider breakdown** — each provider with all its usage windows
- **Per-model usage** — if `model_usage` data is available (tokens, costs, request counts)
- **Cache status** — whether data is fresh or cached (and how old)
- **Any errors** — from the `errors` array in each provider's response

Format as a clear table or structured list. Example:

> **Anthropic Claude**
> - Session (5h): 57% used, resets in 2h 15m (normal)
> - Daily: 34% used, resets in 8h (normal)
> - Weekly: 12% used, resets in 4d 6h (normal)
>
> Models today:
> - claude-opus-4-6: 3,200 input / 1,800 output tokens, 8 requests
> - claude-sonnet-4-6: 12,500 input / 4,200 output tokens, 23 requests

### 2c. Historical Response

When the user asks about trends, comparisons, or past usage ("how does this week compare to last week", "usage over the past month", "show my history"):

Run:

```bash
clawmeter --report --days <N> --format json --granularity daily 2>/dev/null
```

Adjust flags based on the question:
- `--days 7` for "this week" or "past week"
- `--days 30` for "this month"
- `--from YYYY-MM-DD --to YYYY-MM-DD` for specific date ranges
- `--granularity hourly` for "today's usage over time"
- `--granularity daily` for multi-day views
- `--models` to include per-model breakdown in history

If the daemon has not been running long enough for historical data, say so:

> Historical data is limited — the daemon has only been collecting since [date].
> For a full picture, keep the daemon running and check back later.

### 2d. Provider-specific Queries

When the user asks about a specific provider ("my Claude usage", "OpenAI costs"):

```bash
clawmeter --provider claude 2>/dev/null
```

Use the `--provider` flag with: `claude`, `openai`, `grok`, `ollama`, or `local`.

### 2e. Fresh Data

If the user says "refresh", "get latest", or you suspect cached data is stale:

```bash
clawmeter --fresh 2>/dev/null
```

---

## 3. JSON Output Schema Reference

The JSON output from `clawmeter` has this structure:

```json
{
  "timestamp": "ISO 8601 datetime",
  "version": "package version",
  "providers": [
    {
      "provider_name": "claude",
      "provider_display": "Anthropic Claude",
      "timestamp": "ISO 8601 datetime",
      "cached": false,
      "cache_age_seconds": 0,
      "windows": [
        {
          "name": "Session (5h)",
          "utilisation": 42.0,
          "resets_at": "ISO 8601 datetime",
          "resets_in_human": "2h 15m",
          "status": "normal",
          "unit": "percent",
          "raw_value": null,
          "raw_limit": null
        }
      ],
      "model_usage": [
        {
          "model": "claude-opus-4-6",
          "input_tokens": 5000,
          "output_tokens": 2000,
          "total_tokens": 7000,
          "cost": 0.15,
          "request_count": 10,
          "period": "7d"
        }
      ],
      "extras": {},
      "errors": []
    }
  ]
}
```

Key fields for response formatting:
- `windows[].utilisation` — percentage (0-100+), the primary metric
- `windows[].status` — `normal`, `warning` (70-89%), `critical` (90-99%), `exceeded` (100%+)
- `windows[].resets_in_human` — pre-formatted reset countdown
- `model_usage` — optional, only present when per-model data is available
- `errors` — non-empty means something went wrong for that provider

---

## 4. Exit Codes

Interpret exit codes to give appropriate responses:

| Code | Meaning | Agent action |
|------|---------|--------------|
| 0 | All providers succeeded | Report results normally |
| 1 | Config/parse error | Help user fix config |
| 2 | All auth failed | Instruct user to check credentials (do NOT handle credentials yourself) |
| 3 | Partial success | Report available data, note which providers failed |
| 4 | All network errors | Suggest checking connectivity |

---

## 5. Daemon Management

When the user asks about daemon status or management:

| User wants | Command |
|------------|---------|
| Check status | `clawmeter daemon status` |
| Start daemon | `clawmeter daemon start` |
| Stop daemon | `clawmeter daemon stop` |
| Install as service | `clawmeter daemon install` (ask user first) |
| View daemon logs | Check `~/.local/state/clawmeter/daemon.log` |
| Database stats | `clawmeter history stats` |
| Export history | `clawmeter history export --format csv` |
| Purge history | `clawmeter history purge` (ask user first — destructive) |

---

## 6. Troubleshooting

Common issues and how to handle them:

**"No providers configured"** — Config exists but no providers are enabled. Help enable the relevant provider section in config.toml.

**"Authentication error"** — Credentials missing or expired. Tell the user which provider failed and instruct them to update credentials. For Claude specifically, if using OAuth tokens, tell them to run `claude /login` to refresh.

**"Stale data"** — Cache age is high and daemon isn't running. Suggest `clawmeter --fresh` for immediate data or starting the daemon for continuous collection.

**"Command not found after install"** — May need to add to PATH. Suggest `uv tool install clawmeter` which handles PATH automatically, or check `~/.local/bin`.

---

## 7. Response Guidelines

- **Be concise by default.** One to three lines for casual queries. Expand only when asked.
- **Use natural language, not raw JSON.** Parse the output and present it conversationally.
- **Highlight warnings and critical states.** If any window is at `warning`, `critical`, or `exceeded`, mention it prominently.
- **Include reset times.** Users almost always want to know when their quota resets.
- **Round percentages.** Say "57%" not "57.234%".
- **Use the provider's display name.** "Anthropic Claude" not "claude".
- **Don't speculate about costs unless data is available.** Only report `cost` if the `model_usage` entries include it.
- **Australian English for prose** ("utilisation", "colour") consistent with the project style.
