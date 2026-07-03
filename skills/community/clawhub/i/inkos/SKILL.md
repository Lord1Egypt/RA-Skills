---
name: inkos
description: Story Creation AI Agent with Studio Chat, CLI, and TUI - use for long-form novels, standalone short fiction, scripts, storyboards, interactive-film projects, open-world / branching play, fan fiction, spinoffs, style imitation, continuations, covers, EPUB export, AIGC detection, and project analytics. Includes runtime skills, traceable web research, governed context assembly, protected/compressible context budgeting, persistent story state, multi-model routing, cover/image services, custom OpenAI-compatible providers, and InkOS Studio web UI.
version: 2.5.0
metadata: { "openclaw": { "emoji": "📖", "requires": { "bins": ["inkos", "node"], "env": ["OPENAI_API_KEY"] }, "primaryEnv": "OPENAI_API_KEY", "homepage": "https://github.com/Narcooo/inkos", "install": [{ "id": "npm", "kind": "node", "package": "@actalk/inkos", "label": "Install InkOS (npm)" }] } }
---

# InkOS - Story Creation AI Agent

InkOS is a story creation AI agent for long-form novels, short fiction, scripts, storyboards, interactive-film projects, fan works, continuations, covers, and open-world / branching interactive play. Prefer the Studio Chat / action-surface workflow for natural-language requests: the model proposes or invokes typed actions, InkOS executes them, and completion is derived from real tool results and files, not from prose claims.

Long-form writing still uses the chapter pipeline internally:
- **Input governance**: Architect / Planner / Composer preserve author intent, current focus, outline sections, and relevant truth files instead of injecting everything blindly.
- **Writing**: Writer produces prose with length governance, craft rules, and context selected for the current task.
- **Settlement and review**: Observer / Reflector update runtime state; Auditor checks continuity and quality; Reviser handles critical issues. The default write cycle keeps automatic repair conservative and leaves unresolved issues visible for human or agent follow-up.

Truth files are persisted as schema-validated JSON (`story/state/*.json`) with markdown projections for human readability. SQLite temporal memory database (`story/memory.db`) enables relevance-based retrieval on Node 22+.

## v1.6.0 Mental Model

Treat InkOS as a confirmable action system, not a bag of prompt shortcuts.

- Natural-language requests should go through Studio Chat / TUI / `inkos interact` whenever possible.
- Do not infer success from assistant prose. A book, short, cover, or play step is complete only when the corresponding tool result and files exist.
- Use `short_fiction_run` only for a standalone short-fiction package.
- Use `generate_cover` only for cover generation/regeneration.
- Use `play_start` / `play_step` for Open World or Branching Interactive sessions.
- Use script / storyboard / interactive-film tools only for production artifacts that should be saved and exported, not for casual discussion.
- Use `research_web` only when the user explicitly asks for external facts, market references, era/profession details, or worldbuilding research. Research reports are reference material and do not automatically mutate canon or prose.
- Use long-form chapter tools only for existing long-form books.
- Runtime skills provide professional rules, prompt packs, and context requirements. They do not grant new file, network, image, or writing permissions by themselves.
- Context is governed: protected facts and current intent should not be silently compressed away; compressible history may be summarized when the context budget is tight.

v1.6 adds interactive-film production, runtime skills, traceable web research, and stability fixes for targeted chapter edits, chapter index preservation, and model/service switching. Still surface unresolved audit issues plainly instead of claiming they were fixed.

## When to Use InkOS

- **English novel writing**: Native English support with 10 genre profiles (LitRPG, Progression Fantasy, Isekai, etc.). Set `--lang en`
- **Chinese web novel writing**: 5 built-in Chinese genres (xuanhuan, xianxia, urban, horror, other)
- **Fan fiction**: Create fanfic from source material with 4 modes (canon, au, ooc, cp)
- **Batch chapter generation**: Generate multiple chapters with consistent quality
- **Import & continue**: Import existing chapters from a text file, reverse-engineer truth files, and continue writing
- **Style imitation**: Analyze and adopt writing styles from reference texts
- **Spinoff writing**: Write prequels/sequels/spinoffs while maintaining parent canon
- **Standalone short fiction**: Generate a complete short-fiction package with outline, draft, review artifacts, synopsis, selling points, and optional cover image
- **Cover generation**: Generate or regenerate only a cover prompt and cover image from a title, synopsis, or visual direction without rerunning story writing
- **Interactive worlds**: Start Open World or Branching Interactive sessions with world contracts, character agents, inventory/evidence/relationship state, guided choices, free actions, and optional image generation
- **Interactive-film projects**: Create playable branch graphs, variables/flags, relationship state, endings, node images, and exportable interactive project packages
- **Scripts and storyboards**: Convert ideas, outlines, or prose into script/storyboard deliverables while preserving user format choices
- **Runtime skills**: Load built-in or project-local skills, allow Chat to auto-select them, or force a skill with `@skill-id`
- **Traceable web research**: Create sourced Markdown reports for facts, era/profession details, markets, and worldbuilding references
- **Quality auditing**: Detect AI-generated content and perform 33-dimension quality checks
- **Genre exploration**: Explore trends and create custom genre rules
- **Analytics**: Track word count, audit pass rate, and issue distribution per book

