## Description: <br>
Generate videos from text descriptions using ZhipuAI CogVideoX-3, with support for text-to-video, image-to-video, first/last-frame video generation, and multi-segment continuation for videos longer than about five seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baokui](https://clawhub.ai/user/baokui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan, generate, chain, concatenate, and deliver short or multi-segment videos from text prompts or source images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, and continuation frames are sent to ZhipuAI for video generation. <br>
Mitigation: Use the skill only when external processing is acceptable and avoid sensitive prompts or media. <br>
Risk: Video generation can consume provider quota or incur costs through repeated segment generation. <br>
Mitigation: Use a scoped ZhipuAI API key where possible, estimate duration before generation, and monitor provider quota and cost. <br>
Risk: Generated files can exceed messaging or upload limits. <br>
Mitigation: Compress oversized final videos before delivery, as described by the artifact workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baokui/llm-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces video generation plans, progress messages, ZhipuAI task/result JSON files, PNG continuation frames, and MP4 video outputs through bundled scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
