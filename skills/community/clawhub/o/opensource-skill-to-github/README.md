# opensource-skill-to-github

> End-to-end open-source a local AI-agent skill to **GitHub** (primary) and optionally **clawhub.com** — with internal-info stripping, token hygiene, and a decision checkpoint at every risky step.

This skill was itself open-sourced **using itself** (dogfooding). It works across
OpenClaw / Claude Code / Cursor and any agent skill ecosystem.

## Why

Turning an internal/company skill into a clean public release involves a lot of
easy-to-miss steps: slug collision checks, stripping internal hosts/paths/emails,
frontmatter normalization, LICENSE decisions, independent git repo setup, token
hygiene, and multi-hub publishing. This skill scripts the mechanical parts and
**stops for your decision** at every sensitive one.

## Features

- **10-step workflow**: slug pre-check → fork → strip internal info → frontmatter
  normalize → LICENSE → README/.gitignore → git init → UGLIC self-audit → GitHub push → optional clawhub/skillhub publish
- **Fork, never in-place**: the original skill is never modified; the open-source copy
  lives in `opensourceskills/<slug>/` with its own commit / version / sign history
- **Configurable internal-keyword scanning**: default table holds only *generic*
  secrets (sso_token / id_rsa / private-key markers); your company-specific words are
  configured once via `setup_profile.sh` and reused
- **Token hygiene built in**: tokens only via env vars, never written to git/remote/memory;
  GitHub push uses a Basic-Auth header (token never enters the remote URL); 4-tier
  token source (GITHUB_TOKEN → OSG_GITHUB_TOKEN → OSG_GITHUB_TOKEN_CMD → `gh auth token`)
- **Push verification**: compares local vs. remote sha (GitHub API, ls-remote fallback)
  so a "success" that didn't actually reach the remote is caught
- **Cross-platform**: bash-first, with macOS bash 3.2 fallbacks (no `mapfile` dependency)
- **One-shot orchestration**: `run_all.sh` chains the first 6 steps
- **Full methodology bundled**: `references/opensource_playbook.md` (16-section playbook)

## Quick Start

```bash
# 1. Configure your open-source identity once (persisted to ~/.config/, survives reinstall)
bash scripts/setup_profile.sh
#    Prompts: author name, GitHub handle, email, and (optional) company internal keywords

# 2. Open-source a skill (first 6 steps in one go)
bash scripts/run_all.sh <source-skill-name-or-abs-path> [<new-slug>]

# 3. Then push (needs a GitHub repo + token)
bash scripts/github_push.sh <fork-path> <handle>/<repo-name>

# 4. Optional: publish to clawhub
bash scripts/clawhub_publish.sh <fork-path>
```

## Scripts

| Script | Purpose |
|---|---|
| `setup_profile.sh` | One-time identity + internal-keyword config (persisted) |
| `precheck.sh` | slug collision pre-check on clawhub |
| `fork.sh` | Copy skill to `opensourceskills/`, strip artifacts, exclude node_modules |
| `strip_scan.sh` | Scan for internal info (generic + configured keywords) |
| `check_frontmatter.py` | Validate SKILL.md frontmatter (4 cross-agent rules) |
| `gen_license.sh` | Generate MIT / Apache-2.0 / GPL-3.0 LICENSE |
| `scaffold.sh` | Generate README.md + .gitignore |
| `git_init.sh` | Independent git repo (never pollutes a parent repo) |
| `github_push.sh` | Push with Basic-Auth header + retry + sha verification |
| `clawhub_publish.sh` | Publish to clawhub (login-aware, auto version) |
| `skillhub_cn_publish.sh` | Publish to a skillhub.cn-style hub (multipart) |
| `run_all.sh` | Chain the first 6 steps |

## Usage

Full step-by-step guidance is in [SKILL.md](./SKILL.md). The complete vendor-neutral
methodology (decision framework, 11-rule strip checklist, token hygiene, UGLIC review,
anti-patterns) is in [references/opensource_playbook.md](./references/opensource_playbook.md).

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install opensource-skill-to-github` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `.cursor/skills/` |

## Part of build-better-skills

This skill is the **Opensource** stage of the
[build-better-skills](https://github.com/Songhonglei/build-better-skills)
suite — open-source skills that help you build better skills, end-to-end
(Creation → Install → Audit → Release → Documentation → Testing → Sediment →
**Opensource**).

See the [suite README](https://github.com/Songhonglei/build-better-skills#stages)
for the full stage roadmap and sibling skills.

## License

MIT (see [LICENSE](./LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
