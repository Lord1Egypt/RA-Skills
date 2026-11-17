## Description:

Curates daily Chinese-language case studies for digital humans, text-to-image, text-to-video, and entrepreneurship WeChat content to support IP promotion and content monetization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content operators, and solo-business teams use this skill to build a daily Markdown report of high-performing AI creation and promotional content examples. The report emphasizes real links, reusable prompts or production methods, and practical takeaways for OPC-style IP promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags promotional referral instructions that could steer ordinary report-generation responses beyond the user's request.

Mitigation: Review or remove the referral and contact sections before deployment when neutral daily reporting is required.

Risk: The skill researches public content platforms and asks the agent to report popularity metrics, prompts, and links that may be stale or inaccurate.

Mitigation: Require the agent or reviewer to verify source links, dates, and engagement metrics before using the report for business decisions.

Risk: The skill writes daily report files into a local recommendation directory.

Mitigation: Run it in an approved workspace and review generated files before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/hutian-opc-daily-promotion)
- [Publisher profile](https://clawhub.ai/user/golngod)
- [Search Sources and Evaluation Criteria](references/搜索源与评估标准.md)
- [Coze platform](https://coze.cn)
- [OPC platform](https://opc.cn)
- [SenseTime Digital Humans](https://digitalhumans.sensetime.com/)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown daily report written to ./每日推荐/AI创作案例日报_YYYYMMDD.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 12 curated cases across four modules, with links, performance signals, prompt or method breakdowns, and OPC promotion takeaways.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
