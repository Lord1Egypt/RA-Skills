# mem-skill

A self-evolving memory and knowledge accumulation skill for AI agents. Turn your AI assistant from a "use-and-forget" tool into a **persistent second brain** that gets smarter with every conversation.

## What It Does

mem-skill runs as a background meta-skill for AI agents (Claude Code, Cursor, Codex, etc.). On every conversation turn, it:

1. **Extracts keywords** from your request to build a topic fingerprint.
2. **Detects topic switches** to decide when to re-read the knowledge base.
3. **Loads skill experience** when you use another skill — if it has recorded pitfalls or best practices, it surfaces them immediately.
4. **Retrieves relevant knowledge** from your personal knowledge base.
5. **Proactively records** successful solutions when a task is completed, asking your permission before writing.

Over time, your AI remembers what worked, what failed, and how you prefer things done.

---

## Real-World Example

Here's an actual conversation showing mem-skill in action. The user asks their AI to build a landing page — mem-skill runs silently in the background the entire time.

### 1. Initialize

```
You:   /mem-skill init
Agent: ✓ Created knowledge-base/_index.json
       ✓ Created experience/_index.json
       ✓ Created .mem-skill.config.json
       mem-skill initialized.
```

### 2. Work Normally

You just ask for what you need. mem-skill reads the knowledge base automatically:

```
You:   Help me write a simple landing page about NVDA stock introduction
Agent: [reads knowledge-base/_index.json — looking for matching categories]
       ...builds the page...
       Created nvda-landing.html
```

The agent creates a professional landing page with hero section, features grid, company stats, CTAs, and responsive design — all in one HTML file.

### 3. mem-skill Learns (With Your Permission)

When you're happy with the result, mem-skill asks before recording:

```
You:   It is OK
Agent: Great! I'd like to record this approach in my knowledge base
       so I can reference it for future landing page requests.
       Is that okay?
You:   Yes
Agent: ✓ Created knowledge-base/landing-pages.md
       ✓ Updated knowledge-base/_index.json
       Recorded!
```

### 4. Next Time It Remembers

The next time you (or anyone using this workspace) ask for a landing page, mem-skill will automatically surface the recorded approach — the single-file HTML pattern, the hero-features-stats-CTA structure, the responsive grid, and the disclaimer for financial topics. No re-explaining needed.

---

## Real-World Example: QMD Engine

Same workflow, but with semantic search powered by QMD. The key differences: you pass flags to skip prompts, and retrieval uses `qmd query` instead of JSON keyword matching.

### 1. Initialize with Flags

No interactive prompts — everything is configured in one command:

```
You:   /mem-skill init --mem-engine=qmd --qmd-scope=project --qmd-knowledge=demo-kb --qmd-experience=demo-exp
Agent: ✓ Created knowledge-base/_index.json
       ✓ Created experience/_index.json
       ✓ QMD collections: demo-kb, demo-exp
       ✓ Embeddings generated
       mem-skill initialized with QMD engine.
```

### 2. Work Normally — QMD Searches Semantically

```
You:   Help me write a simple landing page about NVDA stock introduction
Agent: [runs: qmd query "landing page NVDA stock introduction" -c demo-kb --json -n 10 --min-score 0.3]
       ...builds the page...
       Created nvda-landing.html
```

QMD uses hybrid search (BM25 + vector + re-ranking) to find relevant knowledge — even fuzzy matches that keyword matching would miss.

### 3. mem-skill Learns + QMD Re-indexes

```
You:   It looks OK
Agent: I'd like to record this approach to the knowledge base
       so I can reference it when creating landing pages in the future.
       Is that okay?
You:   Yes
Agent: ✓ Created knowledge-base/web-development.md
       ✓ Updated knowledge-base/_index.json
       ✓ qmd update && qmd embed
       Recorded and re-indexed!
```

After writing, mem-skill runs `qmd update && qmd embed` so the new entry is immediately searchable via semantic search.

---

## Installation

### As an Agent Skill

```bash
npx skills add oliguo/mem-skill
```

### From Source

```bash
git clone https://github.com/oliguo/mem-skill.git
cp -r mem-skill ~/.agents/skills/mem-skill
```

## Upgrading from v1.1.0

If you already have mem-skill installed and want the new features (activity log, cross-references, source tracking, lint, ingest), you don't need to start over. Just update the skill files and run the upgrade command.

### Step 1: Update the Skill

```bash
# If installed via skills CLI:
npx skills add oliguo/mem-skill

# If installed from source:
cd ~/.agents/skills/mem-skill && git pull
```

### Step 2: Migrate Your Workspace

```bash
/mem-skill upgrade
```

This safely migrates your existing knowledge base:
- Creates `log.md` (activity timeline) if missing
- Adds `**Source:** conversation` to existing entries that lack it
- Adds `**Related:**` placeholder to existing entries for future cross-references
- Updates your config version to 1.2.0

Your existing entries are **never deleted or rewritten** — only new fields are added.