## Initial Setup

### First Time Setup
```bash
# Initialize a project directory (creates config structure)
inkos init my-writing-project

# Configure your LLM provider (OpenAI, Anthropic, or any OpenAI-compatible API)
# Prefer --api-key-env so the key never appears in shell history:
export OPENAI_API_KEY=sk-xxx
inkos config set-global --provider openai --base-url https://api.openai.com/v1 --api-key-env OPENAI_API_KEY --model gpt-4o
# For compatible/proxy endpoints, use --provider custom and point ONLY to trusted endpoints:
# inkos config set-global --provider custom --base-url https://your-trusted-proxy.com/v1 --api-key-env OPENAI_API_KEY --model gpt-4o
```

### Multi-Model Routing (Optional)
```bash
# Assign different models to different agents — balance quality and cost
inkos config set-model writer claude-sonnet-4-20250514 --provider anthropic --base-url https://api.anthropic.com --api-key-env ANTHROPIC_API_KEY
inkos config set-model auditor gpt-4o --provider openai
inkos config show-models
```
Agents without explicit overrides fall back to the global model.

### Provider setup tip

When the user needs an aggregator provider, point them to Studio's service settings. InkOS includes kkaiapi and OpenRouter as optional aggregator choices. For kkaiapi, use:
- Chinese website: https://kkaiapi.com/
- English website: https://en.kkaiapi.com/
- Chinese API docs: https://kkaiapi.com/docs
- English API docs: https://en.kkaiapi.com/docs
- Chinese models/pricing: https://kkaiapi.com/models
- English models/pricing: https://en.kkaiapi.com/models

### View System Status
```bash
# Check installation and configuration
inkos doctor

# View current config
inkos status
```

## Common Workflows

### Workflow 1: Create a New Novel

1. **Initialize and create book**:
   ```bash
   inkos book create --title "My Novel Title" --genre xuanhuan --chapter-words 3000
   # Or with a creative brief (your worldbuilding doc / ideas):
   inkos book create --title "My Novel Title" --genre xuanhuan --chapter-words 3000 --brief my-ideas.md
   ```
   - Genres: `xuanhuan` (cultivation), `xianxia` (immortal), `urban` (city), `horror`, `other`
   - Returns a `book-id` for all subsequent operations

2. **Generate initial chapters** (e.g., 5 chapters):
   ```bash
   inkos write next book-id --count 5 --words 3000 --context "young protagonist discovering powers"
   ```
   - The `write next` command runs the full pipeline: draft → audit → revise
   - `--context` provides guidance to the Architect and Writer agents
   - Returns JSON with chapter details and quality metrics

3. **Review and approve chapters**:
   ```bash
   inkos review list book-id
   inkos review approve-all book-id
   ```

4. **Export the book** (supports txt, md, epub):
   ```bash
   inkos export book-id
   inkos export book-id --format epub
   ```

### Workflow 2: Continue Writing Existing Novel

1. **List your books**:
   ```bash
   inkos book list
   ```

2. **Continue from last chapter**:
   ```bash
   inkos write next book-id --count 3 --words 2500 --context "protagonist faces critical choice"
   ```
   - InkOS maintains structured runtime state, readable Markdown projections, control docs, and temporal memory for consistency
   - If only one book exists, omit `book-id` for auto-detection

3. **Review and approve**:
   ```bash
   inkos review approve-all
   ```

### Workflow 2.5: Shared Natural-Language Control (Recommended For OpenClaw)

When InkOS is being driven by OpenClaw or another external agent, prefer the shared interaction executor instead of stitching together many ad-hoc CLI calls:

```bash
inkos interact --json --message "continue the current book, but keep the pacing tighter"
inkos interact --json --message "rewrite chapter 3"
inkos interact --json --message "start an open-world detective game about a locked archive room"
```

The current JSON payload contains:
- assistant response text
- interaction session id / session kind / active book id when bound

