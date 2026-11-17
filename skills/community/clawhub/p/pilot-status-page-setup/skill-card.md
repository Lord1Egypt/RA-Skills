## Description:

Deploy a status page pipeline with three agents that automate service monitoring, status aggregation, and public incident communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure a three-agent pipeline for endpoint monitoring, status aggregation, public status page updates, and incident notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs multiple role-specific dependencies that may change over time.

Mitigation: Use pinned, trusted dependency versions and review each installed skill before deployment.

Risk: The setup establishes trust between monitoring, aggregation, and publishing agents.

Mitigation: Validate the deployment prefix and verify each peer identity before completing handshakes.

Risk: Incident data can be published to public status pages, subscriber email, and Slack.

Mitigation: Restrict and review incident fields before publication so sensitive operational details are not exposed.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON manifests and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, role-specific Pilot skills, and a running daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
