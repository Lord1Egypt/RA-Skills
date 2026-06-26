## Description: <br>
Enables OpenClaw on macOS to send and receive iMessage messages through Messages, including text, images, recent chats, contacts, and optional remote-control commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and macOS automation users use this skill to let an OpenClaw agent send iMessages, inspect recent local Messages conversations, list contacts, and optionally respond to administrator commands sent over iMessage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent local Messages data and send iMessages from the user's Mac. <br>
Mitigation: Install only when this Messages access is expected, keep trusted contacts narrow, require confirmation for non-trusted contacts, and review the local security log after use. <br>
Risk: The optional remote-control channel can execute allowlisted local commands and auto-reply over iMessage without per-command local approval. <br>
Mitigation: Keep remote control disabled unless specifically needed, limit admin_contacts to a small trusted set, retain a restrictive allowed_commands list, and review control.log regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/imessage) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI-oriented text with JSON-style command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local Messages data, send iMessages, write local security and control logs, and execute a small allowlisted set of remote-control commands when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
