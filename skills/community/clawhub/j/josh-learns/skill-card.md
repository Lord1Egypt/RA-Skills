## Description:

MeshMorize provides a local-first, file-based memory system for AI agents on OpenClaw-like hosts, with rotating recent context, daily logs, mesh indexing, grep search, compliance checks, and crash-gap recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozz0](https://clawhub.ai/user/mozz0)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use MeshMorize to give agents durable local memory across sessions, restarts, and crashes. It helps agents search prior work, log meaningful exchanges, maintain lightweight memory indexes, and recover missing context from approved local sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local memory can capture sensitive personal data or secrets if the agent logs too broadly.

Mitigation: Do not log credentials or unnecessary personal data; keep secrets in a separate ignored local store and scrub memory files before sharing or publishing them.

Risk: Transcript database reads and automation registry changes can expose or alter user context without sufficient scope.

Mitigation: Require explicit approval for the exact transcript session, time range, and automation job before reading or changing them, and remove temporary transcript copies after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mozz0/skills/josh-learns)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, file paths, and Python utility scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local filesystem memory artifacts such as Markdown logs, JSON mesh/checkpoint files, and operational command guidance.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
