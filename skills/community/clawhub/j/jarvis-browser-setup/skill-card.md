## Description: <br>
Setup Jarvis Browser Control System for new users by generating a unique WebSocket auth token, configuring the server, and preparing extension files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evernation](https://clawhub.ai/user/evernation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to package a Jarvis Browser Control setup for a new user or instance, including token generation, server configuration, Chrome extension preparation, and setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup handles a powerful browser-control token and writes it to generated files and terminal output. <br>
Mitigation: Treat the generated folder, config.json, README.md, and terminal output as sensitive secrets; rotate or regenerate the token if it appears in logs or shared files. <br>
Risk: The local WebSocket server and browser extension code are not reviewed by the server evidence. <br>
Mitigation: Review the server and extension code before running the setup, and run the WebSocket server only on a trusted network. <br>
Risk: Anyone with the generated token may be able to control the browser through the configured server. <br>
Mitigation: Do not share the token broadly, restrict access to the server, and regenerate credentials for each user or instance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evernation/jarvis-browser-setup) <br>
- [Publisher Profile](https://clawhub.ai/user/evernation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated configuration and setup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a dated setup folder containing config.json, server files, extension files, and README.md when supporting template files are available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
