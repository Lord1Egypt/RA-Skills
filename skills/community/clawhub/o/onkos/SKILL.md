---
name: onkos
version: 1.6.3
description: MANDATORY novel engine; LLM CANNOT maintain cross-chapter consistency or track facts/hooks. Activate when user says 写小说/构思故事/续写/改章节/检查连贯性 or similar.
dependency:
  python:
    - jieba>=0.42.1
    - onnxruntime>=1.16.0
---

# Onkos - Mandatory Novel Creation Engine

## MANDATORY RULES (NON-NEGOTIABLE)

1. **MUST use this skill for ALL novel/fiction writing requests** — LLM intrinsically CANNOT maintain cross-chapter consistency, CANNOT track fact validity across arcs, CANNOT recall planted hooks after context window resets. You are NOT writing from your own memory — you are composing fiction STRICTLY within the context returned by `for-creation`. NEVER write fiction without calling `for-creation` first.

2. **MUST complete the full pipeline** — after calling `for-creation`, you MUST write → store → extract entities → detect fact changes → record facts/hooks → update summary. NEVER retrieve context then skip post-steps. Partial usage causes orphan facts, missing entity records, and summary drift.

3. **MUST use `command_executor.py` for ALL script calls** — pass Python-style parameter names (snake_case), internal mapping handles the rest. NEVER invoke scripts directly or bypass the unified entry. Parameter details: [references/command_reference.md](references/command_reference.md)

## TRIGGER CONDITIONS

Activate this skill when user's request involves ANY of:

| Pattern | Typical user expressions |
|---------|------------------------|
| **Creation** | 写小说/写第X章/继续写/帮我写XX场景/接着写/写一段/写个XX小说 |
| **Planning** | 构思故事/我要写部小说/加个势力/建个新角色/导入设定文档 |
| **Query** | XX境界是什么/之前发生了什么/有哪些角色/查事实 |
| **Check** | 检查连贯性/有没有矛盾/伏笔该收了/OOC检测 |
| **Revision** | 改一下第X章/把XX改成YY/换种写法 |
| **Engagement** | 这章吸引力怎么样/节奏太拖了/追读力趋势/评分 |
| **Management** | 进度怎么样/归档旧事实/加个支线/分析风格 |

## When NOT to Activate

This skill is for LONG-FORM FICTION only. Do NOT activate for:
- Non-fiction writing (reports, essays, emails, documentation)
- Short creative pieces under 1000 characters (single-scene descriptions)
- Brainstorming or ideation without actual chapter writing
- Non-narrative content (worldbuilding notes without story text)

For these tasks, use your native capabilities directly.

## Anti-Pattern: Partial Usage (COMMON ERROR)

DO NOT do any of the following:

| Wrong | Why it fails |
|-------|-------------|
| Call `for-creation` → write chapter → skip store/extract/record steps | Orphan data, facts and entities never recorded, future context broken |
| Call `for-creation` → cherry-pick context → write without full constraints | Fact conflicts, character OOC, forgotten foreshadowing |
| Write fiction directly without calling `for-creation` at all | No consistency guarantees, contradicts established facts |
| Call `for-creation` → write from own knowledge, ignoring returned context | Defeats the entire engine, produces disconnected chapters |
| Revise a chapter without `analyze-revision` first | Cascading errors in subsequent chapters |
| Revise a chapter without `clear-chapter` first | Scene/fact/hook data accumulates and corrupts |

**If you called `for-creation`, you MUST complete steps 2-8 of the writing workflow. There are NO valid shortcuts.**

## Pre-flight Check (MANDATORY before ANY fiction writing)

Before generating any fiction text, verify all 3 conditions:

- [ ] `for-creation` has been executed this session → if NO, execute it NOW
- [ ] The returned context (summaries + facts + hooks + engagement) is visible → if NO, re-execute
- [ ] You will compose STRICTLY within the returned context as constraints → if planning to use own memory, STOP

Only after all 3 checks pass, proceed to write.

