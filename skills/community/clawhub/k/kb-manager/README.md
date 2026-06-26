# kb-manager

A lightweight OpenClaw skill for building and maintaining a structured local knowledge base inside an agent workspace.

It helps you:

- initialize a standard knowledge base structure
- decide whether content is worth saving
- classify content automatically by purpose
- save knowledge as structured Markdown
- use `00_inbox` as a safe fallback when classification is uncertain
- organize inbox items later
- keep naming, templates, and metadata consistent over time

This version is intentionally small, practical, and easy to extend.

---

## Directory structure

```text
kb-manager/
  SKILL.md
  templates/
    default-entry.md
    project-entry.md
    research-entry.md
    reference-entry.md
  docs/
    classification-rules.md
    naming-rules.md
  examples/
    init.txt
    intake-article.txt
    intake-pdf.txt
    organize-inbox.txt
```

---

## What this skill does

`kb-manager` is meant to work inside a dedicated `knowledge` agent workspace.

Its main responsibilities are:

- initialize a `knowledge/` directory
- create standard subdirectories and core meta files
- evaluate whether incoming content should be saved
- classify content by purpose
- format saved content with Markdown templates
- send uncertain items to `knowledge/00_inbox/`
- help organize inbox items when asked
- keep the knowledge base coherent over time

---

## Recommended usage

Use a dedicated OpenClaw agent for knowledge management.

Example:

```bash
openclaw agents add knowledge
```

Then place this skill in the agent workspace:

```text
skills/
  kb-manager/
    SKILL.md
    templates/
    docs/
    examples/
```

---

## Standard knowledge base structure

When initialized, the skill should create:

```text
knowledge/
  00_inbox/
  01_reference/
  02_learning/
  03_projects/
  04_research/
  05_playbooks/
  06_prompts/
  99_archive/
  _meta/
```

### Core meta files created during initialization

```text
knowledge/_meta/README.md
knowledge/_meta/classification-rules.md
knowledge/_meta/naming-rules.md
knowledge/_meta/template.md
knowledge/_meta/intake-log.md
```

### Optional meta files that can be added later

```text
knowledge/_meta/topics.md
knowledge/_meta/projects-index.md
knowledge/_meta/recent.md
```

Create the optional index files only when the knowledge base grows large enough to benefit from them.

---

## Install options

### Option A: install an existing skill

If a suitable knowledge-base skill exists in ClawHub, install it there.

```bash
clawhub search "knowledge base"
clawhub install <skill-slug>
```

### Option B: add this skill manually

Copy the `kb-manager/` directory into your agent workspace:

```text
skills/kb-manager/
```

This is the simplest way to try the current version.

---

## Quick start

### 1. Create a knowledge agent

```bash
openclaw agents add knowledge
```

### 2. Add the skill

Put the `kb-manager` folder into the agent's `skills/` directory.

### 3. Start a new session with the knowledge agent

Make sure the skill is loaded in the new session.

### 4. Initialize the knowledge base

Use the example prompt from `examples/init.txt`, or send something like:

```text
Please use kb-manager to initialize a knowledge base.

Requirements:
1. Create a `knowledge/` directory in the current workspace
2. Create standard subdirectories:
   - 00_inbox
   - 01_reference
   - 02_learning
   - 03_projects
   - 04_research
   - 05_playbooks
   - 06_prompts
   - 99_archive
   - _meta
3. Copy `docs/classification-rules.md` to `knowledge/_meta/classification-rules.md`
4. Copy `docs/naming-rules.md` to `knowledge/_meta/naming-rules.md`
5. Copy `templates/default-entry.md` to `knowledge/_meta/template.md` as the active template
6. Create `knowledge/_meta/README.md` and `knowledge/_meta/intake-log.md`
7. Keep optional index files for later unless the user explicitly wants them now
8. Use `templates/project-entry.md` for project-related content
9. Put uncertain items into `00_inbox`
```

---

## Common usage examples

### Save an article

Use `examples/intake-article.txt`, or:

```text
Please save this article to the knowledge base.

Requirements:
1. Decide whether it is worth saving
2. Classify it automatically
3. Use the most suitable template
4. If classification is uncertain, put it into `00_inbox`
5. Output the save path, filename, and structured Markdown
```

### Save a PDF

Use `examples/intake-pdf.txt`, or:

```text
Please turn this PDF into a knowledge entry.

Requirements:
1. If it is an official document, prefer `01_reference`
2. If it is a tutorial or study material, prefer `02_learning`
3. Use the most suitable template
4. Output the final path, filename, and structured Markdown
```

### Organize inbox

Use `examples/organize-inbox.txt`, or:

```text
Please organize `knowledge/00_inbox/`.

Requirements:
1. Reclassify items when confidence is high
2. Add or improve tags
3. Suggest archive or deletion for low-value items
4. Keep uncertain items in inbox
5. Output a short organization report
```

---

## Templates

This skill currently includes:

- `templates/default-entry.md`
- `templates/project-entry.md`
- `templates/research-entry.md`
- `templates/reference-entry.md`

### Default entry template

Used for general notes, articles, study materials, prompts, and reusable knowledge.

### Project entry template

Used for project-specific discussions, plans, meeting notes, architecture notes, and decisions.

### Research entry template

Used for comparisons, evaluations, investigations, and exploratory reports.

### Reference entry template

Used for commands, specifications, operational notes, and durable references.
