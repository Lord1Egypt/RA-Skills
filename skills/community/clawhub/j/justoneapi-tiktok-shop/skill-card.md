## Description:

Analyze TikTok Shop workflows with JustOneAPI, including product Search and product Details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and commerce teams use this skill to search TikTok Shop products and retrieve product details through JustOneAPI for market research, catalog building, price and stock monitoring, and product popularity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token is passed through command arguments and query parameters, which may expose it in process metadata, logs, shell history, or full request URLs.

Mitigation: Use a narrowly scoped token, avoid shell tracing and command logging, do not paste tokens into shared outputs, and rotate the token if it may have been logged.

Risk: The skill returns API-backed TikTok Shop product data whose completeness and freshness depend on JustOneAPI and the upstream TikTok Shop source.

Mitigation: Treat returned product fields as point-in-time API results and verify high-impact business decisions against authoritative sources before acting.

## Reference(s):

- [TikTok Shop operations](generated/operations.md)
- [JustOneAPI API homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-tiktok-shop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN for authenticated JustOneAPI requests.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
