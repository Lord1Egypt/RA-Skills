## Description: <br>
Hatsune Miku Monitor provides a desktop system monitor with an animated Hatsune Miku widget, live CPU, memory, disk, and temperature status, edge hiding, opacity controls, and a one-click cleanup action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1173910773](https://clawhub.ai/user/1173910773) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and run a lightweight Linux desktop monitor with an animated Hatsune Miku floating widget. It is intended for local system visibility and optional manual cleanup actions, not unattended system administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-click boost action can interrupt browser work, remove caches, change swap state, and delete recent system logs. <br>
Mitigation: Use the cleanup button only as an intentional system-maintenance action after reviewing the behavior and saving active work. <br>
Risk: Suggested NOPASSWD sudo rules would allow passwordless cache, swap, and journal operations. <br>
Mitigation: Do not add passwordless sudo rules unless the user accepts those privileges and has reviewed the exact commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1173910773/hatsune-miku-monitor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/1173910773) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown installation and usage guidance with shell commands, Python script execution, and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local desktop-monitor setup and operating guidance; runtime behavior is implemented by the bundled GTK Python script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
