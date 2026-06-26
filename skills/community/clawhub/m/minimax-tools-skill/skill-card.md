## Description: <br>
Direct MiniMax API integration for speech synthesis, voice cloning, image generation, video generation, and music generation using local Python scripts instead of MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cytwyatt](https://clawhub.ai/user/cytwyatt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to call MiniMax multimodal APIs from OpenClaw or shell workflows for text-to-speech, voice cloning, image, video, and music generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, audio, lyrics, and voice samples selected by the user are sent to MiniMax's external service. <br>
Mitigation: Use the skill only for intended MiniMax API workflows, avoid confidential or regulated content, and submit third-party media or voice data only with appropriate authorization and consent. <br>
Risk: The skill depends on a MiniMax API key and can be pointed at an alternate API host through MINIMAX_BASE_URL. <br>
Mitigation: Use a dedicated MiniMax API key when possible, keep credentials out of shared logs, and leave MINIMAX_BASE_URL unset unless the endpoint is trusted. <br>


## Reference(s): <br>
- [MiniMax API Notes](references/api-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cytwyatt/minimax-tools-skill) <br>
- [Project Homepage](https://github.com/cytwyatt/minimax-tools-skill) <br>
- [MiniMax API Base URL](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Local media files, JSON status objects, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the requests package, and MINIMAX_API_KEY; generated prompts, media inputs, lyrics, and voice samples may be sent to MiniMax.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
