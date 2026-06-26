# OpenClaw Configurator

> A smart assistant skill that helps users configure their personal AI assistant (OpenClaw) through multi-round dialogue, generating a complete Markdown configuration package.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/license/mit-0)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](#changelog)

---

## Overview

OpenClaw Configurator is a skill built by [qomob](https://clawhub.ai/user/qomob) for the [OpenClaw](https://openclaw.ai) platform. It guides users through a structured dialogue to capture their requirements, then generates 8 configuration files that define the assistant's persona, memory, tools, security, and onboarding ritual.

**Key capabilities:**

- Multi-round requirement clarification for vague inputs
- Generates 8 specification-compliant `.md` files
- Security guidance for public channel deployment (Discord / WhatsApp / Telegram)
- PII protection and multi-channel isolation recommendations
- Structured output validated against JSON Schema

## Generated Files

| File | Purpose | Loading Timing |
|------|---------|---------------|
| `BOOTSTRAP.md` | One-time onboarding ritual | First run only, deleted after |
| `AGENTS.md` | Operation guide & memory rules | Every session start |
| `SOUL.md` | Persona & personality definition | Every session |
| `IDENTITY.md` | Name, emoji, signature | Created during onboarding |
| `USER.md` | User profile | Every session |
| `TOOLS.md` | Tool conventions & skill notes | Reference as needed |
| `HEARTBEAT.md` | Periodic health check | Every 30 minutes |
| `MEMORY.md` | Long-term persistent memory | Main private session only |

All files are placed in `~/.openclaw/workspace/`.

## Usage

### Quick Start

Invoke the skill and describe what you want:

```
我想配置一个专门帮我写代码的助手。他应该很冷静，不废话，用 Emoji 🤖。
```

If your requirements are vague (e.g., "给我写个配置"), the skill will ask clarifying questions about:

- **Personality** — formal, casual, sarcastic, gentle, etc.
- **Use case** — coding, scheduling, emotional support, email management, etc.
- **Security** — how to handle unknown senders on messaging platforms

### Multi-Channel Deployment

For public channels (Discord, WhatsApp, Telegram), the skill provides security configuration guidance:

| Setting | Description |
|---------|-------------|
| `dmPolicy="pairing"` | Unknown senders must enter a pairing code |
| `allowFrom` | Restrict access to specific contact IDs |
| `openclaw onboard --install-daemon` | Keep the assistant running as a background daemon |

## Project Structure

```
openclaw-configurator/
├── SKILL.md                # Skill prompt (English, authoritative source / SSOT)
├── SKILL_zh.md             # Skill prompt (Chinese translation, derived from SKILL.md)
├── _meta.json              # Publish metadata
├── skill-card.md           # Skill card for marketplace listing
├── schemas/
│   └── output-schema.json  # JSON Schema for validating generated config files
├── evals/
│   └── evals.json          # Core eval cases (6 basic)
└── benchmark/
    ├── basic-cases.json       # 6 basic functional tests
    ├── production-cases.json  # 6 production-grade scenarios
    ├── edge-cases.json        # 7 boundary tests
    └── adversarial-cases.json # 5 adversarial/security tests
```

## Testing

This skill includes **24 test cases** across 4 benchmark suites:

| Suite | Cases | Coverage |
|-------|:-----:|----------|
| `basic` | 6 | Full 8-file generation, multi-round guidance, tone matching |
| `production` | 6 | Multi-channel deployment, security policies, team scenarios, voice integration |
| `edge` | 7 | Empty input, partial requirements, contradictions, special characters, mixed languages |
| `adversarial` | 5 | PII leakage attempts, security bypass, prompt injection, harmful config requests |

Each case uses structured assertions (`must_contain_all_files`, `must_contain_keywords`, `must_ask_clarification`, `must_warn_about_pii`, etc.) for automated validation.

## Output Schema

Generated configuration files are validated against [schemas/output-schema.json](schemas/output-schema.json), which defines:

- Required sections for each of the 8 files
- Field types and constraints
- Security keywords required for public channel configurations
- PII plaintext storage prohibition

## Security

### PII Protection

The skill refuses to store plaintext sensitive data (passwords, bank cards, ID numbers, API keys) in configuration files. If a user provides sensitive data, it warns them and suggests environment variables or a secrets manager.

### Known Risks

**Risk:** Generated configuration may not match the user's intended identity, safety boundaries, or target file location.

**Mitigation:** Treat generated files as drafts. Review personality preferences, safety boundaries, and file paths before writing to the workspace.

## References

- [OpenClaw Official Site](https://openclaw.ai)
- [OpenClaw Documentation](https://openclaw.ai/docs)
- [OpenClaw Security Guide](https://openclaw.ai/docs/security)
- [OpenClaw CLI Reference](https://openclaw.ai/docs/cli)

## License

MIT-0 — See [skill-card.md](skill-card.md) for full terms.

## Changelog

### v1.1.0

- Added OpenClaw specification reference tables with authoritative doc links
- Expanded security recommendations: PII protection, multi-channel isolation, content moderation
- Added structured output schema (`schemas/output-schema.json`) for all 8 config files
- Expanded test coverage from 2 to 24 cases across 4 benchmark suites
- Converted all eval assertions to executable format
- Added adversarial tests: PII leakage, prompt injection, security bypass
- Added multi-round dialogue state checklist
- Added SSOT declaration between `SKILL.md` and `SKILL_zh.md`
- Completed YAML front matter (`version`, `author`, `license`)

### v1.0.2

- Initial release
