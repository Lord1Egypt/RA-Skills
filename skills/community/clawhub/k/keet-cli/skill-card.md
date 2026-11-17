## Description:

Safely operate and improve the Keet CLI project and Keet <-> OpenClaw bridge for read-only inspection, debugging, documentation, release checks, bridge supervision, and explicitly approved messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectreturn](https://clawhub.ai/user/projectreturn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate or improve Keet CLI and Keet <-> OpenClaw bridge workflows while keeping messaging, profile storage, daemon, bridge, and Git operations behind explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide access to private Keet profile storage and chat content.

Mitigation: Require explicit confirmation of the profile path and target chat, avoid printing private messages unless requested, and redact secrets or private content in summaries.

Risk: Messaging, file-send, invite, chat creation, bridge, daemon, and watch workflows can change external state or keep a process running.

Mitigation: Confirm the exact target, action, message or file, and long-running process behavior before execution, and provide stop guidance when a process remains active.

Risk: Git pushes can publish unintended changes or sensitive local state.

Mitigation: Confirm the repository, branch, commit diff, and credential identity before pushing, and do not commit live profile storage, generated state, logs, screenshots, or private message content.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, code or configuration snippets, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing messaging, bridge, daemon, invite, chat, file-send, and Git push actions require explicit user confirmation.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
