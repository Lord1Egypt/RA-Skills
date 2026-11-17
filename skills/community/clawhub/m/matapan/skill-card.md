## Description:

Work inside a Matapan workspace: scoped file edits, hardened container runs, commits, and sealing an immutable proposal for human review and compare-and-swap apply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide code changes through a Matapan workspace, including scoped editing, sandboxed command execution, commits, and sealed human-reviewed proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may request egress or secret grants while building or testing workspace changes.

Mitigation: Review each requested grant before approval and keep access limited to the stated workspace need.

Risk: A sealed proposal may still contain incorrect or unwanted code changes.

Mitigation: Inspect the proposal diff and verification evidence before applying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mentholmike/skills/matapan)
- [Publisher profile](https://clawhub.ai/user/mentholmike)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with tool calls, command examples, and review handoff text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to stay within a disposable Matapan workspace and culminate in a sealed proposal for human review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
