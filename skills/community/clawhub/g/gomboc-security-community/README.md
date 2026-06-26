# Gomboc Code Remediation Skill

**Deterministic code remediation powered by ORL (Open Remediation Language).**

Instead of generating alerts, Gomboc delivers merge-ready pull requests that clear your code issues backlogs and keep your pipelines moving.

[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-green)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)]()
[![Version: 0.2.0](https://img.shields.io/badge/version-0.2.0-blue)]()
[![Powered by ORL](https://img.shields.io/badge/powered%20by-ORL-blue)]()

## What This Skill Does

- 🔍 **Scan** any codebase for issues — infrastructure, applications, configs
- 🔧 **Generate** deterministic fixes (same input = same output, always)
- 🤖 **Automate** continuous code remediation via agents
- 📊 **Report** findings in multiple formats (JSON, Markdown, SARIF)
- 🧠 **Perfect for agents** — trustworthy remediation for agentic coding loops
- 🔐 **Syntax-aware** — Tree-sitter based matching (no brittle regex)

## Quick Start

### 1. Sign Up (Free, No Credit Card)

https://app.gomboc.ai — choose your onboarding path:
- **VS Code/Cursor** — IDE plugin for real-time scanning
- **GitHub** — GitHub App for automatic PRs
- **CLI/API** — Direct API access

### 2. Generate Token

Settings → Personal Access Token → Generate

```bash
export GOMBOC_PAT="gpt_your_token"
```

⚠️ **Security Note:** 
- Token grants **read-only API access** (least privilege)
- Safe for CI/CD workflows and GitHub Actions
- **Never commit to code or `.env` files**
- Use GitHub Secrets (Actions) or your CI provider's secret management
- Verify token scope before production use: https://app.gomboc.ai/settings/tokens

### 3. Scan Code

```bash
python scripts/cli-wrapper.py scan --path ./src --format markdown
```

### 4. Review & Apply Fixes

```bash
python scripts/cli-wrapper.py fix --path ./src
python scripts/cli-wrapper.py remediate --path ./src --commit
```

## Key Features

✅ Deterministic AI (no hallucinations)
✅ 94%+ accuracy (merge-ready fixes)
✅ Free forever (Community Edition)
✅ Production-ready code
✅ Secure by design

## Documentation

- **[SKILL.md](SKILL.md)** — Full documentation
- **[references/setup.md](references/setup.md)** — Setup instructions
- **[references/mcp-integration.md](references/mcp-integration.md)** — Agent integration
- **[references/github-action.md](references/github-action.md)** — CI/CD setup
- **[SECURITY.md](SECURITY.md)** — Security audit & practices
- **[CHANGELOG.md](CHANGELOG.md)** — Version history

## Support

- **GitHub:** https://github.com/Gomboc-AI/gomboc-community-agent
- **Gomboc Docs:** https://docs.gomboc.ai
- **Issues:** https://github.com/Gomboc-AI/gomboc-ai-feedback/discussions

## License

MIT License — See LICENSE file
