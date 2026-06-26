---
name: skill-creator
description: >
  Create, edit, improve, tidy, review, audit, or restructure OpenClaw AgentSkills and SKILL.md files.
  Optimized for OpenClaw's architecture: sub-agents, context fork, skill auto-loading, and references/.
  Covers the full lifecycle: analyze existing work → extract patterns → design skill → write SKILL.md → test → iterate.
  Keywords: skill, create skill, skill creator, SKILL.md, 스킬, 스킬 만들기, 스킬 생성, 스킬 개선, 스킬 수정, 스킬 검토, 스킬 작성, スキル, スキル作成, スキル生成, スキル作成, 技能创建, 创建技能, 生成技能, 改进技能.
---

# OpenClaw Skill Creator

Create, improve, and maintain OpenClaw AgentSkills. This guide covers the full lifecycle from pattern extraction through testing.

## Why This Skill Exists

OpenClaw skills are not just simple prompt files. Skills designed for OpenClaw's architecture — 3-layer loading (description → body → references), sub-agent context injection, Phase 0 analysis — significantly improve agent quality. This skill systematizes those design principles and provides validated examples across 5 types (pipeline, single-task, tool integration, code generation, document conversion).

### Language Policy

- **SKILL.md body**: Always write in **English** — this ensures the skill works across all language environments
- **references/**: English by default. Localized copies may be provided as `filename.ko.md`, `filename.ja.md`, `filename.zh.md`
- **description Keywords**: Include keywords in all target languages (English, Korean, Japanese, Chinese)
- **Generated skills**: Follow the same policy — English body, multilingual keywords

## Key Strengths

1. **OpenClaw-native patterns** — Optimized for OpenClaw architecture: sub-agent context fork, references/ lazy loading, Phase 0 structural analysis
2. **5 validated types** — examples/ includes actual generated skills and case analyses for each type
3. **Style Guide-centric** — Skills that specify "what to preserve" and "what to compress" determine agent quality
4. **skill-audit integration** — Validate generated skills with skill-audit to get 0-100 scores and improvement recommendations
5. **Bundled skill porting** — Checklist for porting existing Codex-based bundled skills to OpenClaw patterns

## OpenClaw Skill Anatomy

```
skill-name/
├── SKILL.md                          # Required. Frontmatter + instructions.
├── references/                       # Optional. Loaded on demand by the agent.
│   ├── output-format.md              #   Output specifications
│   └── subagent-prompt-templates.md  #   Sub-agent prompt templates
├── scripts/                          # Optional. Executable code (Python/Bash/etc.)
│   ├── extract_epub.py
│   └── extract_pdf.py
├── assets/                           # Optional. Files used in output, not loaded into context.
│   └── template.html
└── examples/                         # Optional. Example files for reference.
```

**DO NOT create:** README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, LICENSE, or similar auxiliary documentation.

## Frontmatter (Required)

```yaml
---
name: skill-name
description: >
  What this skill does and when it should trigger.
  Include keywords in multiple languages.
  Keywords: keyword1, keyword2, 키워드1, 키워드2.
---
```

- **`name`**: lowercase, hyphens only. Under 64 chars. Prefer short, verb-led names.
- **`description`**: This is the **primary triggering mechanism**. OpenClaw reads this to decide when to load the skill. Include:
  - What the skill does
  - When to use it (triggers, contexts)
  - Keywords in all relevant languages (localized + English)
  - Do NOT put "when to use" info in the body — it's only loaded AFTER triggering.

## Loading Architecture

OpenClaw loads skills in three layers:

1. **Metadata** (name + description) — Always in context. ~100 words per skill.
2. **SKILL.md body** — Loaded when the skill triggers. Keep under 500 lines.
3. **references/** — Loaded on demand when the agent decides it's needed.

**Implication:** Every word in `description` is always costing tokens. Be concise. Every word in SKILL.md costs tokens when the skill triggers. Keep it lean.

---

## Skill Creation: 5-Step Process

### Step 1: Analyze "Well-Done" Results

Before writing anything, analyze examples of **the agent performing the task well without a skill**.

Ask:
- What structure did the output have?
- What did the agent **preserve** (examples, metaphors, quotes, data)?
- What did the agent **compress** (repetition, verbose explanations)?
- What **judgments** did the agent make (grouping, prioritization, restructuring)?
- Why did it make those judgments?

> **This analysis becomes the Style Guide.** This is the most important step.
> A skill that only specifies format but not style produces dry, mediocre results.

### Step 2: Analyze "Failed" Results (if available)

If sub-agents or previous skill versions produced bad results, identify exactly what went wrong:

| Symptom | Likely Cause |
|---------|-------------|
| Output is dry/bland | Missing style guide — no "what to preserve" rules |
| Flow is disconnected | Chunks processed independently — missing Phase 0 context injection |
| Lots of duplication | Missing merge/restructure instructions |
| Inconsistent style | No style rules in sub-agent prompts |
| Sub-agent ignores instructions | Sub-agent prompt lacks context from Phase 0 |

> **Every failure maps to a specific instruction to add to the skill.**

### Step 3: Write Style Guide First

Write the Style Guide **before** the workflow. The workflow is "what order" — the Style Guide is "how to judge."

```markdown
## Style Guide

### Essence
- What is the core of this task? (e.g., "Summarization is restructuring, not compression.")
- What perspective should the agent take?

### Preservation Criteria (NEVER discard)
- Specific examples with "why"

### Compression Criteria (what to reduce)
- Specific examples with "why"

### Style Rules
- Tone, sentence length, formatting conventions
- Rules specific to this context
```

### Step 4: Structure the Workflow

Build the workflow around the Style Guide:

```markdown
## Workflow

### Phase 0: [Analysis Step] (★ Most Important)
What to analyze before starting, and where that information gets used.

### Phase 1~N: [Execution Steps]
Each step's specific instructions.

### Phase N+1: [Validation Step]
How to verify the output meets quality standards.
```

**Key principles:**
- **Phase 0 first** — analyze the full input before dividing into chunks or delegating
- **Context injection for sub-agents** — sub-agents have NO context from the main session. Phase 0 results must be explicitly injected into sub-agent prompts.
- **Validation step** — check output length, structure, and quality

### Step 5: Split into References (if needed)

If SKILL.md approaches 500 lines, split:

| Content type | Where to put it |
|-------------|----------------|
| Output structure/specifications | `references/output-format.md` |
| Sub-agent prompt templates | `references/subagent-prompt-templates.md` |
| Domain knowledge (APIs, schemas) | `references/domain.md` |
| Examples | `references/examples.md` |

Always link references from SKILL.md with a description of **when to read them**.

---

## Sub-Agent Design Patterns

Sub-agents are the #1 source of skill quality degradation. The root cause is always the same: **the sub-agent lacks context that the main agent has.**

### Pattern A: Context Injection

Always include in sub-agent prompts:
1. **Full context** — "This chunk is part of [overall structure]. It covers [topic]."
2. **Specific preservation list** — "In this chunk, preserve: [metaphor, quote, example]"
3. **Judgment criteria** — 3-4 lines from Style Guide
4. **Output format** — How to format the result

### Pattern B: Template with Fill-in-the-Blanks

Don't copy templates verbatim. Use `[ ]` placeholders filled from Phase 0:

```markdown
Sub-agent prompt template (fill `[ ]` from Phase 0 results):

## Context
[Overall structure from Phase 0]
[This chunk's position in the whole]

## Preserve (this chunk only)
[Specific items from Phase 0]

## Instructions
[Depth/format/style rules]

---
[Chunk text]
---
```

**If Phase 0 didn't produce `[ ]` values, the template can't be filled. The sub-agent becomes a context-free "text compressor." This is why Phase 0 is mandatory.**

### Pattern C: Sequential Pipeline

When multiple depth levels exist (e.g., 1x and 5x), use sequential dependency:

```
depth=1x:  Analyze → Chunk → Summarize → Merge → summary.md
depth=5x:  Analyze → Chunk → Summarize → Merge → summary.md
           → Use summary.md as skeleton → Expand → summary_5x.md
```

**Why sequential?** The simpler output provides structure for the complex one. Starting with the complex version means each chunk is independently summarized, losing overall flow.

### Pattern D: Merge ≠ Concatenate

When merging multiple chunk results:
1. Never just concatenate
2. Restructure according to Phase 0's topic flow
3. Remove duplicates (keep the most detailed version)
4. Derive overall takeaways (not just chunk summaries)

---

## Skill File Organization Rules

### Keep SKILL.md Lean

- **Under 500 lines** — split into references/ if longer
- **Only in SKILL.md**: Workflow phases, Style Guide summary, parameter tables, reference links
- **In references/**: Detailed specs, prompt templates, domain knowledge, examples

### Reference File Best Practices

- **One level deep** — all reference files link directly from SKILL.md, not from other references
- **Table of contents** — for reference files over 100 lines
- **Never duplicate** — information lives in either SKILL.md OR a reference file, never both

### Workspace Skills vs Bundled Skills

| | Workspace (`~/.openclaw/workspace/skills/`) | Bundled (`/app/skills/`) |
|---|---|---|
| Persistence | Survives container restarts | Reset on container restart |
| Scope | User-specific, project-specific | Shared, system-wide |
| When to use | Custom workflows, domain knowledge | Universal tools (weather, discord, etc.) |
| Source of truth | **This directory** for new custom skills | Reference only, don't modify |

**Always create custom skills in workspace. Never modify bundled skills.**

---

## Skill Improvement & Auditing

### Audit Checklist

For any skill, check:

**Triggering**
- [ ] `description` clearly explains when to trigger?
- [ ] Keywords in relevant languages?
- [ ] No "when to use" sections in body (should be in description)?

**Style Guide**
- [ ] "What to preserve" with specific examples?
- [ ] "What to compress" with specific examples?
- [ ] Style rules explicit?

**Workflow**
- [ ] Phase 0 (analysis) comes first?
- [ ] Sub-agent context injection specified?
- [ ] Validation/quality check step exists?

**Sub-agent Integration**
- [ ] Prompt templates have `[ ]` placeholders filled from Phase 0?
- [ ] Clear warning about what happens without context injection?

**File Organization**
- [ ] SKILL.md under 500 lines?
- [ ] Long content split to references/?
- [ ] Each reference file describes when to read it?

### Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Format-only, no style | Dry, mediocre output | Add Style Guide |
| Sub-agent without context | Disconnected chunks | Add Phase 0 + context injection |
| Simple concatenation | Duplication, no flow | Add restructure instructions |
| Arbitrary chunk boundaries | Content cut mid-section | "Cut only at section/chapter boundaries" |
| Parallel depth generation | Inconsistent structures | Sequential pipeline (simple → complex) |
| Template used verbatim | Context-free instructions | Fill `[ ]` from Phase 0 results |
| "When to use" in body | Never read (body loads after trigger) | Move to description |

---

## References

- `references/openclaw-vs-codex.md` — Differences from the bundled Codex skill-creator and porting checklist
- `examples/summarize.md` — Validation example: summarize skill (sub-agent pipeline type)
- `examples/changelog.md` — Validation example: changelog skill (doc conversion type)
- `examples/scaffold.md` — Validation example: scaffold skill (code generation type)
- `examples/screenshot-capture.md` — Validation example: screenshot-capture skill (tool integration type)
- `examples/unit-converter.md` — Validation example: unit-converter skill (single-task type)
- `examples/skill-audit.md` — Validation example: skill-audit (meta validation tool)
