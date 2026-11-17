## Description:

Lightweight project management for agents. Create projects, track tasks, set priorities and deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and project contributors use ProjectPilot to create local project task lists, update task state, track deadlines and priorities, and generate concise project status views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Bash to execute its bundled Python tracker.

Mitigation: Review proposed commands before execution and run the tracker only in user-owned workspaces.

Risk: The tracker creates or modifies local project JSON files.

Mitigation: Use a private PROJECTPILOT_DATA directory and avoid importing untrusted project JSON.

Risk: Generic project-management triggers may activate the skill in unrelated conversations.

Mitigation: Narrow or disable triggers when broad project-management terms cause unwanted activation.

## Reference(s):

- [PM Templates & Frameworks](references/pm-templates.md)
- [ProjectPilot ClawHub Page](https://clawhub.ai/raychanpmp/skills/projectpilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and project/task status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local project JSON files through the bundled tracker.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
