# README_FOR_AI.md

> **Purpose**: This document is a meta-instruction set. It directs an AI agent to generate a complete, production-grade **GitHub Novel Serialization Skill** project. Every section below is a mandatory generation directive — follow them precisely.
>
> **Document Metadata**:
> - **Version**: 1.1.2
> - **Status**: Approved
> - **Last Updated**: 2026-09-14
> - **Review**: Post-generation audit completed; see [README_FOR_AI_Audit_Report](README_FOR_AI_Audit_Report.md) — see audit report for issues found and fixes applied
> **File Naming Note**: This file should be named `README FOR AI.md` (with `.md` extension) to match its Markdown content and document title. The filename `README_F.txt` is a temporary upload name and should be corrected during project setup.


---

## 0. Generation Directives

### 0.1 Target Output

You are to generate a **complete Skill project** — not a single file, but a full directory tree of interlocking Markdown files that together form a modular, harness-engineered Skill for AI-assisted novel serialization on GitHub.

### 0.2 Language Policy

| Layer | Language | Rationale |
|-------|----------|-----------|
| SKILL.md frontmatter & body | **English** | Universal compatibility across all AI coding tools (Claude Code, Copilot, Cursor, etc.) |
| `references/*.md` | **English** | Technical templates must be language-agnostic at the structural level |
| `prompts/*.md` | **English** (with `{{OUTPUT_LANGUAGE}}` placeholder) | Prompts are templates; the placeholder is replaced at runtime |
| `.github/` community files | **English** | GitHub standard convention |
| All other project files | **English** | Consistency |
| `LICENSE` / `NOTICE` / `COPYING` | **Fixed text (GPL-3.0 / CC BY-NC-SA 4.0)** | License text must not be translated; must use official original text |

### 0.3 Runtime Output Language (Single Authority)

> **AUTHORITATIVE DECLARATION**: All generated novel content (chapters, character sheets, world-building docs) MUST be output in the language specified by the user via the `{{OUTPUT_LANGUAGE}}` variable.
>
> - **Variable**: `{{OUTPUT_LANGUAGE}}`
> - **Default**: `English`
> - **Supported**: Any language the underlying LLM supports
> - **Scope**: Applies to all generated narrative content, NOT to Skill infrastructure files
> - **Infrastructure files** (SKILL.md, references/, module definitions) remain in English to ensure cross-tool compatibility
>
> **Every prompt template in `prompts/` MUST include this block near the top:**
>
> ```
> ## Output Language Instruction
>
> All novel content you generate MUST be written in: {{OUTPUT_LANGUAGE}}
>
> If {{OUTPUT_LANGUAGE}} is set to "Chinese (简体中文)", write all narrative text,
> dialogue, character names (if appropriate), and world-building descriptions in Chinese.
> Structural labels (e.g., "Chapter 1", "Character Sheet") may remain in English
> or be translated — author's discretion.
>
> Default value: English
> ```
>
> **Each module's SKILL.md MUST include in its Constraints section:**
>
> ```
> - All generated content MUST be output in {{OUTPUT_LANGUAGE}} (default: English)
> - Infrastructure and metadata remain in English
> ```

### 0.4 Core Constraints

1. **SKILL.md is index + quick-reference ONLY** — no code templates, no long-form methodology. It points to `references/` and `prompts/` for depth.
2. **All code templates, structural patterns, and long-form methodology live in `references/method-patterns.md`** (or its split modules if >500 lines).
3. **`prompts/` folder is DUAL-MODE** — files inside are NOT for agent auto-invocation. They are standalone prompt templates for humans to copy-paste into any AI chat window.
4. **Harness Engineering compliance** — the Skill must embody: constraint-before-generation, structured memory, verification gates, modular decomposition, and feedback loops.
5. **Standardization, generalization, modularization, miniaturization, automation** — every module must be independently usable, composable, and under 500 lines.
6. **Split permission** — any file exceeding 500 lines MUST be split into sub-modules under the same directory.

> **NOTE**: This document (`README FOR AI.md`) is a meta-instruction/seed file, not a SKILL.md. It is exempt from the 500-line limit because it serves as the authoritative generation specification. However, it should strive for conciseness and refer to external resources where possible.

### 0.5 License Policy (Dual Licensing)

