## Description: <br>
CLI tool for interacting with Atlassian Jira and Confluence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[festoinc](https://clawhub.ai/user/festoinc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineering teams, and workspace operators use this skill to inspect and manage Jira issues, projects, users, and Confluence pages from an agent-accessible CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real Jira and Confluence changes using the configured Atlassian token. <br>
Mitigation: Use a least-privilege Atlassian account or token and require review before create, update, comment, assign, transition, or Confluence modification commands. <br>
Risk: Broad settings can expose more projects, commands, or Confluence spaces than intended. <br>
Mitigation: Start with read-only or tightly scoped settings, restrict allowed projects, commands, and spaces, and validate settings before applying them. <br>
Risk: The runtime depends on an external npm package. <br>
Mitigation: Verify that the package source is trusted before installation and pin the package version where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/festoinc/jiraandconfluence) <br>
- [jira-ai project repository](https://github.com/festoinc/jira-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe commands that read from or write to Jira and Confluence depending on the user's credentials and configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
