## Description: <br>
Call GET /api/xiaohongshu-pgy/get-kol-fans-summary/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Summary through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, marketers, and creator analysts use this skill to fetch Xiaohongshu Creator Marketplace follower summary data by KOL ID for creator evaluation, campaign planning, and benchmarking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JustOneAPI token may be exposed through command-line arguments or URL/query logging. <br>
Mitigation: Review before installation, avoid pasting token values into chat or logs, and prefer an implementation that reads the token from the environment and sends it through a non-URL credential channel. <br>
Risk: A broadly scoped or paid-quota JustOneAPI token can increase the impact of accidental disclosure or misuse. <br>
Mitigation: Use the narrowest practical token permissions, monitor quota usage, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-get-kol-fans-summary) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_summary&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_summary&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; getKolFansSummaryV1 requires kolId and accepts optional acceptCache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
