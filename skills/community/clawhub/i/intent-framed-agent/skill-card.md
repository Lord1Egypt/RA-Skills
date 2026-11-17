## Description:

Frames coding-agent work sessions with explicit intent capture and drift monitoring. Use when a session transitions from planning/Q&A to implementation for coding tasks, refactors, feature builds, bug fixes, or other multi-step execution where scope drift is a risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao1804](https://clawhub.ai/user/xiao1804)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to make implementation intent explicit before non-trivial code changes, monitor for scope drift during execution, and record how each work session resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned install commands may resolve to changed content over time.

Mitigation: Use pinned or reviewed install commands, and scan the skill before deployment.

Risk: The skill may perform a low-impact local Entire CLI availability check when it activates.

Mitigation: Review tool permissions and allow local command checks only in trusted workspaces.

## Reference(s):

- [Intent Framed Agent on ClawHub](https://clawhub.ai/xiao1804/skills/intent-framed-agent)
- [Entire CLI](https://github.com/entireio/cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured intent, drift-check, and resolution blocks plus optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves fixed block headers and fields for parseable session records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
