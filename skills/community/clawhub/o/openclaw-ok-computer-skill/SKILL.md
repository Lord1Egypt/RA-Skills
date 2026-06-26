---
name: ok-computer-swarm
description: |
  Spawn multiple sub‑agents to perform concurrent research on a list of topics,
  inspired by Kimi.com’s OK Computer and Agent Swarm features【453334500861599†L40-L99】.  Each
  sub‑agent performs a DuckDuckGo search for its assigned topic and returns the
  top results.  When all sub‑agents finish, the skill aggregates their
  findings into a single structured report.  Use this skill for broad,
  multi‑topic research where parallel exploration saves time.
user-invocable: true
metadata:
  moltbot:
    emoji: "🧠"
    requires:
      bins: ["python"]
    homepage: https://www.grahammiranda.com/
---

# OK Computer Swarm

## Overview

This skill lets OpenClaw emulate the “100 sub‑agents” style of Kimi’s Agent Swarm【453334500861599†L40-L99】.  When you need to research several topics at once, the skill
spins up lightweight sub‑agents that fetch the top web results via DuckDuckGo.  By running these tasks in parallel, the skill reduces overall waiting time and surfaces a diverse set of sources.

## Commands

### `/ok-computer-swarm search`

Run concurrent searches for multiple topics.

**Inputs**

- `query` (string, repeated):  One or more search phrases.  You can provide multiple `query` flags to search many topics at once.  At least one `query` is required.

**Example**

```bash
python scripts/swarm_search.py --query "Agent Swarm" --query "OpenClaw skills"
```

**Output**

The script prints a JSON array where each element corresponds to a search query.  Each element contains the original query and an array of result objects (title and URL).  The format is easy for downstream agents to parse and can be further processed or summarised.

## When to use this skill

Use `ok-computer-swarm` whenever you need to gather high‑level information on multiple topics concurrently.  It is ideal for:

- Broad research tasks that involve several different subjects.
- Generating a starting point for more in‑depth analysis.
- Situations where time is critical and sequential research would be too slow.

## Limitations

- The skill uses DuckDuckGo’s free API; results may be less comprehensive than paid search APIs.
- It performs minimal summarisation.  Consider integrating additional summarisation or reading tools if you need deeper insights.

---
