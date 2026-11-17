## Description:

Deploys a three-agent podcast production pipeline for research, production, and distribution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a three-agent Pilot Protocol podcast workflow that moves episode ideas from research to production packaging and distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent setup manifests and hostname changes can affect an existing Pilot deployment.

Mitigation: Inspect existing ~/.pilot/setups state and validate the deployment prefix with a strict hostname-safe pattern before writing manifests or changing hostnames.

Risk: The workflow installs additional skills and establishes trust relationships between agents.

Mitigation: Pin and verify every installed skill, then manually confirm all trust relationships before using the workflow with real content.

Risk: The distributor role can send publish notifications to external podcast, social, and webhook destinations.

Mitigation: Use test publishing credentials and non-public destinations until the workflow and all external targets are verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-podcast-production-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON setup manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup steps for researcher, producer, and distributor agents.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
