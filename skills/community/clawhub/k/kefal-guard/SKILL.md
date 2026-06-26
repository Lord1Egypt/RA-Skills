---
name: kefal_guard
description: Infrastructure security monitor — detects exposed services, privilege escalation paths, and novel threats using compositional reasoning. Read-only host telemetry agent. Manual install, no auto-execution.
metadata: {"openclaw": {"os": ["darwin", "linux"], "requires": {"bins": ["kefal-agent"]}, "homepage": "https://kefal.dev", "docs": "https://kefal.dev/docs/installation.html"}}
---

# Kefal Guard — Infrastructure Security for OpenClaw

Kefal monitors the machine running your OpenClaw gateway. It detects exposed databases, privilege escalation paths, unauthorized SSH keys, novel outbound connections, and services listening where they shouldn't — before an attacker does.

## What it does

Kefal installs a lightweight agent (single static binary, ~6 MB) that scans your system every 60 seconds. It reports to your Kefal dashboard at kefal.dev/app, where you see:

- A live **graph** of every host, service, port, and identity on your infrastructure
- **Incidents** with severity levels (critical, high, medium) and plain-English explanations
- **Remediation plans** with the exact shell commands to fix each issue

32 security invariants run on every scan. When something breaks — a new admin account, a service exposed to the internet, an outbound connection to an unknown IP — Kefal tells you what happened, why it matters, and how to fix it.

## When to use this skill

- After installing OpenClaw on a new server or VPS
- Before exposing your gateway to the internet
- When installing untrusted third-party skills from ClawHub
- As continuous monitoring alongside your OpenClaw agent

## Install

The agent is a separate binary that the operator installs and reviews manually — this skill does not download or execute remote code. Platform-specific install instructions, binary checksums, and verification steps are documented at:

**https://kefal.dev/docs/installation.html**

After install, verify with `kefal-agent --version` and `kefal-agent --status`. The skill below assumes the binary is on `$PATH`.

## Commands

- `/kefal status` — Show agent status, last scan time, and open incidents
- `/kefal scan` — Trigger an immediate scan (normally runs every 60s)
- `/kefal incidents` — List all open incidents with severity and details
- `/kefal remediate <incident-id>` — Show remediation steps for a specific incident
- `/kefal graph` — Open the live infrastructure graph in your browser

## How the agent uses this skill

When the user asks about security, infrastructure health, or mentions concerns about exposed services or vulnerabilities, use the `exec` tool to run `kefal-agent --status` or `kefal-agent --scan` and report the results. If incidents are found, present them with their remediation steps.

When the user installs a new third-party skill, suggest running `/kefal scan` to verify no new attack surface was introduced.

When the user asks "is my server secure?" or "audit my setup", run a full scan and present the results as a security report.

## What data does the agent collect

The agent reads host system metadata only:

- Running processes — name, PID, owning user, CPU usage. (Source: `/proc/<pid>/stat` on Linux, equivalent APIs on macOS/Windows. The agent does not read process memory or open file descriptors.)
- Listening ports — port number, protocol, owning process name. (Source: `/proc/net/tcp` and equivalents. The agent does not capture packets or read network traffic.)
- User accounts with shell access — username and login state. (Source: `/etc/passwd` for the username list, `utmp` for active sessions. The agent reads these as a non-root user when possible; sudo is only needed for full process visibility.)
- SSH authorized keys — public key fingerprints in `~/.ssh/authorized_keys`. (Source: the file is read line-by-line as text. The agent never touches private keys; private keys live in different files and are never read.)

The agent does NOT read application data (databases, application config, business documents), does NOT capture network traffic, and does NOT modify any system file. All telemetry is transmitted over TLS 1.3 to kefal.dev. Each tenant's data is isolated; no data is shared with other customers.

The agent source structure is documented in the [installation guide](https://kefal.dev/docs/installation.html) and the binaries are published with reproducible-build flags (`-trimpath -ldflags="-s -w"`), so the SHA-256 you download can be matched against a future open-source release.

## Pricing

The skill includes a 7-day free trial. Plans start at $49/month for up to 3 agents. No credit card required to start. See https://kefal.dev/#pricing for details.

## Built by

Catalyst AI Research — Haifa, Israel. https://catalystais.com
