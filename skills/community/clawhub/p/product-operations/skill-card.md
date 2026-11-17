## Description:

Helps product teams create operational plans, review actual campaign metrics, and prepare launch checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

Product and operations teams use this skill to turn goals into dated action plans, review user-supplied campaign metrics, generate launch checklists, and export results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product plans and summarized business metrics are sent to the AI Skills service.

Mitigation: Share only necessary metrics and avoid sensitive customer or regulated data in plans and reviews.

Risk: An exposed or overly broad API key could permit unauthorized use.

Mitigation: Use a product-specific or least-privilege key where possible; keep full keys out of chats, logs, and exports.

## Reference(s):

- [ClawHub product-operations release](https://clawhub.ai/youteacher/skills/product-operations)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/product-operations/API-KEY.md)
- [HTTP requests and task handling](https://ai-skills.open-idea.net/skill-docs/product-operations/HTTP-REQUESTS.md)
- [Operations and fields](https://ai-skills.open-idea.net/skill-docs/product-operations/OPERATIONS.md)
- [Metrics and behavior rules](https://ai-skills.open-idea.net/skill-docs/product-operations/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown guidance and checklists; optional CSV, XLSX, Markdown, or ICS exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans include tasks, dates, owners, priorities, and acceptance metrics; reviews distinguish source data, calculated metrics, and recommendations.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
