## Description: <br>
宠物第一视角视频创作技能。当用户发送宠物视频并希望生成"宠物内心独白"风格的配音视频时激活。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanglinghao01-rakuten](https://clawhub.ai/user/zhanglinghao01-rakuten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and pet owners use this skill to turn pet videos into first-person inner-monologue narration videos. It guides an agent through video analysis, pet body-language interpretation, narration scripting, text-to-speech generation, and ffmpeg-based audio/video merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may require pet videos and pet profile details. <br>
Mitigation: Only provide media and profile details the user is comfortable sharing with the agent and any configured media or speech tools. <br>
Risk: The ffmpeg examples overwrite generated media filenames and may require installing ffmpeg. <br>
Mitigation: Confirm output paths before running commands and approve environment changes such as ffmpeg installation only when desired. <br>


## Reference(s): <br>
- [Pet Body Language Reference](references/pet-body-language.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhanglinghao01-rakuten/pet-video-narration) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with narration text and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce text-to-speech audio segments and a merged MP4 when the agent has suitable media tools and user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
