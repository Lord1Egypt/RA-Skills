## Description:

Automates GitLab merge request code review by collecting MR details, using AI review, producing reports, and emailing results to MR authors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[20181112523](https://clawhub.ai/user/20181112523)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review open GitLab merge requests, generate Markdown and PDF review reports, email findings to authors, and avoid duplicate reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitLab access tokens, email credentials, private diffs, and outbound email delivery.

Mitigation: Use only HTTPS GitLab hosts, restrict tokens to the minimum necessary repositories and scopes, protect configuration files, and avoid entering secrets in shared or recorded terminals.

Risk: Generated review reports may expose private code or sensitive findings when emailed to MR authors.

Mitigation: Confirm report distribution is allowed for the repository and add human approval before sending email in sensitive environments.

Risk: The workflow depends on other skills for code review, PDF rendering, and email delivery.

Mitigation: Pin and review dependency skills before use.

## Reference(s):

- [Review Report Template](references/review-report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/20181112523/skills/gitlab-mr-review-pipeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, PDF report files, email messages, JSON configuration, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may contain private repository diffs and review findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
