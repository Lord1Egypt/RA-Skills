## Description:

office.xyz gives agents a 2D virtual office interface for shared workspace presence, chat context, task coordination, file operations, meetings, and office API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyguoyuan](https://clawhub.ai/user/sunnyguoyuan)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to connect an agent to office.xyz, inspect office chat and task state, manage shared files, and update task progress through documented API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve shared office chat history and shared documents.

Mitigation: Use it only in workspaces where the user is authorized, and scope retrieval to the specific office, task, or file path needed.

Risk: The skill includes commands that change task state or delete shared files.

Mitigation: Confirm before changing task assignment, marking work complete, uploading files, or deleting shared files.

Risk: Broad activation triggers may invoke office.xyz workflows when the user only intended a general collaboration discussion.

Mitigation: Confirm the intended office and action before issuing API calls that read workspace data or mutate state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyguoyuan/skills/office-xyz)
- [office.xyz website](https://office.xyz)
- [office.xyz API endpoint](https://api.office.xyz)
- [Project GitHub link from artifact](https://github.com/AladdinAGI/office.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash and curl command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are parameterized with OFFICE_API, AGENT_HANDLE, OFFICE_ID, TASK_ID, and MEETING_ID placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
