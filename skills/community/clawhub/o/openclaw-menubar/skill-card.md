## Description: <br>
Enable OpenClaw as a native macOS menu bar app with a quick-access chat popup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prab002](https://clawhub.ai/user/prab002) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users on macOS use this skill to install and run a native menu bar chat popup without opening the full browser dashboard. Developers can also use the included scripts and Electron app assets to customize the icon, window size, shortcut, or gateway connection behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The app reads an OpenClaw gateway token and can access the user's OpenClaw session. <br>
Mitigation: Install only if the publisher is trusted, review token handling before use, and rotate or remove the gateway token if exposure is suspected. <br>
Risk: The security review says token handling and session access are under-secured. <br>
Mitigation: Harden Electron settings, remove raw token logging, validate custom protocol callbacks, and avoid token-in-URL flows before broader deployment. <br>
Risk: Dropped files may be sent through the configured gateway. <br>
Mitigation: Avoid dragging sensitive files into the app unless the configured gateway and publisher are trusted. <br>
Risk: The app stores local configuration and message history under the user's OpenClaw directory. <br>
Mitigation: Disclose saved config and history behavior clearly and let users inspect or delete the files when needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/prab002/openclaw-menubar) <br>
- [menubar package](https://github.com/maxogden/menubar) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript/Electron files, HTML, CSS, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires Node.js and a local OpenClaw gateway] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
