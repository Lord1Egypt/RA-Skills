## Description:

Deploys a customer onboarding system with three agents that automate the new customer journey from welcome through setup to success tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success, onboarding, and developer operations teams use this skill to configure a three-agent Pilot Protocol workflow for welcome conversations, setup milestone tracking, and adoption health reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run shell setup commands and install dependent skills without pinned versions.

Mitigation: Review commands before execution and pin or verify every dependency before installing in a customer environment.

Risk: The skill persists hostnames, setup manifests, and trust configuration.

Mitigation: Restrict prefixes to safe hostname characters and review configuration changes before writing them to local Pilot state.

Risk: The workflow requires peer handshakes before agents exchange customer onboarding data.

Mitigation: Confirm peer identities and intended roles before initiating or accepting handshakes.

Risk: The success-tracker role can send customer health reports to external webhook, dashboard, or Slack destinations.

Mitigation: Send only minimized customer data to approved destinations with appropriate consent and retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-customer-onboarding-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with Bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides one selected onboarding role setup at a time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
