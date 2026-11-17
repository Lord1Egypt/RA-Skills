## Description:

Deploy an automated newsletter pipeline with three agents that curate content, write newsletter copy, and dispatch emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a three-agent newsletter workflow for content curation, newsletter writing, and email dispatch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead to real bulk email dispatch to subscriber segments.

Mitigation: Use test recipients first and verify the mailer cannot contact real subscriber lists until the deployment is approved.

Risk: The setup installs and runs unpinned components.

Mitigation: Pin and verify every dependency before installing skills or running setup commands.

Risk: Loose hostname input and local setup files can create operational or cleanup issues.

Mitigation: Use a simple hostname prefix containing only letters, numbers, underscores, or hyphens, and review ~/.pilot setup file permissions and cleanup procedures.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-newsletter-automation-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific setup steps for hostnames, skill installation, handshakes, subscriptions, and setup manifests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
