## Description: <br>
Notion 工具包基础版 helps agents use the Notion API to search, read, create, query, and update pages, data sources, databases, and blocks for lightweight knowledge-management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage connected Notion workspace content, including searching pages and data sources, reading page blocks, creating database pages, querying data sources, and updating page properties or blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify connected Notion pages and databases. <br>
Mitigation: Use a least-privilege Notion integration, connect only the pages or databases intended for management, and confirm each create or update action before execution. <br>
Risk: The security evidence says the privacy and scoping instructions are unclear for automatic approval. <br>
Mitigation: Treat API-backed Notion operations as external data transfer, review the requested workspace scope before installation, and keep the Notion token out of source control. <br>
Risk: The optional callback_url can send processing results to an external endpoint. <br>
Mitigation: Avoid callback_url unless it points to a trusted endpoint controlled by the user or organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notion-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API calls] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include structured Notion operation results, execution logs, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
