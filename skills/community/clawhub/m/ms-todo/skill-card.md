## Description:

Microsoft To Do task-management integration for managing task lists and tasks, including creating, updating, completing, and deleting tasks through MorphixAI-mediated access to Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Microsoft To Do task lists and tasks from an agent workflow after configuring MorphixAI credentials and linking a Microsoft To Do account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented tool actions can create, update, complete, and delete Microsoft To Do tasks.

Mitigation: Review task lists before modification and clearly confirm destructive requests before execution.

Risk: The skill depends on an external MorphixAI/OpenClaw plugin, API key, and linked Microsoft To Do account.

Mitigation: Install only from trusted plugin sources and protect MORPHIXAI_API_KEY as a credential.

## Reference(s):

- [Ms Todo ClawHub skill page](https://clawhub.ai/paul-leo/skills/ms-todo)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline tool-call examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Microsoft To Do account.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
