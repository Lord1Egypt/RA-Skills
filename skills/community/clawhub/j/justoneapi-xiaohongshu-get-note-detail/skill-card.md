## Description: <br>
Call 3 get-note-detail versions for Xiaohongshu (RedNote) Note Details through JustOneAPI with noteId. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and campaign teams use this skill to call JustOneAPI Xiaohongshu note-detail endpoints by noteId and summarize returned media and engagement data for content analysis, archiving, or campaign research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a JustOneAPI token, queried note IDs, and returned RedNote content in ways that may expose them through process listings, request URLs, shell history, proxy logs, command logs, or error reports. <br>
Mitigation: Use it only with trusted JustOneAPI credentials, avoid sharing logs or full request URLs, prefer a least-privileged or disposable token where available, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-xiaohongshu-get-note-detail) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_get_note_detail&utm_content=project_link) <br>
- [Xiaohongshu Note Details Operations](generated/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown summary followed by raw JSON from the selected JustOneAPI endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and JUST_ONE_API_TOKEN; noteId is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
