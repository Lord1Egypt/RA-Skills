---
name: compression-monitor
description: >-
  Detect behavioral drift in persistent AI agents after context compression events.
  Use when a long-running agent has compressed its context (compaction, truncation, or
  summarization) and you need to verify the agent is still behaving consistently.
  Measures three observable signals without requiring access to the agent's internals:
  ghost lexicon decay (loss of precise vocabulary), context consistency score (CCS via
  embedding similarity), and tool call distribution shift. Includes ready-to-use
  framework integrations for smolagents, Semantic Kernel, LangChain/DeepAgents, CAMEL,
  and the Anthropic Agent SDK. Triggers on: "context compression", "compaction",
  "agent drift", "behavioral drift", "ghost lexicon", "CCS", "context consistency",
  "did my agent change", "compression boundary", "long-running agent", "persistent agent
  drift", "context window rotation", or any task involving verifying agent behavioral
  consistency across session boundaries.
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://github.com/agent-morrow/compression-monitor
---

# Compression Monitor

Detect when a persistent AI agent has silently changed behavior after context compression.

## The Problem

Agents compress their history when context fills up. After compression, the agent continues running but may have silently lost:

- Precise vocabulary ("ghost terms") that anchored its reasoning
- Risk constraints or compliance anchors present at session start
- Tool call patterns and behavioral tendencies from earlier in the session

The agent reports no change. Benchmarks don't catch it. The behavior is different.

## Three Measurement Signals

```
ghost_lexicon.py     → vocabulary decay: which precise terms vanished post-compaction?
behavioral_probe.py  → active probing: query before/after compression, score semantic shift
ccs_harness.py       → CCS benchmark: full Constraint Consistency Score run (mock or live)
```

All three are output-only — no instrumentation inside the agent or model required.

## Quick Start

```bash
# Run a CCS benchmark (no API key required in mock mode)
python ccs_harness.py --mock

# Check ghost term decay in a session log
python ghost_lexicon.py --before pre_session.txt --after post_session.txt

# Active probe: query agent before and after a compaction event
python behavioral_probe.py --agent-url http://localhost:8080 --probe-file probes.json
```

## Framework Integrations

Ready-to-use wrappers for existing agent frameworks — no changes to the framework required:

| Framework | Module | Integration Point |
|-----------|--------|------------------|
| smolagents | `smolagents_integration.py` | `step_callbacks` — detects consolidation via history-length delta |
| Semantic Kernel | `semantic_kernel_integration.py` | `ChatHistorySummarizationReducer` / `ChatHistoryTruncationReducer` wrappers |
| LangChain/DeepAgents | `deepagents_integration.py` | Filesystem-based compaction detection |
| CAMEL | `camel_integration.py` | ChatAgent truncation boundary hook |
| Anthropic Agent SDK | `sdk_compaction_hook_demo.py` | `OnCompaction` hook pattern |

### smolagents example

```python
from smolagents import CodeAgent, HfApiModel
from smolagents_integration import BehavioralFingerprintMonitor

agent = CodeAgent(tools=[], model=HfApiModel())
monitor = BehavioralFingerprintMonitor(
    agent=agent,
    history_drop_threshold=5,
    verbose=True
)
result = agent.run("Your long-horizon task...")
print(monitor.report())
# → CCS: 0.87 | Ghost terms: 2 | Tool call drift: 0.12
```

## Interpreting Results

| CCS Score | Interpretation |
|-----------|---------------|
| > 0.90 | Minimal drift — agent behaving consistently |
| 0.75–0.90 | Moderate drift — worth investigating |
| < 0.75 | Significant drift — verify critical constraints still active |

Ghost term count > 0 is a flag, especially for domain-specific terms that anchor constraints (risk parameters, compliance anchors, operational rules).

## When to Use This Skill

- You have a long-running agent that performs compaction or context rotation
- You want to verify an agent's behavioral consistency after a session boundary
- You need a measurement layer alongside your memory system (retrieval accuracy ≠ behavioral consistency)
- You want to instrument a specific framework's compaction boundary without modifying it

## Source

- GitHub: https://github.com/agent-morrow/compression-monitor
- Companion article: https://morrow.run/posts/compression-monitor-memory-taxonomy.html
- The third failure class: https://morrow.run/posts/the-third-memory-bottleneck.html
