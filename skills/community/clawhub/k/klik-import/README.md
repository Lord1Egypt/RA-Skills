<p align="center">
  <img src=".github/assets/banner.png" alt="klik-import — Migrate your AI agent's memory to Klik" width="100%" />
</p>

<p align="center">
  Collect and securely import your AI agent's memory and scheduled tasks into Klik — in one command.
</p>

<p align="center">
  <a href="https://agentskills.io/specification"><img src="https://img.shields.io/badge/Agent_Skills-v1.0-4c1?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTUtMTAtNXoiLz48cGF0aCBkPSJNMiAxN2wxMCA1IDEwLTUiLz48cGF0aCBkPSJNMiAxMmwxMCA1IDEwLTUiLz48L3N2Zz4=" alt="Agent Skills v1.0" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/Node.js-%3E%3D18-339933?style=flat-square&logo=node.js&logoColor=white" alt="Node >= 18" />
  <img src="https://img.shields.io/badge/TypeScript-5.4-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Zero_Dependencies-production-2d2d2d?style=flat-square" alt="Zero Dependencies" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-compatible-D97706?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIiIHI9IjEwIi8+PHBhdGggZD0iTTkgOWMuOC0xLjUgMi0yIDMtMnMyLjIuNSAzIDIiLz48cGF0aCBkPSJNOSAxNWMuOCAxLjUgMiAyIDMgMnMyLjItLjUgMy0yIi8+PC9zdmc+" alt="Claude Code" />
  <img src="https://img.shields.io/badge/OpenClaw-compatible-EF4444?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwYXRoIGQ9Ik0yMCA4bC00IDQgNCA0Ii8+PHBhdGggZD0iTTQgOGw0IDQtNCA0Ii8+PHBhdGggZD0iTTEyIDR2MTYiLz48L3N2Zz4=" alt="OpenClaw" />
  <img src="https://img.shields.io/badge/Hermes_Agent-compatible-8B5CF6?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwYXRoIGQ9Ik0xMiAyYTEwIDEwIDAgMSAwIDAgMjAgMTAgMTAgMCAwIDAgMC0yMHoiLz48cGF0aCBkPSJNMTIgNnY2bDQgMiIvPjwvc3ZnPg==" alt="Hermes Agent" />
  <img src="https://img.shields.io/badge/Gemini_CLI-compatible-4285F4?style=flat-square&logo=google&logoColor=white" alt="Gemini CLI" />
  <img src="https://img.shields.io/badge/Codex_CLI-compatible-10A37F?style=flat-square&logo=openai&logoColor=white" alt="Codex CLI" />
</p>

---

## What It Does

**klik-import** lets your AI coding agent collect its memory files and scheduled tasks, then securely import them into [Klik](https://pre.hiklik.ai/?utm_source=github&utm_medium=readme&utm_campaign=kickstarter_prelaunch&utm_content=klik_import_skill_workflow).

Your agent gathers its own memory, and the tool handles cleanup, secret redaction, and secure upload. No API keys stored, no credentials in config files.

**What gets collected:**

- Agent memory files (preferences, project notes, feedback, user context)
- Scheduled tasks and recurring prompts

**What happens to your data:**

- Secrets (API keys, tokens, private keys) are automatically redacted before upload
- Email redaction is optional — you choose
- Data is uploaded securely using a one-time code from the Klik App
- Once imported, your data is available in the Klik App

## Quick Start

### GitHub CLI

```bash
git clone https://github.com/minervacap2022/klik-import-skill
node klik-import-skill/dist/klik-import.mjs doctor
```

### Claude Code

```bash
# Install as a personal skill
git clone https://github.com/minervacap2022/klik-import-skill \
  ~/.claude/skills/klik-import

# Then just tell Claude:
# "import my memory to klik"
```

### OpenClaw

```bash
# Install via ClawHub
claw skill install klik-import

# Or manually
git clone https://github.com/minervacap2022/klik-import-skill \
  ~/.openclaw/skills/klik-import
```

### Hermes Agent

```bash
# Install into Hermes skills directory
git clone https://github.com/minervacap2022/klik-import-skill \
  ~/.hermes/skills/productivity/klik-import
```

### Any Agent Skills-compatible tool

The skill follows the [Agent Skills v1.0 spec](https://agentskills.io/specification). Drop the directory into your agent's skills folder and it works.

## How to Use

1. Open **Klik App > Settings > Import from Agent > Generate Code** to get your 6-digit code
2. Copy the prompt below, replace `XXXXXX` with your code, and paste it to your agent:

```
Install the klik-import skill from https://github.com/minervacap2022/klik-import-skill
and use it to import my memory and scheduled tasks to Klik. My import code is: XXXXXX
```

That's it — your agent will install the skill, collect your data, and handle the import.

## Troubleshooting

| Issue | What to do |
|-------|------------|
| Code not accepted | Generate a new code in Klik App (codes expire after 30 minutes) |
| Too many failed attempts | Generate a new code |
| Import too large | Split into smaller batches |

## Development

```bash
npm install
npm test
npm run lint
npm run build
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) — use it, fork it, ship it.

## Follow Klik

Klik is currently a pre-launch proactive AI project planned for Kickstarter. This skill documents one code-based agent-memory import workflow; it does not establish general availability or universal recorder compatibility. To learn more or join the pre-launch list, visit [pre.hiklik.ai](https://pre.hiklik.ai/?utm_source=github&utm_medium=readme&utm_campaign=kickstarter_prelaunch&utm_content=klik_import_skill).
