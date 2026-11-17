## Description:

Searches Walmart US products by natural-language name and retrieves Sorftime-backed product details, historical trends, and daily or variant sales rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce analysts use this skill to discover related Walmart US products, inspect known product IDs, and summarize product trend or sales-volume data returned by Sorftime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint or credential environment variables could be altered by untrusted parties.

Mitigation: Install and run the skill only in trusted environments where LinkFox endpoint variables and API-key variables are controlled by the user or administrator.

Risk: Onboarding, API keys, payment QR files, cached responses, and saved product-analysis files may expose sensitive account or commerce data.

Mitigation: Avoid shared logs or transcripts unless secrets are redacted, and treat local linkfox cache, payment, and response files as sensitive artifacts.

Risk: The skill includes account, billing, and payment flows.

Mitigation: Prefer a separate, explicit account and billing workflow, and require user confirmation before purchase or recharge actions.

Risk: Follow-up operations, pagination, or changed date ranges can consume additional paid credits.

Mitigation: Reuse cached responses when parameters are unchanged and ask for user authorization before making extra paid calls.

Risk: Feedback reporting can send behavior or result-quality information outside the local session.

Mitigation: Require confirmation for feedback reporting or disable it where organizational policy requires explicit telemetry approval.

## Reference(s):

- [Walmart 产品分析 API 参考](artifact/references/api.md)
- [解决认证和积分问题](artifact/references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-walmart-product-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with JSON API responses and saved response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved under the local linkfox session data directory; larger responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
