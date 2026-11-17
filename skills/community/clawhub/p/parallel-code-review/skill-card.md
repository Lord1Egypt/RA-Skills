## Description:

Parallel Code Review guides an agent through a read-only, dual-lens code review that checks runtime safety and architecture consistency and returns a deduplicated Markdown review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhetli](https://clawhub.ai/user/hhetli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after completing work, before merge, or on a specified PR or diff to surface runtime bugs, fragile edge cases, and architecture contract issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad default review may cause the agent to read more changed repository context than intended.

Mitigation: Specify an explicit diff range, such as review origin/main..HEAD, when tighter scope is needed.

Risk: Review findings can be incomplete or misleading if the resolved diff range is not what the user intended.

Mitigation: Confirm the resolved review range reported in the Overview before relying on the findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hhetli/skills/parallel-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with Overview, Issues, Recommendations, and Verdict sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review output; may include file and line references plus tactical recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
