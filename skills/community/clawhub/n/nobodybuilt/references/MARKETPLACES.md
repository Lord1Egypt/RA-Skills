# Skill Marketplace Publishing Guide

Use this reference when helping the user publish their skill in Phase 5.

## Quick-Publish Platforms (No approval needed)

### skills.sh (by Vercel)
- **How:** Skills auto-appear when users install them via `npx skills add <owner>/<repo>`
- **Requirements:** Public GitHub repo with valid `SKILL.md` (YAML frontmatter)
- **To kickstart:** Tell the user to share `npx skills add <owner>/<repo>` in their README and posts
- **Leaderboard:** Installs drive ranking on skills.sh

### ClawHub
- **How:** CLI publish
  ```bash
  npm i -g clawhub
  # Authenticate with GitHub (account must be >= 1 week old)
  clawhub publish ./path-to-skill --version 1.0.0
  ```
- **Requirements:** Node.js >= 20, `SKILL.md`, semver versioning
- **Note:** Published under MIT-0 license. Malware-scanned via VirusTotal.

### SkillsMP (skillsmp.com)
- **How:** Automatic — scrapes GitHub for repos with `SKILL.md` files
- **Requirements:** Public repo, `SKILL.md`, minimum 2 GitHub stars
- **Tip:** Get 2 stars first (ask friends, post on social), then SkillsMP picks it up automatically

## Web Form Submissions

### Skills Directory (skillsdirectory.com)
- **Submit URL:** https://www.skillsdirectory.com/submit
- **How:** Sign in with GitHub, submit repo URL
- **Requirements:** Valid `SKILL.md` with YAML frontmatter, description under 200 chars
- **Security:** Scanned with 50+ detection rules
- **Approval:** Manual review

### SkillsLLM (skillsllm.com)
- **Submit URL:** https://skillsllm.com/submit
- **How:** Web form, sign in and submit repo URL
- **Approval:** Unknown timeline

### Smithery (smithery.ai)
- **Submit URL:** https://smithery.ai/new
- **How:** Web form (sign in with GitHub) or CLI: `smithery deploy .`
- **CLI:** `npm i -g @anthropic-ai/smithery && smithery auth login && smithery deploy .`
- **Approval:** Instant for MCP servers; skills indexed from GitHub

## Curated Lists (GitHub PRs/Issues — need traction first)

### awesome-claude-code (32K+ stars)
- **Submit:** https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
- **Method:** GitHub Issue form (NOT a PR — PRs forbidden)
- **Requirements:** Human-submitted, good README, clear purpose, no telemetry
- **Note:** OpenClaw submissions temporarily banned

### awesome-claude-skills (9.8K+ stars)
- **Submit:** Fork repo, add entry, open PR
- **Format:** `- **[Name](link)** - Description`
- **Requirements:** >= 10 GitHub stars, no AI-generated PRs, no SaaS wrappers, human-submitted
- **Approval:** Manual; below 10 stars = auto-closed

### awesome-agent-skills (13K+ stars)
- **Submit:** Fork repo, add entry, open PR
- **Format:** `- **[author/skill-name](link)** - Description (10 words max)`
- **Requirements:** Real community usage (not brand new), one skill per PR
- **Approval:** Manual review

### LobeHub
- **Submit:** PR to https://github.com/lobehub/lobe-chat-plugins
- **How:** Copy `plugin-template.json`, fill in details, submit PR
- **Approval:** Manual review

## Publishing Order (Recommended)

1. **Immediately (day 1):** skills.sh (auto), ClawHub (CLI), Skills Directory (web form), SkillsLLM (web form), Smithery (web/CLI)
2. **After 2+ stars:** SkillsMP (auto-indexed)
3. **After 10+ stars:** awesome-claude-skills PR, awesome-agent-skills PR
4. **After good README + traction:** awesome-claude-code issue
