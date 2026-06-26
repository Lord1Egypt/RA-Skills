---
name: oss-contribution-system
description: End-to-end open-source GitHub contribution automation system. Discover high-value issues,
  implement fixes, open quality PRs, monitor CI/review status, and learn from each
  contribution. Uses gh CLI for GitHub API access, git for version control, and
  stores workspace-local data in ./oss-pilot-data/ for profiles and PR context.
  Triggers on "oss discover", "oss auto", "oss pr", "oss check",
  "find issues", "what should I work on", "next PR", "auto PR", "review PR",
  "check PRs", "morning check".
user_invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - gh
        - git
---

# OSS Contribution System

A complete system for contributing to open-source repos. Four skills work together in a learning loop --each contribution makes the next one better.

## Quick Start

1. **First time?** Just say: `oss discover <repo-url-or-name>`
   - The system will create a profile, check repo openness, and find issues for you.

2. **Found an issue?** Say: `oss auto <repo> #12345`
   - End-to-end: implement -> open PR -> respond to bots -> ping maintainer.

3. **Already have a PR?** Say: `oss check <repo>`
   - Checks CI, bot comments, stale status, and takes action.

4. **Want a quality review?** Say: `oss pr review <repo> #12345`
   - Root cause analysis, diff check, description quality, bot response strategy.

## How the System Works

```
discover --> auto --> pr --> check --> retrospective
   ^                   ^       |              |
   |                   +-------+              |
   |              (human review loop)         |
   |                                          v
   |                              profile grows (lessons, patterns)
   |                                          |
   +---- checks archived history -------------+
         (avoid past mistakes)
```

**Profile** (`./oss-pilot-data/profiles/<repo>.md`): Stores repo-specific knowledge --build commands, maintainer styles, bot behavior, lessons learned. Grows with each contribution. See `_template.md` for the schema.

**Context files** (`./oss-pilot-data/context/pr-<repo>-<N>.md`): Track each PR's approach, bot decisions, and outcome. Archived after merge/close for future reference.

## The Four Skills

### oss-discover (find.md)
Find high-value issues with the highest merge probability.
- Checks repo openness (external contributor merge rate)
- Checks issue velocity (how fast issues get claimed)
- Scans 8 sources: high-signal labels -> bugs -> CI failures -> reclaimable PRs -> merged PR gaps -> scoped modules -> area merge rate -> codebase cleanup
- Verifies bugs still exist, checks comments for signals, evaluates fix feasibility

**Read: `discover.md`**

### oss-auto (auto.md)
One command from issue to opened PR. Orchestrates discover + pr.
- Cold start: auto-creates profile for new repos
- Feasibility check -> implement -> open PR -> respond to bots -> mark ready -> ping maintainer
- Auto-detects build tooling (Node/Python/Go/Rust/Make)
- Reads CONTRIBUTING.md and CLAUDE.md for repo conventions

**Read: `auto.md`**

### oss-pr (pr.md)
Quality gate for PRs. Validates before requesting review.
- Root cause analysis (right layer? blast radius? semantic contracts?)
- Common mistake patterns and anti-patterns
- PR description with "What did NOT change" and "What I Did NOT Verify"
- Bot response strategy (accept/decline/repeat handling)
- CI failure triage template

**Read: `pr.md`**

### oss-check (check.md)
Morning check-in for all pending PRs.
- CI/bot/stale status monitoring
- Retrospective on merged/closed PRs (writes Outcome + routes lessons)
- Maintenance: prunes stale lessons, archives old context files
- Handles fork PR CI skipping (normal for external contributors)

**Read: `check.md`**

## Prerequisites

- `gh` CLI installed and authenticated (`gh auth status`)
- GitHub account with a fork of the target repo
- Optional: local clone for codebase scanning (Source 8)

## Security Model

This skill instructs the agent to run build, lint, and test commands (e.g., `pnpm install`, `make`, `cargo test`) from the target repository. This is inherent to contribution automation --you cannot validate a fix without running the repo's toolchain.

**Threat surface**: If the target repo contains malicious build scripts (e.g., postinstall hooks), those commands execute on your machine. This is the same risk as manually cloning a repo and running `npm install`.

**How risk is managed**:
- **User trust boundary**: You choose which repo to target. The skill never picks repos autonomously.
- **Runtime gating**: OpenClaw's exec approval system prompts before executing shell commands. The skill issues instructions; the runtime decides whether to run them.
- **Scope checkpoint**: The skill stops and asks before committing to changes >5 files or >200 lines.

**Recommended hardening**:
- Run inside a container (`openclaw --container <name>`) or VM when targeting unfamiliar repos.
- Review the repo's `package.json` scripts / `Makefile` targets before first run.
- Use a dedicated GitHub account for automation if you prefer isolation.

## Data Directories

The system creates and manages these directories:
- `./oss-pilot-data/profiles/` --one profile per repo
- `./oss-pilot-data/context/` --active PR context files
- `./oss-pilot-data/context/_archived/` --completed PR context files (for learning)
