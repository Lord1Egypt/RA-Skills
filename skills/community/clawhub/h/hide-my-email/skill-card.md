## Description: <br>
Generate Apple Hide My Email addresses from the terminal and copy to clipboard. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[manikal](https://clawhub.ai/user/manikal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External macOS users can use this skill to install and run the hme CLI for creating Apple iCloud+ Hide My Email addresses from a terminal session. It is intended for local, attended use on a signed-in Mac with Terminal Accessibility permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation can fetch runtime hme and AppleScript files that were not included in the reviewed bundle before running code with macOS Accessibility permissions. <br>
Mitigation: Prefer cloning the repository and inspecting hme and hide_my_email.applescript before installation; avoid curl-pipe installation unless the source has been reviewed. <br>
Risk: The tool relies on broad macOS Accessibility automation of System Settings, which can operate on the local GUI and may break when Apple changes the interface. <br>
Mitigation: Run it only in an attended local macOS session, grant Terminal Accessibility only while needed, and revoke the permission after use if continued automation is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manikal/hide-my-email) <br>
- [Project homepage from skill metadata](https://github.com/manikal/hide-my-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The hme CLI prints a masked iCloud email address to stdout, copies the generated address to the clipboard, and prints errors to stderr on failure.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
