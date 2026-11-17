## Description:

Analyze JD.com workflows with JustOneAPI, including product Details, product Comments, and shop Product List.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve JD.com product details, product comments, and shop product lists through JustOneAPI when they have the required item or shop identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through process arguments or logged request URLs.

Mitigation: Use a narrowly scoped token when available, avoid logging full commands or request URLs, and rotate the token if it may have appeared in process or URL logs.

Risk: Tokens with billing, quota, or sensitive-data access increase impact if disclosed.

Mitigation: Review the skill before installation and prefer least-privilege credentials for routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-jd)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd&utm_content=project_link)
- [JD.com operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain-language Markdown summaries with selected API response fields and optional raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and operation-specific identifiers such as itemId, shopId, or page.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
