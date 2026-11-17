## Description:

Finds early IT procurement opportunities in China across proposed projects, purchasing intentions, and upcoming service renewals, then ranks leads and suggests follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business development teams use this skill to identify and prioritize Chinese IT and domestic-technology procurement leads by sector, product, and region, with suggested next steps for each opportunity.

### Deployment Geography for Use:

Global (opportunity data focuses on China)

## Known Risks and Mitigations:

Risk: The third-party service uses an API key and may store it locally or create a trial account using a hashed device identifier.

Mitigation: Review account and privacy terms before use; preconfigure ZLBX_API_KEY to avoid auto-registration, and consent before any device collection.

Risk: API queries can consume account credits, and generated HTML reports persist locally.

Mitigation: Confirm expected query costs and review report contents and storage location before sharing.

Risk: The security review flags hidden request instructions and potentially incomplete or misleading opportunity data.

Mitigation: Review the skill before installation and verify material leads against the linked source records before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/it-project-opportunity-radar)
- [API quick reference](artifact/references/api-quick.md)
- [Opportunity scanning workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML reports, Guidance]

**Output Format:** [Ranked Markdown opportunity list and optional local HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, priority reasons, data gaps, and suggested follow-up actions.]

## Skill Version(s):

1.0.8 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
