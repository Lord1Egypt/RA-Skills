---
name: AI Context Gen
description: Analyzes any codebase and generates AI coding assistant context files for 5 tools simultaneously — CLAUDE.md (Claude Code), AGENTS.md (OpenClaw/Codex), .cursorrules (Cursor), .windsurfrules (Windsurf), and .github/copilot-instructions.md (GitHub Copilot). Reads tech stack, architecture, conventions, and testing setup to produce project-specific, not generic, context. Saves 30-60 minutes of manual writing per project. Trigger: "generate context files", "write CLAUDE.md", "create cursorrules", "AI context setup".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - productivity
  - dx
  - claude-md
  - cursorrules
  - ai-context
  - developer-experience
  - onboarding
---

# phy-ai-context-gen — AI Coding Assistant Context Generator

Analyzes a codebase and generates accurate, **project-specific** context files for every major AI coding assistant — not boilerplate, but rules derived from what your codebase actually does.

## Trigger Phrases

Use when the user says any of:
- "generate context files", "write CLAUDE.md for this project"
- "create .cursorrules", "set up AI context", "AI assistant setup"
- "help the AI understand this project", "generate AGENTS.md"
- "write copilot instructions", "setup Windsurf rules"
- `phy-ai-context-gen` or `/ai-context-gen`

## What Gets Generated

| File | Tool | Purpose |
|------|------|---------|
| `CLAUDE.md` | Claude Code (Anthropic) | Project instructions, API keys, conventions |
| `AGENTS.md` | OpenClaw / Codex / Antigravity | Agent behavior, allowed commands, tool restrictions |
| `.cursorrules` | Cursor AI | Inline suggestions style, framework rules |
| `.windsurfrules` | Windsurf (Codeium) | Same as cursorrules, Windsurf format |
| `.github/copilot-instructions.md` | GitHub Copilot | Completion style, language patterns |

## Instructions

When this skill is invoked:

### Phase 1 — Gather Project Intelligence

Run ALL of the following in parallel to understand the project:

```bash
# 1. Directory structure (top 3 levels)
find . -maxdepth 3 -type f -name "*.json" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" | grep -v node_modules | grep -v .git | head -30

# 2. Detect package managers and tech stack
cat package.json 2>/dev/null | head -60
cat requirements.txt 2>/dev/null || cat pyproject.toml 2>/dev/null | head -40
cat Cargo.toml 2>/dev/null | head -30
cat go.mod 2>/dev/null | head -20
cat composer.json 2>/dev/null | head -30
cat Gemfile 2>/dev/null | head -20

# 3. Read README (if present)
cat README.md 2>/dev/null | head -80

# 4. Detect test framework
ls -la tests/ test/ __tests__/ spec/ 2>/dev/null
cat jest.config.* 2>/dev/null | head -20
cat pytest.ini 2>/dev/null || cat setup.cfg 2>/dev/null | grep -A10 "\[tool:pytest\]"

# 5. Detect linter / formatter
cat .eslintrc* 2>/dev/null | head -30
cat .prettierrc* 2>/dev/null | head -20
cat .ruff.toml 2>/dev/null || cat ruff.toml 2>/dev/null | head -20
cat .flake8 2>/dev/null | head -20

# 6. Detect CI
ls -la .github/workflows/ 2>/dev/null | head -10
ls -la .gitlab-ci.yml .circleci/ 2>/dev/null

# 7. Check for existing context files to avoid overwriting
ls -la CLAUDE.md AGENTS.md .cursorrules .windsurfrules .github/copilot-instructions.md 2>/dev/null

# 8. Detect framework
ls -la src/app/ src/pages/ app/ pages/ 2>/dev/null  # Next.js / React Router
ls -la src/main.py app.py manage.py 2>/dev/null     # Python
ls -la cmd/ main.go 2>/dev/null                      # Go
```

Also read these files if they exist (limit to first 40 lines each):
- `src/index.ts`, `src/main.ts`, `src/app.ts` — entry points
- `src/index.js`, `src/main.js`, `src/app.js`
- `main.py`, `app.py`, `__init__.py`
- `src/main.rs`, `main.go`
- Any existing `CLAUDE.md`, `.cursorrules` (read current content before generating)

### Phase 2 — Synthesize Project Profile

From the gathered data, determine:

