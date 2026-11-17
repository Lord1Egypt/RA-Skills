## Description:

扫描公开采购意向、拟建项目和临期续约信息，按价值排序并给出跟进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and business development teams use this skill to find and prioritize early-stage procurement opportunities in China, track tender progress, and plan outreach before bidding begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party procurement service receives search terms and uses an API key stored locally or supplied through the environment.

Mitigation: Review the service before use; prefer a manually configured API key and keep credentials out of reports and chat.

Risk: Free-trial registration sends a hashed device identifier to the service.

Mitigation: Obtain user consent before registration, or use an existing manually configured API key to skip registration.

Risk: Signed access links can appear in chat and shareable HTML reports; the HTML renderer needs URL-safety fixes.

Mitigation: Avoid sharing reports containing signed links, and review or fix URL handling before distributing generated HTML.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dragonzu/skills/procurement-intent-monitor)
- [Skill workflow](references/workflow.md)
- [API quick reference](references/api-quick.md)
- [Report format](references/report-template.md)
- [Credential setup and registration](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML report]

**Output Format:** [Prioritized Markdown opportunity list; shareable HTML file in full-scan mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes data dates, source links, ranking rationale, and suggested next actions.]

## Skill Version(s):

1.0.8 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
