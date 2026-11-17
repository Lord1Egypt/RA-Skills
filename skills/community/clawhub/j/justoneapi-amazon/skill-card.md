## Description:

Analyze Amazon workflows with JustOneAPI, including product Details, product Top Reviews, and best Sellers across 4 operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Amazon product details, top reviews, best-seller listings, and category product data through JustOneAPI when they can provide ASINs, categories, or filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line arguments and request URLs.

Mitigation: Run the helper only in trusted environments, avoid logging full commands or URLs, and rotate the token if it may have appeared in logs or process telemetry.

Risk: Authenticated API calls may affect account quota, spending, or other account state tied to the JustOneAPI token.

Mitigation: Review token permissions and account impact before installing or using the skill, especially in shared or automated environments.

## Reference(s):

- [ClawHub Amazon API Skill](https://clawhub.ai/justoneapi/skills/justoneapi-amazon)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon&utm_content=project_link)
- [Amazon Operations Reference](generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown answer with optional JSON API payload and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should summarize decision-relevant fields, echo supplied filters, and include backend error payloads with the operation ID when requests fail.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
