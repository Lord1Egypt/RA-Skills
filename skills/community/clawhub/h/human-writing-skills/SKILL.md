---
name: human-writing-skills
description: Multilingual AI humanizer for genre-aware generation, humanize AI text, de-AI writing, natural rewriting, fiction and novels, novel writing assistant, story continuity, multi-agent long-form writing from outlines, long-form audit, chunked audit, style consistency review, character consistency audit, scene ending audit, translationese review, and rewrite fidelity. Use for supplied-draft cleanup, sample-backed voice matching, novel continuation, and factual essays, news, academic, official, legal, or technical prose. Includes generation-time quality guards and independent editorial review. 增强版去 AI 写作 Skill、高级 AI 写作工具、去AI味、去AI写作、消除AI腔、AI文本润色、小说润色、小说续写、多Agent长篇写作、大纲驱动写作、逐块审稿、AI式结尾、生硬结尾审查、无意义升华、长文一致性、长篇审查、分块审查、全书审查、文风统一、人物设定统一、人物一致性审查、人物对白审查、方言语域、翻译腔、战力设定、语义保真审查.
---

# Advanced Human Writing & AI Humanizer

Humanize AI-shaped text, write or continue genre-aware prose, and audit long-form
continuity without flattening a specific voice. Use the smallest set of modules
that covers the task. Keep project facts, prior chapters, rewrite originals, and
continuity ledgers separate from optional style references.

## Capability Layers

- The `humanwriting/` Python package is executable. Its CLI deterministically
  compiles prompts, locates recurring text patterns, calculates diagnostics,
  previews conservative fixes, checks protected content, and writes staged audits.
- The Markdown files under `skills/` are model-executed writing and editorial
  modules. They are selected by the compiler and are intentionally not pretending
  to be deterministic NLP algorithms.
- A normal installation includes both layers. Verify the executable layer with
  `human-writing-skills list --kind module` and run a real draft through `lint`,
  `fix`, `verify`, or `pipeline` rather than judging the package from `SKILL.md` alone.
- `human-writing-mcp` is an optional project-local coordination layer. It gives
  separate agents bounded long-form assignments, stores receipts, and refuses
  reconciliation until coverage verification passes. It does not call a model.
- In DSH agent mode, inspect `writing__human-writing__agent_capabilities` on demand
  before native delegation. Use the configured namespace and advertised schema;
  a visible tool or child-start receipt is not a completed assignment.

## Quick Humanize Route

- For a supplied draft, use `humanize --mode quick` for surface patterns,
  rewrite fidelity, and voice/ambiguity preservation.
- Use `--mode deep` only when structural repetition, cliches, paragraph stagnation,
  or broad editorial reconstruction needs a separate pass.
- Load `humanize-examples` only after an explicit request or `--with-examples`.
- Do not activate rewrite-preservation modules for unrelated new drafting.

## Workflow

1. Select one base style from `skills/`: `fiction`, `webnovel`, `argumentative`,
   `news-report`, `formal-document`, `self-media`, or `academic-paper`.
   Before producing prose, read `skills/generation-quality.md` and apply its compact
   protocol during drafting. The CLI `build` and MCP `compile_generation_prompt`
   include it automatically. Prevent repeated rhetorical moves, redundant explanation,
   decorative details, invented specificity, and unearned closure before they accumulate.
   Let genre, source evidence, and author voice govern choices; do not force roughness,
   body reactions, fragment runs, or open endings as proof of naturalness.
2. Read only the relevant modules. Add continuity, spatial, relationship, number,
   dialogue, dialogue-performance, register, capability, world, process, salience, recurrence, source, rhythm, preservation,
   or AI-trace modules when the text actually needs them.
   `narrative-naturalness-audit` is reserved for deep or explicit AI-trace review of
   narrative prose; it is not loaded for ordinary quick humanization or serious documents.
   For fiction with spoken or wordless interpersonal exchanges, use
   `dialogue-voice-audit` and `dialogue-performance-audit` (CLI: `--profile voice`).
   Check both participants and separate speech from simultaneous action; establish
   reception, refusal, or an evidenced pending state before assuming completion.
   During drafting, reconsider this route when an interaction enters the scene even
   if the original request only said to continue a chapter.
3. Treat user facts and `--context` as authoritative. Never borrow facts from a
   style sample. When `--original` is supplied for a rewrite, activate
   `rewrite-fidelity` and preserve meaning without preserving awkward wording.
   In fiction and webnovels, do not let time/place mini-headings replace scene bridges.
4. Activate `reference-style-alignment` only when the user supplies reference
   material, gives an explicit style direction, or directly asks to match a style.
5. Treat `--source` as factual evidence only. Activate `source-grounding` for
   serious documents or explicitly selected factual `self-media` / `argumentative`
   work with source files. Personal experience and product reviews need evidence too.
