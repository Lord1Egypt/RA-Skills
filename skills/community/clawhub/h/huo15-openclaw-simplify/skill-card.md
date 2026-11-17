## Description:

Reviews recent code changes across reuse, quality, and efficiency, produces an actionable cleanup checklist, and applies user-approved fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after implementing code changes or before pull requests to identify cleanup opportunities in reuse, code quality, and efficiency, then apply selected fixes conservatively.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic cleanup or refactor requests may route to this skill and produce suggested code changes in large or dirty worktrees.

Mitigation: Review the generated checklist and explicitly choose which items to apply before accepting edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-simplify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with file-line findings, severity levels, and concise fix notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce code edits only after user confirmation; does not introduce dependencies, run formatters, or run tests unless requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
