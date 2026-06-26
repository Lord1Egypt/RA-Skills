## Description: <br>
Checks the status of an asynchronous OATDA video generation task and reports whether the video is queued, processing, completed, or failed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to check an existing OATDA video generation task by task ID, retrieve the completed video URL, and understand common status or error responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OATDA API key and sends it to oatda.com when checking task status. <br>
Mitigation: Install only if you trust OATDA, keep the key in the expected environment variable or credentials file, and do not print the full key in agent output. <br>
Risk: The skill runs shell commands that call an external API with a user-provided task ID. <br>
Mitigation: Review the generated command before execution and confirm the task ID is the intended OATDA video task. <br>


## Reference(s): <br>
- [OATDA](https://oatda.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/devcsde/oatda-video-status) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and status-response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OATDA task ID, curl, jq, and an OATDA API key from OATDA_API_KEY or ~/.oatda/credentials.json; completed responses may include video URLs and cost details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
