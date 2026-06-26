# Gomboc Code Remediation Skill

**Deterministic code remediation for any codebase — powered by Gomboc.ai Community Edition.**

[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-green)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)]()
[![Version: 0.2.0](https://img.shields.io/badge/version-0.2.0-blue)]()

## What This Skill Does

- 🔍 **Scan** any codebase for issues — infrastructure, application, config
- 🔧 **Generate** merge-ready fixes with 94%+ acceptance rate
- 🤖 **Automate** continuous code remediation
- 📊 **Report** findings in multiple formats
- 🧠 **Perfect for agents** — deterministic remediation paired with agentic coding

## Quick Start

### 1. Get a Token

```bash
# Sign up at https://app.gomboc.ai (free, no credit card)
# Generate Personal Access Token in Settings
export GOMBOC_PAT="gpt_your_token"
```

### 2. Scan Code

```bash
python scripts/cli-wrapper.py scan --path ./terraform
```

### 3. Generate Fixes

```bash
python scripts/cli-wrapper.py fix --path ./terraform
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
