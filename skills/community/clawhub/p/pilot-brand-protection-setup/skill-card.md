## Description:

Deploy a brand protection system with four agents for scanning, classification, enforcement, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure a four-agent brand protection workflow for monitoring unauthorized brand usage, classifying violations, coordinating enforcement actions, and reporting brand health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports high-impact takedown, reporting, and cease-and-desist workflows that can affect third parties.

Mitigation: Require manual review and explicit authorization before any DMCA notice, platform report, or cease-and-desist request is submitted.

Risk: The setup depends on multiple referenced role skills and agent-to-agent handshakes.

Mitigation: Install only reviewed and pinned trusted skill versions, use an allowlisted hostname prefix, and verify peer identities before handshakes.

Risk: Dashboard reporting can send brand health information through Slack or webhook recipients.

Mitigation: Restrict Slack channels and webhook recipients to approved stakeholders before enabling external reports.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-brand-protection-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON manifest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, clawhub, referenced Pilot role skills, and a running daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
