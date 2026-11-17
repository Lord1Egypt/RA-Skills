## Description:

谷歌搜索专业版 helps agents run Google Custom Search workflows for batch queries, multiple Custom Search Engine configurations, site-restricted searches, exports, scheduled monitoring, and search analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, market researchers, academic researchers, SEO teams, and data analysts use this skill to configure and run structured Google Custom Search workflows, export results, and monitor search topics over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to use Google API credentials and search engine IDs.

Mitigation: Provide credentials through environment variables and review generated configuration files so secrets are not hardcoded or exported.

Risk: Optional REST API mode, cron schedules, alert emails, and exports can create persistent or externally visible behavior.

Mitigation: Require explicit user approval before starting API mode, creating scheduled jobs, sending alert emails, or writing exports outside the chosen project folder.

Risk: Search results, generated reports, and automated monitoring may contain incomplete, outdated, or misleading information.

Mitigation: Review search outputs and analysis reports before using them for business, academic, SEO, or data collection decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/google-search-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of keyword files, exported JSON/CSV/Markdown search results, scheduled jobs, local REST API usage, and analysis reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
