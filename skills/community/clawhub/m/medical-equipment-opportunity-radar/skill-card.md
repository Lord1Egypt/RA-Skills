## Description:

按产品和地区搜索医院拟建项目、采购意向与临期续约机会，按价值排序并给出跟进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Medical equipment sales and procurement teams use this skill to identify early hospital purchasing opportunities in China and prioritize outreach based on project stage, budget, and contract timing.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Search terms are sent to a third-party service; optional registration transmits device-derived identifiers.

Mitigation: Share only necessary search criteria, supply an existing API key when possible, and consent to auto-registration only if comfortable with device-derived data collection.

Risk: API credentials may persist locally, and shared report links may grant access to underlying announcements.

Mitigation: Provide the API key through a trusted secret mechanism, review stored credentials in ~/.zlbx/config.json, and restrict sharing of reports or chat logs containing signed links.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dragonzu/skills/medical-equipment-opportunity-radar)
- [Skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Search workflow](artifact/references/workflow.md)
- [Report template](artifact/references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML report, Guidance]

**Output Format:** [Ranked Markdown opportunity list with an optional shareable HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source announcement links and recommended follow-up actions; full scans can also save a local HTML report.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
