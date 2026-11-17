## Description:

Google Tasks is a currently unavailable task-management integration that helps agents manage task lists and tasks through MorphixAI-secured access to the Google Tasks API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to guide an agent through listing, creating, updating, completing, and deleting Google Tasks items after configuring MorphixAI and linking a Google Tasks account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a MorphixAI API key and a linked Google Tasks account.

Mitigation: Install and use it only when the MorphixAI plugin is trusted, the API key is configured intentionally, and the target Google Tasks account is linked.

Risk: Create, update, complete, and delete operations can make live changes to Google Tasks data.

Mitigation: Review target task list IDs and task IDs before running mutation actions, and use extra care with delete actions.

Risk: The artifact states the skill is temporarily unavailable until Google Tasks is linked.

Mitigation: Confirm account linking through MorphixAI connections or the mx_link workflow before relying on the skill for task-management workflows.

## Reference(s):

- [ClawHub Google Tasks skill page](https://clawhub.ai/paul-leo/skills/google-tasks-2)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Google Tasks account before task operations can run.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
