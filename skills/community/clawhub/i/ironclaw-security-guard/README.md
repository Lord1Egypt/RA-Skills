# OpenClaw IronClaw Security Guard

Defense-in-depth guardrails for OpenClaw: block dangerous tool calls, detect prompt-injection patterns, redact secrets before outgoing messages, and keep an audit trail.

For Chinese docs, see [README.zh-CN.md](./README.zh-CN.md).

## Why this exists

Open-source and local-model workflows often fail in the same ways:

- destructive shell commands run too early
- sensitive paths or credentials leak into tool calls
- untrusted content tries to override system behavior
- agents forward secrets into chats, webhooks, or third-party tools

`ironclaw-security-guard` adds a lightweight security layer at OpenClaw's plugin hook surface without pretending to be a full sandbox or container runtime.

## What it adds

- dangerous shell command blocking
- sensitive path protection
- prompt-injection pattern detection
- outbound secret leak prevention
- secret redaction before outgoing messages
- JSONL audit logging for blocked or risky events
- a callable `ironclaw_security_scan` tool for manual inspection

## Hook coverage

The plugin currently uses these OpenClaw hook points:

- `before_prompt_build`
- `message_received`
- `before_tool_call`
- `message_sending`
- `after_tool_call`

## Quick install

Add this repo path to your OpenClaw plugin load paths, allow `ironclaw-security-guard`, and enable it in your plugin entries.

Minimal example:

```json
{
  "plugins": {
    "load": {
      "paths": ["/absolute/path/to/openclaw-ironclaw-security-guard"]
    },
    "entries": ["ironclaw-security-guard"]
  }
}
```

For a copy-pasteable example, see [examples/openclaw-config.example.json](./examples/openclaw-config.example.json).

Registry-ready package name:

```bash
@wd041216-bit/openclaw-ironclaw-security-guard
```

## 60-second verification

Run the lightweight regression suite:

```bash
npm test
```

Then try the manual scan example against a risky payload:

```bash
node --input-type=module -e "import('./src/config.ts').then(async ({ normalizeSecurityConfig }) => { const { createSecurityScanTool } = await import('./src/tool.ts'); const writes = []; const tool = createSecurityScanTool({ config: normalizeSecurityConfig({}), audit: { write: async (event) => writes.push(event) } }); const result = await tool.execute('demo', { toolName: 'shell', content: 'rm -rf /tmp/demo', redactPreview: true }); console.log(result.content[0].text); })"
```

## Typical protections

- block `rm -rf`, `git reset --hard`, `shutdown`, `curl ... | sh`, and similar destructive shell patterns
- flag `.env`, keychains, SSH keys, `.pypirc`, `.npmrc`, and cloud credential paths
- detect prompt-injection patterns such as "ignore previous instructions" or "reveal system prompt"
- redact secret-looking strings before outgoing messages
- optionally deny outbound hosts not on an allowlist

## Example scan result

```json
{
  "ok": false,
  "severity": "critical",
  "blockRecommended": true,
  "findings": [
    {
      "category": "destructive-command",
      "severity": "critical",
      "message": "Matched destructive-command rule: \\brm\\s+-[A-Za-z]*r[A-Za-z]*f\\b"
    }
  ]
}
```

See [examples/manual-scan-example.md](./examples/manual-scan-example.md) for a fuller example.

## Configuration

Main options from [openclaw.plugin.json](./openclaw.plugin.json):

- `enabled`
- `monitorOnly`
- `blockDestructiveShell`
- `protectSensitivePaths`
- `redactSecretsInMessages`
- `networkDenyByDefault`
- `allowedOutboundHosts`
- `auditLogPath`
- `protectedPathPatterns`
- `blockedCommandPatterns`

If you want a safer default for tool-heavy local agents, enable network allowlisting and keep `monitorOnly` off:

```json
{
  "plugins": {
    "entries": [
      {
        "id": "ironclaw-security-guard",
        "config": {
          "monitorOnly": false,
          "networkDenyByDefault": true,
          "allowedOutboundHosts": ["localhost", "127.0.0.1"]
        }
      }
    ]
  }
}
```

## Audit log

By default, audit events are written to:

`~/.openclaw/logs/ironclaw-security-guard.audit.jsonl`

## Design scope

This plugin is inspired by [IronClaw](https://github.com/nearai/ironclaw), but it is intentionally smaller in scope.

It does:

- add security guidance to prompt construction
- inspect messages and tool parameters
- block obviously risky calls
- record auditable events

It does not:

- provide a WASM sandbox
- isolate the runtime with containers
- guarantee full malware containment
- replace OS-level or network-level security controls

## Repository contents

- [openclaw.plugin.json](./openclaw.plugin.json): plugin manifest and config schema
- [index.ts](./index.ts): plugin entry
- [src/](./src): scanning, config, tool, and audit logic
- [skills/ironclaw-security-guard/SKILL.md](./skills/ironclaw-security-guard/SKILL.md): bundled OpenClaw skill shipped with the plugin
- [SKILL.md](./SKILL.md): public skill instructions
- [CONTRIBUTING.md](./CONTRIBUTING.md): contribution workflow
- [SECURITY.md](./SECURITY.md): vulnerability reporting path
- [examples/openclaw-config.example.json](./examples/openclaw-config.example.json): starter plugin config

## License

MIT