1. **Primary language(s)** — TypeScript, Python, Go, Rust, Java, Ruby, PHP, etc.
2. **Framework(s)** — Next.js, FastAPI, Django, Gin, Rails, Spring, etc.
3. **Package manager** — npm/yarn/pnpm, pip/poetry/uv, cargo, go mod, etc.
4. **Test runner** — Jest, Vitest, pytest, go test, RSpec, etc.
5. **Linter/formatter** — ESLint/Prettier, Ruff/Black, rustfmt, gofmt, etc.
6. **Build tool** — tsc, webpack, vite, esbuild, make, gradle, etc.
7. **Project type** — web app, API, CLI, library, monorepo, data pipeline, etc.
8. **Key conventions** — naming, directory structure, error handling patterns, etc.

**Critical:** If you cannot determine a value from the files, write `# TODO: fill in` rather than inventing plausible-sounding defaults.

### Phase 3 — Generate All 5 Files

Generate each file in sequence, then confirm with the user before writing.

---

#### File 1: `CLAUDE.md`

Format:
```markdown
# [Project Name] — Claude Code Instructions

## Project Overview
[1-2 sentences: what this project does, who uses it]

## Tech Stack
- **Language**: [primary language + version if found]
- **Framework**: [framework name]
- **Package manager**: [npm/yarn/pnpm/pip/poetry/cargo/go]
- **Test runner**: [test command e.g. `npm test`, `pytest`, `go test ./...`]

## Development Commands
```bash
# Install dependencies
[install command]

# Run dev server
[dev command]

# Run tests
[test command]

# Build
[build command]

# Lint
[lint command]
```

## Code Conventions
- [naming convention: snake_case / camelCase / PascalCase — per detected patterns]
- [file size guideline if detectable from existing code]
- [import style: relative vs absolute]
- [error handling pattern if detectable]

## Project Structure
```
[key directories with one-line descriptions, inferred from actual structure]
```

## Important Notes
- [any .env files to be aware of]
- [any generated files not to edit]
- [any protected paths or files]

## Context Awareness
In long conversations (10+ exchanges), proactively re-check constraints from earlier in the session.
```

---

#### File 2: `AGENTS.md`

Format:
```markdown
# [Project Name] — Agent Instructions

## Project Context
[Brief description of what this project does]

## Allowed Operations
- Read any file in the repository
- Run: `[test command]`, `[lint command]`, `[build command]`
- Edit files in: `src/`, `tests/`, `[other safe directories]`

## Restricted Operations
- Do NOT run: `rm -rf`, destructive database commands
- Do NOT modify: `[generated files]`, `[config files that break CI]`
- Do NOT commit without user confirmation
- Do NOT push to remote without explicit approval

## Tech Stack
[Same as CLAUDE.md tech stack section]

## Development Workflow
1. Understand the task — read relevant files before writing
2. Write tests first if adding new functionality
3. Run tests: `[test command]`
4. Run linter: `[lint command]`
5. Only then make the change

## Key File Locations
- Entry point: `[detected entry file]`
- Tests: `[test directory]`
- Config: `[config files]`
- Types/models: `[types directory if present]`

## Tool Preferences
- Search code: use Grep, not `grep` command
- Read files: use Read tool, not `cat`
- File operations: prefer Edit over Write for existing files
```

---

#### File 3: `.cursorrules`

Format (Cursor prefers compact, imperative style):
```
# [Project Name] Cursor Rules

## Stack
[Language] + [Framework] project.
Package manager: [manager]. Test runner: [test runner].

## Code Style
- Use [snake_case/camelCase] for [variables/functions]
- Use [PascalCase] for [classes/components]
- [Import style instruction]
- Max function length: [50/40/30] lines
- [Type annotation instruction for TypeScript/Python]

## Patterns to Follow
- [Detected error handling pattern]
- [Detected async pattern]
- [Testing pattern — e.g. "write tests in __tests__/ using Jest describe/it blocks"]

## Patterns to Avoid
- No `any` types in TypeScript / no untyped Python functions
- No `console.log` in production code — use [detected logger]
- No hardcoded credentials or magic numbers
- [Framework-specific antipatterns if detected]

## File Structure
- New features go in: [detected directory]
- Tests go in: [test directory]
- Shared utilities: [utils directory if present]

## Before Suggesting
1. Check if a similar utility already exists in [utils/lib/common directory]
2. Follow the naming conventions in the surrounding files
3. Run `[test command]` to verify changes
```

---

#### File 4: `.windsurfrules`

Use the **same content as `.cursorrules`** — Windsurf reads the same format. Note this explicitly so the user knows both files are identical (they can diverge later if preferred).

---

#### File 5: `.github/copilot-instructions.md`

