## Description:

Control OctoPrint 3D printer monitoring, webcam snapshots, print management, G-code analysis, and error detection for agent-assisted 3D printing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterhanily](https://clawhub.ai/user/peterhanily)

### License/Terms of Use:


## Use Case:

External users and makers use OctoClaw to let an agent check OctoPrint printer status, inspect job and temperature details, capture webcam snapshots, analyze G-code, upload files, and request print controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real 3D printer, including print, pause, resume, cancel, and temperature actions.

Mitigation: Confirm every print, temperature, pause, resume, and cancel action manually before execution.

Risk: The skill can send printer status, custom messages, and webcam snapshots through Telegram when configured.

Mitigation: Avoid sending sensitive content with Telegram commands and only enable Telegram for approved chats.

Risk: The skill requires an OctoPrint API key and can upload files to the printer.

Mitigation: Use HTTPS for OctoPrint, a least-privileged API key, restricted config file permissions, and known safe directories and G-code files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterhanily/skills/octoclaw-print)
- [Publisher profile](https://clawhub.ai/user/peterhanily)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Terminal text, JSON responses, Markdown guidance, and image files for webcam snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May control printer hardware and send Telegram notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
