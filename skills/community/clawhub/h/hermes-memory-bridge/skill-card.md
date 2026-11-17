## Description:

Hermes Memory Bridge lets agents synchronize memory, search cross-session context, and coordinate task commands between Hermes Agent and WorkBuddy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuboacean](https://clawhub.ai/user/liuboacean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to bridge Hermes Agent and WorkBuddy memory, task signals, feedback, and command handling across local agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a user-level background watcher that reads and writes Hermes and WorkBuddy memory.

Mitigation: Review the watcher before installation, keep the LaunchAgent disabled until approved, and limit shared-directory permissions.

Risk: Local command files are processed automatically and may be unauthenticated.

Mitigation: Authenticate or otherwise validate signal files before processing and require confirmation for memory writes or task changes.

Risk: Task-command handling includes a code injection path in python -c task handlers.

Mitigation: Remove those handlers or replace them with safe argument passing before enabling task creation or completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuboacean/skills/hermes-memory-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local file paths, environment variables, daemon setup, memory synchronization commands, and feedback status.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
