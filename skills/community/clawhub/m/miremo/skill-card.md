## Description: <br>
Access the user's personal Miremo knowledge base to search notes, inspect documents and tags, explore knowledge graph entities, and save new information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansenz42](https://clawhub.ai/user/hansenz42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to work with their own Miremo notes, documents, supertags, workspaces, and knowledge graph through a connected Miremo MCP server. It supports personal knowledge research, exact lookups, workspace-aware browsing, and creating new memos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a user-provided Miremo API key and can access the user's Miremo knowledge base. <br>
Mitigation: Use a dedicated Miremo API key, keep OpenClaw configuration out of untrusted version control and backups, and revoke the key when the skill is no longer needed. <br>
Risk: A misconfigured MCP server URL could send requests or credentials to an unintended endpoint. <br>
Mitigation: Verify that the MCP URL is the official Miremo endpoint or a local server you control before installing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hansenz42/miremo) <br>
- [Publisher profile](https://clawhub.ai/user/hansenz42) <br>
- [Miremo homepage](https://www.miremoapp.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown responses with MCP tool guidance and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Miremo MCP server and user-provided API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
