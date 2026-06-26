## Description: <br>
Integrates Microsoft To Do task management so agents can manage task lists and create, update, complete, and delete tasks through MorphixAI access to Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage Microsoft To Do lists and tasks from an agent workflow after configuring MorphixAI access. It supports listing, creating, updating, completing, and deleting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task deletion can remove Microsoft To Do items without clearly documented confirmation guidance. <br>
Mitigation: Confirm the exact list and task before running delete_task, and verify whether deletion is reversible for the connected account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paul-leo/ms-todo) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline tool-call examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Microsoft To Do account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
