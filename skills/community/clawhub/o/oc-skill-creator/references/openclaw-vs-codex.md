# OpenClaw vs Codex Skill Creator

> Documents the differences between the bundled Codex skill-creator (`/app/skills/skill-creator/`) and the new OpenClaw-native skill-creator. Use this reference when creating new OpenClaw skills or porting existing Codex skills.

## Architecture Differences

| | Codex (CLI Coding Agent) | OpenClaw (Multi-Agent) |
|---|---|---|
| Execution | Single CLI session | Main + sub-agents (spawn/fork) |
| Context | All context exists within the session | Sub-agents start with **empty** context |
| Skill loading | description → body → scripts (sequential) | description(always) → body(on trigger) → references(on demand) |
| Skill storage | Single location | workspace(persists across restarts) vs bundled(resets on update) |
| Prompt injection | Unnecessary (single context) | **Required** (explicit injection into sub-agents) |
| Packaging | `package_skill.py` creates `.skill` file | No packaging — folder structure is recognized directly |

## 5 Key Differences

### 1. Sub-Agent Context Injection

**Codex**: All work happens in one session, so context sharing is natural.

**OpenClaw**: When you spawn a sub-agent, its context is **empty**. The main agent must explicitly inject information gathered during Phase 0 into the sub-agent's prompt.

Codex skills have no concept of this. In OpenClaw, it's the most important pattern.

```
Codex:   "Summarize this text" → OK (context already present)
OpenClaw: "Summarize this text" → FAIL (sub-agent has no context)

OpenClaw correct approach:
"This text is sections 1–5 of the 'OOO User Manual'.
The full document has 27 sections in 5 parts. This chunk covers 'New Design Methodology'.
Preserve the following: [analogies], [quotes], [case studies]..."
```

### 2. Style Guide First

**Codex**: "Concise is key" — focus on saving context window. Assumes the agent is already smart enough.

**OpenClaw**: Without a style guide, sub-agents become "text compressors." **Judgment criteria** are mandatory.

Codex skills focus on format (structure, length), but OpenClaw skills must also include judgment criteria (what to preserve, which tone, which perspective).

### 3. Phase 0 (Analysis Stage) Required

**Codex**: The agent naturally analyzes while working.

**OpenClaw**: A pipeline where the main agent analyzes in Phase 0, then injects results into sub-agent prompts, is required.

Without Phase 0:
- Each chunk is processed independently (overall flow is lost)
- Duplicate content appears across chunks
- Author's voice (analogies, quotes) gets dropped

### 4. Sequential Pipeline

**Codex**: Multiple outputs can be generated in parallel; the agent naturally merges them.

**OpenClaw**: Complex outputs should be expanded sequentially from simple to complex.

Example: summary depth 1x + 5x
- Codex: can generate in parallel (agent merges)
- OpenClaw: 1x → 5x sequential (1x structure serves as the skeleton for 5x)

### 5. No Packaging Needed

**Codex**: `package_skill.py` creates a `.skill` file (essentially a zip) for distribution.

**OpenClaw**: Recognizes folder structure directly. Only `SKILL.md` is needed for a skill to work.

No packaging scripts, validation scripts, or init scripts required.

## Porting Checklist: Codex Skill → OpenClaw Skill

When porting a Codex skill to OpenClaw:

- [ ] **Check if sub-agents are needed** — If the skill does chunking or parallel processing, verify Phase 0 + context injection patterns exist
- [ ] **Style Guide present?** — If not, add one. Format specs alone aren't enough for sub-agents to produce quality output
- [ ] **Add Phase 0** — Is there an analysis stage before work begins?
- [ ] **Prompt templates with `[ ]` placeholders** — Verify placeholders are filled with Phase 0 results
- [ ] **Merge instructions** — Explicitly prevent simple concatenation of multi-chunk outputs
- [ ] **Remove `package_skill.py` references** — Not needed in OpenClaw
- [ ] **Remove `init_skill.py` references** — Not needed in OpenClaw
- [ ] **Trigger keywords in description** — Include both English and localized keywords
- [ ] **Move "When to use" from body to description** — OpenClaw loads body only after trigger

## Patterns to Keep from Codex

The following are good patterns that work in both environments:

1. **Progressive Disclosure** — Keep SKILL.md under 500 lines; move details to references/
2. **"Concise is key" principle** — Don't re-explain what the agent already knows
3. **Degrees of Freedom** — Adjust specificity based on task fragility (high/medium/low)
4. **Single-level reference depth** — Don't reference another references/ from within references/
5. **Improve after use** — Use the skill, observe failures, fix, repeat
