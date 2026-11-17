## Description:

pm-desk helps agents set up a Polymarket trading desk for order placement with protective hard stops, trailing stops, and portfolio stop workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to install a Polymarket desk, configure a funded wallet, run placement and guard services, and operate stop-loss workflows around positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for live trading authority and private-key handling.

Mitigation: Use a dedicated low-balance exit key, avoid long-lived shell environment secrets, and review the setup before enabling live mode.

Risk: The watcher may submit real SELL orders through the trading tooling.

Mitigation: Do not enable live mode or the watcher until the operator understands and accepts the order-submission behavior.

Risk: The release depends on external npm packages used for placement and guard behavior.

Mitigation: Verify the npm package names and pinned versions before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polyparlay/skills/pm-desk)
- [NautilusTrader Polymarket integration docs](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket live examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.18 (source: frontmatter, scripts/package.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
