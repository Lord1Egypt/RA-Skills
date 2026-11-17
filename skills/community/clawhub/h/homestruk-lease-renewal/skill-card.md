## Description:

Tracks lease expirations and manages the 90-day renewal process by checking upcoming expirations, supporting rent increase planning, drafting renewal offers, and managing renewal negotiation timelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamsjb](https://clawhub.ai/user/adamsjb)

### License/Terms of Use:

MIT-0

## Use Case:

Self-managing landlords and property managers use this skill to identify leases expiring within 90 days, plan renewal pricing, draft tenant renewal offers, track follow-ups, and prepare vacancy workflows.

### Deployment Geography for Use:

Massachusetts, United States

## Known Risks and Mitigations:

Risk: The skill can read local tenant, property, and rent records that may contain sensitive business or personal information.

Mitigation: Install only in workspaces where the agent is authorized to access those records, and review file access expectations before use.

Risk: The skill may draft renewal offers or update renewal-related rent-roll and property status records without clear confirmation safeguards.

Mitigation: Require explicit human confirmation before sending drafts, changing rent-roll.json, or updating property status data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adamsjb/skills/homestruk-lease-renewal)
- [Publisher Profile](https://clawhub.ai/user/adamsjb)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown and structured plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May draft renewal letters and propose updates to lease-renewal tracking, rent-roll, and property status records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
