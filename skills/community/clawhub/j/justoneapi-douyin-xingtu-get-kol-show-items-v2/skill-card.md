## Description:

Call GET /api/douyin-xingtu/get-kol-show-items-v2/v1 for Douyin Creator Marketplace (Xingtu) Showcase Items through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch Douyin Creator Marketplace (Xingtu) showcase item data for a creator by KOL ID. The returned data supports creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token can be exposed through command arguments or URL query logs.

Mitigation: Use a short-lived, revocable, least-privilege token; avoid shell tracing or command logging; rotate the token after use when process arguments or outbound URLs may be recorded.

Risk: The skill sends requests to a third-party JustOneAPI service.

Mitigation: Install and run it only when the user trusts JustOneAPI with the token and requested KOL lookup data.

## Reference(s):

- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_show_items_v2&utm_content=project_link)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_show_items_v2&utm_content=project_link)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-show-items-v2)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a JUST_ONE_API_TOKEN; required lookup input is kolId.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
