---
name: llm-as-judge
description: Cross-model verification for complex tasks. Spawn a judge subagent with a different model to review plans, code, architecture, or decisions before execution. Use when working on "architecture", "system design", "complex feature", "security review", "production deployment", financial/trading systems, or when stuck after 3+ attempts. NOT for simple edits, config changes, or routine tasks.
---

# LLM-as-Judge

**Core principle:** Same model = same blind spots. Different model = fresh perspective. Cross-model review catches ~85% of issues vs ~60% for self-reflection.

## Activation Criteria

**Use this pattern when:**
- Architecture or system design decisions
- Multi-file changes affecting >5 files or >500 LOC
- Security-critical code (auth, payments, crypto/DeFi)
- Financial/trading systems (market making, quant strategies)
- Planning documents that will drive weeks of work
- Stuck after 3+ failed attempts on same problem

**Skip when:**
- Simple edits, config tweaks, bug fixes with obvious cause
- Documentation updates
- Single-file changes under 100 LOC
- Tasks where self-review is sufficient

## The Pattern

```
Executor (Model A) → Output → Judge (Model B) → Verdict → Action
```

**Verdicts:** APPROVE | REVISE (with specific feedback) | REJECT (restart)

## Model Pairing

Use a different provider than the executor to avoid shared blind spots:

- **Executor: Claude** → Judge: `kimi` or `grok` or `gemini-pro`
- **Executor: Kimi/Gemini** → Judge: `opus`
- **Principle:** Different provider, similar capability tier

## Judge Prompt Templates

### Plan/Architecture Review
See `references/judge-prompts.md` for full templates covering:
- Plan completeness, feasibility, risk, testing strategy
- Architecture review with scoring (0-10 per dimension)
- Code review checklist (correctness, design, safety, maintainability)

## Integration Points

- **With adversarial review:** This IS the formalized version of "spawn a separate model to review"
- **With planning-protocol:** Judge reviews the plan before the Execute phase
- **With coding workflows:** Code → cross-model review → fix findings → test → build → push

## Quick Decision

```
Simple task?           → Self-review
Complex / high stakes? → LLM-as-Judge
Stuck after retries?   → LLM-as-Judge (fresh perspective)
Financial/security?    → LLM-as-Judge (mandatory)
```

## Gotchas
- **Same provider defeats the purpose** — Claude Opus judging Claude Sonnet shares the same training distribution. Use a different provider (Grok judging Claude, Gemini judging GPT, etc.).
- **Vague judge output is useless** — If the judge says "looks good" without specifics, the prompt is too weak. Always require the judge to produce scored dimensions + specific actionable items, even if approving.
- **Judge scope creep** — Judges sometimes rewrite the entire plan instead of reviewing it. Constrain the verdict to APPROVE / REVISE / REJECT with specific feedback, not a replacement solution.
- **Approval rate drift** — If the judge approves >80% of submissions, the model pairing is too similar or the prompts are too lenient. Target 60-70% approval rate.
- **Don't judge trivial tasks** — A 50-line CSS fix doesn't need cross-model review. Use the activation criteria in this skill strictly.