Real completion still comes from tool results and files. Do not treat assistant prose alone as proof that a book, chapter, short, cover, or play step was created.

Use this as the primary OpenClaw entry because it shares the same control layer as the project TUI.

### Workflow 2.6: Steering Chapter Focus Before Writing

Use this when the user says things like "pull focus back to the mentor conflict", "pause the merchant guild subplot", or "change what the next chapter should prioritize".

1. **Update the book-level control docs when needed**:
   - Use `update_author_intent` to change the long-horizon identity of the book
   - Use `update_current_focus` to change the next 1-3 chapters' focus

2. **Compile the next chapter intent**:
   ```text
   plan_chapter(bookId, guidance?)
   ```
   - Generates `story/runtime/chapter-XXXX.intent.md`
   - Use this to verify what the system thinks the next chapter should do

3. **Compose the actual runtime input package**:
   ```text
   compose_chapter(bookId, guidance?)
   ```
   - Generates `story/runtime/chapter-XXXX.context.json`
   - Generates `story/runtime/chapter-XXXX.rule-stack.yaml`
   - Generates `story/runtime/chapter-XXXX.trace.json`

4. **Only then write**:
   - `write_draft` if the user wants intermediate review
   - `write_full_pipeline` if they want the usual write → audit → revise flow

Recommended orchestration:
- user asks to redirect focus
- `update_current_focus`
- `plan_chapter`
- `compose_chapter`
- inspect the resulting intent/paths
- `write_draft` or `write_full_pipeline`

### Workflow 3: Import Existing Chapters & Continue

Use this when you have an existing novel (or partial novel) and want InkOS to pick up where it left off.

1. **Import from a single text file** (auto-splits by chapter headings):
   ```bash
   inkos import chapters book-id --from novel.txt
   ```
   - Automatically splits by `第X章` pattern
   - Custom split pattern: `--split "Chapter\\s+\\d+"`

2. **Import from a directory** of separate chapter files:
   ```bash
   inkos import chapters book-id --from ./chapters/
   ```
   - Reads `.md` and `.txt` files in sorted order

3. **Resume interrupted import**:
   ```bash
   inkos import chapters book-id --from novel.txt --resume-from 15
   ```

4. **Continue writing** from the imported chapters:
   ```bash
   inkos write next book-id --count 3
   ```
   - InkOS rebuilds structured state, chapter summaries, hooks, character relationships, readable projections, and a style guide from the imported chapters
   - Generates a style guide from the existing text
   - New chapters maintain consistency with imported content

### Workflow 4: Style Imitation

1. **Analyze reference text**:
   ```bash
   inkos style analyze reference_text.txt
   ```
   - Examines vocabulary, sentence structure, tone, pacing

2. **Import style to your book**:
   ```bash
   inkos style import reference_text.txt book-id --name "Author Name"
   ```
   - All future chapters adopt this style profile
   - Style rules become part of the Reviser's audit criteria

### Workflow 5: Spinoff/Prequel Writing

1. **Import parent canon**:
   ```bash
   inkos import canon spinoff-book-id --from parent-book-id
   ```
   - Creates links to parent book's world state, characters, and events
   - Reviser enforces canon consistency

2. **Continue spinoff**:
   ```bash
   inkos write next spinoff-book-id --count 3 --context "alternate timeline after Chapter 20"
   ```

### Workflow 6: Fine-Grained Control (Draft → Audit → Revise)

If you need separate control over each pipeline stage:

1. **Generate draft only**:
   ```bash
   inkos draft book-id --words 3000 --context "protagonist escapes" --json
   ```

2. **Audit the chapter** (33-dimension quality check):
   ```bash
   inkos audit book-id chapter-1 --json
   ```
   - Returns metrics across 33 dimensions including pacing, dialogue, world-building, outline adherence, and more

3. **Revise with specific mode**:
   ```bash
   inkos revise book-id chapter-1 --mode polish --json
   ```
   - Modes: `polish` (minor), `spot-fix` (targeted), `rewrite` (major), `rework` (structure), `anti-detect` (reduce AI traces)

### Workflow 7: Monitor Platform Trends

```bash
inkos radar scan
```
- Analyzes trending genres, tropes, and reader preferences
- Informs Architect recommendations for new books

### Workflow 8: Detect AI-Generated Content

```bash
# Detect AIGC in a specific chapter
inkos detect book-id

# Deep scan all chapters
inkos detect book-id --all
```
- Uses 11 deterministic rules (zero LLM cost) + optional LLM validation
- Returns detection confidence and problematic passages

