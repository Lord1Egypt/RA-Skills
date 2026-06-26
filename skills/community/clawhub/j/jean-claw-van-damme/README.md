![Jean-Claw Van Damme](/assets/banner.jpg)

# Jean-Claw Van Damme 🦞🥋

**The roundhouse kick your agent needs.**

Authorization gatekeeper for OpenClaw agents. Scoped grants, time-bound permissions, skill scanning, prompt injection detection, and full audit trail -- so your agent only does what you've explicitly allowed.

Built on principles from the [APOA (Agentic Power of Attorney)](https://agenticpoa.com) framework by [agenticpoa](https://github.com/agenticpoa).

## Why Jean-Claw?

The OpenClaw ecosystem is powerful and growing fast. But with 13,000+ skills on ClawHub, [341 malicious skills discovered](https://snyk.io/blog/clawhub-malicious-google-skill-openclaw-malware/) in the ClawHavoc incident, and agents that can send messages, run shell commands, and access credentials -- the attack surface is real.

Existing security tools (ClawSec, Validator Agent, Aegis Shield) solve pieces of the puzzle. Jean-Claw takes a different approach:

- **Other tools ask:** "Is this skill safe?"
- **Jean-Claw asks:** "Is this agent *authorized* to do this, right now, in this scope?"

That's the difference between security scanning and authorization governance. And because Jean-Claw is a pure markdown skill with no compiled code or external dependencies, you can read every line of what it does before you install it.

## Quick Start

No dependencies. No build step. Just copy and go.

```bash
# Install from ClawHub
npx clawhub@latest install jean-claw-van-damme

# Or manually
git clone https://github.com/agenticpoa/jean-claw-van-damme.git \
  ~/.openclaw/skills/jean-claw-van-damme

# Restart your agent session
```

That's it. Jean-Claw is a markdown skill -- your agent reads the SKILL.md and starts enforcing. Send `/jcvd status` to verify it's active.

## Core Features

### Three-Tier Action Classification

| Tier | Actions | Authorization |
|------|---------|---------------|
| **Tier 1 -- Open** | Read files, web search, summarize | No approval needed |
| **Tier 2 -- Guarded** | Send messages, install skills, run shell commands, API calls | Requires active grant or real-time approval |
| **Tier 3 -- Restricted** | Delete data, share credentials, modify agent config, financial actions | Always requires real-time approval |

### Time-Bound Authorization Grants

```
/jcvd grant send_message --scope slack:#general --ttl 2h
```

Creates a scoped, time-bound authorization. When it expires, the agent loses that permission automatically. No lingering access.

### Pre-Install Skill Scanning

```
/jcvd scan crypto-trader-pro
```

Deep analysis of any ClawHub skill before you install it:
- Prompt injection markers
- Data exfiltration patterns
- Credential access attempts
- Privilege escalation vectors
- Hidden/obfuscated execution
- Permission scope mismatches

### Prompt Injection Detection

Real-time monitoring for injection attacks in incoming messages, tool outputs, and skill instructions. Patterns detected include instruction override attempts, base64-encoded payloads, unicode homoglyphs, and nested instruction patterns.

### Full Audit Trail

Every authorization decision is logged:

```
/jcvd audit --last 10
```

### Emergency Lockdown

```
/jcvd lockdown
```

Instantly revokes all grants and requires real-time approval for everything.

## Commands

| Command | Description |
|---------|-------------|
| `/jcvd status` | Current security posture, active grants, recent audit |
| `/jcvd scan <skill>` | Deep scan a skill before installation |
| `/jcvd grant <action> [--scope] [--ttl]` | Create a time-bound authorization |
| `/jcvd revoke <id\|all>` | Revoke active grants |
| `/jcvd audit [--last n]` | View authorization audit trail |
| `/jcvd policy` | View or edit security policy |
| `/jcvd lockdown` | Emergency lockdown mode |

## APOA Framework

Jean-Claw implements the authorization model defined by [APOA (Agentic Power of Attorney)](https://agenticpoa.com), an open standard for AI agent authorization.

APOA brings legal concepts of delegated authority to the agent world:

- **Delegation** -- Users grant specific authority to agents
- **Scope Binding** -- Each grant is limited to defined actions and resources
- **Temporal Limits** -- All grants auto-expire
- **Revocation** -- Authority can be pulled instantly
- **Audit Trail** -- Every decision is accountable
- **Escalation** -- Unknown actions escalate to the human

APOA is designed to work with any agent framework. Jean-Claw is its first OpenClaw integration. For the full SDK with cryptographic token signing, delegation chains, and multi-agent authorization, see the [APOA SDK](https://github.com/agenticpoa/apoa).

**APOA GitHub:** [github.com/agenticpoa/apoa](https://github.com/agenticpoa/apoa)

## Architecture

```
jean-claw-van-damme/
  SKILL.md              -- Core skill definition and agent instructions
  README.md             -- This file
  scripts/
    scan-skill.sh       -- Skill scanning helper
    audit-export.sh     -- Export audit logs
  data/                 -- Created at runtime
    grants.json         -- Active authorization grants
    audit.json          -- Full audit trail
    policy.json         -- Security policy config
    threats.json        -- Detected threat log
    scan-results/       -- Archived scan reports
```

## Security Philosophy

> "Installing a skill is basically installing privileged code."
> -- Microsoft Security Blog

Jean-Claw operates on four principles:

1. **Default deny.** If there's no grant, there's no permission.
2. **Least privilege.** Grants are scoped to the minimum needed.
3. **Trust but verify.** Even authorized actions get logged.
4. **Full transparency.** Every line of this skill is readable markdown. No compiled code, no dependencies, no trust required beyond what you can see.

## Roadmap

Jean-Claw v0.1 is a standalone policy engine -- no external dependencies, fully readable, runs entirely within your OpenClaw agent. Future versions will integrate with the [APOA SDK](https://github.com/agenticpoa/apoa) to unlock capabilities that require real trust boundaries:

**v0.1 (current)** -- Policy engine, skill scanning, prompt injection detection, audit trail. Everything you need for a single agent.

**v0.2** -- APOA SDK integration. Cryptographically signed grants using JWT tokens. Verifiable audit trails. Scope resolution using APOA's hierarchical model.

**v0.3** -- Multi-agent delegation. When Vin spins up a sub-agent, Jean-Claw issues attenuated tokens that limit what the sub-agent can do. The delegation chain is cryptographically verifiable.

**v0.4** -- MCP middleware. APOA tokens as authorization headers on MCP tool calls. Any MCP server can verify that the calling agent has permission for the requested action.

If you're building multi-agent systems or MCP servers and need authorization now, check out the [APOA SDK](https://github.com/agenticpoa/apoa) directly.

## Contributing

Jean-Claw is open source under the MIT License. Contributions welcome.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/split-kick`)
3. Commit your changes
4. Push and open a PR

## License

MIT License. See [LICENSE](LICENSE).

## Built by

[agenticpoa](https://github.com/agenticpoa) -- Building the authorization layer for the agentic era.
