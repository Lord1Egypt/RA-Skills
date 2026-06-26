## Description: <br>
Retrieve, analyze, and update Jira tickets directly using MCP-based or direct REST API approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to fetch Jira ticket requirements, extract acceptance criteria, search issues, add progress comments, and transition issue statuses during delivery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable Jira credentials can allow an agent to add comments, create or update issues, and transition statuses. <br>
Mitigation: Use a least-privilege Jira API token and review intended write actions before allowing the agent to apply them. <br>
Risk: Jira API tokens may be exposed if copied into prompts, files, or configuration that is not secret-managed. <br>
Mitigation: Store Jira credentials in environment variables or a secrets manager, never hardcode them, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [Jira Ops on ClawHub](https://clawhub.ai/djc00p/jira-ops) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Jira issue summaries, acceptance criteria analysis, JQL guidance, MCP tool usage, REST API guidance, and proposed ticket updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
