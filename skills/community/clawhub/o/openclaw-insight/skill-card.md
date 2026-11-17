## Description:

Analyze OpenClaw AI assistant usage patterns and generate interactive insight reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linsheng9731](https://clawhub.ai/user/linsheng9731)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local OpenClaw session history, understand usage patterns, estimate token costs, identify friction points, and generate improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path pipes a mutable remote installer into a shell.

Mitigation: Prefer a signed release, pinned commit, separate download-and-review step, or isolated user environment before running installation commands.

Risk: Generated reports may contain sensitive usage patterns, costs, model choices, and transcript-derived details.

Mitigation: Handle reports as sensitive local artifacts and avoid sharing them unless reviewed and redacted.

## Reference(s):

- [OpenClaw Insight ClawHub page](https://clawhub.ai/linsheng9731/skills/openclaw-insight)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, CLI options, and report interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can generate local HTML or JSON usage reports from OpenClaw session data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