Format (Copilot prefers markdown with ## sections):
```markdown
# GitHub Copilot Instructions for [Project Name]

## Project Type
[Project type description]. Built with [framework] in [language].

## Coding Standards

### Naming
- Variables and functions: [convention]
- Classes and types: [convention]
- Files: [convention]
- Constants: [convention]

### TypeScript / Python / Go specifics
[Language-specific rules derived from actual codebase patterns]

### Error Handling
[Detected error handling pattern — e.g. "Use try/catch with typed errors, not bare exceptions"]

## Testing
- Framework: [test framework]
- Test files location: [test directory]
- Pattern: [describe/it blocks, pytest classes, etc.]
- Always write tests for new public functions

## Imports
[Import ordering preference if detectable — e.g. "stdlib → third-party → local"]

## What to Avoid
- [Antipatterns specific to this project]
- Do not suggest deprecated [framework] APIs
- Prefer [detected utility library] over implementing from scratch
```

---

### Phase 4 — Write Files

Before writing:
1. **Check if files already exist** — if they do, show a diff of what would change and ask for confirmation
2. Create `.github/` directory if it doesn't exist (for copilot-instructions.md)
3. Write all 5 files

```bash
# Create .github directory if needed
mkdir -p .github

# Write files
# (Use Write tool for each file)
```

After writing, confirm:
```
✅ Generated 5 AI context files:
  - CLAUDE.md          (Claude Code)
  - AGENTS.md          (OpenClaw / Codex)
  - .cursorrules       (Cursor AI)
  - .windsurfrules     (Windsurf)
  - .github/copilot-instructions.md  (GitHub Copilot)

Next step: Review CLAUDE.md and fill in any # TODO: sections.
Add to .gitignore if you don't want to commit: echo ".cursorrules" >> .gitignore
```

---

## Options

### Generate only one file

User can request a single file:
- "just write the CLAUDE.md" → generate only CLAUDE.md
- "just .cursorrules" → generate only that file
- "update my AGENTS.md" → read existing AGENTS.md, merge with current analysis, write updated version

### Force regenerate (overwrite)

If files already exist, user can say "regenerate" or "overwrite" to skip the diff confirmation.

### Dry run

"show me what you'd generate" → display all 5 files without writing them.

---

## Quality Rules

**DO:**
- Pull specific facts from actual project files (exact framework version, real test command, actual directory names)
- Write `# TODO: [what to fill in]` when information isn't determinable
- Keep instructions short and actionable — each rule should be one line
- Ensure the test command matches what's actually in package.json scripts

**DON'T:**
- Invent plausible-sounding tech stack details you can't confirm
- Copy generic boilerplate (e.g. "write clean, readable code" — useless)
- Add more than 3 levels of nesting in any file
- Generate identical content for every project

---

## Differentiation vs prd-writer / large-codebase-workflow

| Skill | Focus |
|-------|-------|
| `phy-ai-context-gen` | **Generates files** for AI coding tools based on real codebase analysis |
| `phy-prd-writer` | Generates product requirement documents through Q&A |
| `large-codebase-workflow` | Best practices guide for working with large repos |
| `phy-living-adr` | Architecture Decision Records from git diffs |

This skill is the **onboarding layer** — run it once at project start, or whenever you bring a new AI assistant into an existing project. It removes the "cold start" penalty where the agent wastes the first few messages rediscovering obvious context.

---

## Example Usage

**Input:** User runs `/ai-context-gen` in a Next.js 15 + TypeScript + Prisma project.

**What Claude does:**
1. Reads `package.json` → detects Next.js 15, TypeScript, Prisma, Jest, ESLint, Prettier
2. Reads `README.md` → project description
3. Scans `src/` → finds `app/`, `components/`, `lib/`, `prisma/`
4. Detects: camelCase variables, PascalCase components, `.env.local` for secrets

**Generated `.cursorrules` excerpt:**
```
# MyApp Cursor Rules
Next.js 15 App Router + TypeScript + Prisma project.
Package manager: pnpm. Test runner: jest.

## Code Style
- Variables/functions: camelCase
- React components: PascalCase in PascalCase.tsx files
- Imports: React → Next.js → third-party → @/lib → @/components → relative
- No `any` types — use Prisma generated types or explicit interfaces

## Patterns to Follow
- Server components by default, add "use client" only when needed
- Database access only in Server Components or API routes (never in client components)
- Prisma queries go in lib/db/ only

## Before Suggesting
1. Check lib/utils.ts for existing helpers
2. Check components/ui/ for existing UI primitives
3. Run: pnpm test && pnpm lint
```

**Time saved:** ~45 minutes of manual writing per new project onboarding.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