### Workflow 9: View Analytics

```bash
inkos analytics book-id --json
# Shorthand alias
inkos stats book-id --json
```
- Total chapters, word count, average words per chapter
- Audit pass rate and top issue categories
- Chapters with most issues, status distribution
- **Token usage stats**: total prompt/completion tokens, avg tokens per chapter, recent trend

### Workflow 10: Write an English Novel

```bash
# Create an English LitRPG novel (language auto-detected from genre)
inkos book create --title "The Last Delver" --genre litrpg --chapter-words 3000

# Or set language explicitly
inkos book create --title "My Novel" --genre other --lang en

# Set English as default for all projects
inkos config set-global --lang en
```
- 10 English genres: litrpg, progression, isekai, cultivation, system-apocalypse, dungeon-core, romantasy, sci-fi, tower-climber, cozy
- Each genre has dedicated pacing rules, fatigue word lists (e.g., "delve", "tapestry", "testament"), and audit dimensions
- Use `inkos genre list` to see all available genres

### Workflow 11: Fan Fiction

```bash
# Create a fanfic from source material
inkos fanfic init --title "My Fanfic" --from source-novel.txt --mode canon

# Modes: canon (faithful), au (alternate universe), ooc (out of character), cp (ship-focused)
inkos fanfic init --title "What If" --from source.txt --mode au --genre other
```
- Imports and analyzes source material automatically
- Fanfic-specific audit dimensions and information boundary controls
- Ensures new content stays consistent with source canon (or deliberately diverges in au/ooc modes)

### Workflow 12: Edit Persistent Text Through Chat

Use Studio Chat or `inkos interact` for small, explicit edits to generated text artifacts. Treat the chat layer like an external editor: it may edit persisted files, then the writing pipeline can continue from the updated state.

```bash
inkos interact --book my-book --json --message "把第 3 章里那句过长的解释删短一点，但不要改剧情事实"
inkos interact --json --message "把 covers/demo/cover-prompt.md 里的人物拉近一点，标题字更大"
```
- Use for clear text edits, cover prompt edits, and control-document edits.
- Do not infer success from the assistant's prose; check the tool result or changed file.
- For broad story direction changes, prefer updating `author_intent.md` / `current_focus.md`, then run `plan` / `compose` before writing.

### Workflow 13: Explicit Rename / Replacement Requests

When the user asks for a rename or targeted replacement, keep the request explicit and scoped. Prefer Studio Chat / `inkos interact` over hidden slash shortcuts; the agent should route the edit through the shared action surface and report which file changed.

Examples:
- "把当前书里角色 林烬 改成 张三，先说明会影响哪些文件。"
- "只改第 5 章，把这句旧文本换成新文本，改完标记需要复核。"

### Workflow 14: Interactive TUI Dashboard

```bash
inkos tui
```
- Launches a full-screen Ink + React dashboard with conversational creation
- Slash command autocomplete (Tab), input history (arrow keys)
- Themed activity animations per operation (writing, auditing, revising, planning)
- Bilingual i18n (Chinese / English)
- Shares the same interaction kernel as `inkos interact` and Studio

### Workflow 15: Standalone Short Fiction Package

Use this when the user wants a complete short story or short-fiction deliverable that is separate from the active long-form book.

```bash
inkos short run \
  --direction "modern short fiction marriage reversal evidence-driven heroine" \
  --chapters 12 \
  --chars 1000
```

Outputs are written under `shorts/<story-name>/final/`:
- `full.md` — complete short-fiction manuscript
- `sales-package.md` — synopsis and selling points
- `cover-prompt.md` — cover prompt
- `cover.png` — cover image when a cover provider is configured

For OpenClaw/Studio/agent orchestration, call the `short_fiction_run` tool when the user asks for a new complete short-fiction package. Do not use it for the next chapter of an existing long-form book.

### Workflow 16: Standalone Cover Tool

Use this when the user only wants a cover for an existing title, synopsis, or visual direction. Do not rerun the short-fiction pipeline.

In Studio or agent mode, ask naturally:

```text
Generate a short-fiction cover for "The Divorce Papers He Regretted", modern city, high-drama reversal.
```

For tool-using agents, call `generate_cover` with:
- `title` — required
- `intro` or `sellingPoints` — optional story context
- `coverPrompt` — optional visual direction
- `outputDir` — optional; defaults to `covers/<title>/`

The standalone cover tool writes:
- `covers/<title>/cover-prompt.md`
- `covers/<title>/cover.png`

