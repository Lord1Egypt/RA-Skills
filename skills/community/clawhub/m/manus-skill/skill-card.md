## Description:

Interact with the Manus AI agent platform through its REST API to create and continue tasks, manage projects, handle files and webhooks, and track sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishbhimani](https://clawhub.ai/user/krishbhimani)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate work to Manus, continue existing Manus sessions, upload files, organize projects, poll task status, and manage API resources from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts and selected files to Manus and create remote tasks or projects.

Mitigation: Confirm user intent before sending sensitive prompts or files, and limit use to data appropriate for Manus processing.

Risk: The local session registry can retain prompt text, task IDs, and task URLs.

Mitigation: Keep the registry out of version control, restrict local access, and redact or disable full prompt retention for sensitive work.

Risk: Task, file, sharing, connector, and webhook operations can expose or remove remote resources.

Mitigation: Require explicit confirmation with the exact task ID, file name, webhook ID, or connector before upload, sharing, connector, or deletion workflows.

Risk: Creating duplicate Manus tasks can waste credits.

Mitigation: Search and reuse existing sessions or task IDs before creating a new task.

## Reference(s):

- [Manus API - Complete Reference](artifact/references/api-reference.md)
- [Session Management - Full Design](artifact/references/session-management.md)
- [Manus API](https://api.manus.ai)
- [ClawHub Skill Page](https://clawhub.ai/krishbhimani/skills/manus-skill)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MANUS_API_KEY; may create remote Manus tasks, upload files, manage projects and webhooks, and store session metadata locally.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
