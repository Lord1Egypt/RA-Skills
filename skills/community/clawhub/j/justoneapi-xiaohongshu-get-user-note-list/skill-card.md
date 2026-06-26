## Description: <br>
Call 2 get-user-note-list versions for Xiaohongshu (RedNote) User Published Notes through JustOneAPI with userId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to call JustOneAPI for Xiaohongshu (RedNote) account monitoring, retrieving a user's published-note metadata, covers, and publish times by userId. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API token and submitted Xiaohongshu user IDs may be exposed through command arguments, request URLs, chat, screenshots, logs, or monitoring systems. <br>
Mitigation: Keep JUST_ONE_API_TOKEN out of chat, screenshots, shell history, shared logs, and monitoring systems; rotate the token if a command line or request URL may have been exposed. <br>


## Reference(s): <br>
- [JustOneAPI API Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user_note_list&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_user_note_list&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summary with endpoint details and optional raw JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JUST_ONE_API_TOKEN; uses userId and optional lastCursor query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
