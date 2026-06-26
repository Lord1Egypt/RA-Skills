# King's Watching (kingswatching)

AI Workflow Enforcer inspired by the Steam game **The King Is Watching**: just like how subjects in the game only work when the King's gaze is upon them, this tool ensures AI agents cannot cut corners and must execute every step to completion.

Turn natural language "1. 2. 3. 4." into machine-enforced workflows.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Forced Sequence** | Steps execute in strict order, no skipping allowed |
| **State Persistence** | Auto-saves execution state, supports resume from checkpoint |
| **Progress Reports** | Reports after each step, fully observable execution |
| **Flexible API** | Supports both decorator and chain-style APIs |
| **Task Translator** | Converts natural language to execution plans with auto-chunking |
| **Step Verification** | Prevents AI from cutting corners on every step |

## Quick Start

```python
from overseer import Overseer

# Create workflow
workflow = Overseer("my_analysis")

# Define steps
@workflow.step("Search Information")
def search(ctx):
    query = ctx.get("query")
    return kimi_search(query)

@workflow.step("Analyze Results")
def analyze(ctx):
    data = ctx.get_step_result("Search Information")
    return llm_analyze(data)

# Execute (enforced sequential order)
workflow.run(query="AI industry trends")
```

Output:
```
📋 Workflow: my_analysis
⏳ Step 1/2: Search Information...
✅ Step 1/2 Complete: Contains fields: query, results, count

⏳ Step 2/2: Analyze Results...
✅ Step 2/2 Complete: Contains 3 key findings

🎉 All Complete!
```

## Natural Language Execution (Recommended)

```python
from overseer import translate_and_run

# One-liner starts complete workflow
result = translate_and_run("Download 100 photochemistry research reports")

# Auto splits into 10 steps, each verified
# No cutting corners possible
```

## Installation

```bash
# Copy to skills directory
cp -r kingswatching /path/to/openclaw/skills/

# Usage
from overseer import Overseer, translate_and_run
```

## The Story Behind

*The King Is Watching* is a roguelite kingdom builder on Steam. Your subjects only work when your gaze is upon them. Look away, and they slack off immediately.

AI agents do the same. Ask for "100 reports", get 14. King's Watching ensures you get exactly what you asked for.

## Use Cases

- ✅ Complex multi-step tasks (research, reporting, data processing)
- ✅ Scenarios requiring strict sequential execution
- ✅ Auditable, recoverable execution processes
- ✅ Long workflows needing progress visibility
- ✅ Preventing AI from cutting corners on large tasks

## Relationship with Workflow Engine

```
┌─────────────────────────────────────────┐
│           Workflow Engine               │
│  (Declarative - YAML defined)           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│           Overseer                      │
│  (Imperative - Enforced execution)      │
└─────────────────────────────────────────┘
```

Workflow Engine defines "what to do" with YAML. King's Watching ensures "strictly follow the definition". Together: Declarative orchestration + Enforced execution + Checkpoint resume.

## License

MIT
