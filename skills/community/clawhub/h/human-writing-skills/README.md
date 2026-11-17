# Advanced Human Writing & AI Humanizer

<p align="center"><img src="assets/logo.png" width="320" alt="Human Writing: fountain-pen handwriting with terminal code on a milk-white background"></p>

> Make AI-assisted writing more natural with multilingual editing, chunked long-form collaboration, and continuity review, available as Skills and a DSH plugin.

**Advanced AI humanizer and de-AI writing toolkit** for natural rewriting,
AI text cleanup, fiction editing, novel continuation, chunked long-form audit,
writing style unification, and character consistency review.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](pyproject.toml)

[中文说明](README.zh-CN.md) | English | [Español](README.es.md) | [Português (Brasil)](README.pt-BR.md) | [Français](README.fr.md)

**DeepSeek Harness plugin:** generate novels, papers, and reports with generation-time
quality guidance and local review tools. Install the complete bundled runtime:

```powershell
dsh plugin --profile web add https://github.com/whh110112/human-writing-skills/releases/download/dsh-v0.3.1/dsh-advanced-human-writing.tgz
```

Use `desktop` for the desktop profile. Python 3.9+ required; no separate core pip
install. See [DSH compatibility and usage](plugins/deepseek-harness/README.md).

Advanced Human Writing & AI Humanizer is an open-source, modular skill pack and lightweight prompt compiler for natural multilingual AI-assisted writing. The package, repository, and ClawHub slug remain `human-writing-skills` for compatibility.

This is not an empty prompt collection. The repository contains two deliberately
different capability layers:

- **Executable Python tools:** `humanwriting/` provides the installable
  `human-writing-skills` CLI for deterministic lint findings with evidence spans,
  text statistics, conservative fix previews, protected-content verification,
  prompt compilation, and staged audit-file generation.
- **Model-executed editorial modules:** `skills/*.md` contains genre and review
  instructions selected on demand by that compiler. These modules guide the writing
  model; they do not falsely present subjective literary judgment as a deterministic
  algorithm.

The test suite exercises both the executable layer and module-selection gates.

## Agent Orchestration, MCP, And DeepSeek Harness Plugin

DSH agent mode can inspect its actual, scope-visible delegation schema through
`writing__human-writing__agent_capabilities` (custom tool names are configurable).
Discovery is on demand and does not start agents or override model/preset settings.
Native children receive full role assignments; oversized assignments use paged files.
Claims expose their lease and can be renewed by the same identity before expiry.
Official DSH `0.2.1-rc.2` Cordis/MCP integration is tested; live-model child execution
still depends on the host's provider, driver, permissions and available capacity.

### Outline-To-Manuscript Multi-Agent Writing

New long prose can use five roles: outline checker, chunk planner, writers,
independent editors for every block, and a final continuity editor. A 60,000-character
target with 5,000-character blocks creates twelve writing jobs and their reviews.
Each writer receives its assigned outline and approved incoming state; editorial
receipts cover every paragraph, and final review covers every adjacent boundary.
Revision requests reopen affected writers and invalidate dependent approvals.

```powershell
human-writing-skills plan-writing --outline outline.md --context ledger.md --style fiction --target-length 60000 --chunk-size 5000 --output-dir book-writing
human-writing-skills writing-tasks --package-dir book-writing
```

Default dependencies are sequential. Explicit `--execution-mode contract` allows
parallel independent blocks with agreed entry/exit states and `--max-parallel 4`.
Use `--length-unit words` for word targets. The host supplies native subagents;
DSH loads the detailed orchestration protocol only for long output or an explicit
multi-agent request. [Workflow, result schemas and recovery](docs/long-form-writing.md).

### Shared Review State

For book-length novels, report series, or research coverage that cannot be
trusted to one chat window, install the dependency-free `human-writing-mcp`
server. It makes the long-form task graph executable across Codex, Claude Code,
OpenCode, DeepSeek Harness, Manus, and Hermes: agents claim bounded tasks,
submit coverage receipts, and cannot unlock reconciliation until every required
review is complete. The service stays inside a chosen project root and does not
call a model or upload drafts.

```powershell
human-writing-mcp --root C:\writing-project
```

The repository also ships a native DeepSeek Harness npm/Cordis bundle under
[`plugins/deepseek-harness`](plugins/deepseek-harness). It mounts the official
DSH MCP client and starts the same verified local coordination service. See the
[agent orchestration guide](docs/agent-orchestration.md) and
[DeepSeek Harness plugin guide](plugins/deepseek-harness/README.md).

The MCP server also supports day-to-day single-document work: `lint_text`,
`get_style_statistics`, `verify_protected_content`, `verify_fidelity`, `compile_humanize_prompt`,
`compile_audit_prompt`, and `compile_ledger_extraction`. It advertises a small
native prompt menu (`humanize-quick`, `dialogue-audit`, `continuity-audit`,
`serious-rewrite`, and more) for hosts that implement MCP Prompts. These tools
stay local and return evidence or compiled instructions; they never send a draft
to a model themselves.

## Ledger Auto-Extraction And Project Defaults

Long-form continuity should not require hand-maintaining every fact from scratch.
`extract-ledger` compiles an evidence-first prompt for turning existing chapters
into a **candidate** continuity ledger. Its output distinguishes observed facts,
inferences, conflicts, and unknowns, and requires a quote or location for every
proposed state, object, obligation, injury, resource change, or spatial relation.
Review it before making it canonical.

```powershell
human-writing-skills extract-ledger --draft chapters-01-10.md --context novel-ledger.md --output ledger-extraction-prompt.md
```

