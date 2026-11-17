## Description:

Plan Mode helps agents pause for read-only planning with approval gating when work is complex, ambiguous, risky, interrupted, multi-step, or long-running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pieterjanliekens](https://clawhub.ai/user/pieterjanliekens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to pause complex, ambiguous, risky, interrupted, or multi-step work long enough to clarify scope, compare approaches, plan execution, recover state, or maintain a living plan before approving action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Planning output may be acted on before the user has explicitly approved execution.

Mitigation: Keep the agent in a read-only planning stance until clear approval, and treat partial approvals as scoped execution limits.

Risk: Persistent plan files or external registry checks can expose project context or create unwanted workspace changes.

Mitigation: Require explicit user approval before writing living-plan files or performing external registry lookups.

## Reference(s):

- [Plan Mode Patterns Across AI Tools](references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown planning guidance with optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only planning stance until user approval; persistent plan files and external registry lookups require explicit approval.]

## Skill Version(s):

3.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
