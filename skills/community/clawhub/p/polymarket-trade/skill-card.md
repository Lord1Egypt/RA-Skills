## Description:

Provides an agent-facing Polymarket trading desk alias for placing trades and managing hard, trailing, and portfolio stop protections through pinned place and guard tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to install and run a Polymarket trade desk workflow that places orders and configures protective stop behavior for funded proxy wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route Polymarket trades through third-party packages.

Mitigation: Verify the pinned npm packages independently and confirm trade routing before enabling live use.

Risk: A sell-capable private key may be used with broad triggers and limited consent safeguards.

Mitigation: Use only a segregated, least-privilege wallet and keep dry-run enabled until live exits are intentionally authorized.

Risk: Trades or protective exits may carry third-party builder attribution.

Mitigation: Review the attribution behavior and business impact before routing entries or exits through this desk.

## Reference(s):

- [polymarket-trade on ClawHub](https://clawhub.ai/polyparlay/skills/polymarket-trade)
- [NautilusTrader Polymarket integration docs](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket live examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; uses pinned @hypelens/polymarket-place 0.1.17 and @hypelens/hypelens-agent-guard 0.1.18 packages.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, scripts/package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
