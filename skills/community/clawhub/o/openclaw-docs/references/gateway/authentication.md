# Authentication

Source: https://docs.openclaw.ai/gateway/authentication

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConfiguration and operationsAuthenticationGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpGateway
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
- [Authentication](#authentication)
- [Recommended Anthropic setup (API key)](#recommended-anthropic-setup-api-key)
- [Anthropic: setup-token (subscription auth)](#anthropic-setup-token-subscription-auth)
- [Checking model auth status](#checking-model-auth-status)
- [Controlling which credential is used](#controlling-which-credential-is-used)
- [Per-session (chat command)](#per-session-chat-command)
- [Per-agent (CLI override)](#per-agent-cli-override)
- [Troubleshooting](#troubleshooting)
- [“No credentials found”](#%E2%80%9Cno-credentials-found%E2%80%9D)
- [Token expiring/expired](#token-expiring%2Fexpired)
- [Requirements](#requirements)

​Authentication
OpenClaw supports OAuth and API keys for model providers. For Anthropic
accounts, we recommend using an **API key**. For Claude subscription access,
use the long‑lived token created by `claude setup-token`.
See [/concepts/oauth](/concepts/oauth) for the full OAuth flow and storage
layout.
​Recommended Anthropic setup (API key)
If you’re using Anthropic directly, use an API key.

- Create an API key in the Anthropic Console.

- Put it on the **gateway host** (the machine running `openclaw gateway`).

Copy```
export ANTHROPIC_API_KEY="..."
openclaw models status

```

- If the Gateway runs under systemd/launchd, prefer putting the key in
`~/.openclaw/.env` so the daemon can read it:

Copy```
cat >> ~/.openclaw/.env <<&#x27;EOF&#x27;
ANTHROPIC_API_KEY=...
EOF

```

Then restart the daemon (or restart your Gateway process) and re-check:
Copy```
openclaw models status
openclaw doctor

```

If you’d rather not manage env vars yourself, the onboarding wizard can store
API keys for daemon use: `openclaw onboard`.
See [Help](/help) for details on env inheritance (`env.shellEnv`,
`~/.openclaw/.env`, systemd/launchd).
​Anthropic: setup-token (subscription auth)
For Anthropic, the recommended path is an **API key**. If you’re using a Claude
subscription, the setup-token flow is also supported. Run it on the **gateway host**:
Copy```
claude setup-token

```

Then paste it into OpenClaw:
Copy```
openclaw models auth setup-token --provider anthropic

```

If the token was created on another machine, paste it manually:
Copy```
openclaw models auth paste-token --provider anthropic

```

If you see an Anthropic error like:
Copy```
This credential is only authorized for use with Claude Code and cannot be used for other API requests.

```

…use an Anthropic API key instead.
Manual token entry (any provider; writes `auth-profiles.json` + updates config):
Copy```
openclaw models auth paste-token --provider anthropic
openclaw models auth paste-token --provider openrouter

```

Automation-friendly check (exit `1` when expired/missing, `2` when expiring):
Copy```
openclaw models status --check

```

Optional ops scripts (systemd/Termux) are documented here:
[/automation/auth-monitoring](/automation/auth-monitoring)

`claude setup-token` requires an interactive TTY.

​Checking model auth status
Copy```
openclaw models status
openclaw doctor

```

​Controlling which credential is used
​Per-session (chat command)
Use `/model <alias-or-id>@<profileId>` to pin a specific provider credential for the current session (example profile ids: `anthropic:default`, `anthropic:work`).
Use `/model` (or `/model list`) for a compact picker; use `/model status` for the full view (candidates + next auth profile, plus provider endpoint details when configured).
​Per-agent (CLI override)
Set an explicit auth profile order override for an agent (stored in that agent’s `auth-profiles.json`):
Copy```
openclaw models auth order get --provider anthropic
openclaw models auth order set --provider anthropic anthropic:default
openclaw models auth order clear --provider anthropic

```

Use `--agent <id>` to target a specific agent; omit it to use the configured default agent.
​Troubleshooting
​“No credentials found”
If the Anthropic token profile is missing, run `claude setup-token` on the
**gateway host**, then re-check:
Copy```
openclaw models status

```

​Token expiring/expired
Run `openclaw models status` to confirm which profile is expiring. If the profile
is missing, rerun `claude setup-token` and paste the token again.
​Requirements

- Claude Max or Pro subscription (for `claude setup-token`)

- Claude Code CLI installed (`claude` command available)

Configuration ExamplesTrusted proxy auth⌘I