## Description: <br>
Use this skill to read, create, update, and delete ClickUp data through an OOMOL-connected ClickUp account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate ClickUp workspaces, spaces, folders, lists, tasks, comments, tags, templates, members, and custom fields through the oo CLI. It supports read workflows and confirmed write or destructive changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete ClickUp tasks, lists, folders, spaces, comments, attachments, links, tags, dependencies, and custom field values. <br>
Mitigation: Confirm the exact ClickUp target, action, and JSON payload with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: The skill depends on a connected OOMOL account with ClickUp credentials and may fail if authentication, scopes, connection state, or credits are missing. <br>
Mitigation: Use setup or reconnection steps only after the connector reports an authentication, scope, expired credential, app, or billing error. <br>


## Reference(s): <br>
- [ClawHub ClickUp skill page](https://clawhub.ai/oomol/oo-clickup) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [ClickUp homepage](https://clickup.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI and a connected ClickUp account; write and destructive actions require confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
