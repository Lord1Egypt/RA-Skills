## Description: <br>
Provision and control Orgo cloud computers using the orgo_client Python SDK. Use when launching remote desktops, automating browsers, running bash/python remotely, interacting with UI, managing files, or controlling streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohenyehonatan](https://clawhub.ai/user/cohenyehonatan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to provision Orgo cloud desktops, run remote bash or Python, automate browser and UI workflows, capture screenshots, manage files, stream desktops, and stop or clean up remote computers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Orgo API key and can retrieve sensitive remote-desktop credentials or signed download URLs. <br>
Mitigation: Use a limited, rotatable ORGO_API_KEY and avoid printing, logging, or sharing API keys, VNC passwords, screenshots, signed URLs, and real login credentials. <br>
Risk: Remote commands, file transfers, streaming, and desktop automation can expose or modify data in the cloud computer. <br>
Mitigation: Confirm uploads, downloads, streaming, remote command execution, and credential entry before allowing an agent to perform them. <br>
Risk: Delete operations for workspaces, computers, and files are destructive. <br>
Mitigation: Require explicit user confirmation for deletes and prefer stopping computers when the session may continue later. <br>
Risk: UI automation can act on stale or misread screen state. <br>
Mitigation: Use a screenshot-driven loop, wait for UI state changes, and verify state after clicks, typing, scrolling, and navigation. <br>


## Reference(s): <br>
- [ORGO_ACTION_PATTERNS.md](references/ORGO_ACTION_PATTERNS.md) <br>
- [ClawHub skill page](https://clawhub.ai/cohenyehonatan/orgo-desktop-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access and ORGO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
