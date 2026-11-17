## Description:

Provides a local shared-file queue for asynchronous messages between WorkBuddy and Hermes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send, receive, inspect, and mark asynchronous queue messages between WorkBuddy and Hermes without an external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages are stored in local shared queue and history files, which can expose sensitive content to other local users or processes.

Mitigation: Avoid sending secrets and restrict filesystem permissions on the configured communication directory.

Risk: Unattended polling can process untrusted queue contents, including command-type messages.

Mitigation: Treat all queue entries as untrusted and require separate confirmation before acting on command-type messages.

Risk: Shared queue files do not provide authentication or authorization for multi-user or sensitive environments.

Mitigation: Use a safer authenticated channel or deploy only in trusted single-user environments when sensitive messages are possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/hermes-communication-bridge)
- [Publisher profile](https://clawhub.ai/user/liuboacean)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local queue and history JSON files under the configured Hermes communication directory.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
