## Description:

Analyzes security and intelligent-building tenders using historical procurement data to support bid decisions, competitor assessment, pricing, and qualification checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Bid teams and contractors assess whether to pursue a specific security or intelligent-building project, compare past awards and potential competitors, and prepare an evidence-based bid decision and pricing range.

### Deployment Geography for Use:

Global (for projects covered by Zhiliaobiaoxun procurement data)

## Known Risks and Mitigations:

Risk: Account credentials are stored locally and used for the Zhiliaobiaoxun API.

Mitigation: Review credential handling before installation and preconfigure ZLBX_API_KEY if preferred.

Risk: Trial registration collects a hashed MAC address for device deduplication.

Mitigation: Use trial registration only with informed consent; preconfiguring ZLBX_API_KEY avoids it.

Risk: Locally generated HTML reports can contain signed links to procurement records.

Mitigation: Inspect reports before sharing and send them only to intended recipients.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/intelligent-building-bid-decision)
- [Zhiliaobiaoxun skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [API tool reference](artifact/references/api-quick.md)
- [Bid-analysis workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML report]

**Output Format:** [Markdown bid-decision report and optional locally generated HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a bid recommendation, competitor and pricing analysis, cited data, and identified gaps; full analysis generates a shareable HTML report.]

## Skill Version(s):

1.0.9 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
