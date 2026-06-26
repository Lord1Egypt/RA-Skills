# Junie doc notes

This file distills the Junie documentation into the pieces most useful when an agent is asked to install or configure Junie.

## Install

Documented install methods:
- macOS/Linux: `curl -fsSL https://junie.jetbrains.com/install.sh | bash`
- Windows PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -Command "iex (irm 'https://junie.jetbrains.com/install.ps1')"`
- macOS Homebrew: `brew tap jetbrains/junie && brew update && brew install junie`
- npm: `npm install -g @jetbrains/junie`

The bundled helpers in this skill wrap those documented install paths:
- `scripts/install_junie.sh` for POSIX shells
- `scripts/install_junie.ps1` for PowerShell

The official shell installer:
- detects OS and arch
- installs the shim to `~/.local/bin/junie`
- stores versions under `~/.local/share/junie/versions/`
- maintains `~/.local/share/junie/current`
- attempts to add `~/.local/bin` to shell startup files
- supports `JUNIE_VERSION=<version>` for a pinned install

## Quick verification

```bash
export PATH="$HOME/.local/bin:$PATH"
junie --version
junie --help
```

## Authentication

### Junie token
- CLI flag: `--auth`
- env var: `JUNIE_API_KEY`

Example:

```bash
junie --auth="$JUNIE_API_KEY" "review this repository"
```

### BYOK provider keys
Junie documents provider-specific flags and env vars for:
- Anthropic
- OpenAI
- Google
- xAI / Grok
- OpenRouter

Examples:

```bash
export JUNIE_ANTHROPIC_API_KEY='...'
export JUNIE_OPENAI_API_KEY='...'
```

Interactive local auth can also happen from:
- the welcome screen
- `/account`

## Headless mode

Headless mode is the preferred automation path. Junie documents:

```bash
junie --auth="$JUNIE_API_KEY" "Review and fix any code quality issues in the latest commit"
```

This is the main reason installation/configuration usually does not require terminal-UI driving.

## Config files

Default config locations:
- user: `~/.junie/config.json`
- project: `<project>/.junie/config.json`

Junie-native project layout typically centers on a `.junie/` directory. A sensible bootstrap shape is:

```text
.junie/
├── AGENTS.md
├── config.json
├── skills/
├── commands/
├── agents/
├── models/
├── mcp/
└── rules/
```

Precedence documented by Junie:
1. CLI flags
2. `~/.junie/settings.json`
3. project `.junie/config.json`
4. user `~/.junie/config.json`

Common config fields documented by Junie:
- `model`
- `provider`
- `brave`
- `flags`
- `mcp-locations`
- `mcp-default-locations`
- `skill-locations`
- `skill-default-locations`
- `command-locations`
- `command-default-locations`
- `agent-locations`
- `agent-default-location`
- `model-locations`
- `model-default-locations`
- `auto-update`
- `guidelines-location`
- `time-limit`
- `byok`
- `proxies`

Relative paths in config files are resolved relative to the config file's directory.

Guidelines discovery order documented by Junie:
1. custom filename from `--guidelines-filename` / `JUNIE_GUIDELINES_FILENAME` (inside project `.junie/`)
2. `.junie/AGENTS.md`
3. root `AGENTS.md`
4. `.junie/rules/*.md`
5. legacy `.junie/guidelines.md`

## Skills and guidelines

Junie skills live under:
- project: `<project>/.junie/skills/`
- user: `~/.junie/skills/`

Related Junie-native discovery roots are commonly:
- `<project>/.junie/commands/`
- `<project>/.junie/agents/`
- `<project>/.junie/models/`
- `<project>/.junie/mcp/`
- `<project>/.junie/rules/`
- `~/.junie/commands/`, `~/.junie/agents/`, `~/.junie/models/`, `~/.junie/mcp/`

Practical rule: prefer `.junie/AGENTS.md` for repo-specific guidance and `.junie/rules/*.md` for split-out domain rules. Avoid setting `guidelines-location` unless you are intentionally overriding discovery.

Junie can also be pointed at additional skills/guidelines via config or environment variables.

## Practical recommendations

- Prefer headless auth and config files over interactive setup when possible.
- Ask before persisting secrets in `config.json`.
- Merge existing config; do not replace it unless explicitly asked.
- Preserve Junie-owned runtime state such as `~/.junie/settings.json` unless the user explicitly wants it edited.
- Use the interactive UI only when a human specifically wants that experience or when there is no documented non-interactive equivalent.
