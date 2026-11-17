## Description:

Deploy a healthcare triage system with four agents for patient intake, symptom analysis, appointment scheduling, and HIPAA-compliant records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a four-agent healthcare triage setup that routes patient intake data through symptom analysis, appointment scheduling, and records management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles patient medical data with under-documented safeguards.

Mitigation: Do not use real patient data until approved PHI controls cover transport, storage, audit logs, retention, access control, and command-history or process-argument exposure.

Risk: The setup installs mutable dependencies.

Mitigation: Pin and review all required skills and binaries before deployment.

Risk: Incorrect peer identity or hostname configuration could route sensitive data to the wrong agent.

Mitigation: Verify peer identities and validate hostnames before handshakes, subscriptions, or publishing patient-related events.

Risk: Illustrative medical payloads could be mistaken for approved production test data.

Mitigation: Use synthetic test data and replace examples before any deployment review.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-healthcare-triage-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup guidance, hostnames, handshakes, subscriptions, and manifest content for a Pilot healthcare triage deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
