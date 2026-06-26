---
name: open-source-contributor
description: "Autonomous GitHub contribution agent using the Architect-Builder pattern. Buck (main agent) handles all git/network I/O; subagents handle focused cognitive work only. Scouts issues, implements fixes, and submits PRs. Supports three difficulty levels. Triggers on: open source, github, contribution, PR, pull request, issue fix, OSS, contributor."
tags:
  - open-source
  - github
  - contribution
  - PR
  - pull-request
  - issue
  - architect-builder
  - automation
---

# Open Source Contributor

Autonomous GitHub contribution agent using the **Architect-Builder** pattern. The main agent handles all git operations and I/O; subagents handle only focused cognitive work.

## Quality Standards

- Every contribution must be **meaningful** — no typo fixes, no placeholder PRs
- Must pass CI/tests where available
- Must include proper description and tests if applicable
- Must reference the issue it fixes
- Must disclose AI assistance
- **No emojis in PR titles, descriptions, or comments.** Plain text only. Professional tone throughout.

## ⚠️ GitHub Token

Store your GitHub token securely (e.g., `~/.openclaw/.github_token`). Never log or print token values. The agent should read it silently from disk.

## Excluded Repos

Maintain a list of repos you've already contributed to (to avoid duplicate PRs). Store in your config file.

---

## Architecture: The Architect-Builder Pattern

**THE CORE RULE: Subagents do NOT clone repos, push code, or make GitHub API calls. The main agent does all I/O.**

### Why This Pattern?

Subagents timed out when trying to do full git workflows (clone large repos + modify files + push + create PR). Root causes:
1. Each tool call through cloud model proxies takes 5-58 seconds — 50 tool calls = 12+ minutes of pure latency
2. Large repo clones eat into the time budget
3. Context window fills up after many tool calls, causing stalls

The fix: **The main agent owns all I/O and git operations. Subagents only do focused cognitive work on pre-staged content.**

### How It Works

```
┌─────────────────────────────────────────────────────┐
│  MAIN AGENT — The Architect & Builder                │
│                                                       │
│  1. Research: Find issues via GitHub API              │
│  2. Stage: Clone repo, identify files, read context   │
│  3. Delegate: Send focused edit task to subagent      │
│  4. Apply: Review subagent output, apply changes      │
│  5. Push: Commit, push, create PR via GitHub API      │
│                                                       │
│  Uses: exec, GitHub API, git CLI — all I/O tools     │
└─────────────────────────────────────────────────────┘
              │
              │ Focused task + file contents (pasted inline)
              ▼
┌─────────────────────────────────────────────────────┐
│  SUBAGENT — The Specialist                           │
│                                                       │
│  Receives: Specific files + the issue + instructions │
│  Returns: Exact code changes (diff/patch/new content)│
│  Does NOT: Clone repos, push code, create PRs        │
│  Does NOT: Make GitHub API calls                      │
│  Does NOT: Browse the web                             │
│                                                       │
│  Timeout: 600s max (focused work only)                │
└─────────────────────────────────────────────────────┘
```

---

## Difficulty Levels

### Level 1: Easy — Warm-up Contributions

| Criteria | Requirement |
|----------|------------|
| Labels | `good first issue`, `help wanted`, `bug` |
| Stars | 500+ |
| Issue age | 3-30 days |
| Comments | < 10 |
| Scope | Single file, < 30 lines changed |

**Typical fixes:** UI text corrections, missing error handling, simple config fixes, accessibility improvements, missing validation.

### Level 2: Intermediate — Real Feature Work (DEFAULT)

| Criteria | Requirement |
|----------|------------|
| Labels | `bug`, `feature`, `performance`, `enhancement` |
| Stars | 1,000+ |
| Issue age | 7-60 days |
| Comments | < 5 |
| Scope | Multi-file, 30-150 lines changed |

**Typical fixes:** Dependency bumps with tests, missing API parameters, edge case fixes, missing method implementations, performance improvements.

### Level 3: Advanced — Architecture & Deep Fixes

| Criteria | Requirement |
|----------|------------|
| Labels | `bug`, `feature`, `performance`, `enhancement`, `design` |
| Stars | 2,000+ |
| Issue age | 7-90 days |
| Comments | < 8 |
| Scope | Multi-module, 100-500+ lines changed |

**Typical fixes:** Race conditions, memory leaks, API redesigns, query optimization, plugin systems, cross-platform fixes.

**Optional:** Spawn a **Council of LLMs** to evaluate approach before implementing.

---

## Pipeline: Architect-Builder Pattern

### Phase 1: Research — Main Agent Finds the Issue

The main agent searches GitHub for suitable issues:
1. Use GitHub Search API or an authenticated search script
2. Filter by difficulty level criteria (stars, age, labels, comment count)
3. Exclude already-contributed repos
4. Verify no open PRs already address the issue
5. Select the best candidate

### Phase 2: Stage — Main Agent Prepares the Workspace

The main agent does ALL the I/O work directly (no subagent):
1. Fork the repo via GitHub API
2. Shallow clone: `git clone --depth 1`
3. Create branch: `fix/<issue-number>-<short-description>`
4. Read `CONTRIBUTING.md` and relevant source files
5. Identify the files that need to change
6. Read the full content of those files
7. Prepare a focused task for the subagent with all file contents pasted inline

