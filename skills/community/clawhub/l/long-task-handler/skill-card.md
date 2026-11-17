## Description:

Long Task Handler helps an agent identify long-running tasks, run them in the background, and report progress, timeout, failure, and completion status without blocking the main conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankieway](https://clawhub.ai/user/frankieway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage compile, deployment, migration, data processing, and model-training work that is expected to run longer than a normal interactive response. It guides the agent to acknowledge the work quickly, run it in the background, poll for progress, and send concise status or completion updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task progress and completion notifications may expose raw command output, secrets, private paths, or sensitive operational details in chat.

Mitigation: Use the skill only where sending task status to chat is acceptable, avoid commands that print secrets, redact logs, and send summaries by default.

Risk: Task commands and status can be retained in plaintext local state.

Mitigation: Store only minimal task state, restrict file permissions, and clean up or archive task records after they are no longer needed.

Risk: Notifications sent to a broad or incorrect channel can disclose task details to unintended readers.

Mitigation: Route notifications to the originating conversation or an explicitly approved destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankieway/skills/long-task-handler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes periodic status summaries, completion notices, timeout and failure summaries, and recent log excerpts.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
