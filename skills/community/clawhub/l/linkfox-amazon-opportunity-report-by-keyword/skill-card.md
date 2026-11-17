## Description:

Generates AI-assisted Amazon US keyword opportunity reports covering market potential, product attributes, customer reviews, customer profiles, search trends, and pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce researchers use this skill to generate point-in-time US marketplace opportunity reports for keyword-level product selection and market entry decisions.

### Deployment Geography for Use:

Global use; report coverage is limited to the Amazon US marketplace.

## Known Risks and Mitigations:

Risk: The skill handles sensitive login, OTP, API-key, and payment flows.

Mitigation: Use only in a trusted environment, avoid pasting OTPs or API keys into shared logs, prefer secure secret storage, and require explicit confirmation before payment or order actions.

Risk: Endpoint override environment variables can redirect service calls.

Mitigation: Avoid endpoint override environment variables unless the operator controls and trusts the endpoint.

Risk: Feedback submission may disclose user experience details outside the immediate task flow.

Mitigation: Require explicit confirmation before submitting feedback.

Risk: The report service may consume paid compute credits.

Mitigation: Tell users about potential compute-credit cost before running the report and avoid repeated retries or parameter changes without consent.

## Reference(s):

- [亚马逊商业洞察报告 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-opportunity-report-by-keyword)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown report returned in a JSON response, with full responses saved as JSON files and concise stdout summaries for larger results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inputs are site and keyword; site currently supports US only. The script uses a 24-hour local cache and may consume paid compute credits.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