### Step 3 (Optional): Discover Cross-References

```bash
/mem-skill lint
```

After upgrading, run lint to find entries that should be linked together. It detects duplicate entries that can be merged, entries with overlapping keywords, and other health issues.

### What's New in v1.2.0

| Feature | Description |
|---------|-------------|
| `**Source:**` field | Tracks where knowledge came from (conversation, file, URL) |
| `**Related:**` field | Cross-references between entries (Obsidian-compatible wikilinks) |
| `log.md` | Chronological activity log of all operations |
| Compounding updates | Merges into existing entries instead of creating duplicates |
| Filing queries back | Valuable analyses/comparisons offered as knowledge entries |
| `/mem-skill lint` | Health-check: duplicates, stale entries, contradictions, orphans |
| `/mem-skill ingest` | Process external files/URLs into knowledge entries |
| `/mem-skill upgrade` | Safe migration from v1.1.0 |

## Quick Start

### Initialize (Default Engine)

```bash
/mem-skill init
```

Creates `knowledge-base/` and `experience/` directories with starter index files, using simple JSON keyword matching.

### Record Manually

```bash
/mem-skill recordnow
```

Triggers recording for the current conversation — useful when the agent didn't ask automatically after completing tasks. It scans the full conversation, lists all recordable items, and lets you pick which ones to save.

### Health-Check Your Knowledge Base

```bash
/mem-skill lint
```

Runs a comprehensive health-check: detects duplicates, stale entries (> 6 months), contradictions, orphan files, missing cross-references, and index inconsistencies. Presents issues and lets you fix them interactively.

### Ingest External Sources

```bash
/mem-skill ingest ./docs/api-guide.md
/mem-skill ingest https://example.com/best-practices
/mem-skill ingest ./docs/
```

Processes external files or URLs into knowledge base entries. Extracts actionable insights, matches them to categories, checks for compounding opportunities with existing entries, and lets you approve before writing.

### Initialize with QMD Engine

```bash
/mem-skill init --mem-engine=qmd
```