> **DUAL LICENSING MODEL**: This Skill project employs a dual-licensing strategy to separate code infrastructure from creative content:
>
> | Component | License | Scope |
> |-----------|---------|-------|
> | **Skill Infrastructure** (code, templates, prompts, SKILL.md files, GitHub workflows, configuration files) | **GNU General Public License v3.0 (GPL-3.0)** | All Skill infrastructure files including SKILL.md, references/, prompts/, modules/, .github/, .gitignore, .editorconfig, etc. |
> | **Generated Novel Content** (chapters, character sheets, world-building docs produced by the Skill) | **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** | All narrative content generated by the Skill, including chapters, character descriptions, world-building documents, and story outlines |
>
> **Key Rules**:
> - Every generated novel file MUST begin with a CC BY-NC-SA 4.0 license header block
> - The `LICENSE` file at project root MUST contain the full GPL-3.0 text
> - The `LICENSES/` directory (if present) MAY contain the full CC BY-NC-SA 4.0 license text
> - SKILL.md YAML frontmatter MUST declare both licenses: `license: GPL-3.0` and `novel_content_license: CC-BY-NC-SA-4.0`
> - Prompt templates MUST instruct the AI to include the CC BY-NC-SA 4.0 header in all generated novel content
> - The GitHub Actions release workflow MUST verify license compliance before publishing
>
> **GPL-3.0 Summary**: Users are free to use, modify, and distribute the Skill infrastructure under the terms of GPL-3.0. Any modified version of the Skill infrastructure must also be released under GPL-3.0.
>
> **CC BY-NC-SA 4.0 Summary**: Users are free to share and adapt the novel content for non-commercial purposes, provided they give appropriate credit, indicate if changes were made, and distribute contributions under the same license.


---

## 1. Project Directory Structure

Generate the following complete directory tree. Every file listed is **mandatory**.

```text
github-novel-serialization-skill/
│
├── README.md                           # Project overview, quick start, architecture diagram
├── README FOR AI.md                    # THIS FILE — meta-instructions for AI generation (seed file)
├── .gitignore                          # Git ignore rules
├── .editorconfig                       # Editor configuration
├── LICENSE                             # GNU General Public License v3.0 (GPL-3.0)
├── LICENSES/                           # Additional license texts
│   └── CC-BY-NC-SA-4.0.txt             # Full CC BY-NC-SA 4.0 license text
├── CODE_OF_CONDUCT.md                  # Community behavior standards
├── CONTRIBUTING.md                     # Contribution guidelines
├── SECURITY.md                         # Security policy & vulnerability reporting
├── CHANGELOG.md                        # Version history (Keep a Changelog format)
│
├── SKILL.md                            # Index + quick-reference (≤500 lines)
│
├── references/                         # Deep documentation & code templates
│   ├── method-patterns.md              # Master template file (split if >500 lines)
│   ├── method-patterns-worldbuilding.md    # [Split module] World-building templates
│   ├── method-patterns-character.md        # [Split module] Character design templates
│   ├── method-patterns-chapter.md          # [Split module] Chapter writing templates
│   ├── method-patterns-continuity.md       # [Split module] Continuity tracking templates
│   ├── method-patterns-publishing.md       # [Split module] Publishing & release templates
│   ├── glossary.md                         # Domain terminology & conventions
│   └── examples/                           # Concrete worked examples
│       ├── example-worldbuilding.md
│       ├── example-character-sheet.md
│       └── example-chapter-draft.md
│
├── prompts/                            # Dual-mode prompt templates (human copy-paste)
│   ├── README.md                       # How to use these prompts
│   ├── 01-implement-method.md          # Core implementation prompt
│   └── 02-robustness-checks.md         # Validation & quality-check prompt
│
├── modules/                            # Functional modules (independently usable)
│   ├── worldbuilding/
│   │   └── SKILL.md                    # World-building sub-skill
│   ├── character-design/
│   │   └── SKILL.md                    # Character design sub-skill
│   ├── chapter-writing/
│   │   └── SKILL.md                    # Chapter writing sub-skill
│   ├── continuity-check/
│   │   └── SKILL.md                    # Continuity & consistency verification sub-skill
│   ├── publishing-workflow/
│   │   └── SKILL.md                    # GitHub publishing & release sub-skill
│   └── continuity-tracker/
│       └── SKILL.md                    # State tracking & memory persistence sub-skill
│
└── .github/                            # GitHub community health files
    ├── ISSUE_TEMPLATE/
    │   ├── bug-report.yml
    │   ├── feature-request.yml
    │   └── config.yml
    ├── PULL_REQUEST_TEMPLATE.md
    ├── FUNDING.yml
    ├── dependabot.yml
    └── workflows/
        └── novel-release.yml           # Automated release workflow template
```

---

## 2. SKILL.md — Index & Quick-Reference Specification

### 2.1 YAML Frontmatter

```yaml
---
name: github-novel-serialization
description: >
  Orchestrates AI-assisted novel writing and GitHub-based serialization.
  Use when the user asks to write a novel, create characters, build worlds,
  draft chapters, check continuity, or publish chapters to a GitHub repository.
  Covers the full lifecycle: world-building → character design → chapter drafting →
  continuity verification → GitHub publishing.
license: GPL-3.0
novel_content_license: CC-BY-NC-SA-4.0
license_note: >
  Skill infrastructure is licensed under GNU General Public License v3.0 (GPL-3.0).
  Generated novel content (chapters, character sheets, world-building docs) is licensed
  under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
compatibility: Works with any LLM-backed coding agent (Claude Code, GitHub Copilot, Cursor, etc.)
metadata:
  author: community
  version: 1.0.0
  output_language_default: English
---
```

### 2.2 Body Structure (≤500 lines)

The SKILL.md body must contain ONLY the following sections:

