## Description: <br>
Toggl Track lets an agent read, create, update, stop, and delete Toggl Track records through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Toggl Track workspaces, projects, tasks, tags, and time entries from an agent workflow. It supports read operations and user-confirmed write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, stop, and delete Toggl Track projects, tasks, tags, and time entries. <br>
Mitigation: Confirm the exact payload and effect with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: The skill requires an OOMOL account and an active Toggl Track connection with sensitive credentials handled by the connector. <br>
Mitigation: Use only trusted OOMOL and Toggl connections, and retry setup steps only after authentication, connection, scope, credential, or billing errors. <br>


## Reference(s): <br>
- [Toggl Track skill page](https://clawhub.ai/oomol/oo-toggl) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Toggl Track homepage](https://toggl.com/track/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