Uses [QMD](https://github.com/tobi/qmd) for hybrid semantic search (BM25 + vector + LLM re-ranking). Requires Node.js >= 22. The init process will:

1. Install QMD if not already available
2. Ask whether collections should be **project-scoped** or **global**
3. Ask you to **name your collections** (with sensible defaults)

This prevents one project's collections from overwriting another's.

#### Skip Prompts with Flags

Pass `--qmd-*` flags to pre-configure everything in one command:

```bash
# Project-scoped with custom names
/mem-skill init --mem-engine=qmd --qmd-scope=project --qmd-knowledge=myapp-kb --qmd-experience=myapp-exp

# Global with defaults (no prompts)
/mem-skill init --mem-engine=qmd --qmd-scope=global --qmd-knowledge=mem-knowledge --qmd-experience=mem-experience

# Custom file mask
/mem-skill init --mem-engine=qmd --qmd-mask="**/*.md,**/*.txt"
```

| Flag | Description | Default |
|------|-------------|---------|
| `--qmd-scope` | `project` or `global` | _(asks you)_ |
| `--qmd-knowledge` | Knowledge collection name | _(asks you)_ |
| `--qmd-experience` | Experience collection name | _(asks you)_ |
| `--qmd-mask` | File glob for indexing | `**/*.md` |

## Memory Engines

| Engine    | Search Method              | Dependencies     | Best For                     |
|-----------|---------------------------|-------------------|------------------------------|
| `default` | JSON keyword matching      | None              | Small knowledge bases (< 50) |
| `qmd`     | BM25 + Vector + Re-ranking | Node.js >= 22, QMD | Large bases, semantic search  |

More engines can be added — see [references/engines.md](references/engines.md) for the extension architecture.

## How It Works

### The Core Loop (Runs Every Turn)

```
┌─────────────────────────────────────────────────────────────────┐
│                    mem-skill Core Loop                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Extract Keywords                                        │
│     "help me write a landing page about NVDA stock"              │
│     → keywords: [landing-page, NVDA, stock, HTML, introduction]  │
│                                                                  │
│  Step 2: Detect Topic Switch                                     │
│     Compare with last turn's keywords (>= 40% changed? → yes)   │
│     → Topic switch detected → will re-read knowledge base        │
│                                                                  │
│  Step 3: Load Skill Experience                                   │
│     If another skill is active, load its recorded pitfalls       │
│     → (no other skill this turn — skip)                          │
│                                                                  │
│  Step 4: Load Knowledge Base                                     │
│     Match keywords against category index                        │
│     → Match found: "frontend-dev" (HTML, CSS, component)         │
│     → Load knowledge-base/frontend-dev.md                        │
│                                                                  │
│  Step 5: Proactive Recording                                     │
│     User says "it is OK" → task completed successfully           │
│     → Check existing entries for related content (compounding)   │
│     → Ask permission → record/update knowledge-base entry        │
│     → Add cross-references + source provenance                   │
│     → Log operation to log.md                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### What Gets Recorded

mem-skill stores two types of memory:

**Knowledge Base** — reusable patterns, best practices, and preferences:

```markdown
## Single-File Landing Page Pattern
**Date:** 2026-02-19
**Source:** conversation
**Context:** Building quick stock/product intro landing pages
**Best Practice:**
- Use single HTML file with embedded CSS for portability
- Structure: Hero → Features grid → Stats → CTA → Footer
- Use responsive CSS Grid (auto-fit, minmax) for feature cards
- Always include disclaimers for financial/medical content
**Related:** [[design-layout#Responsive Grid Patterns]]
**Keywords:** landing-page, HTML, responsive, single-file, stock
```

**Skill Experience** — pitfalls and solutions for specific skills:

```markdown
## QMD embed fails on large directories
**Date:** 2026-02-19
**Skill:** qmd-search
**Source:** conversation
**Context:** Running qmd embed on 500+ files caused OOM
**Solution:**
- Split into smaller collections (< 200 files each)
- Use `--mask` to exclude non-markdown files
**Key Files/Paths:**
- ~/.cache/qmd/models/
**Related:** [[workflow#QMD Collection Setup]]
**Keywords:** qmd, embed, OOM, large, collection
```

## File Structure

```
<your-workspace>/
├── knowledge-base/
│   ├── _index.json             # Category index (keywords → files)
│   ├── frontend-dev.md         # Recorded: frontend best practices
│   ├── landing-pages.md        # Recorded: landing page patterns
│   └── ...                     # Categories created as you work
├── experience/
│   ├── _index.json             # Skill experience index
│   ├── skill-<id>.md           # Recorded: pitfalls for a specific skill
│   └── ...
├── log.md                      # Chronological activity log
├── references/
│   ├── qmd-engine.md           # QMD engine setup & commands
│   └── engines.md              # How to add new engines
├── scripts/
│   ├── init.sh                 # Workspace initialization
│   ├── bump-version.sh         # Version management
│   └── package.sh              # Clean packaging for distribution
├── SKILL.md                    # Core skill definition
├── .mem-skill.config.json      # Engine configuration (generated)
└── package.json
```

## Starter Categories

When you install mem-skill, you start with 5 empty categories ready to be filled:

| Category | Keywords | What Goes Here |
|----------|----------|----------------|
| Frontend Development | React, Vue, CSS, TypeScript, ... | UI patterns, component practices |
| Backend Development | API, Node.js, database, REST, ... | Server patterns, auth flows |
| Writing & Content | article, documentation, blog, ... | Writing styles, templates |
| Design & Layout | UI, UX, color, typography, ... | Design systems, layout rules |
| Workflow & Automation | CI/CD, DevOps, script, ... | Build processes, automation |

New categories are created automatically when your work doesn't fit an existing one — mem-skill will suggest a name and keywords, then create the file for you.

## FAQ

**Does mem-skill send my data anywhere?**
No. Everything stays in your local workspace files. There are no API calls, no telemetry, no cloud storage.

**What if I want to start fresh?**
Delete the `knowledge-base/` and `experience/` directories, then run `/mem-skill init` again.

**Can I edit the recorded entries manually?**
Yes — they're plain Markdown files. Edit, reorganize, or delete entries anytime.

**When should I upgrade to QMD?**
When your knowledge base exceeds ~50 entries. mem-skill will proactively suggest the upgrade when it detects this threshold.

**Does it work with any AI agent?**
It works with any agent that supports the skill-creator framework (Claude Code, Cursor, Codex, etc.).

**The agent didn't ask to record after completing my tasks. What do I do?**
Run `/mem-skill recordnow`. It reviews the full conversation, finds completed tasks worth saving, and lets you choose which ones to record.

**How do I keep my knowledge base healthy as it grows?**
Run `/mem-skill lint` periodically. It detects duplicates, stale entries, contradictions, and missing cross-references. Think of it as a code linter for your knowledge base.

**Can I import knowledge from external documents?**
Yes — run `/mem-skill ingest <file-or-url>`. It extracts actionable insights, matches them to your categories, and lets you approve before writing. Source provenance is tracked automatically.

**What are cross-references?**
Entries can link to related entries using `**Related:** [[category#entry-title]]` syntax (Obsidian-compatible). When you record a new entry, mem-skill searches for related existing entries and adds bidirectional links — so your knowledge compounds instead of just accumulating.

**What is the log.md file?**
A chronological record of all mem-skill operations (reads, writes, lints, ingests). Helps you see how your knowledge base evolves over time. Parseable with `grep "^## \[" log.md | tail -5`.

## Credits

Inspired by [Auto-Skill](https://github.com/Toolsai/auto-skill) (Toolsai), [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (Andrej Karpathy), and powered by [QMD](https://github.com/tobi/qmd) (Tobi Lütke).

## License

MIT — see [LICENSE](LICENSE).