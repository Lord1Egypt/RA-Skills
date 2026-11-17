## Description:

聚合搜索专业版 helps agents run multi-engine search workflows with batch queries, custom engine configuration, result export, scheduled searches, and search analytics for professional research and data collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, research teams, marketing teams, SEO specialists, and data analysts use this skill to guide agents through batch web research, SearXNG-backed multi-engine search, export workflows, scheduled monitoring, and search result analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for read and command execution access while describing scheduled or background search and alert workflows.

Mitigation: Review before installing; use a dedicated workspace and explicitly approve exec, pip install, cron, API-server, and email-alert actions.

Risk: Search inputs and outputs may include sensitive or unrelated local information if workspace boundaries are not controlled.

Mitigation: Keep search inputs and outputs away from secrets or unrelated local files, and review exported JSON, CSV, Markdown, logs, and archives before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/internet-search-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, CSV, Markdown, YAML, bash, Python, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to read files, execute commands, configure scheduled searches, start API service mode, and export search results.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
