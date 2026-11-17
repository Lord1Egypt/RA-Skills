## Description:

Call GET /api/amazon/get-product-top-reviews/v1 for Amazon Product Top Reviews through JustOneAPI with asin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call JustOneAPI's Amazon top reviews endpoint for an ASIN and summarize review data relevant to sentiment analysis, product research, quality assessment, and competitor customer experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command lines, process telemetry, command history, URL logs, proxy logs, or API logs.

Mitigation: Use a narrowly scoped and revocable token, avoid sharing logs or traces from runs, and rotate the token if exposure is possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-amazon-get-product-top-reviews)
- [JustOneAPI publisher profile](https://clawhub.ai/user/justoneapi)
- [JustOneAPI API homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_top_reviews&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_top_reviews&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown summary with endpoint details followed by raw JSON when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and an asin query value; country is optional and defaults to US.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
