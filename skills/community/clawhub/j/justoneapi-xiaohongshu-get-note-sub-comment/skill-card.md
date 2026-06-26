## Description: <br>
Call GET /api/xiaohongshu/get-note-sub-comment/v2 for Xiaohongshu (RedNote) Comment Replies through JustOneAPI with commentId and noteId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Xiaohongshu (RedNote) comment replies by note and comment identifiers through JustOneAPI. It supports thread analysis and feedback research by returning reply text, author, timestamp, and pagination data from the documented endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a JustOneAPI token and the security summary warns that token handling can expose it outside the intended request. <br>
Mitigation: Pass tokens only from the environment, avoid recording command lines or request URLs that contain credentials, and rotate the token if it may have appeared in logs, process listings, or proxy records. <br>
Risk: Requests send Xiaohongshu note and comment identifiers to JustOneAPI. <br>
Mitigation: Use the skill only when sharing those identifiers with JustOneAPI is acceptable for the user's workflow and data handling requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-get-note-sub-comment) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_sub_comment&utm_content=project_link) <br>
- [Generated Operation Reference](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JustOneAPI token and noteId/commentId query parameters; lastCursor is optional for pagination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
