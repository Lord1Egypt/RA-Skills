## Description: <br>
Install, configure, verify, or troubleshoot the @jwongart/openclaw-minimax-media OpenClaw plugin for MiniMax image understanding, image generation, music generation, video generation, text-to-speech, and web search tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwongpp](https://clawhub.ai/user/junwongpp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, pin, configure, verify, and troubleshoot the MiniMax media plugin and its API-key setup. It supports workflows that expose MiniMax image, music, video, text-to-speech, and web-search tools through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and configures a third-party OpenClaw plugin package. <br>
Mitigation: Prefer the pinned install command and review the referenced package before granting it credentials. <br>
Risk: The plugin requires a MiniMax API key or compatible environment variable. <br>
Mitigation: Use a dedicated or limited key where possible, store it outside source control, and avoid committing real tokens. <br>
Risk: Prompts, media, or generated content may be processed by MiniMax services when the plugin tools are used. <br>
Mitigation: Avoid sending sensitive prompts or media unless the deployment has approved MiniMax processing for that data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/junwongpp/minimax-media-plugin) <br>
- [OpenClaw MiniMax Media plugin repository](https://github.com/jwong-art/openclaw-minimax-media) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package verification commands, plugin-list checks, environment variable names, and migration guidance.] <br>

## Skill Version(s): <br>
0.8.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
