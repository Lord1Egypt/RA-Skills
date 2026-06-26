## Description: <br>
Search Xiaohongshu (RedNote) notes through JustOneAPI using keyword-based query parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call JustOneAPI endpoints that return Xiaohongshu (RedNote) note search data, including snippets, authors, and media for topic discovery. It supports versioned GET operations for keyword-based searches with optional pagination, sort, note type, and note time filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends RedNote search keywords and a JustOneAPI token to api.justoneapi.com. <br>
Mitigation: Use the skill only when that data sharing is acceptable, keep tokens out of chat messages and logs, and rotate the token if it may have been exposed. <br>
Risk: The helper places the token into query parameters for the API request, which can expose credentials through command history, process listings, logs, or monitoring systems. <br>
Mitigation: Prefer passing the token from an environment variable on trusted systems, avoid shared shells and verbose logging, and limit token scope where the provider supports it. <br>


## Reference(s): <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [JustOneAPI usage guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_note&utm_content=project_link) <br>
- [JustOneAPI dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_note&utm_content=project_link) <br>
- [ClawHub release page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-search-note) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Shell commands, Configuration] <br>
**Output Format:** [Short endpoint-specific summary followed by raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a JustOneAPI token supplied through JUST_ONE_API_TOKEN or the helper's token argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
