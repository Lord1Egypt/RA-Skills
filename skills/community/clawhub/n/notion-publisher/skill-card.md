## Description: <br>
Publish articles to Notion using cached local copies of the target database's default Notion template when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miraclemin](https://clawhub.ai/user/miraclemin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft, create, publish, search, and update article pages in Notion databases through available Notion MCP tools or the bundled CLI runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace existing Notion page content during updates. <br>
Mitigation: Prefer append mode unless the user intentionally wants to replace the whole page body, and confirm replacement before updating existing pages. <br>
Risk: Using the skill requires a Notion integration with read, update, and insert access to workspace content. <br>
Mitigation: Install only for workspaces where that access is acceptable, share only the intended database or parent page with the integration, and keep the token local. <br>
Risk: External cover or inline image searches may expose confidential article topics. <br>
Mitigation: Avoid external image searches for confidential articles and use user-provided or approved image URLs instead. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/miraclemin/notion-publisher) <br>
- [Notion Publisher Template Catalog](artifact/templates/catalog.md) <br>
- [Cached Notion Default Templates](artifact/templates/notion-defaults/catalog.md) <br>
- [Notion API Endpoint](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Notion-flavored Markdown article content, JSON CLI responses, and local configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update Notion pages through MCP tools or the bundled CLI when a Notion integration token and target database access are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
