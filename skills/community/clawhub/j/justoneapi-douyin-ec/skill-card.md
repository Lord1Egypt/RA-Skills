## Description:

Analyze Douyin E-commerce workflows with JustOneAPI, including item Details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Douyin E-commerce item details through JustOneAPI when they have an itemId and need an API-backed answer for product monitoring or competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through process listings or URL logs.

Mitigation: Use a narrowly scoped, short-lived token when available, avoid shared systems where command arguments may be visible, and rotate the token if command or URL logs may have captured it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-ec)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec&utm_content=project_link)
- [Douyin E-commerce operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Markdown response with API-backed JSON details when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Douyin E-commerce itemId.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
