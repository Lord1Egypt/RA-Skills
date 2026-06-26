# Mythos Reasoning Protocol — CLAUDE.md 片段（v4 Three-Mode Router）

将以下内容添加到 `CLAUDE.md` 即可启用静默 mythos 推理。
**此协议不重复任何推理规则——它只是一个复杂度 gate + 模式路由器。** 完整规则在 SKILL.md 中。

---

## Reasoning Protocol (Mythos v4 — Three-Mode Router)

Before responding to any non-trivial request:

1. **Assess complexity (1-5):**
   - **1:** respond directly. Zero overhead. Do NOT load any skill.
   - **2-5:** Read `.claude/skills/mythos/SKILL.md` and follow STEP 1–3. SKILL.md is the single source of mode routing — it will pick:
     - **silent mode** (complexity 2-3, default) — Recurrent Block runs in your internal/extended-thinking reasoning; user sees only Coda
     - **agent mode** (complexity 4-5, default) — lenses dispatched as parallel subagents, then merged
     - **trace mode** (only if user explicitly used `trace` keyword) — visible token-level rounds
     
     **Keep all reasoning INTERNAL by default. Only emit visible rounds in trace mode.**

2. **Output expectations:**
   - silent mode (default for /mythos invocations and for everyday non-trivial requests): just the Answer + brief footer. No Prelude, no Rounds.
   - agent mode (high-complexity): Prelude visible + parallel subagent results + merge + Answer.
   - trace mode (opt-in via `/mythos trace …`): full Prelude + each Round + Answer.
   - "think aloud" or `trace` keyword forces trace mode for visibility.

3. **Mode keywords (parsed from user input, case-insensitive, last-wins):**
   - `trace` → force trace mode (visible rotation)
   - `deep` or `agent` → force agent mode (parallel fan-out) even at lower complexity
   - `quick` → force silent mode even at high complexity (skip the agent escalation)

4. **Gate:** Complexity = 1 returns directly without loading SKILL.md.
   For complexity ≥ 2 in silent or agent mode, if a lens application produces no new insight or introduces confusion (negative delta), halt the recurrence immediately and proceed to Coda.

---

## Migration from v3

v3 had two modes (single-pass, agent) and a `quiet` keyword to suppress trace. v4 unifies that:

- v3's `single-pass + visible trace` (default) → v4 **trace** mode (now opt-in)
- v3's `single-pass + quiet` → v4 **silent** mode (now default)
- v3's `agent` (sequential subagents) → v4 **agent** mode (now parallel-then-merge)
- v3's `quiet` keyword → no longer needed (silent IS the default; trace is opt-in)

User-facing changes:
- `/mythos <Q>` now returns just the Answer by default (no visible rounds)
- `/mythos trace <Q>` → old default visible-rounds behavior
- `/mythos deep <Q>` → parallel fan-out (was sequential subagents)
