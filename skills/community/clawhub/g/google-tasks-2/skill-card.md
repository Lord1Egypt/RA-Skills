## Description: <br>
Google Tasks is currently marked unavailable and provides guidance for managing Google Tasks task lists and tasks through MorphixAI-mediated access to the Google Tasks API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure MorphixAI credentials, link a Google Tasks account, and issue mx_google_tasks actions for listing, creating, updating, completing, and deleting Google Tasks items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MorphixAI API key and a linked Google account. <br>
Mitigation: Use the intended Google account, store MORPHIXAI_API_KEY securely, and avoid exposing the key in shared logs or transcripts. <br>
Risk: Update, complete, and delete actions can change or remove Google Tasks data. <br>
Mitigation: Review task list IDs, task IDs, and requested actions before execution, especially for delete or update operations. <br>
Risk: The artifact marks the Google Tasks integration as temporarily unavailable until the account is linked. <br>
Mitigation: Complete account linking through MorphixAI connections or the mx_link tool before relying on task operations. <br>


## Reference(s): <br>
- [ClawHub Google Tasks listing](https://clawhub.ai/paul-leo/google-tasks-2) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tool-call examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Google Tasks account before task operations can run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
