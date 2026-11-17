## Description:

Deploy a dev team assistant system with four agents for PR review, testing, documentation, and coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to set up a four-agent assistant workflow that reviews PRs, runs tests, drafts documentation, and coordinates status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs multiple unpinned agent integrations that may affect PR automation behavior.

Mitigation: Pin and review each dependency before installation in a controlled development environment.

Risk: The configured agents can exchange PR data and post updates through trusted handshakes.

Mitigation: Verify agent identities before handshakes and restrict GitHub and Slack credentials to the minimum required repositories and channels.

Risk: The setup writes or updates a Pilot manifest under ~/.pilot.

Mitigation: Review any existing ~/.pilot manifest before writing the new setup.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON manifest templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps for role-specific agent hostnames, skill installs, handshakes, and Pilot manifest configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
