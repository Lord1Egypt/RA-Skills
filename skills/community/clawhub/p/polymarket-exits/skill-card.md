## Description:

Polymarket Exits helps agents configure and run an automated sidecar for hard stops, trailing stops, portfolio stops, and heartbeat checks around Polymarket positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to add automated exit, stop-loss, trailing-stop, portfolio-stop, and heartbeat controls around Polymarket workflows that otherwise place trades without native stop support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated live exits can sell positions using wallet authority.

Mitigation: Use a dedicated least-privilege wallet or proxy with limited funds, begin in dry-run mode, and inspect the generated policy before enabling live exits.

Risk: Private keys or exit credentials may be exposed through shell history, logs, or shared environments.

Mitigation: Avoid pasting private keys into shell history or logs and run the watcher in an isolated account or container.

Risk: The external @hypelens/hypelens-agent-guard package is part of the trusted computing base.

Mitigation: Review the installed dependency and lockfile before live use and treat dependency updates as security-relevant changes.

Risk: Scope and trust boundaries are under-explained for live trading workflows.

Mitigation: Confirm the intended wallet, policy scope, dry-run status, and heartbeat behavior before increasing position size or enabling live enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polyparlay/skills/polymarket-exits)
- [Nautilus Polymarket sidecar repository referenced by the skill](https://github.com/polyparlay/nautilus-polymarket-stops)
- [NautilusTrader Polymarket integration docs](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket live examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation, setup, watcher startup, MCP use, dry-run checks, and live-exit configuration.]

## Skill Version(s):

1.0.7 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