If cover image generation fails, report the provider/configuration error plainly. Do not rewrite the story, do not rerun `short_fiction_run`, and do not suggest unrelated external tools unless the user asks.

### Workflow 17: Open World / Branching Interactive Play

Use this when the user wants to play inside an interactive world instead of generating a finished manuscript.

In Studio or agent mode, ask naturally:

```text
Create a Warcraft-like border watchtower open world. Time can advance differently by action: patrols take an hour, training can take days. Equipment should show rarity through material and atmosphere, not stat blocks.
```

For tool-using agents:
- Call `play_start` when there is no active world/run yet, or when the user explicitly asks to start a new world.
- Call `play_step` when the user performs an action inside an existing world.
- Keep Open World free-form: do not force clickable choices unless the current session is Branching Interactive.
- If the user changes world rules, persona, visual contract, or character behavior, treat it as a world-state edit or a new instruction for the next step, not as long-form chapter writing.
- If image generation is configured, let Play generate scene / character / item / evidence images through the Play image path. Do not call the short-fiction cover tool for Play scene images.

### Workflow 18: Runtime Skills

Use this when the user wants reusable professional rules, a domain-specific writing mode, or a forced capability for the current Chat turn.

Project-local skills live at:

```text
.inkos/skills/<skill-id>/SKILL.md
```

External skill directories can be loaded with:

```bash
export INKOS_SKILL_DIRS=/abs/path/to/skills
```

Guidelines for agent orchestration:
- Let InkOS auto-select skills when the user gives a natural request such as "make this a detective evidence-chain open world".
- Force a skill by including `@skill-id` in the user message when the user explicitly chooses one.
- Treat skills as expertise packets: they can add rules, prompt packs, context needs, and retrieval guidance.
- Do not treat skills as permissions. File edits, book creation, chapter writing, image generation, and exports still require the normal InkOS tools and confirmation gates.

### Workflow 19: Traceable Web Research

Use this when the user asks for real-world references, external facts, era/profession details, market references, or worldbuilding research.

For tool-using agents, call `research_web` with:
- `topic` — the research question
- `purpose` — `worldbuilding`, `era`, `profession`, `market`, `fact-check`, or `general`
- `depth` — optional: `quick`, `standard`, or `deep`

The tool writes a Markdown report under:

```text
.inkos/research/
```

The report includes sources, claims, unknowns, conflicts, query logs, and confidence. It is reference material only. If research should change canon, wait for explicit user confirmation and then use the normal truth-file editing path.

Search credentials are user/project supplied. Studio can configure a Tavily-compatible search API, or the server can use `TAVILY_API_KEY` from the environment.

### Workflow 20: Script, Storyboard, and Interactive-Film Creation

Use this when the user wants a production artifact rather than a casual answer:
- Script: dramatic scenes, dialogue, acts, episode structure, or format-specific script drafts.
- Storyboard: visual beats, shot descriptions, image prompts, and scene-by-scene production notes.
- Interactive film: branch graph, choices, variables/flags, relationship state, endings, node images, and exportable project package.

In Studio Chat, these actions should be proposed with a confirmation card first. After confirmation, InkOS writes the artifact and reports the saved files. Do not hand-write a fake "created" result in prose.

## InkOS Studio (Web Workbench)

`inkos studio` launches a local web UI (default port 4567) that provides a visual interface for all InkOS operations:

- **Book management** — create, delete, export (TXT/MD/EPUB), configure per-book settings
- **Short fiction & cover tools** — generate independent short-fiction packages, synopsis/selling points, cover prompts, and standalone covers
- **Open World / Branching Interactive** — start and continue interactive worlds with world contracts, free actions, clickable choices, HUD state, and image generation
- **Interactive-film workbench** — create and inspect branch nodes, variables/flags, endings, node images, and export packages
- **Script / storyboard tools** — generate production-oriented script and storyboard files from ideas, prose, or reference notes
- **Runtime Skill management** — list built-in skills, add project-local skills, edit `.inkos/skills/<id>/SKILL.md`, and force skills from Chat
- **Research search provider** — configure external web search API credentials for `research_web`
- **Chapter review & editing** — approve/reject drafts, edit content inline, multi-mode revision (polish/spot-fix/rewrite/anti-detect)
- **Real-time writing progress** — SSE-based live updates during chapter generation
- **Market radar** — AI-powered trend analysis with platform/genre recommendations
- **Analytics** — word count, audit pass rate, chapter ranking, token usage
- **AI detection** — scan chapters for AI-generated content
- **Style analysis** — analyze reference texts and import writing styles
- **Genre management** — create/customize genre profiles with fatigue words, pacing rules, audit dimensions
- **Daemon control** — start/stop background writing with event log
- **Truth file editor** — view and edit canonical knowledge base per book
- **Config editor** — LLM provider, model routing, cover/image services, notifications

