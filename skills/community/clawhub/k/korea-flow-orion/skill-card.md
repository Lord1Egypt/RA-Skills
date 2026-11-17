## Description:

Prompts an agent to provide Korea-focused crypto market snapshots covering kimchi premium direction, Korean BTC volume status, and a concise market read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokoju007](https://clawhub.ai/user/kokoju007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to request quick Korea-focused crypto market snapshots and, when appropriate, route to Orion ACP for more detailed signal output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to produce live-looking financial market readings without defining reliable data sources, timestamps, or verification steps.

Mitigation: Require the agent to independently fetch, timestamp, and cite current exchange and FX data before presenting a market snapshot as current.

Risk: Users might act on free snapshots or signal outputs in swap or automated trading workflows.

Mitigation: Require explicit user confirmation before using any signal for swaps, automated trading, or other financial action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kokoju007/skills/korea-flow-orion)
- [Orion ACP service page](https://app.virtuals.io/virtuals/1809)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or structured JSON market snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free output is a concise snapshot; paid ACP usage may return detailed signals, top movers, swap suggestions, and structured JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
