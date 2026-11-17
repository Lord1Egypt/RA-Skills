## Description:

Call GET /api/douyin-xingtu/get-kol-touch-distribution/v1 for Douyin Creator Marketplace (Xingtu) Audience Touchpoint Distribution through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to call a single JustOneAPI endpoint for Douyin/Xingtu KOL audience touchpoint distribution data by kolId, summarize the segment breakdowns, and return the raw JSON for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a JustOneAPI token, and the security evidence notes that the token is passed as a process argument and URL query parameter.

Mitigation: Use a narrowly scoped, revocable token, avoid sharing command output or logs, and rotate the token if exposure is suspected.

Risk: Results depend on the external JustOneAPI service and the supplied KOL ID.

Mitigation: Confirm the KOL ID before execution and review the returned JSON before using it in traffic or audience analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-touch-distribution)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_touch_distribution&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_touch_distribution&utm_content=project_link)
- [Generated OpenAPI operations](artifact/generated/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, API calls, guidance]

**Output Format:** [Markdown summary followed by raw JSON from the API when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and JUST_ONE_API_TOKEN; endpoint input is kolId with optional acceptCache.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
