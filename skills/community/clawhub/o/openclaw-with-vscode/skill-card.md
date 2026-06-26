## Description: <br>
Bridge between OpenClaw and VS Code Copilot - dispatch coding tasks from any OpenClaw channel to VS Code for execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diankourenxia](https://clawhub.ai/user/diankourenxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route OpenClaw coding requests to VS Code Copilot Agent for local code writing, editing, review, and debugging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad coding requests may be passed to Copilot Agent, which can edit files and run commands in the active workspace. <br>
Mitigation: Use the skill only in workspaces where file edits and command execution are acceptable, and review Copilot changes and commands before keeping them. <br>
Risk: Prompts may include secrets, restricted code, or other sensitive content that Copilot processes under the user's Copilot policy. <br>
Mitigation: Avoid sending secrets or restricted code unless the applicable Copilot policy permits it. <br>
Risk: The skill depends on a separate local VS Code extension that receives task prompts through localhost. <br>
Mitigation: Install only if you trust the VS Code extension and verify the local health endpoint before dispatching tasks. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diankourenxia/openclaw-with-vscode) <br>
- [OpenClaw Chat VS Code Marketplace extension](https://marketplace.visualstudio.com/items?itemName=wodeapp.openclaw-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends task prompts to a local VS Code extension endpoint and returns Copilot response text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
