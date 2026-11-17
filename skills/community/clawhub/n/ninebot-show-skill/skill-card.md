## Description:

Read-only Ninebot/九号 electric vehicle status and report skill that queries battery, range, charging state, smart-service days, location, rides, recent ride details, and generates map or ride-track images through a locally authenticated ninecli session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzhe2333](https://clawhub.ai/user/zzzhe2333)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect a Ninebot/九号 vehicle's current status, ride history, location, and service state from a local authenticated ninecli session. It also supports optional report, static map, and ride-track image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local agent can read Ninebot vehicle status, rides, and location through an already authenticated ninecli session.

Mitigation: Install only where that local access is acceptable, and keep Ninebot credentials and tokens out of chat, public files, logs, and examples.

Risk: Map and ride-visualization features may send location or route-area data to third-party map services.

Mitigation: Use privacy=off or avoid map commands when location sharing is not acceptable; use district mode when approximate location is sufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zzzhe2333/skills/ninebot-show-skill)
- [Configuration](artifact/references/configuration.md)
- [Network Requests and Privacy](artifact/references/network-privacy.md)
- [Safe Public Example Data](artifact/references/example-data.md)
- [Privacy and Publication Notes](artifact/PRIVACY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Image files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands, optional JSON reports, and generated PNG map or ride-track files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only vehicle reporting; location output depends on configured privacy mode.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
