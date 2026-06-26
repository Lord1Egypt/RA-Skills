---
name: publishing-guide
description: Universal skill publishing checklist and rules — ClawHub, GitHub, Claude Code, Hermes, OpenClaw. Pre-publish vetting, anti-duplicate, naming conventions, promotion strategy.
version: 2.0.0
author: nerua1
compatible-with: claude-code, openclaw, hermes-agent, goose
tags: [publishing, github, clawhub, skills, checklist, guidelines]
---

# Publishing Guide

Universal rules for publishing AI skills across all platforms. Use this before every release.

---

## Pre-Publish Checklist

- [ ] **Anti-duplicate check** — search ClawHub, GitHub, and local directories
- [ ] **No hardcoded credentials** — scan for API keys, tokens, passwords
- [ ] **No local paths** — genericize `~/`, `/Users/`, `/home/` to `<workspace>`, `<config>`, etc.
- [ ] **English language** — all descriptions, usage examples, and docs
- [ ] **YAML frontmatter** — name, description, version, author
- [ ] **Usage examples** — at least 2 concrete examples
- [ ] **PayPal + GitHub links** — at end of every SKILL.md
- [ ] **Semver versioning** — start at 1.0.0, bump appropriately
- [ ] **Cross-platform compatible** — mark which agents it works with

---

## Naming Conventions

| Suffix | When to use | Example |
|--------|-------------|---------|
| `-loop` | Iterative feedback loop | `ralph-wiggum-loop` |
| `-bridge` | Cross-agent/system communication | `openclaw-bridge`, `acp-bridge` |
| `-stack` | Architecture / tech stack | `shared-memory-stack` |
| `-guide` | Documentation / setup / onboarding | `openclaw-setup-guide` |
| `-guard` | Security / audit / verification | `skill-vetter` |
| `-agent` | Autonomous agent | `proactive-agent` |
| `-crawler` | Scraping / data fetching | `news-crawler` |
| `-monitor` | Monitoring / observability | `lm-studio-monitor` |
| `-orchestrator` | Model orchestration | `lm-studio-orchestrator` |

Agent-specific prefixes: `openclaw-`, `claude-`, `hermes-`. Universal skills: no prefix.

---

## Anti-Duplicate Check

```bash
# ClawHub
npx clawhub search <skill-name>

# GitHub
gh repo list nerua1 --limit 100 | grep -i "<skill-name>"

# Local OpenClaw
ls <workspace>/skills/ | grep -i "<skill-name>"

# Local Claude Code  
ls <agent-home>/skills/vault/ | grep -i "<skill-name>"

# Local Hermes
ls <agent-home>/skills/ | grep -i "<skill-name>"
```

If something similar exists → merge, don't duplicate.

---

## SKILL.md Template

```markdown
---
name: skill-name
description: One-line English description
version: 1.0.0
author: nerua1
compatible-with: claude-code, openclaw, hermes-agent
---

# Skill Title

Brief description (2-3 sentences).

## Usage

Example usage with actual commands.

## Examples

Real-world scenarios where this helped.

---

If this saved you time: [☕ PayPal.me/nerudek](https://www.paypal.me/nerudek)
GitHub: [github.com/nerua1](https://github.com/nerua1)
```

---

## Where to Publish

| Platform | How | Reach |
|----------|-----|-------|
| **ClawHub** | `npx clawhub publish . --slug <slug>` | OpenClaw users |
| **GitHub** | Public repo, README.md | Developers, search engines |
| **Dev.to** | Article: "How I built X" | Developer community |
| **Reddit** | r/LocalLLaMA, r/selfhosted, r/OpenAI | Enthusiasts |
| **Twitter/X** | Thread with screenshots | Broader reach |
| **Claude Code** | PR to claude-plugins-official | Claude users |

**Minimum for every skill:** ClawHub + GitHub + Dev.to article.

---

## Post-Publish Verification

After publishing, verify:
- [ ] Skill appears in ClawHub search
- [ ] GitHub README has PayPal + description
- [ ] `npx clawhub install <slug>` works
- [ ] Skill loads correctly in a new session

---

If this saved you time: [☕ PayPal.me/nerudek](https://www.paypal.me/nerudek)
GitHub: [github.com/nerua1](https://github.com/nerua1)
