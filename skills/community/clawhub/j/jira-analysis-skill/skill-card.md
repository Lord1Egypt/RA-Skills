## Description:

从 Jira Server/DC 拉取 Bug 数据，进行全面的 AI 分析，并生成交互式 HTML 报表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cntesters](https://clawhub.ai/user/cntesters)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and project teams use this skill to collect Jira Server/Data Center bug data, analyze backlog and resolution patterns, and generate an interactive HTML report for bug metrics and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Jira credentials while retrieving issue data.

Mitigation: Use a short-lived, read-only Jira PAT scoped to the specific project and avoid username/password authentication.

Risk: Disabling TLS verification can expose Jira credentials and issue data to interception.

Mitigation: Avoid --no-verify and curl -k unless the user explicitly accepts that risk for a trusted network.

Risk: Generated HTML and XLS exports can contain sensitive internal Jira issue details.

Mitigation: Treat generated reports and exports as sensitive internal files and share them only through approved channels.

Risk: Dependency installation uses an unpinned requests dependency.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions when operationalizing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cntesters/skills/jira-analysis-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON data handling, and self-contained HTML report code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local HTML report and optional Excel XML export based on Jira issue data.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
