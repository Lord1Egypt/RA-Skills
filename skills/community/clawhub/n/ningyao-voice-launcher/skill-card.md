## Description: <br>
Install and configure a local browser-based Chinese voice chat launcher with the Ning Yao persona, including one-click Windows launchers, browser speech I/O, screen awareness, and a safe terminal panel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiwannian](https://clawhub.ai/user/jiwannian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install and configure a local Chinese voice companion launcher with browser speech input, browser speech output, optional screen awareness, and a restricted terminal panel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local launcher may send chat text, speech-derived text, screen summaries, and screenshots to the configured model provider. <br>
Mitigation: Use it only on a trusted machine and network, avoid sharing sensitive screens, and configure the model provider and API key deliberately. <br>
Risk: The local web server exposes a terminal-capable panel without authentication. <br>
Mitigation: Verify the service is bound to localhost before use and avoid the terminal panel until authentication and stricter file/path controls are added. <br>
Risk: The server stores and uses an OpenAI API key from local environment configuration. <br>
Mitigation: Keep the .env file local, do not publish secrets, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiwannian/ningyao-voice-launcher) <br>
- [README.md](README.md) <br>
- [voice-chat-local README](assets/voice-chat-local/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local setup instructions for Node.js, OpenAI API key configuration, Windows launch scripts, and browser-based voice chat operation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
