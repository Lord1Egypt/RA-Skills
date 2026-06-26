## Description: <br>
Remote Windows desktop control from WSL/Linux via screenshot + mouse/keyboard simulation. Use when the user asks to control their PC, click something, open an app, interact with a GUI program, take a screenshot, or perform desktop automation that has no CLI alternative. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron-G](https://clawhub.ai/user/zeron-G) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to operate a local Windows desktop from WSL/Linux for GUI-only tasks, using screenshots to inspect state and mouse or keyboard actions to interact with applications. It is not intended for tasks that have a reliable CLI or PowerShell alternative. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad live Windows desktop control and can expose the active screen through screenshots. <br>
Mitigation: Install only when this capability is intended, close sensitive windows first, verify each action with a follow-up screenshot, and stop the server when finished. <br>
Risk: Authentication tokens and temporary screenshots can grant access to desktop control context or screen contents if mishandled. <br>
Mitigation: Keep the service bound to localhost, protect or delete the token and temporary screenshots, and avoid using the skill while sensitive content is visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zeron-G/pc-control) <br>
- [Publisher profile](https://clawhub.ai/user/zeron-G) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; runtime use may produce screenshot file paths and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshots are scaled by default; action coordinates must be adjusted to the chosen screenshot scale.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
