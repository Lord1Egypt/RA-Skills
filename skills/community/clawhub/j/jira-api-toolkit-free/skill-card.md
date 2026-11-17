## Description: <br>
Provides read-only Jira Cloud access for JQL issue search, issue details, project metadata, status metadata, and current-user checks through a CLI-backed OAuth workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and automation agents use this skill to query Jira Cloud issues and metadata for standups, personal task review, project browsing, and read-only workflow checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the free edition claims read-only behavior while metadata or instructions describe broader write-style authority. <br>
Mitigation: Use least-privilege Jira access, review commands before execution, and keep usage to read-only Jira queries unless a separately approved edition is installed. <br>
Risk: The skill relies on Jira account access and may expose project inventory, issue details, cloud IDs, or current-user information. <br>
Mitigation: Avoid broad JQL queries and do not share API keys, OAuth details, cloud IDs, whoami output, or project inventory outside approved contexts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/jira-api-toolkit-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>
- [Skill Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Jira query examples, CLI setup steps, and read-only result handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
