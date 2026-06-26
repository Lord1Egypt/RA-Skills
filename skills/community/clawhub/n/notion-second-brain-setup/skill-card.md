## Description: <br>
Sets up a Notion Second Brain page with Reading List and Inbox databases, creating them when missing or adopting existing ones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prakhar728](https://clawhub.ai/user/prakhar728) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Notion users and workspace admins use this skill to scaffold a minimal Second Brain workspace with a parent page, a Reading List database, and an Inbox database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move existing Notion databases named Reading List or Inbox under the Second Brain page without a separate confirmation step. <br>
Mitigation: Before running setup, check for existing Reading List or Inbox databases and limit the Notion integration to the intended workspace area. <br>
Risk: The skill modifies the connected Notion workspace by creating or adopting pages and databases. <br>
Mitigation: Run it only in a workspace where these changes are intended and ensure the Notion integration has access only to appropriate pages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/prakhar728/notion-second-brain-setup) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration] <br>
**Output Format:** [Notion MCP tool calls followed by a concise Markdown status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or adopts one Notion page and two child databases; may move existing Reading List or Inbox databases under Second Brain.] <br>

## Skill Version(s): <br>
0.4.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
