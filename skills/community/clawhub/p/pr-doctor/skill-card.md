## Description:

PR Doctor orchestrates automated pull request code review, test coverage analysis, issue tracking, and continuous improvement into a single quality review workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review GitHub pull requests, assess code and test quality, create follow-up issues, and produce a consolidated review report before merge decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically create GitHub issues from review findings.

Mitigation: Use narrowly scoped GitHub permissions and add a confirmation or dry-run step before issue creation.

Risk: The skill may retain review data in local `.learnings/` files.

Mitigation: Review what information is logged and avoid storing sensitive pull request details unless retention is approved.

Risk: Automated review findings may be incomplete or misleading.

Mitigation: Treat the report as reviewer assistance and keep final merge decisions with a human reviewer.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown review report with quality score, prioritized findings, test coverage assessment, recommended actions, and GitHub issue links when issue creation is enabled.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require GitHub CLI authentication, repository access, and issue creation permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
