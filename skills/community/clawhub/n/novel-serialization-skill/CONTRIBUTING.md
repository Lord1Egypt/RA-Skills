# Contributing to GitHub Novel Serialization Skill

First off, thank you for considering contributing to this project! It's people
like you that make this Skill useful for the novel writing community.

The following is a set of guidelines for contributing to this project. These are
mostly guidelines, not rules. Use your best judgment, and feel free to propose
changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Project Structure](#project-structure)
  - [Development Environment](#development-environment)
  - [Development Workflow](#development-workflow)
- [How To Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Review Process](#review-process)
- [Prompts Directory — Dual-Mode Design Philosophy](#prompts-directory--dual-mode-design-philosophy)
- [Module Development Guidelines](#module-development-guidelines)
  - [The 500-Line Rule](#the-500-line-rule)
  - [Module SKILL.md Structure](#module-skillmd-structure)
- [License Compliance](#license-compliance)
- [Recognition Policy](#recognition-policy)
- [Style Guidelines](#style-guidelines)
- [Git Conventions](#git-conventions)

## Code of Conduct

This project and everyone participating in it is governed by our
[Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to
uphold this code.

## Getting Started

### Project Structure

```
github-novel-serialization-skill/
│
├── README.md                           # Project overview, quick start, architecture diagram
├── README FOR AI.md                    # Meta-instructions for AI generation (seed file)
├── .gitignore                          # Git ignore rules
├── .gitattributes                      # Line-ending and binary policy
├── .editorconfig                       # Editor configuration
├── .markdownlint.json                  # Markdown lint rules
├── .pre-commit-config.yaml             # Local gates (hygiene, references, tests, commit format)
├── pyproject.toml                      # Project metadata + pytest / ruff configuration
├── requirements-dev.txt                # Development-only dependencies
├── Makefile                            # Thin proxy to scripts/dev.py
├── security.txt                        # RFC 9116 machine-readable contact
├── LICENSE                             # GNU General Public License v3.0 (GPL-3.0)
├── LICENSES/                           # Additional license texts
│   └── CC-BY-NC-SA-4.0.txt             # Full CC BY-NC-SA 4.0 license text
├── CODE_OF_CONDUCT.md                  # Community behavior standards
├── CONTRIBUTING.md                     # Contribution guidelines
├── SECURITY.md                         # Security policy & vulnerability reporting
├── SUPPORT.md                          # Where to get help
├── GOVERNANCE.md                       # Roles, responsibilities, decision process
├── CHANGELOG.md                        # Version history (Keep a Changelog format)
├── CITATION.cff                        # Citation metadata
│
├── SKILL.md                            # Index + quick-reference (≤500 lines)
│
├── docs/                               # Engineering documentation
│   ├── README.md                       # Index of this directory
│   └── adr/                            # Architecture decision records
│
├── tests/                              # Regression tests for scripts/
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
├── scripts/                            # Shared automation (invoked from a subproject root)
│   ├── README.md                       # Catalog & invocation conventions
│   ├── dev.py                          # One entry point for every local gate
│   ├── check_refs.py                   # Reference integrity (release-only rule)
│   ├── scan_hygiene.py                 # CRLF / mojibake / junk / line budget
│   ├── init_subproject.py              # Subproject scaffold
│   ├── humanizer_check.py              # De-AI-tone gate
│   ├── review_all.py                   # All-in-one review report
│   └── _review_lib.py                  # Shared library for the review scripts
│
└── .github/                            # GitHub community health files
    ├── CODEOWNERS                      # Directory-level review assignment
    ├── ISSUE_TEMPLATE/
    │   ├── bug-report.yml
    │   ├── feature-request.yml
    │   ├── errata.yml
    │   ├── docs.yml
    │   └── config.yml
    ├── PULL_REQUEST_TEMPLATE.md
    ├── PULL_REQUEST_TEMPLATE/
    │   └── content.md
    ├── FUNDING.yml
    ├── dependabot.yml
    ├── labels.yml
    ├── release.yml
    └── workflows/
        ├── ci.yml                      # hygiene + references + tests + metadata
        ├── codeql.yml                  # Security scan
        ├── label-sync.yml              # Label taxonomy
        ├── stale.yml                   # Stale issue / PR handling
        └── novel-release.yml           # Automated release workflow template
```

### Development Environment

The runtime scripts need nothing but the standard library. The gates need a
little more:

```bash
python -m pip install -r requirements-dev.txt
pre-commit install
pre-commit install --hook-type commit-msg   # enforces the commit format
```

Everything CI runs is available locally through one entry point:

```bash
python scripts/dev.py all        # hygiene + references + lint + tests
make all                         # same, where make is available
```

Individual gates: `test`, `hygiene`, `refs`, `lint`, `scaffold`.

Tests live in `tests/` and run in about a second. A change to a script is
expected to come with a test; a change that alters what a script reports must
update the tests that assert the old behaviour, in the same commit.

### Development Workflow

1. Fork the repository
2. Create a branch using the naming convention below (`git checkout -b feat/my-feature`)
3. Make your changes following the guidelines below
4. Validate your changes. All four gates run locally:
   ```bash
   python scripts/dev.py all
   ```
   They check, in order:
   - **hygiene** — no CRLF, no encoding damage, no editor droppings, no file
     over the 500-line budget (see [The 500-Line Rule](#the-500-line-rule))
   - **refs** — every reference resolves, and no release file points outside
     the release tree (see [ADR-0002](docs/adr/0002-release-references-release.md))
   - **lint** — byte-compilation, plus ruff when installed
   - **test** — the `tests/` suite

   To read a full report instead of a pass/fail, call the scripts directly;
   see [scripts/README.md](scripts/README.md).
5. Commit your changes using conventional commit format
6. Push to the branch (`git push origin feat/my-feature`)
7. Open a Pull Request

## How To Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out
that you don't need to create one. When you are creating a bug report, please
include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Describe the behavior you observed and what you expected to see
- Include screenshots or animated GIFs if possible
- Include details about your environment (OS, editor, AI tool used)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an
enhancement suggestion, please include:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Explain why this enhancement would be useful to most users
- List some examples of how this enhancement would be used
- Explain why this enhancement wouldn't fit in existing modules

### Submitting Pull Requests

- Ensure your code follows the project's style guidelines
- Ensure the manual validation checks in
  [Development Workflow](#development-workflow) pass
- Update documentation as needed
- Follow the [Git Conventions](#git-conventions) below
- Reference any related issues in your PR description

### Review Process

1. A maintainer triages the PR within 7 days and applies labels.
2. Review is against the checklist in
   [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md), including the
   Harness Compliance and license-compliance confirmations.
3. At least one approving review is required. Changes requested must be addressed in the
   same branch; do not open a replacement PR.
4. Merging is squash-only onto the default branch, and the merge commit message must follow
   the [Commit Message Format](#commit-message-format) below.
5. PRs touching `references/`, `modules/`, or `prompts/` additionally require confirmation
   that all cross-references still resolve and that no file exceeds 500 lines.

## Prompts Directory — Dual-Mode Design Philosophy

The `prompts/` directory contains prompt templates that operate in **dual-mode**:

1. **Human copy-paste mode** (primary): Human users open any prompt file in a text
   editor, copy its entire content, and paste it into any AI chat window
   (ChatGPT, Claude, Gemini, Copilot, etc.) to get immediate, structured output.
2. **Agent-assisted mode** (secondary): The modules under `modules/` may refer to the
   *methodology* these prompts encode when orchestrating a workflow. The prompt files
   themselves are **not** invoked directly by an agent — see
   spec Section 4.1 and the anti-pattern table in Section 13 of README FOR AI.md.

**Key rules for prompts/:**
- Files in `prompts/` are **NOT** for agent auto-invocation — they are standalone
  templates designed for human interaction
- Each prompt file must be self-contained and work independently
- The `{{OUTPUT_LANGUAGE}}` placeholder must be present in all prompt templates
  (see Section 0.3 of README FOR AI.md for the authoritative declaration)
- Prompt templates must instruct the AI to include the CC BY-NC-SA 4.0 license
  header in all generated novel content

## Module Development Guidelines

### The 500-Line Rule

Any file exceeding **500 lines** MUST be split into sub-modules under the same
directory. This is a hard constraint to ensure modularity and maintainability.

When splitting:
1. Create sub-modules with descriptive names (e.g., `method-patterns-worldbuilding.md`)
2. The master file becomes an index pointing to each split module
3. Each sub-module must be independently usable
4. Update the parent index file to reflect the new structure

#### Exemptions (must be declared, never assumed)

The budget exists to keep a file readable in review. It was written for prose and
method documents. Three kinds of file legitimately exceed it:

| Kind | Examples | Treatment |
|------|----------|-----------|
| Ledger / log | `CHANGELOG.md`, `progress.md`, decision ledger | Exempt — chronological append, never read end-to-end |
| Reference table | setting compendia | Split by domain first; if one domain is genuinely thousands of lines, split by section and link |
| Generated / seed | `README FOR AI.md` | Exempt, but never hand-edited |

Declare an exemption with `scan_hygiene.py --allow <file>` so it is visible in
CI rather than accumulating silently. A rule with unstated exceptions is a rule
nobody follows. See `references/subproject-playbook.md` Section 10.

### Module SKILL.md Structure

Each module under `modules/` must have its own `SKILL.md` with:

- **YAML Frontmatter**: Including `name`, `description`, `license: GPL-3.0`,
  `novel_content_license: CC-BY-NC-SA-4.0`
- **Purpose**: One-line description of what the module does
- **Triggers**: Keywords that activate this module
- **Constraints**: Hard rules the agent must never violate
- **Cross-References**: Pointers to `references/` for templates and patterns

## License Compliance

This project uses a **dual-licensing** model:

| Component | License | Scope |
|-----------|---------|-------|
| Skill Infrastructure | GPL-3.0 | Code, templates, prompts, SKILL.md files, GitHub workflows, configuration files |
| Generated Novel Content | CC BY-NC-SA 4.0 | Chapters, character sheets, world-building docs produced by the Skill |

**Important rules:**
- Every generated novel file MUST carry the CC BY-NC-SA 4.0 license header block before any narrative content. Where a file also carries YAML frontmatter (mandatory for chapter files — see `references/method-patterns-publishing.md` Section 3), the ordering is: frontmatter at byte 0, then the CC license header, then the narrative.
- Module SKILL.md files MUST declare both licenses in YAML frontmatter
- Prompt templates MUST instruct the AI to include the CC BY-NC-SA 4.0 header
- Do NOT mix license-protected content across license boundaries

## Recognition Policy

Contributions to this project are recognized as follows:

- **CHANGELOG.md** — Substantive changes are recorded under the release
  version in which they land, so the project history stays auditable.
- **Contributors list** — Add your GitHub handle to the **Credits** section of
  `README.md` in the same pull request as your contribution.
- **Commit attribution** — Use the Conventional Commits trailer format so
  authorship survives rebases.
- **Module authorship** — If you add a new module under `modules/`, list
  yourself in that module's `metadata.author` frontmatter field.

Recognition is opt-out: if you would rather not be named publicly, say so in
your pull request description and we will omit your handle while keeping your
Git commit authorship intact.

## Style Guidelines

- **Language**: All infrastructure files (SKILL.md, references/, prompts/, .github/)
  MUST be in English for universal compatibility
- **Markdown**: Use standard Markdown syntax; prefer ATX-style headings (`#`, `##`, etc.)
- **Markdown linting**: Follow the [markdownlint](https://github.com/DavidAnson/markdownlint)
  default rule set, with these project-specific decisions:
  - Blank line required before every heading, and before and after every fenced code block
    (a heading with no preceding blank line renders as literal text on GitHub)
  - One blank line between list items that contain multiple paragraphs; keep simple lists tight
  - No trailing whitespace in `.md` files — `.editorconfig` sets
    `trim_trailing_whitespace = false` for Markdown, so two-space line breaks are preserved
  - Use relative links for internal references, and percent-encode spaces in filenames
    (e.g. `README%20FOR%20AI.md`), because GitHub truncates a link at a raw space
  - No file exceeds 500 lines (see [The 500-Line Rule](#the-500-line-rule))
- **Code blocks**: Use language identifiers where applicable
- **Tables**: Use Markdown tables for structured data
- **Links**: Use relative links for internal references

## Git Conventions

### Branch Naming

- `feat/<name>` — New features (matches the `feat` Conventional Commit type)
- `fix/<name>` — Bug fixes
- `docs/<name>` — Documentation changes
- `refactor/<name>` — Code refactoring
- `chore/<name>` — Maintenance tasks

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Changes to the build process or auxiliary tools

**Examples:**

```
feat(worldbuilding): add magic system template
fix(chapter-writing): correct scene structure example
docs(contributing): update module development guidelines
```

### Tagging and Releases

- Use semantic versioning: `v<major>.<minor>.<patch>`
- Tags follow the format: `v1.0.0`, `v1.1.0`, `v1.1.1`, etc.
- Release notes are generated from CHANGELOG.md entries

---

Thank you for reading through this document. We look forward to your
contributions!
