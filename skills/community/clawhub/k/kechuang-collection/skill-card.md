## Description:

检索固定白名单中的公开政府科创信息，按 KPI 分类并生成可人工复核的线索摘要。适用于项目申报、资质、奖励、补贴、人才、标准与创新平台线索；也支持离线 mock 演示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operations teams use this skill to search approved public Chinese government science-and-innovation sources, classify policy and program leads by KPI, and prepare human-reviewable summaries for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords may be sent to a search service and could expose confidential project names, personal data, credentials, or secrets.

Mitigation: Use only public search terms, generalize sensitive details, and avoid including confidential company, personal, credential, or secret values in queries.

Risk: Government notices may have changing deadlines, eligibility rules, links, or monetary details.

Mitigation: Manually verify deadlines, eligibility, source links, and amounts in the official notice before acting on any lead.

Risk: The workflow is scoped to public Chinese government science-and-innovation sources and may not cover other jurisdictions or non-government sources.

Mitigation: Treat the fixed whitelist as the operating boundary and review any need for additional sources outside the skill before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocxf/skills/kechuang-collection)
- [Fixed source whitelist](references/monitoring-sources.md)
- [KPI criteria and lead matching rules](references/kpi-criteria.md)
- [Quick start](references/quick-start.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and concise summaries with source links and verification status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal output is conversational; files are saved only when the user explicitly asks and provides a target path.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
