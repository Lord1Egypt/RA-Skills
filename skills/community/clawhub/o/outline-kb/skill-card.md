## Description: <br>
Outline 知识库 API 交互。搜索文档、创建/编辑文档、管理 Collections、列出用户等。当用户需要与 Outline 知识库交互时使用，包括搜索内容、创建文档、查看文档结构、导出文档、管理权限等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1944876825](https://clawhub.ai/user/1944876825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base operators use this skill to search, read, create, update, export, and administer content in an Outline workspace through the Outline API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad workspace and admin-level Outline API power through an API key. <br>
Mitigation: Use the least-privileged Outline API key available and install only when the agent should operate on the target Outline workspace. <br>
Risk: Write, delete, export, invite, share, role, OAuth, group, user, and permission actions can materially change workspace data or access. <br>
Mitigation: Require explicit approval before executing any mutating, exporting, sharing, invitation, role, user, group, OAuth, or permission change. <br>
Risk: Pointing OUTLINE_BASE_URL at the wrong service could expose the API key or send workspace actions to an unintended instance. <br>
Mitigation: Set OUTLINE_BASE_URL only to a trusted Outline instance and verify connectivity with auth.info before other calls. <br>


## Reference(s): <br>
- [Outline API Endpoints Reference](references/api-endpoints.md) <br>
- [Outline OpenAPI specification](https://github.com/outline/openapi/blob/main/spec3.yml) <br>
- [ClawHub skill page](https://clawhub.ai/1944876825/outline-kb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OUTLINE_BASE_URL and OUTLINE_API_KEY environment variables; Outline document content is Markdown.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
