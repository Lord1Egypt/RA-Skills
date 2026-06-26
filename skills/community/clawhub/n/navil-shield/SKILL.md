---
name: navil-shield
description: Runtime security for OpenClaw. Protects MCP servers and CLI tools from prompt injection, data exfiltration, and privilege escalation at runtime — not just scan-time. Use when the user asks to secure their setup, protect against MCP attacks, audit installed skills, scan for threats, harden their OpenClaw configuration, check security status, wrap MCP servers with monitoring, block malicious tool calls, enable threat detection, or connect to community threat intelligence. Also activates when user mentions security, ClawHavoc, CVE-2026-25253, malicious skills, prompt injection, or data leaks.
version: 1.0.2
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: https://github.com/navilai/navil
    requires:
      bins:
        - pip
    install:
      - id: pip-navil
        kind: pip
        package: navil
        bins: [navil]
        label: "Install Navil runtime security"
    env:
      - name: NAVIL_DISABLE_CLOUD_SYNC
        required: false
        description: "Set to 'true' to disable anonymous telemetry sharing. Default: false (sharing enabled)."
      - name: NAVIL_API_KEY
        required: false
        description: "API key for Navil Cloud (paid tiers). Not needed for Community tier."
---

# Navil Shield — Runtime Security for OpenClaw

VirusTotal scans skills before install. ClawSec checks file integrity. **Navil Shield protects at runtime — watching what happens after install, while skills and MCP servers are actively executing.**

Static scanning catches 1.7% of threats. Runtime monitoring catches the other 98.3%.

## What This Skill Does

Navil Shield wraps every MCP server in your OpenClaw config with a transparent security proxy that:

- **Intercepts every tool call** in real-time and checks it against 568+ known attack patterns across 30 categories
- **Detects behavioral anomalies** using 11 statistical detectors with adaptive baselines
- **Enforces policies** — restrict which tools each agent can see and call
- **Connects to the Community Threat Network** — attack patterns discovered by other Navil users protect you within seconds
- **Logs everything** — full audit trail of every tool call, policy decision, and anomaly

Overhead: **<3 microseconds per message.** You will not notice it.

## When to Use This Skill

- User says "secure my setup" or "protect my OpenClaw" or "check my security"
- User is concerned about MCP security, prompt injection, or data exfiltration
- User just heard about ClawHavoc or CVE-2026-25253
- User asks "is my setup safe?" or "audit my skills" or "scan for threats"
- User wants to monitor what their MCP servers are doing
- User wants to reduce token costs by scoping which tools agents can see
- Automatically when new MCP servers or skills are added to the config

## First-Time Setup

When the user activates this skill for the first time, follow these steps exactly:

### Step 1: Install Navil

```bash
pip install navil --break-system-packages 2>/dev/null || pip install navil
```

Verify installation:

```bash
navil --version
```

If pip is not available, try:

```bash
pip3 install navil --break-system-packages 2>/dev/null || pip3 install navil
```

### Step 2: Find the OpenClaw MCP Config

Look for the OpenClaw configuration file. Check these locations in order:

1. `./openclaw.json` (current workspace)
2. `~/.openclaw/openclaw.json` (user config)

If found, extract the MCP server configuration section.

### Step 3: Wrap All MCP Servers

Run the one-command setup:

```bash
navil wrap <path-to-config> --dry-run
```

Show the user what will change. If they confirm:

```bash
navil wrap <path-to-config>
```

Tell the user: "Your original config has been backed up automatically. Every MCP server is now monitored by Navil's security proxy. To undo at any time: `navil wrap <path-to-config> --undo`"

### Step 4: Run Initial Scan

```bash
navil scan <path-to-config>
```

Present the security score (0-100) and any findings to the user in plain language. Group by severity: CRITICAL first, then HIGH, MEDIUM, LOW.

### Step 5: Confirm Threat Network Connection

```bash
navil cloud status 2>/dev/null || echo "Running in community mode — threat intelligence active with 48h delay"
```

Tell the user: "You're connected to the Navil Community Threat Network. Attack patterns discovered by other users will automatically protect your setup. No personal data leaves your machine — only anonymized threat metadata."

## Ongoing Protection

After initial setup, this skill provides continuous protection:

### When the User Asks "Check My Security" or "Security Status"

Run:

```bash
navil scan <path-to-config>
```

Present the score and any new findings since last check.

### When the User Installs a New Skill or MCP Server

After any skill installation from ClawHub or manual MCP config change:

1. Re-run `navil scan <path-to-config>` on the updated config
2. If the new server is not yet wrapped, run `navil wrap <path-to-config>`
3. Report any findings about the new addition

### When the User Asks for a Full Audit

Run the penetration test suite:

```bash
navil pentest
```

This runs 11 SAFE-MCP attack simulations (no real network traffic) and reports which threats the current setup catches. Present results as a pass/fail table.

### When the User Asks About Token Costs or Tool Bloat

Navil can scope which tools each agent sees, reducing schema tokens by up to 94%:

```bash
navil policy check --tool <tool-name> --agent <agent-name> --action read
```

Explain that creating a policy file at `~/.navil/policy.yaml` with tool scopes reduces both security risk and inference cost. Offer to generate a starter policy based on current usage.

### When the User Wants to Undo

```bash
navil wrap <path-to-config> --undo
```

This restores the original config from the automatic backup.

## Telemetry Transparency

By default, Navil shares **anonymized threat metadata** with the Community Threat Network. Here is exactly what is sent:

- **Sent:** anomaly type (e.g. "RATE_SPIKE"), severity, confidence score, tool name, timing metadata
- **NOT sent:** raw tool arguments, tool responses, file contents, agent prompts, user data
- **Agent IDs:** one-way HMAC-SHA256 hashed — irreversible, cannot be linked to real identities
- **Destination:** `https://navil-cloud-api.onrender.com/v1/telemetry` (see source: `navil/cloud/telemetry_sync.py`)
- **Opt-out:** set `NAVIL_DISABLE_CLOUD_SYNC=true` to stop all telemetry
- **Full audit:** inspect `navil/cloud/telemetry_sync.py` in the repo to see exactly what is collected

## What Navil Shield Does NOT Do

- It does **not** replace VirusTotal scanning or ClawSec file integrity checks — those catch different threats at different layers. Use all three together for defense in depth.
- It does **not** require an account or API key for the free Community tier.
- It does **not** slow down your agent — 2.7 microsecond overhead per message.
- It does **not** phone home with your data — only anonymized threat metadata is shared, and you can fully opt out with `NAVIL_DISABLE_CLOUD_SYNC=true`.

## Upgrade to Navil Pro

The free Community tier includes full runtime protection with community threat intelligence (48-hour delay on new patterns).

For real-time threat intel, OIDC identity integration, custom policy rules, and fleet analytics:

```bash
navil cloud login
```

Plans start at $59/month. Details at https://navil.ai

## Troubleshooting

- **"navil: command not found"** — Run `pip install navil` again, or check that your pip bin directory is in PATH.
- **"No MCP servers found in config"** — Verify the config path. OpenClaw configs are typically at `~/.openclaw/openclaw.json`.
- **"Redis not available"** — The shim mode (what `navil wrap` uses) works without Redis. Redis is only needed for the full proxy mode.
- **Undo everything** — `navil wrap <config> --undo` restores your original config from the automatic backup.

## Links

- GitHub: https://github.com/navilai/navil
- Documentation: https://navil.ai/docs
- Community Threat Radar: https://navil.ai/radar
- Report an issue: https://github.com/navilai/navil/issues
