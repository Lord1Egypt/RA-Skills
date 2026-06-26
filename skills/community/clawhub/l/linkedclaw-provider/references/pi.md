# Agent = pi (via pi-acp adapter)

Handler command:

```bash
linkedclaw provider run my-provider.yaml --handler-acp "npx -y pi-acp"
```

`pi-acp` (v0.0.31) is a **tier-2 adapter** — it spawns `pi --mode rpc` internally and
bridges ACP JSON-RPC 2.0 over stdio to the LinkedClaw ACP bridge. The adapter is
published as `pi-acp` on npm; `npx -y pi-acp` fetches and runs it without a global
install.

## Credential

Pi supports subscription-based providers via OAuth (stored in `~/.pi/agent/auth.json`
by pi's interactive `/login` command) and direct API-key providers via environment
variables. The env vars are forwarded by the ACP bridge from the `ENV_ALLOWLIST`:

| Model family | Credential |
|---|---|
| Anthropic (Claude) | `ANTHROPIC_API_KEY` (API key) or OAuth stored by `pi /login` → anthropic |
| OpenAI | `OPENAI_API_KEY` (API key) or OAuth stored by `pi /login` → openai-codex (ChatGPT Plus/Pro) |
| Google Gemini | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Groq / Cerebras / xAI / OpenRouter / etc. | Respective `*_API_KEY` env var (see `pi --help` Environment Variables section) |

**Important: pi has NO google-vertex provider.** `GOOGLE_APPLICATION_CREDENTIALS`
(Vertex AI service-account JSON) does NOT work with pi. If the only available credential
is a Vertex ADC file, pi cannot be used without an explicit API key for one of the
providers above.

## Model selection

Pi selects a model from `--model <pattern>` (CLI flag) or `defaultModel` / `defaultProvider`
in `~/.pi/agent/settings.json`. The ACP adapter (`pi-acp`) does not support a
per-session model override in its current version (v0.0.31) — model selection is
governed by pi's global settings or the `PI_ACP_PI_COMMAND` wrapper.

To pin a model for marketplace use, set `defaultModel` and `defaultProvider` in the
global settings, or use a wrapper script (see confinement section below):

```bash
# ~/.pi/agent/settings.json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-sonnet-4-6"
}
```

All available models are shown by `pi --list-models`.

## How tools are confined (read this — it's the load-bearing part)

**`--acp-permissions reject-all` does NOT confine pi — you MUST use a wrapper script
with pi's own `--no-tools` or `--exclude-tools` flags.**

Pi's tools (`read`, `write`, `bash`, `edit`) execute **locally in the pi process**.
They do NOT pass through the ACP permission channel. Therefore `reject-all` and
`_meta.disableBuiltInTools` have no effect on pi's tool execution.

Furthermore, `pi-acp` v0.0.31 **hardcodes** its spawn args as
`["--mode", "rpc", "--no-themes"]` — there is no way to append extra flags via the
`npx -y pi-acp` command itself. The only supported mechanism is:

### Wrapper-script confinement (required for marketplace safety)

Set `PI_ACP_PI_COMMAND` to the path of a shell wrapper that adds confinement flags:

```bash
# /usr/local/bin/pi-no-bash.sh
#!/bin/sh
exec pi --exclude-tools bash "$@"
```

```bash
chmod +x /usr/local/bin/pi-no-bash.sh
```

Then export `PI_ACP_PI_COMMAND` when running the provider daemon:

```bash
PI_ACP_PI_COMMAND=/usr/local/bin/pi-no-bash.sh \
  linkedclaw provider run my-provider.yaml \
  --handler-acp "npx -y pi-acp"
```

`PI_ACP_PI_COMMAND` is on the `ENV_ALLOWLIST` and is forwarded by the bridge to the
`pi-acp` child process, which passes it to the pi spawner.

For a fully tool-free (text-only) provider, use `--no-tools` instead:

```bash
# /usr/local/bin/pi-no-tools.sh
#!/bin/sh
exec pi --no-tools "$@"
```

### Available pi confinement flags

| Flag | Effect |
|---|---|
| `--no-tools`, `-nt` | Disable ALL tools (built-in and extension). Model is text-in/text-out. |
| `--no-builtin-tools`, `-nbt` | Disable built-in tools only; keep extension/custom tools. |
| `--tools read,grep,find` | Enable only the listed tools (allowlist). |
| `--exclude-tools bash` | Enable all tools EXCEPT the listed ones (denylist). |

For marketplace providers, `--no-tools` is the strictest and safest default.
`--exclude-tools bash` keeps read/write/edit but removes shell execution.

### Why reject-all is insufficient

Pi runs as a standalone process. Its tool calls go directly to the OS — the ACP
protocol layer sits between the LinkedClaw bridge and pi-acp, but pi's internal tool
dispatch never touches that channel. The `_meta.disableBuiltInTools` hint in the ACP
session init is interpreted by compliant ACP servers (like `claude-agent-acp`) that
respect it, but pi-acp does not implement this hint — pi uses its own `--mode rpc`
startup, not an ACP-level tool gate.

## OS sandbox (recommended if tools are kept)

If a capability genuinely needs file or network access (e.g. read-only code review),
use `--exclude-tools bash` (no shell) AND wrap the whole process in
`@anthropic-ai/sandbox-runtime` (`srt`) with a default-deny egress allowlist:

```bash
PI_ACP_PI_COMMAND=/usr/local/bin/pi-no-bash.sh \
  linkedclaw provider run my-provider.yaml \
  --acp-permissions allow-reads \
  --handler-acp "srt npx -y pi-acp"
```

The CLI warns if you keep tools without a detected sandbox wrapper. See
[security.md](security.md) for the full rationale.

## Notes

- Pi stores sessions in `~/.pi/agent/sessions/`. `HOME` is on the env allowlist,
  so the daemon process can reach it. Pi-acp stores a session-mapping file at
  `~/.pi/pi-acp/session-map.json`.
- The `PI_ACP_PI_COMMAND` env var is supported by pi-acp as the executable override.
  On macOS/Linux, pi-acp uses `spawn(cmd, args, {shell: false})` — the command must
  be a path to a binary or script, NOT a command with inline flags
  (e.g. `"pi --no-tools"` will fail with ENOENT on non-Windows). Always use a wrapper
  script.
- Pi has NO settings.json key for tool restriction — `--no-tools` and
  `--exclude-tools` are CLI-only flags. A project-level `.pi/settings.json` cannot
  restrict tools.
- Pi reads `AGENTS.md` (and `CLAUDE.md`) from the cwd walking up; it is in the same
  dedupe bucket as hermes/codex/opencode for `linkedclaw init` context blocks.
