## Description:

Google Analytics 4 data analysis and reporting via google-analytics-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to query GA4 accounts and properties, run traffic and behavior reports, monitor realtime activity, and inspect analytics configuration from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing google-analytics-cli globally without pinning a package version.

Mitigation: Review npm package provenance before installation and prefer a pinned, isolated install.

Risk: GA4 access reports and audience exports can expose sensitive identifiers such as emails, device IDs, or user IDs.

Mitigation: Use least-privilege service account credentials and require explicit approval before commands that may return sensitive user-level data.

Risk: The security verdict flags the release as suspicious because sensitive export commands are present despite read-only positioning.

Mitigation: Review the skill before deployment and limit credentials to only the GA4 properties needed for the task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bin-huang/skills/google-analytics-cli)
- [google-analytics-cli documentation](https://github.com/Bin-Huang/google-analytics-cli)
- [GA4 Data API overview](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [Dimensions and metrics reference](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [Realtime API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-api-schema)
- [GA4 Admin API](https://developers.google.com/analytics/devguides/config/admin/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GA4 report outputs in JSON when commands are executed by the agent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
