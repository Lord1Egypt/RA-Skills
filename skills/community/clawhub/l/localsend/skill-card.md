## Description: <br>
Send and receive files to/from nearby devices using the LocalSend protocol with an interactive Telegram menu for device discovery, file sending, text sending, and receiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chordlini](https://clawhub.ai/user/Chordlini) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to move files or text between nearby devices over the LocalSend protocol from a Telegram-style interactive flow. It is intended for trusted local networks where the user controls both the sending and receiving devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-accept nearby LocalSend transfers and save received files into the workspace. <br>
Mitigation: Use receive mode only on trusted local networks and review received files before opening, extracting, installing, previewing, or deploying them. <br>
Risk: The skill depends on an external localsend-cli script for discovery and transfers. <br>
Mitigation: Install the CLI only from a trusted source and keep it available with openssl before using transfer flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chordlini/localsend) <br>
- [localsend-cli repository and documentation](https://github.com/Chordlini/localsend-cli) <br>
- [LocalSend protocol](references/protocol.md) <br>
- [LocalSend protocol repository](https://github.com/localsend/protocol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline JSON button payloads and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires localsend-cli and openssl; uses local network discovery and file-transfer commands.] <br>

## Skill Version(s): <br>
3.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
