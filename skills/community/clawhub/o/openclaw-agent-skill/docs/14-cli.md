# CLI Reference

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 47

---

<!-- SOURCE: https://docs.openclaw.ai/cli/node -->

# node - OpenClaw

Run a **headless node host** that connects to the Gateway WebSocket and exposes `system.run` / `system.which` on this machine.

## Why use a node host?

Use a node host when you want agents to **run commands on other machines** in your network without installing a full macOS companion app there. Common use cases:

*   Run commands on remote Linux/Windows boxes (build servers, lab machines, NAS).
*   Keep exec **sandboxed** on the gateway, but delegate approved runs to other hosts.
*   Provide a lightweight, headless execution target for automation or CI nodes.

Execution is still guarded by **exec approvals** and per‑agent allowlists on the node host, so you can keep command access scoped and explicit.

## Browser proxy (zero-config)

Node hosts automatically advertise a browser proxy if `browser.enabled` is not disabled on the node. This lets the agent use browser automation on that node without extra configuration. Disable it on the node if needed:

```
{
  nodeHost: {
    browserProxy: {
      enabled: false,
    },
  },
}
```

## Run (foreground)

```
openclaw node run --host <gateway-host> --port 18789
```

Options:

*   `--host <host>`: Gateway WebSocket host (default: `127.0.0.1`)
*   `--port <port>`: Gateway WebSocket port (default: `18789`)
*   `--tls`: Use TLS for the gateway connection
*   `--tls-fingerprint <sha256>`: Expected TLS certificate fingerprint (sha256)
*   `--node-id <id>`: Override node id (clears pairing token)
*   `--display-name <name>`: Override the node display name

## Gateway auth for node host

`openclaw node run` and `openclaw node install` resolve gateway auth from config/env (no `--token`/`--password` flags on node commands):

*   `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD` are checked first.
*   Then local config fallback: `gateway.auth.token` / `gateway.auth.password`.
*   In local mode, `gateway.remote.token` / `gateway.remote.password` are also eligible as fallback when `gateway.auth.*` is unset.
*   In `gateway.mode=remote`, remote client fields (`gateway.remote.token` / `gateway.remote.password`) are also eligible per remote precedence rules.
*   Legacy `CLAWDBOT_GATEWAY_*` env vars are ignored for node host auth resolution.

## Service (background)

Install a headless node host as a user service.

```
openclaw node install --host <gateway-host> --port 18789
```

Options:

*   `--host <host>`: Gateway WebSocket host (default: `127.0.0.1`)
*   `--port <port>`: Gateway WebSocket port (default: `18789`)
*   `--tls`: Use TLS for the gateway connection
*   `--tls-fingerprint <sha256>`: Expected TLS certificate fingerprint (sha256)
*   `--node-id <id>`: Override node id (clears pairing token)
*   `--display-name <name>`: Override the node display name
*   `--runtime <runtime>`: Service runtime (`node` or `bun`)
*   `--force`: Reinstall/overwrite if already installed

Manage the service:

```
openclaw node status
openclaw node stop
openclaw node restart
openclaw node uninstall
```

Use `openclaw node run` for a foreground node host (no service). Service commands accept `--json` for machine-readable output.

## Pairing

The first connection creates a pending device pairing request (`role: node`) on the Gateway. Approve it via:

```
openclaw devices list
openclaw devices approve <requestId>
```

The node host stores its node id, token, display name, and gateway connection info in `~/.openclaw/node.json`.

## Exec approvals

`system.run` is gated by local exec approvals:

*   `~/.openclaw/exec-approvals.json`
*   [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals)
*   `openclaw approvals --node <id|name|ip>` (edit from the Gateway)

---

<!-- SOURCE: https://docs.openclaw.ai/cli/acp -->

# acp - OpenClaw

