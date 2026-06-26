# Configuration

Source: https://docs.openclaw.ai/gateway/configuration

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConfiguration and operationsConfigurationGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpGateway
Gateway RunbookConfiguration and operations
ConfigurationConfiguration ReferenceConfiguration ExamplesAuthenticationTrusted proxy authHealth ChecksHeartbeatDoctorLoggingGateway LockBackground Exec and Process ToolMultiple GatewaysTroubleshooting
Security and sandboxingProtocols and APIsNetworking and discovery
Remote access
Remote AccessRemote Gateway SetupTailscale
Security
Formal Verification (Security Models)
Web interfaces
WebControl UIDashboardWebChatTUI
On this page
- [Configuration](#configuration)
- [Minimal config](#minimal-config)
- [Editing config](#editing-config)
- [Strict validation](#strict-validation)
- [Common tasks](#common-tasks)
- [Config hot reload](#config-hot-reload)
- [Reload modes](#reload-modes)
- [What hot-applies vs what needs a restart](#what-hot-applies-vs-what-needs-a-restart)
- [Config RPC (programmatic updates)](#config-rpc-programmatic-updates)
- [Environment variables](#environment-variables)
- [Full reference](#full-reference)

​Configuration
OpenClaw reads an optional **JSON5** config from `~/.openclaw/openclaw.json`.
If the file is missing, OpenClaw uses safe defaults. Common reasons to add a config:

- Connect channels and control who can message the bot

- Set models, tools, sandboxing, or automation (cron, hooks)

- Tune sessions, media, networking, or UI

See the [full reference](/gateway/configuration-reference) for every available field.
**New to configuration?** Start with `openclaw onboard` for interactive setup, or check out the [Configuration Examples](/gateway/configuration-examples) guide for complete copy-paste configs.
​Minimal config
Copy```
// ~/.openclaw/openclaw.json
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}

```

​Editing config

 Interactive wizard CLI (one-liners) Control UI Direct edit
Copy```
openclaw onboard       # full setup wizard
openclaw configure     # config wizard

```

Copy```
openclaw config get agents.defaults.workspace
openclaw config set agents.defaults.heartbeat.every "2h"
openclaw config unset tools.web.search.apiKey

```

Open [http://127.0.0.1:18789](http://127.0.0.1:18789) and use the **Config** tab.
The Control UI renders a form from the config schema, with a **Raw JSON** editor as an escape hatch.Edit `~/.openclaw/openclaw.json` directly. The Gateway watches the file and applies changes automatically (see [hot reload](#config-hot-reload)).
​Strict validation
OpenClaw only accepts configurations that fully match the schema. Unknown keys, malformed types, or invalid values cause the Gateway to **refuse to start**. The only root-level exception is `$schema` (string), so editors can attach JSON Schema metadata.
When validation fails:

- The Gateway does not boot

- Only diagnostic commands work (`openclaw doctor`, `openclaw logs`, `openclaw health`, `openclaw status`)

- Run `openclaw doctor` to see exact issues

- Run `openclaw doctor --fix` (or `--yes`) to apply repairs

​Common tasks
Set up a channel (WhatsApp, Telegram, Discord, etc.)

Each channel has its own config section under `channels.<provider>`. See the dedicated channel page for setup steps:

- [WhatsApp](/channels/whatsapp) — `channels.whatsapp`

- [Telegram](/channels/telegram) — `channels.telegram`

- [Discord](/channels/discord) — `channels.discord`

- [Slack](/channels/slack) — `channels.slack`

- [Signal](/channels/signal) — `channels.signal`

- [iMessage](/channels/imessage) — `channels.imessage`

- [Google Chat](/channels/googlechat) — `channels.googlechat`

- [Mattermost](/channels/mattermost) — `channels.mattermost`

- [MS Teams](/channels/msteams) — `channels.msteams`

All channels share the same DM policy pattern:Copy```
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",   // pairing | allowlist | open | disabled
      allowFrom: ["tg:123"], // only for allowlist/open
    },
  },
}

```

Choose and configure models

Set the primary model and optional fallbacks:Copy```
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
    },
  },
}

```

- `agents.defaults.models` defines the model catalog and acts as the allowlist for `/model`.

- Model refs use `provider/model` format (e.g. `anthropic/claude-opus-4-6`).

- See [Models CLI](/concepts/models) for switching models in chat and [Model Failover](/concepts/model-failover) for auth rotation and fallback behavior.

- For custom/self-hosted providers, see [Custom providers](/gateway/configuration-reference#custom-providers-and-base-urls) in the reference.

Control who can message the bot

DM access is controlled per channel via `dmPolicy`:

- `"pairing"` (default): unknown senders get a one-time pairing code to approve

- `"allowlist"`: only senders in `allowFrom` (or the paired allow store)

- `"open"`: allow all inbound DMs (requires `allowFrom: ["*"]`)

- `"disabled"`: ignore all DMs

For groups, use `groupPolicy` + `groupAllowFrom` or channel-specific allowlists.See the [full reference](/gateway/configuration-reference#dm-and-group-access) for per-channel details.Set up group chat mention gating

Group messages default to **require mention**. Configure patterns per agent:Copy```
{
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          mentionPatterns: ["@openclaw", "openclaw"],
        },
      },
    ],
  },
  channels: {
    whatsapp: {
      groups: { "*": { requireMention: true } },
    },
  },
}

```

- **Metadata mentions**: native @-mentions (WhatsApp tap-to-mention, Telegram @bot, etc.)

- **Text patterns**: regex patterns in `mentionPatterns`

- See [full reference](/gateway/configuration-reference#group-chat-mention-gating) for per-channel overrides and self-chat mode.

Configure sessions and resets

Sessions control conversation continuity and isolation:Copy```
{
  session: {
    dmScope: "per-channel-peer",  // recommended for multi-user
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
  },
}

```

- `dmScope`: `main` (shared) | `per-peer` | `per-channel-peer` | `per-account-channel-peer`

- See [Session Management](/concepts/session) for scoping, identity links, and send policy.

- See [full reference](/gateway/configuration-reference#session) for all fields.

Enable sandboxing

Run agent sessions in isolated Docker containers:Copy```
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",  // off | non-main | all
        scope: "agent",    // session | agent | shared
      },
    },
  },
}

```

Build the image first: `scripts/sandbox-setup.sh`See [Sandboxing](/gateway/sandboxing) for the full guide and [full reference](/gateway/configuration-reference#sandbox) for all options.Set up heartbeat (periodic check-ins)

Copy```
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
      },
    },
  },
}

```

- `every`: duration string (`30m`, `2h`). Set `0m` to disable.

- `target`: `last` | `whatsapp` | `telegram` | `discord` | `none`

- See [Heartbeat](/gateway/heartbeat) for the full guide.

Configure cron jobs

Copy```
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
  },
}

```

See [Cron jobs](/automation/cron-jobs) for the feature overview and CLI examples.Set up webhooks (hooks)

Enable HTTP webhook endpoints on the Gateway:Copy```
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    allowedSessionKeyPrefixes: ["hook:"],
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "main",
        deliver: true,
      },
    ],
  },
}

```

See [full reference](/gateway/configuration-reference#hooks) for all mapping options and Gmail integration.Configure multi-agent routing

Run multiple isolated agents with separate workspaces and sessions:Copy```
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}

```

See [Multi-Agent](/concepts/multi-agent) and [full reference](/gateway/configuration-reference#multi-agent-routing) for binding rules and per-agent access profiles.Split config into multiple files ($include)

Use `$include` to organize large configs:Copy```
// ~/.openclaw/openclaw.json
{
  gateway: { port: 18789 },
  agents: { $include: "./agents.json5" },
  broadcast: {
    $include: ["./clients/a.json5", "./clients/b.json5"],
  },
}

```

- **Single file**: replaces the containing object

- **Array of files**: deep-merged in order (later wins)

- **Sibling keys**: merged after includes (override included values)

- **Nested includes**: supported up to 10 levels deep

- **Relative paths**: resolved relative to the including file

- **Error handling**: clear errors for missing files, parse errors, and circular includes

​Config hot reload
The Gateway watches `~/.openclaw/openclaw.json` and applies changes automatically — no manual restart needed for most settings.
​Reload modes
ModeBehavior**`hybrid`** (default)Hot-applies safe changes instantly. Automatically restarts for critical ones.**`hot`**Hot-applies safe changes only. Logs a warning when a restart is needed — you handle it.**`restart`**Restarts the Gateway on any config change, safe or not.**`off`**Disables file watching. Changes take effect on the next manual restart.
Copy```
{
  gateway: {
    reload: { mode: "hybrid", debounceMs: 300 },
  },
}

```

​What hot-applies vs what needs a restart
Most fields hot-apply without downtime. In `hybrid` mode, restart-required changes are handled automatically.
CategoryFieldsRestart needed?Channels`channels.*`, `web` (WhatsApp) — all built-in and extension channelsNoAgent & models`agent`, `agents`, `models`, `routing`NoAutomation`hooks`, `cron`, `agent.heartbeat`NoSessions & messages`session`, `messages`NoTools & media`tools`, `browser`, `skills`, `audio`, `talk`NoUI & misc`ui`, `logging`, `identity`, `bindings`NoGateway server`gateway.*` (port, bind, auth, tailscale, TLS, HTTP)**Yes**Infrastructure`discovery`, `canvasHost`, `plugins`**Yes**
`gateway.reload` and `gateway.remote` are exceptions — changing them does **not** trigger a restart.
​Config RPC (programmatic updates)
config.apply (full replace)

Validates + writes the full config and restarts the Gateway in one step.`config.apply` replaces the **entire config**. Use `config.patch` for partial updates, or `openclaw config set` for single keys.Params:

- `raw` (string) — JSON5 payload for the entire config

- `baseHash` (optional) — config hash from `config.get` (required when config exists)

- `sessionKey` (optional) — session key for the post-restart wake-up ping

- `note` (optional) — note for the restart sentinel

- `restartDelayMs` (optional) — delay before restart (default 2000)

Copy```
openclaw gateway call config.get --params &#x27;{}&#x27;  # capture payload.hash
openclaw gateway call config.apply --params &#x27;{
  "raw": "{ agents: { defaults: { workspace: \"~/.openclaw/workspace\" } } }",
  "baseHash": "<hash>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123"
}&#x27;

```

config.patch (partial update)

Merges a partial update into the existing config (JSON merge patch semantics):

- Objects merge recursively

- `null` deletes a key

- Arrays replace

Params:

- `raw` (string) — JSON5 with just the keys to change

- `baseHash` (required) — config hash from `config.get`

- `sessionKey`, `note`, `restartDelayMs` — same as `config.apply`

Copy```
openclaw gateway call config.patch --params &#x27;{
  "raw": "{ channels: { telegram: { groups: { \"*\": { requireMention: false } } } } }",
  "baseHash": "<hash>"
}&#x27;

```

​Environment variables
OpenClaw reads env vars from the parent process plus:

- `.env` from the current working directory (if present)

- `~/.openclaw/.env` (global fallback)

Neither file overrides existing env vars. You can also set inline env vars in config:
Copy```
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
  },
}

```

Shell env import (optional)

If enabled and expected keys aren’t set, OpenClaw runs your login shell and imports only the missing keys:Copy```
{
  env: {
    shellEnv: { enabled: true, timeoutMs: 15000 },
  },
}

```

Env var equivalent: `OPENCLAW_LOAD_SHELL_ENV=1`
Env var substitution in config values

Reference env vars in any config string value with `${VAR_NAME}`:Copy```
{
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
  models: { providers: { custom: { apiKey: "${CUSTOM_API_KEY}" } } },
}

```

Rules:

- Only uppercase names matched: `[A-Z_][A-Z0-9_]*`

- Missing/empty vars throw an error at load time

- Escape with `$${VAR}` for literal output

- Works inside `$include` files

- Inline substitution: `"${BASE}/v1"` → `"https://api.example.com/v1"`

See [Environment](/help/environment) for full precedence and sources.
​Full reference
For the complete field-by-field reference, see **[Configuration Reference](/gateway/configuration-reference)**.

*Related: [Configuration Examples](/gateway/configuration-examples) · [Configuration Reference](/gateway/configuration-reference) · [Doctor](/gateway/doctor)*Gateway RunbookConfiguration Reference⌘I