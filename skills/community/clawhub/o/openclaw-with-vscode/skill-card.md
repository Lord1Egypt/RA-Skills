## Description:

Bridge between OpenClaw and VS Code Copilot - dispatch coding tasks from any OpenClaw channel to VS Code for execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diankourenxia](https://clawhub.ai/user/diankourenxia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route OpenClaw coding requests to VS Code Copilot for writing, editing, reviewing, or debugging code in a local VS Code workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can delegate broad coding actions to VS Code Copilot Agent mode, including file edits and command execution.

Mitigation: Use the skill only in trusted workspaces and require explicit user confirmation before edits, deletions, or command execution.

Risk: Coding prompts and potentially code context may be processed through Copilot/GitHub services.

Mitigation: Avoid prompts that contain secrets, credentials, private keys, or sensitive proprietary material.

Risk: The local bridge exposes a localhost trigger endpoint with unclear scoping safeguards.

Mitigation: Run the VS Code extension only when needed, verify the health endpoint before use, and install only from a trusted extension publisher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diankourenxia/skills/openclaw-with-vscode)
- [OpenClaw Chat VS Code Marketplace listing](https://marketplace.visualstudio.com/items?itemName=wodeapp.openclaw-chat)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VS Code, the OpenClaw Chat extension, curl, and a local service on 127.0.0.1:19836.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
