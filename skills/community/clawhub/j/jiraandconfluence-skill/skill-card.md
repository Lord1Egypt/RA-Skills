## Description: <br>
Automates retrieval and summary of Jira Cloud issues and Confluence Cloud pages using secure API tokens for workflow insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arkiant](https://clawhub.ai/user/Arkiant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workflow teams use this skill to retrieve Jira issue details and Confluence page content through Atlassian Cloud APIs, then summarize or inspect project and documentation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Jira and Confluence data through Atlassian API tokens. <br>
Mitigation: Install it only for agents that should access those systems, and use least-privilege read-only tokens by default. <br>
Risk: Comment posting requires broader write permissions and may modify tickets or pages. <br>
Mitigation: Avoid write-scoped tokens unless comment posting is required, and review agent actions before enabling write access. <br>
Risk: Issue keys, page references, and placeholder domains may point to unintended resources if supplied incorrectly. <br>
Mitigation: Replace the placeholder domain carefully and treat unusual issue keys or page references as untrusted input. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Arkiant/jiraandconfluence-skill) <br>
- [Skill README](SKILL.md) <br>
- [Usage Examples](examples/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Atlassian API tokens from environment variables and requires the placeholder Atlassian domain to be replaced before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
