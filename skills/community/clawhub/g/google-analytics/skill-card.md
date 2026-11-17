## Description:

Helps agents run Google Analytics reports and, with explicit approval, manage analytics accounts, properties, and data streams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Analytics teams and developers use this skill to retrieve Google Analytics reports and, when explicitly authorized, update analytics configuration or set up automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Admin API changes can affect live analytics accounts and data collection.

Mitigation: Prefer the read-only Data API for reports; obtain explicit approval and confirm exact account, property, or data stream IDs before changes.

Risk: Hosted functions and triggers can continue running after setup or send data to unintended destinations.

Mitigation: Review and approve each automation, its schedule or event source, and its destinations before enabling it.

Risk: Exposed Maton or provider credentials could permit unauthorized account access.

Mitigation: Keep credentials out of shared output and logs, and authorize only the access needed for the task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/google-analytics)
- [Maton](https://maton.ai)
- [Google Analytics Admin API overview](https://developers.google.com/analytics/devguides/config/admin/v1)
- [Google Analytics Data API overview](https://developers.google.com/analytics/devguides/reporting/data/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use the read-only Data API; administrative changes require explicit user approval.]

## Skill Version(s):

1.2.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
