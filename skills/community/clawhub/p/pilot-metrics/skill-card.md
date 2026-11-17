## Description:

Collect and aggregate agent metrics from connections, peers, and custom events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Pilot Protocol agent health, peer connectivity, connection activity, RTT, throughput, and custom metrics across individual agents or fleets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fleet dashboard example writes predictable files under /tmp, which can be unsafe on shared or privileged hosts.

Mitigation: Use mktemp or a private output directory before adapting the example.

Risk: The skill depends on trusted pilotctl output from the local Pilot Protocol environment.

Mitigation: Confirm pilotctl is trusted in the target environment and review command output before using it for operational decisions.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Metrics on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-metrics)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON-oriented command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, the pilot-protocol skill, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