| Section | Content | Max Lines |
|---------|---------|-----------|
| `## Overview` | One-paragraph mission statement | 5 |
| `## Output Language` | Reference `{{OUTPUT_LANGUAGE}}` (see Section 0.3 for authoritative declaration) | 5 |
| `## Quick Start` | 5-step numbered workflow | 15 |
| `## Module Index` | Table mapping module name → one-line purpose → file path | 20 |
| `## Workflow Pipeline` | DAG-style pipeline: Plan → Build → Draft → Verify → Publish | 30 |
| `## Quick Reference: File Conventions` | Naming rules, directory structure for novel repos | 20 |
| `## Quick Reference: Git Conventions` | Branch naming, commit format, tag format | 15 |
| `## Quick Reference: Continuity State` | What state files to maintain and where | 15 |
| `## Verification Gates` | Checklist of mandatory checks before publish | 15 |
| `## Cross-References` | Pointers to `references/` and `prompts/` | 10 |
| `## Constraints & Boundaries` | Hard rules the agent must never violate | 20 |

**Total target: ~170 lines. Hard ceiling: 500 lines.**

### 2.3 Critical Rule

> **NEVER embed code templates, long-form methodology, or step-by-step procedural instructions in SKILL.md.** All such content belongs in `references/method-patterns.md` or its split modules. SKILL.md only says WHAT exists and WHERE to find it.


---

## 3. references/ — Deep Documentation & Code Templates

### 3.1 `method-patterns.md` — Master Template

This is the **single source of truth** for all structural templates, code patterns, and long-form methodology. It must contain:

| Section | Content |
|---------|---------|
| `## World-Building Templates` | Structured templates for magic systems, geography, politics, technology, history, culture |
| `## Character Design Templates` | Character sheet format: identity, psychology, arc, relationships, voice profile |
| `## Chapter Writing Templates` | Scene structure, POV rules, pacing formula, dialogue formatting, chapter header format |
| `## Continuity Tracking Templates` | State file format: timeline, character states, location states, unresolved threads |
| `## Publishing Workflow Templates` | Git tag format, release note template, chapter file naming convention |
| `## Style Consistency Rules` | Voice register, tense conventions, terminology lock, forbidden patterns |

**Split Rule**: If `method-patterns.md` exceeds 500 lines, split into:
- `method-patterns-worldbuilding.md`
- `method-patterns-character.md`
- `method-patterns-chapter.md`
- `method-patterns-continuity.md`
- `method-patterns-publishing.md`

The master file then becomes an index pointing to each split module. See **Section 8** for the splitting protocol.

### 3.2 `glossary.md`

Define all domain-specific terms used across the Skill:
- Novel serialization terminology (arc, chapter, scene, beat, POV)
- Git terminology as used in this context (tag, release, branch)
- State tracking terminology (continuity file, state snapshot, thread ledger)

### 3.3 `examples/` — Worked Examples

Each example file must demonstrate a complete, concrete instantiation of the corresponding template:
- `example-worldbuilding.md` — A fully filled-out world-building document for a sample novel
- `example-character-sheet.md` — A fully filled-out character sheet
- `example-chapter-draft.md` — A complete sample chapter with annotations

---

## 4. prompts/ — Dual-Mode Prompt Templates

### 4.1 Design Philosophy

Files in `prompts/` are **NOT** for agent auto-invocation. They are **standalone, self-contained prompt templates** that a human user can:
1. Open in any text editor
2. Copy the entire content
3. Paste into ANY AI chat window (ChatGPT, Claude, Gemini, Copilot, etc.)
4. Get immediate, structured output

### 4.2 `prompts/README.md`

Must explain:
- What "dual-mode" means (agent-assisted vs. human copy-paste)
- How to use each prompt file
- How to customize the `{{OUTPUT_LANGUAGE}}` placeholder (see Section 0.3 for authoritative declaration)
- How to combine prompts for complex workflows

### 4.3 `prompts/01-implement-method.md`

A comprehensive prompt template that, when pasted into any AI chat, instructs the AI to:
1. Accept novel parameters (genre, setting, themes, target length)
2. Generate a complete world-building document
3. Generate character sheets for all major characters
4. Produce a chapter-by-chapter outline
5. Draft the first chapter
6. Output everything in `{{OUTPUT_LANGUAGE}}`

Must include:
- Clear role assignment ("You are a professional novel architect...")
- Structured output format specifications
- `{{OUTPUT_LANGUAGE}}` placeholder (see Section 0.3 for authoritative declaration)
- Variable placeholders for user customization: `{{GENRE}}`, `SETTING}}`, `{{THEMES}}`, `{{TARGET_CHAPTERS}}`, `{{TONE}}`, `{{POV_STYLE}}`
- **Novel Content License Header**: Every generated novel file MUST begin with the following CC BY-NC-SA 4.0 license block:

```
# [Novel Title]

This work is licensed under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International License.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/
or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license,
  and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.
- ShareAlike — If you remix, transform, or build upon the material, you must distribute
  your contributions under the same license as the original.
```

