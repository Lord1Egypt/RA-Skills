## Description: <br>
Notion API integration with managed OAuth for querying databases, searching pages, reading workspace content, and performing confirmed write operations against Notion resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access Notion workspaces through Maton-managed OAuth for search, database queries, page and block reads, and user-approved Notion write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton-managed OAuth and a MATON_API_KEY to access Notion content through a connected account. <br>
Mitigation: Install only when Maton is trusted to broker Notion access, and use the least-privileged Notion connection available for the task. <br>
Risk: Requests may target the wrong Notion workspace or connection when multiple connections are available. <br>
Mitigation: Specify and verify the intended connection before accessing or changing Notion resources. <br>
Risk: Create, update, archive, or delete operations can affect pages, databases, or blocks visible to other workspace users. <br>
Mitigation: Approve writes or deletes only after checking the exact page, database, or block ID and confirming the operation scope. <br>


## Reference(s): <br>
- [ClawHub Notion Skill](https://clawhub.ai/byungkyu/notion-api-skill) <br>
- [Maton](https://maton.ai) <br>
- [Notion API Introduction](https://developers.notion.com/reference/intro) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown guidance with CLI, Python, JavaScript, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Maton-managed Notion OAuth connection.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
