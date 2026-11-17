## Description:

Provision and control Orgo cloud computers using the orgo_client Python SDK for remote desktops, browser automation, remote Bash or Python execution, UI interaction, file management, and streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohenyehonatan](https://clawhub.ai/user/cohenyehonatan)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to provision Orgo cloud desktops, automate browser and UI workflows, run remote Bash or Python, transfer files, capture screenshots, and manage computer lifecycle or streaming tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent operate Orgo cloud desktops, execute remote Bash or Python, and interact with remote UI state.

Mitigation: Install only when remote desktop control is intended, use a scoped ORGO_API_KEY when available, and review high-impact actions before execution.

Risk: The skill supports local file upload and remote file export, which can expose sensitive files if broad paths or secrets are selected.

Mitigation: Approve uploads explicitly, avoid secrets and broad directories, and review exported files and signed download URLs before sharing.

Risk: The skill can access VNC credentials and control streaming for remote computers.

Mitigation: Handle VNC passwords as secrets, share them only with intended operators, and stop streaming when it is no longer needed.

Risk: Computers and workspaces can continue running or be deleted irreversibly through lifecycle operations.

Mitigation: Stop or delete remote computers when finished, and require explicit approval before destructive delete operations.

## Reference(s):

- [ORGO_ACTION_PATTERNS.md](references/ORGO_ACTION_PATTERNS.md)
- [ClawHub skill page](https://clawhub.ai/cohenyehonatan/skills/orgo-desktop-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API-client usage examples, lifecycle guidance, file-transfer steps, and remote execution patterns.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