### 4.4 `prompts/02-robustness-checks.md`

A comprehensive prompt template that, when pasted into any AI chat, instructs the AI to:
1. Accept a draft chapter or world-building document as input
2. Run a multi-dimensional quality check:
   - Continuity consistency (character names, locations, timeline)
   - Style consistency (voice, tense, register)
   - Plot logic (causality, motivation, foreshadowing payoff)
   - Pacing analysis (scene-to-sequel ratio, tension curve)
   - Dialogue authenticity (voice differentiation per character)
   - **License compliance**: Verify that the generated content includes the CC BY-NC-SA 4.0 license header
3. Output a structured report with severity levels (Critical / Warning / Suggestion)
4. Output in `{{OUTPUT_LANGUAGE}}`


---

## 5. modules/ — Functional Sub-Skills

### 5.1 Design Principles

Each module is an **independently usable sub-skill** that:
- Has its own `SKILL.md` with proper YAML frontmatter (including `license: GPL-3.0` and `novel_content_license: CC-BY-NC-SA-4.0`)
- Can be loaded independently by an agent
- Follows the same index-only pattern as the root SKILL.md
- References `references/` for templates
- Is under 500 lines

### 5.2 Module Specifications

#### `modules/worldbuilding/SKILL.md`
- **name**: `novel-worldbuilding`
- **Purpose**: Generate and maintain world-building documents
- **Triggers**: "build a world", "create setting", "design magic system"
- **References**: `../../references/method-patterns-worldbuilding.md`

#### `modules/character-design/SKILL.md`
- **name**: `novel-character-design`
- **Purpose**: Generate and maintain character sheets
- **Triggers**: "create character", "design protagonist", "character relationships"
- **References**: `../../references/method-patterns-character.md`

#### `modules/chapter-writing/SKILL.md`
- **name**: `novel-chapter-writing`
- **Purpose**: Draft chapters following established style and continuity
- **Triggers**: "write chapter", "draft next scene", "continue story"
- **References**: `../../references/method-patterns-chapter.md`

#### `modules/continuity-check/SKILL.md`
- **name**: `novel-continuity-check`
- **Purpose**: Verify consistency across all chapters and state files
- **Triggers**: "check continuity", "verify consistency", "find plot holes"
- **References**: `../../references/method-patterns-continuity.md`

#### `modules/publishing-workflow/SKILL.md`
- **name**: `novel-publishing-workflow`
- **Purpose**: Manage Git-based publishing pipeline for serialized chapters
- **Triggers**: "publish chapter", "create release", "tag version"
- **References**: `../../references/method-patterns-publishing.md`

#### `modules/continuity-tracker/SKILL.md`
- **name**: `novel-continuity-tracker`
- **Purpose**: Maintain persistent state files (timeline, character states, thread ledger)
- **Triggers**: "update state", "track timeline", "log character status"
- **References**: `../../references/method-patterns-continuity.md`

---

## 6. Harness Engineering Compliance Matrix

Every generated file must satisfy the following Harness Engineering principles:

| Principle | Implementation Requirement |
|-----------|--------------------------|
| **Constraint before generation** | SKILL.md `## Constraints & Boundaries` section must list hard rules before any workflow steps |
| **Structured memory** | `modules/continuity-tracker/` defines state file formats; state is persisted in structured Markdown files, not in conversation context |
| **Verification gates** | `## Verification Gates` in SKILL.md + `prompts/02-robustness-checks.md` — no chapter publishes without passing checks |
| **Modular decomposition** | Each `modules/*/SKILL.md` is independently loadable; no circular dependencies between modules |
| **Feedback loops** | `02-robustness-checks.md` produces structured feedback that feeds back into the next drafting iteration |
| **Progressive disclosure** | SKILL.md (Layer 1: index) → references/ (Layer 2: templates) → examples/ (Layer 3: worked examples) |
| **Context budget management** | SKILL.md ≤500 lines; each module SKILL.md ≤500 lines; references split at 500-line boundary |
| **Human-in-the-loop** | `prompts/` folder enables human oversight; publishing workflow requires manual Git tag creation |
| **Error recovery** | Continuity tracker maintains state snapshots; if a chapter breaks continuity, the system can identify the exact divergence point |
| **Role isolation** | Each module has a single responsibility; worldbuilding module does not write chapters; chapter module does not design characters |
| **License compliance** | All generated files must include appropriate license headers; novel content must include CC BY-NC-SA 4.0 header |


---

## 7. GitHub Standard Files — Generation Specifications

> **NOTE**: This section provides generation specifications for GitHub standard files. Files marked with [Full Content] include complete file templates that can be copied directly. Files marked with [Description Only] provide structural guidance — the AI agent should generate appropriate content based on the described requirements.

### 7.1 `README.md` [Description Only]

Must contain:
- Project name and badge (license, version)
- One-paragraph description
- Architecture diagram (ASCII or Mermaid)
- Quick Start (3 steps)
- Directory structure overview
- Module descriptions (one line each)
- Installation instructions (how to add to `.github/skills/` or `~/.claude/skills/`)
- Usage examples
- Contributing link
- License link (GPL-3.0)
- Novel content license link (CC BY-NC-SA 4.0)
- Credits

