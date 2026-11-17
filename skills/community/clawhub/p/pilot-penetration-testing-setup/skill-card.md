## Description:

Deploy an automated penetration testing pipeline with 4 agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers and developers use this skill to configure a four-agent penetration testing workflow for authorized reconnaissance, vulnerability scanning, exploit validation, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup is intended for penetration testing and could be misused outside an authorized assessment.

Mitigation: Use it only for approved security assessments with defined targets, scope, and authorization.

Risk: The setup installs dependency skills without pinned versions.

Mitigation: Pin and verify dependency skills before installation.

Risk: Prefix and role placeholders can lead to unsafe or unintended shell and hostname values.

Mitigation: Restrict prefix and role values to reviewed, known-safe names before running setup commands.

Risk: Reports may contain sensitive penetration test findings and can be sent to Slack or webhook destinations.

Mitigation: Review report content and send it only to approved Slack or webhook destinations.

Risk: Peer handshakes can establish trust between the wrong agents if identities are not checked.

Mitigation: Verify peer identities before handshakes and remove ~/.pilot/setups/penetration-testing.json when the deployment is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-penetration-testing-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup steps for a four-agent pipeline and a local penetration-testing manifest.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
