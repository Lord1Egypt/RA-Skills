## Description:

Deploy a four-agent fraud detection pipeline for real-time transaction monitoring, behavioral analysis, case investigation, and enforcement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and fraud operations teams use this skill to configure a four-agent Pilot Protocol pipeline that screens transactions, escalates high-risk cases, assembles evidence, and coordinates enforcement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can configure high-impact fraud enforcement workflows such as blocklists, account freezes, transaction declines, reversals, and webhooks.

Mitigation: Require human approval before any enforcement action and test the workflow in a sandbox or non-production environment before operational use.

Risk: The setup installs role-specific Pilot skills without pinned versions.

Mitigation: Pin and verify every installed Pilot skill before deployment.

Risk: Incorrect peer trust can expose transaction or enforcement messages to the wrong agent.

Mitigation: Confirm peer identities manually before trusting agents or exchanging handshakes.

Risk: The local setup manifest may overwrite an existing `~/.pilot/setups/fraud-detection-pipeline.json` file or expose sensitive workflow configuration.

Mitigation: Check for an existing manifest before writing and restrict access to the manifest file.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-fraud-detection-pipeline-setup)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation of role-specific skills, peer handshakes, hostnames, and a local Pilot setup manifest.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