### 7.2 `.gitignore` [Full Content]

```gitignore
# OS files
.DS_Store
Thumbs.db
ehthumbs.db
Desktop.ini

# Editor files
*.swp
*.swo
*~
.idea/
.vscode/
*.sublime-project
*.sublime-workspace
*.code-workspace

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
.venv/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node (if scripts are added later)
node_modules/
npm-debug.log*
yarn-error.log*

# Draft/temp files
drafts/
temp/
*.tmp
*.bak

# AI tool cache
.claude/
.copilot/
.agents/
.env
.env.local

# Logs
*.log
logs/

# Dependency updates
.pip-wheel-metadata/
```

### 7.3 `.editorconfig` [Full Content]

```editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.yml]
indent_size = 2

[*.yaml]
indent_size = 2
```

### 7.4 `LICENSE` [Full Content]

```
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed to previous
authors.  Some contributors may be motivated by a desire to contribute
to a community of developers and other users.  If contributors don't
see why they should contribute, then it seems inappropriate to require
from them what we should not ask of them.

  For more information on this license and the Free Software Foundation,
please visit <https://www.gnu.org/licenses/>.

  The following applies also to both programmers and users of the software:
If you modify the program (or a work based on it), you must make sure the
modified program is also distributed under the GPL, so that the community
can benefit from your changes.

                    TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list must meet this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in, but do not themselves form
part of, the program.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and convey covered works that you do not
convey, without conditions as long as your license otherwise remains
in force.  You may convey covered works to others for whatever purpose
you wish, without conditions, so long as you meet the following conditions:

    (a) You must give any other recipients of the Program or
    works based on it a copy of this License; and

    (b) You must cause any modified files to carry prominent notices
    stating that you changed the files and the date of any change; and

    (c) You must retain, in the source form of any work based on the
    Program that you convey, any copyright, patent, trademark, and
    attribution notices from the source form of the Program,
    excluding those notices that do not pertain to any part of
    the work; and

    (d) If the work has an interactive user interface, each
    version must display appropriate Legal Notices; however,
    if the Program has interactive interfaces that do not
    display Legal Notices, your work need not do so.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of all copyright and license notices from the
source form of the Program, excluding those notices that do not pertain
to any part of the Program; and provide the complete corresponding
source code under a copy of this License.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the source code form, under the terms
of section 4, provided that you also meet all of these conditions:

    (a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    (b) The work must carry prominent notices stating that it is
    released under this License and the conditions of this License.

    (c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.

    (d) You must give a copy of this License with every copy of the
    work you convey.

    (e) You must not impose any further restrictions on the exercise of the
    rights granted or affirmed under this License.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    (a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    (b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the Corresponding
    Source from a network server at no charge.

    (c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    (d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    (e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    (a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    (b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    (c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    (d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    (e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    (f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material or a modified version of
    it.

  Additional permissions may be subject to the GPL-3.0 terms.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a copyright holder is reinstated (a) provisionally,
unless and until the copyright holder explicitly and finally
terminates your license, and (b) permanently, if the copyright holder
fails to notify you of the violation by some reasonable means prior to
60 days after the cessation.

  Moreover, your license from a copyright holder is reinstated permanently
if the copyright holder notifies you of the violation by some reasonable
means and you are the first to receive notification of a copyrighted
violation applicable to this license after 60 days.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or conveying a
covered work (or operating any platform based on it), you indicate
your acceptance of this License to work with, and to propagate and
modify it given your copies and sources.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  12. Reciprocity.

  If you convey a covered work, you must comply with both the terms of
this License and any other applicable licenses.  If you impose any
further restrictions on the exercise of the rights granted or affirmed
under this License, you may lose your own rights to use the work.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
version 3, shall apply to the combination as a whole.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, additional permissions cannot be imposed on
you by any version of this License, and you may not accept any
additional permissions imposed by any version of this License.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

END OF TERMS AND CONDITIONS

Copyright (c) 2026 github-novel-serialization-skill contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```


### 7.5 `CODE_OF_CONDUCT.md` [Description Only]

Use the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) template. Fill in:
- Project name: `github-novel-serialization-skill`
- Contact email: `[INSERT_CONTACT_EMAIL]`

### 7.6 `CONTRIBUTING.md` [Description Only]

Must cover:
- How to report bugs (link to issue template)
- How to suggest features (link to feature request template)
- How to submit PRs (branch naming, commit format, review process)
- Development setup
- Code style (Markdown linting rules)
- Module contribution guidelines (how to add a new module)
- Recognition policy

### 7.7 `SECURITY.md` [Description Only]

Must cover:
- Supported versions
- How to report a vulnerability (email or GitHub private advisory)
- Response timeline expectations
- Disclosure policy

### 7.8 `CHANGELOG.md` [Full Content]

