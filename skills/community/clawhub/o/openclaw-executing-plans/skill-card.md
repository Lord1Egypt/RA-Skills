## Description:

Use when executing a written implementation plan in the current session with sequential task execution and review checkpoints, especially when subagent-driven mode is not available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to execute a written implementation plan step by step, review the plan before starting, run verification for each task, and pause for blockers or unclear instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can drive code changes from a written plan that may be incomplete, unclear, or unsafe for the current branch.

Mitigation: Review the plan before implementation and pause for blockers, unclear instructions, verification failures, or main/master branch changes without explicit user approval.

Risk: The artifact is a Chinese-language workflow skill, which can be misunderstood by agents or reviewers who cannot reliably read it.

Mitigation: Install and use it only when the operator is comfortable with the language or can reliably translate the workflow guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/openclaw-executing-plans)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with task lists, review checkpoints, code edits, and verification commands as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plain workflow guidance; the skill does not include executable code or hidden network, credential, persistence, or scanner behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
