## Description:

Provides agent-facing setup guidance and launch scripts for running a NautilusTrader Polymarket stop-loss, trailing-stop, and hard-stop sidecar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading bot operators use this skill to attach a stop-management sidecar to a NautilusTrader Polymarket deployment where native stop order types are not supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading setup may expose or misuse private keys for protective sell orders.

Mitigation: Use a dedicated low-balance exit key, keep dry-run enabled until manually verified, and avoid placing private keys in shell history or compose files.

Risk: Trade-routing and builder-attribution defaults may affect how orders are routed or attributed.

Mitigation: Review builder-attribution and entry-routing behavior before accepting defaults.

Risk: Stop behavior runs as an external sidecar beside Nautilus rather than as native Polymarket stop orders.

Mitigation: Verify watcher heartbeat, dry-run behavior, and policy settings before increasing position size.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polyparlay/skills/nautilus-polymarket-stops)
- [NautilusTrader Polymarket integration docs](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Node/npm setup commands and watcher/MCP launch guidance; no structured machine-readable output is promised.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter, scripts/package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
