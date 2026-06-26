## Description: <br>
OpenClaw Wallpaper turns a Windows Lively Wallpaper desktop into a persistent OpenClaw chat companion with streaming replies, image input, achievements, and saved conversation context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femnn](https://clawhub.ai/user/femnn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and desktop-agent enthusiasts use this skill to run an OpenClaw-powered wallpaper chat companion on Windows via Lively Wallpaper. It supports streamed text chat, optional image messages, achievement tracking, and local conversation persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated local HTTP services are exposed broadly and can receive chat, stream, health, and clear-history requests. <br>
Mitigation: Bind services to 127.0.0.1, restrict CORS to trusted origins, and add authentication before use. <br>
Risk: The skill stores conversation history locally and can forward text or image content to the OpenClaw Gateway. <br>
Mitigation: Use only with data you are comfortable storing locally and sending through the configured OpenClaw Gateway. <br>
Risk: A hardcoded gateway token is present in the bridge server configuration. <br>
Mitigation: Remove or rotate the token and load credentials from a protected local configuration source. <br>
Risk: The bundled UI file server and automatic process restart behavior can broaden the local execution and file-serving surface. <br>
Mitigation: Avoid the unsafe UI server and disable or tightly scope automatic restarts. <br>


## Reference(s): <br>
- [OpenClaw Wallpaper on ClawHub](https://clawhub.ai/femnn/openclaw-wallpaper) <br>
- [Publisher profile: femnn](https://clawhub.ai/user/femnn) <br>
- [Lively Wallpaper](https://github.com/rocksdanister/lively) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JavaScript files, JSON configuration, and streamed text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local HTTP bridge for chat, streaming, health checks, and conversation clearing.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release evidence; changelog top entry is 0.2.0, released 2026-03-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