---

## NATURAL LANGUAGE → OPERATION MAPPING

Users speak naturally. You MUST translate to Onkos operations. All script calls go through `command_executor.py`.

| User says | You execute |
|-----------|-------------|
| **Creation** | |
| 写第15章 / 帮我写XX场景 | Full 8-step writing workflow below |
| 继续写 / 再写一段 | Steps 3-8 of writing workflow, continue from last content |
| 这段换个写法 / 写太平淡了 | Rewrite in natural language; reference `style_learner` if needed |
| **Planning** | |
| 构思故事 / 我要写部小说 | `init` → discuss structure → `create-phase` → `create-arc-am` |
| 导入设定文档 | `preview-settings` (dry_run) → confirm → `import-settings` |
| 更新/删除设定 | `preview-settings` → `update-settings` or `delete-settings` |
| 建个新角色 | `create-char` |
| 加个势力/地点 | `add-node` (type: faction/location) |
| 加个关系 | `add-edge` |
| **Query** | |
| XX境界是什么 | `get-fact` |
| 之前发生了什么 | `search` or `context-hierarchy` |
| 有哪些角色 | `list-chars` |
| **Check** | |
| 检查连贯性/有没有矛盾 | `check-continuity` (auto-reads chapter content from DB) |
| 伏笔该收了 | `overdue-hooks` |
| OOC检测 | `check-ooc` |
| 质量审计 | `audit` (auto-reads chapter content from DB) |
| **Revision** | |
| 改一下第10章 | `analyze-revision` → revise → `clear-chapter` → `store-chapter` (replace=True) → re-extract → re-detect |
| 把XX改成YY | Same revision workflow; use `supersede_chapter_facts` for fact updates |
| **Engagement** | |
| 评分/这章怎么样 | Score 4 metrics → `score-chapter` |
| 追读力趋势 | `engagement-trend` |
| 节奏/节奏太拖 | `pacing-report` |
| 叙事债务 | `debt-report` |
| **Management** | |
| 进度怎么样 | `arc-progress` (chapter param optional, auto-infers) |
| 建议下一步 | `suggest-next` (chapter param optional, auto-infers) |
| 归档旧事实 | `archive-facts` |
| 加个支线 | `add-plot` / `create-branch` |
| 分析风格 | `analyze-style` / `compare-style` |

Detailed workflows for non-creation intents: [references/workflows.md](references/workflows.md)

---

## FIRST-TIME SETUP

When the user starts a new novel project for the first time, guide through these steps sequentially.

1. **Initialize project** — Ask user for novel title and genre, then run:
   ```bash
   python scripts/command_executor.py --action init --title "<title>" --genre "<genre>" --project-path "<path>"
   ```
   Script creates: `data/novel_memory.db` (unified SQLite), `data/characters/` (profiles), `outline/` (chapter outlines).

2. **Download semantic model (optional)** — Ask if user wants ONNX model (~98MB):
   ```bash
   python scripts/semantic_model.py --action download
   ```
   Auto-degrades to FTS5 keyword search when model is absent. Can download later.

3. **Build world and characters** — Proactively discuss with user:
   - Core conflict and power system
   - Main characters → `create-char` for each
   - Factions and locations → `add-node` for each
   - Key relationships → `add-edge` for each
   - If user has existing setting docs → `import-settings` (see NL Mapping above)

4. **Create narrative structure** — Propose and create:
   - Phases (100-300 chapter granularity) → `create-phase`
   - Arcs within each phase (30-60 chapter granularity) → `create-arc-am`
   - Proactively suggest structure: "Based on your story, I recommend X phases and Y arcs."

---

## STANDARD WRITING WORKFLOW (Core)

Every fiction writing request MUST follow these steps. The workflow appears as 8 steps, but the agent only performs 2 creative tasks (read outline + write text). The other 6 are automated script calls.

### Write New Chapter (8 steps, NO step may be skipped)