```bash
inkos studio              # Start on default port 4567
inkos studio -p 8080      # Start on custom port
```

The **Studio Chat** surface shares the same action kernel as TUI and CLI. It can answer questions, propose/confirm creation actions, run Short, generate covers, start Play, edit persistent text artifacts, and invoke long-form writing operations.

## Advanced: Natural Language Agent Mode

For flexible, conversational requests:

```bash
inkos agent "写一部都市题材的小说，主角是一个年轻律师，第一章三千字"
```
- Agent interprets natural language and invokes appropriate commands
- Useful for complex multi-step requests

## Input Governance Tools

These tools are the preferred control surface for chapter steering:

- `plan_chapter(bookId, guidance?)`
  - Generates chapter intent for the next chapter
  - Use before writing when the user wants to change focus

- `compose_chapter(bookId, guidance?)`
  - Generates runtime context/rule-stack/trace artifacts
  - Use after planning and before writing

- `update_author_intent(bookId, content)`
  - Rewrites `story/author_intent.md`
  - Use for long-horizon changes to the book's identity

- `update_current_focus(bookId, content)`
  - Rewrites `story/current_focus.md`
  - Use for local steering over the next 1-3 chapters

## Creative, Research, and Play Agent Tools

These are the preferred tools when InkOS is driven by OpenClaw, Studio chat, or `inkos agent`:

- `short_fiction_run`
  - Creates an independent short-fiction package from a direction
  - Runs outline → outline review/revision → full draft → draft review/revision → synopsis/selling points/cover prompt → optional cover image
  - Writes to `shorts/<story-name>/`
  - Use only when the user asks for a separate complete short story / short-fiction deliverable

- `generate_cover`
  - Generates only a cover prompt and cover image
  - Writes to `covers/<title>/` by default
  - Use when the user asks to create or regenerate a cover for an existing title, synopsis, or completed short
  - Also use when the user changes the cover prompt through chat; pass the revised visual direction as `coverPrompt` and reuse the existing `outputDir` when available
  - Do not rerun story generation unless the user explicitly asks for a new story

- `play_start`
  - Starts a new Open World or Branching Interactive run
  - Use when the user asks to play in a world, simulate an interactive story, create a game-like scene, or start a free-action/choice-based session
  - The user's world contract should carry time rules, character agency, item/evidence rules, tone, genre, and visual style when provided

- `play_step`
  - Advances an existing Play run by one user action
  - Use for free-form actions such as "inspect the letter", "talk to the guard", "train for three days", or "choose option 2"
  - Do not use it to write the next chapter of a long-form book

- `research_web`
  - Collects external sources and writes a traceable Markdown research report
  - Use only for explicit research/fact-check/worldbuilding/market requests
  - Never mutate canon or prose directly from research output without explicit user confirmation

- Script / storyboard / interactive-film creation tools
  - Use when the user wants saved production artifacts
  - Preserve the user's requested format, market, target audience, and export needs
  - Do not use these tools for casual analysis unless the user asks to create deliverables

`write_truth_file` remains available for broad file edits, but prefer the dedicated control tools above for input-governance changes.

## Key Concepts

### Book ID Auto-Detection
If your project contains only one book, most commands accept `book-id` as optional. You can omit it for brevity:
```bash
# Explicit
inkos write next book-123 --count 1

# Auto-detected (if only one book exists)
inkos write next --count 1
```

### --json Flag
All content-generating commands support `--json` for structured output. Essential for programmatic use:
```bash
inkos draft book-id --words 3000 --context "guidance" --json
```

### Long-Term Memory
InkOS maintains each book's memory in three layers:
- **Structured state**: `story/state/*.json` is the authoritative runtime state, validated by Zod schemas.
- **Readable projections**: `current_state.md`, `pending_hooks.md`, `chapter_summaries.md`, `character_matrix.md`, and related Markdown files are for humans and debugging.
- **Temporal memory**: `story/memory.db` on Node 22+ supports relevance-based retrieval of facts, hooks, and chapter summaries.

Agents use the governed composer to select the relevant parts for the current task instead of blindly injecting every file. During `import chapters`, InkOS rebuilds structured state and projections from existing content via the ChapterAnalyzerAgent.