Use `.humanwriting.json` in a project root to persist only lightweight defaults:
style, document type, a relative ledger path, and lint allow-list entries. Explicit
CLI flags win, and the file cannot silently activate deep profiles or expensive
reference/source passes. See the [ledger extraction guide](docs/ledger-extraction.md).
Pass `--no-project-config` when a one-off command must ignore the nearest project file.

```json
{
  "style": "fiction",
  "document_type": "fiction",
  "context": "novel-ledger.md",
  "allow": ["END001"]
}
```

## Editor, CI, And Python Distribution

Text-facing commands accept `--draft -` for standard input. `lint --format github`
emits GitHub Actions annotations, while `list --kind rule` prints the current rule
catalog with severity, category, and repair direction.

```powershell
git diff -- docs\ | human-writing-skills lint --draft - --style general --format github --source-name docs-change.md
human-writing-skills list --kind rule --format json
```

Each GitHub Release builds a wheel and source distribution, then attaches them as
Release assets. PyPI publication uses GitHub Trusted Publishing only after the
repository variable `PYPI_PUBLISH_ENABLED=true` and the PyPI trusted publisher
have been configured; no PyPI token is stored in this repository.

It helps a writing agent move away from generic, template-shaped output and toward prose that has intention, texture, continuity, and genre discipline. The project is especially useful for long-form generation, where characters, settings, arguments, facts, and unresolved threads often drift after several passages.

The goal is not deception. The goal is better writing: clearer instructions, stronger revision habits, and reusable style constraints that make AI-assisted drafts feel edited by a human.

## Generation-Time Quality And Independent Review

`build`, `humanize`, and the MCP `compile_generation_prompt` tool now include a
compact generation-quality protocol by default. It prevents repeated rhetorical
moves, padded explanations, decorative details, invented specificity, translation-like
register, and unearned endings while writing. Fiction receives scene/dialogue priorities;
factual prose receives reader-purpose and evidence priorities. Full ending and other
deep audits remain opt-in. Direct emotion labels, deliberate repetition, smooth formal
prose, and useful conclusions are valid; no roughness or sensory-detail quota applies.

Explicit sources also support factual self-media and argumentative essays. Rewrites
with an original automatically preserve evidenced voice as well as meaning.

```powershell
human-writing-skills build --style self-media --task "Explain the supplied test results for buyers." --source test-notes.md
human-writing-skills critique --draft article.md --style self-media --output diagnosis.md
human-writing-skills compare-blind --original original.md --candidate revised.md --style self-media --brief writing-brief.md --output-dir blind-review
human-writing-skills stats --draft article.md --language de --format json
human-writing-skills evaluate-editorial --cases ballots.json --format json
```

Send only `blind-review/comparison.md` to an independent reviewer and retain
`version-key.json` locally. These commands compile prompts or aggregate recorded
ratings; they never call a model. See [editorial evaluation](docs/evaluation.md).
Real-world quality still requires independent fluent reviewers; unit tests do not
prove naturalness. Compact-review and deep-rewrite character budgets are 25,000 and
34,000 respectively (quick rewrite remains below 15,000 on the regression fixture).

## Long-Form Audit And Style Unification

Optional `chunk-audit --book-level` adds one whole-book architecture pass after
chunk reports for fiction/webnovels with at least three chapter headings. It
checks consequential choices, conflict development, time movement, and
over-explained ambiguity. It is not loaded into every chunk or serious report.

The executable `chunk-audit` workflow splits a year-long novel, article series, or
large report at natural boundaries. Each body span is audited once, with a small
read-only lead-in and the same user-confirmed style baseline plus outline or project ledger.
It writes independent chunk prompts, deterministic cross-chunk style diagnostics, and
a reconciliation prompt for model- or prompt-version drift in narration, character
dialogue, terminology, and section function.

For fiction, `--outline` or `--context` makes supported goals, knowledge, relationships,
limits, abilities, and speaker voice canonical. Without it, character inferences remain
provisional. News, academic, official, and report workflows instead align terminology,
facts, attribution, claim scope, and section purpose without loading fiction rules.

```powershell
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline novel-outline.md --output-dir novel-audit
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline novel-outline.md --book-level --output-dir book-audit
```

Discovery terms: **long-form audit, chunked manuscript audit, writing style
unification, style consistency review, character consistency audit, cross-chapter
continuity, novel audit, and report review**. See the
[long-form consistency guide](docs/long-form-consistency.md).

## Earned Scene And Document Endings

AI-assisted drafts often reach a real stopping point and then append a scenic dissolve,
shared silence, life lesson, future-facing reflection, or summary of what the scene
already showed. The `earned-ending-audit` finds this **reflective bookend / false
closure** pattern in Chinese and English by locating the last meaningful change and
applying a deletion test. It does not ban sunsets, silence, reflection, or lyrical prose.

- Fiction and webnovels stop on an earned consequence, decision, discovery, changed
  object, live pressure, or image whose meaning changed inside the scene.
- Hard news ends on the last useful verified fact, response, constraint, or next step;
  feature kickers must add meaning instead of manufacturing uplift.
- Academic, technical, and official writing ends with supported findings, limits,
  implications, decisions, owners, or deadlines rather than a ceremonial conclusion.

```powershell
human-writing-skills audit --draft chapter.md --document-type fiction --profile ending
human-writing-skills lint --draft chapter.md --style fiction
```

The full module loads only through the explicit `ending` profile, while `END001` provides a lightweight
deterministic preflight for narrative endings. Discovery terms: **AI story ending,
reflective ending, scene ending audit, chapter ending audit, formulaic conclusion,
false closure, AI reflective bookend, and can't-help-but-reflect ending**.

## Repetition, Exposition, And Scene Economy

