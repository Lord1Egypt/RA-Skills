# Guard-Scanner Glossary

Security terms used in guard-scanner, with standard equivalents.

## Agent-Native Terms

| Term | Standard Equivalent | Description |
|------|---------------------|-------------|
| SOUL.md | Identity / persistent-memory control file | A configuration file that defines an AI agent's persistent behavior, personality, and rules. Overwriting it can hijack the agent's identity. |
| ClawHavoc | Agent skill supply-chain attack | An attack vector where malicious packages in a skill marketplace (e.g., ClawHub, npm) target AI agents, similar to typosquatting in package managers. |
| ZombieAgent | Persistent rogue agent | An agent process that persists beyond its intended lifecycle, maintaining unauthorized access or executing hidden tasks. |
| Soul Hijack | Agent identity takeover | An attack that overwrites an agent's identity file to change its behavior, bypass safety rules, or impersonate another agent. |
| Moltbook | Third-party agent marketplace (ClawHub/npm) | External skill registries where users can discover and install agent capabilities. These are supply-chain attack surfaces. |
| GuavaSuite | Agent runtime ecosystem | The full stack of tools, memory layers, and security infrastructure used by the Guava AI agent. |

## Threat Categories (OWASP-Aligned)

| Category ID | Description | OWASP Mapping |
|-------------|-------------|---------------|
| prompt-injection | Attempts to override system instructions | ASI01 — Agent Goal Hijack |
| reverse-shell | Remote shell access attempts | ASI05 — Remote Code Execution |
| data-exfiltration | Unauthorized data transfer to external servers | ASI05 — RCE / ASI04 — Supply Chain |
| social-engineering | Trust exploitation and human manipulation | ASI09 — Human-Trust Exploitation |
| malicious-code | Known malicious patterns (eval, exec, etc.) | ASI05 — RCE |
| soul-lock | Identity file tampering attempts | ASI03 — Identity Abuse |
| memory-poisoning | Attempts to corrupt agent memory/context | ASI06 — Memory Poisoning |
| tool-shadowing | MCP tool description containing hidden instructions | ASI02 — Tool Misuse |
| context-crush | Prompt overstuffing to push instructions out of context | ASI01 — Agent Goal Hijack |

## Severity Levels

| Level | Risk Weight | Meaning |
|-------|------------|---------|
| CRITICAL | 40 | Immediate threat — active exploitation attempt |
| HIGH | 15 | Dangerous pattern — likely malicious |
| MEDIUM | 5 | Suspicious pattern — needs review |
| LOW | 2 | Informational — minor concern |

## Verdicts

| Verdict | Risk Range | Action |
|---------|-----------|--------|
| CLEAN | 0 | No threats detected |
| SAFE | 1-19 | Low risk, safe to use |
| SUSPICIOUS | 20-79 | Review recommended |
| MALICIOUS | 80+ | Block / quarantine |