### Multi-Phase Writer Architecture
The Writer operates across multiple phases with specialized agents:
- **Planner**: Generates chapter intent with structured hook agenda (mustAdvance, eligibleResolve, staleDebt) based on memory retrieval.
- **Composer**: Selects relevant context from structured state, control docs, readable projections, and retrieval results, then compiles rule stack and runtime artifacts.
- **Phase 1 (Creative, temp 0.7)**: Generates prose with length governance, English variance brief (anti-repetition), and dialogue-driven guidance.
- **Phase 2a (Observer, temp 0.5)**: Over-extracts 9 categories of facts from the chapter text.
- **Phase 2b (Reflector, temp 0.3)**: Outputs a JSON delta with hookOps (upsert/mention/resolve/defer), currentStatePatch, and chapterSummary. Code-layer validates via Zod schema and applies immutably.
- **Normalizer**: Single-pass compress/expand to bring chapter length into the target band. Safety net rejects destructive normalization (>75% content loss).
- **Auditor**: 33-dimension check including hook health analysis (stale debt, burst detection, no-advance warnings).
- **Reviser**: Attempts one configured repair pass for critical issues, then keeps unresolved findings visible for human or agent follow-up.

Truth files use structured JSON (`story/state/*.json`) as the authoritative source, with markdown projections for human readability. Hook admission control prevents duplicate/family hooks from inflating the hook table.

### Context Guidance
The `--context` parameter provides directional hints to the Writer and Architect:
```bash
inkos write next book-id --count 2 --context "protagonist discovers betrayal, must decide whether to trust mentor"
```
- Context is optional but highly recommended for narrative coherence
- Supports both English and Chinese

## Genre Management

### View Built-In Genres
```bash
inkos genre list
inkos genre show xuanhuan
```

### Create Custom Genre
```bash
inkos genre create my-genre --name "My Genre"
# Options: --numerical, --power, --era
inkos genre create dark-xuanhuan --name "Dark Xuanhuan" --numerical --power
```

### Copy Built-in Genre for Customization
```bash
inkos genre copy xuanhuan
# Copies to project genres/ directory for editing
```

## Command Reference Summary

| Command | Purpose | Notes |
|---------|---------|-------|
| `inkos init [name]` | Initialize project | One-time setup |
| `inkos book create` | Create new book | Returns book-id. `--brief <file>`, `--lang en/zh`, `--genre litrpg/progression/...` |
| `inkos book list` | List all books | Shows IDs, statuses |
| `inkos write next` | Full pipeline (draft→audit→revise) | Primary workflow command |
| `inkos draft` | Generate draft only | No auditing/revision |
| `inkos audit` | 33-dimension quality check | Standalone evaluation |
| `inkos revise` | Revise chapter | Modes: polish/spot-fix/rewrite/rework/anti-detect |
| `inkos agent` | Natural language interface | Flexible requests |
| `inkos style analyze` | Analyze reference text | Extracts style profile |
| `inkos style import` | Apply style to book | Makes style permanent |
| `inkos import canon` | Link spinoff to parent | For prequels/sequels |
| `inkos import chapters` | Import existing chapters | Reverse-engineers truth files for continuation |
| `inkos detect` | AIGC detection | Flags AI-generated passages |
| `inkos export` | Export finished book | Formats: txt, md, epub |
| `inkos analytics` / `inkos stats` | View book statistics | Word count, audit rates, token usage |
| `inkos radar scan` | Platform trend analysis | Informs new book ideas |
| `inkos short run` | Generate standalone short fiction | Outputs manuscript, sales package, cover prompt, optional cover |
| `inkos config set-global` | Configure LLM provider | OpenAI/Anthropic/custom (any OpenAI-compatible) |
| `inkos config set-model <agent> <model>` | Set model override for a specific agent | `--provider`, `--base-url`, `--api-key-env` for multi-provider routing |
| `inkos config show-models` | Show current model routing | View per-agent model assignments |
| `inkos doctor` | Diagnose issues | Check installation |
| `inkos update` | Update to latest version | Self-update |
| `inkos up/down` | Daemon mode | Background processing. Logs to `inkos.log` (JSON Lines). `-q` for quiet mode |
| `inkos review list/approve-all` | Manage chapter approvals | Quality gate |
| `inkos fanfic init` | Create fanfic from source material | `--from <file>`, `--mode canon/au/ooc/cp` |
| `inkos genre list` | List all available genres | Shows English and Chinese genres with default language |
| `inkos genre create <id>` | Create custom genre profile | `--name`, `--numerical`, `--power`, `--era` |
| `inkos genre copy <id>` | Copy built-in genre to project | For customization |
| `inkos write rewrite <book> <ch>` | Rewrite a specific chapter | Deletes chapter and later, rewrites from that point |
| `inkos book update [book-id]` | Update book settings | `--chapter-words`, `--target-chapters`, `--status`, `--lang` |
| `inkos book delete <book-id>` | Delete book and all chapters | `--force` to skip confirmation |
| `inkos plan chapter [book-id]` | Generate chapter intent | Preview what next chapter will do before writing |
| `inkos compose chapter [book-id]` | Generate runtime artifacts | Context, rule-stack, trace for next chapter |
| `inkos consolidate [book-id]` | Consolidate chapter summaries | Reduces context for long books (volume-level summaries) |
| `inkos eval [book-id]` | Quality evaluation report | `--json`, `--chapters <range>`. Composite quality score |
| `inkos` / `inkos studio` | Start web workbench | `-p` for port. Local web UI for book management |
| `inkos fanfic show [book-id]` | Display parsed fanfic canon | Shows imported source material analysis |
| `inkos fanfic refresh [book-id]` | Re-import and regenerate fanfic canon | `--from <file>` for updated source material |
| `inkos interact` | Shared interaction endpoint | `--json`, `--message`, `--book`. Primary entry for OpenClaw |
| `inkos tui` | Launch TUI dashboard | Full-screen Ink + React interactive dashboard |

