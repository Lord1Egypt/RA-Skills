# Orchestration Policy

## Contents

1. Decomposition
2. Agent-count allocation
3. Model routing
4. Common task patterns

## Decomposition

Build a small directed acyclic graph before spawning:

- **Critical path:** the next required action. Keep it with the main agent.
- **Reasoning sidecar:** independent analysis that can return after the main path advances.
- **Mechanical lane:** deterministic and scriptable; do not spawn.
- **I/O lane:** batch with tools; do not spawn.
- **Integration node:** always main-agent owned.
- **QA node:** starts only after the integrated build is frozen.

A good agent lane has one objective, one ownership boundary, one output contract, and one stop condition.

Reject a lane when:

- the main agent needs its answer before doing anything else;
- it duplicates another lane;
- it only reads many files or runs many searches;
- it edits the same file as another active lane;
- it cannot be evaluated independently.

## Agent-Count Allocation

Use the smallest count that covers independent judgment:

| Independent reasoning lanes | First wave |
|---:|---:|
| 0 | 0 agents |
| 1 | 1 sidecar at most |
| 2 | 2 agents |
| 3 or more | 3 agents |

After integration, use 0–2 QA agents. Hard cap the whole run at 5.

Map user intent as follows:

- **"省时间" / deadline:** shorten the critical path and increase safe concurrency up to the cap.
- **"不用省 token":** broaden independent evidence coverage, not context duplication.
- **"准确度100%":** add deterministic gates and source requirements; do not promise literal certainty.
- **"多多多派":** use every genuinely independent lane up to the cap; never invent lanes.

## Model Routing

Route by cognitive requirement rather than prestige:

- **Fast model, low/medium reasoning:** inventory, file localization, bounded comparison, visual checklist.
- **Balanced model, medium/high reasoning:** scoped research, source audit, isolated implementation.
- **Frontier model, high reasoning:** legal/investment judgment, architecture, conflict resolution.
- **Main agent:** synthesis and final write ownership.

Avoid xhigh reasoning for mechanical checks. A smaller context usually improves both speed and reliability more than a larger model improves a duplicated task.

## Common Task Patterns

### Research

Wave one: source discovery, source validation, analytical framework. Main agent synthesizes. QA: factual consistency and audience logic.

### Coding

Wave one: disjoint modules or one implementation plus one test-design sidecar. Main agent owns integration. QA: tests and regression review.

### Decks and documents

Wave one: evidence, content architecture, data sync. Main agent writes the artifact. Scripts check layout and structure. QA: visual quality and decision logic.

### Legal or diligence

Wave one: commercial terms, legal risk, financial evidence. Main agent owns negotiation posture and final conclusions. QA: citation and internal consistency.
