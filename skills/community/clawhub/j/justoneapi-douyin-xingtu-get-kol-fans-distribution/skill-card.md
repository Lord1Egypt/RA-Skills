## Description:

Call GET /api/douyin-xingtu/get-kol-fans-distribution/v1 for Douyin Creator Marketplace (Xingtu) Follower Distribution through JustOneAPI with kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and marketplace operators use this skill to retrieve Douyin Creator Marketplace (Xingtu) follower distribution data for a specified KOL ID. The returned audience demographics, interests, and distribution metrics can support creator evaluation, campaign planning, and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line arguments, URLs, process telemetry, proxy logs, or request logs.

Mitigation: Use a narrowly scoped token where possible, avoid environments that log full command lines or URLs, and rotate the token if exposure is suspected.

Risk: Follower distribution data from the backend can be incomplete, stale, or unsuitable for campaign decisions without review.

Mitigation: Confirm the kolId and fansType inputs, review backend errors and raw JSON, and validate important findings before using the data for creator evaluation or campaign planning.

## Reference(s):

- [Generated operation reference](generated/operations.md)
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_fans_distribution&utm_content=project_link)
- [JustOneAPI API homepage](https://api.justoneapi.com)
- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-douyin-xingtu-get-kol-fans-distribution)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Concise Markdown summary followed by raw JSON when requested or after endpoint-specific summarization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token and a kolId query parameter; optional fansType and acceptCache query parameters are supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
