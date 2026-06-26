-----

## name: memtrap
description: “🧠 MemTrap — The LM-Eval-Harness for agent memory integrity. Score your agent’s memory resistance against DeepMind AI Agent Traps + OWASP ASI06 before attackers exploit them. Runs the official ATRS (Agent Trap Resistance Score) benchmark: DeepMind 6 Traps (SSRN 6372438) + OWASP ASI06 Memory & Context Poisoning. Returns a 0–100 resistance score, per-category breakdown, automatic OWASP hardening, and a verifiable community badge. Use when: testing agent memory security, benchmarking RAG store resistance, hardening LangGraph or CrewAI memory, checking OWASP ASI06 compliance, or any time the user asks if their agent memory is safe, poisonable, or production-ready.”
version: 0.1.0
metadata:
openclaw:
emoji: “🧠”
homepage: https://github.com/shaymizuno/memtrap
requires:
bins:
- python3
install:
- id: pip-atrs
kind: pip
packages:
- memtrap
bins:
- python3
label: “Install MemTrap (pip install memtrap)”

# 🧠 MemTrap — Agent Trap Resistance Score (ATRS)

The open benchmark standard for agent memory integrity. Hunt DeepMind memory traps + OWASP ASI06 before they hunt you.

**“The LM-Eval-Harness for agent memory integrity.”**

## What gets tested

**DeepMind 6 Traps** — SSRN 6372438, March 2026:

- Content Injection, Semantic Manipulation, Cognitive State (RAG poisoning)
- Behavioral Control, Systemic, Human-in-the-Loop

**OWASP ASI06** — Top 10 Agentic Applications 2026:

- RAG store poisoning, long-term context drift, policy corruption, cross-session leakage

## Score your memory (benchmark mode)

```python
from memtrap import MemTrap

atrs = MemTrap(mode="benchmark")
result = atrs.run_benchmark(context="your_memory_context")

print(f"ATRS Score: {result.atrs_score}/100")
for category, score in result.category_scores.items():
    icon = "✅" if score >= 70 else "⚠️" if score >= 40 else "❌"
    print(f"  {icon} {category}: {score}/100")
print(f"\n→ {len(result.hardening_recommendations)} hardenings recommended")
print(f"→ Badge: {result.badge_url}")
```

## Protect your memory store (active mode)

```python
from memtrap import MemTrap

atrs = MemTrap(mode="active", frameworks=["langgraph", "crewai"])
agent.memory = atrs.wrap_memory(agent.memory, context="research_memory")
# Applies OWASP Agent Memory Guard patterns automatically:
# provenance tracking, trust scoring, quarantine, rollback
```

## LangGraph drop-in

```python
from langgraph.checkpoint.memory import MemorySaver
from memtrap import MemTrap

class ATRSMemorySaver(MemorySaver):
    def __init__(self, context: str):
        super().__init__()
        self._atrs = MemTrap(mode="benchmark")
        self._ctx = context

    async def aget(self, config):
        raw = await super().aget(config)
        return self._atrs.wrap_memory(raw, self._ctx) if raw else None

graph.checkpointer = ATRSMemorySaver("long_term_research")
```

## CrewAI drop-in

```python
from memtrap import MemTrap

def protect_crew(crew, context="crew_memory"):
    atrs = MemTrap(mode="active")
    if hasattr(crew, "memory"):
        crew.memory = atrs.wrap_memory(crew.memory, context)
    return crew
```

## Score interpretation

|Score |Verdict    |Action                               |
|------|-----------|-------------------------------------|
|80–100|✅ Resistant|Re-test after model or memory updates|
|60–79 |⚠️ Moderate |Apply recommended hardenings         |
|40–59 |🔶 High risk|Harden before production             |
|0–39  |❌ Critical |Memory is actively exploitable now   |

## Submit to the public leaderboard

```bash
memtrap submit --context your_memory_context
```

Get a verifiable badge for your repo. See where your stack ranks against the community.
Leaderboard → https://github.com/shaymizuno/memtrap#leaderboard

## Why this exists

Memory poisoning (OWASP ASI06) is the #1 persistent threat to agentic systems in 2026.
Once poisoned, the damage survives across sessions and users.
Existing tools detect. ATRS **measures resistance** and **fortifies** automatically.

Sources:

- DeepMind paper: https://ssrn.com/abstract=6372438
- OWASP ASI06: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP Agent Memory Guard: https://owasp.org/www-project-agent-memory-guard/

Zero telemetry. Community-governed. MIT license. Advisory Board open to contributors.
