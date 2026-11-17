## Description:

Send and receive files to and from nearby devices using the LocalSend protocol through an interactive chat menu for device discovery, file sending, text sending, and receiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chordlini](https://clawhub.ai/user/chordlini)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to discover nearby LocalSend devices and guide local file or text transfers through an interactive chat menu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned external CLI code.

Mitigation: Pin the CLI source to a reviewed version or digest and verify it before installation.

Risk: Receive mode can auto-accept files from nearby network devices into the workspace.

Mitigation: Require explicit approval for each transfer and save received files to a controlled incoming directory.

Risk: Received files may be unsafe to open, extract, install, preview, or deploy.

Mitigation: Treat all received files as untrusted and scan or review them before taking follow-up actions.

Risk: Text payload handling may write user-provided content through temporary files.

Mitigation: Use safe temporary-file handling and avoid shell interpolation of untrusted text.

## Reference(s):

- [LocalSend v2 Protocol Reference](artifact/references/protocol.md)
- [localsend-cli documentation](https://github.com/Chordlini/localsend-cli)
- [LocalSend protocol](https://github.com/localsend/protocol)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON button definitions and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires localsend-cli and openssl; operates over the local network with LocalSend-compatible devices.]

## Skill Version(s):

3.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