Some drafts avoid obvious stock phrases yet still feel generated because they repeat a
line, image, action sequence, or narrator explanation with no changed consequence.
The narrative-only `repetition-exposition-audit` separates intentional refrains and
needed recap from exact echoes, repeated choreography, inventory-like viewpoint scans,
and explanation that merely tells the reader what dialogue or action already showed.

```powershell
# Isolated, token-bounded narrative pass
human-writing-skills audit --draft chapter.md --document-type fiction --profile repetition

# Long drafts: add it only when matching narrative cues appear
human-writing-skills pipeline --draft chapter.md --lint-style fiction --auto --output-dir chapter-audit
```

`REP001` flags a non-trivial verbatim sentence echo; `NAT005` and `NAT006` are
low-severity density prompts for repeated interpretive narration and action frames.
They are editing evidence, not authorship claims, and can be allowlisted. Quick
humanization and serious-document workflows do not load this module.

## Why This Exists

AI writing often fails in predictable ways:

| Problem | What this project adds |
| --- | --- |
| Generic "AI voice" | Concrete revision checks for rhythm, specificity, and empty phrasing |
| Repeated not-X/is-Y, is-X/not-Y, or chained Chinese 比 frames | Family- and density-based checks that preserve necessary correction and real comparison |
| Rewriting silently changes facts, uncertainty, or causal meaning | An opt-in original-text fidelity pass with a claim ledger and invention checks |
| Humanizing washes out hesitation, motifs, subtext, or speaker identity | A source-backed preservation ledger that separates useful ambiguity from real defects |
| Fluent-looking sentences drop a word, object, or connector clause | A separate final pass over predicate slots, parallel structure, and references |
| Surface AI patterns recur across a passage | Genre-aware checks for vague attribution, inflated significance, false ranges, synonym cycling, formatting habits, and comparison ladders |
| Fiction is chopped up by time/place mini-headings | Narrative-only checks that preserve titles and chapters but require scene changes to move through prose |
| A finished scene grows a scenic, reflective, or moralizing tail | Last-meaningful-change and deletion tests for false closure, with genre-specific ending contracts |
| A scene replays the same action, reaction, or explanation until it becomes mechanical | Narrative-only evidence for exact echoes, repeated action frames, viewpoint inventory, and redundant gloss |
| One style fits every genre | Separate Markdown `SKILLS` for different writing forms |
| Long text loses continuity | A compact ledger for facts, plot, promises, and voice anchors |
| Prose and character dialogue drift across months or model versions | A fixed baseline, canonical outline, unique audit chunks, and cross-chunk reconciliation |
| Dialogue sounds interchangeable or out of character | Generation and review against baseline voice, scene goal, knowledge, audience, and pressure |
| Dialogue ends in a stock gesture or scenic gloss instead of a real exchange | A dialogue-performance pass checks listener uptake, purposeful physical beats, and the changed option or carried debt |
| Dialect, honorifics, particles, or foreign language jump between characters | An evidence-backed language-identity card with motivated switch gates |
| A consequential line or action receives no uptake before the prose cuts away | Response-obligation checks and deferred interaction debt |
| Power, skill, authority, equipment, injury, or resources drift | Permanent/temporary state separation and earned transition gates |
| Prompts become messy | A CLI that compiles style, context, and task into one clean instruction pack |
| Advice stays abstract | Rules are written as observable editing actions |

## Built-In Style Skills

| Skill | Use it for | Main focus |
| --- | --- | --- |
| `fiction` | literary or commercial fiction | point of view, scene pressure, character behavior |
| `argumentative` | essays and opinion pieces | thesis, evidence, counterargument, logical flow |
| `news-report` | news-style reports | factual order, attribution, neutral wording |
| `self-media` | social posts and creator essays | useful voice without empty hype |
| `academic-paper` | research writing | cautious claims, structure, terminology |
| `formal-document` | official and administrative documents | authority, scope, responsibility, action, deadline, restrained register |
| `webnovel` | serialized genre fiction | hooks, payoffs, power rules, continuity |

## Deep Human-Trace Modules

These modules target deeper AI-writing artifacts, not only surface phrases.

