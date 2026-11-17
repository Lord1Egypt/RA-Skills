## Description:

Dispatches a focused OpenClaw code-review subagent during implementation, major feature completion, and pre-merge workflows to catch issues before they cascade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to gather recent change context, request a focused code review from an OpenClaw subagent, and triage findings before continuing or merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository diffs and change summaries may expose proprietary or sensitive code to a review subagent.

Mitigation: Use the skill only when that sharing is acceptable, and limit review context to the minimum needed for the review.

Risk: The documented fixed temporary path can create local temporary-file hygiene issues.

Mitigation: Prefer sending the diff directly or writing it to a private mktemp-created directory.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with inline shell commands and review prompt structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
