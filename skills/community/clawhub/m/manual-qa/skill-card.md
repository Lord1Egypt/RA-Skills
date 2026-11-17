## Description:

Generate a manual QA checklist from code changes for PRs, commits, branches, staged changes, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipefreitag](https://clawhub.ai/user/felipefreitag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to turn code changes into practical manual QA checklists. It separates terminal-verifiable checks from human-only verification and covers happy paths, error paths, and edge cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local git diffs or PR diffs when asked to create QA guidance.

Mitigation: Use it only on changes intended for review, and require confirmation before running agent-testable commands.

## Reference(s):

- [ClawHub Manual QA skill page](https://clawhub.ai/felipefreitag/skills/manual-qa)
- [ClawHub publisher profile](https://clawhub.ai/user/felipefreitag)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown numbered checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates agent-testable steps from human-only testing steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
