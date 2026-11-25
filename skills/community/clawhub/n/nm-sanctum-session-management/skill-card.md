## Description:

Manages Claude Code sessions with naming, checkpointing, and resume strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Claude Code developers use this skill to organize long-running work, preserve useful checkpoints, and resume named sessions across work periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resuming a named session can restore earlier conversation context that may be outdated or contain information the user does not intend to reuse.

Mitigation: Confirm the session name and review its resumed context before relying on it; refresh repository state when appropriate.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-sanctum-session-management)
- [Sanctum project page](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline session-naming and resume commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples of session naming, checkpoint workflows, resumption, and troubleshooting; no files are generated.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
