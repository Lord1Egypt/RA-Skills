## Description: <br>
Unified MiniMax media generation skill for audio, image, and video creation through a single command entrypoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmww](https://clawhub.ai/user/nmww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate speech audio, images, and videos with MiniMax cloud APIs from a unified command surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, text for speech, and media references are sent to MiniMax's cloud API. <br>
Mitigation: Avoid confidential prompts or private media references unless cloud processing is approved for the use case. <br>
Risk: The skill requires a MiniMax API key. <br>
Mitigation: Store MINIMAX_API_KEY in the local environment or secret manager and do not hardcode it in source files. <br>
Risk: Generated media files are written to user-selected output paths. <br>
Mitigation: Use non-sensitive output directories where file creation or overwrites would not affect important data. <br>


## Reference(s): <br>
- [MiniMax Skill Setup](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nmww/minimax-skill) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/nmww) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media can include MP3 audio, JPEG images, and MP4 video files written to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
