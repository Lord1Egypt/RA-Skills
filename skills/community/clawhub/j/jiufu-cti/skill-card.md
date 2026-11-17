## Description:

Queries a third-party CTI product traceability API to assess consumer product trust, certifications, penalties, enterprise background, and quality signals across product categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiang19680401](https://clawhub.ai/user/jiang19680401)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check product or brand trustworthiness by submitting product, brand, and category details to a third-party CTI verification API. The response is summarized as a grade, score, key findings, and risk alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied product and brand query details are sent to jiufu-trace.cn.

Mitigation: Use the skill only when the third-party API's data handling is acceptable, and avoid entering sensitive business, purchase, or investigation context.

Risk: The skill relies on broad shell execution and raw curl construction for API calls.

Mitigation: Prefer a constrained HTTP client or JSON serializer before deployment, and review generated commands before execution.

Risk: CTI results are based on public data and a third-party API that may be incomplete or stale.

Mitigation: Treat results as informational, verify high-impact findings with authoritative sources, and present risk alerts clearly.

## Reference(s):

- [Jiufu CTI verification API endpoint](https://jiufu-trace.cn/api/cti/verify)
- [ClawHub skill page](https://clawhub.ai/jiang19680401/skills/jiufu-cti)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown summary with CTI grade, score, key findings, risk alerts, and optional curl command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses product_name and brand inputs, with optional category and depth.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
