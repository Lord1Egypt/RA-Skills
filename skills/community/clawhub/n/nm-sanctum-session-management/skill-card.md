## Description:

Manages Claude Code sessions with naming, checkpointing, and resume strategies

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to name, checkpoint, and resume long-running work across breaks or sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags context-capture wording as a potential context-leakage concern, while judging it expected for the skill's purpose.

Mitigation: Review whether session context could contain sensitive information and limit what is carried into sessions before using the workflow.

## Reference(s):

- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
