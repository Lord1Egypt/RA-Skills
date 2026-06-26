## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Notion pages, data sources, and blocks through the Notion API. It provides setup guidance, curl examples, and safety guardrails for scoped access, destructive changes, shared workspace data, and local persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Notion API credential. <br>
Mitigation: Use a dedicated least-privilege Notion integration, grant access only to required pages or data sources, and configure the key through a protected environment variable or secret manager. <br>
Risk: Broad Notion search or page reads can expose personal or shared workspace content. <br>
Mitigation: Access only pages and data sources the user explicitly identifies by name, URL, or ID. <br>
Risk: Bulk, schema-changing, or destructive operations can cause data loss across shared workspaces. <br>
Mitigation: Show affected page titles or record counts and require explicit confirmation before archiving, deleting, modifying schemas, or creating more than five items. <br>
Risk: Saving raw API responses locally can persist sensitive workspace data beyond the session. <br>
Mitigation: Display responses in the terminal by default and ask before writing Notion data to files. <br>


## Reference(s): <br>
- [Notion API Documentation](https://developers.notion.com) <br>
- [Notion integrations setup](https://notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/notion-hardened) <br>
- [Faberlens Notion safety evaluation](https://faberlens.ai/explore/notion) <br>
- [Guardrail feedback](https://github.com/faberlens/hardened-skills/issues/new?template=guardrail-feedback.yml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion API key configured through NOTION_API_KEY or another protected secret mechanism; API responses may contain sensitive workspace content.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
