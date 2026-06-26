## Description: <br>
Joan Workflow guides agents through Joan workspace, pod, todo, plan, CLI, MCP, and context synchronization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donny-son](https://clawhub.ai/user/donny-son) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to work with Joan's knowledge and task management system, including workspace initialization, pod authoring, todo and plan handling, MCP access, and local context generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Push, update, archive, and context-generation workflows may affect shared Joan workspace knowledge or local context files. <br>
Mitigation: Confirm the intended Joan account and workspace before use, and review generated CLAUDE.md content plus any pod, todo, or plan changes before pushing or archiving. <br>
Risk: MCP pod retrieval and workspace context generation may expose shared workspace knowledge to the active agent session. <br>
Mitigation: Retrieve only the intended workspace pods and verify that shared knowledge is appropriate for the current project and agent context. <br>


## Reference(s): <br>
- [Joan MCP server](https://joan.land/mcp/joan) <br>
- [ClawHub release page](https://clawhub.ai/donny-son/joan-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
