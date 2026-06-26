## Description: <br>
Graph-based memory MCP server with 9 consolidated tools, 8-phase auto-linking, persona tracking, emotional memory, adaptive learning, and knowledge graph entities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide OpenClaw agents in storing, searching, and managing persistent memory, persona signals, knowledge graph entities, reminders, project context, and shared memories through a registered memory MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain personal conversation-derived memory across sessions. <br>
Mitigation: Use it only when persistent memory is acceptable, and avoid storing secrets, credentials, or highly sensitive personal, medical, legal, or financial information. <br>
Risk: Shared memory features may disclose stored content to another user or owner. <br>
Mitigation: Review sharing operations before use and confirm that the intended recipient and content are appropriate. <br>
Risk: The skill depends on an external memory MCP server and user-scoped identifiers. <br>
Mitigation: Confirm the memory MCP server is registered and pass the correct userId for each operation to keep memory scoped to the intended owner. <br>


## Reference(s): <br>
- [Memory MCP ClawHub page](https://clawhub.ai/cyber-bye/memory-mcp-cyber-bye) <br>
- [cyber-bye publisher profile](https://clawhub.ai/user/cyber-bye) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and a registered memory MCP server exposing the documented memory, entity, relation, short-term, project, context, extract, share, and tool-search tools.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
