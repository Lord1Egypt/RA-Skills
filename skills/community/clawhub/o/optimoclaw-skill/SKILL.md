# OptimoClaw Token Optimizer

Token optimization advisor for OpenClaw agents. Reads your live config and session data, identifies where tokens are being wasted, and recommends specific changes with rate card math, cost trade-offs, and the exact commands to apply them.

**Source:** https://github.com/Marc4211/optimoclaw | **Author:** Marc Scibelli | **License:** MIT

## Requirements

- **OpenClaw CLI** (`openclaw`) must be installed and available in PATH on the machine where this skill runs.
- This skill reads configuration and session data via the OpenClaw CLI. The outputs may contain **profile names, model identifiers, and gateway connection details**. No API keys are exposed in the commands used below — `config get 'agents'` returns agent configuration (models, heartbeat settings, thresholds), and `status --usage` returns token counts and session metadata.
- This skill does **not** automatically apply changes. All `openclaw config set` commands are presented as recommendations for the user to review and execute.

## What you do

You help users understand and reduce their OpenClaw token spend by:
- Reading their live configuration and session data via the `openclaw` CLI
- Identifying which settings are costing the most
- Recommending specific config changes with clear trade-offs
- Explaining *why* a change helps, not just *what* to change

## How to gather data

Before making recommendations, collect the user's actual configuration:

```bash
# Get the full agents config (models, heartbeat, defaults)
openclaw config get 'agents' --json

# Get live session data (token usage, cache ratios, context utilization)
openclaw status --usage --json
```

If the user has a named profile, use `openclaw --profile '<name>'` before each command.

Read both outputs carefully before advising. Never guess — use the real numbers.

**What these commands return:** Agent names, assigned models, heartbeat frequency, compaction settings, session token counts, cache ratios, and context utilization percentages. They do not return API keys, billing credentials, or authentication tokens.

## Rate card ($/million tokens)

Use these rates to calculate costs. All prices are per million tokens.

### Anthropic
| Model | Input | Cache Read | Output |
|---|---|---|---|
| Claude Opus 4.6 | $5.00 | $0.50 | $25.00 |
| Claude Opus 4.5 | $5.00 | $0.50 | $25.00 |
| Claude Opus 4.1 | $15.00 | $1.50 | $75.00 |
| Claude Opus 4 | $15.00 | $1.50 | $75.00 |
| Claude Sonnet 4.6 | $3.00 | $0.30 | $15.00 |
| Claude Sonnet 4.5 | $3.00 | $0.30 | $15.00 |
| Claude Sonnet 4 | $3.00 | $0.30 | $15.00 |
| Claude Haiku 4.5 | $1.00 | $0.10 | $5.00 |
| Claude 3.5 Haiku | $0.80 | $0.08 | $4.00 |
| Claude 3 Haiku | $0.25 | $0.03 | $1.25 |

### OpenAI
| Model | Input | Cache Read | Output |
|---|---|---|---|
| GPT-5.4 | $2.50 | $0.25 | $15.00 |
| GPT-5.4 Mini | $0.75 | $0.075 | $4.50 |
| GPT-5.4 Nano | $0.20 | $0.02 | $1.25 |
| GPT-5.4 Pro | $30.00 | $30.00 | $180.00 |
| GPT-4.1 | $2.00 | $0.50 | $8.00 |
| GPT-5.3 Codex | $1.75 | $0.175 | $14.00 |

### Local (Ollama)
All local models: **$0** for all token types.

## The 10 optimization levers

These are the settings you can recommend changing. Each has a config path for `openclaw config set`.

### Model Routing (which models handle what)

**1. Default Model** — `agents.defaults.model.primary`
The fallback model for all tasks. This is the baseline cost driver.
- Sonnet is a good default for most setups
- Haiku if most work is routine
- Reserve Opus for specific tasks, not as a default
- Also determines maximum context window size (Haiku caps at 200K, Sonnet/Opus support larger)

**2. Heartbeat Model** — `agents.defaults.heartbeat.model`
Model for routine check-ins. Heartbeats run frequently and don't need to be smart.
- One of the highest single-lever cost wins available
- A local or cheap model here can save $5–15/month depending on frequency
- Only use a stronger model if heartbeat logic makes real judgment calls

**3. Compaction Model** — `plugins.entries.lossless-claw.config.summaryModel`
Model that compresses conversation history into summaries. Runs in the background.
- Doesn't need to be your best model — just needs to summarize accurately
- Haiku or a local model works well for most setups

### Frequency & Volume (how often and how much)

**4. Heartbeat Frequency** — `agents.defaults.heartbeat.every`
How often agents check in. Options: `off`, `15m`, `30m`, `60m`
- Direct multiplier on heartbeat cost — halving frequency roughly halves heartbeat spend
- 30 minutes is the sweet spot for most setups
- Go lower (15m) for time-sensitive workflows, higher (60m) if cost is priority

**5. Subagent Concurrency** — `agents.defaults.subagents.maxConcurrent`
How many subagents run simultaneously. Range: 1–10.
- Higher = faster parallel work but more simultaneous API calls
- Can cause cost spikes or rate limit errors if too high
- Raise for research-heavy parallel workflows, lower if hitting rate limits

