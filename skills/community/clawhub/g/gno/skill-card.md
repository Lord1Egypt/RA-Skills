## Description: <br>
Search local documents, files, notes, and knowledge bases. Index directories, search with BM25/vector/hybrid, get AI answers with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmickel](https://clawhub.ai/user/gmickel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and knowledge workers use this skill to let an agent initialize and maintain local Gno indexes, search local document collections, retrieve cited context, and configure MCP access when persistent document search is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad authority to run gno commands that can index private files or folders. <br>
Mitigation: Use narrow collection paths and exclude secrets, private directories, and unrelated workspaces from indexing. <br>
Risk: The skill can expose a local web UI or install persistent AI integrations. <br>
Mitigation: Avoid broad network interfaces, review MCP installation scope, and enable write tools only when persistent AI-driven file modification is specifically required. <br>
Risk: Publishing workflows can export local content for upload. <br>
Mitigation: Review every publish export before uploading or sharing it. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/gmickel/gno) <br>
- [GNO MCP documentation](https://www.gno.sh/docs/MCP) <br>
- [CLI reference](cli-reference.md) <br>
- [MCP reference](mcp-reference.md) <br>
- [Usage examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, command references, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause an agent to invoke local gno commands, index local files, start a local web UI, install MCP integration, or export publishing artifacts when the user requests those actions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
