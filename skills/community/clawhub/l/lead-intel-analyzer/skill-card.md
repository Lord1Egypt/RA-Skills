## Description:

Generates actionable B2B sales intelligence reports with company insights, target-persona analysis, pain points, sales opportunities, and personalized outreach angles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syed-tahmid99](https://clawhub.ai/user/syed-tahmid99)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and go-to-market users use this skill to prepare concise lead intelligence for cold outreach, lead qualification, and personalized prospecting. The skill is triggered with a company name plus optional website and target persona, then returns a structured report suitable for outreach planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead inputs and any provided API key are sent to the publisher's external backend.

Mitigation: Avoid entering confidential prospect notes, sensitive credentials, or regulated personal data unless the backend and its data practices have been reviewed and trusted.

Risk: The skill depends on a live external backend for enriched lead reports.

Mitigation: Treat backend outages or failed responses as availability failures and retry later rather than relying on partial or stale output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/syed-tahmid99/skills/lead-intel-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown lead intelligence report with section headings and bullet lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a company name, accepts optional website URL and target persona, and may call a disclosed external backend using a user-provided access token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
