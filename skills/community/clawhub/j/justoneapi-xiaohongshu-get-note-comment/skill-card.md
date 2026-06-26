## Description: <br>
Calls JustOneAPI endpoints to retrieve Xiaohongshu (RedNote) note comments by noteId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analysts use this skill to call JustOneAPI for Xiaohongshu note comments and inspect comment text, authors, timestamps, profiles, and interaction data for feedback analysis, sentiment analysis, or community monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JUST_ONE_API_TOKEN may be exposed through command arguments or request URLs. <br>
Mitigation: Use secure secret handling where available, avoid shared or logged environments, do not paste token values into chat or logs, and rotate the token if exposed. <br>
Risk: Note IDs and returned Xiaohongshu comment or profile data pass through JustOneAPI. <br>
Mitigation: Use only when you are comfortable sending the lookup scope to JustOneAPI and receiving the resulting comment/profile data through that service. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-get-note-comment) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_comment&utm_content=project_link) <br>
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_comment&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with a Node.js command and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_ONE_API_TOKEN and a Xiaohongshu noteId; getNoteCommentV2 also accepts lastCursor and sort.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
