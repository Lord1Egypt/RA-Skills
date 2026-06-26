## Description: <br>
Operate Google Workspace from one CLI using dynamic API discovery, secure OAuth flows, and agent-ready automation patterns for Drive and Gmail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and workspace administrators use this skill to plan and run Google Workspace CLI workflows with schema-first command discovery, explicit account routing, MCP exposure, and change control for Drive, Gmail, Calendar, and related APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps operate Google Workspace through a CLI with access to sensitive account and tenant data. <br>
Mitigation: Use minimum OAuth scopes, verify account and tenant context before each operation, and keep credentials or secrets out of chat. <br>
Risk: Write-capable commands can send, share, update, or delete Google Workspace data. <br>
Mitigation: Prefer inspect or dry-run mode, resolve stable object identifiers, document expected side effects, and require explicit confirmation before apply mode. <br>
Risk: Exposing Google Workspace APIs through MCP can create a broad tool surface for an agent. <br>
Mitigation: Limit MCP service exposure to the current task, split profiles when tool counts grow, and keep write-capable services disabled for read-only investigations. <br>
Risk: Large list operations can trigger excessive API calls or produce noisy outputs. <br>
Mitigation: Use bounded pagination, stream structured output through filters such as jq, and avoid unbounded page-all workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/google-workspace-cli) <br>
- [Skill homepage](https://clawic.com/skills/google-workspace-cli) <br>
- [Google APIs discovery endpoint](https://www.googleapis.com/discovery/v1/apis) <br>
- [Google OAuth authorization](https://accounts.google.com) <br>
- [Google OAuth token service](https://oauth2.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON command arguments, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on schema inspection, dry-run planning, explicit confirmation, and safe execution boundaries for Google Workspace operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
