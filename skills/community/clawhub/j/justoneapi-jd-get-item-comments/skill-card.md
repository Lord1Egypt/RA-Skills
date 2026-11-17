## Description:

Call GET /api/jd/get-item-comments/v1 for JD.com Product Comments through JustOneAPI with itemId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to fetch JD.com product comment data through JustOneAPI for customer feedback analysis and product research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command lines, URLs, logs, screenshots, or command history.

Mitigation: Use a narrowly scoped, revocable token, avoid sharing run logs or command history, and rotate the token if exposure is suspected.

Risk: Using the skill sends requests and lookup parameters to api.justoneapi.com.

Mitigation: Install and run the skill only when sharing the required product identifier and API token with JustOneAPI is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-jd-get-item-comments)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_comments&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_item_comments&utm_content=project_link)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary followed by raw JSON API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and itemId; page is optional for pagination.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
