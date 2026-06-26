## Description: <br>
Full multimodal generation via MiniMax CLI (mmx), covering text chat, image generation, video synthesis, TTS speech, music composition, vision analysis, and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariffazil](https://clawhub.ai/user/ariffazil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill as a command reference for generating and analyzing multimodal content with the MiniMax mmx CLI. It helps agents prepare shell commands for text, image, video, speech, music, vision, web search, configuration, and quota workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, audio, files, and search queries may be sent to MiniMax services when using the mmx CLI. <br>
Mitigation: Avoid submitting secrets, sensitive personal data, or proprietary content unless the deployment has approved that data flow. <br>
Risk: Generated or downloaded media can write files to user-selected paths. <br>
Mitigation: Choose output paths deliberately and review generated files before using or publishing them. <br>
Risk: API-key use can affect account security, quota, or billing. <br>
Mitigation: Protect the MiniMax API key, check authentication status, and monitor quota before high-volume generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ariffazil/mmx) <br>
- [Publisher profile](https://clawhub.ai/user/ariffazil) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths, output directories, API authentication, model names, and generated media files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
