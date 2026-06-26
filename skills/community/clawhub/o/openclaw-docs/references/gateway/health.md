# Health Checks

Source: https://docs.openclaw.ai/gateway/health

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConfiguration and operationsHealth ChecksGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpGateway
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
- [Health Checks (CLI)](#health-checks-cli)
- [Quick checks](#quick-checks)
- [Deep diagnostics](#deep-diagnostics)
- [When something fails](#when-something-fails)
- [Dedicated “health” command](#dedicated-%E2%80%9Chealth%E2%80%9D-command)

​Health Checks (CLI)
Short guide to verify channel connectivity without guessing.
​Quick checks

- `openclaw status` — local summary: gateway reachability/mode, update hint, linked channel auth age, sessions + recent activity.

- `openclaw status --all` — full local diagnosis (read-only, color, safe to paste for debugging).

- `openclaw status --deep` — also probes the running Gateway (per-channel probes when supported).

- `openclaw health --json` — asks the running Gateway for a full health snapshot (WS-only; no direct Baileys socket).

- Send `/status` as a standalone message in WhatsApp/WebChat to get a status reply without invoking the agent.

- Logs: tail `/tmp/openclaw/openclaw-*.log` and filter for `web-heartbeat`, `web-reconnect`, `web-auto-reply`, `web-inbound`.

​Deep diagnostics

- Creds on disk: `ls -l ~/.openclaw/credentials/whatsapp/<accountId>/creds.json` (mtime should be recent).

- Session store: `ls -l ~/.openclaw/agents/<agentId>/sessions/sessions.json` (path can be overridden in config). Count and recent recipients are surfaced via `status`.

- Relink flow: `openclaw channels logout && openclaw channels login --verbose` when status codes 409–515 or `loggedOut` appear in logs. (Note: the QR login flow auto-restarts once for status 515 after pairing.)

​When something fails

- `logged out` or status 409–515 → relink with `openclaw channels logout` then `openclaw channels login`.

- Gateway unreachable → start it: `openclaw gateway --port 18789` (use `--force` if the port is busy).

- No inbound messages → confirm linked phone is online and the sender is allowed (`channels.whatsapp.allowFrom`); for group chats, ensure allowlist + mention rules match (`channels.whatsapp.groups`, `agents.list[].groupChat.mentionPatterns`).

​Dedicated “health” command
`openclaw health --json` asks the running Gateway for its health snapshot (no direct channel sockets from the CLI). It reports linked creds/auth age when available, per-channel probe summaries, session-store summary, and a probe duration. It exits non-zero if the Gateway is unreachable or the probe fails/timeouts. Use `--timeout <ms>` to override the 10s default.Trusted proxy authHeartbeat⌘I