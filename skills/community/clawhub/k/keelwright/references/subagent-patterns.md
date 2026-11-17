# Subagent Delegation Patterns (F48, v1.10.3)

WHY: Complex tasks need parallel, isolated reasoning. `delegate_task` spawns subagents with
own context, terminal, tools. But bad delegation = context loss, drift, wasted tokens.

---

## When to Delegate

✅ Reasoning-heavy subtasks (audit, design, research)
✅ Independent parallel workstreams (4 agents × 4 cards)
✅ Tasks that flood context with intermediate data
✅ Need different model/persona per sub-task

❌ Mechanical multi-step work → use `execute_code` / `terminal`
❌ Single tool call → call directly
❌ Tasks needing user interaction → subagents CANNOT ask questions
❌ Durable work surviving session → use `cronjob` / `terminal(background=True)`

---

## Delegation Template

```python
delegate_task(tasks=[
  {"goal": "Audit clean-code on SKILL.md + scripts/*.py",
   "context": "Repo: ratingtesting/keelwright@main. Scope: SKILL.md (index), scripts/*.py, references/*.md. Role: clean-code-review. Use tencent/hy3:free via nous. Output: verdict CRIT/MAJ/MIN + file refs.",
   "output_schema": {"type": "object", "properties": {"verdict": {"type": "string"}, "findings": {"type": "array"}}}}
], max_concurrent=4)
```

---

## Context Packing Rules

Each subagent knows NOTHING of parent conversation. Must include:
- Exact repo/commit/branch
- Scope (files, directories)
- Role + model pin
- Output format (schema if structured)
- Any constraints (time, token, tool limits)

---

## Subagent Output Handling

- Child summaries are SELF-REPORTS, not verified facts
- For external side effects (uploads, writes, publishes): require verifiable handle (URL, ID, path) and VERIFY YOURSELF
- Children cannot call: `delegate_task`, `clarify`, `memory`, `cronjob`
- Model: pinned via `delegation.provider / delegation.model` in config.yaml (default: tencent/hy3:free via nous)

---

## Swarm Kanban Pattern (16 agents)

1. Master writes `brain/plans/AUDIT-PLAN.md` with 16 cards
2. Each card = one subagent task (role + scope + output_schema)
3. `delegate_task` spawns all in parallel (max_concurrent=4-8)
4. Wait for consolidated results
5. Master synthesizes → `brain/plans/AUDIT-RESULTS.md`

---

## Anti-Patterns to Avoid

- "Here, fix this" without scope → drift
- No output_schema → unparseable summaries
- Too many concurrent (>8) → context thrash
- Delegating what you should do yourself (simple edits)