# OpenClaw Safety Coach

**🔗 [View on ClawHub](https://clawhub.ai/justindobbs/openclaw-safety-coach)**

**🔗 [View on GitHub](https://github.com/justindobbs/openclaw-productivity-suite/blob/main/skills/openclaw-safety-coach)**

This skill helps you set up and maintain a secure environment for your OpenClaw instance. OpenClaw ships with conservative defaults — this coach helps you stay on them and harden further as you expose more surface.

## Philosophy

**Start simple, then layer complexity.** Address and understand the most common safety issues quickly, then progress to more sophisticated setups with multiple security layers.

**One trust boundary per gateway.** This skill assumes a single operator or a team whose members trust each other. For mixed-trust or adversarial-user operation, split into separate gateways and credentials.

**Security is continuous, not one-time.** This isn't a "set it and forget it" solution - it's an ongoing process of improvement and adaptation to emerging threats.

## What's New (October 2026)

Modernized to align with the current OpenClaw security documentation:

- **Tool Profiles & Deny Groups** - `tools.profile="messaging"` baseline; deny `group:automation`, `group:runtime`, `group:fs`
- **Cross-Provider Messaging Controls** - `tools.message.crossContext.allowAcrossProviders` / `allowWithinProvider` to confine message actions
- **Elevated Execution Mode** - `tools.elevated` controls for running exec outside the sandbox, with `allowFrom` restrictions
- **Context Visibility** - `contextVisibility` per channel/room (`"all"`, `"allowlist"`, `"allowlist_quote"`) to filter untrusted prompt content
- **Session Visibility & Agent-to-Agent** - `tools.sessions.visibility` (`self`/`tree`/`agent`/`all`) and `tools.agentToAgent` controls
- **Sub-Agent Delegation Guardrails** - `sandbox: "require"` on `sessions_spawn`; `agents.defaults.subagents.allowAgents` restrictions
- **Sandbox Workspace Access** - `agents.defaults.sandbox.workspaceAccess` modes: `"none"`, `"ro"`, `"rw"`
- **Filesystem Restrictions** - `tools.fs.workspaceOnly=true` restricts all read/write/edit paths to the workspace
- **Node Execution (`system.run`)** - Remote code execution on paired macOS nodes with `gateway.nodes.commands.allow`/`.deny` policy
- **`openclaw` Delegation Tool** - Agents request persistent config/lifecycle changes through typed operations with permission policy
- **Requester-Scoped Controls** - `tools.toolsBySender` and owner-only inventories as defense-in-depth
- **Expanded Dangerous Flags Watchlist** - Now includes plugin permission modes, Telegram private network, Synology Chat webhook path, per-mapping `allowUnsafeExternalContent`, audit suppressions
- **Operator Incident Response** - Contain → Rotate → Audit → Deep Scan → Verify → Collect → Redeploy playbook aligned with official docs
- **Retired Flags** - `gateway.controlUi.dangerouslyDisableDeviceAuth` marked as retired/inert; `gateway.controlUi.allowInsecureAuth` removed
- **Gateway Auth Clarified** - `gateway.auth.mode="none"` is explicit opt-in (not removed); trusted-proxy auth and Tailscale auth documented

## Quick Start

1. Load the Safety Coach skill in your OpenClaw instance
2. **Immediate actions:**
   - Run `openclaw security audit --deep` for a full assessment (gateway auth, dangerous flags, file permissions, plugin/skill code scan)
   - Run `openclaw secrets audit` to check for plaintext API keys
   - Verify `dmPolicy="pairing"` is set for all DM-capable channels
   - Review `openclaw pairing list` for unauthorized access attempts
   - Set `session.dmScope="per-channel-peer"` if multiple people can DM the bot
   - Set `contextVisibility="allowlist"` on rooms with untrusted members
   - Ensure `commands.allowFrom` is scoped to trusted operators
   - Confirm `tools.elevated.enabled=false` and `tools.agentToAgent.enabled=false` unless explicitly needed
   - Confirm no `dangerouslyAllow*` flags are enabled and no `permissionMode=approve-all` on plugins
   - Confirm Control UI is behind HTTPS (Tailscale Serve or TLS cert)
3. Review the safety policies and customize for your use case
4. Test with various prompts to ensure proper behavior
5. Monitor and adjust policies as needed

## Usage

The Safety Coach automatically activates when potentially unsafe requests are detected, providing:
- Risk assessment and warnings
- Alternative safe approaches
- Educational guidance on security best practices
- Specific CLI commands and configuration examples

## Security Areas Covered

### Gateway & Network
- Gateway bind and auth (`gateway.bind="loopback"`, `gateway.auth.mode`, trusted-proxy, Tailscale)
- Control UI exposure and origin settings (`gateway.publicOrigin`, `gateway.controlUi.allowedOrigins`)
- Rate limiting (lockouts, throttles, caps, cooldowns)
- Network exposure and reverse proxy hardening

### Access Control
- DM policy (`pairing`, `allowlist`, `open`, `disabled`) and `allowFrom` lists
- DM session isolation (`session.dmScope`) and identity links (`session.identityLinks`)
- Group policy (`groupPolicy="allowlist"`, `groupAllowFrom`, `requireMention`, custom `mentionPatterns`)
- Context visibility filtering (`contextVisibility`)
- Command authorization (`commands.allowFrom`)

### Tool & Agent Permissions
- Tool profiles and deny groups (`tools.profile`, `group:automation`, `group:runtime`, `group:fs`)
- Control-plane tool restrictions (`gateway`, `cron`, `sessions_spawn`, `sessions_send`)
- Cross-provider messaging controls (`tools.message.crossContext`)
- Exec approvals (`exec.security="deny"`, `exec.ask="always"`)
- Node execution (`system.run`) and gateway command policy
- Elevated mode (`tools.elevated`)
- Filesystem restrictions (`tools.exec.applyPatch.workspaceOnly`, `tools.fs.workspaceOnly`)
- `openclaw` delegation tool and requester-scoped controls (`tools.toolsBySender`)

### Sandbox & Isolation
- Sandbox scope (`"agent"`, `"session"`, `"shared"`) and workspace access (`"none"`, `"ro"`, `"rw"`)
- Docker bind validation and blocked-path denylist
- Container dangerous flags (`dangerouslyAllowContainerNamespaceJoin`, etc.)
- Sub-agent delegation guardrails (`sandbox: "require"`, `allowAgents`)
- Session visibility (`tools.sessions.visibility`) and agent-to-agent controls

### Threat Detection
- Malicious skill/plugin detection (`openclaw security audit --deep`)
- Tool abuse and exec escalation prevention
- SSRF/exfiltration protection (browser SSRF policy, Telegram private network)
- Prompt injection defense (sandboxing, `contextVisibility`, untrusted-input wrapping)
- Secret leakage detection and rotation workflows
- Memory poisoning prevention
- Cross-provider messaging abuse detection
- Elevated execution and sub-agent delegation abuse

### Dangerous Flags Watchlist
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback`
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork`
- `agents.defaults.sandbox.docker.dangerouslyAllow*` (three flags)
- `channels.*.dangerouslyAllowNameMatching` (all providers incl. plugin channels)
- `channels.synology-chat.dangerouslyAllowInheritedWebhookPath`
- `channels.telegram.network.dangerouslyAllowPrivateNetwork`
- `hooks.allowUnsafeExternalContent` / `hooks.gmail.allowUnsafeExternalContent` / `hooks.mappings[*].allowUnsafeExternalContent`
- `tools.exec.applyPatch.workspaceOnly=false`
- `plugins.entries.acpx.config.permissionMode=approve-all`
- `security.audit.suppressions` (tracked even when suppressed)

> 📚 Reference: [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security) — trust model, audit checks, hardened baselines, access control, tool permissions, network exposure, secrets/storage, incident response.

## Contributing

We welcome contributions to improve this safety coach.

### Adding New Safety Rules

1. **Identify the Risk**: Clearly define the security concern or threat vector
2. **Research**: Check [OpenClaw security docs](https://docs.openclaw.ai/gateway/security) and [audit checks reference](https://docs.openclaw.ai/gateway/security/audit-checks) for relevant updates
3. **Create Test Cases**: Write examples of both safe and unsafe prompts
4. **Implement Logic**: Add detection and response mechanisms
5. **Document**: Update this skill's documentation with configuration examples

### Version Tracking

When adding new rules, include the relevant OpenClaw version or doc page link to help users understand which features require specific OpenClaw versions.

## License

See LICENSE file in the main repository.
