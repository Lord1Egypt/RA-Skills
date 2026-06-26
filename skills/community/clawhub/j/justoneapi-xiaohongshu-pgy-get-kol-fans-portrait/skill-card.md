## Description: <br>
Call GET /api/xiaohongshu-pgy/get-kol-fans-portrait/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Distribution through JustOneAPI with kolId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI's Xiaohongshu Creator Marketplace follower distribution endpoint for a specific KOL ID. It supports creator evaluation, campaign planning, and creator benchmarking by returning audience demographics, interests, and distribution metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence flags token exposure risk because the JustOneAPI token can appear in command-line arguments and request URLs. <br>
Mitigation: Use a narrowly scoped token where possible, avoid shared machines or CI logs for token-bearing runs, and rotate the token if it may have appeared in logs or process listings. <br>
Risk: The security verdict is suspicious for this focused API wrapper. <br>
Mitigation: Review the helper before installing, especially when the token has paid, broad, or shared-account access. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-get-kol-fans-portrait) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_portrait&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_portrait&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and summarized JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; the endpoint requires kolId and may accept acceptCache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