6. For important revisions, run deterministic `lint`, then independent audit
   profiles, then `verify` protected literals against the source. For consequential
   rewrites use `verify-fidelity` too: changed claims require review even if every
   number and citation is unchanged. Run `stats` only
   when distributional diagnostics help; use `fix` as a preview before writing.
7. Keep `voice`, `serial`, `world`, `process`, `momentum`, `salience`, `recurrence`,
   `ending`, `texture`, `fidelity`, `preservation`, examples, and `sources` separate from the default audit. Activate them explicitly
   or through `pipeline --auto`. `serial` requires context, `recurrence` requires at
   least three chapters, `fidelity` requires `--original`, `preservation` requires
   both explicit selection and `--original`, examples require an explicit request,
   and `sources` requires a factual document type and `--source`.
   For diagnosis without replacement prose use `critique`. For important revisions,
   `compare-blind` writes an A/B prompt and a separate version key: send only the prompt
   to a reviewer without revision history. Accept ties and original wins. Stop when
   further edits have no evidenced benefit; never use AI-trace scores as quality proof.
8. For a book-length manuscript or large report, use `chunk-audit` instead of placing
   the whole draft in one prompt. Supply `--outline` or `--context` for authoritative
   character or report rules. Use `--agent-mode deep` only when every block needs a
   visible coverage receipt, then run `verify-chunk-audit` before reconciliation. Use
   `--translationese` only for an explicitly translated or localized work. Read
   `docs/long-form-consistency.md` only for this workflow.
   Add `--book-level` only for an explicitly requested whole-book fiction/webnovel
   review with at least three identifiable chapters; run it after chunk reports.
9. When multiple agents or sessions share a long-form project, use
   `human-writing-mcp` rather than copying the entire manuscript into each chat.
   Agents must claim a task, submit a complete receipt, and pass coverage
   verification before one final reconciliation task is released. Read
   `docs/agent-orchestration.md` only when an MCP-capable host is available.
10. For requested long-form generation (typically 10,000+ output characters/words)
    or explicit multi-agent writing, read `skills/long-form-writing.md` on demand.
    Use `plan-writing` / `plan_long_form_writing` to check the outline, allocate
    bounded writer/editor tasks, and gate assembly on cross-block continuity.
    Dependent scenes run sequentially; explicit independent state contracts permit
    bounded parallel work. The host supplies native subagents; disclose role-pass
    fallback when no runner exists. An existing long input alone does not activate
    long-form generation. For the detailed commands read `docs/long-form-writing.md`.

## Commands

```powershell
human-writing-skills build --style fiction --context ledger.md --task "Continue the scene."
human-writing-skills humanize --draft chapter.md --style fiction --mode quick
human-writing-skills humanize --draft article.md --style self-media --mode deep --with-examples
human-writing-skills build --style fiction --reference sample.md --task "Match the sample's restrained rhythm."
human-writing-skills build --style self-media --original original.md --task "Rewrite without adding facts."
human-writing-skills audit --draft chapter.md --context ledger.md --profile physical
human-writing-skills audit --draft chapter.md --profile voice
human-writing-skills audit --draft chapter.md --context ledger.md --profile serial
human-writing-skills audit --draft chapters.md --profile momentum
human-writing-skills audit --draft chapters.md --profile recurrence
human-writing-skills audit --draft chapter.md --profile process
human-writing-skills audit --draft chapter.md --document-type fiction --profile ending
human-writing-skills audit --draft paper.md --document-type academic-paper --source study.md --profile sources
human-writing-skills audit --draft revised.md --original original.md --profile fidelity
human-writing-skills audit --draft revised.md --original original.md --profile preservation
human-writing-skills pipeline --draft chapter.md --context ledger.md --auto --with-stats --output-dir audit
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline outline.md --output-dir novel-audit
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline outline.md --agent-mode deep --output-dir novel-agent-audit
human-writing-skills verify-chunk-audit --package-dir novel-agent-audit
human-writing-skills plan-writing --outline outline.md --context ledger.md --style fiction --target-length 60000 --chunk-size 5000 --output-dir book-writing
human-writing-skills writing-tasks --package-dir book-writing
human-writing-skills chunk-audit --draft report-es.md --style news-report --source sources.md --translationese --agent-mode deep --output-dir report-audit
human-writing-mcp --root C:\writing-project
human-writing-skills lint --draft chapter.md --style fiction
human-writing-skills stats --draft chapter.md --style fiction
human-writing-skills fix --draft chapter.md --preview
human-writing-skills verify --source original.md --candidate revised.md
human-writing-skills verify-fidelity --source original.md --candidate revised.md
human-writing-skills evaluate --cases tests/fixtures/quality/multilingual-benchmark.json
```

Read `README.md` or `README.zh-CN.md` for user-facing guidance. Read files under
`docs/` only for the workflow being used. Do not claim detector evasion or infer
authorship from stylistic patterns; frame results as editing evidence.
