## Description:

Triage open PRs by detecting duplicates, assessing quality, and generating prioritized reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone0x](https://clawhub.ai/user/zerone0x)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to analyze busy GitHub repositories, identify likely duplicate pull requests, grade PR quality signals, and generate prioritized review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use the local GitHub CLI authentication context, which may be an unintended GitHub account.

Mitigation: Run it in a constrained environment and confirm the active GitHub CLI account before analysis.

Risk: The skill documentation includes optional pull request commenting and labeling actions.

Mitigation: Treat comments and labels as separate write actions that require explicit confirmation before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zerone0x/skills/pr-triage)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the Markdown report to a caller-specified output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