Use [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. The project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Template:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure

### Changed
- Changes to existing functionality

### Deprecated
- Soon-to-be removed functionality

### Removed
- Removed functionality

### Fixed
- Bug fixes

### Security
- Vulnerability fixes
```

### 7.9 `.github/ISSUE_TEMPLATE/bug-report.yml` [Full Content]

```yaml
name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug"]
assignees:
  - octocat
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: bug-description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
      placeholder: Describe the bug...
    validations:
      required: true
  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior.
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true
  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: A clear and concise description of what you expected to happen.
    validations:
      required: true
  - type: textarea
    id: actual-behavior
    attributes:
      label: Actual Behavior
      description: A clear and concise description of what actually happened.
    validations:
      required: true
  - type: input
    id: environment
    attributes:
      label: Environment
      description: AI tool, model, and version used.
      placeholder: "e.g., Claude Code v1.0, Claude 3 Opus, macOS 14"
  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots / Logs
      description: If applicable, add screenshots or logs to help explain your problem.
```

### 7.10 `.github/ISSUE_TEMPLATE/feature-request.yml` [Full Content]

```yaml
name: Feature Request
description: Suggest an idea for this project
title: "[Feature]: "
labels: ["enhancement"]
assignees:
  - octocat
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a feature request!
  - type: textarea
    id: problem-statement
    attributes:
      label: Problem Statement
      description: Is your feature request related to a problem? Please describe.
      placeholder: A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]
    validations:
      required: true
  - type: textarea
    id: proposed-solution
    attributes:
      label: Proposed Solution
      description: Describe the solution you'd like.
      placeholder: A clear and concise description of what you want to happen.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Describe alternatives you've considered.
      placeholder: A clear and concise description of any alternative solutions or features you've considered.
  - type: input
    id: module-affected
    attributes:
      label: Module Affected
      description: Which module(s) does this feature affect?
      placeholder: "e.g., modules/worldbuilding/, modules/chapter-writing/"
```

### 7.11 `.github/ISSUE_TEMPLATE/config.yml` [Full Content]

```yaml
blank_issues_enabled: false
contact_links:
  - name: Questions & Discussions
    url: https://github.com/[OWNER]/[REPO]/discussions
    about: Ask questions and discuss ideas
```

### 7.12 `.github/PULL_REQUEST_TEMPLATE.md` [Description Only]

Must include:
- Description of changes
- Which module(s) affected
- Checklist: tests, docs, CHANGELOG updated, no breaking changes
- Harness compliance confirmation
- License compliance confirmation

> **Template Content:**
>
> ```markdown
> ## Description of Changes
>
> <!-- Describe the changes you made -->
>
> ## Affected Module(s)
>
> <!-- Which module(s) does this PR affect? -->
> - [ ] modules/worldbuilding/
> - [ ] modules/character-design/
> - [ ] modules/chapter-writing/
> - [ ] modules/continuity-check/
> - [ ] modules/publishing-workflow/
> - [ ] modules/continuity-tracker/
> - [ ] references/
> - [ ] prompts/
> - [ ] Other (please specify)
>
> ## Checklist
>
> - [ ] I have read the CONTRIBUTING.md guide
> - [ ] My changes follow the coding style guidelines
> - [ ] I have updated documentation where needed
> - [ ] I have updated CHANGELOG.md
> - [ ] My changes do not introduce breaking changes
> - [ ] I have added tests to cover my changes (if applicable)
> - [ ] All existing tests pass
> - [ ] License files are up to date (GPL-3.0 in LICENSE, CC BY-NC-SA 4.0 in LICENSES/)
>
> ## Harness Compliance Confirmation
>
> - [ ] Constraint before generation: Rules are defined before workflow steps
> - [ ] Structured memory: State is persisted in structured files
> - [ ] Verification gates: Checks are in place before publish
> - [ ] Modular decomposition: No circular dependencies
> - [ ] Feedback loops: Structured feedback mechanism exists
> - [ ] Progressive disclosure: Content is layered appropriately
> - [ ] Context budget management: Files are under line limits
> - [ ] Human-in-the-loop: Manual oversight steps are present
> - [ ] Error recovery: State snapshots are maintained
> - [ ] Role isolation: Each module has single responsibility
> - [ ] License compliance: GPL-3.0 and CC BY-NC-SA 4.0 headers present where required
>
> ## Related Issues
>
> <!-- Link to related issues -->
> Closes #
> ```

### 7.13 `.github/FUNDING.yml` [Full Content]

```yaml
# Replace with your funding information
github: [YOUR_GITHUB_USERNAME]
```

### 7.14 `.github/dependabot.yml` [Full Content]

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 7.15 `.github/workflows/novel-release.yml` [Full Content]

A GitHub Actions workflow template for automated chapter release.

```yaml
name: Novel Release

on:
  push:
    tags:
      - 'v*'
      - 'chapter-*'

