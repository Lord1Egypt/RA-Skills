## Description: <br>
Personal AI Infrastructure is a broad agent framework that provides the PAI Algorithm, response formats, documentation routing, workflow orchestration, and local tooling for general problem-solving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DurtyDhiana](https://clawhub.ai/user/DurtyDhiana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use PAI as an always-on personal-agent framework for structured task handling, progressive response formatting, documentation routing, PRD workflows, and local automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad personal-agent framework that can govern many interactions and run local commands with limited scoping. <br>
Mitigation: Review the installed files and enable only the workflows and command paths needed for the intended environment before use. <br>
Risk: The security guidance flags memory/logging behavior and USER directory handling as areas that may expose sensitive local context. <br>
Mitigation: Keep secrets out of PRDs, USER templates, and logs; review retained files before sharing or syncing the workspace. <br>
Risk: The security guidance calls out voice notification curls, MCP profile changes, spawned Claude sessions, and autonomous loop commands. <br>
Mitigation: Audit external callbacks, MCP configuration changes, spawned-agent behavior, and loop-mode commands before allowing autonomous execution. <br>


## Reference(s): <br>
- [PAI ClawHub Listing](https://clawhub.ai/DurtyDhiana/pai) <br>
- [DurtyDhiana Publisher Profile](https://clawhub.ai/user/DurtyDhiana) <br>
- [PAI Skill Definition](artifact/SKILL.md) <br>
- [PAI README](artifact/README.md) <br>
- [PAI CLI Reference](artifact/CLI.md) <br>
- [PAI Security System](artifact/PAISECURITYSYSTEM/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progressive, phase-structured agent responses with optional generated files and local command suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
