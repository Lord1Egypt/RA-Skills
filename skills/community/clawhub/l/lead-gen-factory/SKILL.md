---
# SKILL.md — lgf (Lead Gen Factory) skill for Claude Code and OpenClaw.
#
# Compatible with:
#   - Claude Code: auto-loaded from .claude/skills/lgf/SKILL.md
#   - OpenClaw:    publishable to ClawHub → `clawhub install lgf`
#
# The `name` field becomes the /slash-command trigger.
# The `description` field is the primary signal for auto-invocation by the AI.

name: lgf
description: >
  Run B2B lead research with lgf (Lead Gen Factory).
  Use when asked to find leads, prospect companies, research ICPs,
  find decision makers, or generate a lead list for any B2B target profile.
allowed-tools:
  - Bash
  - Read
  - Write
---

# lgf — Lead Gen Factory

A CLI pipeline that takes a free-text ICP (Ideal Customer Profile) and returns
a scored, deduplicated list of B2B leads as both CSV and structured JSON.

## Prerequisites

Install lgf once (requires Python 3.12+):

```bash
# From the repo root
pip install -e .

# Or via pipx for isolated install
pipx install git+https://github.com/Catafal/lead-gen-factory.git
```

Verify installation:

```bash
lgf doctor
```

Required API keys (set in `~/.lgf/.env`):
- `TAVILY_API_KEY` — web search
- `OPENROUTER_API_KEY` — LLM scoring + extraction

---

## Core Command

```bash
lgf research --icp-text "<your ICP>" --json 2>/dev/null
```

The `--json` flag outputs a structured JSON envelope to stdout — perfect for
AI agents to capture and process without touching the filesystem.
All human-facing progress output goes to stderr (suppressed with `2>/dev/null`).

---

## Usage Patterns

### 1. Quick inline ICP (most common)

```bash
lgf research --icp-text "HR Directors at SaaS companies in Spain, 50-500 employees" --json 2>/dev/null
```

### 2. ICP from file (for complex profiles)

```bash
lgf research --icp icp_examples/skillia_spain.md --json 2>/dev/null
```

### 3. Narrow with a focus constraint

```bash
lgf research --icp-text "Tech companies in Madrid" --focus "only companies hiring L&D managers" --json 2>/dev/null
```

### 4. Filter by minimum ICP score

```bash
lgf research --icp-text "..." --min-score 8 --json 2>/dev/null
```

### 5. Dry-run — see search queries only (no crawling, no LLM calls)

```bash
lgf research --icp-text "..." --dry-run
```

### 6. Check current config

```bash
lgf config
```

---

## JSON Output Schema

When `--json` is used, the envelope printed to stdout has this structure:

```json
{
  "leads": [
    {
      "business": "Acme Corp",
      "first": "Ana",
      "last": "García",
      "email": "ana.garcia@acme.com",
      "linkedin": "https://linkedin.com/in/anagarcia",
      "website": "https://acme.com",
      "phone": null,
      "date": "2026-03-09",
      "place_of_work": "Acme Corp, Madrid",
      "icp_fit_score": 9,
      "icp_fit_reason": "HR Director at 120-person SaaS, exact ICP match",
      "source_url": "https://acme.com/team"
    }
  ],
  "count": 1,
  "output_file": "leads_20260309.csv",
  "icp": {
    "target_roles": ["HR Director", "People Director"],
    "company_size_min": 50,
    "company_size_max": 500,
    "industries": ["SaaS", "Tech"],
    "geographies": ["Spain"],
    "min_fit_score": 7
  }
}
```

### Useful jq extractions

```bash
# All emails
lgf research --icp-text "..." --json 2>/dev/null | jq '.leads[].email'

# Count of leads found
lgf research --icp-text "..." --json 2>/dev/null | jq '.count'

# First lead's company + score
lgf research --icp-text "..." --json 2>/dev/null | jq '.leads[0] | {business, icp_fit_score}'

# Filter leads scoring 9+
lgf research --icp-text "..." --json 2>/dev/null | jq '[.leads[] | select(.icp_fit_score >= 9)]'

# LinkedIn URLs only
lgf research --icp-text "..." --json 2>/dev/null | jq '[.leads[].linkedin | select(. != null)]'
```

---

## Writing a Good ICP

Include:
- **Roles**: job titles of your decision makers (e.g. "HR Director", "L&D Manager", "CPO")
- **Company size**: employee range (e.g. "50-500 employees")
- **Industries**: sectors (e.g. "SaaS", "fintech", "consulting")
- **Geography**: countries or cities (e.g. "Spain", "Barcelona", "LATAM")
- **Signals** (optional): growth stage, tech stack, hiring activity

Example ICP text:
```
HR Directors and People Ops leads at B2B SaaS companies in Spain with 50-500 employees.
Focus on companies with active hiring in engineering or sales. Avoid BPO and consulting firms.
```

---

## All Available Commands

| Command | Purpose |
|---------|---------|
| `lgf research` | Full pipeline: search → crawl → extract → score → CSV |
| `lgf validate-icp` | Parse and display an ICP without running the pipeline |
| `lgf config` | Show effective configuration (API keys masked) |
| `lgf config set KEY VALUE` | Update a setting in `~/.lgf/.env` |
| `lgf profile list` | List saved ICP profiles |
| `lgf profile add <name>` | Save current ICP as a named profile |
| `lgf doctor` | Health check: API keys + live connectivity |
| `lgf init` | First-time setup wizard |

---

## Score Interpretation

| Score | Meaning |
|-------|---------|
| 8–10  | Strong ICP fit — prioritize these |
| 6–7   | Moderate fit — worth reviewing |
| < 6   | Weak fit — pipeline default filter |

Default min score is 7. Override with `--min-score`.