| Module | What it repairs |
| --- | --- |
| `controlled-drift` | overly smooth logic, no associative movement, no unfinished thought |
| `narrative-bridges` | weak scene turns, generic transitions, paragraphs that do not cause each other |
| `relationship-state` | relationships that reset, dialogue without leverage, forgotten secrets or boundaries |
| `relationship-stance-audit` | audience-specific stance checks for rivalries, affairs, factions, hierarchy, sects, and family politics |
| `logic-causality-audit` | cause, timeline, knowledge, motive, rule, resource, and consequence failures |
| `character-consistency-audit` | character goal, voice, competence, boundary, knowledge, and change-gate drift |
| `dialogue-voice-audit` | character-fit dialogue plus verbal, physical, silent, interrupted, or deferred uptake for consequential turns |
| `dialogue-performance-audit` | uses the voice audit's response map to test whether a physical beat changes the exchange rather than decorating it |
| `speech-register-continuity` | evidence-backed language, dialect exposure, honorifics, particles, address, and switch gates |
| `capability-state-audit` | power, skill, authority, equipment, injury, resources, cooldowns, counters, and transitions |
| `serial-reentry` | recap dumps and chapter resets when prior chapters or a ledger are supplied |
| `long-form-style-consistency` | chunked long-form style, character-setting, and speaker-voice reconciliation |
| `chapter-momentum-audit` | atmosphere-only chapters, missing payoffs, discarded residue, and unsupported hooks |
| `world-ontology-audit` | incompatible era, technology, institution, social practice, or speculative rule |
| `process-earnedness-audit` | promised processes skipped before an unsupported result |
| `attention-budget-audit` | low-value expansion and semantic echoes displacing consequential material |
| `chapter-pattern-audit` | repeated chapter architecture across three or more chapters |
| `story-architecture-audit` | opt-in whole-book decisions, escalation, temporal shape, and ambiguity with chapter evidence |
| `narrative-distance-control` | unmotivated zoom, missing orientation, and viewpoint-distance drift |
| `imagery-load-audit` | stacked comparisons, competing sensory channels, and show-then-gloss repetition |
| `paragraph-rhythm-audit` | mechanical one-line paragraph runs and overloaded long blocks |
| `detail-disclosure-audit` | biography and appearance inventories delivered before the scene uses them |
| `scene-entry-audit` | exact-time/location/weather/outfit opening bundles before pressure-bearing action |
| `natural-measurement` | false precision: tiny exact measures and counted micro-actions in narrative prose |
| `cliche-phrase-audit` | stock phrases, generic body cues, empty emotion labels, and dead transitions |
| `formulaic-structure-audit` | triplets, bidirectional contrast frames, chained comparisons, and overly neat closure |
| `prose-progress-audit` | static paragraphs and pressure-bearing interactions abandoned before uptake or explicit deferral |
| `narrative-naturalness-audit` | in deep or explicit AI-trace review, catches recurring six-beat scene recipes and copied entry/closure cadence |
| `repetition-exposition-audit` | narrative-only exact echoes, repeated action choreography, inventory drift, and redundant explanatory narration |
| `earned-ending-audit` | reflective bookends, scenic dissolves, false closure, stock kickers, and conclusions added after the last meaningful change |
| `imperfect-prose` | prose that is too clean, too symmetrical, or too polished |
| `vocal-rhythm` | flat cadence and missing read-aloud breath points |
| `embodied-emotion` | emotion labels without body, action, contradiction, or perception |
| `cultural-anchors` | vacuum prose with no era, place, community, or material detail |
| `spatial-blocking` | character teleportation and confused front/back/left/right blocking |
| `occupancy-capacity` | over-occupied or mode-ambiguous seats, benches, beds, stools, aisles, and surfaces |
| `appearance-prop-continuity` | clothing, shoes, props, injuries, and daily-detail drift |
| `physical-continuity-audit` | optional light manual checklist; do not combine with the forensic physical profile |
| `proofreading-audit` | final omissions, predicate slots, stranded connectors, references, punctuation, naming, and layout |
| `style-matrix` | the mistake of applying one generic "human voice" to every genre |
| `editor-loop` | one-shot drafting without a critical human-editor pass |
| `ai-trace-rubric` | vague feedback like "sounds AI" without diagnosis |
| `reference-style-alignment` | explicit reference material into transferable voice features without copying content |
| `rewrite-fidelity` | meaning drift, invented specificity, reversed polarity, and altered uncertainty when an original is supplied |
| `voice-ambiguity-preservation` | over-clean rewrites that erase useful ambiguity, repetition, motifs, hesitation, subtext, or speaker markers |
| `humanize-examples` | an explicit-only before/after repair library; never loaded as a source or default style sample |
| `surface-pattern-audit` | recurrent formatting, false ranges, synonym cycling, and narrative mini-headings without global bans |
| `protected-content` | accidental changes to numbers, citations, equations, URLs, code, quotes, and required terms |
| `source-grounding` | claim-to-source checks for serious documents with explicit factual sources |

## Quick Start

```powershell
git clone https://github.com/whh110112/human-writing-skills.git
cd human-writing-skills
python -m pip install .

human-writing-skills list --kind style
human-writing-skills list --kind module
human-writing-skills build --style fiction --context examples/story-ledger.md --task "Write the next scene."
human-writing-skills humanize --draft chapter.md --style fiction --mode quick
human-writing-skills chunk-audit --draft full-novel.md --style fiction --outline novel-outline.md --output-dir novel-audit
human-writing-skills lint --draft chapter.md --style fiction
human-writing-skills verify --source original.md --candidate revised.md
```

You can also run directly from the source checkout with `python -m humanwriting.cli ...`. The `build` and `humanize` commands print instruction packs that can be pasted into Codex, ChatGPT, Claude, local LLM tools, or another writing agent.

## Quick Humanize

`humanize` is the low-friction rewrite route. It treats `--draft` as the original,
keeps the same language and genre by default, and preserves meaning before changing
surface style.

```powershell
# Minimum stack: surface patterns + fidelity + voice/ambiguity preservation
human-writing-skills humanize --draft chapter.md --style fiction

# Add structural editor passes only when the draft needs them
human-writing-skills humanize --draft article.md --style self-media --mode deep

# Examples remain opt-in and are never treated as factual or stylistic source material
human-writing-skills humanize --draft chapter.md --style fiction --with-examples
```

`quick` does not load cliche, formulaic-structure, paragraph-progress, or editor-loop
modules. `deep` adds those high-cost passes. `humanize-examples` loads only with
`--with-examples`; `voice-ambiguity-preservation` loads only for supplied-text
humanization or an explicit preservation audit.

## Multilingual Scope

The skill instructions have no Chinese-only gate: they can guide fiction and serious
prose in English, Japanese, French, Spanish, Portuguese, Arabic, Latin, and other
languages supported by the selected model. Deterministic lexical rules are naturally
language-specific, while structural continuity and review remain language-agnostic.
The narrative heading scanner recognizes time cards across the languages above, and
`stats` profiles Han, kana, Arabic, and several Latin-script language families. Use
genre context and human review for mixed-language or low-resource text.

