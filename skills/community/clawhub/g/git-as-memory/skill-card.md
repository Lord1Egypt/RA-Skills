## Description:

Git-backed memory policy and CLI workflow for OpenClaw, Hermes, Claude Code, Codex, and other agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure agents to store, search, update, and audit durable user preferences, project decisions, conventions, and lessons in a dedicated Git ref.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External CLI install examples do not pin package versions.

Mitigation: Verify the git-as-memory package source and publisher, prefer an exact pinned version, and use a project-local invocation when it fits the workflow.

Risk: Durable memory entries could accidentally capture secrets, credentials, or noisy one-off data.

Mitigation: Follow the documented write policy: search before writing, keep entries concise and reusable, include a source, and do not store secrets or private authentication material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/femto/skills/git-as-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
