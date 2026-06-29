## Description: <br>
Notion API integration with managed OAuth for querying databases, searching pages, reading workspace content, and performing confirmed write operations against Notion resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access a user's connected Notion workspace through Maton-managed OAuth, including search, database and data source queries, page and block reads, and user-approved create, update, archive, or delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue write operations that create, update, archive, or delete Notion pages, blocks, databases, or data sources. <br>
Mitigation: Require explicit user confirmation of the exact target resource, intended connection, and reversibility before executing any write operation. <br>
Risk: A user with multiple Notion connections could send a request to the wrong workspace. <br>
Mitigation: Ask for or verify the intended Maton connection ID whenever more than one active Notion connection may exist. <br>
Risk: Bulk updates or edits to shared workspace content may affect collaborators or disrupt workflows. <br>
Mitigation: Limit actions to resources named in the task and require explicit approval for each batch or high-impact operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/skills/notion-api-skill) <br>
- [Maton homepage](https://maton.ai) <br>
- [Notion API Introduction](https://developers.notion.com/reference/intro) <br>
- [Notion LLM Reference](https://developers.notion.com/llms.txt) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, a Notion-Version header, and explicit user confirmation before write operations.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
