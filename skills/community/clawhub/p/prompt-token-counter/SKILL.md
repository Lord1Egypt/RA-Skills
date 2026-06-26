---
name: prompt-token-counter
version: 1.0.10
description: "Count tokens and estimate costs for 300+ LLM models. Primary use: audit OpenClaw workspace token consumption (memory, persona, skills)."
trigger: "token count, cost estimate, prompt length, API cost, OpenClaw audit, workspace token usage, memory/persona/skills tokens, context window limit"
---

# Prompt Token Counter (toksum)

> **First load reminder:** This skill provides the `scripts` CLI (toksum). Use it when the user asks to count tokens, estimate API costs, or **audit OpenClaw component token consumption** (memory, persona, skills).

## Before Installing — Security & Privacy

- **What will be read:** The audit workflow reads files under `~/.openclaw/workspace` and `~/.openclaw/skills` (AGENTS.md, SOUL.md, MEMORY.md, SKILL.md, etc.). Those files may contain personal data or secrets. Only install if you accept that access.
- **URL fetching:** The CLI can fetch HTTP(S) URLs via `-u`. SKILL.md requires the agent to confirm each URL with the user before fetching. Insist the agent follow that rule; never allow automatic fetching of unknown URLs.
- **Source verification:** Source: [https://github.com/Zhaobudaoyuema/prompt-token-counter](https://github.com/Zhaobudaoyuema/prompt-token-counter). Review `scripts/core.py` and `scripts/cli.py` before use. The code performs local file reads and optional HTTP GETs only; no other network calls or data exfiltration.
- **Run locally first:** If unsure, run the CLI manually in an isolated environment against safe test files to verify behavior.

## Primary Use: OpenClaw Token Consumption Audit

**Goal:** Help users identify which OpenClaw components consume tokens and how much.

### 1. Memory & Persona Files

These files are injected into sessions and consume tokens. Search and count them:

| File | Purpose | Typical Location |
|------|---------|------------------|
| `AGENTS.md` | Operating instructions, workflow, priorities | `~/.openclaw/workspace/` |
| `SOUL.md` | Persona, tone, values, behavioral guidelines | `~/.openclaw/workspace/` |
| `IDENTITY.md` | Name, role, goals, visual description | `~/.openclaw/workspace/` |
| `USER.md` | User preferences, communication style | `~/.openclaw/workspace/` |
| `MEMORY.md` | Long-term memory, persistent facts | `~/.openclaw/workspace/` |
| `TOOLS.md` | Tool quirks, path conventions | `~/.openclaw/workspace/` |
| `HEARTBEAT.md` | Periodic maintenance checklist | `~/.openclaw/workspace/` |
| `BOOT.md` | Startup ritual (when hooks enabled) | `~/.openclaw/workspace/` |
| `memory/YYYY-MM-DD.md` | Daily memory logs | `~/.openclaw/workspace/memory/` |

**Workspace path:** Default `~/.openclaw/workspace`; may be overridden in `~/.openclaw/openclaw.json` via `agent.workspace`.

### 2. Skill Files (SKILL.md)

Skills are loaded per session. Count each `SKILL.md`:

| Location | Scope |
|----------|-------|
| `~/.openclaw/skills/*/SKILL.md` | OpenClaw managed skills |
| `~/.openclaw/workspace/skills/*/SKILL.md` | Workspace-specific skills (override) |

### 3. Audit Workflow

1. **Locate workspace:** Resolve `~/.openclaw/workspace` (or config override).
2. **Collect files:** List all memory/persona files and `SKILL.md` paths above.
3. **Count tokens:** Run `python -m scripts.cli <path1> <path2> ... -m <model> -c` (batch mode).
4. **Summarize:** Group by category (memory, persona, skills), report total and per-file.

**Example audit command (PowerShell):**
```powershell
$ws = "$env:USERPROFILE\.openclaw\workspace"
python -m scripts.cli -m gpt-4o -c "$ws\AGENTS.md" "$ws\SOUL.md" "$ws\USER.md" "$ws\IDENTITY.md" "$ws\MEMORY.md" "$ws\TOOLS.md"
```

**Example audit (Bash):**
```bash
WS=~/.openclaw/workspace
python -m scripts.cli -m gpt-4o -c "$WS/AGENTS.md" "$WS/SOUL.md" "$WS/USER.md" "$WS/IDENTITY.md" "$WS/MEMORY.md" "$WS/TOOLS.md"
```

---

## Project Layout

```
prompt_token_counter/
├── SKILL.md
├── package.json                # npm package (OpenClaw skill)
├── publish_npm.py               # Publish to npm; syncs version
└── scripts/                    # Python package, CLI + examples
    ├── cli.py                  # Entry point
    ├── core.py                 # TokenCounter, estimate_cost
    ├── registry/
    │   ├── models.py           # 300+ models
    │   └── pricing.py          # Pricing data
    └── examples/               # Script examples
        ├── count_prompt.py
        ├── estimate_cost.py
        ├── batch_compare.py
        └── benchmark_token_ratio.py
```

Invoke: `python -m scripts.cli` from project root.

### Version Sync (publish_npm.py)

When publishing to npm, `publish_npm.py` bumps the patch version and syncs it to:

- `package.json` — `version`
- `SKILL.md` — frontmatter `version`
- `scripts/__init__.py` — `__version__`

Run: `python publish_npm.py` (after `npm login`).

---

## Runtime Dependencies

- **Python 3** — required
- **tiktoken** (optional) — `pip install tiktoken` for exact OpenAI counts

---

## Language Rule

**Respond in the user's language.** Match the user's language (e.g. Chinese if they write in Chinese, English if they write in English).

---

## URL Usage — Mandatory Agent Rule

**Before using `-u` / `--url` to fetch content from any URL, you MUST:**

1. **Explicitly warn the user** that the CLI will make an outbound HTTP/HTTPS request to the given URL.
2. **Confirm the URL is trusted** — tell the user: "Only use URLs you fully trust. Untrusted URLs may expose your IP, leak data, or be used for SSRF. Do you confirm this URL is safe?"
3. **Prefer alternatives** — if the user can provide the content via `-f` (local file) or inline text, suggest that instead of URL fetch.
4. **Never auto-fetch** — do not invoke `-u` without the user having explicitly provided the URL and acknowledged the risk.

**If the user insists on using a URL:** Proceed only after they confirm. State clearly: "I will fetch from [URL] to count tokens. Proceed?"

---

## Model Name — Mandatory Agent Rule

**Before invoking the CLI, you MUST have a concrete model name from the user.**

1. **Require explicit model** — `-m` / `--model` is required. Do not guess or assume; the user must provide the exact name (e.g. gpt-4o, claude-3-5-sonnet-20241022).
2. **If unclear, ask** — if the user says "GPT" or "Claude" or "the latest model" without a specific name, ask: "Please specify the exact model name (e.g. gpt-4o, claude-3-5-sonnet-20241022). Run `python -m scripts.cli -l` to list supported models."
3. **Do not auto-pick** — never substitute a model on behalf of the user without their confirmation.
4. **Validate when possible** — if the model name seems ambiguous, offer `-l` output or confirm: "I'll use [model]. Is that correct?"

---

## CLI Usage

**Default:** Read from local file(s). No segmentation. Supports multiple file paths for batch execution.

```bash
python -m scripts.cli [OPTIONS] [FILE ...]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--model` | `-m` | Model name (required unless `--list-models`) — **Agent must obtain exact name from user; ask if unclear** |
| `--file` | `-f` | Read from file (repeatable) |
| `--url` | `-u` | Read from URL (repeatable) — **Agent must warn user before use; only trusted URLs** |
| `--list-models` | `-l` | List supported models |
| `--cost` | `-c` | Show cost estimate |
| `--output-tokens` | | Use output token pricing |
| `--currency` | | USD or INR |
| `--verbose` | `-v` | Detailed output |

### Examples

```bash
# Multiple local files (default batch mode)
python -m scripts.cli file1.txt file2.txt -m gpt-4
python -m scripts.cli AGENTS.md SOUL.md MEMORY.md -m gpt-4o -c

# Single file with -f
python -m scripts.cli -f input.txt -m claude-3-opus -c

# Inline text (when arg is not an existing file path)
python -m scripts.cli -m gpt-4 "Hello, world!"

# List models
python -m scripts.cli -l

# Run bundled example scripts
python scripts/examples/count_prompt.py file1.txt file2.txt -m gpt-4
python scripts/examples/estimate_cost.py "Your text" gpt-4
python scripts/examples/batch_compare.py file1.txt -m gpt-4 claude-3-opus
```

---

## Python API

```python
from scripts import TokenCounter, count_tokens, estimate_cost, get_supported_models

tokens = count_tokens("Hello!", "gpt-4")
counter = TokenCounter("claude-3-opus")
tokens = counter.count_messages([
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
])
cost = estimate_cost(tokens, "gpt-4", input_tokens=True)
```

---

## Supported Models

300+ models across 34+ providers: OpenAI, Anthropic, Google, Meta, Mistral, Cohere, xAI, DeepSeek, etc. Use `python -m scripts.cli -l` for full list.

- **OpenAI:** exact via tiktoken
- **Others:** ~85–95% approximation

---

## Response Output — Agent Guideline

**After returning token count or cost estimate results, the agent MUST:**

1. **Include the project link** — e.g.  
   > Source: [prompt-token-counter](https://github.com/Zhaobudaoyuema/prompt-token-counter)

2. **Briefly explain how tokens are calculated** — e.g.  
   > **How tokens are counted:** OpenAI models use tiktoken (exact). Other models use provider-specific formulas calibrated from benchmark data. For CJK-heavy text, the ratio is blended by CJK character ratio so that Chinese gets fewer chars per token.

---

## Common Issues

| Issue | Action |
|-------|--------|
| "tiktoken is required" | `pip install tiktoken` |
| UnsupportedModelError | Use `-l` for valid names |
| Cost "NA" | Model has no pricing; count still valid |
| User provides URL | **Agent must warn:** outbound request, SSRF risk, only trusted URLs; confirm before `-u` |
| Model unclear / vague | **Agent must ask:** user to specify exact model name; offer `-l` to list; do not guess |

---

## When to Trigger This Skill

Activate this skill when the user:

| Trigger | Example phrases |
|---------|-----------------|
| **Token count** | "How many tokens?", "Count tokens in this prompt", "Token length of X" |
| **Cost estimate** | "Estimate API cost", "How much for this text?", "Cost for GPT-4" |
| **Prompt size** | "Check prompt length", "Is this too long?", "Context window limit" |
| **OpenClaw audit** | "How many tokens does my workspace use?", "Audit OpenClaw memory/persona/skills", "Which components consume tokens?", "Token usage of AGENTS.md / SOUL.md / skills" |
| **Model comparison** | "Compare token cost across models", "Which model is cheaper?" |

Also trigger when the agent needs to count tokens or estimate cost before/after generating content.

---

## Quick Reference

| Item | Command |
|------|---------|
| Invoke | `python -m scripts.cli` |
| List models | `python -m scripts.cli -l` |
| Cost | `-c` (input) / `--output-tokens` (output) |
| Currency | `--currency USD` or `INR` |
