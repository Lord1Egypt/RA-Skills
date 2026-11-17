## Description:

Nautilus-sidecar-stops helps agents run a Polymarket stop-loss, trailing-stop, and hard-stop sidecar beside a NautilusTrader process using the same funder wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to configure and run a sidecar watcher for hard stops, trailing stops, portfolio stops, and MCP heartbeat checks around NautilusTrader Polymarket activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run external trading code with wallet signing authority.

Mitigation: Use a dedicated low-balance exit signer and review the npm dependency as trusted trading software before live use.

Risk: Live stop execution can sell positions if the policy, wallet, or dry-run setting is wrong.

Mitigation: Keep dry-run enabled until the policy and wallet are verified, then monitor heartbeat status before increasing position size.

Risk: Private keys can be exposed through shell history or environment handling.

Mitigation: Avoid pasting private keys into shell history or Docker environment variables; use a safer secret-management path for live operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polyparlay/skills/nautilus-sidecar-stops)
- [Publisher profile](https://clawhub.ai/user/polyparlay)
- [NautilusTrader Polymarket documentation](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; delegates setup, watcher, and MCP startup to the pinned @hypelens/hypelens-agent-guard package.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter, scripts/package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
