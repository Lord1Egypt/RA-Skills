---
name: openclaw-insight
description: |
  Analyze OpenClaw AI assistant usage patterns and generate interactive insight reports.
  Trigger when users ask about: OpenClaw usage stats, session analytics, token consumption,
  cost estimation, friction analysis, optimization suggestions, or any request to audit/visualize
  OpenClaw session data (e.g. "show my stats", "how much am I spending on AI", "usage report").
---

# OpenClaw Insight — Usage Guide

> CLI tool that analyzes local OpenClaw session history and generates interactive reports with usage statistics, behavior patterns, friction analysis, and improvement suggestions. **100% local — no data leaves your machine.**

## Installation

### One-Click Install (Recommended)

Use the official one-click installation script:

```bash
curl -fsSL https://raw.githubusercontent.com/linsheng9731/openclaw-insight/main/install.sh | bash
```

This script will automatically:
1. Detect your operating system and architecture
2. Download the appropriate binary release
3. Verify the integrity of the downloaded file
4. Install it in a suitable location ($HOME/.local/bin by default)
5. Make the command available in your PATH

### Install Specific Version

To install a specific version (e.g., v1.0.0):

```bash
curl -fsSL https://raw.githubusercontent.com/linsheng9731/openclaw-insight/main/install.sh | bash -s -- --version v1.0.0
```

### From Source

For development or if you want to build from source:

```bash
git clone https://github.com/linsheng9731/openclaw-insight.git
cd openclaw-insight
npm install && npm run build
```

## CLI Usage

```bash
# Default: analyze last 30 days, open HTML report in browser
openclaw-insight

# Analyze last 7 days
openclaw-insight --days 7

# JSON output
openclaw-insight --format json --output report.json

# Specific agent + custom output
openclaw-insight --agent my-agent --output ~/Desktop/insight.html

# Verbose, no auto-open
openclaw-insight --verbose --no-open
```

### Options

| Option | Default | Description |
|---|---|---|
| `-d, --days <n>` | `30` | Number of days to analyze |
| `-m, --max-sessions <n>` | `200` | Maximum sessions to process |
| `-a, --agent <id>` | auto-detect | Agent ID to analyze |
| `-s, --state-dir <path>` | `~/.openclaw` | OpenClaw state directory |
| `-o, --output <path>` | `~/.openclaw/usage-data/report.html` | Output file path |
| `-f, --format <fmt>` | `html` | Output format: `html` or `json` |
| `--no-open` | — | Don not auto-open the report in browser |
| `-v, --verbose` | — | Enable verbose output |

## What the Report Includes

### Usage Statistics
- **Sessions**: total count, daily average, activity streaks
- **Tokens**: input/output breakdown, cache hit rates, cost estimation
- **Temporal**: daily activity charts, peak hours identification
- **Channels**: per-channel session counts and token efficiency
- **Models**: model diversity, per-model cache performance

### Behavior Patterns
Automatically detects: peak hours, channel preferences, session duration profiles, cache utilization efficiency, model diversity, and tool usage preferences. Each pattern has an impact level (high / medium / low).

### Friction Events
Identifies pain points in your sessions:

| Type | Description |
|---|---|
| `high_token_waste` | Excessive output relative to input |
| `excessive_compactions` | Repeatedly hitting context window limits |
| `abandoned_session` | Started but barely used sessions |
| `underutilized_cache` | Large sessions with zero cache hits |
| `context_overflow` | Repeated context window exhaustion |
| `single_message_sessions` | One-shot interactions with high overhead |

### Improvement Suggestions
Prioritized recommendations across these categories:
- **Token Efficiency** — cache optimization, verbosity control, batching
- **Channel Optimization** — multi-channel access, per-channel efficiency
- **Model Selection** — routing simple tasks to cheaper models
- **Context Management** — conversation splitting, token budgets
- **Scheduling** — usage pattern optimization
- **Memory Utilization** — cross-session context retention
- **Feature Discovery** — underused OpenClaw capabilities
- **Workflow Improvement** — conversation depth, specification clarity

Each suggestion includes impact, effort, detailed explanation, and optional config snippets.

## Data Sources

The tool reads from OpenClaw local state directory (read-only, never modifies data):

```
~/.openclaw/
  agents/{agentId}/
    sessions/
      sessions.json          # Session metadata index
      {sessionId}.jsonl      # Per-session conversation transcripts
```

## JSON Output Structure

When using `--format json`, the report contains:

```
InsightReport {
  generatedAt, periodStart, periodEnd, daysAnalyzed,
  summary        — aggregate stats (sessions, tokens, cost, streaks, etc.)
  dailyActivity  — per-day breakdown
  hourlyDistribution — 24-hour activity heatmap
  channelStats   — per-channel metrics
  modelStats     — per-model metrics
  sessionAnalyses — detailed per-session data
  patterns       — detected behavior patterns
  frictions      — friction events
  suggestions    — improvement recommendations
}
```

## Common Scenarios

| User Request | Command |
|---|---|
| Show my stats | `openclaw-insight` |
| How much am I spending? | `openclaw-insight --format json` then read `summary.estimatedCostUsd` |
| Why are my sessions slow? | Run analysis then focus on friction events |
| Compare my channels | Run analysis then present `channelStats` |
| Report for last week | `openclaw-insight --days 7` |
| How can I use OpenClaw better? | Run analysis then present top suggestions |

## Troubleshooting

| Problem | Fix |
|---|---|
| No agents found | Verify `~/.openclaw` exists and contains agent data |
| No sessions in last N days | Increase `--days` value |
| Empty channel/model stats | OpenClaw version may be too old |
| Build errors | Upgrade to Node.js >= 22 |

## Development

```bash
npm install          # Install dependencies
npm run build        # Build
npm run dev          # Development mode
npm test             # Run tests
npm run clean        # Clean build artifacts
```
