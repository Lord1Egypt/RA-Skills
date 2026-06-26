## Description: <br>
OpenClaw Guardian is a security layer plugin for OpenClaw that checks exec, write, and edit tool calls with blacklist rules and LLM-based intent verification before allowing risky operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fatcatMaoFei](https://clawhub.ai/user/fatcatMaoFei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add a safety review layer around potentially destructive shell and file operations. It is intended to catch high-risk actions, verify user intent, and keep a tamper-evident audit trail for matched operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the plugin can read local session history and send recent conversation content plus flagged tool details to a configured LLM provider. <br>
Mitigation: Review the data flow before installing, especially in shared systems or environments with secrets in chats; prefer a version that scopes context to the active session and redacts or minimizes prompt data. <br>
Risk: The server security guidance identifies package path and tsconfig inconsistencies. <br>
Mitigation: Validate the package layout and TypeScript configuration in a test OpenClaw environment before relying on the plugin. <br>


## Reference(s): <br>
- [OpenClaw Guardian README](references/README.md) <br>
- [OpenClaw Guardian ClawHub listing](https://clawhub.ai/fatcatMaoFei/openclaw-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can emit block reasons and audit log records when risky operations are reviewed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
