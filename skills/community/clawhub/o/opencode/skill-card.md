## Description: <br>
OpenCode AI helps agents use the opencode CLI/TUI for AI-assisted coding, refactoring, pull request work, and multi-file codebase tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[csuwl](https://clawhub.ai/user/csuwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to delegate complex OpenCode sessions for codebase exploration, refactoring, feature work, PR review and fixes, and session-based follow-up tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenCode can operate on local codebases and propose or perform code changes and shell commands. <br>
Mitigation: Review generated plans, diffs, and commands before applying changes or executing commands. <br>
Risk: The artifact documents privileged install, symlink, chmod/chown, and removal commands that can alter system locations or files. <br>
Mitigation: Run privileged or destructive commands only after confirming the exact paths, permissions, and rollback plan. <br>
Risk: Session sharing, provider authentication, plugins, MCP servers, and remote attachments can expose private code or credentials if misused. <br>
Mitigation: Avoid sharing private sessions, authenticate only with trusted providers, and use plugins, MCP servers, and remote endpoints only from trusted sources. <br>


## Reference(s): <br>
- [OpenCode AI on ClawHub](https://clawhub.ai/csuwl/opencode) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the opencode binary and may require provider authentication before delegated coding workflows can run.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
