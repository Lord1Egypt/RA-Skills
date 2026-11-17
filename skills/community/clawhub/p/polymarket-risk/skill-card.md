## Description:

Provides ClawHub agent guidance and setup commands for a Polymarket stop-loss sidecar covering hard stops, trailing stops, portfolio stops, heartbeat checks, and protective exits where native stops are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyparlay](https://clawhub.ai/user/polyparlay)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators building ClawHub agents for Polymarket use this skill to add stop-loss, trailing-stop, portfolio-stop, heartbeat, and exit-protection guidance around trading positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watcher can automatically sell positions when live exits are enabled.

Mitigation: Use an isolated low-value exit wallet and keep dry-run behavior unless the operator explicitly understands and accepts live exit behavior.

Risk: The skill depends on external trading code and has install and launcher risks.

Mitigation: Verify the external package source and lockfile before installing or running the watcher.

Risk: The Docker/archive setup snippet is flagged as needing correction.

Mitigation: Avoid the Docker/archive snippet until it is fixed and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/polyparlay/skills/polymarket-risk)
- [Nautilus Polymarket Stops Sidecar](https://github.com/polyparlay/nautilus-polymarket-stops)
- [NautilusTrader Polymarket Integration Docs](https://nautilustrader.io/docs/latest/integrations/polymarket/)
- [NautilusTrader Polymarket Examples](https://github.com/nautechsystems/nautilus_trader/tree/develop/examples/live/polymarket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; live exits require explicit operator configuration and wallet handling.]

## Skill Version(s):

1.0.7 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
