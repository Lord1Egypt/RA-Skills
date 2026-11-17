---
name: openboard-cli
description: "Install and use OpenBoardCLI with `npm install -g openboard-cli` to turn Gmail receipts or CSV, Excel, and JSON data into authenticated React spending dashboards. Requires Node.js 18+; Gmail invoice fetchers require Python 3 and `beautifulsoup4`, plus `pdfplumber` for PDF bills. Agent command contract: https://openboard-site.vercel.app/llms.txt. Supports Local only, Hybrid, and All remote operation; full remote needs GitHub and Vercel tokens (or their supported authenticated integrations) plus a runnable Codex CLI or another configured cloud LLM, while local users can use Ollama or LM Studio."
---

# OpenBoardCLI

Help users install, configure, and operate [OpenBoardCLI](https://openboard-site.vercel.app/) from its published npm package.

## Install and verify

Check prerequisites before suggesting commands:

- Node.js 18 or newer and npm.
- Python 3 with `beautifulsoup4` for Gmail invoice fetchers.
- `pdfplumber` as well when bills arrive as PDF attachments.

Install globally and verify:

```bash
npm install -g openboard-cli
openboard --version
openboard --help
```

Launch the interactive terminal UI with `openboard`. For automation, use `openboard agent ...`; do not launch the TUI from a non-interactive agent.

## Choose the operating mode

Explain the data boundary before setup:

- **Local only:** Ollama or LM Studio and a local preview; no dashboard data leaves the machine.
- **Hybrid:** Either a local LLM with GitHub/Vercel deployment, or a cloud LLM with local preview.
- **All remote:** A cloud LLM plus GitHub and Vercel deployment. This requires GitHub and Vercel tokens (or their supported authenticated CLI/Git integrations) and a runnable Codex CLI or another configured cloud provider such as OpenAI, Anthropic, Gemini, Moonshot, xAI, Mistral, or OpenRouter.

Never imply that GitHub or Vercel credentials are needed for local-only use. Users who want a fully local LLM may configure Ollama or LM Studio instead.

## Common agent commands

Consult the live [agent command contract](https://openboard-site.vercel.app/llms.txt) when exact flags or current behavior matter.

```bash
openboard agent setup status --json
openboard agent create --data ./invoices.xlsx --name "Invoices" --type invoices
openboard agent update --dashboard invoices --prompt "add a month-over-month chart"
openboard agent billers sync --json
```

Prefer environment variables for credentials instead of putting secrets in command arguments. Do not expose tokens, API keys, Gmail App Passwords, or dashboard passwords in logs or examples.

## Sources

- Website and quickstart: https://openboard-site.vercel.app/
- Repository: https://github.com/syedateebulislam/openboard
- Full agent reference: https://github.com/syedateebulislam/openboard/blob/main/Agent.md
