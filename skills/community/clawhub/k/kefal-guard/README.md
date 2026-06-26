# Kefal Guard

Infrastructure security monitoring for OpenClaw. Detects exposed services, privilege escalation paths, and novel threats using compositional reasoning engines.

## What It Does

Kefal installs a lightweight agent (~6 MB static binary) alongside your OpenClaw gateway. Every 60 seconds, it scans your system and checks 32 security invariants. When something is wrong — a database exposed to the internet, an unknown SSH key, a process making outbound connections to an unfamiliar IP — you get an incident with severity, explanation, and the exact commands to fix it.

Your infrastructure appears as a live graph at kefal.dev/app. Nodes are hosts, services, ports, and identities. Edges are relationships and access paths. Incidents overlay the graph so you see exactly where the problem is.

## Why This Exists

OpenClaw runs on your machine with broad access — files, shell, browser, messaging platforms. That power creates a security surface that traditional tools weren't built to monitor. Kefal was purpose-built for this: it understands the context of agent-driven infrastructure and detects threats that signature-based tools miss.

## How to Use

1. Install the skill via ClawHub (`openclaw skills install kefal-guard`) or copy `SKILL.md` into `~/.openclaw/workspace/skills/kefal-guard/` manually. The skill itself is a Markdown file with frontmatter; it does not download or execute anything.
2. Install the `kefal-agent` binary separately. Platform-specific instructions, checksums, and Gatekeeper notes are at **https://kefal.dev/docs/installation.html**.
3. From OpenClaw: `/kefal status`, `/kefal scan`, `/kefal incidents`, `/kefal remediate <id>`, `/kefal graph`.

## Examples

**After installing a third-party skill:**
```
You: I just installed the data-export skill from ClawHub. Can you check if it opened any new attack surface?
Agent: Running Kefal scan... No new incidents detected. The skill did not open any new ports or create outbound connections.
```

**Routine security check:**
```
You: Is my server secure?
Agent: Running full Kefal scan... 1 incident found:
  HIGH: service_privilege_exposure — postgres:5432 is listening on 0.0.0.0 instead of 127.0.0.1.
  Remediation: [3 steps with exact commands]
```

## Requirements

- OpenClaw on Linux (x86_64, ARM64) or macOS (Intel, Apple Silicon)
- Outbound HTTPS access to kefal.dev (for dashboard and incident reporting)
- sudo access for initial agent installation (the agent scans system-level information)

## Permissions Justification

| Permission | Why |
|---|---|
| `exec` (shell commands) | The skill invokes `kefal-agent --status` / `--scan` to read the agent's output. The agent binary is installed and reviewed separately by the operator (this skill never downloads or executes remote code). |
| Network (outbound to kefal.dev) | The agent — not the skill — reports scan telemetry to your dashboard over TLS 1.3. The skill only reads local agent output. |
| sudo (operator-side, one-time) | The operator runs the agent as root once during initial enrollment so it can read `/proc`, listening ports, and `~/.ssh/authorized_keys` for the system view. The skill itself does not request sudo. |

What the agent reads: process list (name/PID/user), listening ports (port/proto/owner), user accounts (`/etc/passwd`), SSH authorized public keys. What it does NOT read: process memory, file contents (databases, configs, documents), network packets, or private keys. What it does NOT modify: nothing — the agent is read-only by design and never writes to your system.

## Troubleshooting

**Agent not running after install:** verify the binary is on `$PATH` (`kefal-agent --version`), check the systemd service status on Linux (`systemctl status kefal-agent`), or run with `--verbose` to see step-by-step traces. Full troubleshooting: https://kefal.dev/docs/installation.html#troubleshooting

**macOS Gatekeeper rejection** ("cannot be opened because the developer cannot be verified"): the binaries are not yet notarized. The installation guide explains how to verify and approve them on a per-binary basis.

**No incidents showing in dashboard:**
The agent needs 2-3 scan cycles (2-3 minutes) to establish a baseline before reporting anomalies. `transition_novelty` incidents may appear during the first few minutes as the system learns your infrastructure's normal patterns.

## Pricing

7-day free trial, no credit card required. $49/month Starter (3 agents), $149/month Professional (15 agents + Cortex adversarial verification), $399/month Enterprise (unlimited). Details: https://kefal.dev/#pricing

## Links

- Dashboard: https://kefal.dev/app
- Documentation: https://kefal.dev/docs
- Install guide: https://kefal.dev/docs/installation.html
- Homepage: https://kefal.dev
- Built by: Catalyst AI Research (https://catalystais.com) — Haifa, Israel