Untyped serious-document detection uses multiple language-specific cues for
French, Spanish, Portuguese, Japanese, and Arabic as well as Chinese and English.
Set `--document-type` explicitly when cues are sparse. Non-Chinese, non-English
style statistics remain descriptive, without purportedly validated thresholds.

## Quality Evaluation

Developer-written multilingual seed cases test routing false positives/negatives
and rewrite-fidelity triage. They are regression examples, not native-speaker
validation. `evaluate` reports separately by language, genre, and reviewer status:

```powershell
human-writing-skills evaluate --cases tests/fixtures/quality/multilingual-benchmark.json
```

See the [annotation protocol](docs/evaluation.md) before making accuracy claims.

## Example Output Shape

```text
# Core Directive
# Continuity Protocol
# Selected Skill: fiction
# Project Context
# Task
# Output Contract
```

This format keeps the model focused on the current task while still carrying the previous facts, style decisions, and unresolved threads.

## Explicit Reference Style

Reference matching is opt-in. It activates only with `--reference`,
`--reference-style`, or explicit task wording such as "match this voice." A
continuity ledger by itself never activates it.

```powershell
human-writing-skills build `
  --style fiction `
  --context examples/story-ledger.md `
  --reference examples/reference-style-source.zh-CN.md `
  --task "Continue the scene while matching the reference's restrained rhythm."

human-writing-skills audit `
  --draft my-chapter.md `
  --reference examples/reference-style-source.zh-CN.md `
  --profile style-match
```

The compiler extracts point of view, rhythm, register, imagery, description,
dialogue cadence, emotion handling, and transitions. Plot facts still come from
`--context`; names, events, and distinctive phrases must not be copied from the
reference. See [docs/reference-style.md](docs/reference-style.md).

## Original-Text Fidelity

`verify` checks only exact protected tokens. For consequential revisions, also
run `verify-fidelity --source original.md --candidate revised.md`. It locates
changed claim spans and potential actor, negation, uncertainty, scope, or
attribution changes. Changed prose is **needs review**, never an automatic
semantic pass. Exit codes: 0 identical, 1 literal mismatch, 2 changed prose
requiring claim review. See [protected-content guidance](docs/protected-content.md).

Use `--original` only when revising an existing text and meaning must remain stable.
It activates a dedicated fidelity module for rewrite and review; ordinary drafting
does not pay this token cost.

```powershell
human-writing-skills build `
  --style self-media `
  --original original.md `
  --task "Rewrite for clarity without adding facts or strengthening claims."

human-writing-skills audit `
  --draft revised.md `
  --original original.md `
  --profile fidelity
```

`--original` is semantic authority, `--reference` is style evidence, and `--source`
is factual evidence for serious documents. They are deliberately isolated so a
style sample cannot rewrite facts and an original cannot silently become a style
target. See [docs/editing-tools.md](docs/editing-tools.md).

## Serious-Document Sources

`--source` is separate from `--reference`. It activates `source-grounding` only for
academic, news, legal, or technical work and builds a claim-to-source evidence map.
Fiction, webnovels, self-media, and casual answers do not auto-load it.

```powershell
human-writing-skills audit `
  --draft paper.md `
  --document-type academic-paper `
  --source study-a.md `
  --source study-b.md `
  --profile sources
```

The audit separates source existence from claim support. Without external registry
access, it marks citation metadata as unverified instead of inventing a verdict.

## Long-Form Continuity

For longer works, this project recommends a small ledger instead of relying only on a large context window. Use context in this order: canonical ledger, latest confirmed state, recent chapters, relevant retrieved older spans, then explicitly uncertain inference. Retrieved text is recall evidence and cannot overwrite a later canonical state.

The ledger tracks:

- fixed facts: names, dates, locations, relationships, rules, timeline
- active threads: unresolved conflicts, clues, promises, open arguments
- relationship state: who knows, wants, hides, owes, refuses, or holds leverage
- relationship stance: public/private posture, current audience, mention policy, forbidden leaks, and exception motives
- voice anchors: point of view, diction, directness, disclosure habits, domain limits, audience shifts, taboo phrases
- language identity: shared scene language, demonstrated dialect/second-language exposure, address forms, particles, and switch gates
- capability state: permanent power/skill/authority plus temporary injury, equipment, resources, cooldowns, counters, costs, and transition gates
- dialogue contract: who speaks to whom, why now, desired listener action, protected information, and intended state change
- interaction debt: which consequential line or action still awaits uptake, refusal, interruption, consequence, or delayed payoff
- current state: where the previous passage ended and what must connect next
- beat bridge: previous residue, entry pressure, micro-turn, and exit hook
- change log: what became newly true in the latest output

See [examples/story-ledger.md](examples/story-ledger.md) for a fiction example.

`speech-register-continuity` auto-loads only for fiction/webnovel dialogue when the task or ledger contains explicit language, regional, dialect, honorific, or register evidence. It can also be selected with `audit --profile register`; region or nationality never licenses an invented accent.

`capability-state-audit` loads during generation only when the current task names a capability constraint. Automatic pipeline review additionally requires context, so ordinary dialogue scenes do not pay its Token cost. Select it explicitly with `audit --profile capability --context ledger.md` when needed.

## Chatbox

Yes, this project works in Chatbox because it outputs plain text prompt packs. For long writing sessions, use the continuity ledger as the source of truth and paste the compiled prompt pack into Chatbox's system prompt or first message.

- English guide: [docs/chatbox.md](docs/chatbox.md)
- Chinese guide: [docs/chatbox.zh-CN.md](docs/chatbox.zh-CN.md)
- Ledger template: [examples/chatbox-ledger-template.md](examples/chatbox-ledger-template.md)

## Physical Continuity

