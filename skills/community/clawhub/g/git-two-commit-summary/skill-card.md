## Description:

Summarizes Git diffs between commits or branches in a structured change report with impact analysis and risk guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahsh](https://clawhub.ai/user/mahsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to compare commits, branches, or working tree changes and prepare a reproducible summary for code review, including affected areas and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs summaries to a GitHub-synchronized archive location, which may share repository details beyond the intended summary task.

Mitigation: Review the archive destination and its synchronization scope before installation; omit or change the archive step if that location is not appropriate. The security scan was partial, so review the unresolved referenced path as well.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mahsh/skills/git-two-commit-summary)
- [Publisher profile](https://clawhub.ai/user/mahsh)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown report with summary bullets, impact table, risk table, and review recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commit and file statistics when available from Git commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