## Error Handling

### Common Issues

**"book-id not found"**
- Verify the ID with `inkos book list`
- Ensure you're in the correct project directory

**"Provider not configured"**
- Run `inkos config set-global` with valid credentials
- Check API key and base URL with `inkos doctor`

**"Context invalid"**
- Ensure `--context` is a string (wrap in quotes if multi-word)
- Context can be in English or Chinese

**"Audit failed"**
- Check chapter for encoding issues
- Ensure chapter-words matches actual word count
- Try `inkos revise` with `--mode rewrite`

**"Book already has chapters" (import)**
- Use `--resume-from <n>` to append to existing chapters
- Or delete existing chapters first

### Running Daemon Mode

For long-running operations:
```bash
# Start background daemon
inkos up

# Stop daemon
inkos down

# Daemon auto-processes queued chapters
```

## Tips for Best Results

1. **Provide rich context**: The more guidance in `--context`, the more coherent the narrative
2. **Start with style**: If imitating an author, run `inkos style import` before generation
3. **Import first**: For existing novels, use `inkos import chapters` to bootstrap truth files before continuing
4. **Review regularly**: Use `inkos review` to catch issues early
5. **Monitor audits**: Check `inkos audit` metrics to understand quality bottlenecks
6. **Use spinoffs strategically**: Import canon before writing prequels/sequels
7. **Batch generation**: Generate multiple chapters together (better continuity)
8. **Check analytics**: Use `inkos analytics` to track quality trends over time
9. **Export frequently**: Keep backups with `inkos export`

## Security & Trust

- **License**: the ClawHub skill descriptor is MIT-0 per platform policy, but the underlying `@actalk/inkos`, `@actalk/inkos-core`, and `@actalk/inkos-studio` npm packages are **AGPL-3.0-only**. Running InkOS and distributing modified versions are governed by AGPL. Full source on GitHub for auditability.
- **No install hooks**: npm package has no `preinstall`/`postinstall`/`install` scripts. Install is inert.
- **Local-only file I/O**: all read/write stays inside the project directory (`books/*`, `inkos.json`, `inkos.log`). No writes outside the working directory.
- **No telemetry**: InkOS does not phone home, collect usage stats, or ship any data to InkOS-controlled servers. The only outbound traffic is to the LLM provider endpoint you explicitly configure.
- **Credential handling**: prefer Studio service settings or `--api-key-env <VAR_NAME>` over literal keys. Studio stores service secrets in project-local `.inkos/secrets.json`; CLI env settings live in `~/.inkos/.env` or project `.env`. Treat all of these as secrets and keep them out of commits.
- **Custom provider base-URL**: `--provider custom` forwards your API key to whatever URL you specify. Only point it at endpoints you trust (your own proxy or an audited reverse-proxy). Never paste an untrusted `--base-url`.
- **No elevated privileges**: InkOS requires no sudo, no global state mutation, no network listening port (Studio binds `localhost:4567` only).

## Support & Resources

- **Homepage**: https://github.com/Narcooo/inkos
- **Configuration**: Stored in project root after `inkos init`
- **Truth files**: Located in `books/<id>/story/` per book, with structured JSON in `story/state/`
- **Logs**: Check output of `inkos doctor` for troubleshooting
