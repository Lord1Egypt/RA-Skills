## Description: <br>
Call GET /api/xiaohongshu-pgy/get-note-detail/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Details through JustOneAPI with noteId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to call JustOneAPI for Xiaohongshu Creator Marketplace note details by noteId, then summarize media and engagement data for content analysis, archiving, and campaign review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real JustOneAPI token can be exposed through command arguments, URLs, shell history, process listings, screenshots, or logs. <br>
Mitigation: Use a protected environment variable or secret store, avoid pasting token values into chat or logs, and review execution context before using a production token. <br>
Risk: The skill may surface backend error payloads from the external API. <br>
Mitigation: Review returned error details before sharing them and redact tokens, identifiers, or sensitive campaign data from logs and reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-pgy-get-note-detail) <br>
- [JustOneAPI homepage](https://api.justoneapi.com) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_note_detail&utm_content=project_link) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_note_detail&utm_content=project_link) <br>
- [Generated operation reference](artifact/generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with raw JSON response data and optional shell command invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses noteId as the required lookup scope and may include backend error payloads when the API request fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