permissions:
  contents: write
  packages: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate Chapter Format
        run: |
          echo "Validating chapter file format..."
          # Check that chapter files follow naming convention: ch-{number}-{title}.md
          find chapters/ -name 'ch-*' -type f | while read -r file; do
            if [[ ! "$file" =~ ^chapters/ch-[0-9]+-.*\.md$ ]]; do
              echo "ERROR: Invalid chapter file format: $file"
              exit 1
            fi
          done
          echo "Chapter format validation passed."

      - name: Verify License Compliance
        run: |
          echo "Verifying license compliance..."
          # Check LICENSE file exists and contains GPL-3.0
          if [ ! -f LICENSE ]; then
            echo "ERROR: LICENSE file not found"
            exit 1
          fi
          if ! grep -q "GNU GENERAL PUBLIC LICENSE" LICENSE; then
            echo "ERROR: LICENSE file does not contain GPL-3.0 text"
            exit 1
          fi
          # Check LICENSES directory for CC BY-NC-SA 4.0
          if [ ! -d LICENSES ]; then
            echo "ERROR: LICENSES directory not found"
            exit 1
          fi
          if [ ! -f LICENSES/CC-BY-NC-SA-4.0.txt ]; then
            echo "ERROR: LICENSES/CC-BY-NC-SA-4.0.txt not found"
            exit 1
          fi
          echo "License compliance verification passed."

      - name: Run Continuity Check
        run: |
          echo "Running continuity verification..."
          # Run the continuity check module
          if [ -f modules/continuity-check/SKILL.md ]; then
            echo "Continuity check module found."
          else
            echo "WARNING: Continuity check module not found."
          fi

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
          files: |
            chapters/*.md
            SKILL.md
            README.md

      - name: Generate Release Notes
        run: |
          echo "Generating release notes..."
          TAG_NAME=${{ github.ref_name }}
          echo "Release tag: $TAG_NAME"
          # Extract changelog entries for this version
          if [ -f CHANGELOG.md ]; then
            echo "CHANGELOG entries for $TAG_NAME:"
            sed -n "/## \\[$TAG_NAME\\]/,/## \\[/p" CHANGELOG.md | head -n -1
          fi
```


---

## 8. File Size & Splitting Rules

### 8.1 Hard Limit

**No single file shall exceed 500 lines.** This applies to:
- SKILL.md (root and all modules)
- references/method-patterns.md (and its split modules)
- prompts/*.md
- Any other Markdown file in the project

> **Exception**: `README FOR AI.md` (this document) is a meta-instruction/seed file and is exempt from the 500-line limit, as it serves as the authoritative generation specification.

### 8.2 Splitting Protocol

When a file approaches 500 lines:
1. Identify logical section boundaries
2. Extract each section into its own file with a descriptive name
3. Replace the extracted section with a one-line pointer: `See [filename](filepath) for details.`
4. Update all cross-references

### 8.3 Split Example

If `method-patterns.md` exceeds 500 lines:

```text
references/
├── method-patterns.md                  # Now an INDEX only (~30 lines)
├── method-patterns-worldbuilding.md    # Extracted: world-building templates
├── method-patterns-character.md        # Extracted: character design templates
├── method-patterns-chapter.md          # Extracted: chapter writing templates
├── method-patterns-continuity.md       # Extracted: continuity tracking templates
└── method-patterns-publishing.md       # Extracted: publishing workflow templates
```

The master `method-patterns.md` becomes:

```markdown
# Method Patterns — Index

This file is an index. Detailed templates are split into sub-modules.

| Module | File | Content |
|--------|------|---------|
| World-Building | [method-patterns-worldbuilding.md](method-patterns-worldbuilding.md) | Magic systems, geography, politics |
| Character Design | [method-patterns-character.md](method-patterns-character.md) | Character sheets, arcs, voice |
| Chapter Writing | [method-patterns-chapter.md](method-patterns-chapter.md) | Scene structure, pacing, dialogue |
| Continuity | [method-patterns-continuity.md](method-patterns-continuity.md) | State tracking, timeline, ledger |
| Publishing | [method-patterns-publishing.md](method-patterns-publishing.md) | Git workflow, release format |
```

---

## 9. Versioning Strategy

The project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **MAJOR** version: Increment for incompatible API/skill contract changes
- **MINOR** version: Increment for backwards-compatible functionality additions
- **PATCH** version: Increment for backwards-compatible bug fixes

Version tags follow the format `v{major}.{minor}.{patch}` (e.g., `v1.2.3`).

---

## 10. Quality Assurance Checklist

Before finalizing the generated project, verify:

- [ ] SKILL.md has valid YAML frontmatter with `name` and `description`
- [ ] SKILL.md body is ≤500 lines
- [ ] SKILL.md contains NO code templates or long-form methodology
- [ ] All code templates are in `references/method-patterns.md` (or split modules)
- [ ] `prompts/` files are self-contained and copy-pasteable
- [ ] `prompts/` files include `{{OUTPUT_LANGUAGE}}` placeholder
- [ ] All module SKILL.md files have valid YAML frontmatter
- [ ] All module SKILL.md files are ≤500 lines
- [ ] No file exceeds 500 lines (see Section 8.1 for exceptions)
- [ ] All GitHub standard files are present and properly formatted
- [ ] Cross-references between files are valid
- [ ] `{{OUTPUT_LANGUAGE}}` instruction appears in SKILL.md, all prompts, and all module SKILLs (see Section 0.3 for authoritative declaration)
- [ ] Harness Engineering compliance matrix is fully satisfied
- [ ] `.gitignore` covers all necessary patterns
- [ ] `CHANGELOG.md` follows Keep a Changelog format
- [ ] `LICENSE` file contains full GPL-3.0 text
- [ ] `LICENSES/CC-BY-NC-SA-4.0.txt` contains full CC BY-NC-SA 4.0 license text
- [ ] SKILL.md frontmatter declares `license: GPL-3.0` and `novel_content_license: CC-BY-NC-SA-4.0`
- [ ] Generated novel content includes CC BY-NC-SA 4.0 license header
- [ ] `.editorconfig` covers both `*.yml` and `*.yaml`
- [ ] `.github/dependabot.yml` is present

---

## 11. Automated Verification

To ensure generated projects meet all requirements, run the following verification steps:

1. **Line count check**: Verify no file exceeds 500 lines (excluding exempt files)
2. **File presence check**: Verify all mandatory files from Section 1 directory tree exist
3. **YAML validation**: Validate all `.yml` files are syntactically correct
4. **Link check**: Verify all internal cross-references resolve
5. **Language check**: Verify `{{OUTPUT_LANGUAGE}}` placeholder appears in all required locations
6. **Frontmatter check**: Verify all SKILL.md files have valid YAML frontmatter
7. **License check**: Verify `LICENSE` file contains "GNU GENERAL PUBLIC LICENSE" and version "3"
8. **Novel content license check**: Verify `LICENSES/CC-BY-NC-SA-4.0.txt` exists and contains "Creative Commons"
9. **SKILL.md license field check**: Verify `license: GPL-3.0` and `novel_content_license: CC-BY-NC-SA-4.0` are present in SKILL.md frontmatter

---

## 12. Generation Sequence

> **IMPORTANT**: `README FOR AI.md` (this file) is the **seed file**. It must be created first as the authoritative specification. All other files are generated based on its instructions.

Execute file generation in this order to maintain referential integrity:

1. `README FOR AI.md` — **seed file (already created)**
2. `references/method-patterns.md` (and split modules) — templates first
3. `references/glossary.md` — terminology
4. `references/examples/*` — worked examples
5. `modules/*/SKILL.md` — sub-skills referencing templates
6. `SKILL.md` — root index referencing modules and references
7. `prompts/README.md` — usage guide
8. `prompts/01-implement-method.md` — implementation prompt
9. `prompts/02-robustness-checks.md` — validation prompt
10. `README.md` — project overview
11. `.gitignore`, `.editorconfig`, `LICENSE`, `LICENSES/CC-BY-NC-SA-4.0.txt`, `.github/dependabot.yml`
12. `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`
13. `.github/` community files (issue templates, PR template, FUNDING, workflows)

---

## 13. Anti-Patterns — What NOT To Do

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|---------------|-----------------|
| Embedding full templates in SKILL.md | Bloats context, violates progressive disclosure | Put templates in `references/`, SKILL.md only indexes |
| Making `prompts/` files auto-invocable | Defeats the dual-mode design | Keep them as standalone copy-paste templates |
| Writing prompts in a specific language | Limits portability | Write in English with `{{OUTPUT_LANGUAGE}}` placeholder |
| Creating monolithic modules | Violates modularization principle | Each module = one responsibility, ≤500 lines |
| Hardcoding output language | Prevents multilingual use | Always use `{{OUTPUT_LANGUAGE}}` variable (see Section 0.3) |
| Skipping verification gates | Breaks harness engineering | Every chapter must pass continuity check before publish |
| Putting state in conversation context | Loses state across sessions | Persist state in structured Markdown files |
| Ignoring `.gitignore` | Commits temp files, leaks secrets | Include comprehensive ignore rules |
| Missing license headers | Violates dual licensing model | Every novel file must include CC BY-NC-SA 4.0 header; all infrastructure files must comply with GPL-3.0 |

> **NOTE**: Sections 0.4 (Core Constraints) and this Anti-Patterns table serve complementary purposes: Section 0.4 states the positive rules, while this table illustrates common violations. Together they form the complete constraint specification.

---

## 14. Final Note

This Skill project is not just a collection of prompts. It is a **harness-engineered system** that transforms a raw LLM into a reliable, stateful, multi-session novel-writing agent. Every file exists to constrain, guide, and verify. The goal is deterministic quality — not lucky outputs.

**Dual Licensing Notice**:
- The Skill infrastructure (code, templates, prompts, configuration) is licensed under **GNU General Public License v3.0 (GPL-3.0)**. See the `LICENSE` file for full terms.
- Generated novel content (chapters, character sheets, world-building documents) is licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**. See the `LICENSES/CC-BY-NC-SA-4.0.txt` file for full terms.

Generate all files now. Follow every specification above. Do not improvise structure.
