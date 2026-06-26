## Description: <br>
Helps agents use the MiniMax CLI (`mmx`) for multimodal generation, vision understanding, text chat, web search, quota checks, configuration, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sswhite](https://clawhub.ai/user/sswhite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install and configure `mmx`, then run MiniMax API tasks for image, video, music, speech, vision, text, and search workflows from an agent-assisted command-line session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill involves MiniMax API credentials, and the security evidence warns that API keys should not be pasted into an AI chat or agent prompt. <br>
Mitigation: Configure credentials directly through a trusted local terminal or secure credential flow, and avoid exposing API keys in prompts, logs, or shared transcripts. <br>
Risk: The skill can send images, documents, media, URLs, and text to MiniMax services for processing. <br>
Mitigation: Do not submit sensitive screenshots, documents, personal media, confidential URLs, or private text unless that processing is intended and permitted. <br>


## Reference(s): <br>
- [MiniMax CLI GitHub Repository](https://github.com/MiniMax-AI/cli) <br>
- [ClawHub Skill Page](https://clawhub.ai/sswhite/mmx-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or retrieval of media files through the external `mmx` CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