For scenes where space matters, such as cars, elevators, hospital rooms, dining tables, and bedrooms, use `--strict-continuity`. It adds occupancy, spatial blocking, and appearance/prop generation guards. Use `audit --profile physical` for one evidence-first forensic pass on an existing draft; it owns capacity, blocking, appearance, props, barriers, reach, and body-state contradictions in one ledger.

```powershell
python -m humanwriting.cli build `
  --style fiction `
  --strict-continuity `
  --review `
  --context examples/vehicle-scene-ledger.md `
  --task "Continue the car argument. Every seat change must have an on-page transition. Keep clothing and props consistent."
```

- Guide: [docs/physical-continuity.md](docs/physical-continuity.md)
- Vehicle ledger example: [examples/vehicle-scene-ledger.md](examples/vehicle-scene-ledger.md)
- Capacity ledger template: [examples/capacity-ledger-template.md](examples/capacity-ledger-template.md)
- Capacity conflict example: [examples/capacity-conflict-draft.zh-CN.md](examples/capacity-conflict-draft.zh-CN.md)
- Draft audit example: [examples/problem-car-scene-draft.md](examples/problem-car-scene-draft.md)

## Relationship Stance Continuity

For scenes with rival factions, secret relationships, hierarchy, family politics,
office politics, or sect leaders, use `--deep-review` or add `relationship-stance-audit`.
It extracts each dialogue line as `speaker -> listener/audience -> referenced party`
and checks whether praise, criticism, comparison, naming, secrecy, and rank fit
the established relationship graph.

- Guide: [docs/relationship-stance-continuity.md](docs/relationship-stance-continuity.md)
- Ledger template: [examples/relationship-stance-ledger.zh-CN.md](examples/relationship-stance-ledger.zh-CN.md)

## Character- and Situation-Fit Dialogue

**Bidirectional interaction review addresses missing reactions and unfinished actions.**
It covers speech, wordless exchanges, and the viewpoint character's own responses.
Track initiator, affected recipient, separate speech/action obligations, evidence of
reception, and completed or pending state. A spoken answer may leave a simultaneous
action unfinished; one person's movement does not establish that another followed.
Refusal, unawareness, stillness, or delayed uptake can be valid. Clearly implied
completion needs no added gesture or emotional commentary.

Fiction and webnovel base Skills retain a brief check; detailed review uses the
existing on-demand `voice` profile. Automatic pipelines and deep chunk reviews also
route directed interpersonal actions. Use `--profile voice` when automatic cues miss
a language or phrasing. Reconciliation checks responses across chunk boundaries.
These are model-executed contextual checks; routing tests and deterministic lint do
not establish that a model will catch every omitted reaction.

`dialogue-voice-audit` and `dialogue-performance-audit` separate stable speaker baseline,
situation-driven modulation, and the action each turn is trying to perform. Occupation, class, region, and trait
labels supply possible knowledge, incentives, duties, and register pressure; they do
not substitute for personality. An explicit speech or interpersonal-action task activates
the module on demand. Review an existing scene with an independent `voice` pass:

```powershell
human-writing-skills audit `
  --draft my-dialogue-scene.md `
  --context my-novel-ledger.md `
  --profile voice
```

The audit separates contradiction from motivated contrast and checks scene purpose,
knowledge boundaries, practical constraints, response linkage, audience, and power.
A consequential line or action does not require a mechanical spoken reply, but it
must receive verbal, physical, silently legible, interrupted, or deliberately deferred
uptake before the prose shifts away. A physical beat is retained only when it changes
access, attention, leverage, permission, distance, or the next available action; the
module does not prescribe touch, gestures, weather, clothing, or scenery after every line.

If the draft already exists, use `audit`:

```powershell
python -m humanwriting.cli audit `
  --draft examples/problem-car-scene-draft.md `
  --context examples/vehicle-scene-ledger.md
```

## Project Layout

```text
humanwriting/        Python package and CLI
skills/              reusable writing SKILLS in Markdown
examples/            sample continuity ledgers and article briefs
tests/               standard-library unit tests
```

## CLI Usage

### Optional Narrative Modules

The narrative controls use progressive disclosure. Generation adds
the dialogue modules only when a fiction or webnovel task explicitly asks for a
speech-centered or character-interaction scene such as dialogue, negotiation, reunion,
testing, reconciliation, confrontation, a meeting, interrogation, or argument.
Narration-only and serious-document tasks do not trigger them. The `voice`,
`serial`, `world`, `process`, `momentum`, `salience`, `recurrence`, `repetition`, `texture`, and
`sources` and `preservation` audit profiles remain outside broad `full` review:

```powershell
human-writing-skills build --style fiction --task "Write a negotiation in which both speakers want different outcomes."
human-writing-skills build --style webnovel --context ledger.md --module serial-reentry --task "Continue chapter 18."
human-writing-skills audit --draft chapters.md --profile momentum
human-writing-skills audit --draft chapter.md --profile texture
human-writing-skills audit --draft chapter.md --profile process
human-writing-skills audit --draft chapters.md --profile recurrence
```

The dialogue modules model baseline speech, practical incentives, knowledge limits,
scene goals, response linkage, and purposeful performance beats without treating a job as a personality. `dialogue-voice-audit` owns response obligation and deferred interaction debt; `dialogue-performance-audit` only tests whether a selected physical beat earns its place. Use
`speech-register-continuity` for evidence-backed language identity, particles,
honorifics, and code-switching; use `capability-state-audit` for power and resource
state. Use `serial-reentry` only with
prior chapters or a ledger, `momentum` for a multi-chapter draft, and `texture` for
narrative distance, cinematic opening stacks, imagery load, paragraph fragmentation,
emotional over-explanation, and detail inventory. Use `world` only with explicit
setting constraints, `process` for consequential domain work, `salience` for long
drafts, `recurrence` for at least three chapters, `repetition` for long enough narrative
drafts with matching repetition/exposition cues, and `sources` only with serious
documents and factual source files.

