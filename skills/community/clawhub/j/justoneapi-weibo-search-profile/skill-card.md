## Description: <br>
Call GET /api/weibo/search-profile/v1 for Weibo Search User Published Posts through JustOneAPI with q and uid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query JustOneAPI's Weibo search-profile endpoint by user ID and keyword. It supports author research and historical content discovery by returning matched posts, metadata, and ranking signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a real JustOneAPI token and may expose it through command arguments, shell history, logs, or request URLs. <br>
Mitigation: Use it only in trusted environments, avoid shared shells and command logging, keep the token in an environment variable or secret store, and review commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-weibo-search-profile) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_profile&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the operation ID, endpoint path, required q and uid lookup scope, and backend error payloads when requests fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
