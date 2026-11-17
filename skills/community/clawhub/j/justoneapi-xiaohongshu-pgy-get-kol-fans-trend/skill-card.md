## Description:

Call GET /api/xiaohongshu-pgy/get-kol-fans-trend/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History through JustOneAPI with dateType, increaseType, and kolId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace follower growth history endpoint for creator evaluation, campaign planning, and benchmarking. It requires a JustOneAPI token plus kolId, dateType, and increaseType query parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token may be exposed through command-line arguments or URL query logs.

Mitigation: Use a narrowly scoped token where possible, avoid sharing command transcripts or logs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justoneapi/skills/justoneapi-xiaohongshu-pgy-get-kol-fans-trend)
- [JustOneAPI homepage](https://api.justoneapi.com)
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_trend&utm_content=project_link)
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_trend&utm_content=project_link)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown summary followed by raw JSON from the API when the endpoint succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses operation getKolFansTrendV1 on /api/xiaohongshu-pgy/get-kol-fans-trend/v1 and echoes the lookup scope before summarizing results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