During generation, world, process, and attention-budget modules activate only from
explicit setting, consequential-process, expansion, long-form, or dilution signals;
ordinary `--deep-review` does not load them.
The repetition/exposition module is likewise audit-first: use `--profile repetition`
or narrative `ai-trace`, and let `pipeline --auto` add its separate pass only when
the draft supplies matching cues.

### Audit Profiles

`audit` can load only the checks needed for the current pass:

| Profile | Purpose |
| --- | --- |
| `full` | Broad default audit; high-cost and strongly gated profiles remain separate |
| `logic` | Cause, timeline, knowledge, motive, rules, resources, and consequences |
| `character` | Character goal, voice, competence, boundaries, and change gates |
| `voice` | Speaker baseline, scene goal, role/knowledge limits, audience register, change gates, and response obligations |
| `register` | Language identity, dialect exposure, honorifics, particles, vocabulary, and code-switch gates |
| `capability` | Power, skill, authority, equipment, injury, resources, counters, and transition gates; requires `--context` |
| `serial` | Recap dumps, missing carryovers, and chapter resets; requires `--context` |
| `momentum` | Multi-chapter entry pressure, irreversible turns, payoff, residue, and exit pressure |
| `world` | Era, technology, institution, social-practice, and world-rule compatibility |
| `process` | Promise, attempt, resistance, judgment, cost, evidence, and earned result |
| `salience` | Long-draft attention allocation, dilution, and semantic echoes |
| `recurrence` | Chapter fingerprints and repeated architecture across three or more chapters |
| `repetition` | Narrative-only exact echoes, repeated action frames, and explanation that duplicates visible evidence |
| `texture` | Narrative distance, scene-entry load, imagery, paragraph cadence, and detail disclosure |
| `physical` | Position, capacity, reach, clothing, props, and injuries |
| `relationship` | Audience, stance, information permissions, rank, and secret leaks |
| `ai-trace` | Cliches, formulaic structure, static paragraphs, and other AI traces |
| `ending` | Last meaningful change, reflective bookends, false closure, and genre-specific ending function |
| `numbers` | False precision in action and emotion |
| `proofread` | Omissions, sentence slots, stranded connectors, references, punctuation, naming, and layout |
| `fidelity` | Meaning, entity, polarity, uncertainty, chronology, attribution, and invention checks; requires `--original` |
| `preservation` | Useful ambiguity, repetition, motifs, hesitation, subtext, and speaker identity; requires `--original` and explicit selection |
| `style-match` | Drift from explicitly supplied reference material; unavailable without a reference signal |
| `sources` | Claim grounding against factual sources; requires a serious document and `--source` |

Profiles can be combined, for example `--profile relationship --profile ai-trace`.

Ordinary generation loads only a lightweight sentence-completeness guard. Full
omission, missing-object, stranded-connector, and reference checks load only in the
`proofread` profile or pipeline proofreading stage, preserving the generation token budget.

### Chunked Long-Form Audit

Use `chunk-audit` when a manuscript exceeds one reliable context window or was written
across model, prompt, or time changes. It complements `pipeline`: chunking handles
manuscript size and cross-block drift, while the pipeline separates different review
responsibilities for one draft.

```powershell
human-writing-skills chunk-audit `
  --draft full-novel.md `
  --style fiction `
  --outline novel-outline.md `
  --reference approved-sample.md `
  --output-dir novel-consistency-audit
```

Without an explicit reference, `--baseline-chunk` selects a candidate manuscript block;
approve or correct it during baseline extraction. Reference prose supplies style evidence only. Fiction uses the
outline or ledger for character canon and permits earned development; serious reports
protect facts, numbers, terminology, attribution, and conclusion scope. Default body,
context, and baseline budgets keep the workflow usable on smaller-context models.

### Verified Agent Review For Long Documents

Add `--agent-mode deep` when coverage matters more than token cost. It writes an explicit
task graph in `agent-plan.json`, requires a Coverage Receipt from every reviewer, and
reserves report paths under `reports/`. After the baseline is approved, tasks that depend
only on `baseline` may run in parallel in fresh model conversations or API calls.

```powershell
human-writing-skills chunk-audit `
  --draft full-novel.md `
  --style fiction `
  --outline novel-outline.md `
  --agent-mode deep `
  --output-dir novel-agent-audit

human-writing-skills verify-chunk-audit `
  --package-dir novel-agent-audit
```

Do not run `9999-reconcile-prompt.md` until verification reports complete coverage. Deep
mode adds a paragraph-level prose pass for every block, an interaction pass where dialogue
or directed actions occur, and an evidence pass only for serious documents with explicit `--source` files.
Standard mode remains one complete audit per unique block. For an explicitly translated or
localized long document, add `--translationese`; it never activates merely because the text
uses another language.

- Guide: [docs/long-form-consistency.md](docs/long-form-consistency.md)

### Multi-Stage Pipeline

For high-precision review, generate independent single-purpose passes instead of asking one model to check everything at once:

```powershell
human-writing-skills pipeline `
  --draft my-chapter.md `
  --context my-novel-ledger.md `
  --auto `
  --output-dir chapter-audit
