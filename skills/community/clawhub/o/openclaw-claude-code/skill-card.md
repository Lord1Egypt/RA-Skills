## Description: <br>
Control Claude Code via MCP protocol to execute commands, read and write files, search code, and use Claude Code tools programmatically with agent team support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Enderfga](https://clawhub.ai/user/Enderfga) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to control Claude Code for multi-step coding work, code search, file edits, command execution, testing, code review, and coordinated agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give Claude Code broad authority to run commands, edit files, and continue autonomous sessions. <br>
Mitigation: Use plan or default permission modes for sensitive work, restrict allowed tools and added directories, and stop persistent sessions when finished. <br>
Risk: Bypass-style permission settings can remove review points before high-impact tool use. <br>
Mitigation: Avoid bypassPermissions and skip-permissions except in trusted, isolated workspaces with intentionally limited scope. <br>
Risk: Configured MCP servers and process environments can expose more local capabilities or ambient secrets than expected. <br>
Mitigation: Run with a minimal environment, use only trusted and pinned MCP servers, and keep backend URLs local or controlled by the operator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Enderfga/openclaw-claude-code) <br>
- [Publisher profile](https://clawhub.ai/user/Enderfga) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, JSON tool responses, streamed text, and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Claude Code session responses and tool results from configured MCP servers.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
