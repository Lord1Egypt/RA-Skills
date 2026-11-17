## Description:

Open Health Link helps users authorize a breo Scalp5 account, view scalp detection reports, retrieve scalp-care plans, and bind or unbind the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breo](https://clawhub.ai/user/breo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill in OpenClaw to connect their breo account, scan an authorization QR code, and ask an agent for recent Scalp5 scalp reports, trends, and care-plan summaries. The skill is intended for health-data access and personal care guidance, not diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable local authorization credential for breo health-account access.

Mitigation: Use it only in trusted workspaces, avoid shared or indexed machines, and clear the account binding when access is no longer needed.

Risk: Generated QR authorization images and agent execution output may expose account authorization material or health report details.

Mitigation: Treat generated QR images and report outputs as sensitive, avoid logging or sharing them, and remove temporary authorization artifacts after use.

Risk: Health report and care-plan responses may be mistaken for medical conclusions.

Mitigation: Keep responses grounded in retrieved report fields, state when information is insufficient, and present care suggestions as health-management guidance rather than diagnosis.

## Reference(s):

- [Open Health Link ClawHub Page](https://clawhub.ai/breo/skills/open-health-link)
- [Setup Guide](assets/setup-guide.md)
- [API Reference](references/api-reference.md)
- [Data Schema](references/data-schema.md)
- [breo Care Plan Catalog](https://breo-obs.obs.cn-south-1.myhuaweicloud.com/agents/plan-catalog.csv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with concise natural-language summaries; scripts emit JSON for agent-side processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include QR image file output during authorization and summarized health report or care-plan content after authorization.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
