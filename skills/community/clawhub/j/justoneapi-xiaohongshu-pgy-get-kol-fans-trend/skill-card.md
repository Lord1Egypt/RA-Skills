## Description: <br>
Call GET /api/xiaohongshu-pgy/get-kol-fans-trend/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History through JustOneAPI with dateType, increaseType, and kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketers, and creator-analytics teams use this skill to call JustOneAPI's Xiaohongshu Pugongying follower growth history endpoint for creator evaluation, campaign planning, and benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token may be exposed through logs, shell history, process listings, or error output. <br>
Mitigation: Use a scoped token when possible, avoid pasting token values into chat or logs, and review command output before sharing it. <br>
Risk: The release was flagged suspicious by the authoritative security scan despite its narrow read-only API scope. <br>
Mitigation: Review the helper before installing and use it only in an environment where exposure of the configured JustOneAPI token would be acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-get-kol-fans-trend) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_trend&utm_content=project_link) <br>
- [Xiaohongshu Pugongying Follower Growth Operations](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response and optional shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token plus kolId, dateType, and increaseType query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
