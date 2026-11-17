## Description:

Generates GitLab team reports with merge request categorization, contributor and repository summaries, Markdown and HTML outputs, charts, historical report indexes, and optional Feishu publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzn](https://clawhub.ai/user/wangzn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering managers, and team leads use this skill to summarize GitLab merge requests, commits, contributors, repositories, and product-area work for weekly reviews or stakeholder updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect GitLab team activity on a recurring schedule.

Mitigation: Review before installing, use a dedicated read-only GitLab token, require HTTPS for the GitLab URL, and run scripts/setup-cron.sh only when a persistent scheduled report is intended.

Risk: Generated reports can contain internal repository and personnel activity data.

Mitigation: Keep configuration and token files protected, and confirm exactly which Feishu document or wiki will be modified before publishing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, HTML pages, JSON statistics, chart assets, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally upload generated reports to Feishu when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