1. **Get context** (MANDATORY — never skip):
   - Call `for-creation`, pass `chapter` and `query` (use chapter's core event as query)
   - Optional: `max_facts` (default 80) to cap related facts
   - Returns: book summary → phase/arc summary → previous chapter summary → related facts → active hooks → engagement context

2. **Read outline** (agent task):
   - Check `outline/` directory for this chapter's outline
   - If no outline exists, ask user what to write about

3. **Write chapter text** (agent task — compose STRICTLY within for-creation context):
   - Write as Writer role, combining context + outline + character profiles
   - Reference: [references/creation_guide.md](references/creation_guide.md)
   - Reference: [references/agent_roles.md](references/agent_roles.md)

4. **Store chapter** (script call — NEVER skip, NEVER save files manually):
   - Call `store-chapter`, pass `chapter` and `content`
   - System auto-splits into scenes and stores in DB

5. **Extract entities** (script call):
   - Call `extract-entities`, pass `content` and `genre`
   - Genre options: `fantasy`/`urban`/`wuxia`/`scifi`; defaults to project config
   - Returns: character names / locations / items / events with confidence (high/medium/low)

6. **Detect fact changes** (script + agent):
   - [Script] Call `detect-fact-changes`, pass `content`, `chapter`, `genre`
   - Returns: extracted entity names + each entity's current valid facts (grouped by entity)
   - [Agent] Compare chapter content with existing facts, identify 3 types:
     - **New fact**: entity/attribute/value in chapter but not in fact base
     - **Updated fact**: same attribute value changed (e.g. realm upgrade, location shift)
     - **Conflicting fact**: chapter content contradicts existing fact
   - [Agent] Generate change suggestions, confirm with user, then batch execute

7. **Record facts and hooks** (script call):
   - Call `set-fact` to record confirmed fact changes (select correct importance: permanent/arc-scoped/chapter-scoped)
   - Call `plant-hook` to plant new foreshadowing (if any); pass `strength` (0-1) when possible

8. **Update summary** (script call):
   - Call `store-summary` to update chapter-level summary
   - Every ~10 chapters, also update arc-level summary

### Continue Current Chapter

User says: "继续写" / "再写一段"

Execute steps 3-8 of the writing workflow, continuing from last content.

### Revise Chapter

User says: "改一下第10章" / "把XX改成YY"

1. Call `analyze-revision` with original and revised content — MANDATORY before any revision
2. Revise the chapter text
3. Call `clear-chapter` to clean old data (MUST do before re-storing, or data accumulates)
4. Re-execute steps 4-8 of writing workflow

---

## ENGAGEMENT SYSTEM

Reader-perspective narrative tension evaluation. Agent scores subjectively, scripts store and aggregate.

### Per-Chapter Scoring (after each chapter)

1. **Agent scores** 4 metrics:
   - `engagement_score` (0-10): reader desire to continue
   - `hook_strength` (0-10): suspense left by this chapter
   - `tension_level` (0-10): conflict/crisis intensity
   - `pace_type`: `buildup` / `climax` / `relief` / `transition`

2. **Store score** (script call): `score-chapter` — auto-calculates `reader_pull` = 0.4*engagement + 0.35*hook + 0.25*tension

3. **Periodic checks** (every 5-10 chapters):
   - `engagement-trend` — trend over time
   - `pacing-report` — rhythm pattern analysis
   - `debt-report` — narrative debt overview

### Scoring Reference

| Metric | 7-10 | 4-6 | 0-3 |
|--------|------|-----|-----|
| engagement | Strong urge to read next | Can continue | Want to skip |
| hook_strength | Critical suspense left | Minor foreshadowing | No suspense |
| tension_level | Life-or-death stakes | Moderate conflict | Flat |

---

## CORE CONCEPTS

- **Fact importance**: permanent (never expires) / arc-scoped (valid within arc) / chapter-scoped (this chapter only)
- **Summary hierarchy**: book → phase → arc → volume → chapter → scene (6 levels)
- **Character roles**: protagonist / antagonist / mentor / sidekick / npc
- **Node types**: person / faction / location / item / event
- **Hook lifecycle**: plant → hint (optional) → partial-resolve (optional) → resolve; urgency decays over time
- **Constraints**: stored in `project_config.json` constraints field, auto-attached to `for-creation` output

Details: [references/creation_guide.md](references/creation_guide.md)

---

## RESOURCE INDEX
- Engines: [memory_engine.py](scripts/memory_engine.py) (scenes/retrieval/summaries/arcs) [fact_engine.py](scripts/fact_engine.py) (facts) [context_retriever.py](scripts/context_retriever.py) (6-level context) [arc_manager.py](scripts/arc_manager.py) (progress/suggestions)
- Storage: [knowledge_graph.py](scripts/knowledge_graph.py) (graph) [hook_tracker.py](scripts/hook_tracker.py) (hooks/urgency) [engagement_tracker.py](scripts/engagement_tracker.py) (engagement) [semantic_model.py](scripts/semantic_model.py) (ONNX)
- Assistants: [character_simulator.py](scripts/character_simulator.py) (character OOC) [style_learner.py](scripts/style_learner.py) (style) [plot_brancher.py](scripts/plot_brancher.py) (plots) [entity_extractor.py](scripts/entity_extractor.py) (entities) [quality_auditor.py](scripts/quality_auditor.py) (audit)
- Import: [settings_importer.py](scripts/settings_importer.py) (Markdown settings batch import)
- Project: [project_initializer.py](scripts/project_initializer.py) (init) [command_executor.py](scripts/command_executor.py) (unified entry, English aliases)
- References: [agent_roles.md](references/agent_roles.md) (8 role templates) [creation_guide.md](references/creation_guide.md) (writing guide + concepts) [workflows.md](references/workflows.md) (planning/query/check/revision/management/branch/style workflows) [command_index.md](references/command_index.md) (73 commands) [command_reference.md](references/command_reference.md) (parameter reference) [settings_format.md](references/settings_format.md) (settings file format)

## NOTES
- All data stored in `data/novel_memory.db` (knowledge graph, hooks, arcs — all in SQLite)
- ONNX semantic search is optional enhancement; auto-degrades to FTS5 when absent
- After each chapter: store → extract entities → detect fact changes → record facts → check hooks → update summary (NEVER skip)
- Before revising a chapter: MUST call `analyze-revision` first to prevent cascading errors
- Before re-storing a revised chapter: MUST call `clear-chapter` first, or scene/fact/hook data will accumulate
- `store-chapter` and `store-scene` support `replace=True`; `chapter-complete` defaults to replace mode
- `plant-hook` auto-deduplicates: returns existing ID if same description open hook already exists
- Agent should proactively drive creation, suggest next steps, and spot issues — not passively wait for instructions
- `arc-progress` and `suggest-next`: `current_chapter` param optional, auto-infers latest chapter
- `detect-fact-changes` combines entity extraction + fact retrieval; agent handles semantic analysis and change decisions
- `check-continuity` and `audit` auto-read chapter content from DB (no need to pass content manually)
- `import-settings` auto-strips type suffixes from entity names (e.g. "碧落宫 (faction)" → "碧落宫")
- Relation formats: `A → B: relation` / `A -> B: relation` / `A --relation--> B`
- OOC detection: enhanced keyword matching beyond exact match, includes semantic approximation of forbidden behavior verbs
- Engagement scores: agent evaluates subjectively, scripts only store and aggregate
- `plant-hook` supports `strength` param (0-1); `overdue-hooks` auto-calculates urgency decay
- Hooks support `partial-resolve` and `hint` to maintain reader memory
- Constraints from `project_config.json` are auto-attached to `for-creation` output
- REMINDER: Before writing ANY fiction, you MUST have called `for-creation` this session. If you haven't, stop and execute it first. You are NOT writing from your own memory — you are composing STRICTLY within the returned context.