Run the [Agent Client Protocol (ACP)](https://agentclientprotocol.com/) bridge that talks to a OpenClaw Gateway. This command speaks ACP over stdio for IDEs and forwards prompts to the Gateway over WebSocket. It keeps ACP sessions mapped to Gateway session keys.

## Usage

```
openclaw acp

# Remote Gateway
openclaw acp --url wss://gateway-host:18789 --token <token>

# Remote Gateway (token from file)
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Attach to an existing session key
openclaw acp --session agent:main:main

# Attach by label (must already exist)
openclaw acp --session-label "support inbox"

# Reset the session key before the first prompt
openclaw acp --session agent:main:main --reset-session
```

## ACP client (debug)

Use the built-in ACP client to sanity-check the bridge without an IDE. It spawns the ACP bridge and lets you type prompts interactively.

```
openclaw acp client

# Point the spawned bridge at a remote Gateway
openclaw acp client --server-args --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token

# Override the server command (default: openclaw)
openclaw acp client --server "node" --server-args openclaw.mjs acp --url ws://127.0.0.1:19001
```

Permission model (client debug mode):

*   Auto-approval is allowlist-based and only applies to trusted core tool IDs.
*   `read` auto-approval is scoped to the current working directory (`--cwd` when set).
*   Unknown/non-core tool names, out-of-scope reads, and dangerous tools always require explicit prompt approval.
*   Server-provided `toolCall.kind` is treated as untrusted metadata (not an authorization source).

## How to use this

Use ACP when an IDE (or other client) speaks Agent Client Protocol and you want it to drive a OpenClaw Gateway session.

1.  Ensure the Gateway is running (local or remote).
2.  Configure the Gateway target (config or flags).
3.  Point your IDE to run `openclaw acp` over stdio.

Example config (persisted):

```
openclaw config set gateway.remote.url wss://gateway-host:18789
openclaw config set gateway.remote.token <token>
```

Example direct run (no config write):

```
openclaw acp --url wss://gateway-host:18789 --token <token>
# preferred for local process safety
openclaw acp --url wss://gateway-host:18789 --token-file ~/.openclaw/gateway.token
```

## Selecting agents

ACP does not pick agents directly. It routes by the Gateway session key. Use agent-scoped session keys to target a specific agent:

```
openclaw acp --session agent:main:main
openclaw acp --session agent:design:main
openclaw acp --session agent:qa:bug-123
```

Each ACP session maps to a single Gateway session key. One agent can have many sessions; ACP defaults to an isolated `acp:<uuid>` session unless you override the key or label.

## Use from `acpx` (Codex, Claude, other ACP clients)

If you want a coding agent such as Codex or Claude Code to talk to your OpenClaw bot over ACP, use `acpx` with its built-in `openclaw` target. Typical flow:

1.  Run the Gateway and make sure the ACP bridge can reach it.
2.  Point `acpx openclaw` at `openclaw acp`.
3.  Target the OpenClaw session key you want the coding agent to use.

Examples:

```
# One-shot request into your default OpenClaw ACP session
acpx openclaw exec "Summarize the active OpenClaw session state."

# Persistent named session for follow-up turns
acpx openclaw sessions ensure --name codex-bridge
acpx openclaw -s codex-bridge --cwd /path/to/repo \
  "Ask my OpenClaw work agent for recent context relevant to this repo."
```

If you want `acpx openclaw` to target a specific Gateway and session key every time, override the `openclaw` agent command in `~/.acpx/config.json`:

```
{
  "agents": {
    "openclaw": {
      "command": "env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 openclaw acp --url ws://127.0.0.1:18789 --token-file ~/.openclaw/gateway.token --session agent:main:main"
    }
  }
}
```

For a repo-local OpenClaw checkout, use the direct CLI entrypoint instead of the dev runner so the ACP stream stays clean. For example:

```
env OPENCLAW_HIDE_BANNER=1 OPENCLAW_SUPPRESS_NOTES=1 node openclaw.mjs acp ...
```

This is the easiest way to let Codex, Claude Code, or another ACP-aware client pull contextual information from an OpenClaw agent without scraping a terminal.

## Zed editor setup

Add a custom ACP agent in `~/.config/zed/settings.json` (or use Zed’s Settings UI):

```
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": ["acp"],
      "env": {}
    }
  }
}
```

To target a specific Gateway or agent:

```
{
  "agent_servers": {
    "OpenClaw ACP": {
      "type": "custom",
      "command": "openclaw",
      "args": [
        "acp",
        "--url",
        "wss://gateway-host:18789",
        "--token",
        "<token>",
        "--session",
        "agent:design:main"
      ],
      "env": {}
    }
  }
}
```

In Zed, open the Agent panel and select “OpenClaw ACP” to start a thread.

## Session mapping

By default, ACP sessions get an isolated Gateway session key with an `acp:` prefix. To reuse a known session, pass a session key or label:

*   `--session <key>`: use a specific Gateway session key.
*   `--session-label <label>`: resolve an existing session by label.
*   `--reset-session`: mint a fresh session id for that key (same key, new transcript).

If your ACP client supports metadata, you can override per session:

```
{
  "_meta": {
    "sessionKey": "agent:main:main",
    "sessionLabel": "support inbox",
    "resetSession": true
  }
}
```

Learn more about session keys at [/concepts/session](https://docs.openclaw.ai/concepts/session).

## Options

*   `--url <url>`: Gateway WebSocket URL (defaults to gateway.remote.url when configured).
*   `--token <token>`: Gateway auth token.
*   `--token-file <path>`: read Gateway auth token from file.
*   `--password <password>`: Gateway auth password.
*   `--password-file <path>`: read Gateway auth password from file.
*   `--session <key>`: default session key.
*   `--session-label <label>`: default session label to resolve.
*   `--require-existing`: fail if the session key/label does not exist.
*   `--reset-session`: reset the session key before first use.
*   `--no-prefix-cwd`: do not prefix prompts with the working directory.
*   `--verbose, -v`: verbose logging to stderr.

Security note:

*   `--token` and `--password` can be visible in local process listings on some systems.
*   Prefer `--token-file`/`--password-file` or environment variables (`OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_PASSWORD`).
*   Gateway auth resolution follows the shared contract used by other Gateway clients:
    *   local mode: env (`OPENCLAW_GATEWAY_*`) -> `gateway.auth.*` -> `gateway.remote.*` fallback when `gateway.auth.*` is unset
    *   remote mode: `gateway.remote.*` with env/config fallback per remote precedence rules
    *   `--url` is override-safe and does not reuse implicit config/env credentials; pass explicit `--token`/`--password` (or file variants)
*   ACP runtime backend child processes receive `OPENCLAW_SHELL=acp`, which can be used for context-specific shell/profile rules.
*   `openclaw acp client` sets `OPENCLAW_SHELL=acp-client` on the spawned bridge process.

### `acp client` options

*   `--cwd <dir>`: working directory for the ACP session.
*   `--server <command>`: ACP server command (default: `openclaw`).
*   `--server-args <args...>`: extra arguments passed to the ACP server.
*   `--server-verbose`: enable verbose logging on the ACP server.
*   `--verbose, -v`: verbose client logging.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/pairing -->

# pairing - OpenClaw

Approve or inspect DM pairing requests (for channels that support pairing). Related:

*   Pairing flow: [Pairing](https://docs.openclaw.ai/channels/pairing)

## Commands

```
openclaw pairing list telegram
openclaw pairing list --channel telegram --account work
openclaw pairing list telegram --json

openclaw pairing approve telegram <code>
openclaw pairing approve --channel telegram --account work <code> --notify
```

## Notes

*   Channel input: pass it positionally (`pairing list telegram`) or with `--channel <channel>`.
*   `pairing list` supports `--account <accountId>` for multi-account channels.
*   `pairing approve` supports `--account <accountId>` and `--notify`.
*   If only one pairing-capable channel is configured, `pairing approve <code>` is allowed.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/onboard -->

# onboard - OpenClaw

Interactive onboarding wizard (local or remote Gateway setup).

*   CLI onboarding hub: [Onboarding Wizard (CLI)](https://docs.openclaw.ai/start/wizard)
*   Onboarding overview: [Onboarding Overview](https://docs.openclaw.ai/start/onboarding-overview)
*   CLI onboarding reference: [CLI Onboarding Reference](https://docs.openclaw.ai/start/wizard-cli-reference)
*   CLI automation: [CLI Automation](https://docs.openclaw.ai/start/wizard-cli-automation)
*   macOS onboarding: [Onboarding (macOS App)](https://docs.openclaw.ai/start/onboarding)

## Examples

```
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url wss://gateway-host:18789
```

For plaintext private-network `ws://` targets (trusted networks only), set `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` in the onboarding process environment. Non-interactive custom provider:

```
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --secret-input-mode plaintext \
  --custom-compatibility openai
```

`--custom-api-key` is optional in non-interactive mode. If omitted, onboarding checks `CUSTOM_API_KEY`. Store provider keys as refs instead of plaintext:

```
openclaw onboard --non-interactive \
  --auth-choice openai-api-key \
  --secret-input-mode ref \
  --accept-risk
```

With `--secret-input-mode ref`, onboarding writes env-backed refs instead of plaintext key values. For auth-profile backed providers this writes `keyRef` entries; for custom providers this writes `models.providers.<id>.apiKey` as an env ref (for example `{ source: "env", provider: "default", id: "CUSTOM_API_KEY" }`). Non-interactive `ref` mode contract:

*   Set the provider env var in the onboarding process environment (for example `OPENAI_API_KEY`).
*   Do not pass inline key flags (for example `--openai-api-key`) unless that env var is also set.
*   If an inline key flag is passed without the required env var, onboarding fails fast with guidance.

Gateway token options in non-interactive mode:

*   `--gateway-auth token --gateway-token <token>` stores a plaintext token.
*   `--gateway-auth token --gateway-token-ref-env <name>` stores `gateway.auth.token` as an env SecretRef.
*   `--gateway-token` and `--gateway-token-ref-env` are mutually exclusive.
*   `--gateway-token-ref-env` requires a non-empty env var in the onboarding process environment.
*   With `--install-daemon`, when token auth requires a token, SecretRef-managed gateway tokens are validated but not persisted as resolved plaintext in supervisor service environment metadata.
*   With `--install-daemon`, if token mode requires a token and the configured token SecretRef is unresolved, onboarding fails closed with remediation guidance.
*   With `--install-daemon`, if both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, onboarding blocks install until mode is set explicitly.

Example:

```
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN \
  --accept-risk
```

Interactive onboarding behavior with reference mode:

*   Choose **Use secret reference** when prompted.
*   Then choose either:
    *   Environment variable
    *   Configured secret provider (`file` or `exec`)
*   Onboarding performs a fast preflight validation before saving the ref.
    *   If validation fails, onboarding shows the error and lets you retry.

Non-interactive Z.AI endpoint choices: Note: `--auth-choice zai-api-key` now auto-detects the best Z.AI endpoint for your key (prefers the general API with `zai/glm-5`). If you specifically want the GLM Coding Plan endpoints, pick `zai-coding-global` or `zai-coding-cn`.

```
# Promptless endpoint selection
openclaw onboard --non-interactive \
  --auth-choice zai-coding-global \
  --zai-api-key "$ZAI_API_KEY"

# Other Z.AI endpoint choices:
# --auth-choice zai-coding-cn
# --auth-choice zai-global
# --auth-choice zai-cn
```

Non-interactive Mistral example:

```
openclaw onboard --non-interactive \
  --auth-choice mistral-api-key \
  --mistral-api-key "$MISTRAL_API_KEY"
```

Flow notes:

*   `quickstart`: minimal prompts, auto-generates a gateway token.
*   `manual`: full prompts for port/bind/auth (alias of `advanced`).
*   Local onboarding DM scope behavior: [CLI Onboarding Reference](https://docs.openclaw.ai/start/wizard-cli-reference#outputs-and-internals).
*   Fastest first chat: `openclaw dashboard` (Control UI, no channel setup).
*   Custom Provider: connect any OpenAI or Anthropic compatible endpoint, including hosted providers not listed. Use Unknown to auto-detect.

## Common follow-up commands

```
openclaw configure
openclaw agents add <name>
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/agent -->

# agent - OpenClaw

Run an agent turn via the Gateway (use `--local` for embedded). Use `--agent <id>` to target a configured agent directly. Related:

*   Agent send tool: [Agent send](https://docs.openclaw.ai/tools/agent-send)

## Examples

```
openclaw agent --to +15555550123 --message "status update" --deliver
openclaw agent --agent ops --message "Summarize logs"
openclaw agent --session-id 1234 --message "Summarize inbox" --thinking medium
openclaw agent --agent ops --message "Generate report" --deliver --reply-channel slack --reply-to "#reports"
```

## Notes

*   When this command triggers `models.json` regeneration, SecretRef-managed provider credentials are persisted as non-secret markers (for example env var names or `secretref-managed`), not resolved secret plaintext.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/plugins -->

# plugins - OpenClaw

Manage Gateway plugins/extensions (loaded in-process). Related:

*   Plugin system: [Plugins](https://docs.openclaw.ai/tools/plugin)
*   Plugin manifest + schema: [Plugin manifest](https://docs.openclaw.ai/plugins/manifest)
*   Security hardening: [Security](https://docs.openclaw.ai/gateway/security)

## Commands

```
openclaw plugins list
openclaw plugins info <id>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins uninstall <id>
openclaw plugins doctor
openclaw plugins update <id>
openclaw plugins update --all
```

Bundled plugins ship with OpenClaw but start disabled. Use `plugins enable` to activate them. All plugins must ship a `openclaw.plugin.json` file with an inline JSON Schema (`configSchema`, even if empty). Missing/invalid manifests or schemas prevent the plugin from loading and fail config validation.

### Install

```
openclaw plugins install <path-or-spec>
openclaw plugins install <npm-spec> --pin
```

Security note: treat plugin installs like running code. Prefer pinned versions. Npm specs are **registry-only** (package name + optional **exact version** or **dist-tag**). Git/URL/file specs and semver ranges are rejected. Dependency installs run with `--ignore-scripts` for safety. Bare specs and `@latest` stay on the stable track. If npm resolves either of those to a prerelease, OpenClaw stops and asks you to opt in explicitly with a prerelease tag such as `@beta`/`@rc` or an exact prerelease version such as `@1.2.3-beta.4`. If a bare install spec matches a bundled plugin id (for example `diffs`), OpenClaw installs the bundled plugin directly. To install an npm package with the same name, use an explicit scoped spec (for example `@scope/diffs`). Supported archives: `.zip`, `.tgz`, `.tar.gz`, `.tar`. Use `--link` to avoid copying a local directory (adds to `plugins.load.paths`):

```
openclaw plugins install -l ./my-plugin
```

Use `--pin` on npm installs to save the resolved exact spec (`name@version`) in `plugins.installs` while keeping the default behavior unpinned.

### Uninstall

```
openclaw plugins uninstall <id>
openclaw plugins uninstall <id> --dry-run
openclaw plugins uninstall <id> --keep-files
```

`uninstall` removes plugin records from `plugins.entries`, `plugins.installs`, the plugin allowlist, and linked `plugins.load.paths` entries when applicable. For active memory plugins, the memory slot resets to `memory-core`. By default, uninstall also removes the plugin install directory under the active state dir extensions root (`$OPENCLAW_STATE_DIR/extensions/<id>`). Use `--keep-files` to keep files on disk. `--keep-config` is supported as a deprecated alias for `--keep-files`.

### Update

```
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins update <id> --dry-run
```

Updates only apply to plugins installed from npm (tracked in `plugins.installs`). When a stored integrity hash exists and the fetched artifact hash changes, OpenClaw prints a warning and asks for confirmation before proceeding. Use global `--yes` to bypass prompts in CI/non-interactive runs.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/qr -->

# qr - OpenClaw

Generate an iOS pairing QR and setup code from your current Gateway configuration.

## Usage

```
openclaw qr
openclaw qr --setup-code-only
openclaw qr --json
openclaw qr --remote
openclaw qr --url wss://gateway.example/ws --token '<token>'
```

## Options

*   `--remote`: use `gateway.remote.url` plus remote token/password from config
*   `--url <url>`: override gateway URL used in payload
*   `--public-url <url>`: override public URL used in payload
*   `--token <token>`: override gateway token for payload
*   `--password <password>`: override gateway password for payload
*   `--setup-code-only`: print only setup code
*   `--no-ascii`: skip ASCII QR rendering
*   `--json`: emit JSON (`setupCode`, `gatewayUrl`, `auth`, `urlSource`)

## Notes

*   `--token` and `--password` are mutually exclusive.
*   With `--remote`, if effectively active remote credentials are configured as SecretRefs and you do not pass `--token` or `--password`, the command resolves them from the active gateway snapshot. If gateway is unavailable, the command fails fast.
*   Without `--remote`, local gateway auth SecretRefs are resolved when no CLI auth override is passed:
    *   `gateway.auth.token` resolves when token auth can win (explicit `gateway.auth.mode="token"` or inferred mode where no password source wins).
    *   `gateway.auth.password` resolves when password auth can win (explicit `gateway.auth.mode="password"` or inferred mode with no winning token from auth/env).
*   If both `gateway.auth.token` and `gateway.auth.password` are configured (including SecretRefs) and `gateway.auth.mode` is unset, setup-code resolution fails until mode is set explicitly.
*   Gateway version skew note: this command path requires a gateway that supports `secrets.resolve`; older gateways return an unknown-method error.
*   After scanning, approve device pairing with:
    *   `openclaw devices list`
    *   `openclaw devices approve <requestId>`

---

<!-- SOURCE: https://docs.openclaw.ai/cli/approvals -->

# approvals - OpenClaw

Manage exec approvals for the **local host**, **gateway host**, or a **node host**. By default, commands target the local approvals file on disk. Use `--gateway` to target the gateway, or `--node` to target a specific node. Related:

*   Exec approvals: [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals)
*   Nodes: [Nodes](https://docs.openclaw.ai/nodes)

## Common commands

```
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway
```

## Replace approvals from a file

```
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json
```

## Allowlist helpers

```
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"
```

## Notes

*   `--node` uses the same resolver as `openclaw nodes` (id, name, ip, or id prefix).
*   `--agent` defaults to `"*"`, which applies to all agents.
*   The node host must advertise `system.execApprovals.get/set` (macOS app or headless node host).
*   Approvals files are stored per host at `~/.openclaw/exec-approvals.json`.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/reset -->

# reset - OpenClaw

Reset local config/state (keeps the CLI installed).

```
openclaw backup create
openclaw reset
openclaw reset --dry-run
openclaw reset --scope config+creds+sessions --yes --non-interactive
```

Run `openclaw backup create` first if you want a restorable snapshot before removing local state.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/agents -->

# agents - OpenClaw

Manage isolated agents (workspaces + auth + routing). Related:

*   Multi-agent routing: [Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
*   Agent workspace: [Agent workspace](https://docs.openclaw.ai/concepts/agent-workspace)

## Examples

```
openclaw agents list
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents bindings
openclaw agents bind --agent work --bind telegram:ops
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
openclaw agents set-identity --agent main --avatar avatars/openclaw.png
openclaw agents delete work
```

## Routing bindings

Use routing bindings to pin inbound channel traffic to a specific agent. List bindings:

```
openclaw agents bindings
openclaw agents bindings --agent work
openclaw agents bindings --json
```

Add bindings:

```
openclaw agents bind --agent work --bind telegram:ops --bind discord:guild-a
```

If you omit `accountId` (`--bind <channel>`), OpenClaw resolves it from channel defaults and plugin setup hooks when available.

### Binding scope behavior

*   A binding without `accountId` matches the channel default account only.
*   `accountId: "*"` is the channel-wide fallback (all accounts) and is less specific than an explicit account binding.
*   If the same agent already has a matching channel binding without `accountId`, and you later bind with an explicit or resolved `accountId`, OpenClaw upgrades that existing binding in place instead of adding a duplicate.

Example:

```
# initial channel-only binding
openclaw agents bind --agent work --bind telegram

# later upgrade to account-scoped binding
openclaw agents bind --agent work --bind telegram:ops
```

After the upgrade, routing for that binding is scoped to `telegram:ops`. If you also want default-account routing, add it explicitly (for example `--bind telegram:default`). Remove bindings:

```
openclaw agents unbind --agent work --bind telegram:ops
openclaw agents unbind --agent work --all
```

## Identity files

Each agent workspace can include an `IDENTITY.md` at the workspace root:

*   Example path: `~/.openclaw/workspace/IDENTITY.md`
*   `set-identity --from-identity` reads from the workspace root (or an explicit `--identity-file`)

Avatar paths resolve relative to the workspace root.

## Set identity

`set-identity` writes fields into `agents.list[].identity`:

*   `name`
*   `theme`
*   `emoji`
*   `avatar` (workspace-relative path, http(s) URL, or data URI)

Load from `IDENTITY.md`:

```
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
```

Override fields explicitly:

```
openclaw agents set-identity --agent main --name "OpenClaw" --emoji "🦞" --avatar avatars/openclaw.png
```

Config sample:

```
{
  agents: {
    list: [
      {
        id: "main",
        identity: {
          name: "OpenClaw",
          theme: "space lobster",
          emoji: "🦞",
          avatar: "avatars/openclaw.png",
        },
      },
    ],
  },
}
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/browser -->

# browser - OpenClaw

Manage OpenClaw’s browser control server and run browser actions (tabs, snapshots, screenshots, navigation, clicks, typing). Related:

*   Browser tool + API: [Browser tool](https://docs.openclaw.ai/tools/browser)
*   Chrome extension relay: [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension)

## Common flags

*   `--url <gatewayWsUrl>`: Gateway WebSocket URL (defaults to config).
*   `--token <token>`: Gateway token (if required).
*   `--timeout <ms>`: request timeout (ms).
*   `--browser-profile <name>`: choose a browser profile (default from config).
*   `--json`: machine-readable output (where supported).

## Quick start (local)

```
openclaw browser --browser-profile chrome tabs
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

## Profiles

Profiles are named browser routing configs. In practice:

*   `openclaw`: launches/attaches to a dedicated OpenClaw-managed Chrome instance (isolated user data dir).
*   `chrome`: controls your existing Chrome tab(s) via the Chrome extension relay.

```
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser delete-profile --name work
```

Use a specific profile:

```
openclaw browser --browser-profile work tabs
```

## Tabs

```
openclaw browser tabs
openclaw browser open https://docs.openclaw.ai
openclaw browser focus <targetId>
openclaw browser close <targetId>
```

## Snapshot / screenshot / actions

Snapshot:

```
openclaw browser snapshot
```

Screenshot:

```
openclaw browser screenshot
```

Navigate/click/type (ref-based UI automation):

```
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser type <ref> "hello"
```

This mode lets the agent control an existing Chrome tab that you attach manually (it does not auto-attach). Install the unpacked extension to a stable path:

```
openclaw browser extension install
openclaw browser extension path
```

Then Chrome → `chrome://extensions` → enable “Developer mode” → “Load unpacked” → select the printed folder. Full guide: [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension)

## Remote browser control (node host proxy)

If the Gateway runs on a different machine than the browser, run a **node host** on the machine that has Chrome/Brave/Edge/Chromium. The Gateway will proxy browser actions to that node (no separate browser control server required). Use `gateway.nodes.browser.mode` to control auto-routing and `gateway.nodes.browser.node` to pin a specific node if multiple are connected. Security + remote setup: [Browser tool](https://docs.openclaw.ai/tools/browser), [Remote access](https://docs.openclaw.ai/gateway/remote), [Tailscale](https://docs.openclaw.ai/gateway/tailscale), [Security](https://docs.openclaw.ai/gateway/security)

---

<!-- SOURCE: https://docs.openclaw.ai/cli/channels -->

# channels - OpenClaw

Manage chat channel accounts and their runtime status on the Gateway. Related docs:

*   Channel guides: [Channels](https://docs.openclaw.ai/channels/index)
*   Gateway configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration)

## Common commands

```
openclaw channels list
openclaw channels status
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels logs --channel all
```

## Add / remove accounts

```
openclaw channels add --channel telegram --token <bot-token>
openclaw channels remove --channel telegram --delete
```

Tip: `openclaw channels add --help` shows per-channel flags (token, app token, signal-cli paths, etc). When you run `openclaw channels add` without flags, the interactive wizard can prompt:

*   account ids per selected channel
*   optional display names for those accounts
*   `Bind configured channel accounts to agents now?`

If you confirm bind now, the wizard asks which agent should own each configured channel account and writes account-scoped routing bindings. You can also manage the same routing rules later with `openclaw agents bindings`, `openclaw agents bind`, and `openclaw agents unbind` (see [agents](https://docs.openclaw.ai/cli/agents)). When you add a non-default account to a channel that is still using single-account top-level settings (no `channels.<channel>.accounts` entries yet), OpenClaw moves account-scoped single-account top-level values into `channels.<channel>.accounts.default`, then writes the new account. This preserves the original account behavior while moving to the multi-account shape. Routing behavior stays consistent:

*   Existing channel-only bindings (no `accountId`) continue to match the default account.
*   `channels add` does not auto-create or rewrite bindings in non-interactive mode.
*   Interactive setup can optionally add account-scoped bindings.

If your config was already in a mixed state (named accounts present, missing `default`, and top-level single-account values still set), run `openclaw doctor --fix` to move account-scoped values into `accounts.default`.

## Login / logout (interactive)

```
openclaw channels login --channel whatsapp
openclaw channels logout --channel whatsapp
```

## Troubleshooting

*   Run `openclaw status --deep` for a broad probe.
*   Use `openclaw doctor` for guided fixes.
*   `openclaw channels list` prints `Claude: HTTP 403 ... user:profile` → usage snapshot needs the `user:profile` scope. Use `--no-usage`, or provide a claude.ai session key (`CLAUDE_WEB_SESSION_KEY` / `CLAUDE_WEB_COOKIE`), or re-auth via Claude Code CLI.
*   `openclaw channels status` falls back to config-only summaries when the gateway is unreachable. If a supported channel credential is configured via SecretRef but unavailable in the current command path, it reports that account as configured with degraded notes instead of showing it as not configured.

## Capabilities probe

Fetch provider capability hints (intents/scopes where available) plus static feature support:

```
openclaw channels capabilities
openclaw channels capabilities --channel discord --target channel:123
```

Notes:

*   `--channel` is optional; omit it to list every channel (including extensions).
*   `--target` accepts `channel:<id>` or a raw numeric channel id and only applies to Discord.
*   Probes are provider-specific: Discord intents + optional channel permissions; Slack bot + user scopes; Telegram bot flags + webhook; Signal daemon version; MS Teams app token + Graph roles/scopes (annotated where known). Channels without probes report `Probe: unavailable`.

## Resolve names to IDs

Resolve channel/user names to IDs using the provider directory:

```
openclaw channels resolve --channel slack "#general" "@jane"
openclaw channels resolve --channel discord "My Server/#support" "@someone"
openclaw channels resolve --channel matrix "Project Room"
```

Notes:

*   Use `--kind user|group|auto` to force the target type.
*   Resolution prefers active matches when multiple entries share the same name.
*   `channels resolve` is read-only. If a selected account is configured via SecretRef but that credential is unavailable in the current command path, the command returns degraded unresolved results with notes instead of aborting the entire run.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/sandbox -->

# Sandbox CLI - OpenClaw

Manage Docker-based sandbox containers for isolated agent execution.

## Overview

OpenClaw can run agents in isolated Docker containers for security. The `sandbox` commands help you manage these containers, especially after updates or configuration changes.

## Commands

### `openclaw sandbox explain`

Inspect the **effective** sandbox mode/scope/workspace access, sandbox tool policy, and elevated gates (with fix-it config key paths).

```
openclaw sandbox explain
openclaw sandbox explain --session agent:main:main
openclaw sandbox explain --agent work
openclaw sandbox explain --json
```

### `openclaw sandbox list`

List all sandbox containers with their status and configuration.

```
openclaw sandbox list
openclaw sandbox list --browser  # List only browser containers
openclaw sandbox list --json     # JSON output
```

**Output includes:**

*   Container name and status (running/stopped)
*   Docker image and whether it matches config
*   Age (time since creation)
*   Idle time (time since last use)
*   Associated session/agent

### `openclaw sandbox recreate`

Remove sandbox containers to force recreation with updated images/config.

```
openclaw sandbox recreate --all                # Recreate all containers
openclaw sandbox recreate --session main       # Specific session
openclaw sandbox recreate --agent mybot        # Specific agent
openclaw sandbox recreate --browser            # Only browser containers
openclaw sandbox recreate --all --force        # Skip confirmation
```

**Options:**

*   `--all`: Recreate all sandbox containers
*   `--session <key>`: Recreate container for specific session
*   `--agent <id>`: Recreate containers for specific agent
*   `--browser`: Only recreate browser containers
*   `--force`: Skip confirmation prompt

**Important:** Containers are automatically recreated when the agent is next used.

## Use Cases

### After updating Docker images

```
# Pull new image
docker pull openclaw-sandbox:latest
docker tag openclaw-sandbox:latest openclaw-sandbox:bookworm-slim

# Update config to use new image
# Edit config: agents.defaults.sandbox.docker.image (or agents.list[].sandbox.docker.image)

# Recreate containers
openclaw sandbox recreate --all
```

### After changing sandbox configuration

```
# Edit config: agents.defaults.sandbox.* (or agents.list[].sandbox.*)

# Recreate to apply new config
openclaw sandbox recreate --all
```

### After changing setupCommand

```
openclaw sandbox recreate --all
# or just one agent:
openclaw sandbox recreate --agent family
```

### For a specific agent only

```
# Update only one agent's containers
openclaw sandbox recreate --agent alfred
```

## Why is this needed?

**Problem:** When you update sandbox Docker images or configuration:

*   Existing containers continue running with old settings
*   Containers are only pruned after 24h of inactivity
*   Regularly-used agents keep old containers running indefinitely

**Solution:** Use `openclaw sandbox recreate` to force removal of old containers. They’ll be recreated automatically with current settings when next needed. Tip: prefer `openclaw sandbox recreate` over manual `docker rm`. It uses the Gateway’s container naming and avoids mismatches when scope/session keys change.

## Configuration

Sandbox settings live in `~/.openclaw/openclaw.json` under `agents.defaults.sandbox` (per-agent overrides go in `agents.list[].sandbox`):

```
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all", // off, non-main, all
        "scope": "agent", // session, agent, shared
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "containerPrefix": "openclaw-sbx-",
          // ... more Docker options
        },
        "prune": {
          "idleHours": 24, // Auto-prune after 24h idle
          "maxAgeDays": 7, // Auto-prune after 7 days
        },
      },
    },
  },
}
```

## See Also

*   [Sandbox Documentation](https://docs.openclaw.ai/gateway/sandboxing)
*   [Agent Configuration](https://docs.openclaw.ai/concepts/agent-workspace)
*   [Doctor Command](https://docs.openclaw.ai/gateway/doctor) - Check sandbox setup

---

<!-- SOURCE: https://docs.openclaw.ai/cli/secrets -->

# secrets - OpenClaw

Use `openclaw secrets` to manage SecretRefs and keep the active runtime snapshot healthy. Command roles:

*   `reload`: gateway RPC (`secrets.reload`) that re-resolves refs and swaps runtime snapshot only on full success (no config writes).
*   `audit`: read-only scan of configuration/auth/generated-model stores and legacy residues for plaintext, unresolved refs, and precedence drift.
*   `configure`: interactive planner for provider setup, target mapping, and preflight (TTY required).
*   `apply`: execute a saved plan (`--dry-run` for validation only), then scrub targeted plaintext residues.

Recommended operator loop:

```
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets audit --check
openclaw secrets reload
```

Exit code note for CI/gates:

*   `audit --check` returns `1` on findings.
*   unresolved refs return `2`.

Related:

*   Secrets guide: [Secrets Management](https://docs.openclaw.ai/gateway/secrets)
*   Credential surface: [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface)
*   Security guide: [Security](https://docs.openclaw.ai/gateway/security)

## Reload runtime snapshot

Re-resolve secret refs and atomically swap runtime snapshot.

```
openclaw secrets reload
openclaw secrets reload --json
```

Notes:

*   Uses gateway RPC method `secrets.reload`.
*   If resolution fails, gateway keeps last-known-good snapshot and returns an error (no partial activation).
*   JSON response includes `warningCount`.

## Audit

Scan OpenClaw state for:

*   plaintext secret storage
*   unresolved refs
*   precedence drift (`auth-profiles.json` credentials shadowing `openclaw.json` refs)
*   generated `agents/*/agent/models.json` residues (provider `apiKey` values and sensitive provider headers)
*   legacy residues (legacy auth store entries, OAuth reminders)

Header residue note:

*   Sensitive provider header detection is name-heuristic based (common auth/credential header names and fragments such as `authorization`, `x-api-key`, `token`, `secret`, `password`, and `credential`).

```
openclaw secrets audit
openclaw secrets audit --check
openclaw secrets audit --json
```

Exit behavior:

*   `--check` exits non-zero on findings.
*   unresolved refs exit with higher-priority non-zero code.

Report shape highlights:

*   `status`: `clean | findings | unresolved`
*   `summary`: `plaintextCount`, `unresolvedRefCount`, `shadowedRefCount`, `legacyResidueCount`
*   finding codes:
    *   `PLAINTEXT_FOUND`
    *   `REF_UNRESOLVED`
    *   `REF_SHADOWED`
    *   `LEGACY_RESIDUE`

## Configure (interactive helper)

Build provider and SecretRef changes interactively, run preflight, and optionally apply:

```
openclaw secrets configure
openclaw secrets configure --plan-out /tmp/openclaw-secrets-plan.json
openclaw secrets configure --apply --yes
openclaw secrets configure --providers-only
openclaw secrets configure --skip-provider-setup
openclaw secrets configure --agent ops
openclaw secrets configure --json
```

Flow:

*   Provider setup first (`add/edit/remove` for `secrets.providers` aliases).
*   Credential mapping second (select fields and assign `{source, provider, id}` refs).
*   Preflight and optional apply last.

Flags:

*   `--providers-only`: configure `secrets.providers` only, skip credential mapping.
*   `--skip-provider-setup`: skip provider setup and map credentials to existing providers.
*   `--agent <id>`: scope `auth-profiles.json` target discovery and writes to one agent store.

Notes:

*   Requires an interactive TTY.
*   You cannot combine `--providers-only` with `--skip-provider-setup`.
*   `configure` targets secret-bearing fields in `openclaw.json` plus `auth-profiles.json` for the selected agent scope.
*   `configure` supports creating new `auth-profiles.json` mappings directly in the picker flow.
*   Canonical supported surface: [SecretRef Credential Surface](https://docs.openclaw.ai/reference/secretref-credential-surface).
*   It performs preflight resolution before apply.
*   Generated plans default to scrub options (`scrubEnv`, `scrubAuthProfilesForProviderTargets`, `scrubLegacyAuthJson` all enabled).
*   Apply path is one-way for scrubbed plaintext values.
*   Without `--apply`, CLI still prompts `Apply this plan now?` after preflight.
*   With `--apply` (and no `--yes`), CLI prompts an extra irreversible confirmation.

Exec provider safety note:

*   Homebrew installs often expose symlinked binaries under `/opt/homebrew/bin/*`.
*   Set `allowSymlinkCommand: true` only when needed for trusted package-manager paths, and pair it with `trustedDirs` (for example `["/opt/homebrew"]`).
*   On Windows, if ACL verification is unavailable for a provider path, OpenClaw fails closed. For trusted paths only, set `allowInsecurePath: true` on that provider to bypass path security checks.

## Apply a saved plan

Apply or preflight a plan generated previously:

```
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --dry-run
openclaw secrets apply --from /tmp/openclaw-secrets-plan.json --json
```

Plan contract details (allowed target paths, validation rules, and failure semantics):

*   [Secrets Apply Plan Contract](https://docs.openclaw.ai/gateway/secrets-plan-contract)

What `apply` may update:

*   `openclaw.json` (SecretRef targets + provider upserts/deletes)
*   `auth-profiles.json` (provider-target scrubbing)
*   legacy `auth.json` residues
*   `~/.openclaw/.env` known secret keys whose values were migrated

## Why no rollback backups

`secrets apply` intentionally does not write rollback backups containing old plaintext values. Safety comes from strict preflight + atomic-ish apply with best-effort in-memory restore on failure.

## Example

```
openclaw secrets audit --check
openclaw secrets configure
openclaw secrets audit --check
```

If `audit --check` still reports plaintext findings, update the remaining reported target paths and rerun audit.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/clawbot -->

# clawbot - OpenClaw

Legacy alias namespace kept for backwards compatibility. Current supported alias:

*   `openclaw clawbot qr` (same behavior as [`openclaw qr`](https://docs.openclaw.ai/cli/qr))

## Migration

Prefer modern top-level commands directly:

*   `openclaw clawbot qr` -> `openclaw qr`

---

<!-- SOURCE: https://docs.openclaw.ai/cli/sessions -->

# sessions - OpenClaw

List stored conversation sessions.

```
openclaw sessions
openclaw sessions --agent work
openclaw sessions --all-agents
openclaw sessions --active 120
openclaw sessions --json
```

Scope selection:

*   default: configured default agent store
*   `--agent <id>`: one configured agent store
*   `--all-agents`: aggregate all configured agent stores
*   `--store <path>`: explicit store path (cannot be combined with `--agent` or `--all-agents`)

JSON examples: `openclaw sessions --all-agents --json`:

```
{
  "path": null,
  "stores": [
    { "agentId": "main", "path": "/home/user/.openclaw/agents/main/sessions/sessions.json" },
    { "agentId": "work", "path": "/home/user/.openclaw/agents/work/sessions/sessions.json" }
  ],
  "allAgents": true,
  "count": 2,
  "activeMinutes": null,
  "sessions": [
    { "agentId": "main", "key": "agent:main:main", "model": "gpt-5" },
    { "agentId": "work", "key": "agent:work:main", "model": "claude-opus-4-5" }
  ]
}
```

## Cleanup maintenance

Run maintenance now (instead of waiting for the next write cycle):

```
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --agent work --dry-run
openclaw sessions cleanup --all-agents --dry-run
openclaw sessions cleanup --enforce
openclaw sessions cleanup --enforce --active-key "agent:main:telegram:dm:123"
openclaw sessions cleanup --json
```

`openclaw sessions cleanup` uses `session.maintenance` settings from config:

*   Scope note: `openclaw sessions cleanup` maintains session stores/transcripts only. It does not prune cron run logs (`cron/runs/<jobId>.jsonl`), which are managed by `cron.runLog.maxBytes` and `cron.runLog.keepLines` in [Cron configuration](https://docs.openclaw.ai/automation/cron-jobs#configuration) and explained in [Cron maintenance](https://docs.openclaw.ai/automation/cron-jobs#maintenance).
*   `--dry-run`: preview how many entries would be pruned/capped without writing.
    *   In text mode, dry-run prints a per-session action table (`Action`, `Key`, `Age`, `Model`, `Flags`) so you can see what would be kept vs removed.
*   `--enforce`: apply maintenance even when `session.maintenance.mode` is `warn`.
*   `--active-key <key>`: protect a specific active key from disk-budget eviction.
*   `--agent <id>`: run cleanup for one configured agent store.
*   `--all-agents`: run cleanup for all configured agent stores.
*   `--store <path>`: run against a specific `sessions.json` file.
*   `--json`: print a JSON summary. With `--all-agents`, output includes one summary per store.

`openclaw sessions cleanup --all-agents --dry-run --json`:

```
{
  "allAgents": true,
  "mode": "warn",
  "dryRun": true,
  "stores": [
    {
      "agentId": "main",
      "storePath": "/home/user/.openclaw/agents/main/sessions/sessions.json",
      "beforeCount": 120,
      "afterCount": 80,
      "pruned": 40,
      "capped": 0
    },
    {
      "agentId": "work",
      "storePath": "/home/user/.openclaw/agents/work/sessions/sessions.json",
      "beforeCount": 18,
      "afterCount": 18,
      "pruned": 0,
      "capped": 0
    }
  ]
}
```

Related:

*   Session config: [Configuration reference](https://docs.openclaw.ai/gateway/configuration-reference#session)

---

<!-- SOURCE: https://docs.openclaw.ai/cli/setup -->

# setup - OpenClaw

Initialize `~/.openclaw/openclaw.json` and the agent workspace. Related:

*   Getting started: [Getting started](https://docs.openclaw.ai/start/getting-started)
*   Wizard: [Onboarding](https://docs.openclaw.ai/start/onboarding)

## Examples

```
openclaw setup
openclaw setup --workspace ~/.openclaw/workspace
```

To run the wizard via setup:

---

<!-- SOURCE: https://docs.openclaw.ai/cli/completion -->

# completion - OpenClaw

Generate shell completion scripts and optionally install them into your shell profile.

## Usage

```
openclaw completion
openclaw completion --shell zsh
openclaw completion --install
openclaw completion --shell fish --install
openclaw completion --write-state
openclaw completion --shell bash --write-state
```

## Options

*   `-s, --shell <shell>`: shell target (`zsh`, `bash`, `powershell`, `fish`; default: `zsh`)
*   `-i, --install`: install completion by adding a source line to your shell profile
*   `--write-state`: write completion script(s) to `$OPENCLAW_STATE_DIR/completions` without printing to stdout
*   `-y, --yes`: skip install confirmation prompts

## Notes

*   `--install` writes a small “OpenClaw Completion” block into your shell profile and points it at the cached script.
*   Without `--install` or `--write-state`, the command prints the script to stdout.
*   Completion generation eagerly loads command trees so nested subcommands are included.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/nodes -->

# nodes - OpenClaw

Manage paired nodes (devices) and invoke node capabilities. Related:

*   Nodes overview: [Nodes](https://docs.openclaw.ai/nodes)
*   Camera: [Camera nodes](https://docs.openclaw.ai/nodes/camera)
*   Images: [Image nodes](https://docs.openclaw.ai/nodes/images)

Common options:

*   `--url`, `--token`, `--timeout`, `--json`

## Common commands

```
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h
```

`nodes list` prints pending/paired tables. Paired rows include the most recent connect age (Last Connect). Use `--connected` to only show currently-connected nodes. Use `--last-connected <duration>` to filter to nodes that connected within a duration (e.g. `24h`, `7d`).

## Invoke / run

```
openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
openclaw nodes run --node <id|name|ip> <command...>
openclaw nodes run --raw "git status"
openclaw nodes run --agent main --node <id|name|ip> --raw "git status"
```

Invoke flags:

*   `--params <json>`: JSON object string (default `{}`).
*   `--invoke-timeout <ms>`: node invoke timeout (default `15000`).
*   `--idempotency-key <key>`: optional idempotency key.

### Exec-style defaults

`nodes run` mirrors the model’s exec behavior (defaults + approvals):

*   Reads `tools.exec.*` (plus `agents.list[].tools.exec.*` overrides).
*   Uses exec approvals (`exec.approval.request`) before invoking `system.run`.
*   `--node` can be omitted when `tools.exec.node` is set.
*   Requires a node that advertises `system.run` (macOS companion app or headless node host).

Flags:

*   `--cwd <path>`: working directory.
*   `--env <key=val>`: env override (repeatable). Note: node hosts ignore `PATH` overrides (and `tools.exec.pathPrepend` is not applied to node hosts).
*   `--command-timeout <ms>`: command timeout.
*   `--invoke-timeout <ms>`: node invoke timeout (default `30000`).
*   `--needs-screen-recording`: require screen recording permission.
*   `--raw <command>`: run a shell string (`/bin/sh -lc` or `cmd.exe /c`). In allowlist mode on Windows node hosts, `cmd.exe /c` shell-wrapper runs require approval (allowlist entry alone does not auto-allow the wrapper form).
*   `--agent <id>`: agent-scoped approvals/allowlists (defaults to configured agent).
*   `--ask <off|on-miss|always>`, `--security <deny|allowlist|full>`: overrides.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/status -->

# status - OpenClaw

Diagnostics for channels + sessions.

```
openclaw status
openclaw status --all
openclaw status --deep
openclaw status --usage
```

Notes:

*   `--deep` runs live probes (WhatsApp Web + Telegram + Discord + Google Chat + Slack + Signal).
*   Output includes per-agent session stores when multiple agents are configured.
*   Overview includes Gateway + node host service install/runtime status when available.
*   Overview includes update channel + git SHA (for source checkouts).
*   Update info surfaces in the Overview; if an update is available, status prints a hint to run `openclaw update` (see [Updating](https://docs.openclaw.ai/install/updating)).
*   Read-only status surfaces (`status`, `status --json`, `status --all`) resolve supported SecretRefs for their targeted config paths when possible.
*   If a supported channel SecretRef is configured but unavailable in the current command path, status stays read-only and reports degraded output instead of crashing. Human output shows warnings such as “configured token unavailable in this command path”, and JSON output includes `secretDiagnostics`.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/configure -->

# configure - OpenClaw

Interactive prompt to set up credentials, devices, and agent defaults. Note: The **Model** section now includes a multi-select for the `agents.defaults.models` allowlist (what shows up in `/model` and the model picker). Tip: `openclaw config` without a subcommand opens the same wizard. Use `openclaw config get|set|unset` for non-interactive edits. Related:

*   Gateway configuration reference: [Configuration](https://docs.openclaw.ai/gateway/configuration)
*   Config CLI: [Config](https://docs.openclaw.ai/cli/config)

Notes:

*   Choosing where the Gateway runs always updates `gateway.mode`. You can select “Continue” without other sections if that is all you need.
*   Channel-oriented services (Slack/Discord/Matrix/Microsoft Teams) prompt for channel/room allowlists during setup. You can enter names or IDs; the wizard resolves names to IDs when possible.
*   If you run the daemon install step, token auth requires a token, and `gateway.auth.token` is SecretRef-managed, configure validates the SecretRef but does not persist resolved plaintext token values into supervisor service environment metadata.
*   If token auth requires a token and the configured token SecretRef is unresolved, configure blocks daemon install with actionable remediation guidance.
*   If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, configure blocks daemon install until mode is set explicitly.

## Examples

```
openclaw configure
openclaw configure --section model --section channels
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/security -->

# security - OpenClaw

Security tools (audit + optional fixes). Related:

*   Security guide: [Security](https://docs.openclaw.ai/gateway/security)

## Audit

```
openclaw security audit
openclaw security audit --deep
openclaw security audit --fix
openclaw security audit --json
```

The audit warns when multiple DM senders share the main session and recommends **secure DM mode**: `session.dmScope="per-channel-peer"` (or `per-account-channel-peer` for multi-account channels) for shared inboxes. This is for cooperative/shared inbox hardening. A single Gateway shared by mutually untrusted/adversarial operators is not a recommended setup; split trust boundaries with separate gateways (or separate OS users/hosts). It also emits `security.trust_model.multi_user_heuristic` when config suggests likely shared-user ingress (for example open DM/group policy, configured group targets, or wildcard sender rules), and reminds you that OpenClaw is a personal-assistant trust model by default. For intentional shared-user setups, the audit guidance is to sandbox all sessions, keep filesystem access workspace-scoped, and keep personal/private identities or credentials off that runtime. It also warns when small models (`<=300B`) are used without sandboxing and with web/browser tools enabled. For webhook ingress, it warns when `hooks.defaultSessionKey` is unset, when request `sessionKey` overrides are enabled, and when overrides are enabled without `hooks.allowedSessionKeyPrefixes`. It also warns when sandbox Docker settings are configured while sandbox mode is off, when `gateway.nodes.denyCommands` uses ineffective pattern-like/unknown entries (exact node command-name matching only, not shell-text filtering), when `gateway.nodes.allowCommands` explicitly enables dangerous node commands, when global `tools.profile="minimal"` is overridden by agent tool profiles, when open groups expose runtime/filesystem tools without sandbox/workspace guards, and when installed extension plugin tools may be reachable under permissive tool policy. It also flags `gateway.allowRealIpFallback=true` (header-spoofing risk if proxies are misconfigured) and `discovery.mdns.mode="full"` (metadata leakage via mDNS TXT records). It also warns when sandbox browser uses Docker `bridge` network without `sandbox.browser.cdpSourceRange`. It also flags dangerous sandbox Docker network modes (including `host` and `container:*` namespace joins). It also warns when existing sandbox browser Docker containers have missing/stale hash labels (for example pre-migration containers missing `openclaw.browserConfigEpoch`) and recommends `openclaw sandbox recreate --browser --all`. It also warns when npm-based plugin/hook install records are unpinned, missing integrity metadata, or drift from currently installed package versions. It warns when channel allowlists rely on mutable names/emails/tags instead of stable IDs (Discord, Slack, Google Chat, MS Teams, Mattermost, IRC scopes where applicable). It warns when `gateway.auth.mode="none"` leaves Gateway HTTP APIs reachable without a shared secret (`/tools/invoke` plus any enabled `/v1/*` endpoint). Settings prefixed with `dangerous`/`dangerously` are explicit break-glass operator overrides; enabling one is not, by itself, a security vulnerability report. For the complete dangerous-parameter inventory, see the “Insecure or dangerous flags summary” section in [Security](https://docs.openclaw.ai/gateway/security).

## JSON output

Use `--json` for CI/policy checks:

```
openclaw security audit --json | jq '.summary'
openclaw security audit --deep --json | jq '.findings[] | select(.severity=="critical") | .checkId'
```

If `--fix` and `--json` are combined, output includes both fix actions and final report:

```
openclaw security audit --fix --json | jq '{fix: .fix.ok, summary: .report.summary}'
```

## What `--fix` changes

`--fix` applies safe, deterministic remediations:

*   flips common `groupPolicy="open"` to `groupPolicy="allowlist"` (including account variants in supported channels)
*   sets `logging.redactSensitive` from `"off"` to `"tools"`
*   tightens permissions for state/config and common sensitive files (`credentials/*.json`, `auth-profiles.json`, `sessions.json`, session `*.jsonl`)

`--fix` does **not**:

*   rotate tokens/passwords/API keys
*   disable tools (`gateway`, `cron`, `exec`, etc.)
*   change gateway bind/auth/network exposure choices
*   remove or rewrite plugins/skills

---

<!-- SOURCE: https://docs.openclaw.ai/cli/skills -->

# skills - OpenClaw

Inspect skills (bundled + workspace + managed overrides) and see what’s eligible vs missing requirements. Related:

*   Skills system: [Skills](https://docs.openclaw.ai/tools/skills)
*   Skills config: [Skills config](https://docs.openclaw.ai/tools/skills-config)
*   ClawHub installs: [ClawHub](https://docs.openclaw.ai/tools/clawhub)

## Commands

```
openclaw skills list
openclaw skills list --eligible
openclaw skills info <name>
openclaw skills check
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/cron -->

# cron - OpenClaw

Manage cron jobs for the Gateway scheduler. Related:

*   Cron jobs: [Cron jobs](https://docs.openclaw.ai/automation/cron-jobs)

Tip: run `openclaw cron --help` for the full command surface. Note: isolated `cron add` jobs default to `--announce` delivery. Use `--no-deliver` to keep output internal. `--deliver` remains as a deprecated alias for `--announce`. Note: one-shot (`--at`) jobs delete after success by default. Use `--keep-after-run` to keep them. Note: recurring jobs now use exponential retry backoff after consecutive errors (30s → 1m → 5m → 15m → 60m), then return to normal schedule after the next successful run. Note: `openclaw cron run` now returns as soon as the manual run is queued for execution. Successful responses include `{ ok: true, enqueued: true, runId }`; use `openclaw cron runs --id <job-id>` to follow the eventual outcome. Note: retention/pruning is controlled in config:

*   `cron.sessionRetention` (default `24h`) prunes completed isolated run sessions.
*   `cron.runLog.maxBytes` + `cron.runLog.keepLines` prune `~/.openclaw/cron/runs/<jobId>.jsonl`.

## Common edits

Update delivery settings without changing the message:

```
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"
```

Disable delivery for an isolated job:

```
openclaw cron edit <job-id> --no-deliver
```

Enable lightweight bootstrap context for an isolated job:

```
openclaw cron edit <job-id> --light-context
```

Announce to a specific channel:

```
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
```

Create an isolated job with lightweight bootstrap context:

```
openclaw cron add \
  --name "Lightweight morning brief" \
  --cron "0 7 * * *" \
  --session isolated \
  --message "Summarize overnight updates." \
  --light-context \
  --no-deliver
```

`--light-context` applies to isolated agent-turn jobs only. For cron runs, lightweight mode keeps bootstrap context empty instead of injecting the full workspace bootstrap set.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/dashboard -->

# dashboard - OpenClaw

Open the Control UI using your current auth.

```
openclaw dashboard
openclaw dashboard --no-open
```

Notes:

*   `dashboard` resolves configured `gateway.auth.token` SecretRefs when possible.
*   For SecretRef-managed tokens (resolved or unresolved), `dashboard` prints/copies/opens a non-tokenized URL to avoid exposing external secrets in terminal output, clipboard history, or browser-launch arguments.
*   If `gateway.auth.token` is SecretRef-managed but unresolved in this command path, the command prints a non-tokenized URL and explicit remediation guidance instead of embedding an invalid token placeholder.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/system -->

# system - OpenClaw

System-level helpers for the Gateway: enqueue system events, control heartbeats, and view presence.

## Common commands

```
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence
```

## `system event`

Enqueue a system event on the **main** session. The next heartbeat will inject it as a `System:` line in the prompt. Use `--mode now` to trigger the heartbeat immediately; `next-heartbeat` waits for the next scheduled tick. Flags:

*   `--text <text>`: required system event text.
*   `--mode <mode>`: `now` or `next-heartbeat` (default).
*   `--json`: machine-readable output.

## `system heartbeat last|enable|disable`

Heartbeat controls:

*   `last`: show the last heartbeat event.
*   `enable`: turn heartbeats back on (use this if they were disabled).
*   `disable`: pause heartbeats.

Flags:

*   `--json`: machine-readable output.

## `system presence`

List the current system presence entries the Gateway knows about (nodes, instances, and similar status lines). Flags:

*   `--json`: machine-readable output.

## Notes

*   Requires a running Gateway reachable by your current config (local or remote).
*   System events are ephemeral and not persisted across restarts.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/uninstall -->

# uninstall - OpenClaw

Uninstall the gateway service + local data (CLI remains).

```
openclaw backup create
openclaw uninstall
openclaw uninstall --all --yes
openclaw uninstall --dry-run
```

Run `openclaw backup create` first if you want a restorable snapshot before removing state or workspaces.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/directory -->

# directory - OpenClaw

Directory lookups for channels that support it (contacts/peers, groups, and “me”).

## Common flags

*   `--channel <name>`: channel id/alias (required when multiple channels are configured; auto when only one is configured)
*   `--account <id>`: account id (default: channel default)
*   `--json`: output JSON

## Notes

*   `directory` is meant to help you find IDs you can paste into other commands (especially `openclaw message send --target ...`).
*   For many channels, results are config-backed (allowlists / configured groups) rather than a live provider directory.
*   Default output is `id` (and sometimes `name`) separated by a tab; use `--json` for scripting.

## Using results with `message send`

```
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"
```

## ID formats (by channel)

*   WhatsApp: `+15551234567` (DM), `1234567890-1234567890@g.us` (group)
*   Telegram: `@username` or numeric chat id; groups are numeric ids
*   Slack: `user:U…` and `channel:C…`
*   Discord: `user:<id>` and `channel:<id>`
*   Matrix (plugin): `user:@user:server`, `room:!roomId:server`, or `#alias:server`
*   Microsoft Teams (plugin): `user:<id>` and `conversation:<id>`
*   Zalo (plugin): user id (Bot API)
*   Zalo Personal / `zalouser` (plugin): thread id (DM/group) from `zca` (`me`, `friend list`, `group list`)

## Self (“me”)

```
openclaw directory self --channel zalouser
```

```
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory peers list --channel zalouser --limit 50
```

## Groups

```
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/devices -->

# devices - OpenClaw

Manage device pairing requests and device-scoped tokens.

## Commands

### `openclaw devices list`

List pending pairing requests and paired devices.

```
openclaw devices list
openclaw devices list --json
```

### `openclaw devices remove <deviceId>`

Remove one paired device entry.

```
openclaw devices remove <deviceId>
openclaw devices remove <deviceId> --json
```

### `openclaw devices clear --yes [--pending]`

Clear paired devices in bulk.

```
openclaw devices clear --yes
openclaw devices clear --yes --pending
openclaw devices clear --yes --pending --json
```

### `openclaw devices approve [requestId] [--latest]`

Approve a pending device pairing request. If `requestId` is omitted, OpenClaw automatically approves the most recent pending request.

```
openclaw devices approve
openclaw devices approve <requestId>
openclaw devices approve --latest
```

### `openclaw devices reject <requestId>`

Reject a pending device pairing request.

```
openclaw devices reject <requestId>
```

### `openclaw devices rotate --device <id> --role <role> [--scope <scope...>]`

Rotate a device token for a specific role (optionally updating scopes).

```
openclaw devices rotate --device <deviceId> --role operator --scope operator.read --scope operator.write
```

### `openclaw devices revoke --device <id> --role <role>`

Revoke a device token for a specific role.

```
openclaw devices revoke --device <deviceId> --role node
```

## Common options

*   `--url <url>`: Gateway WebSocket URL (defaults to `gateway.remote.url` when configured).
*   `--token <token>`: Gateway token (if required).
*   `--password <password>`: Gateway password (password auth).
*   `--timeout <ms>`: RPC timeout.
*   `--json`: JSON output (recommended for scripting).

Note: when you set `--url`, the CLI does not fall back to config or environment credentials. Pass `--token` or `--password` explicitly. Missing explicit credentials is an error.

## Notes

*   Token rotation returns a new token (sensitive). Treat it like a secret.
*   These commands require `operator.pairing` (or `operator.admin`) scope.
*   `devices clear` is intentionally gated by `--yes`.
*   If pairing scope is unavailable on local loopback (and no explicit `--url` is passed), list/approve can use a local pairing fallback.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/config -->

# config - OpenClaw

Config helpers: get/set/unset/validate values by path and print the active config file. Run without a subcommand to open the configure wizard (same as `openclaw configure`).

## Examples

```
openclaw config file
openclaw config get browser.executablePath
openclaw config set browser.executablePath "/usr/bin/google-chrome"
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config set agents.list[0].tools.exec.node "node-id-or-name"
openclaw config unset tools.web.search.apiKey
openclaw config validate
openclaw config validate --json
```

## Paths

Paths use dot or bracket notation:

```
openclaw config get agents.defaults.workspace
openclaw config get agents.list[0].id
```

Use the agent list index to target a specific agent:

```
openclaw config get agents.list
openclaw config set agents.list[1].tools.exec.node "node-id-or-name"
```

## Values

Values are parsed as JSON5 when possible; otherwise they are treated as strings. Use `--strict-json` to require JSON5 parsing. `--json` remains supported as a legacy alias.

```
openclaw config set agents.defaults.heartbeat.every "0m"
openclaw config set gateway.port 19001 --strict-json
openclaw config set channels.whatsapp.groups '["*"]' --strict-json
```

## Subcommands

*   `config file`: Print the active config file path (resolved from `OPENCLAW_CONFIG_PATH` or default location).

Restart the gateway after edits.

## Validate

Validate the current config against the active schema without starting the gateway.

```
openclaw config validate
openclaw config validate --json
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/voicecall -->

# voicecall - OpenClaw

`voicecall` is a plugin-provided command. It only appears if the voice-call plugin is installed and enabled. Primary doc:

*   Voice-call plugin: [Voice Call](https://docs.openclaw.ai/plugins/voice-call)

## Common commands

```
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "Hello" --mode notify
openclaw voicecall continue --call-id <id> --message "Any questions?"
openclaw voicecall end --call-id <id>
```

## Exposing webhooks (Tailscale)

```
openclaw voicecall expose --mode serve
openclaw voicecall expose --mode funnel
openclaw voicecall expose --mode off
```

Security note: only expose the webhook endpoint to networks you trust. Prefer Tailscale Serve over Funnel when possible.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/daemon -->

# daemon - OpenClaw

Legacy alias for Gateway service management commands. `openclaw daemon ...` maps to the same service control surface as `openclaw gateway ...` service commands.

## Usage

```
openclaw daemon status
openclaw daemon install
openclaw daemon start
openclaw daemon stop
openclaw daemon restart
openclaw daemon uninstall
```

## Subcommands

*   `status`: show service install state and probe Gateway health
*   `install`: install service (`launchd`/`systemd`/`schtasks`)
*   `uninstall`: remove service
*   `start`: start service
*   `stop`: stop service
*   `restart`: restart service

## Common options

*   `status`: `--url`, `--token`, `--password`, `--timeout`, `--no-probe`, `--deep`, `--json`
*   `install`: `--port`, `--runtime <node|bun>`, `--token`, `--force`, `--json`
*   lifecycle (`uninstall|start|stop|restart`): `--json`

Notes:

*   `status` resolves configured auth SecretRefs for probe auth when possible.
*   On Linux systemd installs, `status` token-drift checks include both `Environment=` and `EnvironmentFile=` unit sources.
*   When token auth requires a token and `gateway.auth.token` is SecretRef-managed, `install` validates that the SecretRef is resolvable but does not persist the resolved token into service environment metadata.
*   If token auth requires a token and the configured token SecretRef is unresolved, install fails closed.
*   If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, install is blocked until mode is set explicitly.

## Prefer

Use [`openclaw gateway`](https://docs.openclaw.ai/cli/gateway) for current docs and examples.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/tui -->

# tui - OpenClaw

Open the terminal UI connected to the Gateway. Related:

*   TUI guide: [TUI](https://docs.openclaw.ai/web/tui)

Notes:

*   `tui` resolves configured gateway auth SecretRefs for token/password auth when possible (`env`/`file`/`exec` providers).
*   When launched from inside a configured agent workspace directory, TUI auto-selects that agent for the session key default (unless `--session` is explicitly `agent:<id>:...`).

## Examples

```
openclaw tui
openclaw tui --url ws://127.0.0.1:18789 --token <token>
openclaw tui --session main --deliver
# when run inside an agent workspace, infers that agent automatically
openclaw tui --session bugfix
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/update -->

# update - OpenClaw

Safely update OpenClaw and switch between stable/beta/dev channels. If you installed via **npm/pnpm** (global install, no git metadata), updates happen via the package manager flow in [Updating](https://docs.openclaw.ai/install/updating).

## Usage

```
openclaw update
openclaw update status
openclaw update wizard
openclaw update --channel beta
openclaw update --channel dev
openclaw update --tag beta
openclaw update --dry-run
openclaw update --no-restart
openclaw update --json
openclaw --update
```

## Options

*   `--no-restart`: skip restarting the Gateway service after a successful update.
*   `--channel <stable|beta|dev>`: set the update channel (git + npm; persisted in config).
*   `--tag <dist-tag|version>`: override the npm dist-tag or version for this update only.
*   `--dry-run`: preview planned update actions (channel/tag/target/restart flow) without writing config, installing, syncing plugins, or restarting.
*   `--json`: print machine-readable `UpdateRunResult` JSON.
*   `--timeout <seconds>`: per-step timeout (default is 1200s).

Note: downgrades require confirmation because older versions can break configuration.

## `update status`

Show the active update channel + git tag/branch/SHA (for source checkouts), plus update availability.

```
openclaw update status
openclaw update status --json
openclaw update status --timeout 10
```

Options:

*   `--json`: print machine-readable status JSON.
*   `--timeout <seconds>`: timeout for checks (default is 3s).

## `update wizard`

Interactive flow to pick an update channel and confirm whether to restart the Gateway after updating (default is to restart). If you select `dev` without a git checkout, it offers to create one.

## What it does

When you switch channels explicitly (`--channel ...`), OpenClaw also keeps the install method aligned:

*   `dev` → ensures a git checkout (default: `~/openclaw`, override with `OPENCLAW_GIT_DIR`), updates it, and installs the global CLI from that checkout.
*   `stable`/`beta` → installs from npm using the matching dist-tag.

The Gateway core auto-updater (when enabled via config) reuses this same update path.

## Git checkout flow

Channels:

*   `stable`: checkout the latest non-beta tag, then build + doctor.
*   `beta`: checkout the latest `-beta` tag, then build + doctor.
*   `dev`: checkout `main`, then fetch + rebase.

High-level:

1.  Requires a clean worktree (no uncommitted changes).
2.  Switches to the selected channel (tag or branch).
3.  Fetches upstream (dev only).
4.  Dev only: preflight lint + TypeScript build in a temp worktree; if the tip fails, walks back up to 10 commits to find the newest clean build.
5.  Rebases onto the selected commit (dev only).
6.  Installs deps (pnpm preferred; npm fallback).
7.  Builds + builds the Control UI.
8.  Runs `openclaw doctor` as the final “safe update” check.
9.  Syncs plugins to the active channel (dev uses bundled extensions; stable/beta uses npm) and updates npm-installed plugins.

## `--update` shorthand

`openclaw --update` rewrites to `openclaw update` (useful for shells and launcher scripts).

## See also

*   `openclaw doctor` (offers to run update first on git checkouts)
*   [Development channels](https://docs.openclaw.ai/install/development-channels)
*   [Updating](https://docs.openclaw.ai/install/updating)
*   [CLI reference](https://docs.openclaw.ai/cli)

---

<!-- SOURCE: https://docs.openclaw.ai/cli/doctor -->

# doctor - OpenClaw

Health checks + quick fixes for the gateway and channels. Related:

*   Troubleshooting: [Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
*   Security audit: [Security](https://docs.openclaw.ai/gateway/security)

## Examples

```
openclaw doctor
openclaw doctor --repair
openclaw doctor --deep
```

Notes:

*   Interactive prompts (like keychain/OAuth fixes) only run when stdin is a TTY and `--non-interactive` is **not** set. Headless runs (cron, Telegram, no terminal) will skip prompts.
*   `--fix` (alias for `--repair`) writes a backup to `~/.openclaw/openclaw.json.bak` and drops unknown config keys, listing each removal.
*   State integrity checks now detect orphan transcript files in the sessions directory and can archive them as `.deleted.<timestamp>` to reclaim space safely.
*   Doctor includes a memory-search readiness check and can recommend `openclaw configure --section model` when embedding credentials are missing.
*   If sandbox mode is enabled but Docker is unavailable, doctor reports a high-signal warning with remediation (`install Docker` or `openclaw config set agents.defaults.sandbox.mode off`).

## macOS: `launchctl` env overrides

If you previously ran `launchctl setenv OPENCLAW_GATEWAY_TOKEN ...` (or `...PASSWORD`), that value overrides your config file and can cause persistent “unauthorized” errors.

```
launchctl getenv OPENCLAW_GATEWAY_TOKEN
launchctl getenv OPENCLAW_GATEWAY_PASSWORD

launchctl unsetenv OPENCLAW_GATEWAY_TOKEN
launchctl unsetenv OPENCLAW_GATEWAY_PASSWORD
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/docs -->

# docs - OpenClaw

## `openclaw docs`

Search the live docs index.

```
openclaw docs browser extension
openclaw docs sandbox allowHostControl
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/webhooks -->

# webhooks - OpenClaw

Webhook helpers and integrations (Gmail Pub/Sub, webhook helpers). Related:

*   Webhooks: [Webhook](https://docs.openclaw.ai/automation/webhook)
*   Gmail Pub/Sub: [Gmail Pub/Sub](https://docs.openclaw.ai/automation/gmail-pubsub)

## Gmail

```
openclaw webhooks gmail setup --account you@example.com
openclaw webhooks gmail run
```

See [Gmail Pub/Sub documentation](https://docs.openclaw.ai/automation/gmail-pubsub) for details.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/gateway -->

# gateway - OpenClaw

## Gateway CLI

The Gateway is OpenClaw’s WebSocket server (channels, nodes, sessions, hooks). Subcommands in this page live under `openclaw gateway …`. Related docs:

*   [/gateway/bonjour](https://docs.openclaw.ai/gateway/bonjour)
*   [/gateway/discovery](https://docs.openclaw.ai/gateway/discovery)
*   [/gateway/configuration](https://docs.openclaw.ai/gateway/configuration)

## Run the Gateway

Run a local Gateway process:

Foreground alias:

Notes:

*   By default, the Gateway refuses to start unless `gateway.mode=local` is set in `~/.openclaw/openclaw.json`. Use `--allow-unconfigured` for ad-hoc/dev runs.
*   Binding beyond loopback without auth is blocked (safety guardrail).
*   `SIGUSR1` triggers an in-process restart when authorized (`commands.restart` is enabled by default; set `commands.restart: false` to block manual restart, while gateway tool/config apply/update remain allowed).
*   `SIGINT`/`SIGTERM` handlers stop the gateway process, but they don’t restore any custom terminal state. If you wrap the CLI with a TUI or raw-mode input, restore the terminal before exit.

### Options

*   `--port <port>`: WebSocket port (default comes from config/env; usually `18789`).
*   `--bind <loopback|lan|tailnet|auto|custom>`: listener bind mode.
*   `--auth <token|password>`: auth mode override.
*   `--token <token>`: token override (also sets `OPENCLAW_GATEWAY_TOKEN` for the process).
*   `--password <password>`: password override. Warning: inline passwords can be exposed in local process listings.
*   `--password-file <path>`: read the gateway password from a file.
*   `--tailscale <off|serve|funnel>`: expose the Gateway via Tailscale.
*   `--tailscale-reset-on-exit`: reset Tailscale serve/funnel config on shutdown.
*   `--allow-unconfigured`: allow gateway start without `gateway.mode=local` in config.
*   `--dev`: create a dev config + workspace if missing (skips BOOTSTRAP.md).
*   `--reset`: reset dev config + credentials + sessions + workspace (requires `--dev`).
*   `--force`: kill any existing listener on the selected port before starting.
*   `--verbose`: verbose logs.
*   `--claude-cli-logs`: only show claude-cli logs in the console (and enable its stdout/stderr).
*   `--ws-log <auto|full|compact>`: websocket log style (default `auto`).
*   `--compact`: alias for `--ws-log compact`.
*   `--raw-stream`: log raw model stream events to jsonl.
*   `--raw-stream-path <path>`: raw stream jsonl path.

## Query a running Gateway

All query commands use WebSocket RPC. Output modes:

*   Default: human-readable (colored in TTY).
*   `--json`: machine-readable JSON (no styling/spinner).
*   `--no-color` (or `NO_COLOR=1`): disable ANSI while keeping human layout.

Shared options (where supported):

*   `--url <url>`: Gateway WebSocket URL.
*   `--token <token>`: Gateway token.
*   `--password <password>`: Gateway password.
*   `--timeout <ms>`: timeout/budget (varies per command).
*   `--expect-final`: wait for a “final” response (agent calls).

Note: when you set `--url`, the CLI does not fall back to config or environment credentials. Pass `--token` or `--password` explicitly. Missing explicit credentials is an error.

### `gateway health`

```
openclaw gateway health --url ws://127.0.0.1:18789
```

### `gateway status`

`gateway status` shows the Gateway service (launchd/systemd/schtasks) plus an optional RPC probe.

```
openclaw gateway status
openclaw gateway status --json
```

Options:

*   `--url <url>`: override the probe URL.
*   `--token <token>`: token auth for the probe.
*   `--password <password>`: password auth for the probe.
*   `--timeout <ms>`: probe timeout (default `10000`).
*   `--no-probe`: skip the RPC probe (service-only view).
*   `--deep`: scan system-level services too.

Notes:

*   `gateway status` resolves configured auth SecretRefs for probe auth when possible.
*   If a required auth SecretRef is unresolved in this command path, probe auth can fail; pass `--token`/`--password` explicitly or resolve the secret source first.
*   On Linux systemd installs, service auth drift checks read both `Environment=` and `EnvironmentFile=` values from the unit (including `%h`, quoted paths, multiple files, and optional `-` files).

### `gateway probe`

`gateway probe` is the “debug everything” command. It always probes:

*   your configured remote gateway (if set), and
*   localhost (loopback) **even if remote is configured**.

If multiple gateways are reachable, it prints all of them. Multiple gateways are supported when you use isolated profiles/ports (e.g., a rescue bot), but most installs still run a single gateway.

```
openclaw gateway probe
openclaw gateway probe --json
```

#### Remote over SSH (Mac app parity)

The macOS app “Remote over SSH” mode uses a local port-forward so the remote gateway (which may be bound to loopback only) becomes reachable at `ws://127.0.0.1:<port>`. CLI equivalent:

```
openclaw gateway probe --ssh user@gateway-host
```

Options:

*   `--ssh <target>`: `user@host` or `user@host:port` (port defaults to `22`).
*   `--ssh-identity <path>`: identity file.
*   `--ssh-auto`: pick the first discovered gateway host as SSH target (LAN/WAB only).

Config (optional, used as defaults):

*   `gateway.remote.sshTarget`
*   `gateway.remote.sshIdentity`

### `gateway call <method>`

Low-level RPC helper.

```
openclaw gateway call status
openclaw gateway call logs.tail --params '{"sinceMs": 60000}'
```

## Manage the Gateway service

```
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall
```

Notes:

*   `gateway install` supports `--port`, `--runtime`, `--token`, `--force`, `--json`.
*   When token auth requires a token and `gateway.auth.token` is SecretRef-managed, `gateway install` validates that the SecretRef is resolvable but does not persist the resolved token into service environment metadata.
*   If token auth requires a token and the configured token SecretRef is unresolved, install fails closed instead of persisting fallback plaintext.
*   For password auth on `gateway run`, prefer `OPENCLAW_GATEWAY_PASSWORD`, `--password-file`, or a SecretRef-backed `gateway.auth.password` over inline `--password`.
*   In inferred auth mode, shell-only `OPENCLAW_GATEWAY_PASSWORD`/`CLAWDBOT_GATEWAY_PASSWORD` does not relax install token requirements; use durable config (`gateway.auth.password` or config `env`) when installing a managed service.
*   If both `gateway.auth.token` and `gateway.auth.password` are configured and `gateway.auth.mode` is unset, install is blocked until mode is set explicitly.
*   Lifecycle commands accept `--json` for scripting.

## Discover gateways (Bonjour)

`gateway discover` scans for Gateway beacons (`_openclaw-gw._tcp`).

*   Multicast DNS-SD: `local.`
*   Unicast DNS-SD (Wide-Area Bonjour): choose a domain (example: `openclaw.internal.`) and set up split DNS + a DNS server; see [/gateway/bonjour](https://docs.openclaw.ai/gateway/bonjour)

Only gateways with Bonjour discovery enabled (default) advertise the beacon. Wide-Area discovery records include (TXT):

*   `role` (gateway role hint)
*   `transport` (transport hint, e.g. `gateway`)
*   `gatewayPort` (WebSocket port, usually `18789`)
*   `sshPort` (SSH port; defaults to `22` if not present)
*   `tailnetDns` (MagicDNS hostname, when available)
*   `gatewayTls` / `gatewayTlsSha256` (TLS enabled + cert fingerprint)
*   `cliPath` (optional hint for remote installs)

### `gateway discover`

```
openclaw gateway discover
```

Options:

*   `--timeout <ms>`: per-command timeout (browse/resolve); default `2000`.
*   `--json`: machine-readable output (also disables styling/spinner).

Examples:

```
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq '.beacons[].wsUrl'
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/health -->

# health - OpenClaw

Fetch health from the running Gateway.

```
openclaw health
openclaw health --json
openclaw health --verbose
```

Notes:

*   `--verbose` runs live probes and prints per-account timings when multiple accounts are configured.
*   Output includes per-agent session stores when multiple agents are configured.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/dns -->

# dns - OpenClaw

DNS helpers for wide-area discovery (Tailscale + CoreDNS). Currently focused on macOS + Homebrew CoreDNS. Related:

*   Gateway discovery: [Discovery](https://docs.openclaw.ai/gateway/discovery)
*   Wide-area discovery config: [Configuration](https://docs.openclaw.ai/gateway/configuration)

## Setup

```
openclaw dns setup
openclaw dns setup --apply
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/hooks -->

# hooks - OpenClaw

Manage agent hooks (event-driven automations for commands like `/new`, `/reset`, and gateway startup). Related:

*   Hooks: [Hooks](https://docs.openclaw.ai/automation/hooks)
*   Plugin hooks: [Plugins](https://docs.openclaw.ai/tools/plugin#plugin-hooks)

## List All Hooks

List all discovered hooks from workspace, managed, and bundled directories. **Options:**

*   `--eligible`: Show only eligible hooks (requirements met)
*   `--json`: Output as JSON
*   `-v, --verbose`: Show detailed information including missing requirements

**Example output:**

```
Hooks (4/4 ready)

Ready:
  🚀 boot-md ✓ - Run BOOT.md on gateway startup
  📎 bootstrap-extra-files ✓ - Inject extra workspace bootstrap files during agent bootstrap
  📝 command-logger ✓ - Log all command events to a centralized audit file
  💾 session-memory ✓ - Save session context to memory when /new command is issued
```

**Example (verbose):**

```
openclaw hooks list --verbose
```

Shows missing requirements for ineligible hooks. **Example (JSON):**

```
openclaw hooks list --json
```

Returns structured JSON for programmatic use.

## Get Hook Information

```
openclaw hooks info <name>
```

Show detailed information about a specific hook. **Arguments:**

*   `<name>`: Hook name (e.g., `session-memory`)

**Options:**

*   `--json`: Output as JSON

**Example:**

```
openclaw hooks info session-memory
```

**Output:**

```
💾 session-memory ✓ Ready

Save session context to memory when /new command is issued

Details:
  Source: openclaw-bundled
  Path: /path/to/openclaw/hooks/bundled/session-memory/HOOK.md
  Handler: /path/to/openclaw/hooks/bundled/session-memory/handler.ts
  Homepage: https://docs.openclaw.ai/automation/hooks#session-memory
  Events: command:new

Requirements:
  Config: ✓ workspace.dir
```

## Check Hooks Eligibility

Show summary of hook eligibility status (how many are ready vs. not ready). **Options:**

*   `--json`: Output as JSON

**Example output:**

```
Hooks Status

Total hooks: 4
Ready: 4
Not ready: 0
```

## Enable a Hook

```
openclaw hooks enable <name>
```

Enable a specific hook by adding it to your config (`~/.openclaw/config.json`). **Note:** Hooks managed by plugins show `plugin:<id>` in `openclaw hooks list` and can’t be enabled/disabled here. Enable/disable the plugin instead. **Arguments:**

*   `<name>`: Hook name (e.g., `session-memory`)

**Example:**

```
openclaw hooks enable session-memory
```

**Output:**

```
✓ Enabled hook: 💾 session-memory
```

**What it does:**

*   Checks if hook exists and is eligible
*   Updates `hooks.internal.entries.<name>.enabled = true` in your config
*   Saves config to disk

**After enabling:**

*   Restart the gateway so hooks reload (menu bar app restart on macOS, or restart your gateway process in dev).

## Disable a Hook

```
openclaw hooks disable <name>
```

Disable a specific hook by updating your config. **Arguments:**

*   `<name>`: Hook name (e.g., `command-logger`)

**Example:**

```
openclaw hooks disable command-logger
```

**Output:**

```
⏸ Disabled hook: 📝 command-logger
```

**After disabling:**

*   Restart the gateway so hooks reload

## Install Hooks

```
openclaw hooks install <path-or-spec>
openclaw hooks install <npm-spec> --pin
```

Install a hook pack from a local folder/archive or npm. Npm specs are **registry-only** (package name + optional **exact version** or **dist-tag**). Git/URL/file specs and semver ranges are rejected. Dependency installs run with `--ignore-scripts` for safety. Bare specs and `@latest` stay on the stable track. If npm resolves either of those to a prerelease, OpenClaw stops and asks you to opt in explicitly with a prerelease tag such as `@beta`/`@rc` or an exact prerelease version. **What it does:**

*   Copies the hook pack into `~/.openclaw/hooks/<id>`
*   Enables the installed hooks in `hooks.internal.entries.*`
*   Records the install under `hooks.internal.installs`

**Options:**

*   `-l, --link`: Link a local directory instead of copying (adds it to `hooks.internal.load.extraDirs`)
*   `--pin`: Record npm installs as exact resolved `name@version` in `hooks.internal.installs`

**Supported archives:** `.zip`, `.tgz`, `.tar.gz`, `.tar` **Examples:**

```
# Local directory
openclaw hooks install ./my-hook-pack

# Local archive
openclaw hooks install ./my-hook-pack.zip

# NPM package
openclaw hooks install @openclaw/my-hook-pack

# Link a local directory without copying
openclaw hooks install -l ./my-hook-pack
```

## Update Hooks

```
openclaw hooks update <id>
openclaw hooks update --all
```

Update installed hook packs (npm installs only). **Options:**

*   `--all`: Update all tracked hook packs
*   `--dry-run`: Show what would change without writing

When a stored integrity hash exists and the fetched artifact hash changes, OpenClaw prints a warning and asks for confirmation before proceeding. Use global `--yes` to bypass prompts in CI/non-interactive runs.

## Bundled Hooks

### session-memory

Saves session context to memory when you issue `/new`. **Enable:**

```
openclaw hooks enable session-memory
```

**Output:** `~/.openclaw/workspace/memory/YYYY-MM-DD-slug.md` **See:** [session-memory documentation](https://docs.openclaw.ai/automation/hooks#session-memory)

Injects additional bootstrap files (for example monorepo-local `AGENTS.md` / `TOOLS.md`) during `agent:bootstrap`. **Enable:**

```
openclaw hooks enable bootstrap-extra-files
```

**See:** [bootstrap-extra-files documentation](https://docs.openclaw.ai/automation/hooks#bootstrap-extra-files)

### command-logger

Logs all command events to a centralized audit file. **Enable:**

```
openclaw hooks enable command-logger
```

**Output:** `~/.openclaw/logs/commands.log` **View logs:**

```
# Recent commands
tail -n 20 ~/.openclaw/logs/commands.log

# Pretty-print
cat ~/.openclaw/logs/commands.log | jq .

# Filter by action
grep '"action":"new"' ~/.openclaw/logs/commands.log | jq .
```

**See:** [command-logger documentation](https://docs.openclaw.ai/automation/hooks#command-logger)

### boot-md

Runs `BOOT.md` when the gateway starts (after channels start). **Events**: `gateway:startup` **Enable**:

```
openclaw hooks enable boot-md
```

**See:** [boot-md documentation](https://docs.openclaw.ai/automation/hooks#boot-md)

---

<!-- SOURCE: https://docs.openclaw.ai/cli/logs -->

# logs - OpenClaw

Tail Gateway file logs over RPC (works in remote mode). Related:

*   Logging overview: [Logging](https://docs.openclaw.ai/logging)

## Examples

```
openclaw logs
openclaw logs --follow
openclaw logs --json
openclaw logs --limit 500
openclaw logs --local-time
openclaw logs --follow --local-time
```

Use `--local-time` to render timestamps in your local timezone.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/message -->

# message - OpenClaw

Single outbound command for sending messages and channel actions (Discord/Google Chat/Slack/Mattermost (plugin)/Telegram/WhatsApp/Signal/iMessage/MS Teams).

## Usage

```
openclaw message <subcommand> [flags]
```

Channel selection:

*   `--channel` required if more than one channel is configured.
*   If exactly one channel is configured, it becomes the default.
*   Values: `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams` (Mattermost requires plugin)

Target formats (`--target`):

*   WhatsApp: E.164 or group JID
*   Telegram: chat id or `@username`
*   Discord: `channel:<id>` or `user:<id>` (or `<@id>` mention; raw numeric ids are treated as channels)
*   Google Chat: `spaces/<spaceId>` or `users/<userId>`
*   Slack: `channel:<id>` or `user:<id>` (raw channel id is accepted)
*   Mattermost (plugin): `channel:<id>`, `user:<id>`, or `@username` (bare ids are treated as channels)
*   Signal: `+E.164`, `group:<id>`, `signal:+E.164`, `signal:group:<id>`, or `username:<name>`/`u:<name>`
*   iMessage: handle, `chat_id:<id>`, `chat_guid:<guid>`, or `chat_identifier:<id>`
*   MS Teams: conversation id (`19:...@thread.tacv2`) or `conversation:<id>` or `user:<aad-object-id>`

Name lookup:

*   For supported providers (Discord/Slack/etc), channel names like `Help` or `#help` are resolved via the directory cache.
*   On cache miss, OpenClaw will attempt a live directory lookup when the provider supports it.

## Common flags

*   `--channel <name>`
*   `--account <id>`
*   `--target <dest>` (target channel or user for send/poll/read/etc)
*   `--targets <name>` (repeat; broadcast only)
*   `--json`
*   `--dry-run`
*   `--verbose`

## Actions

### Core

*   `send`
    *   Channels: WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams
    *   Required: `--target`, plus `--message` or `--media`
    *   Optional: `--media`, `--reply-to`, `--thread-id`, `--gif-playback`
    *   Telegram only: `--buttons` (requires `channels.telegram.capabilities.inlineButtons` to allow it)
    *   Telegram only: `--thread-id` (forum topic id)
    *   Slack only: `--thread-id` (thread timestamp; `--reply-to` uses the same field)
    *   WhatsApp only: `--gif-playback`
*   `poll`
    *   Channels: WhatsApp/Telegram/Discord/Matrix/MS Teams
    *   Required: `--target`, `--poll-question`, `--poll-option` (repeat)
    *   Optional: `--poll-multi`
    *   Discord only: `--poll-duration-hours`, `--silent`, `--message`
    *   Telegram only: `--poll-duration-seconds` (5-600), `--silent`, `--poll-anonymous` / `--poll-public`, `--thread-id`
*   `react`
    *   Channels: Discord/Google Chat/Slack/Telegram/WhatsApp/Signal
    *   Required: `--message-id`, `--target`
    *   Optional: `--emoji`, `--remove`, `--participant`, `--from-me`, `--target-author`, `--target-author-uuid`
    *   Note: `--remove` requires `--emoji` (omit `--emoji` to clear own reactions where supported; see /tools/reactions)
    *   WhatsApp only: `--participant`, `--from-me`
    *   Signal group reactions: `--target-author` or `--target-author-uuid` required
*   `reactions`
    *   Channels: Discord/Google Chat/Slack
    *   Required: `--message-id`, `--target`
    *   Optional: `--limit`
*   `read`
    *   Channels: Discord/Slack
    *   Required: `--target`
    *   Optional: `--limit`, `--before`, `--after`
    *   Discord only: `--around`
*   `edit`
    *   Channels: Discord/Slack
    *   Required: `--message-id`, `--message`, `--target`
*   `delete`
    *   Channels: Discord/Slack/Telegram
    *   Required: `--message-id`, `--target`
*   `pin` / `unpin`
    *   Channels: Discord/Slack
    *   Required: `--message-id`, `--target`
*   `pins` (list)
    *   Channels: Discord/Slack
    *   Required: `--target`
*   `permissions`
    *   Channels: Discord
    *   Required: `--target`
*   `search`
    *   Channels: Discord
    *   Required: `--guild-id`, `--query`
    *   Optional: `--channel-id`, `--channel-ids` (repeat), `--author-id`, `--author-ids` (repeat), `--limit`

### Threads

*   `thread create`
    *   Channels: Discord
    *   Required: `--thread-name`, `--target` (channel id)
    *   Optional: `--message-id`, `--message`, `--auto-archive-min`
*   `thread list`
    *   Channels: Discord
    *   Required: `--guild-id`
    *   Optional: `--channel-id`, `--include-archived`, `--before`, `--limit`
*   `thread reply`
    *   Channels: Discord
    *   Required: `--target` (thread id), `--message`
    *   Optional: `--media`, `--reply-to`

### Emojis

*   `emoji list`
    *   Discord: `--guild-id`
    *   Slack: no extra flags
*   `emoji upload`
    *   Channels: Discord
    *   Required: `--guild-id`, `--emoji-name`, `--media`
    *   Optional: `--role-ids` (repeat)

### Stickers

*   `sticker send`
    *   Channels: Discord
    *   Required: `--target`, `--sticker-id` (repeat)
    *   Optional: `--message`
*   `sticker upload`
    *   Channels: Discord
    *   Required: `--guild-id`, `--sticker-name`, `--sticker-desc`, `--sticker-tags`, `--media`

### Roles / Channels / Members / Voice

*   `role info` (Discord): `--guild-id`
*   `role add` / `role remove` (Discord): `--guild-id`, `--user-id`, `--role-id`
*   `channel info` (Discord): `--target`
*   `channel list` (Discord): `--guild-id`
*   `member info` (Discord/Slack): `--user-id` (+ `--guild-id` for Discord)
*   `voice status` (Discord): `--guild-id`, `--user-id`

### Events

*   `event list` (Discord): `--guild-id`
*   `event create` (Discord): `--guild-id`, `--event-name`, `--start-time`
    *   Optional: `--end-time`, `--desc`, `--channel-id`, `--location`, `--event-type`

### Moderation (Discord)

*   `timeout`: `--guild-id`, `--user-id` (optional `--duration-min` or `--until`; omit both to clear timeout)
*   `kick`: `--guild-id`, `--user-id` (+ `--reason`)
*   `ban`: `--guild-id`, `--user-id` (+ `--delete-days`, `--reason`)
    *   `timeout` also supports `--reason`

### Broadcast

*   `broadcast`
    *   Channels: any configured channel; use `--channel all` to target all providers
    *   Required: `--targets` (repeat)
    *   Optional: `--message`, `--media`, `--dry-run`

## Examples

Send a Discord reply:

```
openclaw message send --channel discord \
  --target channel:123 --message "hi" --reply-to 456
```

Send a Discord message with components:

```
openclaw message send --channel discord \
  --target channel:123 --message "Choose:" \
  --components '{"text":"Choose a path","blocks":[{"type":"actions","buttons":[{"label":"Approve","style":"success"},{"label":"Decline","style":"danger"}]}]}'
```

See [Discord components](https://docs.openclaw.ai/channels/discord#interactive-components) for the full schema. Create a Discord poll:

```
openclaw message poll --channel discord \
  --target channel:123 \
  --poll-question "Snack?" \
  --poll-option Pizza --poll-option Sushi \
  --poll-multi --poll-duration-hours 48
```

Create a Telegram poll (auto-close in 2 minutes):

```
openclaw message poll --channel telegram \
  --target @mychat \
  --poll-question "Lunch?" \
  --poll-option Pizza --poll-option Sushi \
  --poll-duration-seconds 120 --silent
```

Send a Teams proactive message:

```
openclaw message send --channel msteams \
  --target conversation:19:abc@thread.tacv2 --message "hi"
```

Create a Teams poll:

```
openclaw message poll --channel msteams \
  --target conversation:19:abc@thread.tacv2 \
  --poll-question "Lunch?" \
  --poll-option Pizza --poll-option Sushi
```

React in Slack:

```
openclaw message react --channel slack \
  --target C123 --message-id 456 --emoji "✅"
```

React in a Signal group:

```
openclaw message react --channel signal \
  --target signal:group:abc123 --message-id 1737630212345 \
  --emoji "✅" --target-author-uuid 123e4567-e89b-12d3-a456-426614174000
```

Send Telegram inline buttons:

```
openclaw message send --channel telegram --target @mychat --message "Choose:" \
  --buttons '[ [{"text":"Yes","callback_data":"cmd:yes"}], [{"text":"No","callback_data":"cmd:no"}] ]'
```

---

<!-- SOURCE: https://docs.openclaw.ai/cli/memory -->

# memory - OpenClaw

Manage semantic memory indexing and search. Provided by the active memory plugin (default: `memory-core`; set `plugins.slots.memory = "none"` to disable). Related:

*   Memory concept: [Memory](https://docs.openclaw.ai/concepts/memory)
*   Plugins: [Plugins](https://docs.openclaw.ai/tools/plugin)

## Examples

```
openclaw memory status
openclaw memory status --deep
openclaw memory index --force
openclaw memory search "meeting notes"
openclaw memory search --query "deployment" --max-results 20
openclaw memory status --json
openclaw memory status --deep --index
openclaw memory status --deep --index --verbose
openclaw memory status --agent main
openclaw memory index --agent main --verbose
```

## Options

`memory status` and `memory index`:

*   `--agent <id>`: scope to a single agent. Without it, these commands run for each configured agent; if no agent list is configured, they fall back to the default agent.
*   `--verbose`: emit detailed logs during probes and indexing.

`memory status`:

*   `--deep`: probe vector + embedding availability.
*   `--index`: run a reindex if the store is dirty (implies `--deep`).
*   `--json`: print JSON output.

`memory index`:

*   `--force`: force a full reindex.

`memory search`:

*   Query input: pass either positional `[query]` or `--query <text>`.
*   If both are provided, `--query` wins.
*   If neither is provided, the command exits with an error.
*   `--agent <id>`: scope to a single agent (default: the default agent).
*   `--max-results <n>`: limit the number of results returned.
*   `--min-score <n>`: filter out low-score matches.
*   `--json`: print JSON results.

Notes:

*   `memory index --verbose` prints per-phase details (provider, model, sources, batch activity).
*   `memory status` includes any extra paths configured via `memorySearch.extraPaths`.
*   If effectively active memory remote API key fields are configured as SecretRefs, the command resolves those values from the active gateway snapshot. If gateway is unavailable, the command fails fast.
*   Gateway version skew note: this command path requires a gateway that supports `secrets.resolve`; older gateways return an unknown-method error.

---

<!-- SOURCE: https://docs.openclaw.ai/cli/models -->

# models - OpenClaw

Model discovery, scanning, and configuration (default model, fallbacks, auth profiles). Related:

*   Providers + models: [Models](https://docs.openclaw.ai/providers/models)
*   Provider auth setup: [Getting started](https://docs.openclaw.ai/start/getting-started)

## Common commands

```
openclaw models status
openclaw models list
openclaw models set <model-or-alias>
openclaw models scan
```

`openclaw models status` shows the resolved default/fallbacks plus an auth overview. When provider usage snapshots are available, the OAuth/token status section includes provider usage headers. Add `--probe` to run live auth probes against each configured provider profile. Probes are real requests (may consume tokens and trigger rate limits). Use `--agent <id>` to inspect a configured agent’s model/auth state. When omitted, the command uses `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR` if set, otherwise the configured default agent. Notes:

*   `models set <model-or-alias>` accepts `provider/model` or an alias.
*   Model refs are parsed by splitting on the **first** `/`. If the model ID includes `/` (OpenRouter-style), include the provider prefix (example: `openrouter/moonshotai/kimi-k2`).
*   If you omit the provider, OpenClaw treats the input as an alias or a model for the **default provider** (only works when there is no `/` in the model ID).
*   `models status` may show `marker(<value>)` in auth output for non-secret placeholders (for example `OPENAI_API_KEY`, `secretref-managed`, `minimax-oauth`, `qwen-oauth`, `ollama-local`) instead of masking them as secrets.

### `models status`

Options:

*   `--json`
*   `--plain`
*   `--check` (exit 1=expired/missing, 2=expiring)
*   `--probe` (live probe of configured auth profiles)
*   `--probe-provider <name>` (probe one provider)
*   `--probe-profile <id>` (repeat or comma-separated profile ids)
*   `--probe-timeout <ms>`
*   `--probe-concurrency <n>`
*   `--probe-max-tokens <n>`
*   `--agent <id>` (configured agent id; overrides `OPENCLAW_AGENT_DIR`/`PI_CODING_AGENT_DIR`)

## Aliases + fallbacks

```
openclaw models aliases list
openclaw models fallbacks list
```

## Auth profiles

```
openclaw models auth add
openclaw models auth login --provider <id>
openclaw models auth setup-token
openclaw models auth paste-token
```

`models auth login` runs a provider plugin’s auth flow (OAuth/API key). Use `openclaw plugins list` to see which providers are installed. Notes:

*   `setup-token` prompts for a setup-token value (generate it with `claude setup-token` on any machine).
*   `paste-token` accepts a token string generated elsewhere or from automation.
*   Anthropic policy note: setup-token support is technical compatibility. Anthropic has blocked some subscription usage outside Claude Code in the past, so verify current terms before using it broadly.

---

<!-- SOURCE: https://docs.openclaw.ai/cli -->

# CLI Reference - OpenClaw

This page describes the current CLI behavior. If commands change, update this doc.

## Command pages

*   [`setup`](https://docs.openclaw.ai/cli/setup)
*   [`onboard`](https://docs.openclaw.ai/cli/onboard)
*   [`configure`](https://docs.openclaw.ai/cli/configure)
*   [`config`](https://docs.openclaw.ai/cli/config)
*   [`completion`](https://docs.openclaw.ai/cli/completion)
*   [`doctor`](https://docs.openclaw.ai/cli/doctor)
*   [`dashboard`](https://docs.openclaw.ai/cli/dashboard)
*   [`backup`](https://docs.openclaw.ai/cli/backup)
*   [`reset`](https://docs.openclaw.ai/cli/reset)
*   [`uninstall`](https://docs.openclaw.ai/cli/uninstall)
*   [`update`](https://docs.openclaw.ai/cli/update)
*   [`message`](https://docs.openclaw.ai/cli/message)
*   [`agent`](https://docs.openclaw.ai/cli/agent)
*   [`agents`](https://docs.openclaw.ai/cli/agents)
*   [`acp`](https://docs.openclaw.ai/cli/acp)
*   [`status`](https://docs.openclaw.ai/cli/status)
*   [`health`](https://docs.openclaw.ai/cli/health)
*   [`sessions`](https://docs.openclaw.ai/cli/sessions)
*   [`gateway`](https://docs.openclaw.ai/cli/gateway)
*   [`logs`](https://docs.openclaw.ai/cli/logs)
*   [`system`](https://docs.openclaw.ai/cli/system)
*   [`models`](https://docs.openclaw.ai/cli/models)
*   [`memory`](https://docs.openclaw.ai/cli/memory)
*   [`directory`](https://docs.openclaw.ai/cli/directory)
*   [`nodes`](https://docs.openclaw.ai/cli/nodes)
*   [`devices`](https://docs.openclaw.ai/cli/devices)
*   [`node`](https://docs.openclaw.ai/cli/node)
*   [`approvals`](https://docs.openclaw.ai/cli/approvals)
*   [`sandbox`](https://docs.openclaw.ai/cli/sandbox)
*   [`tui`](https://docs.openclaw.ai/cli/tui)
*   [`browser`](https://docs.openclaw.ai/cli/browser)
*   [`cron`](https://docs.openclaw.ai/cli/cron)
*   [`dns`](https://docs.openclaw.ai/cli/dns)
*   [`docs`](https://docs.openclaw.ai/cli/docs)
*   [`hooks`](https://docs.openclaw.ai/cli/hooks)
*   [`webhooks`](https://docs.openclaw.ai/cli/webhooks)
*   [`pairing`](https://docs.openclaw.ai/cli/pairing)
*   [`qr`](https://docs.openclaw.ai/cli/qr)
*   [`plugins`](https://docs.openclaw.ai/cli/plugins) (plugin commands)
*   [`channels`](https://docs.openclaw.ai/cli/channels)
*   [`security`](https://docs.openclaw.ai/cli/security)
*   [`secrets`](https://docs.openclaw.ai/cli/secrets)
*   [`skills`](https://docs.openclaw.ai/cli/skills)
*   [`daemon`](https://docs.openclaw.ai/cli/daemon) (legacy alias for gateway service commands)
*   [`clawbot`](https://docs.openclaw.ai/cli/clawbot) (legacy alias namespace)
*   [`voicecall`](https://docs.openclaw.ai/cli/voicecall) (plugin; if installed)

## Global flags

*   `--dev`: isolate state under `~/.openclaw-dev` and shift default ports.
*   `--profile <name>`: isolate state under `~/.openclaw-<name>`.
*   `--no-color`: disable ANSI colors.
*   `--update`: shorthand for `openclaw update` (source installs only).
*   `-V`, `--version`, `-v`: print version and exit.

## Output styling

*   ANSI colors and progress indicators only render in TTY sessions.
*   OSC-8 hyperlinks render as clickable links in supported terminals; otherwise we fall back to plain URLs.
*   `--json` (and `--plain` where supported) disables styling for clean output.
*   `--no-color` disables ANSI styling; `NO_COLOR=1` is also respected.
*   Long-running commands show a progress indicator (OSC 9;4 when supported).

## Color palette

OpenClaw uses a lobster palette for CLI output.

*   `accent` (#FF5A2D): headings, labels, primary highlights.
*   `accentBright` (#FF7A3D): command names, emphasis.
*   `accentDim` (#D14A22): secondary highlight text.
*   `info` (#FF8A5B): informational values.
*   `success` (#2FBF71): success states.
*   `warn` (#FFB020): warnings, fallbacks, attention.
*   `error` (#E23D2D): errors, failures.
*   `muted` (#8B7F77): de-emphasis, metadata.

Palette source of truth: `src/terminal/palette.ts` (aka “lobster seam”).

## Command tree

```
openclaw [--dev] [--profile <name>] <command>
  setup
  onboard
  configure
  config
    get
    set
    unset
  completion
  doctor
  dashboard
  backup
    create
    verify
  security
    audit
  secrets
    reload
    migrate
  reset
  uninstall
  update
  channels
    list
    status
    logs
    add
    remove
    login
    logout
  directory
  skills
    list
    info
    check
  plugins
    list
    info
    install
    enable
    disable
    doctor
  memory
    status
    index
    search
  message
  agent
  agents
    list
    add
    delete
  acp
  status
  health
  sessions
  gateway
    call
    health
    status
    probe
    discover
    install
    uninstall
    start
    stop
    restart
    run
  daemon
    status
    install
    uninstall
    start
    stop
    restart
  logs
  system
    event
    heartbeat last|enable|disable
    presence
  models
    list
    status
    set
    set-image
    aliases list|add|remove
    fallbacks list|add|remove|clear
    image-fallbacks list|add|remove|clear
    scan
    auth add|setup-token|paste-token
    auth order get|set|clear
  sandbox
    list
    recreate
    explain
  cron
    status
    list
    add
    edit
    rm
    enable
    disable
    runs
    run
  nodes
  devices
  node
    run
    status
    install
    uninstall
    start
    stop
    restart
  approvals
    get
    set
    allowlist add|remove
  browser
    status
    start
    stop
    reset-profile
    tabs
    open
    focus
    close
    profiles
    create-profile
    delete-profile
    screenshot
    snapshot
    navigate
    resize
    click
    type
    press
    hover
    drag
    select
    upload
    fill
    dialog
    wait
    evaluate
    console
    pdf
  hooks
    list
    info
    check
    enable
    disable
    install
    update
  webhooks
    gmail setup|run
  pairing
    list
    approve
  qr
  clawbot
    qr
  docs
  dns
    setup
  tui
```

Note: plugins can add additional top-level commands (for example `openclaw voicecall`).

## Security

*   `openclaw security audit` — audit config + local state for common security foot-guns.
*   `openclaw security audit --deep` — best-effort live Gateway probe.
*   `openclaw security audit --fix` — tighten safe defaults and chmod state/config.

## Secrets

*   `openclaw secrets reload` — re-resolve refs and atomically swap the runtime snapshot.
*   `openclaw secrets audit` — scan for plaintext residues, unresolved refs, and precedence drift.
*   `openclaw secrets configure` — interactive helper for provider setup + SecretRef mapping + preflight/apply.
*   `openclaw secrets apply --from <plan.json>` — apply a previously generated plan (`--dry-run` supported).

## Plugins

Manage extensions and their config:

*   `openclaw plugins list` — discover plugins (use `--json` for machine output).
*   `openclaw plugins info <id>` — show details for a plugin.
*   `openclaw plugins install <path|.tgz|npm-spec>` — install a plugin (or add a plugin path to `plugins.load.paths`).
*   `openclaw plugins enable <id>` / `disable <id>` — toggle `plugins.entries.<id>.enabled`.
*   `openclaw plugins doctor` — report plugin load errors.

Most plugin changes require a gateway restart. See [/plugin](https://docs.openclaw.ai/tools/plugin).

## Memory

Vector search over `MEMORY.md` + `memory/*.md`:

*   `openclaw memory status` — show index stats.
*   `openclaw memory index` — reindex memory files.
*   `openclaw memory search "<query>"` (or `--query "<query>"`) — semantic search over memory.

## Chat slash commands

Chat messages support `/...` commands (text and native). See [/tools/slash-commands](https://docs.openclaw.ai/tools/slash-commands). Highlights:

*   `/status` for quick diagnostics.
*   `/config` for persisted config changes.
*   `/debug` for runtime-only config overrides (memory, not disk; requires `commands.debug: true`).

## Setup + onboarding

### `setup`

Initialize config + workspace. Options:

*   `--workspace <dir>`: agent workspace path (default `~/.openclaw/workspace`).
*   `--wizard`: run the onboarding wizard.
*   `--non-interactive`: run wizard without prompts.
*   `--mode <local|remote>`: wizard mode.
*   `--remote-url <url>`: remote Gateway URL.
*   `--remote-token <token>`: remote Gateway token.

Wizard auto-runs when any wizard flags are present (`--non-interactive`, `--mode`, `--remote-url`, `--remote-token`).

### `onboard`

Interactive wizard to set up gateway, workspace, and skills. Options:

*   `--workspace <dir>`
*   `--reset` (reset config + credentials + sessions before wizard)
*   `--reset-scope <config|config+creds+sessions|full>` (default `config+creds+sessions`; use `full` to also remove workspace)
*   `--non-interactive`
*   `--mode <local|remote>`
*   `--flow <quickstart|advanced|manual>` (manual is an alias for advanced)
*   `--auth-choice <setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|ai-gateway-api-key|moonshot-api-key|moonshot-api-key-cn|kimi-code-api-key|synthetic-api-key|venice-api-key|gemini-api-key|zai-api-key|mistral-api-key|apiKey|minimax-api|minimax-api-lightning|opencode-zen|custom-api-key|skip>`
*   `--token-provider <id>` (non-interactive; used with `--auth-choice token`)
*   `--token <token>` (non-interactive; used with `--auth-choice token`)
*   `--token-profile-id <id>` (non-interactive; default: `<provider>:manual`)
*   `--token-expires-in <duration>` (non-interactive; e.g. `365d`, `12h`)
*   `--secret-input-mode <plaintext|ref>` (default `plaintext`; use `ref` to store provider default env refs instead of plaintext keys)
*   `--anthropic-api-key <key>`
*   `--openai-api-key <key>`
*   `--mistral-api-key <key>`
*   `--openrouter-api-key <key>`
*   `--ai-gateway-api-key <key>`
*   `--moonshot-api-key <key>`
*   `--kimi-code-api-key <key>`
*   `--gemini-api-key <key>`
*   `--zai-api-key <key>`
*   `--minimax-api-key <key>`
*   `--opencode-zen-api-key <key>`
*   `--custom-base-url <url>` (non-interactive; used with `--auth-choice custom-api-key`)
*   `--custom-model-id <id>` (non-interactive; used with `--auth-choice custom-api-key`)
*   `--custom-api-key <key>` (non-interactive; optional; used with `--auth-choice custom-api-key`; falls back to `CUSTOM_API_KEY` when omitted)
*   `--custom-provider-id <id>` (non-interactive; optional custom provider id)
*   `--custom-compatibility <openai|anthropic>` (non-interactive; optional; default `openai`)
*   `--gateway-port <port>`
*   `--gateway-bind <loopback|lan|tailnet|auto|custom>`
*   `--gateway-auth <token|password>`
*   `--gateway-token <token>`
*   `--gateway-token-ref-env <name>` (non-interactive; store `gateway.auth.token` as an env SecretRef; requires that env var to be set; cannot be combined with `--gateway-token`)
*   `--gateway-password <password>`
*   `--remote-url <url>`
*   `--remote-token <token>`
*   `--tailscale <off|serve|funnel>`
*   `--tailscale-reset-on-exit`
*   `--install-daemon`
*   `--no-install-daemon` (alias: `--skip-daemon`)
*   `--daemon-runtime <node|bun>`
*   `--skip-channels`
*   `--skip-skills`
*   `--skip-health`
*   `--skip-ui`
*   `--node-manager <npm|pnpm|bun>` (pnpm recommended; bun not recommended for Gateway runtime)
*   `--json`

### `configure`

Interactive configuration wizard (models, channels, skills, gateway).

### `config`

Non-interactive config helpers (get/set/unset/file/validate). Running `openclaw config` with no subcommand launches the wizard. Subcommands:

*   `config get <path>`: print a config value (dot/bracket path).
*   `config set <path> <value>`: set a value (JSON5 or raw string).
*   `config unset <path>`: remove a value.
*   `config file`: print the active config file path.
*   `config validate`: validate the current config against the schema without starting the gateway.
*   `config validate --json`: emit machine-readable JSON output.

### `doctor`

Health checks + quick fixes (config + gateway + legacy services). Options:

*   `--no-workspace-suggestions`: disable workspace memory hints.
*   `--yes`: accept defaults without prompting (headless).
*   `--non-interactive`: skip prompts; apply safe migrations only.
*   `--deep`: scan system services for extra gateway installs.

## Channel helpers

### `channels`

Manage chat channel accounts (WhatsApp/Telegram/Discord/Google Chat/Slack/Mattermost (plugin)/Signal/iMessage/MS Teams). Subcommands:

*   `channels list`: show configured channels and auth profiles.
*   `channels status`: check gateway reachability and channel health (`--probe` runs extra checks; use `openclaw health` or `openclaw status --deep` for gateway health probes).
*   Tip: `channels status` prints warnings with suggested fixes when it can detect common misconfigurations (then points you to `openclaw doctor`).
*   `channels logs`: show recent channel logs from the gateway log file.
*   `channels add`: wizard-style setup when no flags are passed; flags switch to non-interactive mode.
    *   When adding a non-default account to a channel still using single-account top-level config, OpenClaw moves account-scoped values into `channels.<channel>.accounts.default` before writing the new account.
    *   Non-interactive `channels add` does not auto-create/upgrade bindings; channel-only bindings continue to match the default account.
*   `channels remove`: disable by default; pass `--delete` to remove config entries without prompts.
*   `channels login`: interactive channel login (WhatsApp Web only).
*   `channels logout`: log out of a channel session (if supported).

Common options:

*   `--channel <name>`: `whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams`
*   `--account <id>`: channel account id (default `default`)
*   `--name <label>`: display name for the account

`channels login` options:

*   `--channel <channel>` (default `whatsapp`; supports `whatsapp`/`web`)
*   `--account <id>`
*   `--verbose`

`channels logout` options:

*   `--channel <channel>` (default `whatsapp`)
*   `--account <id>`

`channels list` options:

*   `--no-usage`: skip model provider usage/quota snapshots (OAuth/API-backed only).
*   `--json`: output JSON (includes usage unless `--no-usage` is set).

`channels logs` options:

*   `--channel <name|all>` (default `all`)
*   `--lines <n>` (default `200`)
*   `--json`

More detail: [/concepts/oauth](https://docs.openclaw.ai/concepts/oauth) Examples:

```
openclaw channels add --channel telegram --account alerts --name "Alerts Bot" --token $TELEGRAM_BOT_TOKEN
openclaw channels add --channel discord --account work --name "Work Bot" --token $DISCORD_BOT_TOKEN
openclaw channels remove --channel discord --account work --delete
openclaw channels status --probe
openclaw status --deep
```

### `skills`

List and inspect available skills plus readiness info. Subcommands:

*   `skills list`: list skills (default when no subcommand).
*   `skills info <name>`: show details for one skill.
*   `skills check`: summary of ready vs missing requirements.

Options:

*   `--eligible`: show only ready skills.
*   `--json`: output JSON (no styling).
*   `-v`, `--verbose`: include missing requirements detail.

Tip: use `npx clawhub` to search, install, and sync skills.

### `pairing`

Approve DM pairing requests across channels. Subcommands:

*   `pairing list [channel] [--channel <channel>] [--account <id>] [--json]`
*   `pairing approve <channel> <code> [--account <id>] [--notify]`
*   `pairing approve --channel <channel> [--account <id>] <code> [--notify]`

### `devices`

Manage gateway device pairing entries and per-role device tokens. Subcommands:

*   `devices list [--json]`
*   `devices approve [requestId] [--latest]`
*   `devices reject <requestId>`
*   `devices remove <deviceId>`
*   `devices clear --yes [--pending]`
*   `devices rotate --device <id> --role <role> [--scope <scope...>]`
*   `devices revoke --device <id> --role <role>`

### `webhooks gmail`

Gmail Pub/Sub hook setup + runner. See [/automation/gmail-pubsub](https://docs.openclaw.ai/automation/gmail-pubsub). Subcommands:

*   `webhooks gmail setup` (requires `--account <email>`; supports `--project`, `--topic`, `--subscription`, `--label`, `--hook-url`, `--hook-token`, `--push-token`, `--bind`, `--port`, `--path`, `--include-body`, `--max-bytes`, `--renew-minutes`, `--tailscale`, `--tailscale-path`, `--tailscale-target`, `--push-endpoint`, `--json`)
*   `webhooks gmail run` (runtime overrides for the same flags)

### `dns setup`

Wide-area discovery DNS helper (CoreDNS + Tailscale). See [/gateway/discovery](https://docs.openclaw.ai/gateway/discovery). Options:

*   `--apply`: install/update CoreDNS config (requires sudo; macOS only).

## Messaging + agent

### `message`

Unified outbound messaging + channel actions. See: [/cli/message](https://docs.openclaw.ai/cli/message) Subcommands:

*   `message send|poll|react|reactions|read|edit|delete|pin|unpin|pins|permissions|search|timeout|kick|ban`
*   `message thread <create|list|reply>`
*   `message emoji <list|upload>`
*   `message sticker <send|upload>`
*   `message role <info|add|remove>`
*   `message channel <info|list>`
*   `message member info`
*   `message voice status`
*   `message event <list|create>`

Examples:

*   `openclaw message send --target +15555550123 --message "Hi"`
*   `openclaw message poll --channel discord --target channel:123 --poll-question "Snack?" --poll-option Pizza --poll-option Sushi`

### `agent`

Run one agent turn via the Gateway (or `--local` embedded). Required:

*   `--message <text>`

Options:

*   `--to <dest>` (for session key and optional delivery)
*   `--session-id <id>`
*   `--thinking <off|minimal|low|medium|high|xhigh>` (GPT-5.2 + Codex models only)
*   `--verbose <on|full|off>`
*   `--channel <whatsapp|telegram|discord|slack|mattermost|signal|imessage|msteams>`
*   `--local`
*   `--deliver`
*   `--json`
*   `--timeout <seconds>`

### `agents`

Manage isolated agents (workspaces + auth + routing).

#### `agents list`

List configured agents. Options:

*   `--json`
*   `--bindings`

#### `agents add [name]`

Add a new isolated agent. Runs the guided wizard unless flags (or `--non-interactive`) are passed; `--workspace` is required in non-interactive mode. Options:

*   `--workspace <dir>`
*   `--model <id>`
*   `--agent-dir <dir>`
*   `--bind <channel[:accountId]>` (repeatable)
*   `--non-interactive`
*   `--json`

Binding specs use `channel[:accountId]`. When `accountId` is omitted, OpenClaw may resolve account scope via channel defaults/plugin hooks; otherwise it is a channel binding without explicit account scope.

#### `agents bindings`

List routing bindings. Options:

*   `--agent <id>`
*   `--json`

#### `agents bind`

Add routing bindings for an agent. Options:

*   `--agent <id>`
*   `--bind <channel[:accountId]>` (repeatable)
*   `--json`

#### `agents unbind`

Remove routing bindings for an agent. Options:

*   `--agent <id>`
*   `--bind <channel[:accountId]>` (repeatable)
*   `--all`
*   `--json`

#### `agents delete <id>`

Delete an agent and prune its workspace + state. Options:

*   `--force`
*   `--json`

### `acp`

Run the ACP bridge that connects IDEs to the Gateway. See [`acp`](https://docs.openclaw.ai/cli/acp) for full options and examples.

### `status`

Show linked session health and recent recipients. Options:

*   `--json`
*   `--all` (full diagnosis; read-only, pasteable)
*   `--deep` (probe channels)
*   `--usage` (show model provider usage/quota)
*   `--timeout <ms>`
*   `--verbose`
*   `--debug` (alias for `--verbose`)

Notes:

*   Overview includes Gateway + node host service status when available.

### Usage tracking

OpenClaw can surface provider usage/quota when OAuth/API creds are available. Surfaces:

*   `/status` (adds a short provider usage line when available)
*   `openclaw status --usage` (prints full provider breakdown)
*   macOS menu bar (Usage section under Context)

Notes:

*   Data comes directly from provider usage endpoints (no estimates).
*   Providers: Anthropic, GitHub Copilot, OpenAI Codex OAuth, plus Gemini CLI/Antigravity when those provider plugins are enabled.
*   If no matching credentials exist, usage is hidden.
*   Details: see [Usage tracking](https://docs.openclaw.ai/concepts/usage-tracking).

### `health`

Fetch health from the running Gateway. Options:

*   `--json`
*   `--timeout <ms>`
*   `--verbose`

### `sessions`

List stored conversation sessions. Options:

*   `--json`
*   `--verbose`
*   `--store <path>`
*   `--active <minutes>`

## Reset / Uninstall

### `reset`

Reset local config/state (keeps the CLI installed). Options:

*   `--scope <config|config+creds+sessions|full>`
*   `--yes`
*   `--non-interactive`
*   `--dry-run`

Notes:

*   `--non-interactive` requires `--scope` and `--yes`.

### `uninstall`

Uninstall the gateway service + local data (CLI remains). Options:

*   `--service`
*   `--state`
*   `--workspace`
*   `--app`
*   `--all`
*   `--yes`
*   `--non-interactive`
*   `--dry-run`

Notes:

*   `--non-interactive` requires `--yes` and explicit scopes (or `--all`).

## Gateway

### `gateway`

Run the WebSocket Gateway. Options:

*   `--port <port>`
*   `--bind <loopback|tailnet|lan|auto|custom>`
*   `--token <token>`
*   `--auth <token|password>`
*   `--password <password>`
*   `--password-file <path>`
*   `--tailscale <off|serve|funnel>`
*   `--tailscale-reset-on-exit`
*   `--allow-unconfigured`
*   `--dev`
*   `--reset` (reset dev config + credentials + sessions + workspace)
*   `--force` (kill existing listener on port)
*   `--verbose`
*   `--claude-cli-logs`
*   `--ws-log <auto|full|compact>`
*   `--compact` (alias for `--ws-log compact`)
*   `--raw-stream`
*   `--raw-stream-path <path>`

### `gateway service`

Manage the Gateway service (launchd/systemd/schtasks). Subcommands:

*   `gateway status` (probes the Gateway RPC by default)
*   `gateway install` (service install)
*   `gateway uninstall`
*   `gateway start`
*   `gateway stop`
*   `gateway restart`

Notes:

*   `gateway status` probes the Gateway RPC by default using the service’s resolved port/config (override with `--url/--token/--password`).
*   `gateway status` supports `--no-probe`, `--deep`, and `--json` for scripting.
*   `gateway status` also surfaces legacy or extra gateway services when it can detect them (`--deep` adds system-level scans). Profile-named OpenClaw services are treated as first-class and aren’t flagged as “extra”.
*   `gateway status` prints which config path the CLI uses vs which config the service likely uses (service env), plus the resolved probe target URL.
*   On Linux systemd installs, status token-drift checks include both `Environment=` and `EnvironmentFile=` unit sources.
*   `gateway install|uninstall|start|stop|restart` support `--json` for scripting (default output stays human-friendly).
*   `gateway install` defaults to Node runtime; bun is **not recommended** (WhatsApp/Telegram bugs).
*   `gateway install` options: `--port`, `--runtime`, `--token`, `--force`, `--json`.

### `logs`

Tail Gateway file logs via RPC. Notes:

*   TTY sessions render a colorized, structured view; non-TTY falls back to plain text.
*   `--json` emits line-delimited JSON (one log event per line).

Examples:

```
openclaw logs --follow
openclaw logs --limit 200
openclaw logs --plain
openclaw logs --json
openclaw logs --no-color
```

### `gateway <subcommand>`

Gateway CLI helpers (use `--url`, `--token`, `--password`, `--timeout`, `--expect-final` for RPC subcommands). When you pass `--url`, the CLI does not auto-apply config or environment credentials. Include `--token` or `--password` explicitly. Missing explicit credentials is an error. Subcommands:

*   `gateway call <method> [--params <json>]`
*   `gateway health`
*   `gateway status`
*   `gateway probe`
*   `gateway discover`
*   `gateway install|uninstall|start|stop|restart`
*   `gateway run`

Common RPCs:

*   `config.apply` (validate + write config + restart + wake)
*   `config.patch` (merge a partial update + restart + wake)
*   `update.run` (run update + restart + wake)

Tip: when calling `config.set`/`config.apply`/`config.patch` directly, pass `baseHash` from `config.get` if a config already exists.

## Models

See [/concepts/models](https://docs.openclaw.ai/concepts/models) for fallback behavior and scanning strategy. Anthropic setup-token (supported):

```
claude setup-token
openclaw models auth setup-token --provider anthropic
openclaw models status
```

Policy note: this is technical compatibility. Anthropic has blocked some subscription usage outside Claude Code in the past; verify current Anthropic terms before relying on setup-token in production.

### `models` (root)

`openclaw models` is an alias for `models status`. Root options:

*   `--status-json` (alias for `models status --json`)
*   `--status-plain` (alias for `models status --plain`)

### `models list`

Options:

*   `--all`
*   `--local`
*   `--provider <name>`
*   `--json`
*   `--plain`

### `models status`

Options:

*   `--json`
*   `--plain`
*   `--check` (exit 1=expired/missing, 2=expiring)
*   `--probe` (live probe of configured auth profiles)
*   `--probe-provider <name>`
*   `--probe-profile <id>` (repeat or comma-separated)
*   `--probe-timeout <ms>`
*   `--probe-concurrency <n>`
*   `--probe-max-tokens <n>`

Always includes the auth overview and OAuth expiry status for profiles in the auth store. `--probe` runs live requests (may consume tokens and trigger rate limits).

### `models set <model>`

Set `agents.defaults.model.primary`.

### `models set-image <model>`

Set `agents.defaults.imageModel.primary`.

### `models aliases list|add|remove`

Options:

*   `list`: `--json`, `--plain`
*   `add <alias> <model>`
*   `remove <alias>`

### `models fallbacks list|add|remove|clear`

Options:

*   `list`: `--json`, `--plain`
*   `add <model>`
*   `remove <model>`
*   `clear`

### `models image-fallbacks list|add|remove|clear`

Options:

*   `list`: `--json`, `--plain`
*   `add <model>`
*   `remove <model>`
*   `clear`

### `models scan`

Options:

*   `--min-params <b>`
*   `--max-age-days <days>`
*   `--provider <name>`
*   `--max-candidates <n>`
*   `--timeout <ms>`
*   `--concurrency <n>`
*   `--no-probe`
*   `--yes`
*   `--no-input`
*   `--set-default`
*   `--set-image`
*   `--json`

### `models auth add|setup-token|paste-token`

Options:

*   `add`: interactive auth helper
*   `setup-token`: `--provider <name>` (default `anthropic`), `--yes`
*   `paste-token`: `--provider <name>`, `--profile-id <id>`, `--expires-in <duration>`

### `models auth order get|set|clear`

Options:

*   `get`: `--provider <name>`, `--agent <id>`, `--json`
*   `set`: `--provider <name>`, `--agent <id>`, `<profileIds...>`
*   `clear`: `--provider <name>`, `--agent <id>`

## System

### `system event`

Enqueue a system event and optionally trigger a heartbeat (Gateway RPC). Required:

*   `--text <text>`

Options:

*   `--mode <now|next-heartbeat>`
*   `--json`
*   `--url`, `--token`, `--timeout`, `--expect-final`

### `system heartbeat last|enable|disable`

Heartbeat controls (Gateway RPC). Options:

*   `--json`
*   `--url`, `--token`, `--timeout`, `--expect-final`

### `system presence`

List system presence entries (Gateway RPC). Options:

*   `--json`
*   `--url`, `--token`, `--timeout`, `--expect-final`

## Cron

Manage scheduled jobs (Gateway RPC). See [/automation/cron-jobs](https://docs.openclaw.ai/automation/cron-jobs). Subcommands:

*   `cron status [--json]`
*   `cron list [--all] [--json]` (table output by default; use `--json` for raw)
*   `cron add` (alias: `create`; requires `--name` and exactly one of `--at` | `--every` | `--cron`, and exactly one payload of `--system-event` | `--message`)
*   `cron edit <id>` (patch fields)
*   `cron rm <id>` (aliases: `remove`, `delete`)
*   `cron enable <id>`
*   `cron disable <id>`
*   `cron runs --id <id> [--limit <n>]`
*   `cron run <id> [--force]`

All `cron` commands accept `--url`, `--token`, `--timeout`, `--expect-final`.

## Node host

`node` runs a **headless node host** or manages it as a background service. See [`openclaw node`](https://docs.openclaw.ai/cli/node). Subcommands:

*   `node run --host <gateway-host> --port 18789`
*   `node status`
*   `node install [--host <gateway-host>] [--port <port>] [--tls] [--tls-fingerprint <sha256>] [--node-id <id>] [--display-name <name>] [--runtime <node|bun>] [--force]`
*   `node uninstall`
*   `node stop`
*   `node restart`

Auth notes:

*   `node` resolves gateway auth from env/config (no `--token`/`--password` flags): `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`, then `gateway.auth.*`, with remote-mode support via `gateway.remote.*`.
*   Legacy `CLAWDBOT_GATEWAY_*` env vars are intentionally ignored for node-host auth resolution.

## Nodes

`nodes` talks to the Gateway and targets paired nodes. See [/nodes](https://docs.openclaw.ai/nodes). Common options:

*   `--url`, `--token`, `--timeout`, `--json`

Subcommands:

*   `nodes status [--connected] [--last-connected <duration>]`
*   `nodes describe --node <id|name|ip>`
*   `nodes list [--connected] [--last-connected <duration>]`
*   `nodes pending`
*   `nodes approve <requestId>`
*   `nodes reject <requestId>`
*   `nodes rename --node <id|name|ip> --name <displayName>`
*   `nodes invoke --node <id|name|ip> --command <command> [--params <json>] [--invoke-timeout <ms>] [--idempotency-key <key>]`
*   `nodes run --node <id|name|ip> [--cwd <path>] [--env KEY=VAL] [--command-timeout <ms>] [--needs-screen-recording] [--invoke-timeout <ms>] <command...>` (mac node or headless node host)
*   `nodes notify --node <id|name|ip> [--title <text>] [--body <text>] [--sound <name>] [--priority <passive|active|timeSensitive>] [--delivery <system|overlay|auto>] [--invoke-timeout <ms>]` (mac only)

Camera:

*   `nodes camera list --node <id|name|ip>`
*   `nodes camera snap --node <id|name|ip> [--facing front|back|both] [--device-id <id>] [--max-width <px>] [--quality <0-1>] [--delay-ms <ms>] [--invoke-timeout <ms>]`
*   `nodes camera clip --node <id|name|ip> [--facing front|back] [--device-id <id>] [--duration <ms|10s|1m>] [--no-audio] [--invoke-timeout <ms>]`

Canvas + screen:

*   `nodes canvas snapshot --node <id|name|ip> [--format png|jpg|jpeg] [--max-width <px>] [--quality <0-1>] [--invoke-timeout <ms>]`
*   `nodes canvas present --node <id|name|ip> [--target <urlOrPath>] [--x <px>] [--y <px>] [--width <px>] [--height <px>] [--invoke-timeout <ms>]`
*   `nodes canvas hide --node <id|name|ip> [--invoke-timeout <ms>]`
*   `nodes canvas navigate <url> --node <id|name|ip> [--invoke-timeout <ms>]`
*   `nodes canvas eval [<js>] --node <id|name|ip> [--js <code>] [--invoke-timeout <ms>]`
*   `nodes canvas a2ui push --node <id|name|ip> (--jsonl <path> | --text <text>) [--invoke-timeout <ms>]`
*   `nodes canvas a2ui reset --node <id|name|ip> [--invoke-timeout <ms>]`
*   `nodes screen record --node <id|name|ip> [--screen <index>] [--duration <ms|10s>] [--fps <n>] [--no-audio] [--out <path>] [--invoke-timeout <ms>]`

Location:

*   `nodes location get --node <id|name|ip> [--max-age <ms>] [--accuracy <coarse|balanced|precise>] [--location-timeout <ms>] [--invoke-timeout <ms>]`

## Browser

Browser control CLI (dedicated Chrome/Brave/Edge/Chromium). See [`openclaw browser`](https://docs.openclaw.ai/cli/browser) and the [Browser tool](https://docs.openclaw.ai/tools/browser). Common options:

*   `--url`, `--token`, `--timeout`, `--json`
*   `--browser-profile <name>`

Manage:

*   `browser status`
*   `browser start`
*   `browser stop`
*   `browser reset-profile`
*   `browser tabs`
*   `browser open <url>`
*   `browser focus <targetId>`
*   `browser close [targetId]`
*   `browser profiles`
*   `browser create-profile --name <name> [--color <hex>] [--cdp-url <url>]`
*   `browser delete-profile --name <name>`

Inspect:

*   `browser screenshot [targetId] [--full-page] [--ref <ref>] [--element <selector>] [--type png|jpeg]`
*   `browser snapshot [--format aria|ai] [--target-id <id>] [--limit <n>] [--interactive] [--compact] [--depth <n>] [--selector <sel>] [--out <path>]`

Actions:

*   `browser navigate <url> [--target-id <id>]`
*   `browser resize <width> <height> [--target-id <id>]`
*   `browser click <ref> [--double] [--button <left|right|middle>] [--modifiers <csv>] [--target-id <id>]`
*   `browser type <ref> <text> [--submit] [--slowly] [--target-id <id>]`
*   `browser press <key> [--target-id <id>]`
*   `browser hover <ref> [--target-id <id>]`
*   `browser drag <startRef> <endRef> [--target-id <id>]`
*   `browser select <ref> <values...> [--target-id <id>]`
*   `browser upload <paths...> [--ref <ref>] [--input-ref <ref>] [--element <selector>] [--target-id <id>] [--timeout-ms <ms>]`
*   `browser fill [--fields <json>] [--fields-file <path>] [--target-id <id>]`
*   `browser dialog --accept|--dismiss [--prompt <text>] [--target-id <id>] [--timeout-ms <ms>]`
*   `browser wait [--time <ms>] [--text <value>] [--text-gone <value>] [--target-id <id>]`
*   `browser evaluate --fn <code> [--ref <ref>] [--target-id <id>]`
*   `browser console [--level <error|warn|info>] [--target-id <id>]`
*   `browser pdf [--target-id <id>]`

## Docs search

### `docs [query...]`

Search the live docs index.

## TUI

### `tui`

Open the terminal UI connected to the Gateway. Options:

*   `--url <url>`
*   `--token <token>`
*   `--password <password>`
*   `--session <key>`
*   `--deliver`
*   `--thinking <level>`
*   `--message <text>`
*   `--timeout-ms <ms>` (defaults to `agents.defaults.timeoutSeconds`)
*   `--history-limit <n>`

---

<!-- SOURCE: https://docs.openclaw.ai/cli/backup -->

# backup - OpenClaw

Create a local backup archive for OpenClaw state, config, credentials, sessions, and optionally workspaces.

```
openclaw backup create
openclaw backup create --output ~/Backups
openclaw backup create --dry-run --json
openclaw backup create --verify
openclaw backup create --no-include-workspace
openclaw backup create --only-config
openclaw backup verify ./2026-03-09T00-00-00.000Z-openclaw-backup.tar.gz
```

## Notes

*   The archive includes a `manifest.json` file with the resolved source paths and archive layout.
*   Default output is a timestamped `.tar.gz` archive in the current working directory.
*   If the current working directory is inside a backed-up source tree, OpenClaw falls back to your home directory for the default archive location.
*   Existing archive files are never overwritten.
*   Output paths inside the source state/workspace trees are rejected to avoid self-inclusion.
*   `openclaw backup verify <archive>` validates that the archive contains exactly one root manifest, rejects traversal-style archive paths, and checks that every manifest-declared payload exists in the tarball.
*   `openclaw backup create --verify` runs that validation immediately after writing the archive.
*   `openclaw backup create --only-config` backs up just the active JSON config file.

## What gets backed up

`openclaw backup create` plans backup sources from your local OpenClaw install:

*   The state directory returned by OpenClaw’s local state resolver, usually `~/.openclaw`
*   The active config file path
*   The OAuth / credentials directory
*   Workspace directories discovered from the current config, unless you pass `--no-include-workspace`

If you use `--only-config`, OpenClaw skips state, credentials, and workspace discovery and archives only the active config file path. OpenClaw canonicalizes paths before building the archive. If config, credentials, or a workspace already live inside the state directory, they are not duplicated as separate top-level backup sources. Missing paths are skipped. The archive payload stores file contents from those source trees, and the embedded `manifest.json` records the resolved absolute source paths plus the archive layout used for each asset.

## Invalid config behavior

`openclaw backup` intentionally bypasses the normal config preflight so it can still help during recovery. Because workspace discovery depends on a valid config, `openclaw backup create` now fails fast when the config file exists but is invalid and workspace backup is still enabled. If you still want a partial backup in that situation, rerun:

```
openclaw backup create --no-include-workspace
```

That keeps state, config, and credentials in scope while skipping workspace discovery entirely. If you only need a copy of the config file itself, `--only-config` also works when the config is malformed because it does not rely on parsing the config for workspace discovery.

## Size and performance

OpenClaw does not enforce a built-in maximum backup size or per-file size limit. Practical limits come from the local machine and destination filesystem:

*   Available space for the temporary archive write plus the final archive
*   Time to walk large workspace trees and compress them into a `.tar.gz`
*   Time to rescan the archive if you use `openclaw backup create --verify` or run `openclaw backup verify`
*   Filesystem behavior at the destination path. OpenClaw prefers a no-overwrite hard-link publish step and falls back to exclusive copy when hard links are unsupported

Large workspaces are usually the main driver of archive size. If you want a smaller or faster backup, use `--no-include-workspace`. For the smallest archive, use `--only-config`.

