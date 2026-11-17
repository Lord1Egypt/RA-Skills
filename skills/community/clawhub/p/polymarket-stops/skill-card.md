## Description:

Polymarket Stops helps agents configure and run a sidecar for hard, trailing, and portfolio stop exits on Polymarket positions where native stop orders are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-agent operators use this skill to add stop-loss, trailing-stop, portfolio-stop, heartbeat, and watcher guidance around Polymarket place-only agents before increasing live position size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading automation can place protective sells with signing-key access.

Mitigation: Use a dedicated, low-balance wallet and keep the watcher in dry-run until the setup and policy are verified.

Risk: Private keys supplied through shell or container environment variables can be exposed through process state, shell history, or logs.

Mitigation: Avoid environment variables for private keys where possible and use a local secret manager or narrowly scoped runtime secret injection.

Risk: Direct npx or runtime npm install paths can execute package code outside a reviewed local install.

Mitigation: Prefer lockfile-based local installs and review pinned package versions before running setup, MCP, or watcher commands.

Risk: Builder attribution may have commercial or operational implications for live exits.

Mitigation: Confirm whether the configured builder attribution is acceptable or configurable before enabling live exits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/polyparlay/skills/polymarket-stops)
- [Nautilus Polymarket Stops Compose Reference](https://github.com/polyparlay/nautilus-polymarket-stops)
- [NautilusTrader Polymarket Integration Docs](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket Live Examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on Node/npm setup, MCP or watcher startup, dry-run operation, and live-exit configuration.]

## Skill Version(s):

1.0.15 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
