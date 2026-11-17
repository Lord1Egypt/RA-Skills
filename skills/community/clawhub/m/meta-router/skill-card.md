## Description:

Meta-Router indexes installed OpenClaw skills and routes user intents to relevant skill contexts so an agent can load fewer instructions per task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawliet-ai](https://clawhub.ai/user/lawliet-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Meta-Router to keep installed skill contexts indexed and load relevant skill instructions only when a task needs them. It is intended for environments with multiple installed skills where reducing context overhead is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A central router for other skills can influence which instructions the agent loads and follows.

Mitigation: Treat routing as advisory, keep mounted skill counts limited, and require visible status for routing failures or state changes.

Risk: Hidden persistent indexing and silent background maintenance can make local state changes hard to audit.

Mitigation: Make indexing visible, ask before scans or state updates, and document how to disable and delete the local index.

Risk: Scanning installed skills may expose local skill metadata or retain stale routing information.

Mitigation: Limit scans to necessary skill metadata, avoid storing sensitive content, and refresh the index only when the user approves or when changes are clearly visible.

## Reference(s):

- [Meta-Router ClawHub skill page](https://clawhub.ai/lawliet-ai/skills/meta-router)
- [Lawliet-ai ClawHub publisher profile](https://clawhub.ai/user/lawliet-ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text agent instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and maintain a local skill index for routing decisions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
