# Pi CLI Reference

## Modes

| Flag | Description |
|------|-------------|
| (default) | Interactive mode |
| `-p, --print` | Print mode, outputs then exits |
| `--mode json` | JSON event stream |
| `--mode rpc` | RPC stdin/stdout |

Print mode supports pipe input: `cat README.md | pi -p "Summarize"`

## Model Options

| Option | Description |
|--------|-------------|
| `--provider <name>` | Provider: anthropic/openai/google etc. |
| `--model <pattern>` | Model ID, supports `provider/id` and `:<thinking>` |
| `--api-key <key>` | API key (overrides env var) |
| `--thinking <level>` | off/minimal/low/medium/high/xhigh |
| `--models <patterns>` | Model list for Ctrl+P cycling |
| `--list-models [search]` | List available models |

## Session Options

| Option | Description |
|--------|-------------|
| `-c, --continue` | Continue most recent session |
| `-r, --resume` | Browse session history |
| `--session <path\|id>` | Specify a session |
| `--fork <path\|id>` | Fork to a new session |
| `--session-dir <dir>` | Custom storage directory |
| `--no-session` | Temporary mode |

## Tool Options

| Option | Description |
|--------|-------------|
| `-t, --tools <list>` | Allowlist |
| `-nbt, --no-builtin-tools` | Disable built-in tools |
| `-nt, --no-tools` | Disable all tools |

Built-in tools: read, bash, edit, write, grep, find, ls

## Resource Loading

| Option | Description |
|--------|-------------|
| `-e, --extension <source>` | Load extension (repeatable) |
| `--no-extensions` | Disable extension discovery |
| `--skill <path>` | Load skill (repeatable) |
| `--no-skills` | Disable skill discovery |
| `--prompt-template <path>` | Load prompt template |
| `--no-prompt-templates` | Disable template discovery |
| `--theme <path>` | Load theme |
| `--no-context-files, -nc` | Disable AGENTS.md/CLAUDE.md |

## Miscellaneous

| Option | Description |
|--------|-------------|
| `--system-prompt <text>` | Replace system prompt |
| `--append-system-prompt <text>` | Append to system prompt |
| `--verbose` | Verbose startup logs |
| `-h, --help` | Help |
| `-v, --version` | Version |

## @ File Prefix

Include file contents in messages:

```bash
pi @code.ts @test.ts "Review these files"
pi -p @screenshot.png "What's this?"
pi "List all .ts files in src/"
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PI_CODING_AGENT_DIR` | Config directory (default ~/.pi/agent) |
| `PI_CODING_AGENT_SESSION_DIR` | Session directory |
| `PI_PACKAGE_DIR` | Package install directory |
| `PI_OFFLINE` | Disable startup network operations |
| `PI_SKIP_VERSION_CHECK` | Skip version check |
| `PI_TELEMETRY` | 1/0 to override telemetry |
| `PI_CACHE_RETENTION` | `long` to extend prompt cache |
| `VISUAL`, `EDITOR` | Ctrl+G external editor |

## Design Philosophy

Pi keeps its core minimal — no built-in MCP, sub-agents, permission popups, plan mode, todos, or background bash. These are built through extensions/packages or external tools.