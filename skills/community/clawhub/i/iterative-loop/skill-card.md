## Description:

Provides a Chinese-documented loop controller for bounded iterative agent work using fixed, max-with-condition, and adaptive modes backed by a local JSON state file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure iterative work such as refactoring, test repair, and optimization with explicit stop conditions, iteration limits, and JSON state tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loop state files can contain task summaries, metrics, artifact paths, or other sensitive project details.

Mitigation: Choose state-file locations deliberately and review or delete loop-state.json when it may contain sensitive information.

Risk: Iterative work can run longer than intended when limits or completion checks are unclear.

Mitigation: Set a clear maximum iteration count and use explicit completion conditions before starting the loop.

## Reference(s):

- [Iteration Patterns Reference](references/iteration-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/paudyyin/skills/iterative-loop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local JSON loop state file, typically loop-state.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