### Phase 3: Implement — Subagent Does Focused Cognitive Work

Spawn a **specialist subagent** with:
- `runTimeoutSeconds: 600` (10 min max — focused work only)
- `lightContext: true`
- All file contents PASTED INLINE in the task description
- Clear instructions: "Return the EXACT modified file content" or "Return a unified diff"

The subagent task MUST include:
- The exact files to modify (full content pasted inline)
- The issue being fixed (full description)
- The project's style/lint requirements (from CONTRIBUTING.md)
- A request for EXACT code changes (not a plan, the actual code)

The subagent does NOT:
- Clone repos
- Run git commands
- Make GitHub API calls
- Browse the web
- Install packages

### Phase 4: Apply & Push — Main Agent Finishes the Job

The main agent takes the subagent's output and:
1. Applies the code changes to local files
2. Runs linters/tests if available
3. Fixes any remaining issues (lint errors, test failures)
4. Commits, pushes, and creates the PR via GitHub API
5. Returns the final summary

### Phase 4.5: Council Review (Level 3 only — optional)

For Level 3 fixes that are security-sensitive or architecturally complex, spawn a **Council of LLMs** BEFORE Phase 3. Use 3 different models as Strategos, Analyticos, and Creativos with distinct analytical perspectives. If consensus is "don't implement" → skip, move to next candidate.

---

## API-First Approach (Preferred for Simple Fixes)

For simple fixes (Level 1, some Level 2), **skip cloning entirely** and use the GitHub API directly:

1. Read files via `GET /repos/{owner}/{repo}/contents/{path}`
2. Send modified content via `PUT /repos/{owner}/{repo}/contents/{path}`
3. Create PR via `POST /repos/{owner}/{repo}/pulls`

This eliminates clone time entirely and completes in 2-5 minutes.

**Use API-first when:**
- Fix touches 1-3 files
- Files are under 500 lines each
- No test suite needs to run
- No complex branching required

**Use clone when:**
- Fix touches 4+ files or needs cross-file understanding
- Need to run tests/linters locally
- Need to understand project structure deeply

---

## Configuration

Store your settings in a config file (e.g., `contrib-scout/config.json`):

```json
{
  "difficulty_level": 2,
  "github_token_path": "~/.openclaw/.github_token",
  "max_contributions_per_night": 1,
  "languages": ["python", "javascript", "typescript", "go", "rust"],
  "excluded_repos": ["your-org/your-repo"]
}
```

### Council Models (Optional)

For Level 3 Council review, configure your preferred models in `~/.openclaw/council-config.json`:

```json
{
  "council_models": [
    "your-first-model-here",
    "your-second-model-here",
    "your-third-model-here"
  ],
  "default_timeout": 900,
  "max_tokens": 8192
}
```

**Example** (using Ollama cloud models):
```json
{
  "council_models": [
    "ollama/kimi-k2.6:cloud",
    "ollama/deepseek-v4-pro:cloud",
    "ollama/gemma4:31b-cloud"
  ]
}
```

Choose models with different strengths — one strategic, one analytical, one creative. The more diverse, the better the council output.

---

## Critical Rules

### Timeout Rules
- **Subagents: max 600s (10 min)** — they only do focused cognitive work, not I/O
- **Main agent has no timeout** — it handles all long-running I/O directly
- Never set `runTimeoutSeconds` above 600 for subagents — if they need more, the task is too broad

### Subagent Constraints
- Subagents do NOT clone repos, push code, or create PRs
- Subagents do NOT make GitHub API calls
- Subagents do NOT browse the web
- Subagents receive file contents inline and return code changes
- Keep subagent task descriptions under 1500 words
- Use `lightContext: true` on all subagent spawns

### Quality Rules
- **Never force a contribution** — if no good fit, report "no suitable issues found"
- Every PR must reference the issue it fixes
- Every PR must disclose AI assistance
- No emojis in PR titles, descriptions, or comments
- Professional, concise tone in all PR communications

### Workflow Rules
- **API-first** for simple fixes — no clone needed for 1-3 file changes
- **Clone only** when you need to run tests or understand complex structure
- **Batch tool calls** — read all files first, then send to subagent in one task
- **Verify before push** — run linters/tests locally after applying changes

---

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Subagent times out | Task too broad (clone + edit + push) | Use Architect-Builder pattern: main agent does I/O |
| Shallow code changes | Vague subagent prompt | Paste full file contents + specific instructions |
| Lint failures after subagent edit | Subagent didn't know lint rules | Include lint config in the prompt or run lint before subagent |
| PR rejected by maintainer | Low-quality contribution | Follow CONTRIBUTING.md, write meaningful fixes only |
| Context overflow in subagent | Too much data pasted inline | Summarize to <1500 words, paste only relevant files |

## Companion Skills

- **subagent-orchestration** — Required. Provides spawn patterns, timeout config, sandbox constraints.
- **council-of-llms** — Optional. For Level 3 complex decisions before implementing.

## Storage

```
contrib-scout/
├── repos/              # Cloned repositories (cleaned up after each run)
├── logs/               # Activity + audit trail (JSONL)
├── config.json         # Difficulty level + settings
└── nightly-report.json # Daily summary
```