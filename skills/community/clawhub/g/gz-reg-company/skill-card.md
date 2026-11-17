## Description:

A Chinese-language advisor skill for Guangzhou limited-company registration that supports customer self-service Q&A, advisor-prepared registration proposals, and internal policy-response workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business advisors use this skill to understand Guangzhou limited-company registration choices, collect required client information, and prepare customer-facing registration guidance or proposal materials. It is scoped to Guangzhou limited-liability company registration and related post-registration compliance reminders.

### Deployment Geography for Use:

China, with Guangzhou-specific operating assumptions

## Known Risks and Mitigations:

Risk: The skill may request contact details or company-registration information as part of commercial lead intake.

Mitigation: Use a trusted secure channel for identity documents, phone numbers, and client materials, and confirm who will receive the information before sharing it.

Risk: Registration, tax, and fee guidance may become outdated or may not fit a specific client situation.

Mitigation: Confirm final requirements, fees, timelines, and legal or tax treatment with the relevant authorities or qualified professionals before filing or relying on proposal materials.

Risk: The workflow is scoped to Guangzhou limited-liability companies and can be inappropriate for other entity types or regions.

Mitigation: Redirect non-Guangzhou, sole-proprietor, partnership, joint-stock company, or complex regulated-industry questions to local or specialist review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xtoyun/skills/gz-reg-company)
- [README](README.md)
- [顾问版《公司注册全流程方案书》逐节模板](references/deliverable-spec.md)
- [广州本地参数](references/guangzhou-params.md)
- [信息采集字段](references/intake-fields.md)
- [名称、注册资本、经营范围与股权建议](references/naming-capital-scope.md)
- [行业证照映射](references/permit-map.md)
- [高频问答](references/faq-qa.md)
- [零申报与经营红线](references/risk-zero.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance, Configuration]

**Output Format:** [Chinese-language Markdown guidance and, in advisor mode, Word proposal content assembled from structured references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer mode provides advisory summaries and risk reminders; advisor mode can produce formal proposal content and uses pricing configuration as read-only evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
