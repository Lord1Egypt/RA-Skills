## Description:

Audit GitHub Actions run reliability by actor to surface high-risk contributors and flaky automation owners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and CI maintainers use this skill to analyze exported GitHub Actions run data, rank unreliable actors or actor-workflow groups, and support triage or policy gating decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub Actions run exports may include repository names, actor logins, branch names, events, run URLs, and failure history.

Mitigation: Keep RUN_GLOB pointed at the intended export directory and review JSON output before enabling FAIL_ON_CRITICAL as an automated gate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daniellummis/skills/github-actions-actor-reliability-audit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit with code 1 when FAIL_ON_CRITICAL=1 and one or more critical actor groups are detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
