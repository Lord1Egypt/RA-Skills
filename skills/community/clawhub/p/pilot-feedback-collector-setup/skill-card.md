## Description:

Deploy a feedback collection pipeline with 3 agents that automate intake, sentiment analysis, and actionable routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer experience teams use this skill to configure a three-agent feedback workflow that collects customer feedback, scores sentiment and themes, and routes actionable items to product, engineering, or support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Bash setup commands and persistent Pilot configuration can change the local environment.

Mitigation: Inspect generated commands before execution, use a simple validated hostname prefix, and apply the setup only in the intended Pilot environment.

Risk: Unpinned skill installation can pull changing dependencies.

Mitigation: Pin and verify the installed Pilot and ClawHub skills before deploying the feedback pipeline.

Risk: Auto-approved handshakes can trust the wrong peer if hostnames are mistyped or spoofed.

Mitigation: Confirm peer identities and expected hostnames before initiating reciprocal handshakes.

Risk: Feedback routed to Slack or webhooks can expose customer identifiers or sensitive feedback.

Mitigation: Send feedback only to approved, access-controlled destinations and avoid raw customer identifiers unless explicitly permitted.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-feedback-collector-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs role-specific setup steps for intake, analyzer, and router agents, including hostname, manifest, handshake, subscription, and publish examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