```

Run every stage in a fresh model conversation or independent API request. Automatic mode keeps logic, AI-trace, and proofreading stages, then adds focused stages only when their cues and gates match. `serial` and `capability` require context; `fidelity` requires an original; `salience` requires a long narrative of at least 4,000 characters; `recurrence` requires at least three chapters; `repetition` requires a sufficiently long narrative with repeated explanation or choreography cues; and `sources` requires both a serious document and explicit factual sources. The higher-cost `preservation` comparison is explicit-only: use `--stage preservation --original original.md`. Add `--with-stats` only when distributional diagnostics are useful. The manifest explains every selection and skip.

- Guide: [docs/audit-pipeline.md](docs/audit-pipeline.md)

### Deterministic Safeguards

Use `lint` for evidence-located pattern checks, `stats` for optional distributional
diagnostics, `fix` for conservative mechanical cleanup, and `verify` to catch
protected facts changed during rewriting. Scores and statistics are editing
heuristics, not authorship proof.

Protected-content instructions auto-load only for academic papers, formal documents,
news reports, and strongly identified legal or technical documents. Fiction, webnovels, casual
Q&A, playful text, and self-media do not auto-load them; use `--protect-content`
or `--protect-term` to override this gate.

With `--style fiction` or `--style webnovel`, `lint` also flags unrequested narrative
mini-headings and multilingual standalone time cards. It preserves work/chapter titles
and does not apply the rule to news or academic section headings. The repair restores
a prose transition; it does not merely delete the label and join two disconnected blocks.

```powershell
human-writing-skills lint --draft my-chapter.md --style fiction
human-writing-skills stats --draft my-chapter.md --style fiction
human-writing-skills fix --draft my-chapter.md --preview
human-writing-skills verify --source original.md --candidate revised.md --protect-term "Project Atlas"
```

- Pattern lint: [docs/pattern-linter.md](docs/pattern-linter.md)
- Fidelity, statistics, and conservative fixes: [docs/editing-tools.md](docs/editing-tools.md)
- Protected content: [docs/protected-content.md](docs/protected-content.md)

### Number Sense

Use this to catch false precision such as unnecessary exact centimeters, seconds, or micro-counts in emotional and bodily action, while preserving necessary numbers in medicine, forensics, engineering, architecture, news, and technical writing.

```powershell
python -m humanwriting.cli audit `
  --draft examples/false-precision-draft.zh-CN.md `
  --profile numbers
```

- Guide: [docs/number-sense.md](docs/number-sense.md)
- Example: [examples/false-precision-draft.zh-CN.md](examples/false-precision-draft.zh-CN.md)

### Common Writing Problems

The project converts recurring long-form writing problems into executable checks: stock phrasing, plastic prose, triplet structures, over-smooth transitions, static paragraphs, hollow emotion, cultural vacuum, and long-form drift.

- Rule map: [docs/forum-complaint-research.md](docs/forum-complaint-research.md)

List styles:

```powershell
python -m humanwriting.cli list
```

Build a prompt pack:

```powershell
python -m humanwriting.cli build `
  --style webnovel `
  --module narrative-bridges `
  --module relationship-state `
  --module natural-measurement `
  --module embodied-emotion `
  --module vocal-rhythm `
  --strict-continuity `
  --review `
  --context examples/story-ledger.md `
  --task "Continue chapter 3. Keep the confrontation unresolved but reveal one new clue."
```

The compact `--review` flag adds only:

- `editor-loop`: draft, diagnose, locally rewrite, then finalize
- `ai-trace-rubric`: score cognitive smoothness, generic diction, emotional flatness, rhythm monotony, context drift, weak beat bridges, relationship resets, false precision, cultural vacuum, over-clean prose, and closure addiction

The `--deep-review` flag adds the compact review plus:

- `relationship-stance-audit`: check speaker, listener, referenced party, secrecy, stance, rank, and audience permissions
- `cliche-phrase-audit`: check stock phrases, generic body cues, empty emotion labels, and dead transitions
- `formulaic-structure-audit`: check triplets, bidirectional contrasts, chained comparisons, and paragraphs that close too neatly
- `surface-pattern-audit`: check recurring significance, attribution, range, lexical, formatting, and mini-heading patterns in genre context
- `prose-progress-audit`: check whether each paragraph advances facts, relationships, evidence, action, or pressure
- `narrative-naturalness-audit`: in deep or explicit AI-trace review, check recurring scene-entry/closure recipes across six or more beats; local phrase, structure, and uptake findings stay with their owning modules
- `natural-measurement`: check false precision in fiction, webnovels, and self-media

The `--strict-continuity` flag adds:

- `spatial-blocking`: position and movement checks
- `occupancy-capacity`: physical resource mode, capacity, occupancy, and transformation checks
- `appearance-prop-continuity`: clothing, shoes, props, and body-state checks

Use `audit --profile physical` for the final physical-state contradiction pass. The optional `physical-continuity-audit` is a light manual checklist and cannot be combined with this forensic profile.

Run tests:

```powershell
python -m unittest discover -s tests -v
```

## Writing Philosophy

Good AI-assisted prose should be:

- situated: it knows who is speaking, what changed, and why this passage exists
- specific: it uses details that belong to this topic, not any topic
- continuous: it respects previous facts, costs, injuries, claims, and promises
- shaped: it understands the genre before choosing structure and diction
- revised: it removes filler, canned transitions, and decorative certainty

## Editorial Guardrails

This project avoids claiming that any tool can perfectly hide authorship or beat detectors. It focuses on craft: voice, context, genre, revision, and continuity.

When studying published work, use short analysis, public-domain sources, licensed material, or your own examples. Do not copy protected passages into skills.

## Contributing

Contributions are welcome. Useful additions include:

- new Markdown skills
- Chinese and multilingual style packs
- model-specific adapters
- stronger continuity ledger examples
- tests for prompt compilation and context preservation

Please keep each skill practical. A good rule should tell the model what to do, what to avoid, and how to check the result.

## License

MIT. See [LICENSE](LICENSE).
