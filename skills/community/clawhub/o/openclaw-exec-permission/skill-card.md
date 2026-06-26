## Description: <br>
Guides agents through OpenClaw exec security, approval, and allowlist configuration for command execution permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[embracex1998](https://clawhub.ai/user/embracex1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to understand and adjust OpenClaw exec security, approval behavior, and command allowlists for agent command execution environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Following full access and approval-off guidance can disable OpenClaw command restrictions and approval prompts. <br>
Mitigation: Use the skill only when intentionally changing exec safeguards; prefer allowlist with approvals on shared, production, or sensitive machines. <br>
Risk: Direct configuration edits can persist unsafe exec settings until they are changed back. <br>
Mitigation: Review the exact configuration change, keep a rollback plan, and restart the gateway only after confirming the intended settings. <br>


## Reference(s): <br>
- [OpenClaw Exec Permission on ClawHub](https://clawhub.ai/embracex1998/openclaw-exec-permission) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
