## Description:

Deploy an automated code review pipeline with three agents that scan pull requests, analyze code quality, and report review results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to configure a three-agent code review workflow for pull request scanning, review analysis, and reporting to development channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs multiple helper skills without pinned versions.

Mitigation: Pin and verify helper skills before using the pipeline in a real repository environment.

Risk: Trusted agent handshakes and deployment prefixes may be accepted without enough validation.

Mitigation: Validate deployment prefixes and verify peer identities before running handshake commands.

Risk: Review findings and repository details may be sent to broad channels or unapproved external endpoints.

Mitigation: Restrict GitHub and Slack credentials to the minimum required scope and approve reporting channels or webhooks before sending results.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-code-review-pipeline-setup)
- [Publisher Profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup instructions, command examples, hostnames, handshakes, and JSON setup manifests.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