**6. Search Batch Limit** — `agents.defaults.searchBatchLimit`
Max web searches per batch before a cooldown. Range: 1–20.
- Uncapped search is one of the easiest ways to run up a bill
- 5 searches per batch works well for most research tasks

**7. Rate Limit Delay** — `agents.defaults.rateLimitDelay`
Minimum seconds between consecutive API calls. Range: 1–15.
- 5 seconds is a safe default
- Reduce to 2–3 for time-sensitive work with a higher-tier API plan
- Increase if hitting 429 errors

### Context & Memory (how much gets loaded)

**8. Session Context Loading** — `agents.defaults.sessionContextLoading`
Which files load at session start. Options: `lean`, `standard`, `full`
- One of the largest hidden cost drivers in OpenClaw
- Full loading can 3–5× your input token cost per call vs lean
- Lean (identity, soul, today's memory) works for most sessions
- Full only needed when agents need deep historical context

**9. Memory File Scope** — `agents.defaults.memoryFileScope`
Days of daily memory files loaded per session. Range: 1–30.
- Direct multiplier on input token cost (~3K tokens per day of memory files)
- 7 days is a good default
- 3 days if cost is priority
- 30+ only for agents that reference historical decisions regularly

**10. Compaction Threshold** — `agents.defaults.compaction.threshold`
Token count before conversation history gets compressed. Range: 20K–200K.
- Lower = more aggressive compaction = smaller context = lower cost
- Higher = more history preserved = richer context = higher cost
- If agents forget things mid-session, raise it
- If costs are high and context quality isn't a concern, lower it
- Works with LosslessClaw plugin for intelligent summarization

## Optimization profiles

When the user wants a quick preset, recommend one of these:

### Lean (minimize cost)
- Heartbeat Frequency: Every 60 min
- Compaction Threshold: 50K tokens
- Subagent Concurrency: 1
- Session Context Loading: Lean
- Memory File Scope: 3 days
- Rate Limit Delay: 8 sec
- Search Batch Limit: 3

### Balanced (cost and quality)
- Heartbeat Frequency: Every 30 min
- Compaction Threshold: 100K tokens
- Subagent Concurrency: 2
- Session Context Loading: Standard
- Memory File Scope: 7 days
- Rate Limit Delay: 5 sec
- Search Batch Limit: 5

### Quality (maximize capability)
- Heartbeat Frequency: Every 15 min
- Compaction Threshold: 150K tokens
- Subagent Concurrency: 4
- Session Context Loading: Full
- Memory File Scope: 30 days
- Rate Limit Delay: 2 sec
- Search Batch Limit: 10

## How to analyze session data

When you have `openclaw status --usage --json` output, look at:

### Cache efficiency
- **Cache reads** (cheapest — 10% of input cost): Higher is better
- **Cache writes** (1.25× input cost): High ratio is normal for new sessions, concerning if persistent
- **>90% cache reads**: Excellent, nothing to change
- **60–90% reads**: Good, improves naturally as sessions stay alive
- **>20% writes**: Likely transient if sessions are new. If persistent, Session Context Loading and Memory File Scope control how much gets written per session start, and Heartbeat Frequency controls restart frequency
- **<40% reads**: Normal right after session starts, shifts toward reads as conversations mature

### Context utilization
- **<15% used**: Normal for new/short sessions, nothing to change
- **15–40%**: Optimal — healthy headroom for growth
- **40–75%**: Good — can tune Compaction Threshold if needed
- **75–90%**: Lower the Compaction Threshold to summarize earlier
- **90%+**: Lower Compaction Threshold AND reduce Heartbeat Frequency to slow context accumulation
- **Large windows barely used**: The model determines window size. If sessions don't need extended context, switching to Haiku caps the window at 200K and reduces per-write cost

## How to give recommendations

Always follow this pattern:

1. **State what you see** — cite the actual numbers from their config/sessions
2. **Explain the cost impact** — use the rate card to show what it costs
3. **Recommend a specific change** — name the exact setting and the new value
4. **Explain the trade-off** — what improves and what might be affected
5. **Give the command** — provide the exact `openclaw config set` command to make the change

Example:
> Your heartbeat model is set to Claude Opus 4.6 ($5/MTok input, $25/MTok output) running every 15 minutes across 3 agents. That's roughly 288 heartbeat calls per day at ~2K tokens each — about $4.32/day just on heartbeats.
>
> Switching to Haiku 4.5 ($1/$5) drops that to $0.86/day — saving ~$100/month. Heartbeats just check task queues; they don't need Opus-level reasoning.
>
> ```bash
> openclaw config set 'agents.defaults.heartbeat.model' 'anthropic/claude-haiku-4-5'
> ```
>
> Trade-off: If your heartbeat logic does complex analysis, quality may drop slightly. For standard check-ins, you won't notice a difference.

## Rules

- Never fabricate numbers. If you don't have session data, ask the user to run the status command.
- Always show your math when estimating costs.
- Be honest about trade-offs — cheaper isn't always better.
- If a setting is already optimal, say so. Don't recommend changes for the sake of it.
- If there's no lever for something (e.g., context window size is model-determined), say that clearly instead of leaving the user without an answer.
- Local/Ollama models are always $0 — recommend them for heartbeat and compaction when available.
- Per-agent overrides exist. If a specific agent has different settings from the defaults, note that and address both levels.
