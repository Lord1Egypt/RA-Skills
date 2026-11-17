## Description:

Call GET /api/amazon/get-best-sellers/v1 for Amazon Best Sellers through JustOneAPI with category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to call JustOneAPI's Amazon Best Sellers endpoint for category-based product rankings, metadata, and pricing. It supports category research, market analysis, and sales-rank tracking through a focused API wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the JustOneAPI token as a query parameter and accepts it on the command line, which can expose it through logs, shell history, or process metadata.

Mitigation: Use a narrowly scoped or disposable token where available, avoid shared shells and CI logs, and rotate the token if command-line or URL logging may have captured it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-amazon-get-best-sellers)
- [JustOneAPI homepage](https://api.justoneapi.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; required query scope is category, with optional country and page parameters.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
