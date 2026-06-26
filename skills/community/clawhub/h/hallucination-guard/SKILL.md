---
name: hallucination-guard
description: "Detect and prevent AI agent hallucinations during task execution. Use when: (1) an agent claims to have created files, commits, or artifacts — verify them, (2) an agent produces data reports or numbers — audit against source, (3) running long multi-step tasks where fabrication risk is high, (4) you need cross-model verification of critical outputs. Provides 4-layer defense: L0 context hygiene, L1 claim-evidence protocol, L2 cross-model audit, L3 drift detection. NOT for: simple Q&A, opinion-based tasks, or conversations where factual accuracy is not critical."
---

# Hallucination Guard

4-layer defense against agent fabrication. Each layer is independent — use one or combine.

## When Hallucinations Happen

Highest risk conditions (apply more layers when these are present):
- Extended sessions (>50 turns or >30min continuous work)
- Tasks involving file creation, code, git, or data analysis
- Agent reporting quantitative results (numbers, metrics, PnL)
- Multiple sequential "successes" with no errors or retries

## Layer 0: Context Hygiene (Prevention)

Reduce hallucination probability before it starts.

**For long tasks (>10 steps):**
1. Break into segments of ≤8 steps each
2. Between segments: flush working state to a file, reload from file (not from in-context memory)
3. Each segment starts with `read` of the state file — never trust carried-over context for facts

**For data-intensive tasks:**
- Load source data from files at point of use, not from earlier context
- If a number was mentioned 20+ turns ago, re-read the source before citing it

**Cost: Zero.** This is a workflow discipline, not an API call.

## Layer 1: Claim-Evidence Protocol (Detection)

Every agent claim of physical action must include tool-verified evidence.

### The Rule

```
CLAIM:    "I created/modified/committed X"
EVIDENCE: Tool output proving X exists and matches the claim
STATUS:   VERIFIED (evidence confirms) or UNVERIFIED (no evidence yet)
```

### Verification Commands by Claim Type

| Claim | Verify With |
|-------|-------------|
| Created file | `ls -la {path} && head -20 {path}` |
| Modified file | `grep -n '{expected_content}' {path}` |
| Git commit | `git log --oneline -3` |
| Git push | `git log --oneline origin/{branch} -3` |
| Ran tests | Show actual test output (pass AND fail counts) |
| API response | Show raw response body |
| Data analysis | Show `wc -l` of source + sample rows |

### Red Flags (claim likely fabricated)

- Claim references a file but no `read`/`exec` tool was called
- Exact round numbers in data (187 trades, +$126.50) without source
- "All tests passed" with no test output shown
- Multiple consecutive successes with zero errors

**Cost: ~50 tokens per claim.** One `exec` call per physical claim.

## Layer 2: Cross-Model Audit (Verification)

Spawn a second agent (different model) to independently verify claims.

### When to Use

- Critical outputs: financial reports, deployment decisions, data analysis
- When L1 evidence exists but numbers need independent validation
- After any task where the agent reported unusually perfect results

### How to Run

See [references/audit-prompt.md](references/audit-prompt.md) for the spawn template.

Key principles:
1. Auditor receives ONLY the evidence (files, outputs) — not the original agent's conclusions
2. Auditor independently extracts facts from evidence and compares to claims
3. Auditor uses the cheapest model that can do the verification (flash for file checks, sonnet for logic)

**Cost: 1 subagent spawn.** Use flash/gemini for simple checks (~$0.001). Reserve sonnet/opus for complex logic verification.

## Layer 3: Drift Detection (Monitoring)

Monitor long-running agent tasks for hallucination patterns.

### When to Use

- Tasks expected to take >15 minutes
- Agent is working autonomously (coding agent, research agent)
- High-stakes tasks where undetected fabrication causes real damage

### Setup

See [references/drift-monitor.md](references/drift-monitor.md) for implementation.

Core signals:
- **Claim/Tool Ratio**: If claims > 3× tool calls → alert
- **Zero-Error Streak**: 8+ consecutive "successes" with 0 errors → suspicious
- **Phantom References**: Agent references files/branches never created → critical alert

**Cost: Periodic check via `sessions_history`.** No extra model calls unless alert triggers.

## Choosing Layers

| Scenario | Recommended |
|----------|-------------|
| Quick file creation | L1 only |
| Data report from CSV | L0 + L1 |
| Multi-step coding task | L0 + L1 + L2 |
| Autonomous long-running agent | All four layers |
| Routine conversation | None needed |

## Integration with Other Skills

- **War Room**: Add L1 verification to each agent's output (verify cited data)
- **Coding agents**: Wrap with L3 drift monitor for long sessions
- **Any task with `sessions_spawn`**: Add L2 audit as a final verification step

## References

- [references/audit-prompt.md](references/audit-prompt.md) — Cross-model audit spawn template
- [references/drift-monitor.md](references/drift-monitor.md) — Drift detection implementation
- [references/taxonomy.md](references/taxonomy.md) — Hallucination types with real-world examples
