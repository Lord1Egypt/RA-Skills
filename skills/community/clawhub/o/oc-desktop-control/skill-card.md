## Description:

Remote desktop control and automation. Capture screenshots, control mouse and keyboard, automate UI interactions. Supports VNC, RDP, and local desktop environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect and control desktop sessions for UI automation, testing, server administration, and data-entry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the active desktop, capture screenshots, type into applications, and open or close apps.

Mitigation: Install it only when that control is intended; prefer a VM or test account and keep sensitive windows and secrets out of the session.

Risk: The skill can read and write local files as the running user.

Mitigation: Run it with a constrained account or workspace and review automation scripts before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, images, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, CLI commands, Python examples, automation scripts, text status output, file content, and base64 PNG screenshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May act on the active desktop and local filesystem using the privileges of the running user.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
